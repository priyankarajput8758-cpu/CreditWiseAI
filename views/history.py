"""
Assessment History — CreditWise AI
Session assessment log with search, filter, and summary stats.
"""

import streamlit as st
import pandas as pd
from utils.styling import render_page_header, render_disclaimer, navigate_to


def render_history_page(artifacts):
    render_page_header("Assessment History", "Complete log of assessments from this session")
    render_disclaimer()

    history = st.session_state.get('assessment_history', [])

    # ── Page Title ──
    col_t, col_btn = st.columns([4, 1])
    with col_t:
        st.markdown("""
        <div style="margin-bottom:1rem;">
            <h1 style="margin-bottom:0;">Assessment History</h1>
            <p style="color:#64748B;font-size:0.88rem;margin-top:4px;">
                All credit risk assessments submitted during this session.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        st.markdown("<div style='padding-top:0.6rem;'>", unsafe_allow_html=True)
        if st.button("+ New Assessment", type="primary", use_container_width=True):
            navigate_to("New Assessment")
        st.markdown("</div>", unsafe_allow_html=True)

    if not history:
        # Empty state
        st.markdown("""
        <div class="cw-card" style="text-align:center;padding:3.5rem 2rem;">
            <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#94A3B8;margin-bottom:0.5rem;">Ledger Empty</div>
            <h3 style="color:#0F172A;margin-bottom:0.4rem;">No assessments yet</h3>
            <p style="color:#64748B;font-size:0.88rem;max-width:400px;margin:0 auto 1.25rem auto;">
                Submit a loan application in the New Assessment page to populate your history.
            </p>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("Go to New Assessment", type="primary", use_container_width=True):
                navigate_to("New Assessment")
        return

    df = pd.DataFrame(history)
    total = len(df)
    approved_n = df['Recommendation'].str.contains('Approved').sum()
    rejected_n = total - approved_n
    approval_rate = round(approved_n / total * 100, 1) if total > 0 else 0

    # ── Summary KPIs ──
    k1, k2, k3, k4 = st.columns(4)
    kpi_style = """
        background:#FFFFFF;border:1px solid #E8EDF3;border-radius:10px;
        padding:1rem 1.25rem;box-shadow:0 1px 4px rgba(15,23,42,0.04);
    """
    with k1:
        st.markdown(f"""
        <div style="{kpi_style}">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.07em;color:#64748B;margin-bottom:4px;">Total</div>
            <div style="font-size:1.8rem;font-weight:800;color:#0F172A;letter-spacing:-0.03em;">{total}</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div style="{kpi_style}border-top:3px solid #10B981;">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.07em;color:#64748B;margin-bottom:4px;">Approved</div>
            <div style="font-size:1.8rem;font-weight:800;color:#065F46;letter-spacing:-0.03em;">{approved_n}</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div style="{kpi_style}border-top:3px solid #EF4444;">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.07em;color:#64748B;margin-bottom:4px;">Rejected</div>
            <div style="font-size:1.8rem;font-weight:800;color:#991B1B;letter-spacing:-0.03em;">{rejected_n}</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div style="{kpi_style}border-top:3px solid #8B5CF6;">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.07em;color:#64748B;margin-bottom:4px;">Approval Rate</div>
            <div style="font-size:1.8rem;font-weight:800;color:#6D28D9;letter-spacing:-0.03em;">{approval_rate}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.25rem;'></div>", unsafe_allow_html=True)

    # ── Filter & Search Controls ──
    st.markdown("""
    <div class="cw-card" style="padding:1rem 1.25rem;margin-bottom:1rem;">
        <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.07em;color:#64748B;margin-bottom:0.75rem;">
            Filter & Search
        </div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([2, 1, 1])
    with fc1:
        search = st.text_input("Search by Case ID", placeholder="e.g. APP-101", label_visibility="collapsed")
    with fc2:
        filter_rec = st.selectbox(
            "Recommendation",
            ["All", "Likely Approved", "Likely Rejected"],
            label_visibility="collapsed"
        )
    with fc3:
        sort_order = st.selectbox(
            "Sort",
            ["Newest First", "Oldest First"],
            label_visibility="collapsed"
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Apply Filters ──
    filtered = df.copy()
    if search:
        filtered = filtered[filtered['Case ID'].str.contains(search, case=False, na=False)]
    if filter_rec != "All":
        filtered = filtered[filtered['Recommendation'] == filter_rec]
    if sort_order == "Oldest First":
        filtered = filtered.iloc[::-1]

    # ── Results Table ──
    st.markdown("""
    <div class="cw-card">
        <div class="cw-card-header">
            <span class="cw-card-title">Assessment Records</span>
        </div>
    """, unsafe_allow_html=True)

    if filtered.empty:
        st.markdown("""
        <div style="text-align:center;padding:2rem;color:#94A3B8;font-size:0.88rem;">
            No records match your current filters.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="font-size:0.75rem;color:#64748B;margin-bottom:0.75rem;">
            Showing <strong>{len(filtered)}</strong> of <strong>{total}</strong> records
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(filtered, hide_index=True, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Clear History ──
    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    with st.expander("Session Options"):
        if st.button("Clear Session History", type="secondary"):
            st.session_state['assessment_history'] = []
            st.session_state['prediction_result'] = None
            st.session_state['shap_result'] = None
            st.toast("Session history cleared.")
            st.rerun()
