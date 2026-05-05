"""Streamlit UI for Meeting Insights AI.

Run:
  streamlit run streamlit_app.py

This app intentionally imports the LLM-powered agents lazily (on button click)
so the UI can load even if environment variables/config are not set yet.
"""

from __future__ import annotations

import traceback

import streamlit as st

from main import generate_insights
from src.util.output_formatter import format_insights_as_markdown


def _clear_notes() -> None:
    # Clear the widget state (must match the text_area key)
    st.session_state["notes"] = ""


st.set_page_config(page_title="Meeting Insights AI", layout="centered")

st.title("Meeting Insights AI")
st.caption("Enter your meeting notes. Click Generate to generate insights.")


notes = st.text_area(
    "Meeting notes",
    key="notes",
    value="",
    height=120,
    placeholder="Type or paste meeting notes here...",
)

notes = notes or ""

col1, col2 = st.columns([1, 1])
with col1:
    generate_clicked = st.button("Generate", type="primary", use_container_width=True)
with col2:
    st.button("Clear", use_container_width=True, on_click=_clear_notes)

if generate_clicked:
    if not notes.strip():
        st.warning("Please enter at least one line of meeting notes.")
    else:
        try:
            with st.spinner("Generating insights..."):
                final_output = generate_insights(notes)

            st.subheader("Result")
            st.markdown(format_insights_as_markdown(final_output))


        except Exception as e:
            st.error("Failed to generate insights.")
            st.write(f"**Error:** {e}")
            with st.expander("Details (traceback)"):
                st.code(traceback.format_exc(), language="text")

