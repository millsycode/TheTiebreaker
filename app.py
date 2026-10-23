import os
import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="The Tiebreaker | AI Decision Engine",
    page_icon="⚖️",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.3rem; font-weight: 700; color: #1E293B; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #64748B; margin-bottom: 2rem; }
    .card { background-color: #F8FAFC; padding: 1.2rem; border-radius: 8px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚖️ The Tiebreaker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Stop agonizing over tough choices. Get instant clarity, objective trade-offs, and a decisive recommendation.</div>', unsafe_allow_html=True)

# Sidebar for Setup
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Get a free key from Google AI Studio (aistudio.google.com)")
    st.divider()
    st.markdown("### 💡 How to use")
    st.markdown("1. Describe the choice you're facing.\n2. Mention the two or three options.\n3. Add any constraints (budget, timeline, values).\n4. Click **Break the Tie**!")

# Main Input Section
with st.container():
    decision_prompt = st.text_area(
        "What decision are you trying to make?",
        placeholder="Example: I work at a B2B SaaS company and need to choose whether to focus on 21 CFR Part 11 compliance or build an AI booking assistant next quarter...",
        height=140
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        submitted = st.button("🚀 Break the Tie", type="primary", use_container_width=True)

SYSTEM_PROMPT = """
You are 'The Tiebreaker', an elite, hyper-rational executive decision advisor.
Your job is to objectively analyze tough choices and guide the user to a definitive path forward.

When given a dilemma, return your output strictly in these 4 markdown tabs:

## TAB 1: ⚖️ Pros & Cons
Provide a clear, categorized pros and cons breakdown for each option. Differentiate between practical/business impact and emotional/team impact.

## TAB 2: 📊 Comparison Matrix
Provide a Markdown table comparing the options across:
- Effort / Execution Friction
- Long-Term Upside
- Moat / Defensibility
- Regret Risk (Score each 1-10)

## TAB 3: 🧭 SWOT Analysis
Provide a structured 2x2 SWOT (Strengths, Weaknesses, Opportunities, Threats) for the primary candidates.

## TAB 4: 🎯 The Tiebreaker Verdict
Pick a winner. Do NOT sit on the fence. 
1. Use the '10/10/10' rule (Impact in 10 days, 10 months, 10 years).
2. Clarify if this is a 'One-Way Door' (irreversible) or 'Two-Way Door' (reversible) decision.
3. Deliver the final, decisive recommendation and the immediate next step.
"""

def generate_decision(prompt, key):
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2
        )
    )
    return response.text

if submitted:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API key in the sidebar to run the analysis.")
    elif not decision_prompt.strip():
        st.warning("⚠️ Please describe the decision you need help with.")
    else:
        with st.spinner("Analyzing trade-offs, calculating regret risk, and formulating verdict..."):
            try:
                result = generate_decision(decision_prompt, api_key)
                
                # Split and present in tabs if possible, or display directly
                st.success("Decision breakdown generated!")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"Error processing your request: {e}")
