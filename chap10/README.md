# Chapter 10. 웹 검색과 유튜브 검색 도구 활용하기

LangChain과 검색 도구를 연결해 LLM이 최신 웹 정보와 유튜브 영상 자막을 참고하여 답변하도록 실습하는 예제입니다.

## 학습 내용

1. [`1_duckduckgo_search.ipynb`](./1_duckduckgo_search.ipynb)
   - DuckDuckGo 검색 결과를 프롬프트의 문맥으로 활용하기
   - 검색 결과의 웹페이지 내용을 가져와 답변에 반영하기
2. [`2_tavily_search.ipynb`](./2_tavily_search.ipynb)
   - Tavily로 웹 자료를 검색하고 원문 가져오기
   - 검색 자료를 바탕으로 출처가 포함된 보고서 생성하기
3. [`3_youtbe_summary.ipynb`](./3_youtbe_summary.ipynb)
   - 유튜브 영상을 검색하고 자막 불러오기
   - 영상 자막을 한국어로 요약하기
4. [`streamlit_with_web_search.py`](./streamlit_with_web_search.py)
   - 현재 시각과 웹 검색 도구를 사용하는 대화형 앱
5. [`streamlit_with_youtube_search.py`](./streamlit_with_youtube_search.py)
   - 웹 검색에 유튜브 영상 검색을 더한 대화형 앱
