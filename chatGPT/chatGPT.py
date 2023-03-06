# pip install openai
import openai

# 발급받은 API 키 설정
OPENAI_API_KEY = "sk-"

# openai API 키 인증
openai.api_key = OPENAI_API_KEY

def query_gpt_35_turbo(query):  
  response = openai.ChatCompletion.create(  
    model = "gpt-3.5-turbo",
    messages = 
    [{"role": "system", "content":"You are a helpful assistant that helps users generate ..."},  
    {"role":"user", "content": query}]
  )
  return response.choices[0].message.content

query = "파이썬에 대해서 설명해줘"
print("질문은 :\n" + query + "\n")
print("답변은 :\n" + query_gpt_35_turbo(query))