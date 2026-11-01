# 지식 ID를 미리 알려주지 않은 검색 실험

별도 Codex 세션에 `prompt.txt`의 업무 요청과 `before.py`에 해당하는 초기 코드, `AGENTS.md`에 기록한 로컬 API·Git checkout 환경 안내를 제공했다. 프롬프트와 환경 안내에 지식 ID·지식 파일 경로·Bank ID를 넣지 않았다. 완전히 무도구 환경은 아니며 Hindsight API 주소와 Git checkout 위치는 제공했다.

Agent는 Bank 목록을 조회해 team-knowledge-showcase를 선택하고 검색으로 COMP-015 v2를 찾았다. 제출용 checkout의 로컬 main과 YAML을 확인했지만, 별도 원본 저장소에 있는 근거 커밋은 제출용 checkout에서 `bad object`가 나 재검증하지 못했다. 원격 main을 새로 확인한 기록도 없다. 이 차이를 trace.md에 기록했다.

Agent가 작성한 `config_checker.py`, `test_config_checker.py`는 두 필수 키의 누락 이름을 출력하며 테스트 5개가 통과했다. 이 결과의 메시지 끝에는 마침표가 있으나 현재 승인 YAML의 예시 출력에는 없다. 실제 동작 차이이며, 원본의 정확한 문자열과 완전히 일치하는 검증이 아니다. 출력값과 적용 범위에 대한 별도 검증의 중요성을 보여준다.

한 번의 안내된 환경에서 지식 탐색·적용 사례일 뿐 모든 Agent의 자율적 발견 능력이나 검색 우월성을 증명하지 않는다. 설정과 코드의 내용으로 지식과 연결할 단서는 제공되었다.

```bash
cd experiments/blind-discovery
python3 -m unittest discover -s . -p 'test_*.py' -v
```
