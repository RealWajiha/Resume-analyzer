import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="Resume AI Analyzer",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Theme, Header & Box Fixes
st.markdown("""
<style>
    /* Main Dark Warm Espresso Background */
    .stApp {
        background: linear-gradient(135deg, #120e0c 0%, #1c1512 50%, #261d18 100%);
        color: #f3ece7;
    }

    /* Top Header Fix */
    [data-testid="stHeader"] {
        background-color: #120e0c !important;
    }
    [data-testid="stHeader"] * {
        color: #f3ece7 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e1714 !important;
        color: #f3ece7 !important;
        border-right: 1px solid rgba(217, 119, 6, 0.2);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown {
        color: #f3ece7 !important;
    }
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #2a201c !important;
        color: #f3ece7 !important;
        border: 1px solid rgba(217, 119, 6, 0.3) !important;
    }

    /* Column Glassmorphism Cards */
    [data-testid="stColumn"] > div {
        background: rgba(38, 29, 24, 0.5);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(217, 119, 6, 0.25);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
    }

    /* Headings & Subtitles */
    .brown-title {
        background: linear-gradient(90deg, #f59e0b, #d97706, #b45309);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }
    .brown-subtitle {
        color: #c5a898;
        font-size: 1.15rem;
        margin-bottom: 28px;
    }

    /* Job Description Input */
    .stTextArea textarea {
        background-color: #fcf9f6 !important;
        color: #261d18 !important;
        border: 1px solid rgba(217, 119, 6, 0.4) !important;
        border-radius: 10px !important;
    }
    .stTextArea textarea::placeholder {
        color: rgba(38, 29, 24, 0.6) !important;
    }

    /* File Upload Button */
    [data-testid="stFileUploader"] button {
        background-color: #2a201c !important;
        color: #f59e0b !important;
        border: 1px solid rgba(217, 119, 6, 0.4) !important;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #3f312b !important;
        color: #ffffff !important;
        border-color: #f59e0b !important;
    }

    /* Main Action Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #b45309 0%, #d97706 100%);
        color: #ffffff;
        font-weight: 700;
        border: none;
        padding: 14px 28px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(180, 83, 9, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 28px rgba(217, 119, 6, 0.65);
        background: linear-gradient(90deg, #d97706 0%, #f59e0b 100%);
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
    }
    .badge-amber {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-red {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("Resume icon.png", width=75)
    st.title("⚙️ n8n Connection")
    webhook_url = st.text_input(
        "n8n Webhook URL",
        value="http://localhost:5678/webhook/resume-analyze",
        type="password",
        help="Paste your active n8n Webhook POST URL here"
    )
    st.divider()
    st.markdown("### 📌 Instructions")
    st.caption("1. Upload candidate's PDF resume\n2. Add target Job Description\n3. Click 'Analyze Resume' to trigger n8n workflow")

# Main Header
st.markdown('<h1 class="brown-title">Resume AI Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="brown-subtitle">Automated Screening & Candidate Evaluation Pipeline powered by n8n & OpenAI</p>', unsafe_allow_html=True)

# Input Section
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Enter Job Requirements",
        height=220,
        placeholder="e.g. Looking for a Python AI Engineer with hands-on experience in n8n automations, Streamlit dashboards, and LLM integrations...",
        label_visibility="collapsed"
    )

with col2:
    st.subheader("📄 Candidate Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"], label_visibility="collapsed")
    st.write("")
    analyze_button = st.button("⚡ Run n8n Evaluation Workflow")

# Workflow Processing & Results
if analyze_button:
    if not uploaded_file:
        st.error("⚠️ Please upload a candidate PDF resume.")
    elif not webhook_url or "your-n8n-instance" in webhook_url:
        st.error("⚠️ Please configure your valid n8n Webhook URL in the sidebar.")
    else:
        with st.spinner("☕ Processing Resume through n8n AI pipeline..."):
            try:
                files = {
                    "resume": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
                }
                data = {
                    "job_description": job_description if job_description else "General Technical Role"
                }

                response = requests.post(webhook_url, files=files, data=data, timeout=60)

                if response.status_code == 200:
                    result = response.json()

                    # Handle list format if returned by n8n
                    if isinstance(result, list) and len(result) > 0:
                        result = result[0]

                    st.divider()
                    st.markdown("## 📊 Evaluation Report")

                    col_res1, col_res2, col_res3 = st.columns([1, 2, 1], gap="medium")

                    with col_res1:
                        st.markdown("### 👤 Candidate")
                        st.markdown(f"**Name:** {result.get('candidate_name', 'N/A')}")
                        st.markdown(f"**Email:** {result.get('email', 'N/A')}")
                        st.markdown(f"**Phone:** {result.get('phone', 'N/A')}")
                        st.markdown(f"**Experience:** {result.get('total_experience_years', 0)} Years")

                    with col_res2:
                        st.markdown("### 📝 AI Evaluation Summary")
                        st.write(result.get("summary", "No summary generated."))

                    with col_res3:
                        st.markdown("#### Match Score")
                        score = result.get("match_score", 0)
                        st.markdown(f"### {score}%")
                        st.progress(score / 100 if isinstance(score, (int, float)) else 0.0)

                    col_sk1, col_sk2 = st.columns(2, gap="medium")
                    
                    with col_sk1:
                        st.markdown("### 🌟 Matched Skills")
                        top_skills = result.get("top_skills", [])
                        if top_skills and isinstance(top_skills, list):
                            skills_html = "".join([f'<span class="badge badge-amber">{skill}</span>' for skill in top_skills])
                            st.markdown(skills_html, unsafe_allow_html=True)
                        else:
                            st.caption("No specific matching skills extracted.")

                    with col_sk2:
                        st.markdown("### ⚠️ Skill Gaps")
                        missing_skills = result.get("missing_skills", [])
                        if missing_skills and isinstance(missing_skills, list):
                            missing_html = "".join([f'<span class="badge badge-red">{skill}</span>' for skill in missing_skills])
                            st.markdown(missing_html, unsafe_allow_html=True)
                        else:
                            st.success("No major skill gaps found!")

                else:
                    st.error(f"❌ n8n Webhook Error ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")