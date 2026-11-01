# GitHub PR Merge → Hindsight API 자동 게시 확장 설계 (미구현)

> **상태 표기:** 이 문서는 향후 구현할 자동화 설계다. 현재 코드에는 GitHub `push(main)` 자동 게시 Workflow와 서버 인증 처리, 운영용 실패 알림이 없다. 검증 완료된 기능은 PR 단계의 `validate-knowledge` CI와 **로컬 수동 `scripts/reconcile.py`**다.
>
> **평가자 실습:** Fork·PR·수동 게시의 재현 명령은 [`GITHUB_SETUP.md`](GITHUB_SETUP.md)에 있다.

## 1. 목표와 책임 분리

```text
Contributor/Codex Skill --지식 YAML 및 근거--> GitHub PR
GitHub CI --schema+unit tests--> 상태 검사
Human reviewer --Diff/근거 검토, Merge--> 보호된 main
main push event --(향후) trusted Publisher Workflow--> 고정 main SHA 확인
Publisher --관리 대상 비교, 검증--> Hindsight REST API
Hindsight --Retain/Replace/Delete--> Team Bank
Publisher --게시 응답 + 후속 Recall 확인--> 감사 로그 및 실패 알림
```

- **승인의 경계:** 미병합 PR이나 `Approve`만으로는 Team Bank에 쓰지 않는다. Merge로 실제 `main`이 변경되어야 게시 대상이 된다.
- **원본:** Git `main`의 YAML만 권위 있는 지식이다. Hindsight 기억은 검색용 파생 데이터다.
- **권한:** PR 검증 Job에는 게시 비밀값이 없어야 한다. Publisher만 쓰기 권한을 갖도록 별도 서버·비밀 관리가 필요하다.
- **지식 최신성:** Hindsight 교체는 기존 Agent 대화·개인 기억 캐시를 자동 정정하지 않는다. Agent의 최신 원본 확인은 별도 검증 책임이다.

## 2. 단계별 운영 선택

| 옵션 | 실행 주체 | 네트워크 | 상태/제약 |
|---|---|---|---|
| A. 수동 실행 | 운영자의 로컬 터미널 | 로컬 API `127.0.0.1:8888` | **구현됨**. Merge 후 사람이 실행. 배포 지연 가능 |
| B. 로컬 주기 동기화 | 신뢰된 Mac의 `launchd`/전용 스케줄러 | 로컬 API | **미구현**. Mac 종료 시 중단; 실행 중복·오류 알림 필요 |
| C. Merge 트리거 자동화 | GitHub Actions의 별도 신뢰 작업 | HTTPS 서버 또는 격리된 접근망 | **미구현**. 인증/네트워크/경쟁 상태 처리가 필요 |

**중요:** GitHub-hosted Runner는 작성자의 Mac `localhost`에 접속할 수 없다. 로컬 Self-hosted Runner를 공개 저장소의 외부 PR 코드와 함께 실행하면 공격면이 생긴다. 따라서 CI와 게시 작업의 권한·실행 환경을 강하게 분리해야 한다.

## 3. 구체적인 GitHub 설정 및 Workflow 트리거

1. `main` PR 필수/상태 검사 필수/강제 Push 차단/리뷰 정책을 적용한다. 소유자 자기 PR 병합은 독립 리뷰가 아니며, 개인 저장소의 실제 보호 기능 강제 가능 여부는 GitHub 플랜과 설정에서 검증한다.
2. 기존 `.github/workflows/validate.yml`은 PR에서 **스키마·테스트만** 수행하고 Secret을 사용하지 않는다.
3. 향후 `.github/workflows/publish.yml`은 오직 보호된 `main`의 `push` 및 승인된 수동 `workflow_dispatch`를 허용한다. `pull_request_target`에서 PR 코드를 체크아웃하거나 Secret과 함께 실행하지 않는다.
4. `contents: read`, 고정된 의존성/Action 버전, 게시 전용 Environment, 비밀값 마스킹, 작업 동시성 제어를 설정한다.

아래 예시는 **개발 방향을 보여주는 의사 구성**이다. 인증 기능과 신뢰 실행 환경이 없는 현재 ZIP에 그대로 저장해 동작한다고 주장하거나 배포해서는 안 된다.

```yaml
# DESIGN ONLY — DO NOT DEPLOY without verified credentials/network and safety gates
name: publish-team-knowledge
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: team-knowledge-publish
  cancel-in-progress: false
jobs:
  publish:
    runs-on: ubuntu-latest   # Hindsight가 인증된 HTTPS로 접근될 때만 사용
    environment: knowledge-publisher
    steps:
      - uses: actions/checkout@v4  # 운영에서는 사용 SHA pinning 권장
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m pip install -r requirements.txt
      - run: python scripts/validate.py knowledge
      # 여기는 인증·접근성·최신 HEAD 보장 검증을 통과한 후에만 구현할 자리
      # publisher HTTP Client의 인증 헤더 지원은 현재 코드에 없음
      # run: python scripts/reconcile.py --snapshot-commit "$(git rev-parse HEAD)" ...
```

