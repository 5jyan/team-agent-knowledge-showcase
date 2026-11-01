# 팀 Agent 지식 저장소

팀원 A와 Agent가 확인한 개선을 Git에서 검토한 후 Hindsight에 게시하고, B의 Agent가 이를 검색·활용·갱신하는 프로토타입입니다. **Git YAML이 지식 원본**이고, Hindsight는 검색용 저장소입니다.

> **설계 의사결정:** Hindsight의 Bank·Recall·문서 API를 재사용하고, 팀 지식 후보 분류·근거 검증·PR 승인·게시·갱신 정책을 추가했습니다. [요구사항별 판단 및 구현 범위](docs/DESIGN.md#과제-요구사항에서-기능을-도출한-이유)에 기존 기능과 직접 구현한 기능을 비교했습니다.

> **버전 표기 안내:** 이 제출용 저장소와 ZIP은 지식과 실행 기록의 버전 이름을 `v1`·`v2`로 통일한 제출용 사본입니다. 실제 GitHub·Hindsight의 과거 원본은 바꾸지 않았으므로 버전 필드와 실행 로그가 이 사본과 다를 수 있습니다. 과거 프롬프트와 실행 기록은 표기를 치환한 사본이며, 실제 원문은 링크한 저장소에서 확인할 수 있습니다. 과거 실험을 수행한 원본 저장소의 이력은 그대로 유지합니다.

## 예제: 설정 오류 메시지

설정에서 `model`이 빠져도 기존 프로그램은 `설정 오류`만 표시했습니다. v1은 빠진 항목 이름을 알려주도록 개선했습니다. 이후 `model`과 `version`이 동시에 빠지는 경우를 확인해 v2는 누락된 항목을 모두 표시하도록 갱신했습니다.

| 상황 | 출력 |
|---|---|
| 기존: model 누락 | `설정 오류` |
| v1: model 누락 | `설정 오류: model 항목이 없습니다` |
| v2: model·version 누락 | `설정 오류: model, version 항목이 없습니다` |

이 코드는 가상의 Python 예제이며 실제 제품의 설정 규칙이나 성능을 대표하지 않습니다. v2는 두 키의 **존재 여부**만 확인합니다.

## 처음 실행하기

macOS/Linux 셸, Python 3.12, 패키지 설치를 위한 인터넷 연결이 필요합니다. **이 절은 ZIP 압축 해제본에서도 실행 가능한 코드 테스트 경로(A)**입니다. `team-agent-knowledge-showcase` 폴더에서 다음 명령을 실행합니다. 이 단계에는 Hindsight나 GitHub 인증이 필요하지 않습니다. **실제 PR·게시 실습(B/C)은 ZIP이 아닌 자신의 GitHub Fork를 clone한 Git 저장소에서 진행**합니다. 상세 명령은 [GitHub 재현 가이드](docs/GITHUB_SETUP.md)를 참고하세요.

```bash
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

예상 결과: 지식 1건 검증, 핵심 테스트 21개, 설정 예제 테스트 5개, Agent B가 남긴 v2 코드 테스트 5개, 추가 검색 실험 테스트 5개 통과. 각 테스트는 서로 다른 코드·검증 단위를 확인하며, 전부 독립적인 종단 간 검증은 아닙니다. Agent 코드를 실행하는 테스트는 과거에 작성된 코드를 검증하며 Agent를 새로 호출하는 것은 아닙니다. 원본 지식의 GitHub 근거 커밋을 추가 확인하려면 `python scripts/validate.py knowledge --verify-remote`를 실행합니다.

## 실제로 확인한 흐름

1. A 역할에서 예제와 지식 `COMP-015 v1`을 제안하고 사용자가 병합했습니다.
2. 운영자가 Publisher를 **수동 실행**해 로컬 Hindsight 팀 Bank에 게시했습니다.
3. 별도 Codex 세션의 B가 지식을 검색하고 승인된 Git 원본을 확인한 뒤 독립 예제에 적용했습니다. v1에서 다루지 않는 version 규칙은 보류했습니다.
4. v2 변경을 사용자가 병합하고 수동 게시했습니다. 새 Codex 세션이 이전 B의 작업 기록을 읽고 v2를 재확인한 뒤 코드를 갱신했습니다.

기존 대화 세션의 기억이 자동 갱신된 실험이나 실제 다른 팀원 계정 간 협업은 아닙니다. 새 예제에서 대안별 반복 실험, 자동 게시, Bank별 ACL, 독립 제3자 리뷰는 검증하지 않았습니다.

## 제출 자료와 실제 원본의 관계

이 저장소는 설정 오류 사례만 추린 **제출용 스냅샷**으로 새로 만들었습니다. 이곳의 Git 이력은 원래 PR 이력이 아닙니다. 실제 최초 실험과 사람의 병합 이력은 별도의 공개 [원본 저장소](https://github.com/5jyan/team-agent-knowledge)에 남아 있습니다.

- [v1 제안·병합 PR #5](https://github.com/5jyan/team-agent-knowledge/pull/5)
- [v2 갱신·병합 PR #6](https://github.com/5jyan/team-agent-knowledge/pull/6)
- [v2 코드·테스트 근거 커밋](https://github.com/5jyan/team-agent-knowledge/commit/f712c83919e17bfcbd9de099b0deef00c54ecaee)
- [설계](docs/DESIGN.md) · [실제 검증 기록](docs/EVIDENCE.md) · [AI 활용 내역](docs/AI_USAGE.md)
- [상세 HTML 보고서](docs/report.html): GitHub에서 파일을 내려받아 브라우저로 열어 주세요. 화면 캡처가 파일 안에 포함돼 있습니다.
- [Agent 실행 기록](experiments/config-agent-b/) · [추가 검색 실험](experiments/blind-discovery/) · [개인 Bank 추가 실험](experiments/personal-bank/) · [버전 표기를 통일한 Agent 요청 기록](prompts/)

여기 포함된 Skill은 원래 스킬을 **이 제출용 저장소 구조에 맞게 수정한 사본**입니다. 과거 PR #5에서 실제 실행한 스킬은 원본 저장소와 원래 스킬 구조를 대상으로 했습니다. 실제 프롬프트 중 이전 사례 관련 문장 두 개는 제출용 발췌에서 생략했다고 표시했습니다.

## Hindsight 설치와 수동 게시 — 반드시 Git clone에서 실행

**ZIP은 Git 이력이 없으므로 `reconcile.py` 게시 대상으로 사용할 수 없습니다.** ZIP으로 코드 테스트(A)를 한 뒤, 실제 게시(C)를 재현하려면 GitHub에서 자신의 **Fork를 clone(B)**하고 그 Git 저장소 루트로 이동하세요. 이미 Fork를 clone한 경우에는 다시 압축 해제본으로 돌아오지 않습니다.

- **B: GitHub 준비 및 PR** — [Fork → Branch → PR → GitHub Actions → 사람 병합](docs/GITHUB_SETUP.md#2-b-경로--개인-fork에서-실제-pr-재현)
- **C: 로컬 Hindsight 1.1.0** — [Docker 실행, LLM API 키, `/health`, Bank 생성, 게시, Recall](docs/GITHUB_SETUP.md#3-c-경로--hindsight-110-로컬-설치)
- **자동화 미구현 설계** — [`main` Push → 신뢰된 Publisher → Hindsight REST API](docs/AUTOMATION_DESIGN.md)

Fork 저장소를 clone하고 Hindsight API를 준비한 뒤에는 다음처럼 실행합니다. `<YOUR_GITHUB_ID>`는 자신의 GitHub 계정으로 바꾸고, `team-knowledge-repro`는 평가자 전용으로 새로 만든 Bank입니다.

```bash
# 자신의 Fork에서 복제한 Git clone 루트에서만 실행
git switch main && git fetch origin && git pull --ff-only origin main
python scripts/reconcile.py --snapshot-commit "$(git rev-parse HEAD)" \
  --source-repository "<YOUR_GITHUB_ID>/team-agent-knowledge-showcase" \
  --bank-id team-knowledge-repro --dry-run
# 위 계획과 API 응답을 확인한 후 --dry-run 없이 동일 명령을 실행
```

Bank 이름은 **과거 원본 실험 `team-compiler` / 현재 제출본 `team-knowledge-showcase` / 평가자 실습 `team-knowledge-repro`**로 구분합니다. 로컬 Bank 분리는 서버 측 보안 ACL을 의미하지 않습니다. 지금 구현된 것은 **수동 Publisher**이며, 인증 헤더·분산 잠금·머지 후 자동 게시는 구현하지 않았습니다.

## 동일 입력으로 v1·v2 비교

실제 과거 원본 저장소의 두 커밋에서 코드 파일을 읽어 같은 입력으로 실행합니다. 임의의 Git 코드를 실행하므로 신뢰하는 원본 checkout에만 사용하세요.

```bash
git clone https://github.com/5jyan/team-agent-knowledge.git ../team-agent-knowledge
python experiments/revision-comparison/compare.py ../team-agent-knowledge
```

v1은 당시 model만 필수였던 예제입니다. v2에서 version을 추가한 요구사항 변화이며, v1이 당시부터 잘못됐다는 뜻은 아닙니다.
