import streamlit as st
from faker import Faker
import json
import pandas as pd

st.set_page_config(page_title="Mock Data Generator", layout="wide")
st.title("Mock Data Generator")

fake = Faker()

with st.sidebar:
    st.header("Settings")
    num_records = st.number_input("Number of Records", min_value=1, max_value=1000, value=10)
    schema_input = st.text_area(
        "Schema (JSON)",
        value=json.dumps({"name": "name", "address": "address", "email": "email"}, indent=2),
        height=200
    )
    generate = st.button("Generate Mock Data")

if generate:
    try:
        schema = json.loads(schema_input)
        data = []
        for _ in range(num_records):
            row = {}
            for field, method in schema.items():
                if hasattr(fake, method):
                    row[field] = getattr(fake, method)()
                else:
                    row[field] = f"<invalid faker method: {method}>"
            data.append(row)
        df = pd.DataFrame(data)
        st.subheader("Generated Data")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="mock_data.csv",
            mime="text/csv"
        )
    except json.JSONDecodeError as e:
        st.error(f"Error parsing schema JSON: {e}")
