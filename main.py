import streamlit as st
import plotly.graph_objects as go
import numpy as np
import vpython as vp

# 웹사이트 제목 설정
st.title("행성 식현상(Transit) 시뮬레이션")

# 사이드바에 입력 변수 설정
st.sidebar.header("변수 설정")

# 행성 반경 슬라이더 (단위: 지구 반경)
planet_radius_earth = st.sidebar.slider("행성 반경 (지구 반경)", 0.5, 2.0, 1.0, 0.1)
planet_radius = planet_radius_earth * 6371  # 지구 반경 (km) 기준

# 항성 반경 슬라이더 (단위: 태양 반경)
star_radius_sun = st.sidebar.slider("항성 반경 (태양 반경)", 0.5, 2.0, 1.0, 0.1)
star_radius = star_radius_sun * 696340  # 태양 반경 (km) 기준

# 행성과 항성 사이 거리 슬라이더 (단위: AU)
distance_au = st.sidebar.slider("행성과 항성 사이 거리 (AU)", 0.1, 5.0, 1.0, 0.1)
distance = distance_au * 1.496e8  # AU를 km로 변환

# 항성 온도 슬라이더 (단위: 1,000K)
star_temp_k = st.sidebar.slider("항성 온도 (1,000K)", 1.0, 20.0, 5.0, 0.5)
star_temp = star_temp_k * 1000

# 항성 밝기 계산 함수
def calculate_star_brightness(star_radius, planet_radius, distance):
    # 정사영 공식을 활용한 밝기 감소율 계산
    # 행성의 면적 / 항성의 면적
    area_ratio = (planet_radius / star_radius)**2
    # 밝기 변화율: 1 - (행성의 면적 / 항성의 면적)
    brightness_change = 1 - area_ratio
    return brightness_change

# 밝기 변화 계산
brightness_change = calculate_star_brightness(star_radius, planet_radius, distance)

# 시뮬레이션 섹션
st.header("시뮬레이션 결과")

# 밝기 변화 그래프 (Plotly)
st.subheader("항성의 밝기 변화 그래프")

# x축: 행성의 위치, y축: 밝기 변화
x = np.linspace(-star_radius - planet_radius, star_radius + planet_radius, 1000)
y = np.ones_like(x)

# 식현상 구간
transit_start = -star_radius + planet_radius
transit_end = star_radius - planet_radius

for i, pos in enumerate(x):
    # 행성이 항성 앞을 지나는 경우 (밝기 감소)
    if pos >= -planet_radius and pos <= planet_radius:
        y[i] = brightness_change

fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
fig.update_layout(
    title="행성 식현상에 따른 항성 밝기 변화",
    xaxis_title="시간 (상대적 위치)",
    yaxis_title="상대적 밝기",
    yaxis_range=[brightness_change - 0.01, 1.01]
)
st.plotly_chart(fig)

# 애니메이션 출력 (WebVPython)
st.subheader("행성 공전 애니메이션")
st.write("`웹 환경에서는 VPython이 작동하지 않을 수 있습니다. 로컬 환경에서 VPython으로 실행하면 확인 가능합니다.`")

# VPython 애니메이션 코드 (Streamlit에서는 직접 실행되지 않음)
# 웹에서 실행 가능한 형태로 변환하거나 별도 라이브러리 사용 필요
# VPython 코드를 Streamlit에서 직접 실행하는 것은 복잡하므로,
# 실제 VPython 환경에서 실행 가능한 코드를 예시로 제공합니다.
# 이 코드는 Streamlit 웹 페이지에 직접적으로 시각화되지는 않습니다.
vpython_code = """
from vpython import *

# 행성, 항성 반경 및 거리 설정 (VPython용)
planet_radius_vp = {0}
star_radius_vp = {1}
distance_vp = {2}

# 화면 설정
scene = canvas(title='행성 식현상 애니메이션', width=600, height=600)
scene.range = distance_vp * 1.5

# 항성 객체
star = sphere(pos=vector(0,0,0), radius=star_radius_vp, color=color.yellow, emissive=True)
star.shininess = 0.5
star.material = materials.emissive

# 행성 객체
planet = sphere(pos=vector(distance_vp,0,0), radius=planet_radius_vp, color=color.blue)

# 공전 궤도
orbit = ring(pos=vector(0,0,0), axis=vector(0,1,0), radius=distance_vp, thickness=distance_vp*0.01, color=color.gray(0.5))

# 조명
local_light(pos=vector(0,0,0), color=color.white)

# 애니메이션 루프
t = 0
dt = 0.01
while True:
    rate(100)
    theta = 2 * pi * t
    x = distance_vp * cos(theta)
    y = distance_vp * sin(theta)
    planet.pos = vector(x, y, 0)
    t += dt

""".format(planet_radius/10000, star_radius/10000, distance/10000) # 값을 적절히 스케일링하여 시각화

st.code(vpython_code, language='python')
