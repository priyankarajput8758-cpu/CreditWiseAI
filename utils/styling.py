"""
Institutional Fintech Design System & Styling Components for CreditWise AI.
Crafted for modern fintech aesthetics: Inter typography, deep forest navy sidebar,
crisp borders, minimal cards, and Lucide SVG iconography (zero emojis).
"""

import streamlit as st
from utils.icons import get_svg_icon

def apply_fintech_theme():
    """Injects institutional fintech SaaS CSS into the Streamlit application."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Reset */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: #0F172A;
    }

    /* Background Setup */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* Hide Streamlit Default Chrome */
    #MainMenu, footer, header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Top Main Container Spacing */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1280px !important;
    }

    /* Headings Hierarchy */
    h1 {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 0.4rem !important;
    }

    h2 {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        letter-spacing: -0.02em !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.5rem !important;
    }

    h3 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        letter-spacing: -0.01em !important;
    }

    p, span, label {
        color: #334155;
    }

    /* Persistent Left Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #091E16 !important;
        border-right: 1px solid #142F24 !important;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.08);
    }

    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.6rem !important;
    }

    /* Sidebar Brand Header */
    .sidebar-brand-wrapper {
        padding: 0.8rem 0.4rem 1.4rem 0.4rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-logo-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
    }

    .brand-text-block {
        display: flex;
        flex-direction: column;
    }

    .brand-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #FFFFFF !important;
        letter-spacing: 0.04em;
        line-height: 1.1;
    }

    .brand-subtitle {
        font-size: 0.7rem;
        color: #94A3B8;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 500;
        margin-top: 3px;
    }

    /* Sidebar Navigation Radio Override */
    div[data-testid="stRadio"] > div {
        background-color: transparent !important;
        gap: 4px !important;
    }

    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background-color: transparent !important;
        padding: 0.65rem 0.85rem !important;
        border-radius: 8px !important;
        margin-bottom: 2px !important;
        transition: all 0.15s ease !important;
        border: 1px solid transparent !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        background-color: rgba(255, 255, 255, 0.06) !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"] span {
        color: #CBD5E1 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: rgba(16, 185, 129, 0.14) !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span {
        color: #34D399 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }

    /* Sidebar User / Profile Box */
    .sidebar-user-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 0.75rem 0.85rem;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 1.5rem;
    }

    .user-avatar-initials {
        width: 32px;
        height: 32px;
        background: #10B981;
        color: #FFFFFF;
        font-size: 0.8rem;
        font-weight: 700;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .user-meta {
        display: flex;
        flex-direction: column;
    }

    .user-name {
        font-size: 0.82rem;
        font-weight: 600;
        color: #F8FAFC !important;
        line-height: 1.2;
    }

    .user-role {
        font-size: 0.7rem;
        color: #94A3B8;
        line-height: 1.2;
    }

    /* Top Navigation Bar */
    .top-app-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 0 1.25rem 0;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 1.75rem;
    }

    .top-breadcrumb {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #64748B;
    }

    .top-breadcrumb span.active {
        color: #0F172A;
        font-weight: 600;
    }

    .top-status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        color: #334155;
        font-weight: 500;
    }

    .status-dot-active {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
    }

    /* Minimal Fintech Surface Cards */
    .saas-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.25rem;
    }

    .saas-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #F1F5F9;
    }

    .saas-card-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #0F172A;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Modern KPI Metric Box */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        position: relative;
    }

    .kpi-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        color: #64748B;
        margin-bottom: 0.35rem;
    }

    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.1;
        letter-spacing: -0.02em;
        margin-bottom: 0.35rem;
    }

    .kpi-subtext {
        font-size: 0.75rem;
        color: #64748B;
    }

    /* Badges & Status Pills */
    .badge-approved {
        background: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .badge-rejected {
        background: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FECACA;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .badge-neutral {
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    /* Primary & Secondary Buttons */
    div.stButton > button:first-child {
        background-color: #091E16 !important;
        color: #FFFFFF !important;
        border: 1px solid #091E16 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.25rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.15s ease !important;
    }

    div.stButton > button:first-child:hover {
        background-color: #10B981 !important;
        border-color: #10B981 !important;
        color: #FFFFFF !important;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background-color: #F8FAFC !important;
        border-color: #94A3B8 !important;
    }

    /* Input Field Polish */
    input[type="text"], input[type="number"], div[data-baseweb="select"] > div {
        border-radius: 8px !important;
        border-color: #CBD5E1 !important;
        font-size: 0.88rem !important;
    }

    /* Data Table Clean Styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* Workflow Pipeline Step Item */
    .workflow-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-top: 1rem;
    }

    .workflow-node {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        position: relative;
    }

    .workflow-num {
        font-size: 0.7rem;
        font-weight: 700;
        color: #10B981;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }

    .workflow-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.25rem;
    }

    .workflow-detail {
        font-size: 0.74rem;
        color: #64748B;
        line-height: 1.35;
    }

    /* Subtle Academic Disclaimer Banner */
    .academic-disclaimer {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 3px solid #64748B;
        padding: 0.65rem 0.95rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.78rem;
        color: #475569;
        margin-bottom: 1.25rem;
        line-height: 1.45;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_top_navigation(page_name: str):
    """Renders the top application header with breadcrumbs and system status."""
    st.markdown(f"""
    <div class="top-app-bar">
        <div class="top-breadcrumb">
            <span>CreditWise AI</span>
            <span>/</span>
            <span class="active">{page_name}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="top-status-indicator">
                <span class="status-dot-active"></span>
                <span>Production XGBoost v1.2</span>
            </div>
            <div class="top-status-indicator" style="background: #FFFFFF;">
                <span>Holdout Accuracy: <strong>75.5%</strong></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_academic_disclaimer():
    """Renders the standard minimal educational disclaimer."""
    st.markdown("""
    <div class="academic-disclaimer">
        <strong>Academic Prototype:</strong> Trained on the benchmark UCI Statlog German Credit dataset. 
        Credit risk categories (Good/Bad) are mapped to <em>Likely Approved</em> and <em>Likely Rejected</em> 
        for educational transparency demonstration.
    </div>
    """, unsafe_allow_html=True)

# Backward-compatibility aliases
apply_custom_styles = apply_fintech_theme
render_disclaimer = render_academic_disclaimer

