import streamlit as st
import random
from datetime import datetime, date

# 1. 응원 메시지 리스트 정의
morning_messages = [
    "{name}님, 상쾌한 아침이에요! 당신의 멋진 하루를 기대하고 응원합니다.",
    "오늘은 {name}님에게 어제보다 더 행복할 거예요. 활기차게 시작해 보세요!",
    "{name}님, 힘든 일이 있어도 괜찮아요. 당신은 이미 충분히 잘하고 있습니다.",
    "출근(등교)길, 이 노래와 메시지가 {name}님께 작은 힘이 되길 바랍니다.",
    "모닝 커피처럼 향긋하고 에너지 넘치는 하루 되세요, {name}님!", "{name}님, 잠재력을 믿으세요!", "{name}님 주변의 작은 행복들을 발견하는 하루가 되길 바랍니다.", "오늘 날씨가 어떻든, {name}님의 마음은 늘 따뜻하고 포근했으면 좋겠습니다."
]

# 2. 온도별/장르별 노래 리스트 정의 (재생 가능한 링크로 최종 확정)
song_recommendations = {
    "추워요 ❄️": {
        "발라드/R&B": [
            # 재생 오류 해결을 위해 링크를 교체했습니다.
            {"title": "눈사람", "artist": "정승환", "url": "https://youtu.be/MEqHS1bybMQ?si=FanaVN4iYxqGkknm"},  # MV 리부트 버전
            {"title": "첫 눈", "artist": "EXO", "url": "https://youtu.be/mHe3amVvtVo?si=YDevgRIjCMjJymHv"},    # SM STATION 버전
            {"title": "눈", "artist": "자이언티 (feat. 이문세)", "url": "https://youtu.be/X9UTOEcO-1s?si=2Rit0usTdoM4HIOa"}, # 공식 채널 라이브 클립
            {"title": "This Christmas", "artist": "태연", "url": "https://youtu.be/sN-kdckGLiE?si=gkfFS6Yd2C3iDwls"}, 
            {"title": "for you", "artist": "성시경", "url": "https://youtu.be/EXO4x9pCxag?si=VEVyUQIeqT-AOre4"},
        ],
        "재즈/클래식": [
            {"title": "Moon River", "artist": "Audrey Hepburn", "url": "https://youtu.be/yqiPEQFJM98?si=DnRZKYdERg2V04SL"},
            {"title": "Chopin Nocturne Op. 9 No. 2", "artist": "쇼팽", "url": "https://youtu.be/YpC4lS3GvF8"}
        ]
    },
    "적당해요 😊": {
        "K-POP/댄스": [
            {"title": "청춘찬가", "artist": "세븐틴", "url": "https://youtu.be/SHQ0tGLuY6A?si=iJEW8RWIJhGD923F"}, 
            {"title": "행운을 빌어줘", "artist": "원필", "url": "https://youtu.be/iHYTp1LuWYY?si=BIMp3ZrLNkV5zsXB"},
            {"title": "시작", "artist": "가호", "url": "https://youtu.be/O9aQXFTbCDY?si=59w94zgR-siLxKG6"}
        ],
        "POP/록": [
            {"title": "Good Day", "artist": "아이유 (IU)", "url": "https://youtu.be/jeqdYqsrsA0"},
            {"title": "Viva La Vida", "artist": "Coldplay", "url": "https://youtu.be/dvgZkm1xWPE"}
        ]
    },
    "더워요 🥵": {
        "HIPHOP/EDM": [
            {"title": "wu", "artist": "나플라", "url": "https://youtu.be/isGDGhBsOT4?si=aRh2rC-ecv2O2tqH"},
            {"title": "뜨거워 완전", "artist": "제네더질라", "url": "https://youtu.be/1JTa9bOaYI8?si=po1hisuw0pG52pph"}
        ],
        "R&B/시티팝": [
            {"title": "여름 안에서", "artist": "듀스", "url": "https://youtu.be/vV1p2f9mQkQ"},
            {"title": "Roller Coaster", "artist": "청하", "url": "https://youtu.be/hS18dCP4Eck"}
        ]
    }
}

# 3. 페이지 설정 및 제목
st.set_page_config(layout="wide")
st.title("☀️ 아침을 여는 응원 메시지 & 맞춤 노래 추천")

# 4. 사용자 입력 섹션 (Sidebar 사용)
with st.sidebar:
    st.header("사용자 설정")
    
    # 🗓️ 날짜 입력 위젯
    selected_date = st.date_input("🗓️ 날짜를 선택해 주세요", value=datetime.now().date())
    st.caption(f"선택된 날짜: {selected_date.strftime('%Y년 %m월 %d일')}")
    st.markdown("---")
    
    # 👤 사용자 이름 입력 위젯
    user_name = st.text_input("👤 당신의 이름을 입력해주세요.", value="친구")
    st.caption("이름을 입력하면 맞춤형 응원 메시지를 받을 수 있어요.")
    st.markdown("---")
    
    # ⭐ 체감 온도 선택: st.radio 위젯 (안정적인 버전) ⭐
    st.subheader("오늘의 체감 온도는?")
    temp_choice = st.radio(
        "🌡️ 당신이 느끼는 온도를 선택하세요.",
        options=list(song_recommendations.keys()),
        index=1 # 기본값은 '적당해요 😊'
    )
    
    # 🎸 장르 선택 (st.selectbox)
    available_genres = list(song_recommendations[temp_choice].keys())
    genre_choice = st.selectbox(
        "🎸 원하는 노래 장르를 선택하세요.",
        options=available_genres
    )


# 5. 선택된 날짜 표시 (메인 화면)
st.subheader(f"📅 {selected_date.strftime('%Y년 %m월 %d일, %A')}")

st.markdown("---")

# 6. 추천 요약 섹션
st.header("🎵 오늘의 맞춤 추천 설정")
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.info(f"**체감 온도**: {temp_choice}", icon="🌡️")
with col_info2:
    st.info(f"**선택 장르**: {genre_choice}", icon="🎧")
    
st.markdown("---")


# 7. 주요 응원 메시지 및 추천 노래 섹션
col1, col2 = st.columns(2)

# 응원 메시지 및 To-Do 리스트 표시
with col1:
    st.header("💖 오늘의 맞춤 응원 메시지")
    
    recommended_message_template = random.choice(morning_messages)
    final_message = recommended_message_template.format(name=user_name) 
    
    st.success(f"**\" {final_message} \"**", icon="✨")
    
    st.subheader("✅ 오늘 할 일 (To-Do)")
    st.checkbox("따뜻한 물 한 잔 마시기")
    st.checkbox("오늘 할 일 3가지 정리하기")
    st.checkbox("추천 노래 들으며 활력 충전하기")

# 추천 노래 표시
with col2:
    st.header("🎧 오늘의 맞춤 추천 음악")
    
    selected_song_list = song_recommendations[temp_choice][genre_choice]
    recommended_song = random.choice(selected_song_list)
    
    st.markdown(f"**🎶 {recommended_song['title']}** - {recommended_song['artist']}")
    
    # 유튜브 영상 임베드 (링크 최종 교체)
    st.video(recommended_song['url'])
    
st.markdown("---")
st.caption("설정(날짜/이름/온도/장르)을 변경하거나, 브라우저를 새로고침(F5)하면 앱이 업데이트됩니다.")