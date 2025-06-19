import streamlit as st
import pandas as pd

DATA_FILE = "samples.csv"

try:
    df = pd.read_csv(DATA_FILE)
except:
    df = pd.DataFrame(columns=["Sample ID", "Mouse ID", "Tissue Type", "Status"])
    df.to_csv(DATA_FILE, index=False)

st.title("🧪 Lab Sample Tracker")

# Form to add a new sample
st.header("Add New Sample")
with st.form("sample_form"):
    sample_id = st.text_input("Sample ID")
    mouse_id = st.text_input("Mouse ID")
    tissue = st.selectbox("Tissue Type", ["Brain", "Spinal Cord", "Muscle", "Other"])
    status = st.selectbox("Status", ["Collected", "Stored", "Analyzed"])
    submitted = st.form_submit_button("Add Sample")

    if submitted:
        if sample_id and mouse_id:
            new_row = pd.DataFrame([[sample_id, mouse_id, tissue, status]],
                                   columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Sample added successfully!")
        else:
            st.error("❌ Please enter both Sample ID and Mouse ID.")

# Display the current sample table
st.header("📋 All Samples")
st.dataframe(df)

# Filter samples
st.header("🔍 Filter Samples")
if not df.empty:
    selected_status = st.selectbox("Filter by status", ["All"] + df["Status"].unique().tolist())
    if selected_status != "All":
        filtered_df = df[df["Status"] == selected_status]
        st.dataframe(filtered_df)
else:
    st.info("No samples to display yet.")
