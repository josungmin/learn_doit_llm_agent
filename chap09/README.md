# Chapter 09. RAG 시스템 만들기

PDF 문서를 검색하고, 검색된 문서에 기반해 답변하는 RAG 챗봇을 만드는 예제입니다.

## 학습 내용

1. [`1_rag_basic.ipynb`](./1_rag_basic.ipynb)
   - PDF 문서를 청크로 나누고 임베딩하여 Chroma 벡터 저장소에 저장하기
   - 관련 문서 검색, 문서 기반 답변, 대화 이력을 활용한 질문 재작성 실습하기
2. [`2_rag.py`](./2_rag.py)
   - Streamlit으로 문서 기반 RAG 챗봇 실행하기
   - 검색된 문서와 페이지 정보를 함께 확인하기
3. [`retriever.py`](./retriever.py)
   - 저장된 Chroma 벡터 저장소에서 관련 문서 검색하기
   - 문서 기반 답변과 질문 재작성 체인 구성하기
