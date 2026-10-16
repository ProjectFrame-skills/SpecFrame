# SpecFrame — 적응형 질의 · 프로젝트 전체 요구사항 · 검토와 승인

[English](README.md) · **한국어** · [简体中文](README.zh.md)

[![npm](https://img.shields.io/npm/v/specframe-cli?color=cb3837)](https://www.npmjs.com/package/specframe-cli)
![Skill](https://img.shields.io/badge/skill-SpecFrame-2563eb)
![Python](https://img.shields.io/badge/python-3.11%2B-3776ab?logo=python&logoColor=white)
![Runtime](https://img.shields.io/badge/runtime-standard%20library-16a34a)
![Checks](https://github.com/ProjectFrame-skills/SpecFrame/actions/workflows/verify.yml/badge.svg)

## 필수 프로그램

| 프로그램 | 필요한 경우 |
|---|---|
| Codex 앱 또는 CLI | `$specframe`을 실행할 AI 호스트입니다. skills·로컬 파일 접근·Python 실행 권한이 필요하며, npm 패키지만 설치한다고 AI 호스트가 제공되는 것은 아닙니다. |
| [Python 3.11 이상](https://www.python.org/downloads/) | skill 설치와 상태 저장·복구에 항상 필요합니다. Python 표준 라이브러리를 사용하며 별도 데이터베이스나 pip 패키지는 필요하지 않습니다. |
| [Node.js 18 이상](https://nodejs.org/en/download) + npm/npx | npm/npx 방식으로 설치하거나 `specframe` 명령을 쓸 때 필요합니다. 현재 지원되는 Node.js LTS 버전을 권장하며, npm/npx는 보통 Node.js와 함께 설치됩니다. |
| [Git](https://git-scm.com/downloads/) | 아래 `git clone` 소스 설치 방식을 사용할 때만 필요합니다. |

**npm 설치:** Codex + Node.js/npm/npx + Python. **소스 설치:** Codex + Git + Python이며, npm CLI를 쓰지 않으면 SpecFrame 자체에는 Node.js가 필요하지 않습니다.

npm 설치 전에 다음 명령으로 확인할 수 있습니다.

```bash
node --version
npm --version
npx --version
python3 --version
```

Windows에서 Python 명령이 `python` 또는 `py -3`라면 해당 명령을 사용하세요. `SPECFRAME_PYTHON`은 이미 설치된 Python 실행 파일을 선택하며 Python을 설치해 주지는 않습니다. 다른 AI 호스트는 호환되는 skill 지원과 로컬 실행 기능이 필요합니다. 작업별 추가 도구·서비스 권한은 실제 목표에 따라 달라지며 공통 필수 프로그램은 아닙니다.

## 🚀 npm으로 설치하기

```bash
npm install -g specframe-cli@latest
specframe install
```

**전역 CLI 설치 없이 한 번에 skill을 설치할 수도 있습니다.**

```bash
npx --yes specframe-cli@latest install
```

설치 후 새 Codex 대화에서 `$specframe`을 호출하세요. 설치 도구는 해당 대화의 상태만 복구하는 hook을 Codex 설정에 병합합니다. 실제 실행에는 호스트의 정확한 hook 정의에 대한 신뢰 승인이 필요합니다.

**웹·앱·프로그램 아이디어를 검토하고 승인할 수 있는 프로젝트 요구사항으로 구체화하는 AI skill.**

SpecFrame은 **누구의 문제를 해결하는지, 어떤 기능과 동작이 필요한지, 성공을 어떻게 확인할지** 구체화합니다. 신규 아이디어와 기존 프로젝트 개선을 모두 지원합니다. 답변에 따라 질의를 이어가며 제품의 중요한 선택은 사용자가 결정합니다.

전체 범위의 요구사항 정의와 최종 승인 이후 [SynFrame](https://github.com/ProjectFrame-skills/SynFrame)이 구현 도구·방법과 그 조합을 탐색하도록 이어갈 수 있습니다.

## 주요 기능

| 기능 | 하는 일 |
|---|---|
| 적응형 질의 | 지금 독립적으로 답할 중요한 질문을 함께 제시하고 고정 질문 수 없이 남은 미확정을 구체화합니다. |
| 명확한 답변 틀 | 번호와 짧은 답변 이름을 제공하고 간단한 입력은 묶되 복잡한 결정과 택일 대안을 구분합니다. |
| 전체 범위 요구사항 | 목표·범위·제약·주체·흐름·제외사항을 보존하며 임의로 MVP로 축소하지 않습니다. |
| 요구사항 공학 | 입력이 확보된 단계에서 식별 가능한 의무·EARS·NASA 품질 점검·인수 기준·목적 실패 반례를 적용합니다. |
| UI의 조건부 검토 | 관련 웹 동작과 시각적 선호를 확인하며 프레임워크·테마·설치·오프라인·푸시를 일괄 확정하지 않습니다. |
| 답변 의미 보존 | 확정 사실·제안·근거·미정을 구분하고 부분 답변은 실제 답한 요소만 해결합니다. |
| 복구와 승인 | 현재 요구사항과 작은 진행 정보를 유지하며 사용자 확인 전에 전체 범위를 검토합니다. |

## 설치

보조 코드는 Python 표준 라이브러리만 사용합니다. 추가 Python 패키지·전용 모델 API 키·추론 서버는 필요하지 않습니다. 판단과 실제 도구 사용은 호스트 AI가 수행합니다.

npm CLI는 `CODEX_HOME`을 따르며, 설정이 없으면 `~/.codex`를 사용합니다. 그 아래 `skills/specframe`에 skill을 설치하고 `hooks.json`에 복구 hook을 병합합니다. 경로를 직접 지정할 수도 있습니다.

```bash
specframe install \
  --destination /absolute/path/to/skills/specframe \
  --hooks /absolute/path/to/hooks.json
```

설치 도구는 구현체를 복사하고 기존 hook 그룹을 유지합니다. hook을 처음 변경하기 전 기존 설정이 있으면 `hooks.json.before-specframe`으로 보존합니다. 호스트의 신뢰 설정은 변경하지 않습니다. 기존 skill 설치본은 백업하지 않으므로 이전 버전이 필요하면 따로 보관하세요.

### 소스에서 설치하기 (선택)

```bash
git clone https://github.com/ProjectFrame-skills/SpecFrame.git
cd SpecFrame
python3 tools/install_specframe.py
```

소스 설치에는 Python 3.11 이상이 필요하며 기본 홈은 `~/.codex`입니다. 다른 경로는 `--destination`과 `--hooks`로 지정하세요. npm CLI에는 추가 npm 의존성이 없고 동일한 Python 설치 도구를 호출합니다. 이미 설치된 Python 실행 파일을 직접 고르려면 `SPECFRAME_PYTHON`을 설정하세요. 이 설정이 Python을 설치하지는 않습니다.

다른 호스트에서도 skills와 로컬 Python 실행을 지원하면 `skills/specframe/SKILL.md`와 연결 문서를 불러올 수 있습니다. hook 자동 호출은 호스트 지원에 달려 있습니다. 자동 호출이 없다면 이전 결정에 의존하는 작업 전에 복구 상태를 명시적으로 읽어야 합니다.

## 사용법

### 1. 새로운 아이디어 구체화

```text
$specframe 맞춤 주문을 관리하는 웹을 만들고 싶어.
현재 업무의 문제는 알지만 필요한 기능과 운영 규칙은 아직 잘 모르겠어.
프로젝트 전체를 구체화해줘.
```

**진행:** 목표·환경 확인 → 독립적으로 답할 중요한 질문 → 확정 답변과 미정의 현재 요구사항 반영 → 답변에 의존하는 후속 질의.

번호로 답하거나 일부만 답해도 됩니다. “미정”이라고 남기거나 추천을 요청할 수 있습니다. 실제 사례가 없으면 평소 흐름이나 예상 상황을 설명해도 되며 가상 상황은 실제 사건과 구분합니다.

### 2. 기존 프로젝트 개선

```text
$specframe 이 프로젝트에서 직원들이 변경을 관리하는 방식을 개선하고 싶어.
기존 고객 데이터와 확정된 접근 정책은 유지해줘.
현재 동작을 확인하고 변경할 요구사항을 구체화해줘.
```

**진행:** 알려진 기능·데이터·정책 확인 → 유지와 변경 구분 → 관련 흐름과 인수 기준 구체화.

### 3. 저장된 작업 이어가기

```text
$specframe 현재 프로젝트의 구체화를 이어가줘.
다음 질문 전에 저장된 요구사항과 남은 결정 위치를 읽어줘.
```

기본적으로 프로젝트의 `.specframe/<CODEX_THREAD_ID>.json`을 찾습니다. 다른 세션에서 이어갈 때는 상태 경로와 원래 owner ID를 알려주세요. 상태는 설치된 skill 폴더가 아니라 사용자 프로젝트에 저장합니다.

이 사례는 README 사용법이며 운영 프리셋이 아닙니다. 자동 선택은 호스트 설정에 따르며 `$specframe`으로 명시적으로 호출할 수 있습니다.

## 작동 구조

```text
아이디어 또는 기존 프로젝트
             ↕
적응형 질의 ↔ 현재 요구사항과 미확정
             ↕
전체 검토 → 사용자 최종 승인 → SynFrame → 구현

       맥락 소실 → 현재 상태 읽기 → 계속
```

**호스트 AI**가 질문 선택·답변 해석·요구사항 작성·품질 판단을 담당합니다. **상태 보조 코드**는 호스트가 작성한 판단을 저장·조회하고 구조 검사와 원자적 저장을 수행합니다. 제품 결정을 추론하거나 의미 품질을 검토하지 않습니다.

현재 문서에서 출처·목표와 독립적으로 검증할 의무, 조건, 관찰 결과, 통과·실패 기준, 예상 또는 실제 증거를 연결합니다. 증거가 없으면 미검증으로 유지합니다. 화면 흐름은 텍스트로 구체화하며 시안과 와이어프레임은 기본 산출물에 포함하지 않습니다.

## 상태와 컨텍스트 비용

- 전체 질문·답변 전문 대신 하나의 현재 요구사항을 유지합니다.
- 조건·예외·책임·제외사항·미정을 보존합니다.
- 집중 위치·미정 위치·다음 작업·승인 여부만 작은 진행 정보로 유지합니다.
- 의미 있는 변경을 함께 저장하고 변경이 없으면 쓰지 않습니다.
- 복구 시 전체 대화 재탐색 대신 관련 현재 요구사항을 읽습니다.

품질·복구·최종 검토를 토큰·시간 절감보다 먼저 확인합니다. 질문 수와 문서 길이로 완성도를 판정하지 않습니다. 전체 응답 시간·토큰 절감·사용자 피로도는 호스트와 작업에 따라 달라지며 보편적 개선을 주장하지 않습니다.

## 고급 사용

일반 사용자는 상태 JSON을 직접 작성할 필요가 없습니다. 연동 시 현재 요구사항을 확인할 수 있습니다.

```bash
python3 skills/specframe/scripts/state.py resume
python3 skills/specframe/scripts/state.py index
python3 skills/specframe/scripts/state.py read GOAL SCOPE CONSTRAINTS
python3 skills/specframe/scripts/state.py read --all
```

현재 `CODEX_THREAD_ID`를 사용하는 명령입니다. 다른 세션이나 독립 실행에서는 일치하는 경로·owner를 하위 명령 **앞에** 전달하세요.

```bash
python3 skills/specframe/scripts/state.py \
  --state /absolute/project/path/.specframe/session-id.json \
  --owner session-id resume
```

[전체 운영 계약](skills/specframe/references/operating-contract.md)은 책임을 정의합니다. [skill 진입점](skills/specframe/SKILL.md)은 저장·검토·승인과 조건부 참고 문서를 설명합니다. 플래그는 호스트 판단을 저장하며 의미 검토나 실제 사용자 승인을 증명하지 않습니다.

## 개발 및 검증

```bash
python3 -m unittest discover -s tests -v
npm test
```

Python 검사는 현재 상태 검증·변경 없는 저장·복구 읽기·owner 분리·hook 필터·승인 해제·표준입력 전달을 다룹니다. Node 검사는 CLI 인자·격리 설치·기존 hook 보존·경로 처리를 확인합니다. 질의 품질이나 실제 호스트 자동 압축을 입증하지 않습니다. 행동 검증은 파일 존재에 그치지 않고 실제 재개와 의미 보존을 확인해야 합니다.

```text
skills/specframe/             진입점·운영 계약·참고 문서·보조 코드
tests/                       재현 가능한 상태·복구 검사
cli/specframe.mjs            npm 명령과 Python 설치 도구 연결
package.json                 npm 메타데이터와 포함 파일 목록
tools/install_specframe.py   skill 복사와 복구 hook 통합
.github/workflows/verify.yml Python/Node 검사와 격리 설치 확인
```

구현체와 사용 문서를 배포합니다. 사적 합의·개인 원문 링크·대화 전문·프로젝트 상태·로컬 평가 이력은 제외합니다. SynFrame과 ProjectFrame은 별도 범위이며 함께 설치하거나 제품을 자동 구현하지 않습니다.

## 문제 해결

- **skill이 보이지 않음:** 설치 위치와 `SKILL.md`를 확인하고 새 대화에서 호출하세요.
- **복구가 실행되지 않음:** 호스트 지원과 hook 신뢰를 확인하세요. `resume` 이후 관련 미정·연결 문서를 읽고 의존 작업을 진행하세요.
- **상태가 없거나 손상됐거나 다른 세션 소유임:** 연속성 공백을 드러내고 의도한 경로·owner를 사용하세요. 과거 결정을 만들거나 다른 대화를 덮어쓰지 마세요.
- **질문 범위가 너무 넓음:** 작은 묶음으로 요청할 수 있습니다. 답한 요소는 유지하고 남은 중요한 결정을 이어가야 합니다.
- **승인 후 의미가 변경됨:** 초안으로 돌아가며 전체 검토와 실제 사용자 확인을 다시 받아야 합니다.

README는 [SynFrame의 구성](https://github.com/ProjectFrame-skills/SynFrame)을 따르며 기능과 설치 안내는 SpecFrame 구현을 기준으로 작성했습니다.
