# AI Coding Agent 활용 내역

OpenAI Codex 앱을 사용해 요구사항 정리, 설계, 코드·테스트 작성, 검증, PR 준비와 보고서 작성을 수행했다. 사용자는 사례와 작업 방향을 선택하고 PR #5, #6, #7을 직접 병합했다. 별도의 독립 리뷰어 승인은 확인하지 않았다.

Codex CLI의 `gpt-5.6-luna`로 설정 사례의 `share-knowledge` Skill 실행을 시작했으나 사용량 제한으로 중단됐다. 이후 Codex 앱 세션이 생성된 코드를 확인하고 지식 YAML과 PR #5를 완성했다. Skill은 승인·병합 및 팀 Bank 쓰기를 수행하지 않는다.

별도 Codex 세션 B는 team-compiler Bank를 검색하고 Git main의 COMP-015 r1을 확인해 독립 예제에 적용했다. 이후 별도의 새 Codex 세션이 이전 실행 기록과 코드 파일을 읽고 r2를 재검색해 코드를 갱신했다. 이는 동일한 대화 세션의 기억이 자동 갱신된 실험이 아니다. 실제 서로 다른 사람의 계정도 아니다.

설정 예제의 실제 주요 지시 전문은 압축파일 루트의 `prompts/` 아래 세 텍스트 파일이며, Agent 기록은 `experiments/config-agent-b/trace.md`, `post-update-trace.md`를 참고한다. 원래 대화 전체나 과제 원문은 포함하지 않는다.

추가 검토에서 별도 Codex CLI `gpt-5.6-luna` 세션에 지식 ID, 지식 YAML 경로, Bank ID를 지정하지 않은 업무 요청을 수행했다. Hindsight API 주소, Git checkout 위치와 관련 초기 코드는 환경 지침으로 제공했다. 실제 프롬프트와 환경 지침은 `experiments/blind-discovery/prompt.txt`와 `AGENTS.md`, Agent 작성 결과 및 한계는 같은 폴더의 `trace.md`와 `README.md`에 있다. Agent는 관련 지식을 찾았지만 원본 근거 커밋을 검증하지 못했고 출력 문자열의 마침표가 승인 원본과 다르다. 이 점은 자동 발견·검증의 완전한 성공으로 간주하지 않는다.
