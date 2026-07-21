import streamlit as st
from openai import RateLimitError

try:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

except Exception as e:
    st.error(e)
st.title("🧠 AI 토론 연습")

# -----------------------
# 세션 초기화
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False

# -----------------------
# 입력
# -----------------------
topic = st.text_input("토론 주제")

position = st.radio(
    "나의 입장",
    ["찬성", "반대"]
)

difficulty = st.selectbox(
    "난이도",
    ["쉬움", "보통", "어려움"]
)

# -----------------------
# 토론 시작
# -----------------------
if st.button("토론 시작"):

    st.session_state.started = True
    st.session_state.messages = []

    prompt = f"""
    너는 토론 전문가이다.

    토론 주제:
    {topic}

    사용자는 {position} 입장이다.

    너는 반드시 사용자의 반대 입장에서 토론한다.

    난이도는 {difficulty}이다.

    먼저 자신의 주장 2~3개를 말하고
    마지막에는 질문을 하나 해라.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":"너는 토론 전문가이다."},
            {"role":"user","content":prompt}
        ]
    )

    ai = response.choices[0].message.content

    st.session_state.messages.append(
        {"role":"assistant","content":ai}
    )

# -----------------------
# 대화 출력
# -----------------------
if st.session_state.started:

    for msg in st.session_state.messages:

        if msg["role"]=="assistant":
            st.chat_message("assistant").write(msg["content"])

        else:
            st.chat_message("user").write(msg["content"])

    user_input = st.chat_input("답변을 입력하세요.")

    if user_input:

        st.session_state.messages.append(
            {"role":"user","content":user_input}
        )

        system_prompt = f"""
        너는 토론 전문가이다.

        토론 주제는
        {topic}

        사용자는 {position} 입장이다.

        너는 반드시 반대 입장을 유지한다.

        너무 공격적이지 말고
        논리적으로 반박하라.

        마지막에는 반드시 질문 하나를 해라.
        """

        messages = [
            {"role":"system","content":system_prompt}
        ]

        messages.extend(st.session_state.messages)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        ai = response.choices[0].message.content

        st.session_state.messages.append(
            {"role":"assistant","content":ai}
        )

        st.rerun()

# -----------------------
# 최종 평가
# -----------------------
if st.button("최종 피드백"):

    conversation = ""

    for msg in st.session_state.messages:
        conversation += f"{msg['role']} : {msg['content']}\n"

    prompt = f"""
    다음 토론 내용을 평가하라.

    {conversation}

    아래 형식으로 작성하라.

    ## 총점(20점)

    ## 논리성

    ## 설득력

    ## 근거 제시

    ## 반박 능력

    ## 좋았던 점

    ## 개선할 점

    ## 다음에 이렇게 말하면 더 좋다.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    st.subheader("📊 토론 피드백")
    st.write(response.choices[0].message.content)
