# uv 간단 사용 매뉴얼

## 1. uv란?

> **uv는 Python 버전, 가상환경, 패키지 의존성을 빠르고 통합적으로 관리하는 Python 프로젝트 관리 도구입니다.**

Astral에서 개발하며, 기존의 `pip`, `venv`, 일부 `pyenv` 역할을 하나의 도구로 통합할 수 있습니다.

### 설치하기

Windows

```bash
winget install --id=astral-sh.uv -e
```

정상 설치 여부는 다음으로 확인합니다.

```bash
uv --version
```

---

## 2. 왜 패키지 관리가 필요한가?

Python 프로젝트는 보통 여러 외부 라이브러리에 의존합니다.

```python
import requests
import fastapi
import sqlalchemy
```

문제는 개발자마다 설치된 패키지 버전이 다르면 프로그램의 동작도 달라질 수 있다는 것입니다.

```text
개발자 A
Python 3.12
FastAPI 0.116
SQLAlchemy 2.0

개발자 B
Python 3.11
FastAPI 0.103
SQLAlchemy 1.4

→ "내 컴퓨터에서는 되는데?"
```

따라서 프로젝트에서는 다음 정보를 관리해야 합니다.

- 어떤 Python 버전을 사용하는가?
- 어떤 패키지가 필요한가?
- 어떤 버전의 패키지를 사용하는가?
- 다른 컴퓨터에서도 같은 환경을 만들 수 있는가?

즉, **패키지 관리의 핵심 목적은 개발 환경을 재현 가능하게 만드는 것**입니다.

---

## 3. pip보다 uv를 사용하는 이유

`pip`는 기본적으로 **Python 패키지를 설치하는 도구**입니다.

```bash
pip install requests
```

전통적으로는 여러 도구를 함께 사용했습니다.

```text
pyenv / python   → Python 버전
venv             → 가상환경
pip              → 패키지 설치
requirements.txt → 패키지 버전 기록
```

`uv`를 사용하면 이를 하나의 흐름으로 관리할 수 있습니다.

```text
                 uv

Python 버전 ──────┐
가상환경 ─────────┤
패키지 설치 ──────┤
의존성 해결 ──────┤
lock 파일 ────────┘
```

사용법도 단순합니다.

```bash
uv add requests
uv remove requests
uv run python main.py
```

또한 `uv.lock`을 통해 정확한 의존성 버전을 기록하여 다른 컴퓨터에서도 동일한 환경을 재현하기 쉽습니다.

---

## 4. 기본 사용 흐름

### 새로운 프로젝트 만들기

#### 프로젝트 생성

```bash
uv init my-project
cd my-project
```

또는 현재 디렉터리에서:

```bash
mkdir my-project
cd my-project

uv init
```

기본적으로 다음과 같은 파일이 생성됩니다.

```text
my-project/
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

최소한의 프로젝트만 만들고 싶다면:

```bash
uv init --bare
```

```text
my-project/
└── pyproject.toml
```

`--bare`는 README, Python 버전 파일, 샘플 코드, Git 초기화 등을 생략하고 최소한의 프로젝트만 생성합니다.

#### 패키지 추가

예를 들어 `requests`를 사용한다면:

```bash
uv add requests
```

여러 개도 가능합니다.

```bash
uv add fastapi uvicorn sqlalchemy
```

그러면 `pyproject.toml`에 의존성이 기록되고 `uv.lock`도 함께 갱신됩니다.

#### 프로그램 실행

```bash
uv run python main.py
```

또는:

```bash
uv run main.py
```

`uv run`은 프로젝트 환경에서 명령을 실행합니다. 필요한 경우 `.venv`를 만들고 프로젝트 의존성을 맞춰주기 때문에 보통 직접 가상환경을 활성화하지 않아도 됩니다.

```bash
source .venv/bin/activate
```

새 프로젝트의 기본 흐름은 다음과 같습니다.

```text
uv init
   ↓
uv add <package>
   ↓
코드 작성
   ↓
uv run ...
```

---

### Git에서 프로젝트 받아서 실행하기

uv 프로젝트가 Git 저장소에 있다고 가정합니다.

```bash
git clone https://github.com/example/my-project.git
cd my-project
```

프로젝트에는 일반적으로 다음 파일들이 포함됩니다.

```text
pyproject.toml
uv.lock
.python-version
```

하지만 `.venv`는 Git에 포함하지 않습니다.

프로젝트 환경을 구성하려면:

```bash
uv sync
```

개념적으로 다음 작업이 이루어집니다.

```text
.python-version
      ↓
적절한 Python 선택

pyproject.toml
      +
