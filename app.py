import streamlit as st
import pandas as pd
import os


st.set_page_config(page_title="Re:Festival", layout="wide")

# 파일 경로
SUGGESTION_FILE = "suggestions.csv"
RATING_FILE = "ratings.csv"
REVIEW_FILE = "reviews.csv"

# 파일 없으면 초기 생성
if not os.path.exists(SUGGESTION_FILE):
    pd.DataFrame(columns=["이름", "이메일", "내용", "축제"]).to_csv(SUGGESTION_FILE, index=False)
if not os.path.exists(RATING_FILE):
    pd.DataFrame(columns=["축제", "평점"]).to_csv(RATING_FILE, index=False)
if not os.path.exists(REVIEW_FILE):
    pd.DataFrame(columns=["축제", "작성자", "리뷰"]).to_csv(REVIEW_FILE, index=False)

# 저장 함수
def save_suggestion(name, email, content, festival):
    df = pd.DataFrame([{
        "이름": name,
        "이메일": email,
        "내용": content,
        "축제": festival
    }])
    df.to_csv(SUGGESTION_FILE, mode='a', header=False, index=False)

def load_suggestions():
    return pd.read_csv(SUGGESTION_FILE)

def save_rating(festival, rating):
    df = pd.DataFrame([{"축제": festival, "평점": rating}])
    df.to_csv(RATING_FILE, mode='a', header=False, index=False)

def get_average_rating(festival):
    if os.path.exists(RATING_FILE):
        df = pd.read_csv(RATING_FILE)
        ratings = df[df["축제"] == festival]["평점"]
        if len(ratings) > 0:
            return round(ratings.mean(), 2)
    return None

def save_review(festival, author, content):
    df = pd.DataFrame([{"축제": festival, "작성자": author, "리뷰": content}])
    df.to_csv(REVIEW_FILE, mode='a', header=False, index=False)

def load_reviews(festival):
    if os.path.exists(REVIEW_FILE):
        df = pd.read_csv(REVIEW_FILE)
        return df[df["축제"] == festival]
    return pd.DataFrame(columns=["축제", "작성자", "리뷰"])

# 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_festival" not in st.session_state:
    st.session_state.selected_festival = None

festival_list = [
    "구례 산수유꽃축제", "광양 매화축제", "무안 연꽃축제", "보성차밭 빛축제 / 녹차축제",
    "담양 대나무축제", "해남 공룡대축제", "목포뮤직플레이", "진도 신비의 바닷길 축제",
    "일림산 철쭉문화행사", "목포해상W쇼", "여수 밤바다 불꽃축제", "영광 법성포 단오제",
    "낙안읍성 민속문화축제", "함평 국향대전", "함평 국화축제", "모악산 꽃무릇축제",
    "불갑산 상사화축제", "신안 섬 라일락축제", "석류 추수 축제", "땅끝 해넘이·해맞이 축제",
    "여수 향일암 일출제", "신안 겨울꽃축제", "보성 율포해변 불꽃축제", "담양 산타축제",
    "해남 명량대첩축제"
]

festival_coords = {
    "구례 산수유꽃축제": (35.2424, 127.5257), "광양 매화축제": (35.0156, 127.6915),
    "무안 연꽃축제": (34.9906, 126.4714), "보성차밭 빛축제 / 녹차축제": (34.7717, 127.0804),
    "담양 대나무축제": (35.3215, 126.9858), "해남 공룡대축제": (34.5726, 126.6020),
    "목포뮤직플레이": (34.8118, 126.3922), "진도 신비의 바닷길 축제": (34.3164, 126.3006),
    "일림산 철쭉문화행사": (34.8352, 127.2146), "목포해상W쇼": (34.7945, 126.3775),
    "여수 밤바다 불꽃축제": (34.7435, 127.7374), "영광 법성포 단오제": (35.2786, 126.5094),
    "낙안읍성 민속문화축제": (34.9319, 127.3844), "함평 국향대전": (35.0652, 126.5174),
    "함평 국화축제": (35.0652, 126.5174), "모악산 꽃무릇축제": (35.6545, 127.0758),
    "불갑산 상사화축제": (35.0053, 126.5190), "신안 섬 라일락축제": (34.8412, 125.9320),
    "석류 추수 축제": (34.8652, 126.2896), "땅끝 해넘이·해맞이 축제": (34.3016, 126.5232),
    "여수 향일암 일출제": (34.7181, 127.7454), "신안 겨울꽃축제": (34.8312, 126.1084),
    "보성 율포해변 불꽃축제": (34.7586, 127.0638), "담양 산타축제": (35.3215, 126.9858),
    "해남 명량대첩축제": (34.5430, 126.5965)
}

