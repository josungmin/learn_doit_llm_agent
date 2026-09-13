# Ollama 간단 사용 매뉴얼

## 1. Ollama란?

https://ollama.com/

Ollama는 **로컬 PC에서 LLM을 다운로드하고 실행하기 위한 도구**입니다.

공식 홈페이지는 `ollama.com`이며, 여기서 설치 파일과 모델 라이브러리를 확인할 수 있습니다.

구조는 단순합니다.

```text
내 PC
  ↓
Ollama
  ↓
Qwen / Gemma / Llama 등
  ↓
CLI / Python / HTTP API
```

Ollama의 핵심 용도는 **모델을 내 컴퓨터에서 직접 실행하는 것**입니다.

---

## 2. 공식 홈페이지와 모델 찾기

Ollama 홈페이지의 **Library**에서 사용 가능한 모델을 검색할 수 있습니다.

예:

```text
qwen3.5
gemma4
```

`qwen3.5`와 `gemma4`는 여러 크기의 모델이 제공될 수 있으므로, 자신의 RAM/GPU 환경에 맞는 tag를 선택하는 것이 중요합니다.

예:

```text
qwen3.5:9b
gemma4:e4b
```

정확한 모델명과 tag는 Ollama Library에서 확인하는 것이 좋습니다.

---

## 3. Ollama 설치

### Windows

공식 Windows 설치 프로그램을 사용할 수 있습니다.

PowerShell 설치 방식:

```powershell
irm https://ollama.com/install.ps1 | iex
```

설치 확인:

```powershell
ollama --version
```

---

## 4. 모델 실행하기

Ollama는 모델이 로컬에 없으면 처음 실행할 때 자동으로 다운로드합니다.

### Qwen 3.5

```bash
ollama run qwen3.5:9b
```

특정 크기를 선택하는 경우:

```bash
ollama run qwen3.5:9b
```

### Gemma 4

```bash
ollama run gemma4:e4b
```

특정 tag를 선택하는 경우:

```bash
ollama run gemma4:e4b
```

---

## 5. 기본적인 사용 흐름

일반적인 흐름은 다음과 같습니다.

```text
ollama pull
    ↓
모델 다운로드

ollama list
    ↓
설치된 모델 확인

ollama run
    ↓
모델 실행
```

예:

```bash
ollama pull qwen3.5:9b
ollama list
ollama run qwen3.5:9b
```

Gemma도 동일합니다.

```bash
ollama pull gemma4:e4b
ollama run gemma4:e4b
```

---

## 6. 자주 사용하는 명령어

| 명령어 | 설명 |
|---|---|
| `ollama run <model>` | 모델 실행 |
| `ollama pull <model>` | 모델 다운로드 |
| `ollama list` | 다운로드한 모델 확인 |
| `ollama show <model>` | 모델 정보 확인 |
| `ollama ps` | 현재 실행 중인 모델 확인 |
| `ollama stop <model>` | 모델 실행 종료 |
| `ollama rm <model>` | 모델 삭제 |

예:

```bash
ollama show qwen3.5:9b
```

---

## 7. Ollama API

Ollama는 로컬에서 HTTP API도 제공합니다.

기본 주소:

```text
http://localhost:11434
```

구조는 다음과 같습니다.

```text
내 프로그램
   ↓
localhost:11434
   ↓
Ollama
   ↓
qwen3.5 / gemma4
```

따라서 CLI뿐 아니라 Python, LangChain, LiteLLM 등의 프로그램에서도 동일한 로컬 모델을 사용할 수 있습니다.

## CanIRun.ai

모델을 다운로드하기 전에는 [CanIRun.ai](https://www.canirun.ai/)에서 내 PC의 GPU와 VRAM으로 어느 정도의 모델을 실행할 수 있는지 가늠할 수 있습니다.

### CanIRun.ai로 시스템 요구사항 확인하기

1. 상단의 `GPU`와 `VRAM`에서 내 그래픽카드와 VRAM 용량을 선택합니다. 자동 감지가 맞지 않거나 내장 그래픽을 사용한다면 직접 선택합니다.
2. 검색창에 실행하려는 모델을 입력합니다. 예: `Gemma 4 E4B IT`
3. 모델 목록의 `Runs great`부터 `Too heavy`까지의 등급을 확인합니다. `Runs well` 이상을 우선 선택하고, `Tight fit`은 속도 저하나 메모리 부족 가능성을 고려합니다.

---

## 정리

| 질문 | 답 |
|---|---|
| 공식 홈페이지 | `ollama.com` |
| 지원 OS | macOS / Windows / Linux |
| 모델 검색 | Ollama Library |
| Qwen 예제 | `ollama run qwen3.5:9b` |
| Gemma 예제 | `ollama run gemma4:e4b` |
| 설치된 모델 확인 | `ollama list` |
| 기본 API 주소 | `localhost:11434` |
| 모델 다운로드 | `ollama pull <model>` |

핵심적인 사용 흐름은 **Ollama 설치 → Library에서 모델 선택 → `ollama run`으로 다운로드 및 실행**입니다.
