import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 출처: https://python.langchain.com/docs/tutorials/summarization/
# Refine 방식:
# 1. 첫 번째 청크를 요약합니다.
# 2. 첫 번째 요약문과 두 번째 청크를 LLM에 전달하여, 새로운 정보(두 번째 청크)를 반영해 요약을 업데이트(Refine)합니다.
# 3. 모든 청크에 대해 이 과정을 순차적으로 반복합니다.

def main():
    # 1. 모델 설정
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # 2. 긴 텍스트 예시 (에이전트 시스템에 대한 설명)
    long_text = """
    AI 에이전트(AI Agent)는 단순히 질문에 답하는 것을 넘어, 주어진 목표를 달성하기 위해 스스로 계획을 세우고 도구(Tool)를 사용하여 행동하는 시스템을 말합니다.
    기존의 LLM이 수동적인 지식 검색기였다면, 에이전트는 능동적인 문제 해결사입니다.
    
    에이전트의 주요 구성 요소:
    1. 프로파일링(Profiling): 에이전트의 역할과 성격을 정의합니다.
    2. 메모리(Memory): 과거의 행동과 대화를 기억하여 일관된 처리를 돕습니다. 단기 기억과 장기 기억으로 나뉩니다.
    3. 계획(Planning): 복잡한 작업을 작은 단계로 나누는 과정입니다. Chain of Thought(CoT)나 Tree of Thoughts(ToT) 같은 기법이 사용됩니다.
    4. 도구 사용(Tool Use): 웹 검색, 계산기, API 호출 등 외부 세계와 상호작용할 수 있는 능력을 부여합니다.

    Refine 방식은 순차적(Sequential)으로 처리되므로 Map-Reduce보다 시간이 더 걸릴 수 있습니다.
    하지만 앞부분의 문맥(Context)을 유지하면서 점진적으로 요약을 발전시키기 때문에, 
    글의 흐름이 중요하거나 상호 연관성이 높은 텍스트를 요약할 때 더 높은 품질의 결과를 보여줍니다.
    
    LangChain에서는 load_summarize_chain 함수에 chain_type="refine"을 인자로 주어 이 방식을 쉽게 구현할 수 있습니다.
    이 방식은 토큰 비용이 많이 들 수 있으나, 정교한 요약이 필요할 때 적합합니다.
    """

    # 3. 문서 청킹 (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    docs = [Document(page_content=x) for x in text_splitter.split_text(long_text)]
    
    print(f"--- 총 {len(docs)}개의 청크로 분할됨 ---")

    # 4. Refine 체인 로드
    # chain_type="refine"을 사용하여 Refine 방식 적용
    # 순차적으로 진행되므로 병렬 처리는 불가능합니다.
    chain = load_summarize_chain(llm, chain_type="refine", verbose=True)

    # 5. 실행
    print("--- Refine 요약 시작 (순차적 실행) ---")
    result = chain.invoke(docs)
    
    print("\n--- 최종 요약 결과 ---")
    print(result["output_text"])

if __name__ == "__main__":
    main()
