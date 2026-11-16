"""
Page 3: Prediction Results View
Presents the model decision, predicted probabilities, key influencing factors,
and model performance evaluation metrics.
"""

import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from utils.styling import render_disclaimer

def render_results_page(artifacts):
    """Renders the Prediction Results page."""
    st.markdown("## 📊 AI Credit Risk Assessment Result")
    render_disclaimer()

    # Empty State Check
    if 'prediction_result' not in st.session_state or st.session_state['prediction_result'] is None:
        st.markdown("""
        <div class="fintech-card" style="text-align: center; padding: 3rem 2rem;">
            <div style="font-size: 2.8rem; margin-bottom: 0.8rem;">📋</div>
            <h3 style="color: #0F382C; margin-bottom: 0.5rem;">No Applicant Assessment Run Yet</h3>
            <p style="color: #6C7D75; max-width: 500px; margin: 0 auto 1.5rem auto;">
                Please configure an applicant's financial profile or load a demo preset in the 
                <strong>Applicant Prediction</strong> page to generate a real-time assessment.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📝 Go to Applicant Prediction Form", use_container_width=True, type="primary"):
                st.session_state['current_page'] = "Applicant Prediction"
                st.rerun()
        return

    result = st.session_state['prediction_result']
    shap_res = st.session_state.get('shap_result', None)
    applicant = st.session_state.get('applicant_data')
    if not isinstance(applicant, dict):
        applicant = {}
    metrics = artifacts['metrics']

    is_approved = (result['prediction'] == 1)
    status_label = result['status_label']
    prob_approved = result['approval_percentage']
    prob_rejected = result['rejection_percentage']
    risk_tier = result['risk_tier']

    # Big Prominent Decision Banner
    if is_approved:
        st.markdown(f"""
        <div class="decision-banner-approved">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <span class="pill-approved" style="font-size: 0.88rem; padding: 6px 14px; margin-bottom: 0.6rem;">
                        ✔ Recommended Credit Decision
                    </span>
                    <h1 style="color: #176B41 !important; margin: 0.3rem 0; font-size: 2.4rem;">{status_label}</h1>
                    <p style="color: #26593F; margin: 0; font-size: 1.05rem;">
                        The model classifies this profile as <strong>Good Credit Risk</strong> with <strong>{prob_approved}%</strong> confidence.
                    </p>
                </div>
                <div style="text-align: right; background: rgba(255,255,255,0.7); padding: 1rem 1.6rem; border-radius: 12px; border: 1px solid #C4EBD4;">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: #507A65; font-weight: 600;">Approval Probability</div>
                    <div style="font-size: 2.2rem; font-weight: 700; color: #176B41; font-family: 'Space Grotesk', sans-serif;">{prob_approved}%</div>
                    <div style="font-size: 0.8rem; color: #507A65;">Tier: <strong>{risk_tier}</strong></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="decision-banner-rejected">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <span class="pill-rejected" style="font-size: 0.88rem; padding: 6px 14px; margin-bottom: 0.6rem;">
                        ✖ Elevated Credit Risk Detected
                    </span>
                    <h1 style="color: #BA2D21 !important; margin: 0.3rem 0; font-size: 2.4rem;">{status_label}</h1>
                    <p style="color: #792A23; margin: 0; font-size: 1.05rem;">
                        The model classifies this profile as <strong>Bad Credit Risk</strong>. Probability of default risk: <strong>{prob_rejected}%</strong>.
                    </p>
                </div>
                <div style="text-align: right; background: rgba(255,255,255,0.7); padding: 1rem 1.6rem; border-radius: 12px; border: 1px solid #F5CDC9;">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: #8F4C45; font-weight: 600;">Rejection Probability</div>
                    <div style="font-size: 2.2rem; font-weight: 700; color: #BA2D21; font-family: 'Space Grotesk', sans-serif;">{prob_rejected}%</div>
                    <div style="font-size: 0.8rem; color: #8F4C45;">Tier: <strong>{risk_tier}</strong></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4 Quantitative Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-box {'positive' if is_approved else 'negative'}">
            <div class="metric-label">Approval Confidence</div>
            <div class="metric-value">{prob_approved}%</div>
            <div class="metric-subtext">Estimated likelihood of timely repayment</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Loan Principal</div>
            <div class="metric-value">{applicant.get('credit_amount', 0):,} DM</div>
            <div class="metric-subtext">Tenure: {applicant.get('duration_months', 0)} months</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Checking Balance</div>
            <div class="metric-value" style="font-size: 1.25rem; line-height: 1.4;">{applicant.get('checking_status', 'N/A')}</div>
            <div class="metric-subtext">Liquid account standing</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Savings Position</div>
            <div class="metric-value" style="font-size: 1.25rem; line-height: 1.4;">{applicant.get('savings_status', 'N/A')}</div>
            <div class="metric-subtext">Capital buffer reserve</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Two columns: Key Factors Preview & Model Test Set Snapshot
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown("""
        <div class="fintech-card">
            <div class="fintech-card-header">
                <h4 class="fintech-card-title">🔍 Primary Influencing Factors Preview</h4>
                <span class="pill-neutral">Local SHAP</span>
            </div>
            <p style="font-size: 0.84rem; color: #6C7D75; margin-bottom: 0.8rem;">
                The primary attributes driving the XGBoost tree ensemble decision for this specific applicant:
            </p>
        """, unsafe_allow_html=True)

        if shap_res:
            top_pos = shap_res['top_positive'][:2]
            top_neg = shap_res['top_risk'][:2]

            for item in top_pos:
                st.markdown(f"""
                <div class="factor-item factor-positive">
                    <span><strong>{item['label']}</strong>: {item['value']}</span>
                    <span style="font-weight: 600;">+{item['shap_value']:.2f} (Boosts Approval)</span>
                </div>
                """, unsafe_allow_html=True)

            for item in top_neg:
                st.markdown(f"""
                <div class="factor-item factor-negative">
                    <span><strong>{item['label']}</strong>: {item['value']}</span>
                    <span style="font-weight: 600;">{item['shap_value']:.2f} (Increases Risk)</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
            <div style="margin-top: 1.2rem; text-align: center;">
        """, unsafe_allow_html=True)
        if st.button("🔎 Inspect Full SHAP Explanation Waterfall ➔", type="primary", use_container_width=True):
            st.session_state['current_page'] = "SHAP Explanation"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    with right_col:
        st.markdown(f"""
        <div class="fintech-card">
            <div class="fintech-card-header">
                <h4 class="fintech-card-title">📈 Model Test Performance Snapshot</h4>
                <span class="pill-approved">Trained Model</span>
            </div>
            <p style="font-size: 0.84rem; color: #6C7D75; margin-bottom: 0.8rem;">
                Evaluated on an independent 20% holdout test partition (200 credit applicants):
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 1rem;">
                <div style="background: #F8FAF9; padding: 8px 12px; border-radius: 8px; border: 1px solid #E8EFEA;">
                    <span style="font-size: 0.75rem; color: #6C7D75;">Test Accuracy:</span><br>
                    <strong style="color: #0F382C; font-size: 1.1rem;">{metrics['accuracy']*100:.1f}%</strong>
                </div>
                <div style="background: #F8FAF9; padding: 8px 12px; border-radius: 8px; border: 1px solid #E8EFEA;">
                    <span style="font-size: 0.75rem; color: #6C7D75;">F1-Score (Macro):</span><br>
                    <strong style="color: #0F382C; font-size: 1.1rem;">{metrics['f1_score']:.3f}</strong>
                </div>
                <div style="background: #F8FAF9; padding: 8px 12px; border-radius: 8px; border: 1px solid #E8EFEA;">
                    <span style="font-size: 0.75rem; color: #6C7D75;">Precision (Approved):</span><br>
                    <strong style="color: #0F382C; font-size: 1.1rem;">{metrics['precision']*100:.1f}%</strong>
                </div>
                <div style="background: #F8FAF9; padding: 8px 12px; border-radius: 8px; border: 1px solid #E8EFEA;">
                    <span style="font-size: 0.75rem; color: #6C7D75;">Recall (Approved):</span><br>
                    <strong style="color: #0F382C; font-size: 1.1rem;">{metrics['recall']*100:.1f}%</strong>
                </div>
            </div>
            <div style="font-size: 0.78rem; color: #7F8E87;">
                Confusion Matrix: True Rejected: <strong>{metrics['confusion_matrix'][0][0]}</strong> | False Approved: <strong>{metrics['confusion_matrix'][0][1]}</strong> | False Rejected: <strong>{metrics['confusion_matrix'][1][0]}</strong> | True Approved: <strong>{metrics['confusion_matrix'][1][1]}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Detailed Applicant Profile Snapshot
    st.markdown("### 📋 Captured Applicant Data Summary")
    with st.expander("Click to view complete submitted applicant feature table", expanded=False):
        summary_rows = []
        for k, v in applicant.items():
            if k not in ['name', 'description']:
                summary_rows.append({
                    "Feature Name": artifacts.get('feature_labels', {}).get(k, k.replace('_', ' ').title()),
                    "Applicant Value": str(v)
                })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
