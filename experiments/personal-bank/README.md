# 개인 Bank 추가 실험

2026-10-31에 기존 r1/r2 실험 이후 별도로 수행한 가상 데이터 실험이다. 개인 Bank `personal-config-experiment`를 만들고 `CONFIG-PERSONAL-HYPOTHESIS` 문서로 “model이 빈 문자열이면 오류일 수도 있다”는 미검증 가설을 동기 저장했다. 실제 사용자 정보는 포함하지 않았다.

문서 목록에서 개인 Bank에는 해당 ID가 1건, 팀 Bank `team-knowledge-showcase`에는 0건이었다. 같은 질의의 recall에서 해당 문서 ID가 개인 Bank에서 1건, 팀 Bank에서 0건이었다. 이는 두 Bank의 라우팅을 확인한 결과이며 접근 권한 강제나 모든 검색에서의 비노출을 증명하지 않는다.

이 실험은 실제 과거 r1 PR의 입력 경로가 아니다. 개인 Bank의 메모가 PR을 통해 승격된 과정은 실제로 확인하지 않았다. 과거 설정 지식의 PR·팀 게시와 이 추가 실험을 인과 관계로 연결하지 않는다.
