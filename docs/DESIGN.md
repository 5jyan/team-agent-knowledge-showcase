# 팀 Agent 지식 저장소 설계

가상의 팀 A가 설정 검사 오류에서 빠진 항목을 알려주는 개선을 발견하면, 다른 팀원 B의 Agent가 근거와 적용 조건을 확인하고 활용할 수 있어야 한다. A의 확인되지 않은 추측은 개인 기록에 두고, 테스트·출처·적용 조건을 갖춘 후보만 팀 지식으로 제안한다.

Git main의 YAML은 사람이 검토해 병합한 원본이다. Hindsight team-compiler Bank는 원본에서 파생된 검색 공간이다. Agent는 recall 결과의 ID와 원본 커밋을 확인하고 최신 Git 원본의 상태·범위·근거를 확인한 뒤 적용하도록 지침을 받는다. 원본 확인이 불가능하거나 범위 밖이면 적용을 보류한다. 이는 Agent 지침이지 서버에서 모든 Agent에게 강제하는 통제가 아니다.

Codex `share-knowledge` Skill은 기존 지식을 읽고 새 근거·적용 범위·제외 조건을 YAML과 draft PR에 기록한다. 스킬은 승인·병합하거나 팀 Bank에 직접 쓰지 않는다. YAML의 ID, revision, status, problem, cause, solution, scope, limitations, evidence, maintenance 필드는 `schemas/knowledge.schema.yaml`에서 검증한다. 스키마에 proposed가 없으므로 PR의 active는 제안이며 main에 병합되기 전에는 승인 원본이 아니다.

GitHub Actions는 PR과 main에서 형식 및 테스트를 실행한다. 사람이 내용·테스트·근거를 검토하고 병합한다. 별도 `--verify-remote`는 커밋 접근 여부만 확인하며 기본 CI에 포함되지 않는다. 자동 검사는 주장의 옳음이나 독립 검토를 보장하지 않는다.

Publisher는 운영자가 수동 실행한다. 최신 Git main과 원격 main, 스키마, 관리 대상 문서와 메타데이터를 확인해 Hindsight에 동일 ID로 게시·갱신하고 retired 관리 문서는 삭제한다. 성공 기록은 처리 후 작성되며 도중 실패 시 일부 반영이 가능하다. 잠금은 같은 checkout에서만 유효하다.

Hindsight의 Bank·문서 저장·사실 추출·검색은 오픈소스 기본 기능이다. 지식 스키마, 검증기, Skill, Publisher 및 원본 재확인 정책은 이 프로젝트에서 추가했다. 머지 후 자동 게시, 서버 측 Bank별 권한, 인증 헤더, 독립 리뷰 강제, 분산 잠금과 실패 알림은 설계 제안이며 구현하지 않았다. GitHub 원격 실행기는 로컬 Mac의 127.0.0.1에 접근할 수 없으므로 접근 가능한 실행 환경과 인증이 필요하다.

설정 예제의 팀 지식 r1/r2, 실제 실행과 한계는 `EVIDENCE.md`와 `experiments/config-agent-b/`를 참고한다. 개인 기억/Git/Hindsight 조건별 새 예제 반복 실험은 수행하지 않았으므로 정확도·효율성 우위는 주장하지 않는다.
