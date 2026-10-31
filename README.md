# 팀 Agent 지식 저장소

팀원 A와 Agent가 확인한 개선을 Git에서 검토한 후 Hindsight에 게시하고, B의 Agent가 이를 검색·활용·갱신하는 프로토타입입니다. **Git YAML이 지식 원본**이고, Hindsight는 검색용 저장소입니다.

## 예제: 설정 오류 메시지

설정에서 `model`이 빠져도 기존 프로그램은 `설정 오류`만 표시했습니다. r1은 빠진 항목 이름을 알려주도록 개선했습니다. 이후 `model`과 `version`이 동시에 빠지는 경우를 확인해 r2는 누락된 항목을 모두 표시하도록 갱신했습니다.

| 상황 | 출력 |
|---|---|
| 기존: model 누락 | `설정 오류` |
| r1: model 누락 | `설정 오류: model 항목이 없습니다` |
| r2: model·version 누락 | `설정 오류: model, version 항목이 없습니다` |

이 코드는 가상의 Python 예제이며 실제 제품의 설정 규칙이나 성능을 대표하지 않습니다. r2는 두 키의 **존재 여부**만 확인합니다.

## 처음 실행하기

macOS/Linux 셸, Python 3.12, 패키지 설치를 위한 인터넷 연결이 필요합니다. 다음 단계에는 Hindsight나 GitHub 인증이 필요하지 않습니다.

```bash
git clone https://github.com/5jyan/team-agent-knowledge-showcase.git
cd team-agent-knowledge-showcase
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate.py knowledge
python -m unittest discover -s tests -v
python -m unittest discover -s examples/config-validation -p 'test_*.py' -v
python examples/config-validation/run_demo.py
(cd experiments/config-agent-b && python -m unittest discover -s tests -p 'test_*.py' -v)
python -m unittest discover -s experiments/blind-discovery -p 'test_*.py' -v
```

예상 결과: 지식 1건 검증, 핵심 테스트 21개, 설정 예제 테스트 5개, Agent B가 남긴 r2 코드 테스트 5개, 추가 검색 실험 테스트 5개 통과. 테스트는 과거 Agent가 작성한 코드를 실행하며, Agent를 새로 호출하는 것은 아닙니다. 원본 지식의 GitHub 근거 커밋을 추가 확인하려면 `python scripts/validate.py knowledge --verify-remote`를 실행합니다.

## 실제로 확인한 흐름

1. A 역할에서 예제와 지식 `COMP-015 r1`을 제안하고 사용자가 병합했습니다.
2. 운영자가 Publisher를 **수동 실행**해 로컬 Hindsight 팀 Bank에 게시했습니다.
3. 별도 Codex 세션의 B가 지식을 검색하고 승인된 Git 원본을 확인한 뒤 독립 예제에 적용했습니다. r1에서 다루지 않는 version 규칙은 보류했습니다.
4. r2 변경을 사용자가 병합하고 수동 게시했습니다. 새 Codex 세션이 이전 B의 작업 기록을 읽고 r2를 재확인한 뒤 코드를 갱신했습니다.

기존 대화 세션의 기억이 자동 갱신된 실험이나 실제 다른 팀원 계정 간 협업은 아닙니다. 새 예제에서 대안별 반복 실험, 자동 게시, Bank별 ACL, 독립 제3자 리뷰는 검증하지 않았습니다.

## 제출 자료와 실제 원본의 관계

이 저장소는 설정 오류 사례만 추린 **제출용 스냅샷**으로 새로 만들었습니다. 이곳의 Git 이력은 원래 PR 이력이 아닙니다. 실제 최초 실험과 사람의 병합 이력은 별도의 공개 [원본 저장소](https://github.com/5jyan/team-agent-knowledge)에 남아 있습니다.

- [r1 제안·병합 PR #5](https://github.com/5jyan/team-agent-knowledge/pull/5)
- [r2 갱신·병합 PR #6](https://github.com/5jyan/team-agent-knowledge/pull/6)
- [r2 코드·테스트 근거 커밋](https://github.com/5jyan/team-agent-knowledge/commit/f712c83919e17bfcbd9de099b0deef00c54ecaee)
- [설계](docs/DESIGN.md) · [실제 검증 기록](docs/EVIDENCE.md) · [AI 활용 내역](docs/AI_USAGE.md)
- [상세 HTML 보고서](docs/report.html): GitHub에서 파일을 내려받아 브라우저로 열어 주세요. 화면 캡처가 파일 안에 포함돼 있습니다.
- [Agent 실행 기록](experiments/config-agent-b/) · [추가 검색 실험](experiments/blind-discovery/) · [개인 Bank 추가 실험](experiments/personal-bank/) · [Agent 요청 발췌와 전문](prompts/)

여기 포함된 Skill은 원래 스킬을 **이 제출용 저장소 구조에 맞게 수정한 사본**입니다. 과거 PR #5에서 실제 실행한 스킬은 원본 저장소와 원래 스킬 구조를 대상으로 했습니다. 실제 프롬프트 중 이전 사례 관련 문장 두 개는 제출용 발췌에서 생략했다고 표시했습니다.

## Hindsight와 수동 게시

Hindsight API 1.1.0과 LLM 제공자 설정이 필요합니다. 설치는 [Hindsight 공식 안내](https://hindsight.vectorize.io/developer/installation)를 참고하세요. 별도의 로컬 Bank를 만든 후 아래를 실행합니다.

```bash
curl -X PUT http://127.0.0.1:8888/v1/default/banks/team-knowledge-showcase \
  -H 'Content-Type: application/json' -d '{"name":"team-knowledge-showcase"}'
python scripts/reconcile.py --snapshot-commit "$(git rev-parse main)" --dry-run
python scripts/reconcile.py --snapshot-commit "$(git rev-parse main)"
```

Publisher는 로컬 및 원격의 최신 `main`이 일치하고 추적 파일에 변경이 없는지 확인합니다. 기본 Bank는 `team-knowledge-showcase`입니다. 이전 실험 Bank `team-compiler`와 이름을 분리했으며 서버 측 접근 권한 분리를 의미하지 않습니다. 같은 ID라도 다른 저장소가 관리하는 문서는 덮어쓰지 않습니다. API 인증 헤더, 여러 컴퓨터의 분산 잠금과 머지 후 자동 게시는 구현하지 않았습니다.

## 동일 입력으로 r1·r2 비교

실제 과거 원본 저장소의 두 커밋에서 코드 파일을 읽어 같은 입력으로 실행합니다. 임의의 Git 코드를 실행하므로 신뢰하는 원본 checkout에만 사용하세요.

```bash
git clone https://github.com/5jyan/team-agent-knowledge.git ../team-agent-knowledge
python experiments/revision-comparison/compare.py ../team-agent-knowledge
```

r1은 당시 model만 필수였던 예제입니다. r2에서 version을 추가한 요구사항 변화이며, r1이 당시부터 잘못됐다는 뜻은 아닙니다.
