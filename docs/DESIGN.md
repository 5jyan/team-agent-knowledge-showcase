# 팀 Agent 지식 저장소 설계

## 과제 요구사항에서 기능을 도출한 이유

**선택 기준:** Hindsight가 제공하는 기억 저장·추출·Recall·문서 교체/삭제를 재구현하지 않는다. 이번 과제에서 별도로 필요한 것은 **공유 자격 판단, 재현 가능한 근거, 사람의 승인, 승인 원본의 생명주기 관리**다. 따라서 Git `main`의 승인된 YAML을 기준 원본으로 삼고 Hindsight를 파생 검색 저장소로 사용한다.

| 과제 요구사항 | 기존 오픈소스 기능 | 직접 추가한 기능·이유 | 구현 상태 |
|---|---|---|---|
| 개인 기억과 팀 지식 구분 | Hindsight Bank 저장·검색 | 분류 정책과 Codex `share-knowledge` Skill로 미검증 기록을 후보 PR과 분리 | 정책·Skill 구현; Bank ACL 미검증 |
| 검증·적용 범위 관리 | Git Commit 및 변경 이력 | YAML에 근거·적용 조건·예외·담당자 명시, `validate.py`와 CI 검증 | 구조 검증 구현; 내용의 타당성은 사람 검토 |
| 공유 승인과 원본 추적 | GitHub PR·Actions | Agent는 제안, 사람은 diff/근거 검토 및 Merge; 병합된 `main`만 게시 | 워크플로 구현; 독립 리뷰 강제 미구현 |
| 다른 Agent의 지식 활용 | Hindsight Recall/MCP | 검색 결과의 지식 ID·최신 Git 상태·적용 범위를 다시 검증하도록 Agent 지침 작성 | Agent B 사례 검증; 서버 강제 아님 |
| 지식 변경·폐기 | Hindsight 문서 교체·삭제 API | 동일 ID의 v1→v2 PR과 `reconcile.py` 수동 게시; retired 처리 | 수동 게시 구현; 열린 세션 기억 자동 갱신 미검증 |
| 장기 관리·자동화 | Git 이력, GitHub 이벤트, Hindsight API | owner/review_after/update_trigger 필드; Merge 후 자동 Publisher 및 인증 경계 설계 | 운영 필드 구현, 자동 게시·ACL은 후속 설계 |

**구현과 재사용의 경계:** 자체 구현은 YAML 계약·검증기·Codex Skill·수동 Publisher·테스트다. Hindsight 기억 엔진과 GitHub PR/CI를 활용한다. PR 독립 승인 강제, 서버 권한 격리, 자동 게시, 정기 재검증은 설계만 했다. Hindsight가 단순 Git 문서보다 검색 정확도·시간·비용에서 우월하다는 반복 비교 실험은 수행하지 않았다.


가상의 팀 A가 설정 검사 오류에서 빠진 항목을 알려주는 개선을 발견하면, 다른 팀원 B의 Agent가 근거와 적용 조건을 확인하고 활용할 수 있어야 한다. A의 확인되지 않은 추측은 개인 기록에 두고, 테스트·출처·적용 조건을 갖춘 후보만 팀 지식으로 제안한다.

Git main의 YAML은 사람이 검토해 병합한 원본이다. Hindsight의 팀 Bank는 승인된 Git 원본에서 파생된 검색 공간이다. **과거 원본 실험은 `team-compiler`, 현재 제출용 검색은 `team-knowledge-showcase`, 평가자 Fork 실습은 `team-knowledge-repro`**를 사용한다. Agent는 recall 결과의 ID와 원본 커밋을 확인하고 최신 Git 원본의 상태·범위·근거를 확인한 뒤 적용하도록 지침을 받는다. 원본 확인이 불가능하거나 범위 밖이면 적용을 보류한다. 이는 Agent 지침이지 서버에서 모든 Agent에게 강제하는 통제가 아니다.

