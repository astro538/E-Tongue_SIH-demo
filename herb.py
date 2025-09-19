import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------
# Reference Herb Data
# ---------------------------
herbs_data = {
    "Herb": ["Tulsi", "Basil", "Mint", "Oregano", "Thyme"],
    "Property1": [0.2, 0.5, 0.8, 0.3, 0.6],
    "Property2": [0.7, 0.4, 0.9, 0.2, 0.5]
}
df = pd.DataFrame(herbs_data)

st.title("🌿 Herb Fingerprint Matcher")

st.write("### Reference Herb Table")
st.table(df)

# ---------------------------
# User Input
# ---------------------------
st.write("### Enter Unknown Herb Properties")
p1 = st.number_input("Enter Property 1 value:", min_value=0.0, max_value=1.0, step=0.01)
p2 = st.number_input("Enter Property 2 value:", min_value=0.0, max_value=1.0, step=0.01)

# ---------------------------
# Matching Logic
# ---------------------------
if st.button("Find Matching Herb"):
    # Calculate distance from each herb fingerprint
    df["distance"] = np.sqrt((df["Property1"] - p1)**2 + (df["Property2"] - p2)**2)

    # Find closest match
    best_match = df.loc[df["distance"].idxmin()]

    if best_match["distance"] == 0:
        st.success(f"✅ Exact Match Found: **{best_match['Herb']}**")
    else:
        st.warning(f"⚠️ No exact match. Closest Match: **{best_match['Herb']}** (distance = {best_match['distance']:.2f})")
