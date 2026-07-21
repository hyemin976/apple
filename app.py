import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧠 AI 토론 연습")

topic = st.text_input("토론 주제를 입력하세요")

position = st.radio(
    "나의 입장",
    ["찬성", "반대"]
)

difficulty = st.selectbox(
    "난이도",
    ["쉬움", "보통", "어려움"]
)

if st.button("토론 시작"):

    prompt = f"""
토론 주제는 "{topic}"이다.

사용자의 입장은 {position}이다.

난이도는 {difficulty}이다.

사용자의 입장이 찬성이면 반대 입장의 서로 다른 주장 3개를 만들어라.

사용자의 입장이 반대이면 찬성 입장의 서로 다른 주장 3개를 만들어라.

마지막에는
'당신의 의견은 무엇인가요?'
라고 질문해라.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"오류가 발생했습니다.\n\n{e}")

user_answer = st.text_area("당신의 의견을 작성하세요.")

if st.button("피드백 받기"):

    prompt = f"""
토론 주제
{topic}

학생의 답변
{user_answer}

다음 형식으로 평가하라.

논리성 : 5점 만점

설득력 : 5점 만점

근거 제시 : 5점 만점

좋은 점

부족한 점

더 설득력 있게 말하는 방법
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"오류가 발생했습니다.\n\n{e}")
