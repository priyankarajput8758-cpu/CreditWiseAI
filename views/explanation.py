"""
Explainability (SHAP) — CreditWise AI
Dedicated SHAP transparency audit for the active applicant assessment.
Features interactive Plotly feature attribution charts, positive vs risk factors,
and regulatory adverse action reason codes.
"""

import streamlit as st
import plotly.graph_objects as go
from utils.styling import render_page_header, render_disclaimer, navigate_to


def render_explanation_page(artifacts):
    render_page_header("Explainability", "Game-theoretic local feature attributions via TreeSHAP")
    render_disclaimer()

    # Empty State Check
    if 'shap_result' not in st.session_state or st.session_state['shap_result'] is None:
        st.markdown("""
        <div class="cw-card" style="text-align:center;padding:3.5rem 2rem;">
            <div style="font-size:0.85rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#64748B;margin-bottom:0.5rem;">
                Audit Log
            </div>
            <h3 style="color:#0F172A;margin-bottom:0.5rem;font-size:1.25rem;">No Active Assessment to Explain</h3>
            <p style="color:#64748B;max-width:520px;margin:0 auto 1.5rem auto;font-size:0.9rem;line-height:1.6;">
                TreeSHAP computes individual feature attributions for a concrete applicant profile.
                Please run a loan assessment first in the <strong>New Assessment</strong> module.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Start New Assessment", use_container_width=True, type="primary"):
                navigate_to("New Assessment")
        return

    shap_res = st.session_state['shap_result']
    pred_res = st.session_state['prediction_result']
    applicant = st.session_state.get('applicant_data', {})
    base_val = shap_res['base_value']
    contributions = shap_res['contributions']

    is_approved = (pred_res['prediction'] == 1)
    accent = "#10B981" if is_approved else "#EF4444"
    badge_cls = "cw-badge-approved" if is_approved else "cw-badge-rejected"

    # Context Header Card
    st.markdown(f"""
    <div class="cw-card" style="border-left:4px solid {accent};padding:1.25rem 1.5rem;margin-bottom:1.25rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
                <span class="cw-badge {badge_cls}" style="margin-bottom:0.4rem;">
                    {pred_res['status_label']} · {pred_res['approval_percentage']}% Approval Probability
                </span>
                <h2 style="margin:0.25rem 0 0.25rem 0;font-size:1.35rem;">SHAP Local Attribution Audit</h2>
                <div style="font-size:0.85rem;color:#64748B;margin-top:4px;">
                    Requested Loan: <strong>{applicant.get('credit_amount', 0):,} DM</strong> over <strong>{applicant.get('duration_months', 0)} months</strong>
                    &nbsp;·&nbsp; Risk Tier: <strong>{pred_res['risk_tier']}</strong>
                </div>
            </div>
            <div style="text-align:right;background:#F8FAFC;padding:10px 18px;border-radius:8px;border:1px solid #E2E8F0;">
                <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;font-weight:700;">Population Base Value</div>
                <div style="font-size:1.45rem;font-weight:800;color:#0F172A;font-family:'JetBrains Mono',monospace;">{base_val:.3f}</div>
                <div style="font-size:0.72rem;color:#64748B;">Prior expected log-odds</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dedicated Adverse Action Notice Box when Rejected
    if not is_approved:
        st.markdown(f"""
        <div style="background:#FEF2F2;border:1px solid #FECACA;border-left:4px solid #EF4444;border-radius:0 8px 8px 0;padding:1.1rem 1.35rem;margin-bottom:1.25rem;">
            <div style="font-weight:700;color:#991B1B;font-size:0.92rem;margin-bottom:6px;">
                Adverse Action Notice: Principal Rejection Factors
            </div>
            <p style="font-size:0.84rem;color:#7F1D1D;line-height:1.55;margin-bottom:8px;">
                Under consumer lending regulations (such as ECOA / Regulation B and the EU AI Act), adverse credit decisions must disclose the specific principal factors for denial. For this applicant, the primary factors that reduced the score below threshold are:
            </p>
            <div style="font-size:0.82rem;color:#991B1B;line-height:1.65;">
        """, unsafe_allow_html=True)
        for r_item in shap_res['top_risk'][:3]:
            st.markdown(f"""
                <div style="margin-bottom:4px;">
                    • <strong>{r_item['label']} ({r_item['value']}):</strong> Subtracted <strong>{abs(r_item['shap_value']):.2f}</strong> from the creditworthiness score.
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # Local Feature Attribution Chart Section
    st.markdown("""
    <div class="cw-card">
        <div class="cw-card-header">
            <span class="cw-card-title">Feature Attribution Matrix (Local SHAP Values)</span>
            <span class="cw-badge cw-badge-neutral">TreeSHAP Engine</span>
        </div>
        <p style="font-size:0.82rem;color:#64748B;margin-bottom:0.75rem;">
            Visualizes the mathematical attribution of each attribute pushing the prediction toward
            <span style="color:#065F46;font-weight:600;">Good Credit Risk (Green)</span> or
            <span style="color:#991B1B;font-weight:600;">Bad Credit Risk (Red)</span>.
        </p>
    """, unsafe_allow_html=True)

    top_n = st.slider("Display Top Contributing Attributes:", min_value=6, max_value=20, value=12, step=1, key="shap_top_slider_page")
    subset = contributions[:top_n]
    subset_plot = list(reversed(subset))

    y_labels = [f"{item['label']} = {item['value']}" for item in subset_plot]
    x_vals = [item['shap_value'] for item in subset_plot]
    colors = ['#10B981' if val > 0 else '#EF4444' for val in x_vals]

    fig_shap = go.Figure()
    fig_shap.add_trace(go.Bar(
        x=x_vals,
        y=y_labels,
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:+.3f}" for v in x_vals],
        textposition='outside',
        textfont=dict(size=10, family='Inter', color='#475569'),
        hovertemplate="<b>%{y}</b><br>SHAP Attribution: <b>%{x:.3f}</b><extra></extra>"
    ))

    fig_shap.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=20, r=60, t=10, b=50),
        height=max(400, top_n * 36),
        xaxis=dict(
            title=dict(
                text="SHAP Value  ←  Rejection Risk  |  Approval Boost  →",
                font=dict(size=11, color='#475569', family='Inter')
            ),
            zeroline=True,
            zerolinecolor="#334155",
            zerolinewidth=1.5,
            gridcolor="#F1F5F9",
            tickfont=dict(size=11, color='#64748B', family='Inter'),
        ),
        yaxis=dict(
            title="",
            autorange=True,
            tickfont=dict(size=11, color='#0F172A', family='Inter')
        ),
        bargap=0.28
    )
    st.plotly_chart(fig_shap, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Top Drivers Comparison Cards (Positive vs Risk)
    c_pos, c_risk = st.columns(2)

    with c_pos:
        st.markdown("""
        <div class="cw-card" style="height:100%;">
            <div class="cw-card-header">
                <span class="cw-card-title" style="color:#065F46;">Positive Approval Drivers</span>
                <span class="cw-badge cw-badge-approved">Confidence Factors</span>
            </div>
            <p style="font-size:0.8rem;color:#64748B;margin-bottom:0.6rem;">Attributes providing the strongest positive push toward approval:</p>
        """, unsafe_allow_html=True)

        if shap_res['top_positive']:
            for item in shap_res['top_positive']:
                st.markdown(f"""
                <div class="cw-factor-positive">
                    <div>
                        <div style="font-size:0.82rem;font-weight:600;color:#065F46;">{item['label']}</div>
                        <div style="font-size:0.74rem;color:#047857;">Value: {item['value']}</div>
                    </div>
                    <span style="font-weight:700;color:#065F46;font-size:0.9rem;">+{item['shap_value']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size:0.82rem;color:#64748B;'>No significant positive drivers identified.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_risk:
        st.markdown("""
        <div class="cw-card" style="height:100%;">
            <div class="cw-card-header">
                <span class="cw-card-title" style="color:#991B1B;">Primary Risk Factors</span>
                <span class="cw-badge cw-badge-rejected">Adverse Action Reasons</span>
            </div>
            <p style="font-size:0.8rem;color:#64748B;margin-bottom:0.6rem;">Attributes representing elevated default risks:</p>
        """, unsafe_allow_html=True)

        if shap_res['top_risk']:
            for item in shap_res['top_risk']:
                st.markdown(f"""
                <div class="cw-factor-negative">
                    <div>
                        <div style="font-size:0.82rem;font-weight:600;color:#991B1B;">{item['label']}</div>
                        <div style="font-size:0.74rem;color:#B91C1C;">Value: {item['value']}</div>
                    </div>
                    <span style="font-weight:700;color:#991B1B;font-size:0.9rem;">{item['shap_value']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size:0.82rem;color:#64748B;'>No significant adverse risk factors identified.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Regulatory & Mathematical Interpretation Guide
    st.markdown(f"""
    <div class="cw-card" style="background:#F8FAFC;">
        <h3 class="cw-card-title" style="margin-bottom:0.6rem;">How to Interpret This Attribution Chart</h3>
        <div style="font-size:0.83rem;color:#475569;line-height:1.65;">
            <ol style="margin-bottom:0;padding-left:1.2rem;">
                <li><strong>Baseline Anchor ({base_val:.3f}):</strong> Represents the prior expected log-odds across the training population before inspecting this individual's application.</li>
                <li><strong>Mathematical Additivity:</strong> The final log-odds prediction is computed as <code>f(x) = Base Value + &sum; SHAP Values</code>. Applying the logistic sigmoid transformation yields the final approval probability of <strong>{pred_res['approval_percentage']}%</strong>.</li>
                <li><strong>Regulatory Reason Codes:</strong> Under the Equal Credit Opportunity Act (ECOA) and EU GDPR Article 22, the top negative SHAP attributes serve as legally defensible, objective adverse action reason codes.</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action footer buttons
    btn_c1, btn_c2, _ = st.columns([1, 1, 2])
    with btn_c1:
        if st.button("New Assessment", type="primary", use_container_width=True):
            navigate_to("New Assessment")
    with btn_c2:
        if st.button("View Model Analytics", type="secondary", use_container_width=True):
            navigate_to("Analytics")