## 4. Publisher API 계약 및 구현 전제

Hindsight 1.1.0 기준 REST API를 사용하며, 현재 `scripts/reconcile.py`는 다음 기능을 가지고 있다.

| 작업 | REST API | 현재 코드 동작 |
|---|---|---|
| 문서 목록 조회 | `GET /v1/default/banks/{bank_id}/documents` | 구현됨. `document_metadata`의 관리 출처 확인 |
| 신규/갱신 | `POST /v1/default/banks/{bank_id}/memories` | 구현됨. `document_id` 고정, 동기 Retain. `update_mode`를 생략하며 Hindsight의 기본값이 `replace` |
| 폐기 | `DELETE /v1/default/banks/{bank_id}/documents/{document_id}` | 구현됨. 승인 스냅샷에서 retired 또는 관리 대상 누락 판정 |
| 검색 확인 | `POST /v1/default/banks/{bank_id}/memories/recall` | 현재 CLI Publisher의 필수 검증 단계는 아님. 운영 확장 시 별도 확인/알림 추가 필요 |

**정확한 한계:** 현재 HTTP Client에는 서버용 `Authorization` 헤더, 게시용 Secret 지원, HTTP 429/5xx 자동 backoff 재시도, 분산 Lock이 없다. 따라서 인터넷에서 접근할 수 있는 Hindsight에 바로 연결하는 운용 설계는 현재 구현으로 충족되지 않는다. 자동화 전에 인증/권한 코드와 테스트를 추가해야 한다.

### 게시 불변조건

- `snapshot_commit`은 승인된 Git `main`의 실제 SHA와 일치해야 한다.
- `origin/main`, 원격 GitHub HEAD와 로컬 `main`이 일치하고, 추적 파일에 커밋되지 않은 변경이 없어야 한다.
- 모든 지식 YAML 및 Schema가 유효해야 하며, **관리 소유권 (`managed_by`, `source_repository`)이 정확히 일치하는 문서만** 변경한다.
- 동일 `document_id`는 전체 문서 대체를 사용한다. 동시 실행 시 오래된 Snapshot이 최신 것을 덮지 않게 실행을 직렬화하고 게시 전후 HEAD를 재확인한다.
- 부분 성공 뒤 실패한 경우 전체 성공으로 기록하지 않고 최신 승인된 스냅샷을 기준으로 재실행한다. 특히 삭제 예정 문서는 `--dry-run` 및 소유권·범위를 확인한다.

## 5. 추가 구현 우선순위

1. **인증:** API 토큰/HTTPS 연결, 서버 권한 분리, `Authorization` 헤더, 안전한 비밀값 취급, 401/403 즉시 실패 테스트.
2. **연결:** 운영자가 관리하는 HTTPS Hindsight 또는 PR 코드와 분리된 신뢰 실행기 확보. 인터넷 공개 서버에는 인증·네트워크 통제 적용.
3. **내구성:** Rate Limit/서버 오류 재시도, 타임아웃, 멱등 게시, 최신 HEAD 확인, 분산 Lock 또는 단일 Writer 보장, 실패 알림/감사 로그.
4. **CI 정책:** 신뢰된 `main`만 게시, PR 검증과 Publisher 권한 분리, 직접 Push 차단 여부 확인, 동시 Merge 순서 역전 테스트.
5. **신뢰성 검증:** 재사용 Agent의 원본 Git 재검증, 퇴역 지식의 삭제 후 fresh Recall, 기존 세션의 오래된 문맥을 별도 처리.

## 6. 자동화 완료로 인정할 실험

| 시나리오 | 기대 결과 |
|---|---|
| PR 생성, 아직 Merge 안 됨 | Team Bank 불변 |
| Merge 후 push(main) | 승인된 COMP-015가 동일 ID로 게시되고 source SHA 기록 |
| 다음 Merge에서 동일 ID 갱신 | 문서 하나를 교체하고 최신 적용 조건 검색 가능 |
| retired로 Merge | 관리 소유권 일치 문서만 제거 |
| LLM/HTTP 장애 | 실패 상태와 원본 SHA 기록, 성공으로 오인하지 않음 |
| 빠르게 두 번 Merge | 최종 main 기준 상태로 수렴, 이전 동작이 최신 지식을 덮지 않음 |
| 인증 실패/무권한 PR | 게시 거부, Secret 미노출 |

자동화 통합 테스트에서는 PR URL, CI Run URL, 게시 Job/Run, 요청 문서 ID, HTTP 응답, 현재 Bank 검색 결과를 함께 보존한다. **이번 제출물은 이 자동화 완료 테스트를 실행했다고 주장하지 않는다.**

## 7. 자료

- [Hindsight 1.1.0 REST API](https://hindsight.vectorize.io/api-reference)
- [Retain / 갱신](https://hindsight.vectorize.io/developer/api/retain)
- [Document 조회·삭제](https://hindsight.vectorize.io/developer/api/documents)
- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
