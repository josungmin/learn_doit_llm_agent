# Chapter 14. 멀티 에이전트 시스템 구현하기

LangGraph와 LangChain을 활용해 여러 AI 에이전트가 협력하여 사용자의 요구사항에 맞는 책의 목차를 작성하는 예제입니다. Supervisor가 작업을 배분하고, 웹 검색과 벡터 검색으로 수집한 자료를 바탕으로 목차를 생성하고 수정합니다.

## 학습 내용

1. [`1_multi_agent_tutorial.ipynb`](./1_multi_agent_tutorial.ipynb)
   - Supervisor가 작업을 계획하고 담당 에이전트를 선택하는 상태 그래프 구성하기
   - 웹 검색, 벡터 검색, 콘텐츠 전략, 사용자 소통 에이전트를 연결하기
   - 사용자와 대화하며 책의 목차를 생성하고 수정하기
2. [`2_models.ipynb`](./2_models.ipynb)
   - Pydantic으로 담당 에이전트, 작업 설명, 완료 여부와 완료 시각을 담는 `Task` 모델 정의하기
   - LLM의 작업 지시를 구조화된 출력으로 받기
3. [`3_tools.ipynb`](./3_tools.ipynb)
   - Tavily로 웹 자료를 검색하고 웹페이지 본문을 수집하기
   - 검색 결과를 JSON 파일로 저장하고 문서 청크로 나누어 Chroma에 추가하기
   - 에이전트가 호출할 수 있는 웹 검색 및 벡터 검색 도구 정의하기
4. [`4_utils.ipynb`](./4_utils.ipynb)
   - 대화 메시지, 작업 이력, 검색 쿼리와 참고 문서 메타데이터를 `data/state.json`에 저장하기
   - 작성한 목차를 `data/outline.md`에 저장하고 불러오기
