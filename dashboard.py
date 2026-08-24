import json
from pathlib import Path

import streamlit as st


SUMMARIES_FILE = Path("data/summaries.json")

st.set_page_config(
    page_title="Market Pulse",
    page_icon="📈",
    layout="wide"
)

st.title("Market Pulse")
st.write("SEC filing event monitor and summarisation pipeline")

if not SUMMARIES_FILE.exists():
    st.error(
        "data/summaries.json was not found. "
        "Run the pipeline scripts first."
    )
    st.stop()

with SUMMARIES_FILE.open("r", encoding="utf-8") as json_file:
    summaries = json.load(json_file)

companies = sorted({
    item["company"]
    for item in summaries
})

forms = sorted({
    item["form"]
    for item in summaries
})

selected_company = st.sidebar.selectbox(
    "Company",
    ["All"] + companies
)

selected_form = st.sidebar.selectbox(
    "Filing form",
    ["All"] + forms
)

filtered_summaries = []

for item in summaries:
    company_matches = (
        selected_company == "All"
        or item["company"] == selected_company
    )

    form_matches = (
        selected_form == "All"
        or item["form"] == selected_form
    )

    if company_matches and form_matches:
        filtered_summaries.append(item)

column1, column2, column3 = st.columns(3)

column1.metric(
    "Companies monitored",
    len(companies)
)

column2.metric(
    "Total summaries",
    len(summaries)
)

column3.metric(
    "Visible records",
    len(filtered_summaries)
)

st.divider()

for item in filtered_summaries:
    with st.container(border=True):
        st.subheader(
            f"{item['company']} ({item['ticker']}) - "
            f"{item['form']}"
        )

        st.caption(
            f"Filed: {item['filing_date']} | "
            f"Event type: {item['event_type']}"
        )

        st.write(item["summary"])

        st.caption(
            f"Method: {item['summary_method']} | "
            f"Source words: {item['source_word_count']:,}"
        )

        st.markdown(
            f"[Open the official SEC filing]"
            f"({item['filing_url']})"
        )