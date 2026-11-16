"""
Page 3: Explainability View
Dedicated SHAP transparency audit for the active applicant assessment.
Features interactive Plotly feature attribution waterfalls, positive vs risk factors,
and mathematical interpretation guidelines.
"""

import streamlit as st
import plotly.graph_objects as go
from utils.styling import render_top_navigation, render_academic_disclaimer

def render_explanation_page(artifacts):
    """Renders the Explainability (SHAP) audit page."""
    render_top_navigation("Explainability")
    render_academic_disclaimer()

    # Empty State Check
    if 'shap_result' not in st.session_state or st.session_state['shap_result'] is None:
        st.markdown("""
        <div class="saas-card" style="text-align: center; padding: 3rem 2rem;">
            <h3 style="color: #0F172A; margin-bottom: 0.5rem;">No Active Assessment to Explain</h3>
            <p style="color: #64748B; max-width: 500px; margin: 0 auto 1.5rem auto; font-size: 0.9rem;">
                Please run a loan assessment first in the <strong>Loan Assessment</strong> module. 
                SHAP computes local game-theoretic feature attributions for a concrete applicant profile.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Go to Loan Assessment", use_container_width=True, type="primary"):
                st.session_state['current_page'] = "Loan Assessment"
                st.rerun()
        return

    shap_res = st.session_state['shap_result']
    pred_res = st.session_state['prediction_result']
    applicant = st.session_state.get('applicant_data', {})
    base_val = shap_res['base_value']
    contributions = shap_res['contributions']

    is_approved = (pred_res['prediction'] == 1)

    # Context Header Card
    st.markdown(f"""
    <div class="saas-card" style="border-left: 4px solid {'#10B981' if is_approved else '#EF4444'};">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <span class="{'badge-approved' if is_approved else 'badge-rejected'}" style="margin-bottom: 0.4rem;">
                    {pred_res['status_label']} ({pred_res['approval_percentage']}% Approval Prob)
                </span>
                <h2 style="margin: 0.2rem 0 0 0;">SHAP Local Attribution Audit</h2>
                <div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">
                    Requested Loan: <strong>{applicant.get('credit_amount', 0):,} DM</strong> over <strong>{applicant.get('duration_months', 0)} months</strong> | Risk Tier: <strong>{pred_res['risk_tier']}</strong>
                </div>
            </div>
            <div style="text-align: right; background: #F8FAFC; padding: 10px 16px; border-radius: 8px; border: 1px solid #E2E8F0;">
                <div style="font-size: 0.72rem; text-transform: uppercase; color: #64748B; font-weight: 600;">Population Base Value</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: #0F172A; font-family: 'JetBrains Mono', monospace;">{base_val:.3f}</div>
                <div style="font-size: 0.72rem; color: #64748B;">Prior expected log-odds</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dedicated Adverse Action Notice Box when Rejected
    if not is_approved:
        st.markdown(f"""
        <div style="background: #FEF2F2; border: 1.5px solid #FECACA; border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 1.25rem;">
            <div style="font-weight: 700; color: #991B1B; font-size: 0.92rem; margin-bottom: 6px;">
                Adverse Action Notice: Why This Loan Application Was Rejected
            </div>
            <p style="font-size: 0.84rem; color: #7F1D1D; line-height: 1.5; margin-bottom: 8px;">
                Under consumer lending regulations (such as ECOA / FCRA and the EU AI Act), adverse credit decisions must disclose the specific principal factors for denial. For this applicant, the primary factors that pulled the score into the rejection zone are:
            </p>
            <div style="font-size: 0.82rem; color: #991B1B; line-height: 1.6;">
        """, unsafe_allow_html=True)
        for r_item in shap_res['top_risk'][:3]:
            st.markdown(f"""
                <div style="margin-bottom: 4px;">
                    • <strong>{r_item['label']} ({r_item['value']}):</strong> Subtracted <strong>{abs(r_item['shap_value']):.2f}</strong> from the creditworthiness margin score.
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # Local Feature Attribution Chart Section
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-header">
            <h3 class="saas-card-title">Feature Attribution Matrix (Local SHAP Values)</h3>
            <span class="badge-neutral">TreeSHAP Engine</span>
        </div>
        <p style="font-size: 0.84rem; color: #64748B; margin-bottom: 0.8rem;">
            Visualizes the mathematical force of each attribute pushing the log-odds toward 
            <span style="color: #065F46; font-weight: 600;">Good Credit Risk (Green)</span> or 
            <span style="color: #991B1B; font-weight: 600;">Bad Credit Risk (Red)</span>.
        </p>
    """, unsafe_allow_html=True)

    # Filter top features
    top_n = st.slider("Display Top Contributing Attributes:", min_value=6, max_value=20, value=12, step=1)
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
        marker=dict(
            color=colors,
            line=dict(color='rgba(0,0,0,0.1)', width=1)
        ),
        text=[f"{v:+.2f}" for v in x_vals],
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>SHAP Attribution: <b>%{x:.3f}</b><extra></extra>"
    ))

    fig_shap.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=20, r=40, t=10, b=50),
        height=480,
        xaxis=dict(
            title="<b>SHAP Value (Impact on Log-Odds)</b><br><span style='font-size: 11px; color: #64748B;'>← Increases Rejection Risk | Increases Approval Likelihood →</span>",
            zeroline=True,
            zerolinecolor="#334155",
            zerolinewidth=2,
            gridcolor="#F1F5F9"
        ),
        yaxis=dict(
            title="",
            autorange=True,
            tickfont=dict(size=12, color='#0F172A')
        ),
        bargap=0.25
    )
    st.plotly_chart(fig_shap, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Top Drivers Comparison Cards (Positive vs Risk)
    c_pos, c_risk = st.columns(2)

    with c_pos:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div class="saas-card-header">
                <h3 class="saas-card-title" style="color: #065F46;">Positive Approval Drivers</h3>
                <span class="badge-approved">Confidence Factors</span>
            </div>
            <p style="font-size: 0.8rem; color: #64748B; margin-bottom: 0.6rem;">Attributes providing the strongest positive push toward approval:</p>
        """, unsafe_allow_html=True)

        if shap_res['top_positive']:
            for item in shap_res['top_positive']:
                st.markdown(f"""
                <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 0.82rem; color: #065F46;">{item['label']}</strong><br>
                        <span style="font-size: 0.74rem; color: #047857;">Value: {item['value']}</span>
                    </div>
                    <span style="font-weight: 700; color: #065F46; font-size: 0.9rem;">+{item['shap_value']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size: 0.82rem; color: #64748B;'>No significant positive drivers identified.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_risk:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div class="saas-card-header">
                <h3 class="saas-card-title" style="color: #991B1B;">Primary Risk Factors</h3>
                <span class="badge-rejected">Adverse Action Reasons</span>
            </div>
            <p style="font-size: 0.8rem; color: #64748B; margin-bottom: 0.6rem;">Attributes representing elevated default risks:</p>
        """, unsafe_allow_html=True)

        if shap_res['top_risk']:
            for item in shap_res['top_risk']:
                st.markdown(f"""
                <div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 0.82rem; color: #991B1B;">{item['label']}</strong><br>
                        <span style="font-size: 0.74rem; color: #B91C1C;">Value: {item['value']}</span>
                    </div>
                    <span style="font-weight: 700; color: #991B1B; font-size: 0.9rem;">{item['shap_value']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size: 0.82rem; color: #64748B;'>No significant adverse risk factors identified.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # Academic & Regulatory Interpretation Guide
    st.markdown(f"""
    <div class="saas-card" style="background: #F8FAFC;">
        <h3 class="saas-card-title" style="margin-bottom: 0.6rem;">How to Interpret This Attribution Chart</h3>
        <div style="font-size: 0.84rem; color: #475569; line-height: 1.6;">
            <ol style="margin-bottom: 0; padding-left: 1.2rem;">
                <li><strong>Baseline Anchor ({base_val:.3f}):</strong> Represents the prior expected log-odds across all 1,000 training cases before inspecting this individual's application.</li>
                <li><strong>Mathematical Additivity:</strong> The final prediction is computed directly as <code>f(x) = Base Value + &sum; SHAP Values</code>. Applying the logistic sigmoid transformation yields the final approval probability of <strong>{pred_res['approval_percentage']}%</strong>.</li>
                <li><strong>Regulatory Reason Codes:</strong> Under the Equal Credit Opportunity Act (ECOA) and EU GDPR Article 22, the top negative SHAP attributes serve as legally defensible, objective adverse action reason codes.</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
