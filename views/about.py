"""
Page 5: About Project View
Institutional academic documentation covering the problem statement, objectives,
dataset specifications, machine learning architecture, and future research roadmap.
"""

import streamlit as st
from utils.styling import render_top_navigation, render_academic_disclaimer

def render_about_page():
    """Renders the About Project documentation page."""
    render_top_navigation("About Project")
    render_academic_disclaimer()

    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="margin-bottom: 0.2rem;">About CreditWise AI</h1>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 0;">
            Institutional documentation on transparent algorithmic underwriting, regulatory requirements, and technical architecture.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Section 1: Executive Abstract & Problem Statement
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-header">
            <h3 class="saas-card-title">1. Problem Statement & Regulatory Mandate</h3>
            <span class="badge-neutral">Context</span>
        </div>
        <p style="font-size: 0.88rem; color: #334155; line-height: 1.6; margin-bottom: 0.75rem;">
            Modern credit institutions are transitioning from traditional linear scorecards (e.g. FICO score cutoffs) 
            to high-capacity non-linear machine learning ensembles such as <strong>XGBoost</strong>. 
            While ensemble methods deliver significantly superior predictive discrimination and reduced default rates, 
            their multi-layered tree splits function as opaque <strong>"black boxes."</strong>
        </p>
        <p style="font-size: 0.88rem; color: #334155; line-height: 1.6; margin-bottom: 0;">
            In consumer lending, opacity creates substantial legal and procedural liability:
            <ul style="margin-top: 6px; padding-left: 1.2rem; color: #475569; font-size: 0.85rem;">
                <li><strong>ECOA Adverse Action Notices:</strong> The U.S. Equal Credit Opportunity Act mandates that every rejected borrower receive clear, principal reasons for denial.</li>
                <li><strong>EU AI Act & GDPR Article 22:</strong> High-risk automated financial decision-making requires algorithmic transparency, contestability, and a documented right to explanation.</li>
                <li><strong>Fairness & Model Governance:</strong> Underwriting teams require rigorous mathematical tools to verify that models do not replicate historical bias or rely on prohibited proxy attributes.</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Section 2: Core Objectives & Dataset
    col_obj, col_data = st.columns(2)

    with col_obj:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div class="saas-card-header">
                <h3 class="saas-card-title">2. Prototype Objectives</h3>
                <span class="badge-neutral">Scope</span>
            </div>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.6;">
                <p>• <strong>Predictive Accuracy:</strong> Train a gradient-boosted classifier optimized on tabular financial ratios.</p>
                <p>• <strong>Axiomatic Transparency:</strong> Utilize TreeSHAP to compute exact Shapley values that satisfy local accuracy and consistency.</p>
                <p>• <strong>Actionable Explanations:</strong> Translate log-odds contributions into intuitive positive confidence drivers and negative risk factors.</p>
                <p style="margin-bottom: 0;">• <strong>Production UI:</strong> Build an institutional fintech interface designed for underwriting officers and regulatory auditors.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_data:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div class="saas-card-header">
                <h3 class="saas-card-title">3. Benchmark Dataset</h3>
                <span class="badge-neutral">UCI Statlog German Credit</span>
            </div>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.6;">
                <p>• <strong>Source:</strong> University of Hamburg, distributed by UCI Machine Learning Repository.</p>
                <p>• <strong>Scope:</strong> 1,000 historical credit applicants evaluated across 20 financial and demographic features.</p>
                <p>• <strong>Distribution:</strong> 700 Good Credit Risk (Class 1) and 300 Bad Credit Risk (Class 0).</p>
                <p style="margin-bottom: 0;">• <strong>Attributes:</strong> Checking status, savings balance, loan tenure, loan purpose, property ownership, employment tenure, and existing credits.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # Section 3: Technical Foundation (XGBoost & SHAP)
    col_xgb, col_shap = st.columns(2)

    with col_xgb:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div class="saas-card-header">
                <h3 class="saas-card-title">4. Machine Learning: XGBoost</h3>
                <span class="badge-neutral">Ensemble Model</span>
            </div>
            <p style="font-size: 0.84rem; color: #475569; line-height: 1.55;">
                <strong>Extreme Gradient Boosting (XGBoost)</strong> was chosen for tabular credit risk modeling because:
            </p>
            <ul style="font-size: 0.82rem; color: #475569; line-height: 1.5; padding-left: 1.1rem; margin-bottom: 0;">
                <li>Consistently outperforms deep learning architectures on small-to-medium tabular credit datasets.</li>
                <li>Captures complex non-linear feature interactions (such as loan amount versus checking balance).</li>
                <li>Employs L1/L2 leaf weight regularization and max depth constraints to prevent overfitting.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_shap:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div class="saas-card-header">
                <h3 class="saas-card-title">5. Explainability: TreeSHAP</h3>
                <span class="badge-neutral">Game Theory Core</span>
            </div>
            <p style="font-size: 0.84rem; color: #475569; line-height: 1.55;">
                <strong>SHAP (SHapley Additive exPlanations)</strong> provides four fundamental mathematical guarantees:
            </p>
            <ul style="font-size: 0.82rem; color: #475569; line-height: 1.5; padding-left: 1.1rem; margin-bottom: 0;">
                <li><strong>Local Accuracy:</strong> Sum of SHAP attributions exactly equals the difference between model output and expected baseline.</li>
                <li><strong>Consistency:</strong> If a model changes such that a feature's marginal contribution increases, its SHAP attribution never decreases.</li>
                <li><strong>TreeSHAP Efficiency:</strong> Evaluates exact Shapley values in polynomial time rather than exponential time.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # Section 4: Planned Future Enhancements Roadmap
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-header">
            <h3 class="saas-card-title">6. Planned Research Roadmap & Future Enhancements</h3>
            <span class="badge-neutral">Subsequent Iterations</span>
        </div>
        <p style="font-size: 0.84rem; color: #64748B; margin-bottom: 1rem;">
            The following enhancements are formally structured for subsequent releases of this research project:
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 14px;">
                <strong style="color: #0F172A; font-size: 0.86rem;">1. LIME Integration & Comparative Explainability</strong>
                <p style="font-size: 0.8rem; color: #64748B; margin-top: 4px; margin-bottom: 0;">
                    Incorporate Local Interpretable Model-agnostic Explanations (LIME) to generate local linear surrogate approximations and contrast stability against SHAP.
                </p>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 14px;">
                <strong style="color: #0F172A; font-size: 0.86rem;">2. Counterfactual Explanations (DiCE)</strong>
                <p style="font-size: 0.8rem; color: #64748B; margin-top: 4px; margin-bottom: 0;">
                    Implement Diverse Counterfactual Explanations to deliver actionable recourse (e.g. <em>"If loan amount is reduced to 4,500 DM, application will be approved"</em>).
                </p>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 14px;">
                <strong style="color: #0F172A; font-size: 0.86rem;">3. Algorithmic Fairness Auditing</strong>
                <p style="font-size: 0.8rem; color: #64748B; margin-top: 4px; margin-bottom: 0;">
                    Audit predictions across demographic subsets using Disparate Impact Ratio, Equalized Odds, and Demographic Parity metrics.
                </p>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 14px;">
                <strong style="color: #0F172A; font-size: 0.86rem;">4. Explanation Stability & Sensitivity Testing</strong>
                <p style="font-size: 0.8rem; color: #64748B; margin-top: 4px; margin-bottom: 0;">
                    Measure attribution invariance under input perturbations and random seed retraining to test adversarial robustness.
                </p>
            </div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 14px; margin-top: 12px;">
            <strong style="color: #0F172A; font-size: 0.86rem;">5. Real-World Evaluation & Regulatory Reason Codes</strong>
            <p style="font-size: 0.8rem; color: #64748B; margin-top: 4px; margin-bottom: 0;">
                Conduct qualitative user evaluations with professional commercial underwriters and map negative SHAP factors directly to standardized credit bureau reason codes.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
