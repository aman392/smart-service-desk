import json
import os
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from core import PROMPTS, SAMPLES, process

st.set_page_config(page_title="Smart Service Desk", page_icon="🛠️", layout="wide")
st.markdown("""<style>
.block-container {max-width: 1100px; padding-top: 2rem;}
h1,h2,h3 {letter-spacing:-0.025em;}
div[data-testid="stMetric"] {border:1px solid #d9dee5; border-radius:10px; padding:12px 16px;}
</style>""", unsafe_allow_html=True)


st.title("Smart Service Desk")
st.write("Organize incoming service requests, extract key details, and flag requests that need attention.")

try:
    secret_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    secret_key = ""
key = os.getenv("GEMINI_API_KEY", "") or secret_key

with st.sidebar:
    st.header("Processing")
    mode = st.radio("Mode", ["Demo", "Gemini API"], help="Demo is deterministic and does not call a language model.")
    model = st.text_input("Gemini model", value="gemini-3.5-flash-lite", disabled=mode == "Demo")
    version = st.selectbox("Instruction version", list(PROMPTS), index=1, disabled=mode == "Demo")
    if mode == "Gemini API" and not key:
        st.warning("No GEMINI_API_KEY found. Configure it locally in .streamlit/secrets.toml.")
    st.divider()
    st.caption("Local demo • Session-only history")

if "history" not in st.session_state:
    st.session_state.history = []

left, right = st.columns([1.05, 0.95], gap="large")
with left:
    st.subheader("Incoming request")
    choice = st.selectbox("Example", ["Custom"] + [f"Example {i+1}" for i in range(len(SAMPLES))])
    initial = SAMPLES[int(choice.split()[-1]) - 1] if choice != "Custom" else ""
    message = st.text_area("Customer message", value=initial, height=175, placeholder="Paste a fictional service request...")
    execute = st.button("Analyze request", type="primary", use_container_width=True)

with right:
    st.subheader("Decision")
    if execute:
        if mode == "Gemini API" and not key:
            st.error("Add a Gemini API key first, or switch to Demo mode.")
        else:
            try:
                with st.spinner("Checking the request..."):
                    result = process(message, mode=mode, key=key, model=model, version=version)
                st.session_state.history.insert(0, {"time": datetime.now(timezone.utc).strftime("%H:%M UTC"), **result})
            except Exception as ex:
                st.error(f"Processing failed: {type(ex).__name__}: {ex}")
    if st.session_state.history:
        current = st.session_state.history[0]
        if current["status"] == "Needs review":
            st.warning("HOLD · Needs human review")
        else:
            st.success("READY · Manual dispatch review")
        c1, c2 = st.columns(2)
        c1.metric("Category", current["extraction"]["category"].title())
        c2.metric("Priority", current["extraction"]["priority"].title())
        st.caption(f"ID {current['request_id']} · {current['mode']}")
        if current["issues"]:
            for issue in current["issues"]:
                st.write(f"• {issue}")
        else:
            st.write("No missing required details detected by the current validation rules.")
        with st.expander("Structured result", expanded=True):
            st.json(current)
        st.download_button("Download JSON", data=json.dumps(current, indent=2), file_name="work_order.json", mime="application/json")
    else:
        st.caption("Analysis results will appear here.")

st.divider()
st.subheader("Recent requests")
if st.session_state.history:
    rows = [{"Time": r["time"], "ID": r["request_id"], "Category": r["extraction"]["category"], "Status": r["status"], "Issues": len(r["issues"])} for r in st.session_state.history]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    st.download_button("Export session CSV", data=pd.DataFrame(rows).to_csv(index=False), file_name="serviceops_session.csv", mime="text/csv")
else:
    st.caption("Your processed examples appear here. Session data is not stored permanently.")

with st.expander("Prompt versions"):
    st.write("The two instruction sets are available for later controlled evaluation. Switching prompts alone does not prove improvement.")
    for name, prompt in PROMPTS.items():
        st.markdown(f"**{name}**")
        st.code(prompt, language="text")

st.caption("Service requests are reviewed before dispatch.")
