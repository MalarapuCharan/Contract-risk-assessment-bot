
import streamlit as st
import re
from PyPDF2 import PdfReader

st.set_page_config(page_title="Contract Risk Assessment Bot", layout="centered")

st.title("Contract Risk Assessment Bot")
st.write("Upload a contract file (.txt or .pdf) to analyze legal risk.")

uploaded_file = st.file_uploader("Upload contract file", type=["txt", "pdf"])

text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        text = text.lower()
    else:
        text = uploaded_file.read().decode("utf-8").lower()

if text:
    risk_score = 0
    max_score = 25
    detected = []

    def match(patterns):
        return any(re.search(p, text) for p in patterns)

    rules = [
        ("Unilateral Termination", [r"terminate.*without notice", r"sole discretion"], 4),
        ("Penalty / Liquidated Damages", [r"liquidated damages", r"penalty", r"without dispute"], 4),
        ("Jurisdiction / Arbitration", [r"exclusive jurisdiction", r"foreign court", r"arbitration"], 3),
        ("Non-Compete Clause", [r"non[- ]?compete", r"worldwide", r"five \(5\) years"], 4),
        ("Unlimited Liability", [r"unlimited liability", r"without limitation", r"regardless of fault"], 5),
        ("Waiver of Legal Rights", [r"waives all rights", r"no right to contest"], 5)
    ]

    for name, patterns, weight in rules:
        if match(patterns):
            detected.append(name)
            risk_score += weight

    risk_percentage = int((risk_score / max_score) * 100)

    st.subheader("Detected Risk Clauses")
    if detected:
        for d in detected:
            st.write("-", d)
    else:
        st.write("No major risk clauses detected.")

    st.subheader("Risk Percentage")
    st.write(f"{risk_percentage}%")

    if risk_percentage < 30:
        st.success("Low Risk")
    elif risk_percentage < 65:
        st.warning("Medium Risk")
    else:
        st.error("High Risk")

    st.subheader("Explanation")
    st.write(
        "This system analyzes contract text using rule-based pattern matching. "
        "Each risky clause contributes a weighted score based on its legal impact, "
        "which is converted into an overall risk percentage."
    )

st.caption("Hackathon Project | Simple Rule-Based Analysis")
