import streamlit as st

st.header("앱 UI 만들기")
user_id = st.text_input("이름", placeholder="이름")
ai_model = st.radio("학년", ["1", "2", "3"], horizontal=True)
tone = st.selectbox("반", ["1", "2", "3", "4", "5"])
ai_speed = st.select_slider("난이도",options=["매우 느림", "느림", "보통", "빠름", "실시간"],value="보통")
creativity = st.slider("점수", 0, 100, 50)
question = st.text_area("소감", placeholder="소감입니다.")
age = st.number_input("나이를 입력하세요", min_value=1, max_value=100, value=17)
question = st.text_area("AI에게 보낼 질문을 입력하세요", placeholder="여기에 소감을 작성해 주세요.")

if st.button("질문 전송하기"):
    if agree:
        st.success(f"이름: {user_id}/{ai_model}학년/{tone}반/{ai_speed}")
        st.markdown(f"""
        **점수:** {creativity}
        """)
        st.success(f"소감: {question}")
        
        else:
        st.error("⚠️ 동의 항목에 체크해야 전송이 가능합니다.")
