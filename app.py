"""
CreditWise AI – Intelligent & Transparent Credit Assessment
Main Application Entrypoint & Persistent Left Navigation Router
"""

import streamlit as st

# Streamlit Page Configuration must be the first command
st.set_page_config(
    page_title="CreditWise AI | Transparent Credit Decisioning",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Design System & Core Modules
from utils.styling import apply_fintech_theme
from utils.icons import get_svg_icon
from utils.presets import PRESET_PROFILES
from model.pipeline import initialize_ai_pipeline

# Import Views
from views.home import render_home_page
from views.prediction import render_prediction_page
from views.explanation import render_explanation_page
from views.analytics import render_analytics_page
from views.about import render_about_page

# Inject Institutional Fintech CSS
apply_fintech_theme()

# Page Definitions matching user specification
PAGES = [
    "Overview",
    "Loan Assessment",
    "Explainability",
    "Model Analytics",
    "About Project"
]

# Session State Initialization
if 'current_page' not in st.session_state or st.session_state['current_page'] not in PAGES:
    st.session_state['current_page'] = "Overview"

if 'applicant_data' not in st.session_state or st.session_state['applicant_data'] is None:
    first_preset_key = list(PRESET_PROFILES.keys())[0]
    st.session_state['applicant_data'] = PRESET_PROFILES[first_preset_key].copy()

if 'prediction_result' not in st.session_state:
    st.session_state['prediction_result'] = None

if 'shap_result' not in st.session_state:
    st.session_state['shap_result'] = None

if 'assessment_history' not in st.session_state:
    st.session_state['assessment_history'] = []

# Initialize AI Pipeline (Cached for instant responsiveness)
artifacts = initialize_ai_pipeline()

# Persistent Left Sidebar Navigation
with st.sidebar:
    # Brand Identity Section
    shield_svg = get_svg_icon("shield-check", size=22, color="#FFFFFF")
    st.markdown(f"""
    <div class="sidebar-brand-wrapper">
        <div class="brand-logo-icon">
            {shield_svg}
        </div>
        <div class="brand-text-block">
            <span class="brand-title">CREDITWISE AI</span>
            <span class="brand-subtitle">Risk Underwriting Engine</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean Navigation Router
    def on_nav_select():
        st.session_state['current_page'] = st.session_state['app_sidebar_nav']

    active_index = PAGES.index(st.session_state['current_page'])
    selected_page = st.radio(
        "Navigation Menu",
        options=PAGES,
        index=active_index,
        key='app_sidebar_nav',
        on_change=on_nav_select
    )

    # Active Assessment Telemetry Pill
    if st.session_state.get('prediction_result') is not None:
        p_res = st.session_state['prediction_result']
        is_appr = (p_res['prediction'] == 1)
        st.markdown(f"""
        <div style="background: {'rgba(16, 185, 129, 0.12)' if is_appr else 'rgba(239, 68, 68, 0.12)'}; border: 1px solid {'rgba(16, 185, 129, 0.3)' if is_appr else 'rgba(239, 68, 68, 0.3)'}; border-radius: 8px; padding: 10px 12px; margin-top: 1.25rem;">
            <div style="font-size: 0.7rem; text-transform: uppercase; color: {'#34D399' if is_appr else '#F87171'}; font-weight: 700; letter-spacing: 0.05em;">Active Assessment</div>
            <div style="font-size: 0.88rem; font-weight: 700; color: #FFFFFF; margin: 2px 0;">
                {p_res['status_label']}
            </div>
            <div style="font-size: 0.72rem; color: #94A3B8;">Prob: {p_res['approval_percentage']}% | {p_res['risk_tier']}</div>
        </div>
        """, unsafe_allow_html=True)

    # User Profile / System Footer at bottom of sidebar
    user_svg = get_svg_icon("user", size=16, color="#FFFFFF")
    st.markdown(f"""
    <div class="sidebar-user-card">
        <div class="user-avatar-initials">
            RA
        </div>
        <div class="user-meta">
            <span class="user-name">Senior Risk Analyst</span>
            <span class="user-role">Credit Underwriting Dept</span>
        </div>
    </div>
    <div style="font-size: 0.68rem; color: #64748B; text-align: center; margin-top: 1rem; letter-spacing: 0.04em;">
        CreditWise Platform v1.2 • Production Build
    </div>
    """, unsafe_allow_html=True)

# Main Content Routing
current_view = st.session_state['current_page']

if current_view == "Overview":
    render_home_page(artifacts)
elif current_view == "Loan Assessment":
    render_prediction_page(artifacts)
elif current_view == "Explainability":
    render_explanation_page(artifacts)
elif current_view == "Model Analytics":
    render_analytics_page(artifacts)
elif current_view == "About Project":
    render_about_page()
