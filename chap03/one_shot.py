from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-5.4-mini",
    # 유치원생 유치원생 페르소나의 '엉뚱함'과 '다양성' 유도하기 위하여 temperature 값을 1에 가깝게 설정한다.
    # 단, 정해진 패턴(동물 -> 의성어)을 정확하게 출력하는것이 목적이라면 temperature를 낮게 설정해야하는것 아닌가?
    temperature=0.9,
    messages=[
        {"role": "system", "content": "너는 유치원 학생이야. 유치원생처럼 답변해줘."},
        {"role": "user", "content": "참새"},
        {"role": "assistant", "content": "짹짹"},
        {"role": "user", "content": "오리"},
    ]
)

print(response)

print('----')
print(response.choices[0].message.content) 