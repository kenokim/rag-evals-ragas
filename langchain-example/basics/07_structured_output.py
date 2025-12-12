from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. 원하는 출력 구조 정의 (Pydantic)
# .with_structured_output()을 사용할 때는 모델이 더 직관적으로 이해할 수 있는 구조가 좋습니다.
class MovieReview(BaseModel):
    title: str = Field(description="영화 제목")
    rating: int = Field(description="영화 평점 (1-10점)", min_value=1, max_value=10)
    summary: str = Field(description="영화의 간단한 줄거리 요약 (한 문장)")
    genres: List[str] = Field(description="영화 장르 리스트 (예: 액션, 로맨스 등)")
    is_recommended: bool = Field(description="추천 여부")

# 2. 모델 설정
# Gemini 모델은 function calling을 지원하므로 structured output을 잘 생성합니다.
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# 3. Structured Output 설정
# .with_structured_output() 메서드를 사용하여 출력 스키마를 강제합니다.
# 이 방식은 PydanticOutputParser보다 더 안정적이고 코드가 간결합니다.
structured_llm = model.with_structured_output(MovieReview)

# 4. 프롬프트 정의
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 영화 평론가입니다. 사용자가 영화에 대해 물어보면 구조화된 리뷰를 반환하세요."),
    ("user", "{movie_name}에 대한 리뷰를 작성해줘."),
])

# 5. 체인 연결
chain = prompt | structured_llm

# 6. 실행
def print_review(movie_name: str):
    print(f"\nRequesting review for: {movie_name}...")
    try:
        review = chain.invoke({"movie_name": movie_name})
        
        # 결과는 Pydantic 객체로 반환됩니다.
        print(f"--- {review.title} 리뷰 ---")
        print(f"평점: {review.rating}/10 {'⭐️' * review.rating}")
        print(f"장르: {', '.join(review.genres)}")
        print(f"요약: {review.summary}")
        print(f"추천: {'✅ 강력 추천' if review.is_recommended else '❌ 비추천'}")
        
    except Exception as e:
        print(f"Error processing {movie_name}: {e}")

if __name__ == "__main__":
    print("=== LangChain .with_structured_output() 예제 ===")
    print_review("인셉션")
    print_review("기생충")
