# GitHub PR부터 Hindsight 게시까지: 평가자 재현 가이드

> **구현 상태:** GitHub PR의 CI 검증과 사람의 Merge, 로컬 수동 Publisher는 구현됨. PR Merge 이후 Hindsight 자동 게시는 **미구현**이며 [`AUTOMATION_DESIGN.md`](AUTOMATION_DESIGN.md)에 별도로 설계함.
>
> **중요:** ZIP 압축 해제본은 **코드 테스트용**이다. `scripts/reconcile.py`는 **승인된 Git `main`과 원격 저장소를 검증**하므로, 게시 실습은 반드시 실제 GitHub **clone/Fork**에서 실행해야 한다. 단순히 ZIP 폴더에서 `git init`하는 방식으로 대체할 수 없다.

## 0. 무엇을 재현하는가

| 범위 | 사전 준비 | 실제 수행 가능 작업 | 미검증·미구현 영역 |
|---|---|---|---|
| A: ZIP 코드 검사 | Python 3.12 | YAML Schema, 단위 테스트 36개, 예제 출력 | Hindsight·Agent를 새로 호출하지 않음 |
| B: GitHub 협업 | 자신의 공개 Fork, GitHub 계정 | 분기·PR·Actions·사람의 검토/병합 | 본인 Merge는 독립 제3자 승인이 아님 |
| C: 로컬 Hindsight 동기화 | B의 Git clone, Docker/LLM 키 | 승인 main snapshot → 로컬 Bank 게시 → Recall | 사용자별 ACL·자동 게시·독립 Agent의 새 실행은 포함하지 않음 |

