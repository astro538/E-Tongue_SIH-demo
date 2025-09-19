import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------
# Initial Herb Data
# ---------------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Herb": ["Tulsi", "Basil", "Mint", "Oregano", "Thyme"],
        "Property1": [0.2, 0.5, 0.8, 0.3, 0.6],
        "Property2": [0.7, 0.4, 0.9, 0.2, 0.5]
    })

st.title("🌿 Herb Fingerprint App")

# ---------------------------
# Select App Option
# ---------------------------
option = st.selectbox("Choose an option:", 
                      ["Match Fingerprint", "Check Adulteration", "Enter New Dataset"])

# ---------------------------
# Option 1: Match Fingerprint
# ---------------------------
if option == "Match Fingerprint":
    st.write("### Enter Unknown Herb Properties")
    p1 = st.number_input("Enter Property 1 value:", min_value=0.0, max_value=1.0, step=0.01)
    p2 = st.number_input("Enter Property 2 value:", min_value=0.0, max_value=1.0, step=0.01)

    if st.button("Find Matching Herb"):
        df = st.session_state.df.copy()
        df["distance"] = np.sqrt((df["Property1"] - p1)**2 + (df["Property2"] - p2)**2)
        best_match = df.loc[df["distance"].idxmin()]
        
        if best_match["distance"] == 0:
            st.success(f"✅ Exact Match Found: **{best_match['Herb']}**")
        else:
            st.warning(f"⚠️ No exact match. Closest Match: **{best_match['Herb']}** (distance = {best_match['distance']:.2f})")

# ---------------------------
# Option 2: Check Adulteration
# ---------------------------
elif option == "Check Adulteration":
    st.write("### Check for Adulteration")
    herb_name = st.text_input("Enter Herb Name to check adulteration:").title()
    p1 = st.number_input("Enter Property 1 value:", min_value=0.0, max_value=1.0, step=0.01, key="adul_p1")
    p2 = st.number_input("Enter Property 2 value:", min_value=0.0, max_value=1.0, step=0.01, key="adul_p2")

    if st.button("Check Adulteration"):
        df = st.session_state.df.copy()
        if herb_name in df["Herb"].values:
            herb_row = df[df["Herb"] == herb_name].iloc[0]
            distance = np.sqrt((herb_row["Property1"] - p1)**2 + (herb_row["Property2"] - p2)**2)
            if distance == 0:
                st.success(f"✅ No Adulteration Detected for **{herb_name}**")
            else:
                st.error(f"⚠️ Adulteration Detected in **{herb_name}**! (distance = {distance:.2f})")
        else:
            st.error("Herb not found in the dataset.")

# ---------------------------
# Option 3: Enter New Dataset
# ---------------------------
elif option == "Enter New Dataset":
    st.write("### Add a New Herb to Dataset")
    new_herb = st.text_input("Enter New Herb Name:").title()
    new_p1 = st.number_input("Enter Property 1 value:", min_value=0.0, max_value=1.0, step=0.01, key="new_p1")
    new_p2 = st.number_input("Enter Property 2 value:", min_value=0.0, max_value=1.0, step=0.01, key="new_p2")

    if st.button("Add Herb"):
        if new_herb and new_herb not in st.session_state.df["Herb"].values:
            st.session_state.df = pd.concat([
                st.session_state.df,
                pd.DataFrame({"Herb": [new_herb], "Property1": [new_p1], "Property2": [new_p2]})
            ], ignore_index=True)
            st.success(f"✅ Herb **{new_herb}** added to dataset!")
        else:
            st.warning("Herb already exists or name is empty.")

# ---------------------------
# Show Updated Dataset
# ---------------------------
st.write("### Current Herb Dataset")
st.table(st.session_state.df)
