import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("ResultsGrid_ExportData - 2025-08-25T150651.766.csv")
    return df

df = load_data()

st.set_page_config(page_title="BOMA SF Member Directory", layout="wide")
st.title("🔍 BOMA SF Searchable Directory")

# Sidebar filters
st.sidebar.header("Filters")

# Search bar
search = st.sidebar.text_input("Search by Company, Name, Email, or City")

# Category filter
categories = []
for i in range(1, 9):
    col = f"Category {i}"
    if col in df.columns:
        categories.extend(df[col].dropna().unique().tolist())

categories = sorted(set(categories))
selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + categories)

# Apply search filter
filtered_df = df.copy()
if search:
    search_lower = search.lower()
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: any(
                search_lower in str(value).lower()
                for value in [
                    row.get("Company", ""),
                    row.get("First Name", ""),
                    row.get("Last Name", ""),
                    row.get("Email", ""),
                    row.get("City", "")
                ]
            ),
            axis=1
        )
    ]

# Apply category filter
if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df[[f"Category {i}" for i in range(1, 9) if f"Category {i}" in df.columns]]
        .apply(lambda row: selected_category in row.values, axis=1)
    ]

st.subheader(f"Results: {len(filtered_df)} entries")

# Format clickable links
if "Website" in filtered_df.columns:
    filtered_df["Website"] = filtered_df["Website"].apply(lambda x: f"[Link]({x})" if pd.notna(x) else "")
if "Email" in filtered_df.columns:
    filtered_df["Email"] = filtered_df["Email"].apply(lambda x: f"[{x}](mailto:{x})" if pd.notna(x) else "")

# Display table
st.dataframe(
    filtered_df[
        ["Company", "First Name", "Last Name", "Email", "Work Phone", "City", "State Province", "Website", "Category 1"]
    ],
    use_container_width=True
)

# Download button
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download results as CSV",
    data=csv,
    file_name="filtered_results.csv",
    mime="text/csv"
)
