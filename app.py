
import streamlit as st
import pandas as pd
import pydeck as pdk

# تحميل البيانات
stations = pd.read_csv("srbp_station_requests_refinery.csv")
routes = pd.read_csv("srbp_routes_with_time.csv")

# إعداد الصفحة
st.set_page_config(page_title="SRBP Delivery Time Simulation", layout="wide")
st.title("🚛 Estimated Travel Time from SRBP to Stations")

# عرض جدول زمن الوصول والمسافة
st.subheader("📋 Travel Time and Distance")
stations = stations.merge(routes, left_on="Name", right_on="to_lat", how="left")
full_data = pd.read_csv("srbp_routes_with_time.csv")
st.dataframe(full_data)

# عرض خريطة المسار والمسافة
arc_layer = pdk.Layer(
    "ArcLayer",
    data=full_data,
    get_source_position=["from_lon", "from_lat"],
    get_target_position=["to_lon", "to_lat"],
    get_source_color=[0, 128, 255],
    get_target_color=[255, 100, 0],
    auto_highlight=True,
    width_scale=0.5,
    get_width=3,
    pickable=True
)

# عرض الخريطة
st.subheader("🗺️ Travel Paths with Estimated Time")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/streets-v11",
    initial_view_state=pdk.ViewState(
        latitude=24.63,
        longitude=46.77,
        zoom=11,
        pitch=45,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=stations,
            get_position='[Longitude', 'Latitude]',
            get_color='[255, 100, 0]',
            get_radius=300,
        ),
        arc_layer
    ],
))
