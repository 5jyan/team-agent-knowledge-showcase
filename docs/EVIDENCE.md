# 설정 오류 사례 실행 및 검증 기록

- PR #5: 필수 model 누락 오류 메시지에 관한 COMP-015 v1 제안. 설정 예제의 누락·정상·설정값 미노출 테스트 3개를 확인하고 사용자가 병합했다.
- 사용자 병합 후 Publisher를 수동 실행했다. team-compiler Bank에 COMP-015를 게시하고 Git snapshot `a54e8d6326cd2c7c0ec3f2dd474b79e9e7da68f1` 및 recall을 확인했다.
- 별도 Codex Agent는 v1을 검색하고 Git 원본과 적용 조건을 확인해 독립 예제에 적용했다. 당시 테스트 4개가 통과했으며 version 동시 누락은 v1의 승인 범위 밖이므로 판단을 보류했다. `experiments/config-agent-b/trace.md` 참고.
- PR #6: model·version 중 빠진 항목을 모두 안내하는 v2 제안. 예제 테스트 5개를 확인하고 사용자가 병합했다.
- 병합 후 Publisher를 수동 실행해 Git snapshot `f15b4847adee6c60992299e73eb8b446e7bb0587` 기준 COMP-015를 갱신하고 이전 실험의 관리 대상 문서를 정리했다. 문서 목록에 COMP-015만 남았고 설정 오류 검색 결과를 확인했다. 모든 질의나 다른 저장 공간까지 내용이 삭제됐다는 보장은 아니다.
- 새 Codex 세션은 이전 B 기록과 코드 파일을 읽은 뒤 v2를 검색하고 Git 원본을 확인해 B 예제를 갱신했다. 테스트 5개가 통과했다. `experiments/config-agent-b/post-update-trace.md` 참고.

Agent B의 두 실행은 서로 다른 세션이며 실제 여러 팀원 계정의 협업은 아니다. 모델이 자동으로 열린 기존 세션의 기억을 갱신했는지 확인하지 않았다. 자동 게시, 서버 측 Bank ACL, 독립 제3자 리뷰는 구현·검증하지 않았다. 새 설정 사례에 대한 개인 기억/Git/Hindsight 반복 비교, 실제 업무 성능과 시간·비용은 측정하지 않았다.

## 추가 검증: 동일 입력과 검색

원본 저장소의 실제 v1 커밋 `a54e8d6`과 v2 커밋 `f15b484`의 함수를 같은 입력으로 실행했다. `{}`에서 v1은 model만, v2는 model·version을 안내했다. `{"model":"demo"}`에서 v1은 정상, v2는 version 누락을 반환했다. 두 키가 있으면 모두 정상이었다. version은 v2에서 추가된 요구사항이다. `experiments/revision-comparison/compare.py`로 재현한다.

추가 별도 Codex 세션에는 Bank ID, 지식 ID, YAML 파일 경로를 제시하지 않았다. API 주소와 Git checkout 위치는 안내했다. Agent는 Bank 목록과 recall로 COMP-015 v2를 찾고 코드를 수정했으며 테스트 5개가 통과했다. 원격 최신 main의 재확인 기록이 없고 실제 근거 커밋은 제출용 checkout에서 확인하지 못했다. 작성한 오류 메시지는 승인 원본과 마침표 한 글자가 다르다. 자율적 발견의 한 사례이며 원본 검증이 완전하거나 일반적 우위를 입증한 실험이 아니다. `experiments/blind-discovery/` 참고.

별도 사후 개인 Bank 실험에서 미검증 가상 메모는 해당 개인 Bank의 문서 목록·검색에 있었고 팀 Bank에는 같은 문서 ID가 없었다. 개인 Bank와 팀 Bank를 직접 지정한 라우팅 실험이며 사용자별 접근 통제나 과거 PR의 개인 Bank 기원을 입증하지 않는다. `experiments/personal-bank/` 참고.
