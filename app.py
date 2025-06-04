
import streamlit as st
import pandas as pd
import pydeck as pdk

# بيانات المحطات ومواقعها
stations = pd.DataFrame({
    'Name': ['Al Muhsen Station', 'Naft', 'Al Daleel', 'Gas Station 1', 'Gas Station 2'],
    'Latitude': [24.734223, 24.730529, 24.691334, 24.723658, 24.708406],
    'Longitude': [46.794444, 46.788447, 46.718527, 46.797141, 46.687040],
})

# موقع محطة SRBP
srbp = {'Name': 'SRBP (South Riyadh Bulk Plant)', 'Latitude': 24.724824, 'Longitude': 46.757489}
stations = pd.concat([pd.DataFrame([srbp]), stations], ignore_index=True)

# سعة وهمية للمنتجات
capacity = {
    'Diesel': 65000,
    'Gasoline 91': 52000,
    'Gasoline 95': 26000
}

# تطبيق Streamlit
st.set_page_config(page_title="SRBP Slot Management", layout="wide")
st.title("🚛 SRBP Slot Booking Simulation")

product = st.selectbox("Select Product", list(capacity.keys()))
requested_qty = st.slider("Requested Quantity (liters)", 5000, 30000, 10000, step=1000)
current_load = st.slider("Current SRBP Load (liters)", 0, capacity[product], int(capacity[product]*0.6), step=1000)

remaining = capacity[product] - current_load
st.metric(label="Remaining Capacity", value=f"{remaining:,} L", delta=f"-{requested_qty:,} L")

if requested_qty > remaining:
    st.error("⛔ Capacity Exceeded! Try later or redirect to NRBP.")
    redirect = st.checkbox("Redirect to NRBP?")
    if redirect:
        st.success("✅ Request routed to NRBP.")
else:
    st.success("✅ Slot Confirmed at SRBP.")

# عرض الخريطة
st.subheader("Map of SRBP and Stations")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/streets-v11",
    initial_view_state=pdk.ViewState(
        latitude=srbp["Latitude"],
        longitude=srbp["Longitude"],
        zoom=11,
        pitch=45,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=stations,
            get_position='[Longitude, Latitude]',
            get_color='[0, 100, 200, 160]',
            get_radius=200,
        ),
        pdk.Layer(
            "TextLayer",
            data=stations,
            get_position='[Longitude, Latitude]',
            get_text='Name',
            get_size=14,
            get_color=[0, 0, 0],
            get_alignment_baseline="'bottom'"
        )
    ],
))
