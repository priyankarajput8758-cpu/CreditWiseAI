"""
CreditWise AI — Premium FinTech Design System
Deep navy, emerald green, white & soft grey palette.
Clean typography, consistent spacing, subtle shadows, elegant cards.
"""

import streamlit as st
from utils.icons import get_svg_icon


def apply_fintech_theme():
    """Injects premium fintech CSS into the Streamlit application."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ─── Global Reset & Typography ─── */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* ─── App Background ─── */
    .stApp {
        background-color: #F0F4F8 !important;
    }

    /* ─── Hide Streamlit Chrome ─── */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }
    div[data-testid="stDecoration"] { display: none !important; }

    /* ─── Main Content Spacing ─── */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1300px !important;
    }

    /* ─── Headings ─── */
    h1 {
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 0.25rem !important;
        line-height: 1.2 !important;
    }
    h2 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        letter-spacing: -0.015em !important;
    }
    h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #0F172A !important;
    }
    p, span, label { color: #334155; }

    /* ─── SIDEBAR ─── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1628 0%, #0D1F3C 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.2) !important;
        width: 270px !important;
        min-width: 270px !important;
        padding-top: 0 !important;
    }

    /* Collapse Streamlit default top spacing in sidebar */
    section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    section[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding-top: 0.75rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.4rem !important;
    }

    /* ─── Sidebar Brand ─── */
    .cw-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.5rem 0.5rem 1rem 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 0.75rem;
        white-space: nowrap !important;
    }
    .cw-brand-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #10B981, #059669);
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(16,185,129,0.4);
        flex-shrink: 0;
    }
    .cw-brand-name {
        font-size: 1.15rem;
        font-weight: 800;
        color: #FFFFFF !important;
        letter-spacing: 0.02em;
        line-height: 1.1;
        white-space: nowrap !important;
        display: inline-block !important;
    }
    .cw-brand-sub {
        font-size: 0.68rem;
        color: #94A3B8 !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: 2px;
        white-space: nowrap !important;
    }

    /* ─── Sidebar Nav Section Label ─── */
    .cw-nav-section {
        font-size: 0.7rem;
        font-weight: 700;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 0.25rem 0.5rem 0.4rem 0.5rem;
        margin-bottom: 0.25rem;
        display: block;
    }

    /* ─── Sidebar Radio Nav ─── */
    div[data-testid="stRadio"] > div {
        background-color: transparent !important;
        gap: 4px !important;
        padding: 0 !important;
    }
    div[data-testid="stRadio"] > label {
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background-color: transparent !important;
        padding: 0.65rem 0.85rem !important;
        border-radius: 8px !important;
        margin-bottom: 2px !important;
        transition: all 0.15s ease !important;
        border: 1px solid transparent !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"] p,
    div[data-testid="stRadio"] label[data-baseweb="radio"] span,
    div[data-testid="stRadio"] label[data-baseweb="radio"] div {
        color: #E2E8F0 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover p,
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover span {
        color: #FFFFFF !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: rgba(16, 185, 129, 0.16) !important;
        border-color: rgba(16, 185, 129, 0.35) !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p,
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span,
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) div {
        color: #34D399 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stRadio"] input[type="radio"] { display: none !important; }

    /* ─── Sidebar Status Badge ─── */
    .cw-status-pill {
        background: rgba(16,185,129,0.1);
        border: 1px solid rgba(16,185,129,0.25);
        border-radius: 6px;
        padding: 8px 12px;
        margin: 1rem 0.75rem 0 0.75rem;
    }
    .cw-status-label {
        font-size: 0.62rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #34D399;
        margin-bottom: 2px;
    }
    .cw-status-value {
        font-size: 0.82rem;
        font-weight: 600;
        color: #FFFFFF;
    }
    .cw-status-sub {
        font-size: 0.68rem;
        color: #64748B;
        margin-top: 1px;
    }

    /* ─── Sidebar User Card ─── */
    .cw-user-card {
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 0.75rem 1rem;
        margin: 1.5rem 0.75rem 0.5rem 0.75rem;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
    }
    .cw-avatar {
        width: 30px;
        height: 30px;
        background: linear-gradient(135deg, #10B981, #0D9488);
        color: #fff;
        font-size: 0.72rem;
        font-weight: 700;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .cw-user-name {
        font-size: 0.78rem;
        font-weight: 600;
        color: #E2E8F0;
        line-height: 1.1;
    }
    .cw-user-role {
        font-size: 0.65rem;
        color: #64748B;
        line-height: 1.1;
    }
    .cw-version {
        font-size: 0.6rem;
        color: #334155;
        text-align: center;
        padding-bottom: 1rem;
        letter-spacing: 0.04em;
    }

    /* ─── Page Header Bar ─── */
    .cw-page-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 0 1.25rem 0;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 1.75rem;
        background: transparent;
    }
    .cw-breadcrumb {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 500;
    }
    .cw-breadcrumb .sep { color: #CBD5E1; }
    .cw-breadcrumb .active {
        color: #0F172A;
        font-weight: 600;
    }
    .cw-header-right {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .cw-system-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        color: #475569;
        font-weight: 500;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .cw-dot-green {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 0 2px rgba(16,185,129,0.2);
        display: inline-block;
    }

    /* ─── KPI Cards ─── */
    .cw-kpi {
        background: #FFFFFF;
        border: 1px solid #E8EDF3;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 1px 4px rgba(15,23,42,0.04), 0 4px 16px rgba(15,23,42,0.03);
        position: relative;
        overflow: hidden;
        transition: box-shadow 0.2s ease;
        margin-bottom: 0;
    }
    .cw-kpi::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--kpi-accent, #10B981);
        border-radius: 12px 12px 0 0;
    }
    .cw-kpi-label {
        font-size: 0.69rem;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-weight: 700;
        color: #64748B;
        margin-bottom: 0.5rem;
    }
    .cw-kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1;
        letter-spacing: -0.03em;
        margin-bottom: 0.4rem;
    }
    .cw-kpi-delta {
        font-size: 0.75rem;
        font-weight: 500;
        color: #64748B;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .cw-kpi-delta.up { color: #10B981; }
    .cw-kpi-delta.down { color: #EF4444; }

    /* ─── Main Cards ─── */
    .cw-card {
        background: #FFFFFF;
        border: 1px solid #E8EDF3;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 4px rgba(15,23,42,0.04), 0 4px 16px rgba(15,23,42,0.03);
        margin-bottom: 1.25rem;
    }
    .cw-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.1rem;
        padding-bottom: 0.85rem;
        border-bottom: 1px solid #F1F5F9;
    }
    .cw-card-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #0F172A;
        margin: 0;
        letter-spacing: -0.01em;
    }

    /* ─── Status Badges ─── */
    .cw-badge {
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        letter-spacing: 0.01em;
    }
    .cw-badge-approved {
        background: #ECFDF5; color: #065F46;
        border: 1px solid #A7F3D0;
    }
    .cw-badge-rejected {
        background: #FEF2F2; color: #991B1B;
        border: 1px solid #FECACA;
    }
    .cw-badge-neutral {
        background: #F1F5F9; color: #475569;
        border: 1px solid #E2E8F0;
    }
    .cw-badge-warning {
        background: #FFFBEB; color: #92400E;
        border: 1px solid #FDE68A;
    }
    .cw-badge-info {
        background: #EFF6FF; color: #1D4ED8;
        border: 1px solid #BFDBFE;
    }

    /* ─── Decision Banner ─── */
    .cw-decision-approved {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 1px solid #6EE7B7;
        border-left: 4px solid #10B981;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
    }
    .cw-decision-rejected {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border: 1px solid #FCA5A5;
        border-left: 4px solid #EF4444;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
    }

    /* ─── Form Section Headers ─── */
    .cw-form-section {
        font-size: 0.8rem;
        font-weight: 700;
        color: #0F172A;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 0.5rem 0 0.5rem 0;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 1rem;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .cw-form-section-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px; height: 20px;
        background: #0A1628;
        color: #10B981;
        border-radius: 50%;
        font-size: 0.65rem;
        font-weight: 800;
        flex-shrink: 0;
    }

    /* ─── SHAP Factor Row ─── */
    .cw-factor-positive {
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-left: 3px solid #10B981;
        border-radius: 7px;
        padding: 9px 12px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .cw-factor-negative {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        border-left: 3px solid #EF4444;
        border-radius: 7px;
        padding: 9px 12px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* ─── History Table ─── */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E8EDF3 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 1px 4px rgba(15,23,42,0.04) !important;
    }

    /* ─── Buttons ─── */
    div.stButton > button:first-child {
        background: #0A1628 !important;
        color: #FFFFFF !important;
        border: 1px solid #0A1628 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        padding: 0.55rem 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: all 0.15s ease !important;
        letter-spacing: 0.01em !important;
    }
    div.stButton > button:first-child:hover {
        background: #10B981 !important;
        border-color: #10B981 !important;
        box-shadow: 0 4px 12px rgba(16,185,129,0.3) !important;
    }
    div.stButton > button[kind="primary"]:first-child {
        background: #10B981 !important;
        border-color: #10B981 !important;
    }
    div.stButton > button[kind="primary"]:first-child:hover {
        background: #059669 !important;
        border-color: #059669 !important;
    }
    div.stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #F8FAFC !important;
        border-color: #94A3B8 !important;
    }

    /* ─── Form Submit Button ─── */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 0.7rem 1.5rem !important;
        box-shadow: 0 4px 14px rgba(16,185,129,0.35) !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        box-shadow: 0 6px 20px rgba(16,185,129,0.45) !important;
        transform: translateY(-1px) !important;
    }

    /* ─── Input Polish ─── */
    input[type="text"], input[type="number"], div[data-baseweb="select"] > div:first-child {
        border-radius: 8px !important;
        border-color: #CBD5E1 !important;
        font-size: 0.875rem !important;
    }
    div[data-baseweb="select"] > div:first-child:focus-within {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16,185,129,0.15) !important;
    }

    /* ─── Info/Warning Disclaimer ─── */
    .cw-disclaimer {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 3px solid #94A3B8;
        padding: 0.6rem 1rem;
        border-radius: 0 7px 7px 0;
        font-size: 0.76rem;
        color: #475569;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }

    /* ─── Empty State ─── */
    .cw-empty-state {
        text-align: center;
        padding: 3rem 2rem;
    }
    .cw-empty-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        opacity: 0.4;
    }

    /* ─── Progress Bar ─── */
    .cw-prob-bar-wrap {
        margin-top: 0.75rem;
    }
    .cw-prob-bar-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #64748B;
        margin-bottom: 4px;
        font-weight: 500;
    }
    .cw-prob-bar-track {
        width: 100%;
        height: 8px;
        background: #E2E8F0;
        border-radius: 4px;
        overflow: hidden;
    }
    .cw-prob-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.6s ease;
    }

    /* ─── Tabs Styling ─── */
    div[data-baseweb="tab-list"] {
        background: #F1F5F9 !important;
        border-radius: 8px !important;
        padding: 3px !important;
        gap: 2px !important;
        border: none !important;
    }
    div[data-baseweb="tab"] {
        border-radius: 6px !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1rem !important;
        color: #64748B !important;
        background: transparent !important;
        border: none !important;
    }
    div[data-baseweb="tab"][aria-selected="true"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    }
    div[data-testid="stTabPanel"] {
        padding-top: 1.25rem !important;
        border: none !important;
    }

    /* ─── Expander ─── */
    div[data-testid="stExpander"] {
        border: 1px solid #E8EDF3 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* ─── Slider ─── */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
        background: #10B981 !important;
        border-color: #10B981 !important;
    }

    /* ─── Tooltip cards ─── */
    .cw-info-row {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        padding: 8px 0;
        border-bottom: 1px solid #F1F5F9;
        font-size: 0.82rem;
    }
    .cw-info-row:last-child { border-bottom: none; }
    .cw-info-label { color: #64748B; min-width: 140px; flex-shrink: 0; }
    .cw-info-value { color: #0F172A; font-weight: 500; }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_page_header(page_name: str, subtitle: str = ""):
    """Renders the top breadcrumb + system status bar."""
    sub_html = f'<div style="font-size:0.82rem;color:#64748B;margin-top:2px;">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="cw-page-header">
        <div>
            <div class="cw-breadcrumb">
                <span>CreditWise AI</span>
                <span class="sep">/</span>
                <span class="active">{page_name}</span>
            </div>
            {sub_html}
        </div>
        <div class="cw-header-right">
            <div class="cw-system-badge">
                <span class="cw-dot-green"></span>
                <span>XGBoost v1.2 · Live</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_disclaimer():
    """Renders the standard minimal educational disclaimer."""
    st.markdown("""
    <div class="cw-disclaimer">
        <strong>Academic Prototype:</strong> Trained on the UCI Statlog German Credit benchmark dataset.
        Decisions are illustrative — not for real credit decisioning.
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label: str, value: str, subtext: str = "", accent: str = "#10B981", delta: str = "", delta_up: bool = True):
    """Renders a KPI card with optional accent color and delta."""
    delta_html = ""
    if delta:
        cls = "up" if delta_up else "down"
        arrow = "↑" if delta_up else "↓"
        delta_html = f'<div class="cw-kpi-delta {cls}">{arrow} {delta}</div>'
    return f"""
    <div class="cw-kpi" style="--kpi-accent: {accent};">
        <div class="cw-kpi-label">{label}</div>
        <div class="cw-kpi-value">{value}</div>
        {f'<div class="cw-kpi-delta">{subtext}</div>' if subtext and not delta_html else ''}
        {delta_html}
    </div>
    """


def navigate_to(page_name: str):
    """Programmatically navigates to a target page."""
    st.session_state['current_page'] = page_name
    st.rerun()


# ── Backward-compatibility aliases ──
apply_custom_styles = apply_fintech_theme
render_top_navigation = render_page_header
render_academic_disclaimer = render_disclaimer
