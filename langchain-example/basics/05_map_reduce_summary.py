import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 출처: https://python.langchain.com/docs/tutorials/summarization/
# Map-Reduce 방식:
# 1. 문서를 청크로 나눔
# 2. 각 청크를 개별적으로 요약 (Map)
# 3. 요약된 내용들을 합쳐서 최종 요약 생성 (Reduce)

def main():
    # 1. 모델 설정
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # 2. 긴 텍스트 예시 (RAG에 대한 설명)
    long_text = """
    검색 증강 생성(Retrieval-Augmented Generation, RAG)은 대규모 언어 모델(LLM)의 출력을 최적화하여 응답을 생성하기 전에 학습 데이터 소스 외부의 신뢰할 수 있는 지식 베이스를 참조하도록 하는 기술입니다.
    대규모 언어 모델(LLM)은 방대한 양의 데이터를 기반으로 학습되며 수십억 개의 매개변수를 사용하여 텍스트 생성, 언어 번역, 질문 답변과 같은 작업에 대한 독창적인 결과를 생성합니다. 
    RAG는 이미 강력한 LLM의 기능을 특정 도메인이나 조직의 내부 지식 기반으로 확장하므로 모델을 다시 학습시킬 필요가 없습니다. 
    이는 LLM 결과를 개선하여 다양한 상황에서 관련성, 정확성 및 유용성을 유지하기 위한 비용 효율적인 접근 방식입니다.

    RAG가 중요한 이유
    LLM은 강력하지만 한계가 있습니다. 예를 들어, 학습 데이터에 포함되지 않은 최신 정보나 비공개 정보에는 액세스할 수 없습니다. 
    또한 '환각(Hallucination)'이라고 불리는 현상, 즉 사실이 아닌 정보를 마치 사실인 것처럼 확신을 가지고 답변하는 경우가 있습니다.
    RAG는 이러한 문제를 해결하기 위해 검색 메커니즘을 도입합니다. 사용자의 질문이 들어오면, 먼저 벡터 데이터베이스 등에서 관련 문서를 검색합니다.
    그 후 검색된 문서를 LLM에 문맥(Context)으로 함께 제공하여, LLM이 이 정보를 바탕으로 답변을 생성하도록 유도합니다.

    RAG의 작동 방식
    1. 검색(Retrieval): 사용자의 쿼리를 임베딩으로 변환하고, 벡터 데이터베이스에서 가장 유사한 청크(Chunk)를 찾습니다.
    2. 증강(Augmentation): 검색된 청크를 프롬프트에 포함시킵니다. "다음 정보를 바탕으로 질문에 답하세요"와 같은 지시문을 추가합니다.
    3. 생성(Generation): LLM이 증강된 프롬프트를 바탕으로 최종 답변을 생성합니다.

    Map-Reduce의 장점은 긴 문서를 병렬로 처리할 수 있다는 점입니다. 각 청크를 독립적으로 요약하므로 속도가 빠릅니다.
    하지만 정보가 분절되어 문맥이 끊길 수 있다는 단점도 존재합니다.
    """

    # 3. 문서 청킹 (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=x) for x in text_splitter.split_text(long_text)]
    
    print(f"--- 총 {len(docs)}개의 청크로 분할됨 ---")

    # 4. Map-Reduce 체인 로드
    # chain_type="map_reduce"를 사용하여 Map-Reduce 방식 적용
    # verbose=True로 설정하면 중간 과정을 볼 수 있습니다.
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)

    # 5. 실행
    print("--- Map-Reduce 요약 시작 ---")
    result = chain.invoke(docs)
    
    print("\n--- 최종 요약 결과 ---")
    print(result["output_text"])

if __name__ == "__main__":
    main()
