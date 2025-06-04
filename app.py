
import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime, timedelta

# تحميل البيانات
stations = pd.read_csv("srbp_stations_fixed_daily.csv")

# إعداد الصفحة
st.set_page_config(page_title="SRBP Slot Booking with Demand", layout="wide")
st.title("🛢️ SRBP Slot Booking + Daily Demand Simulation")

# اختيار محطة
station_selected = st.selectbox("Select Station", stations[stations["Source"] != "Main Bulk Plant"]["Name"].tolist())
station_data = stations[stations["Name"] == station_selected].iloc[0]

# عرض الكميات اليومية المطلوبة
st.markdown("### 📦 Daily Demand (bbl)")
st.write(f"Diesel: {station_data['Diesel_daily_bbl']} bbl/day")
st.write(f"Gasoline 91: {station_data['Gasoline91_daily_bbl']} bbl/day")
st.write(f"Gasoline 95: {station_data['Gasoline95_daily_bbl']} bbl/day")

# حجز الوقت
st.markdown("### 🕒 Book a Slot")
selected_time = st.time_input("Choose time for loading", value=datetime.now().time())
loading_duration = st.slider("Estimated loading duration (minutes)", 10, 60, 30, step=5)

arrival_time = datetime.combine(datetime.today(), selected_time)
departure_time = arrival_time + timedelta(minutes=loading_duration)

st.success(f"✅ Slot booked for {station_selected} from {arrival_time.strftime('%H:%M')} to {departure_time.strftime('%H:%M')}")

# عرض الخريطة
st.subheader("🗺️ Map View of Station")
station_map = pd.DataFrame([{
    "Latitude": station_data["Latitude"],
    "Longitude": station_data["Longitude"],
    "Name": station_data["Name"],
    "color": [255, 100, 0]
}])

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/streets-v11",
    initial_view_state=pdk.ViewState(
        latitude=station_data["Latitude"],
        longitude=station_data["Longitude"],
        zoom=13,
        pitch=30,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=station_map,
            get_position='[Longitude, Latitude]',
            get_color='color',
            get_radius=300,
        ),
        pdk.Layer(
            "TextLayer",
            data=station_map,
            get_position='[Longitude, Latitude]',
            get_text='Name',
            get_size=16,
            get_color=[0, 0, 0],
            get_alignment_baseline="'bottom'"
        )
    ],
))