menu = st.sidebar.radio("📌 메뉴", ["메인", "축제 리스트", "건의 모아보기"])

# 메인 페이지
if menu == "메인":
    st.session_state.page = "home"
    st.title("Re:Festival - 전라남도 축제 개혁 프로젝트")
    st.header("🎉 전라남도 축제, 이대로 괜찮을까요?")
    st.image("photo1.png", width=1000)
    st.markdown("""
전라남도 축제는 해마다 수십 개가 열리지만,  
대부분 비슷한 구성과 반복되는 콘텐츠로 시민들의 관심에서 멀어지고 있습니다.

**이제는 바꿔야 할 때입니다.**  
이 사이트는 전남 축제를 개선하고자 하는 사람들의 의견과 대안을 모으는 공간입니다.
""")

# 축제 리스트
elif menu == "축제 리스트":
    if st.session_state.page == "home":
        st.title("📋 전라남도 축제 리스트")
        for fest in festival_list:
            avg = get_average_rating(fest)
            label = f"{fest} {'⭐ ' + str(avg) if avg else ''}"
            if st.button(label):
                st.session_state.page = "festival_detail"
                st.session_state.selected_festival = fest

    elif st.session_state.page == "festival_detail":
        fest = st.session_state.selected_festival
        st.title(f"🔍 {fest}")

        if st.button("← 축제 목록으로 돌아가기"):
            st.session_state.page = "home"
            st.session_state.selected_festival = None

        if fest in festival_coords:
            lat, lon = festival_coords[fest]
            st.subheader("📍 축제 위치")
            st.map(pd.DataFrame([{"lat": lat, "lon": lon}]), zoom=12)

        st.write("### 📌 의견을 작성해주세요.")
        with st.form("suggestion_form_detail"):
            name = st.text_input("이름")
            email = st.text_input("이메일 (선택)")
            suggestion = st.text_area("건의 내용을 입력해주세요")
            submitted = st.form_submit_button("제출")
            if submitted:
                save_suggestion(name, email, suggestion, fest)
                st.success("의견이 성공적으로 제출되었습니다. 감사합니다!")

        st.write("### ⭐ 평점 (1~5)")
        rating = st.slider("이 축제를 어떻게 평가하시겠습니까?", 1, 5, 3)
        if st.button("평점 제출"):
            save_rating(fest, rating)
            st.success(f"평점 {rating}점이 저장되었습니다.")

        avg_rating = get_average_rating(fest)
        if avg_rating:
            st.info(f"현재 평균 평점: ⭐ {avg_rating}")

        st.write("### 💬 리뷰 작성")
        with st.form("review_form"):
            review_author = st.text_input("작성자 이름")
            review_text = st.text_area("리뷰를 입력해주세요")
            review_submitted = st.form_submit_button("리뷰 등록")
            if review_submitted:
                if review_author.strip() and review_text.strip():
                    save_review(fest, review_author, review_text)
                    st.success("리뷰가 등록되었습니다.")
                else:
                    st.warning("이름과 리뷰를 모두 입력해주세요.")

        st.write("### 📢 리뷰 목록")
        review_df = load_reviews(fest)
        if review_df.empty:
            st.info("아직 등록된 리뷰가 없습니다.")
        else:
            for idx, row in review_df[::-1].iterrows():
                st.markdown(f"<div style='border:1px solid #ccc; border-radius:8px; padding:10px; margin-bottom:10px;'>"
                            f"<b>{row['작성자']}</b>님의 리뷰<br>"
                            f"{row['리뷰']}</div>", unsafe_allow_html=True)

# 건의 모아보기
elif menu == "건의 모아보기":
    st.markdown("## 📖 제출된 건의 모아보기")
    df = load_suggestions()
    if df.empty:
        st.info("아직 제출된 건의가 없습니다.")
    else:
        for idx, row in df[::-1].iterrows():
            st.markdown(f"<div style='border:1px solid #ccc; border-radius:8px; padding:10px; margin-bottom:10px;'>"
                        f"<b>✉️ {row['이름']}</b>님의 의견<br>"
                        f"<b>📍 관련 축제:</b> {row['축제']}<br>"
                        f"<b>📝 내용:</b> {row['내용']}</div>", unsafe_allow_html=True)
