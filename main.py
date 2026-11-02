import json
import os
import pandas as pd
import streamlit as st

# 1. 페이지 및 브라우저 탭 설정 (제목 및 아이콘)
st.set_page_config(page_title="뇌졸중 예측 실습실", page_icon="🧠", layout="wide")

# 저장 폴더 및 파일 경로 설정
SAVE_DIR = "내_기록"
SAVE_FILE = os.path.join(SAVE_DIR, "data_info.json")

# 저장 폴더 자동 생성
os.makedirs(SAVE_DIR, exist_ok=True)


# JSON 데이터 로드 함수
def load_user_data():
  if os.path.exists(SAVE_FILE):
    try:
      with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      pass
  return {"meanings": {}, "source": ""}


# JSON 데이터 저장 함수
def save_user_data(data):
  with open(SAVE_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# 저장된 사용자 데이터 불러오기
user_records = load_user_data()

# 앱 상단 제목
st.title("🧠 뇌졸중 예측 실습실")
st.markdown("---")

# 데이터 로드
DATA_URL = "https://raw.githubusercontent.com/ianchoe62-dotcom/data/refs/heads/main/stroke.csv"


@st.cache_data
def load_data():
  return pd.read_csv(DATA_URL, encoding="utf-8")


try:
  df = load_data()
except Exception as e:
  st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
  st.stop()

# 2. 상단 4개의 숫자 카드 (Metrics)
total_count = len(df)
col_count = len(df.columns)
stroke_count = int(df["stroke"].sum())
stroke_ratio = (stroke_count / total_count) * 100 if total_count > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("전체 사람 수", f"{total_count:,}명")
m2.metric("열 개수", f"{col_count}개")
m3.metric("뇌졸중 환자 수 (stroke=1)", f"{stroke_count:,}명")
m4.metric("뇌졸중 환자 비율", f"{stroke_ratio:.2f}%")

st.markdown("---")

# 3. 열 정보 및 입력 폼
st.subheader("📋 데이터 열 정보 및 우리말 뜻")
st.caption(
    "우리말 뜻 칸을 직접 입력하고 하단의 저장 버튼을 누르면 기록이 유지됩니다."
)

cols_list = list(df.columns)
null_counts = df.isnull().sum()
dtypes = df.dtypes

with st.form("column_meaning_form"):
  updated_meanings = {}

  # 테이블 헤더
  c1, c2, c3, c4 = st.columns([2, 3, 2, 2])
  c1.markdown("**열 이름**")
  c2.markdown("**우리말 뜻**")
  c3.markdown("**값의 종류 (데이터 타입)**")
  c4.markdown("**빈 값 (결측치) 개수**")
  st.markdown("---")

  saved_meanings = user_records.get("meanings", {})

  for col_name in cols_list:
    c1, c2, c3, c4 = st.columns([2, 3, 2, 2])
    c1.text(col_name)
    default_val = saved_meanings.get(col_name, "")
    updated_meanings[col_name] = c2.text_input(
        label=f"meaning_{col_name}",
        value=default_val,
        label_visibility="collapsed",
        key=f"input_{col_name}",
    )
    c3.text(str(dtypes[col_name]))
    c4.text(f"{null_counts[col_name]}개")

  st.markdown("")

  # 4. 데이터 출처 입력
  st.subheader("📌 데이터 출처")
  current_source = user_records.get("source", "")
  updated_source = st.text_area(
      "교재에 적힌 데이터 출처를 아래에 입력해 주세요.",
      value=current_source,
      height=100,
      key="source_input",
  )

  # 저장 버튼
  submit_btn = st.form_submit_button("💾 내용 저장하기")
  if submit_btn:
    save_data_payload = {
        "meanings": updated_meanings,
        "source": updated_source,
    }
    save_user_data(save_data_payload)
    st.success("내_기록/data_info.json 파일에 성공적으로 저장되었습니다!")
    st.rerun()

st.markdown("---")

# 5. 상위 5줄 데이터 미리보기
st.subheader("🔍 데이터 미리보기 (상위 5줄)")
st.dataframe(df.head(5), use_container_width=True)streamlit
pandas
plotly
scikit-learn