Codex `share-knowledge` Skill은 기존 지식을 읽고 새 근거·적용 범위·제외 조건을 YAML과 draft PR에 기록한다. 스킬은 승인·병합하거나 팀 Bank에 직접 쓰지 않는다. YAML의 ID, revision, status, problem, cause, solution, scope, limitations, evidence, maintenance 필드는 `schemas/knowledge.schema.yaml`에서 검증한다. 스키마에 proposed가 없으므로 PR의 active는 제안이며 main에 병합되기 전에는 승인 원본이 아니다.

GitHub Actions는 PR과 main에서 형식 및 테스트를 실행한다. 사람이 내용·테스트·근거를 검토하고 병합한다. 별도 `--verify-remote`는 커밋 접근 여부만 확인하며 기본 CI에 포함되지 않는다. 자동 검사는 주장의 옳음이나 독립 검토를 보장하지 않는다.

Publisher는 운영자가 수동 실행한다. 최신 Git main과 원격 main, 스키마, 관리 대상 문서와 메타데이터를 확인해 Hindsight에 동일 ID로 게시·갱신하고 retired 관리 문서는 삭제한다. 성공 기록은 처리 후 작성되며 도중 실패 시 일부 반영이 가능하다. 잠금은 같은 checkout에서만 유효하다.

Hindsight의 Bank·문서 저장·사실 추출·검색은 오픈소스 기본 기능이다. 지식 스키마, 검증기, Skill, Publisher 및 원본 재확인 정책은 이 프로젝트에서 추가했다. 머지 후 자동 게시, 서버 측 Bank별 권한, 인증 헤더, 독립 리뷰 강제, 분산 잠금과 실패 알림은 설계 제안이며 구현하지 않았다. GitHub 원격 실행기는 로컬 Mac의 127.0.0.1에 접근할 수 없으므로 접근 가능한 실행 환경과 인증이 필요하다.

설정 예제의 팀 지식 v1/v2, 실제 실행과 한계는 `EVIDENCE.md`와 `experiments/config-agent-b/`를 참고한다. 개인 기억/Git/Hindsight 조건별 새 예제 반복 실험은 수행하지 않았으므로 정확도·효율성 우위는 주장하지 않는다.

## 병합 후 자동 게시 확장안 — 미구현

목표는 신뢰된 main에 변경이 병합되면 Publisher가 최신 main 스냅샷을 다시 확인하고 전체 관리 대상 지식을 Hindsight에 동기화하는 것이다. PR 단계에서는 기존 Actions가 검증만 하며 게시 API를 호출하지 않는다. 현재 프로토타입은 이 자동화 없이 운영자가 Publisher를 직접 실행한다.

1. 단기에는 로컬 Hindsight에 접근 가능한 신뢰된 실행기에서 main 변경을 감지하고 기존 Publisher를 실행하는 방안을 고려한다. 개인 Mac이 꺼지면 실행이 지연될 수 있다.
2. 운영 환경에서는 인증된 HTTPS API 또는 격리된 실행기, 게시 전용 자격증명과 권한, 요청 시간 제한 및 비밀값 마스킹을 준비한다. 공개 저장소의 외부 PR 코드는 신뢰 실행기에서 실행하지 않는다.
3. 재시도와 중복 호출을 안전하게 처리하고, 오래된 실행이 최신 게시를 덮지 않도록 순서 제어 및 분산 잠금을 구현한다. 실패 알림과 재실행 방법, 감사 기록도 필요하다.
4. 병합 후 게시·동일 변경 재실행·실패 후 복구·연속 병합의 순서 역전·폐기 지식 삭제를 실제 서버에서 통합 테스트해야 자동 게시 완료로 판단할 수 있다.

위 항목은 운영 설계와 후속 검증 계획이며 이 ZIP에 자동 게시 기능이 구현되었다는 뜻은 아니다.


## 독립 재현 및 배포 경계

ZIP은 코드 검증용이고 Git History가 필요한 Publisher는 자신의 Fork에서 clone한 Git Repository에서만 실행할 수 있다. [GitHub·Hindsight 실제 재현](GITHUB_SETUP.md)과 [자동 게시 확장 설계](AUTOMATION_DESIGN.md)를 참고한다. 자동 Workflow는 이 제출물에 존재하지 않으며, 인증 헤더와 신뢰 실행 환경 없이는 운영 서버로 게시할 수 없다.