uv.lock
      ↓
.venv 생성
      ↓
필요한 패키지 설치
```

그 다음 프로그램을 실행합니다.

```bash
uv run python main.py
```

즉, Git 프로젝트를 받아 실행하는 기본 패턴은:

```bash
git clone <repository>
cd <project>

uv sync

uv run python main.py
```

입니다.

많은 경우 `uv run` 자체가 환경을 동기화해주므로 바로 실행할 수도 있습니다.

```bash
git clone <repository>
cd <project>

uv run python main.py
```

---

## 5. uv 프로젝트 파일 설명

대표적인 uv 프로젝트 구조는 다음과 같습니다.

```text
my-project/
│
├── .python-version
├── pyproject.toml
├── uv.lock
├── .venv/
│
├── README.md
└── main.py
```

### `pyproject.toml`

**프로젝트의 설계도**라고 생각하면 됩니다.

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "requests>=2.32.0",
]
```

주로 다음 정보가 들어갑니다.

- 프로젝트 이름
- Python 버전 조건
- 사용하는 패키지
- 프로젝트 버전
- 빌드 설정
- uv 관련 설정

`uv add`와 `uv remove`를 사용하면 의존성 정보가 이 파일에 반영됩니다.

---

### `uv.lock`

**실제로 사용할 패키지 버전을 정확하게 기록한 파일**입니다.

개념적으로:

```text
pyproject.toml
"requests가 필요해"

        ↓ 의존성 해결

uv.lock
"그럼 정확히 이 버전들을 사용해"
```

`uv.lock`은 직접 수정하지 않고 `uv`가 관리하도록 두는 것이 좋습니다.

일반적으로 Git에 포함합니다.

---

### `.python-version`

프로젝트에서 기본적으로 사용할 Python 버전을 지정합니다.

예:

```text
3.12
```

uv는 이 파일을 참고하여 적절한 Python 버전을 선택합니다.

---

### `.venv/`

프로젝트 전용 **가상환경**입니다.

```text
.venv/
├── bin/
├── lib/
└── ...
```

설치된 패키지가 실제로 들어가는 장소입니다.

```text
내 시스템
   │
   ├── Project A
   │     └── .venv
   │          └── FastAPI 0.116
   │
   └── Project B
         └── .venv
              └── FastAPI 0.110
```

각 프로젝트의 환경을 서로 분리하기 위한 것입니다.

`.venv`는 다시 생성할 수 있으므로 **Git에는 포함하지 않습니다.**

---

### Git 커밋 기준

프로젝트 환경을 다른 컴퓨터에서도 동일하게 재현하려면 다음 파일을 함께 커밋합니다.

| 파일 | Git 커밋 | 이유 |
|---|---|---|
| `pyproject.toml` | 포함 | 필요한 패키지와 Python 조건을 정의합니다. |
| `uv.lock` | 포함 | 실제 설치할 패키지의 정확한 버전을 고정합니다. |
| `.python-version` | 포함 | 프로젝트의 Python 버전을 팀원과 동일하게 맞춥니다. |
| `README.md`, `main.py` | 포함 | 프로젝트 설명과 소스 코드입니다. |
| `.venv/` | 제외 | `uv sync`로 다시 만들 수 있는 로컬 가상환경입니다. |
| `.env` | 제외 | API 키 등 민감한 값이 포함될 수 있습니다. |
| `.env.example` | 포함 | 필요한 환경 변수 이름만 공유합니다. |

`.venv/`와 `.env`는 `.gitignore`에 추가합니다.

---

## 6. 자주 사용하는 명령어

| 명령 | 의미 |
|---|---|
| `uv init` | 프로젝트 생성 |
| `uv init --bare` | 최소 프로젝트 생성 |
| `uv add requests` | 패키지 추가 |
| `uv remove requests` | 패키지 제거 |
| `uv sync` | 프로젝트 환경 구성 및 동기화 |
| `uv run python main.py` | 프로젝트 환경에서 실행 |
| `uv python install 3.12` | Python 설치 |
| `uv python pin 3.12` | 프로젝트 Python 버전 지정 |

---

## 7. 핵심 흐름 요약

### 새 프로젝트

```text
uv init
   ↓
uv add <package>
   ↓
uv run ...
```

### 기존 프로젝트

```text
git clone
   ↓
uv sync
   ↓
uv run ...
```

### 핵심 파일

```text
pyproject.toml   = 필요한 환경과 의존성을 정의
uv.lock          = 실제 사용할 정확한 패키지 버전을 고정
.python-version  = 사용할 Python 버전
.venv            = 실제 프로젝트 가상환경
```
