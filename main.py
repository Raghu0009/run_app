import streamlit as st
from db_cont import list_tables
from df_data import fetch_table_data

st.markdown(
    """
    <style>
    .css-1v0mbdj { font-size: 20px !important; font-weight: bold !important; color: #2e3d49 !important; text-align: center !important; margin-top: 100px !important; margin-bottom: 50px !important; }
    .stButton > button { background-color: transparent !important; border: none !important; color: #000 !important; text-align: left; }
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.header("UNITS")
sidebar_options = {
    'HSM1': 'db1_phsm1',
    'HSM2': 'db1_phsm2',
    'SMS1': 'db1_psms1',
    'SMS2': 'db1_psms2'
}

st.title("IPQMS - DATA VERIFICATION")

if "sidebar_activated" not in st.session_state:
    st.session_state.update({
        "sidebar_activated": None,
        "selected_subunit": None,
        "available_tables": [],
        "subunits": ['APFC', 'ODG', 'IBA', 'IMS'],
        "schema_name": None,
        "sidebar_label": None,
        "selected_table": None
    })

def handle_sidebar_click():
    for label, schema in sidebar_options.items():
        if st.sidebar.button(label):
            st.session_state.update({
                "sidebar_activated": label,
                "schema_name": schema,
                "sidebar_label": label
            })
            break

handle_sidebar_click()

if st.session_state.sidebar_activated:
    col1, col2 = st.columns(2)

    with col1:
        st.session_state.selected_subunit = st.selectbox(
            "Select Subunit:",
            [""] + st.session_state.subunits,
            key="subunit_selectbox"
        )

    with col2:
        if st.session_state.selected_subunit:
            subunit = st.session_state.selected_subunit.upper()
            schema_prefix = st.session_state.sidebar_label
            table_name_filter = f"{schema_prefix}_{subunit}%"

            tables = list_tables(st.session_state.schema_name, table_name_filter)
            st.session_state.available_tables = tables

            if tables:
                st.session_state.selected_table = st.selectbox(
                    "Select a table:",
                    [""] + tables,
                    key="table_selectbox"
                )
                if st.session_state.selected_table:
                    st.write(f"You selected: {st.session_state.selected_table}.")
            else:
                st.write("No tables available for this subunit.")

if st.session_state.selected_table:
    if st.button("Retrieve"):
        schema_name = st.session_state.schema_name
        table_name = st.session_state.selected_table
        #here we'll fetch df and also query from db_cont for debugging
        df, query = fetch_table_data(schema_name, table_name)

        if query:
            with st.expander("View SQL Query - 1"):
                st.code(query, language="sql")

        if not df.empty:
            #df = df.reset_index(drop=True)  # Remove the index column
            st.write(f"Data from table: {table_name}")
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No data found or error fetching data.")
