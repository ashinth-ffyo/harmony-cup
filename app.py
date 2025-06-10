import streamlit as st
import pandas as pd
from database import DatabaseManager
from excel_export import export_to_excel
from model import TeamModel
import os

# Initialize Streamlit app
st.set_page_config(page_title="Harmony Cup Manager", layout="wide")
st.title("Harmony Cup Manager")

# Initialize database and model
db_manager = DatabaseManager()
model = TeamModel()

# Sidebar for category selection and theme
with st.sidebar:
    st.header("Navigation")
    category = st.selectbox("Select Category", model.categories, key="category_select")
    theme = st.selectbox("Theme", ["Light", "Dark"], key="theme_select")
    if theme == "Dark":
        st.markdown(
            """
            <style>
            .stApp { background-color: #1e1e1e; color: white; }
            .stDataFrame { background-color: #2e2e2e; }
            </style>
            """,
            unsafe_allow_html=True
        )

# Fetch teams for the selected category
@st.cache_data
def load_teams(category):
    return pd.DataFrame(db_manager.get_teams(category))

df = load_teams(category)

# Display teams in a dataframe
st.subheader(f"Teams in {category}")
if not df.empty:
    # Sorting
    sort_col = st.selectbox("Sort By", model.columns, key=f"sort_{category}")
    df = df.sort_values(by=sort_col)
    st.dataframe(df, use_container_width=True, height=400)
else:
    st.info("No teams in this category.")

# Form for adding/editing teams
st.subheader("Add/Edit Team")
with st.form("team_form"):
    team_data = {}
    cols = st.columns(3)
    for i, field in enumerate(model.team_fields):
        with cols[i % 3]:
            if field.startswith("Name"):
                team_data[field] = st.text_input(field, key=f"{field}_{category}")
            elif field.startswith("Class"):
                team_data[field] = st.text_input(field, key=f"{field}_{category}")
            elif field == "Type":
                team_data[field] = st.text_input("Type (optional)", key=f"Type_{category}")
    for i, field in enumerate(model.round_fields):
        with cols[i % 3]:
            team_data[field] = st.selectbox(field, model.status_options, key=f"{field}_{category}")

    ref_no = st.number_input("REF_NO (leave 0 for auto-assign)", min_value=0, value=0, key=f"ref_no_{category}")
    submit = st.form_submit_button("Submit Team")

    if submit:
        # Validate inputs
        for field in model.team_fields:
            if field != "Type" and not team_data.get(field):
                st.error(f"{field} cannot be empty")
                break
        else:
            try:
                if ref_no == 0:  # Add new team
                    db_manager.add_team(category, team_data)
                    st.success("Team added successfully")
                else:  # Update existing team
                    db_manager.update_team(category, ref_no, team_data)
                    st.success("Team updated successfully")
                st.cache_data.clear()  # Clear cache to refresh dataframe
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Delete team
st.subheader("Delete Team")
delete_ref_no = st.number_input("Enter REF_NO to Delete", min_value=1, value=1, key=f"delete_ref_no_{category}")
if st.button("Delete Team", key=f"delete_{category}"):
    try:
        db_manager.delete_team(category, delete_ref_no)
        st.success("Team deleted successfully")
        st.cache_data.clear()
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Export to Excel
if st.button("Export to Excel", key="export"):
    try:
        export_to_excel(db_manager, model)
        with open("Harmony Cup.xlsx", "rb") as file:
            st.download_button(
                label="Download Harmony Cup.xlsx",
                data=file,
                file_name="Harmony Cup.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Error: {str(e)}")