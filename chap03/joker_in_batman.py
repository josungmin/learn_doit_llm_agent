from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# ② 
response = client.chat.completions.create(
    model="gpt-5.4-mini",
    # 단순한 정보 전달이 아닌 문학적인 역할극이 필요한 상황이기 때문에 temperature 값을 1에 가깝게 설정한다.
    # 0에 가깝게 설정된 경우 기계적인 답변을 할 가능성이 크다.
    temperature=0.9,
    messages=[
        {"role": "system", "content": "너는 배트맨에 나오는 조커야. 조커의 악당 캐릭터에 맞게 답변해줘"},
        {"role": "user", "content": "세상에서 누가 제일 아름답니?"},
    ]
)

print(response)

print('----')
print(response.choices[0].message.content) 