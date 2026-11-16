"""
CreditWise AI — Premium FinTech Credit Assessment Platform
Main application entry point & navigation router.
"""

import streamlit as st

st.set_page_config(
    page_title="CreditWise AI | Credit Risk Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.styling import apply_fintech_theme, navigate_to
from utils.icons import get_svg_icon
from utils.presets import PRESET_PROFILES
from model.pipeline import initialize_ai_pipeline

from views.home import render_home_page
from views.prediction import render_prediction_page
from views.history import render_history_page
from views.explanation import render_explanation_page
from views.analytics import render_analytics_page
from views.about import render_about_page

# ── Inject Design System ──
apply_fintech_theme()

# ── Page Definitions ──
PAGES = [
    "Overview",
    "New Assessment",
    "Assessment History",
    "Explainability",
    "Analytics",
    "About",
]

# ── Session State Init ──
defaults = {
    'current_page': 'Overview',
    'applicant_data': None,
    'prediction_result': None,
    'shap_result': None,
    'assessment_history': [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state['current_page'] not in PAGES:
    st.session_state['current_page'] = 'Overview'

# Clear any legacy widget keys
if '_sidebar_nav' in st.session_state:
    del st.session_state['_sidebar_nav']

if st.session_state['applicant_data'] is None:
    first_key = list(PRESET_PROFILES.keys())[0]
    st.session_state['applicant_data'] = PRESET_PROFILES[first_key].copy()

# ── Load ML Pipeline (cached) ──
artifacts = initialize_ai_pipeline()

# ── Sidebar ──
with st.sidebar:
    # Brand (CreditWise AI guaranteed on a single line)
    st.markdown("""
    <div class="cw-brand">
        <div class="cw-brand-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                 fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <polyline points="9 12 11 14 15 10"/>
            </svg>
        </div>
        <div style="white-space:nowrap;overflow:visible;">
            <div class="cw-brand-name">CreditWise AI</div>
            <div class="cw-brand-sub">Risk Assessment Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nav section label
    st.markdown('<div class="cw-nav-section">Navigation</div>', unsafe_allow_html=True)

    # Navigation
    active_idx = PAGES.index(st.session_state['current_page'])
    selected_page = st.radio(
        "nav",
        options=PAGES,
        index=active_idx,
        label_visibility="collapsed"
    )
    if selected_page != st.session_state['current_page']:
        st.session_state['current_page'] = selected_page
        st.rerun()

    # Active assessment status pill
    pr = st.session_state.get('prediction_result')
    if pr is not None:
        is_appr = pr['prediction'] == 1
        accent = "rgba(16,185,129,0.12)" if is_appr else "rgba(239,68,68,0.12)"
        border = "rgba(16,185,129,0.3)" if is_appr else "rgba(239,68,68,0.3)"
        label_color = "#34D399" if is_appr else "#F87171"
        st.markdown(f"""
        <div class="cw-status-pill" style="background:{accent};border-color:{border};">
            <div class="cw-status-label" style="color:{label_color};">Last Assessment</div>
            <div class="cw-status-value">{pr['status_label']}</div>
            <div class="cw-status-sub">{pr['approval_percentage']}% · {pr['risk_tier']}</div>
        </div>
        """, unsafe_allow_html=True)

    # History count pill
    history_count = len(st.session_state.get('assessment_history', []))
    if history_count > 0:
        st.markdown(f"""
        <div style="margin: 0.75rem 0.5rem 0 0.5rem; padding: 7px 12px;
                    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 6px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.72rem; color:#64748B;">Session Assessments</span>
            <span style="font-size:0.78rem; font-weight:700; color:#94A3B8;">{history_count}</span>
        </div>
        """, unsafe_allow_html=True)

    # User card
    st.markdown("""
    <div class="cw-user-card">
        <div class="cw-avatar">RA</div>
        <div>
            <div class="cw-user-name">Risk Analyst</div>
            <div class="cw-user-role">Credit Underwriting</div>
        </div>
    </div>
    <div class="cw-version">CreditWise v2.0 · Production</div>
    """, unsafe_allow_html=True)

# ── Page Router ──
page = st.session_state['current_page']

if page == "Overview":
    render_home_page(artifacts)
elif page == "New Assessment":
    render_prediction_page(artifacts)
elif page == "Assessment History":
    render_history_page(artifacts)
elif page == "Explainability":
    render_explanation_page(artifacts)
elif page == "Analytics":
    render_analytics_page(artifacts)
elif page == "About":
    render_about_page()
