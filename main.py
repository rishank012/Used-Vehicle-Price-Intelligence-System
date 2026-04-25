# dashboard.py
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Used Vehicle Price Intelligence", layout="centered")


@st.cache_data
def load_data():
    return pd.read_csv("data/cars_cleaned.csv")


df = load_data()

st.title("🚗 Used Vehicle Price Intelligence System")
st.markdown("Fair pricing • Fraud detection • Feature insights")

# --- User Inputs with Suggestions ---
car_input = st.text_input(
    "Enter Car Name (e.g. Swift, Creta, i20)").strip().lower()
fuel_input = st.text_input("Enter Fuel Type (optional)").strip().lower()
region_input = st.text_input("Enter Region/City (optional)").strip().lower()

# Suggest car names dynamically
if car_input:
    suggestions = df["car_name"].unique()
    matches = [c for c in suggestions if car_input in c.lower()]
    if matches:
        st.info("Suggestions: " + ", ".join(matches))

# --- Region mapping dictionary ---
region_map = {
    "delhi": "DL", "new delhi": "DL", "dl": "DL",
    "haryana": "HR", "hr": "HR",
    "uttar pradesh": "UP", "up": "UP", "lucknow": "UP", "noida": "UP",
    "uttarakhand": "UK", "uk": "UK", "dehradun": "UK",
    "punjab": "PB", "pb": "PB", "chandigarh": "PB",
    "maharashtra": "MH", "mh": "MH", "mumbai": "MH", "pune": "MH",
    "karnataka": "KA", "ka": "KA", "bangalore": "KA",
    "west bengal": "WB", "wb": "WB", "kolkata": "WB",
    "tamil nadu": "TN", "tn": "TN", "chennai": "TN"
}

region_code = None
if region_input in region_map:
    region_code = region_map[region_input]

# --- Flexible Filtering ---
fdf = df.copy()
if car_input:
    fdf = fdf[fdf["car_name"].str.lower().str.contains(car_input)]
if fuel_input:
    fdf = fdf[fdf["fuel_type"].str.lower().str.contains(fuel_input)]
if region_code:
    fdf = fdf[fdf["region"].str.upper().str.contains(region_code)]

if fdf.empty:
    st.warning("No listings found. Try entering only car name or check spelling.")
else:
    row = fdf.iloc[0]  # first match for demo

    # --- Show Car Details ---
    st.subheader("📋 Car Details")
    st.write(f"**Car Name:** {row['car_name']}")
    st.write(f"**Variant:** {row['variant']}")
    st.write(f"**Owner Type:** {row['owner_type']}")
    st.write(f"**Transmission:** {row['transmission']}")
    st.write(f"**Fuel Type:** {row['fuel_type']}")
    st.write(f"**Region:** {row['region']}")
    st.write(f"**KM Driven:** {row['km_driven']} km")

    # --- Price Analysis ---
    st.subheader("💰 Price Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fair Price (Estimate)", f"₹{row['fair_price']:.0f}")
    col2.metric("Listing Price (Seller)", f"₹{row['price']:.0f}")
    col3.metric("Price Difference", f"{row['deviation_pct']:.2%}")

    # --- Fraud/Manipulation Check ---
    st.subheader("⚠️ Manipulation Risk")
    prob = row["manipulation_prob"]
    if prob > 0.5:
        st.error(f"High Risk of Manipulation ({prob:.0%})")
    else:
        st.success(f"Likely Genuine ({prob:.0%})")

    # --- Explanation ---
    st.subheader("📝 Explanation")
    explanation = []
    if row["deviation_pct"] > 0.2:
        explanation.append(
            "Seller asking significantly higher than fair price.")
    elif row["deviation_pct"] < -0.2:
        explanation.append(
            "Seller asking unusually low price (possible scam).")
    else:
        explanation.append("Price is within normal range.")

    if row["km_driven"] > 100000:
        explanation.append("High km driven reduces resale value.")
    if "2nd" in row["owner_type"].lower():
        explanation.append("Second owner usually lowers resale value.")
    if row["transmission"].lower() == "automatic":
        explanation.append("Automatic cars usually have higher resale value.")

    st.write(" • " + "\n • ".join(explanation))
