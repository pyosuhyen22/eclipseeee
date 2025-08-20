import streamlit as st
import numpy as np
import plotly.graph_objects as go
from vpython import sphere, vector, rate, color, canvas

# ---------------------
# 기본 설정
# ---------------------
st.set_page_config(page_title="식현상 시뮬레이션", layout="wide")
st.title("🌍 식현상 기반 항성 밝기 변화 시뮬레이터")

# ---------------------
# 사용자 입력
# ---------------------
st.sidebar.header("⚙️ 파라미터 설정")

R_planet = st.sidebar.slider("행성 반경 (지구 반경)", 0.1, 5.0, 1.0, 0.1)   # 지구 반경 단위
R_star = st.sidebar.slider("항성 반경 (태양 반경)", 0.5, 5.0, 1.0, 0.1)     # 태양 반경 단위
distance = st.sidebar.slider("행성과 항성 거리 (항성 반경 단위)", 2.0, 20.0, 10.0, 0.5)
T_star = st.sidebar.slider("항성 온도 (1000 K)", 2.0, 10.0, 6.0, 0.1) * 1000  # Kelvin

# ---------------------
# 광도 계산 함수
# ---------------------
def luminosity(R_star, T_star):
    # 상대적 광도 (스테판-볼츠만 법칙, 상수 제외)
    return R_star**2 * T_star**4

# 두 원의 겹치는 면적 (항성 원반과 행성 원반)
def overlap_area(Rs, Rp, d):
    if d >= Rs + Rp:  # 안겹침
        return 0.0
    if d <= abs(Rs - Rp):  # 작은 원이 큰 원 안에 완전히 포함
        return np.pi * min(Rs, Rp)**2
    r2, R2 = Rp**2, Rs**2
    alpha = np.arccos((d**2 + r2 - R2) / (2*d*Rp))
    beta  = np.arccos((d**2 + R2 - r2) / (2*d*Rs))
    return (r2 * alpha + R2 * beta -
            0.5 * np.sqrt((-d+Rp+Rs)*(d+Rp-Rs)*(d-Rp+Rs)*(d+Rp+Rs)))

# ---------------------
# 밝기 곡선 계산
# ---------------------
time = np.linspace(0, 1, 200)  # 공전 주기 정규화
brightness = []

for t in time:
    # 행성의 x좌표 (항성 앞을 가로지르는 단순 모델)
    x = (t - 0.5) * 2 * distance
    d = abs(x)  # 중심에서 거리
    A_overlap = overlap_area(R_star, R_planet/10, d)  # Rp 단위 맞춤 (대략 조정)
    A_star = np.pi * R_star**2
    flux = (A_star - A_overlap) / A_star
    brightness.append(flux)

# ---------------------
# Plotly 그래프
# ---------------------
fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=brightness, mode="lines", name="상대 밝기"))
fig.update_layout(
    title="항성 밝기 변화 (Transit Light Curve)",
    xaxis_title="시간 (공전 주기)",
    yaxis_title="상대 밝기",
    yaxis=dict(range=[min(brightness)-0.01, 1.01])
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------
# WebVPython 애니메이션
# ---------------------
st.subheader("🌌 공전 애니메이션")

# Streamlit에서 WebVPython 캔버스는 직접 보여주기 어려움 → iframe 삽입 방식
# 단독 실행 시에는 아래 코드가 VPython 창에서 실행됨
scene = canvas(title="행성 공전", width=600, height=400, background=color.black)

star = sphere(pos=vector(0,0,0), radius=R_star*0.2, color=color.yellow, emissive=True)
planet = sphere(pos=vector(distance,0,0), radius=R_planet*0.05, color=color.blue, make_trail=True)

for t in np.linspace(0, 2*np.pi, 200):
    rate(50)
    planet.pos = vector(distance*np.cos(t), distance*np.sin(t), 0)
