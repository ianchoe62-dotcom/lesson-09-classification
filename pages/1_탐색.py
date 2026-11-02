import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="데이터 탐색 - 뇌졸중 예측 실습실", page_icon="📊", layout="wide"
)

st.title("📊 뇌졸중 데이터 탐색 실습실")
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

# 1. 나이와 평균 혈당의 분포 (히스토그램 2개 나란히)
st.subheader("1. 나이와 평균 혈당 분포")
col1, col2 = st.columns(2)

with col1:
  fig_age = px.histogram(
      df,
      x="age",
      nbins=30,
      title="나이(Age) 분포",
      labels={"age": "나이", "count": "사람 수"},
  )
  st.plotly_chart(fig_age, use_container_width=True)

with col2:
  fig_glucose = px.histogram(
      df,
      x="avg_glucose_level",
      nbins=30,
      title="평균 혈당(Avg Glucose Level) 분포",
      labels={"avg_glucose_level": "평균 혈당", "count": "사람 수"},
  )
  st.plotly_chart(fig_glucose, use_container_width=True)

st.markdown("---")

# 2. 뇌졸중 유무에 따른 나이와 평균 혈당 비교 (상자그림 2개 + 평균값 표)
st.subheader("2. 뇌졸중 유무에 따른 나이 및 평균 혈당 비교")

df_plot = df.copy()
df_plot["stroke_label"] = df_plot["stroke"].map({0: "정상 (0)", 1: "뇌졸중 (1)"})

col1, col2 = st.columns(2)

with col1:
  fig_box_age = px.box(
      df_plot,
      x="stroke_label",
      y="age",
      title="뇌졸중 유무에 따른 나이 비교",
      labels={"stroke_label": "뇌졸중 여부", "age": "나이"},
  )
  st.plotly_chart(fig_box_age, use_container_width=True)

with col2:
  fig_box_glucose = px.box(
      df_plot,
      x="stroke_label",
      y="avg_glucose_level",
      title="뇌졸중 유무에 따른 평균 혈당 비교",
      labels={"stroke_label": "뇌졸중 여부", "avg_glucose_level": "평균 혈당"},
  )
  st.plotly_chart(fig_box_glucose, use_container_width=True)

# 두 그룹의 평균값 표
st.markdown("##### 📌 두 그룹의 평균값 요약")
mean_table = df.groupby("stroke")[["age", "avg_glucose_level"]].mean().reset()
mean_table["stroke"] = mean_table["stroke"].map(
    {0: "정상 (0)", 1: "뇌졸중 (1)"}
)
mean_table.columns = ["뇌졸중 여부", "나이 평균", "평균 혈당 평균"]
st.dataframe(mean_table, use_container_width=True)

st.markdown("---")

# 3. 고혈압/심장병과 뇌졸중 비율 막대그래프
st.subheader("3. 고혈압 및 심장병에 따른 뇌졸중 비율")

col1, col2 = st.columns(2)

with col1:
  hyp_stroke = df.groupby("hypertension")["stroke"].mean().reset()
  hyp_stroke["hypertension"] = hyp_stroke["hypertension"].map(
      {0: "고혈압 없음", 1: "고혈압 있음"}
  )
  hyp_stroke["stroke_percent"] = hyp_stroke["stroke"] * 100
  fig_hyp = px.bar(
      hyp_stroke,
      x="hypertension",
      y="stroke_percent",
      title="고혈압 여부에 따른 뇌졸중 비율 (%)",
      text_auto=".2f",
      labels={"hypertension": "고혈압 여부", "stroke_percent": "뇌졸중 비율 (%)"},
  )
  st.plotly_chart(fig_hyp, use_container_width=True)

with col2:
  heart_stroke = df.groupby("heart_disease")["stroke"].mean().reset()
  heart_stroke["heart_disease"] = heart_stroke["heart_disease"].map(
      {0: "심장병 없음", 1: "심장병 있음"}
  )
  heart_stroke["stroke_percent"] = heart_stroke["stroke"] * 100
  fig_heart = px.bar(
      heart_stroke,
      x="heart_disease",
      y="stroke_percent",
      title="심장병 여부에 따른 뇌졸중 비율 (%)",
      text_auto=".2f",
      labels={"heart_disease": "심장병 여부", "stroke_percent": "뇌졸중 비율 (%)"},
  )
  st.plotly_chart(fig_heart, use_container_width=True)

st.markdown("---")

# 4. 체질량지수(bmi) 결측치 그룹과 전체 뇌졸중 비율 비교 표
st.subheader("4. 체질량지수(bmi) 결측치 그룹 vs 전체 뇌졸중 비율 비교")

total_stroke_ratio = (df["stroke"].sum() / len(df)) * 100

bmi_null_df = df[df["bmi"].isnull()]
bmi_null_count = len(bmi_null_df)
if bmi_null_count > 0:
  bmi_null_stroke_ratio = (bmi_null_df["stroke"].sum() / bmi_null_count) * 100
else:
  bmi_null_stroke_ratio = 0.0

comparison_data = {
    "구분": ["전체 데이터", "BMI 비어 있는 사람들 (결측치)"],
    "인원 수": [len(df), bmi_null_count],
    "뇌졸중 환자 수": [
        int(df["stroke"].sum()),
        int(bmi_null_df["stroke"].sum()) if bmi_null_count > 0 else 0,
    ],
    "뇌졸중 비율 (%)": [
        f"{total_stroke_ratio:.2f}%",
        f"{bmi_null_stroke_ratio:.2f}%",
    ],
}
comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True)

st.markdown("---")

# 5. 흡연 상태의 값마다 사람 수 세기 표
st.subheader("5. 흡연 상태(Smoking Status)별 사람 수")

smoking_counts = df["smoking_status"].value_counts().reset_index()
smoking_counts.columns = ["흡연 상태", "사람 수"]
st.dataframe(smoking_counts, use_container_width=True)
