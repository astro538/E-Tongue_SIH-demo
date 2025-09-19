import streamlit as st
import pandas as pd
import numpy as np
import os
import json

# ---------------------------
# Sensors
# ---------------------------
sensors = ["Voltammetric Sensor", "Biosensor", "Photochemical Sensor", "pH Sensor"]

# ---------------------------
# Initialize universal dataset
# ---------------------------
if not os.path.exists("universal_dataset.csv"):
    universal_df = pd.DataFrame({
        "Herb": ["Tulsi", "Basil", "Mint", "Oregano", "Thyme"],
        "Voltammetric Sensor": [0.2, 0.5, 0.8, 0.3, 0.6],
        "Biosensor": [0.7, 0.4, 0.9, 0.2, 0.5],
        "Photochemical Sensor": [0.3, 0.6, 0.2, 0.7, 0.4],
        "pH Sensor": [0.5, 0.1, 0.8, 0.4, 0.6]
    })
    universal_df.to_csv("universal_dataset.csv", index=False)
else:
    universal_df = pd.read_csv("universal_dataset.csv")


# ---------------------------
# Persistent Pending Requests
# ---------------------------
PENDING_REQUESTS_FILE = "pending_requests.json"
def load_pending_requests():
    if os.path.exists(PENDING_REQUESTS_FILE):
        with open(PENDING_REQUESTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_pending_requests(requests):
    with open(PENDING_REQUESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)

if "pending_requests" not in st.session_state:
    st.session_state.pending_requests = load_pending_requests()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

# ---------------------------
# Hardcoded login credentials
# ---------------------------
users = {"admin": "admin123", "user1": "user123", "user2": "user234"}

st.title("🌿 E-Tongue Herb Fingerprint Management System")

# ---------------------------
# Login
# ---------------------------
if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username or password")

# ---------------------------
# Main app after login
# ---------------------------
if st.session_state.logged_in:
    username = st.session_state.username
    user_type = "Admin" if username == "admin" else "User"
    st.subheader(f"Welcome {username} ({user_type})")

    # Load personal dataset
    personal_file = f"{username}_personal.csv"
    if os.path.exists(personal_file):
        personal_df = pd.read_csv(personal_file)
    else:
        personal_df = pd.DataFrame(columns=["Herb"] + sensors)

    # ---------------------------
    # Admin Interface
    # ---------------------------
    if user_type == "Admin":
        st.write("### Universal Herb Dataset")
        display_universal = universal_df.copy()
        display_universal.index = np.arange(1, len(display_universal)+1)  # S.No starts from 1
        st.table(display_universal)

        # Add new herb to Universal dataset
        st.write("### Add New Herb to Universal Dataset")
        with st.form("add_herb_form"):
            new_herb = st.text_input("Herb Name")
            new_sensor_values = []
            for sensor in sensors:
                value = st.number_input(f"{sensor} value", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
                new_sensor_values.append(value)
            submitted = st.form_submit_button("Add Herb")
            if submitted and new_herb:
                if new_herb in universal_df["Herb"].values:
                    st.warning(f"Herb '{new_herb}' already exists in the universal dataset.")
                else:
                    new_row = pd.DataFrame({
                        "Herb": [new_herb],
                        sensors[0]: [new_sensor_values[0]],
                        sensors[1]: [new_sensor_values[1]],
                        sensors[2]: [new_sensor_values[2]],
                        sensors[3]: [new_sensor_values[3]]
                    })
                    universal_df = pd.concat([universal_df, new_row], ignore_index=True)
                    universal_df.to_csv("universal_dataset.csv", index=False)
                    st.success(f"✅ Added {new_herb} to Universal Dataset")
                    st.rerun()

        # Remove herb from Universal dataset
        if not universal_df.empty:
            remove_herb = st.selectbox("Select Herb to Remove (Universal)", universal_df["Herb"])
            if st.button("Remove Selected Herb (Universal)"):
                universal_df = universal_df[universal_df["Herb"] != remove_herb]
                universal_df.to_csv("universal_dataset.csv", index=False)
                st.success(f"✅ Removed {remove_herb} from Universal Dataset")
                st.rerun()

        # Pending requests
        st.write("### Pending User Requests (Universal)")
        for i, req in enumerate(st.session_state.pending_requests):
            if req["type"] == "Universal":
                st.write(f"Request #{i+1} by {req['username']} to add **{req['herb']}** - Properties: {req['properties']}")
                if st.button(f"Approve #{i+1}", key=f"approve_{i}"):
                    new_row = pd.DataFrame({
                        "Herb": [req['herb']],
                        sensors[0]: [req['properties'][0]],
                        sensors[1]: [req['properties'][1]],
                        sensors[2]: [req['properties'][2]],
                        sensors[3]: [req['properties'][3]]
                    })
                    universal_df = pd.concat([universal_df, new_row], ignore_index=True)
                    universal_df.to_csv("universal_dataset.csv", index=False)
                    st.session_state.pending_requests.pop(i)
                    save_pending_requests(st.session_state.pending_requests)
                    st.rerun()
                if st.button(f"Reject #{i+1}", key=f"reject_{i}"):
                    st.session_state.pending_requests.pop(i)
                    save_pending_requests(st.session_state.pending_requests)
                    st.rerun()

    # ---------------------------
    # User Interface
    # ---------------------------
    else:
        action = st.selectbox("Choose action:", ["Match Fingerprint", "Check Adulteration", "Submit New Herb", "Remove Personal Herb"])

        # Show dataset to user
        st.write("### Your Dataset for Reference (Universal + Personal)")
        combined_df = pd.concat([universal_df, personal_df], ignore_index=True)
        display_combined = combined_df.copy()
        display_combined.index = np.arange(1, len(display_combined)+1)
        st.table(display_combined)

        # Percentage Match Function
        def get_match(df, props):
            max_distance = np.sqrt(len(props))
            df = df.copy()
            df["distance"] = np.sqrt(np.sum([(df[sensors[i]] - props[i])**2 for i in range(len(props))], axis=0))
            df["percent_match"] = 100 * (1 - df["distance"]/max_distance)
            best = df.loc[df["percent_match"].idxmax()]
            return best

        # ---------------------------
        # Match Fingerprint
        # ---------------------------
        if action == "Match Fingerprint":
            st.write("### Enter Herb Sensor Values")
            p = [st.number_input(f"{sensors[i]} value", min_value=0.0, max_value=1.0, step=0.01, key=f"match_p{i}") for i in range(4)]
            
            if st.button("Find Match"):
                best = get_match(combined_df, p)
                if best["percent_match"] >= 85:
                    st.success(f"✅ Match Found: **{best['Herb']}** ({best['percent_match']:.2f}%)")
                else:
                    st.warning(f"⚠️ No sufficient match. Closest: **{best['Herb']}** ({best['percent_match']:.2f}%)")

        # ---------------------------
        # Check Adulteration
        # ---------------------------
        elif action == "Check Adulteration":
            st.write("### Check Adulteration")
            herb_name = st.text_input("Enter Herb Name").title()
            p = [st.number_input(f"{sensors[i]} value", min_value=0.0, max_value=1.0, step=0.01, key=f"adul_p{i}") for i in range(4)]
            if st.button("Check"):
                if herb_name in combined_df["Herb"].values:
                    herb_row = combined_df[combined_df["Herb"] == herb_name].iloc[0]
                    distance = np.sqrt(sum([(herb_row[sensors[i]] - p[i])**2 for i in range(4)]))
                    percent_match = 100 * (1 - distance/np.sqrt(4))
                    if percent_match >= 85:
                        st.success(f"✅ No Adulteration Detected ({percent_match:.2f}%)")
                    else:
                        st.error(f"⚠️ Adulteration Detected! Closest match percentage: {percent_match:.2f}%")
                else:
                    st.error("Herb not found.")

        # ---------------------------
        # Submit New Herb
        # ---------------------------
        elif action == "Submit New Herb":
            st.write("### Submit New Herb")
            new_herb = st.text_input("Herb Name").title()
            props = [st.number_input(f"{sensors[i]} value", min_value=0.0, max_value=1.0, step=0.01, key=f"new_p{i}") for i in range(4)]
            update_type = st.radio("Update Type", ["Universal", "Personal"])

            if st.button("Submit Herb"):
                if new_herb:
                    if update_type == "Personal":
                        new_row = pd.DataFrame({
                            "Herb": [new_herb],
                            sensors[0]: [props[0]],
                            sensors[1]: [props[1]],
                            sensors[2]: [props[2]],
                            sensors[3]: [props[3]]
                        })
                        personal_df = pd.concat([personal_df, new_row], ignore_index=True)
                        personal_df.to_csv(personal_file, index=False)
                        st.success("✅ Added to your personal dataset!")
                    else:
                        # Universal request goes to admin
                        st.session_state.pending_requests.append({
                            "username": username,
                            "herb": new_herb,
                            "properties": props,
                            "type": "Universal"
                        })
                        save_pending_requests(st.session_state.pending_requests)
                        st.info("📨 Request submitted to admin for approval.")

        # ---------------------------
        # Remove Personal Herb
        # ---------------------------
        elif action == "Remove Personal Herb":
            st.write("### Remove a Herb from Your Personal Dataset")
            if not personal_df.empty:
                remove_herb_personal = st.selectbox("Select Herb to Remove", personal_df["Herb"])
                if st.button("Remove Selected Herb (Personal)"):
                    personal_df = personal_df[personal_df["Herb"] != remove_herb_personal]
                    personal_df.to_csv(personal_file, index=False)
                    st.success(f"✅ Removed {remove_herb_personal} from Personal Dataset")
                    st.rerun()