원본 실험 PR은 [`team-agent-knowledge` #5](https://github.com/5jyan/team-agent-knowledge/pull/5)와 [#6](https://github.com/5jyan/team-agent-knowledge/pull/6)에 보존되어 있다. 제출용 `team-agent-knowledge-showcase`를 Fork하면 **과거 PR 기록까지 복사되지는 않는다.** 다음 단계는 평가자 자신의 **새 PR 워크플로를 검증**하기 위한 실습이다.

## 1. A 경로 — ZIP에서 코드만 검증

ZIP 압축 해제 후 프로젝트 루트에서 실행한다. Git 저장소나 Hindsight 서버가 없어도 된다.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate.py knowledge
python -m unittest discover -s tests -v
python -m unittest discover -s examples/config-validation -p 'test_*.py' -v
(cd experiments/config-agent-b && python -m unittest discover -s tests -p 'test_*.py' -v)
python -m unittest discover -s experiments/blind-discovery -p 'test_*.py' -v
python examples/config-validation/run_demo.py
```

정상 기대값: YAML 1건, 21+5+5+5=36개 테스트 통과. 모든 테스트가 라이브 Hindsight E2E를 뜻하지는 않는다.

**이후 게시까지 확인하려면 2절의 Fork/clone으로 작업 디렉터리를 전환한다.** ZIP 폴더에서 게시 명령을 계속 실행하지 않는다.

## 2. B 경로 — 개인 Fork에서 실제 PR 재현

1. [제출용 공개 저장소](https://github.com/5jyan/team-agent-knowledge-showcase)에서 **Fork**를 클릭하고 소유자를 자신의 GitHub 계정으로 선택한다.
2. 아래 `YOUR_GITHUB_ID`를 자신의 계정으로 바꾸고 **Fork를 clone**한다.

```bash
export GITHUB_USER=YOUR_GITHUB_ID
git clone "https://github.com/$GITHUB_USER/team-agent-knowledge-showcase.git"
cd team-agent-knowledge-showcase
git remote -v
git switch -c demo/review-date
```

3. `knowledge/COMP-015.yaml`의 `maintenance.review_after`를 적절한 미래 날짜로 변경한다. **기존 근거 커밋이나 검증 결과를 임의로 수정하지 않는다.**
4. 아래 검사 후 커밋·Push 한다.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate.py knowledge
git add knowledge/COMP-015.yaml
git commit -m "docs: update knowledge review date"
git push -u origin demo/review-date
```

5. GitHub에서 **base: 내 Fork의 `main`**, compare: `demo/review-date`로 새 Pull Request를 만든다. 원본 작성자의 저장소에 PR을 보내지 않아도 된다.
6. Fork에서 Actions가 비활성화되어 있다면 활성화하고, `validate-knowledge` 검사 결과를 확인한다. Diff와 근거를 사람이 검토한 후 Merge한다. **자기 PR을 본인이 Merge하는 시연은 독립된 제3자 승인과 다르다.**
7. 운영팀 도입 시에는 `main`에 PR 필수, 필수 검사, 강제 Push 금지, 리뷰어 1명 이상 등의 보호 규칙을 적용하고 자신의 GitHub 플랜에서 실제 강제가 가능한지 확인한다. 외부 기여자의 PR에 Publisher 비밀값을 노출하지 않는다.

새 PR은 *날짜 변경을 통한 승인 경로 시연*이며 새로운 bugfix나 Agent의 자동 분류 성공을 증명하지 않는다.

## 3. C 경로 — Hindsight 1.1.0 로컬 설치

아래는 공개 공식 Docker 설치 방식을 **1.1.0 버전으로 고정한 재현 예시**다. Docker Desktop, 외부 LLM 제공자 API 키, 모델 비용과 최초 이미지 다운로드가 필요하다. 이 세션에서는 **깨끗한 Mac에서 새 Hindsight 인스턴스를 직접 재설치해 E2E 검증한 것이 아니므로**, 환경별 문제는 공식 [설치](https://hindsight.vectorize.io/developer/installation)·[설정](https://hindsight.vectorize.io/developer/configuration) 문서를 참고한다.

API 키는 저장소나 쉘 스크립트에 기록하지 않는다. 터미널 세션에 `OPENAI_API_KEY`가 설정된 상태를 전제로 한다. 모델은 사용하는 계정에 접근 가능한 이름으로 조정할 수 있다.

```bash
# 환경에 OpenAI API 키가 준비되어 있는지 먼저 확인 (키 값은 출력하지 않음)
test -n "${OPENAI_API_KEY:-}" && echo 'API 키 설정 확인' || echo 'OPENAI_API_KEY를 먼저 설정하세요 (현재 미설정)'

docker run -d --name team-knowledge-hindsight --shm-size=1g \
  -p 127.0.0.1:8888:8888 -p 127.0.0.1:9999:9999 \
  -e HINDSIGHT_API_LLM_PROVIDER=openai \
  -e HINDSIGHT_API_LLM_API_KEY="$OPENAI_API_KEY" \
  -e HINDSIGHT_API_LLM_MODEL=gpt-4o-mini \
  -v team-knowledge-hindsight-data:/home/hindsight/.pg0 \
  ghcr.io/vectorize-io/hindsight:1.1.0

# 서버 API·데이터베이스 준비가 끝났는지 확인
curl -fsS http://127.0.0.1:8888/health
curl -fsS http://127.0.0.1:8888/version
# 브라우저 UI: http://127.0.0.1:9999
```

컨테이너를 재시작할 때는 `docker start team-knowledge-hindsight`, 로그는 `docker logs team-knowledge-hindsight`를 사용한다. 위 예시는 호스트에서 loopback만 공개하며 프로덕션 인증·TLS 설정을 대신하지 않는다.

### Bank 이름 구분

| Bank | 용도 |
|---|---|
| `team-compiler` | 과거 원본 실험에서 사용한 Bank |
| `team-knowledge-showcase` | 작성자의 최신 제출용 Bank. 첨부된 v2 Recall 화면에 표시됨 |
| `team-knowledge-repro` | **평가자 Fork 재현용 새 Bank**. 작성자의 기존 Bank를 덮어쓰지 않음 |

다음은 **C 경로에서만** 실행한다. ZIP에서 실행하지 않는다.

```bash
export HINDSIGHT_API_URL=http://127.0.0.1:8888
export REPRO_BANK=team-knowledge-repro
curl -fsS -X PUT "$HINDSIGHT_API_URL/v1/default/banks/$REPRO_BANK" \
  -H 'Content-Type: application/json' -d '{"name":"team-knowledge-repro"}'
```

## 4. 승인된 Git `main`을 Hindsight에 수동 게시

**2절의 자신의 Fork clone 루트**에서 작업한다. `origin`이 자신의 Fork URL이고 `main`의 최신 Commit이 원격 `origin/main`과 일치해야 한다. 테스트용 Branch의 커밋을 직접 게시하지 않는다.

```bash
# ZIP 디렉터리가 아니라 git clone 루트에서 실행
git switch main
git fetch origin
git pull --ff-only origin main
git status --short
git rev-parse HEAD

# 먼저 계획만 조회 (이 단계도 로컬 Hindsight 연결이 필요함)
python scripts/reconcile.py \
  --snapshot-commit "$(git rev-parse HEAD)" \
  --source-repository "$GITHUB_USER/team-agent-knowledge-showcase" \
  --bank-id "$REPRO_BANK" \
  --api-url "$HINDSIGHT_API_URL" \
  --dry-run

# 계획 확인 후, 동일한 승인 Snapshot을 실제 게시
python scripts/reconcile.py \
  --snapshot-commit "$(git rev-parse HEAD)" \
  --source-repository "$GITHUB_USER/team-agent-knowledge-showcase" \
  --bank-id "$REPRO_BANK" \
  --api-url "$HINDSIGHT_API_URL"
```

`reconcile.py`는 **현재 원격 main SHA, 로컬 main SHA, 추적 파일의 변경 여부, source_repository 소유권, YAML 유효성**을 확인한다. 조건에 맞지 않으면 게시를 거절한다. 그래서 ZIP 해제본이나 임의의 로컬 Git 초기화 폴더에서는 게시를 재현할 수 없다. 수동 게시 결과는 실제 서버 응답과 Recall을 별도로 확인해야 한다.

## 5. 게시·검색 확인

```bash
# 게시된 문서의 ID와 메타데이터 확인
curl -fsS "$HINDSIGHT_API_URL/v1/default/banks/$REPRO_BANK/documents"

# 메모리 Recall (검색 내용/순위는 모델 및 실행 환경에 따라 달라질 수 있음)
curl -fsS -X POST "$HINDSIGHT_API_URL/v1/default/banks/$REPRO_BANK/memories/recall" \
  -H 'Content-Type: application/json' \
  -d '{"query":"COMP-015 v2 model version 설정 누락"}'
```

기대 확인 항목: `COMP-015` 문서, 현재 제출 Fork의 source_repository와 게시 snapshot, `model`·`version` 필수 조건을 반영한 검색 결과. 4건이라는 검색 수는 과거 스크린샷의 관찰이며 새 서버에 동일 수가 나온다는 보장은 없다. **Hindsight 자체 Recall이 성공한 것과 Codex Agent가 원본 검증까지 성공했다는 것은 별개**다.

## 6. 흔한 오류와 안전 경계

- `git rev-parse ...` 실패: ZIP 압축 해제본이므로 **2절 Fork clone**에서 실행한다.
- `origin` 불일치: `--source-repository`에 실제 Fork의 `<owner>/team-agent-knowledge-showcase`를 사용한다.
- `snapshot is not the current main`: `git switch main && git fetch origin && git pull --ff-only origin main` 후 다시 시도한다.
- `127.0.0.1:8888` 연결 실패: `docker ps`, `docker logs team-knowledge-hindsight`, `/health` 응답 확인.
- LLM/Embedding 초기화 실패: API 키·모델 접근 권한·메모리·이미지 버전 점검. API 키·회사 기밀을 로그나 공유 자료에 붙이지 않는다.
- Fork의 Actions가 실행되지 않음: GitHub Actions 활성화 여부와 워크플로 권한 확인.
- **보안:** 로컬 Bank 이름은 논리적 구분이다. 이 프로젝트는 인증 헤더·Bank별 ACL·독립 리뷰 강제·머지 후 자동 게시를 구현했다고 주장하지 않는다.

## 7. 운영 자동화는 별도 설계

[자동 게시 상세 설계](AUTOMATION_DESIGN.md)를 참고한다. 현재는 **PR CI 자동화까지만 구현**했고, `main`의 게시 API 호출은 운영자가 로컬에서 수동으로 수행한다.
