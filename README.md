# 📚 LLM을 활용한 AI 에이전트 개발 학습

『Do it! LLM을 활용한 AI 에이전트 개발 입문』을 읽고, LLM 애플리케이션부터 RAG와 멀티에이전트 시스템까지 직접 구현하며 학습하는 저장소입니다.
책의 예제를 실습하며 각 구성 요소의 역할을 이해하고, 궁금한 내용은 별도로 정리합니다.

## 🔎 주요 학습 내용

- **LLM 애플리케이션**: OpenAI API를 이용한 텍스트·이미지·음성 처리
- **Tool Calling**: LLM과 외부 함수 및 데이터 연결
- **RAG**: 문서를 검색하고 검색 결과를 바탕으로 답변하는 흐름 구현
- **LangChain과 LangGraph**: 도구, 상태, 에이전트를 연결하는 워크플로 구성
- **멀티에이전트**: 역할별 에이전트가 검색과 콘텐츠 작성에 협력하는 과정 학습
- **로컬 LLM**: Ollama와 DeepSeek을 활용한 실습

## 🛠️ 대표 실습

### [문서 기반 질의응답 — RAG](./chap09/)

문서를 검색하고 관련 내용을 바탕으로 답변하는 RAG 예제를 실습합니다.  
문서 검색과 답변 생성이 연결되는 흐름을 학습합니다.

### [검색과 협업을 활용한 멀티에이전트](./chap14/)

LangGraph로 Supervisor와 역할별 에이전트를 연결해 책의 목차를 작성하는 예제를 구현합니다.  
웹 검색과 벡터 검색 도구를 활용하고, 작업을 나누어 처리하는 흐름을 살펴봅니다.

### [판단과 검토 과정을 추가한 멀티에이전트](./chap15/)

멀티에이전트 목차 작성 예제에 요구사항 분석과 목차 검토 단계를 추가합니다.  
에이전트 간 작업 결과를 공유하고, 반복 호출을 제한하며, 사용자 의견이 필요한 상황을 다룹니다.

## 📖 장별 학습

| Chapter | 학습 내용 | 주요 기술·주제 |
| :---: | --- | --- |
| [Ch02](./chap02/) | 환경 설정하고 GPT API 시작하기 | Python, OpenAI API |
| [Ch03](./chap03/) | Open AI의 API로 챗봇 만들기 | 프롬프트, 챗봇 |
| [Ch04](./chap04/) | 문서와 논문을 요약하는 AI 연구원 | PDF 전처리, 텍스트 요약 |
| [Ch05](./chap05/) | 회의록을 정리하는 AI 서기 | 음성 인식, 화자 분리 |
| [Ch06](./chap06/) | GPT-4o를 이용한 AI 이미지 분석가 | Vision, 이미지 분석, TTS |
| [Ch07](./chap07/) | 최신 주식 정보를 알려 주는 AI 투자자 | Function Calling, 주식 데이터 |
| [Ch08](./chap08/) | 랭체인으로 에이전트 만들기 | LangChain, LCEL, Pydantic |
| [Ch09](./chap09/) | RAG로 문서에 기반해 답변하는 챗봇 만들기 | RAG, 벡터 검색 |
| [Ch10](./chap10/) | 인터넷 검색을 활용해 답변하는 챗봇 만들기 | 웹 검색, YouTube |
| [Ch11](./chap11/) | 로컬에서 DeepSeek-R1 모델 사용하기 | 로컬 LLM, DeepSeek |
| [Ch12](./chap12/) | 랭그래프와 친해지기 | LangGraph, 상태, 메모리 |
| [Ch13](./chap13/) | 랭그래프를 활용한 멀티에이전트 RAG 만들기 | LangGraph, RAG, 멀티에이전트 |
| [Ch14](./chap14/) | 랭그래프로 목차를 작성하는 멀티에이전트 만들기 | LangGraph, 멀티에이전트, 검색 |
| [Ch15](./chap15/) | 스스로 판단하고 작업하는 멀티에이전트 만들기 | 멀티에이전트, 작업 관리, 검토 |
| Ch16 | 인공지능 더 안전하게 활용하기 | AI 안전 |

## 💡 추가 학습 기록

책의 예제를 실습하며 필요한 도구와 개념을 별도로 정리합니다.
- [Python 가상 환경과 uv 사용법](./Note/venv_and_uv_manual.md)
- [LangChain 퀵스타트](./Note/LangChainTutorial/)
- [Ollama 퀵 가이드](./Note/Ollama/ollama_quick_manual.md)

## 🗂️ 저장소 구성

```text
learn_do_it_llm_agent/
├── chap02/ ~ chap15/      # 장별 예제와 실습
├── Note/                  # 추가 학습 기록
└── README.md
```

## 📚 참고 자료
- 『Do it! LLM을 활용한 AI 에이전트 개발 입문』
- [교보문고 도서](https://ebook-product.kyobobook.co.kr/dig/epd/ebook/E000011504732)
- [예제 저장소](https://github.com/saintdragon2/gpt_agent_2025_easyspub)