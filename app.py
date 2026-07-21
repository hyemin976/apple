import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧠 AI 토론 연습")

topic = st.text_input("토론 주제를 입력하세요")

position = st.radio(
    "나의 입장",
    ["찬성", "반대", "랜덤"]
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

너의 입장은 반드시 사용자의 입장과 반대이다.

절대로 사용자의 편을 들지 말고,
항상 "{ai_position}" 입장에서만 토론하라.

먼저 자신의 주장 3개를 제시하고,
마지막에 "당신의 의견은 무엇인가요?"라고 질문하라.
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
