"""
About — CreditWise AI
Project overview, tech stack, dataset info, and methodology.
"""

import streamlit as st
from utils.styling import render_page_header, render_disclaimer


def render_about_page():
    render_page_header("About", "Project documentation & technical overview")
    render_disclaimer()

    st.markdown("""
    <div style="margin-bottom:1.25rem;">
        <h1 style="margin-bottom:0;">About CreditWise AI</h1>
        <p style="color:#64748B;font-size:0.9rem;margin-top:4px;">
            An explainable AI credit risk platform built for transparent, fair lending decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Mission Card ──
    st.markdown("""
    <div class="cw-card" style="border-left:4px solid #10B981;">
        <div style="display:flex;gap:1.25rem;align-items:flex-start;flex-wrap:wrap;">
            <div style="flex:1;min-width:260px;">
                <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;
                            color:#10B981;margin-bottom:0.5rem;">Mission</div>
                <h2 style="margin-bottom:0.5rem;font-size:1.2rem;">
                    Transparent Credit Decisioning with Explainable AI
                </h2>
                <p style="font-size:0.85rem;color:#475569;line-height:1.65;margin-bottom:0;">
                    CreditWise AI demonstrates how machine learning can power credit risk assessment while
                    remaining fully transparent to applicants, analysts, and regulators. Every prediction
                    comes with mathematical attribution explaining exactly <em>why</em> a decision was reached —
                    not just <em>what</em> the decision was.
                </p>
            </div>
            <div style="display:flex;flex-direction:column;gap:8px;min-width:180px;">
                <div style="background:#F0FDF4;border:1px solid #A7F3D0;border-radius:8px;padding:0.75rem 1rem;text-align:center;">
                    <div style="font-size:1.6rem;font-weight:800;color:#065F46;">1,000</div>
                    <div style="font-size:0.72rem;color:#047857;font-weight:600;">Training Records</div>
                </div>
                <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:0.75rem 1rem;text-align:center;">
                    <div style="font-size:1.6rem;font-weight:800;color:#1D4ED8;">20</div>
                    <div style="font-size:0.72rem;color:#1D4ED8;font-weight:600;">Input Features</div>
                </div>
                <div style="background:#F5F3FF;border:1px solid #DDD6FE;border-radius:8px;padding:0.75rem 1rem;text-align:center;">
                    <div style="font-size:1.6rem;font-weight:800;color:#6D28D9;">100</div>
                    <div style="font-size:0.72rem;color:#6D28D9;font-weight:600;">XGBoost Trees</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Two column layout ──
    col_left, col_right = st.columns([1, 1])

    with col_left:
        # Tech Stack
        st.markdown("""
        <div class="cw-card">
            <div class="cw-card-header">
                <span class="cw-card-title">Technology Stack</span>
                <span class="cw-badge cw-badge-info">Open Source</span>
            </div>
        """, unsafe_allow_html=True)

        stack = [
            ("Python 3.10+",         "Core application language"),
            ("Streamlit",            "Interactive web application framework"),
            ("XGBoost",              "Gradient boosted tree ensemble classifier"),
            ("SHAP (TreeSHAP)",      "Game-theoretic local & global explanations"),
            ("Scikit-Learn",         "Preprocessing, encoding, evaluation metrics"),
            ("Plotly",               "Interactive charts and visualizations"),
            ("Pandas / NumPy",       "Data manipulation and numerical computing"),
        ]
        for icon_name, desc in stack:
            st.markdown(f"""
            <div class="cw-info-row">
                <div class="cw-info-label">{icon_name}</div>
                <div class="cw-info-value">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Model Architecture
        st.markdown("""
        <div class="cw-card">
            <div class="cw-card-header">
                <span class="cw-card-title">Model Architecture</span>
                <span class="cw-badge cw-badge-neutral">XGBoost Config</span>
            </div>
        """, unsafe_allow_html=True)

        config = [
            ("Estimators",        "100 boosted trees"),
            ("Max Depth",         "4 levels per tree"),
            ("Learning Rate",     "0.08 (conservative)"),
            ("Subsample",         "85% row sampling"),
            ("Col Sample",        "85% feature sampling"),
            ("Train / Test Split","80% / 20% stratified"),
            ("Eval Metric",       "Log-loss (logloss)"),
            ("Random Seed",       "42 (reproducible)"),
        ]
        for label, val in config:
            st.markdown(f"""
            <div class="cw-info-row">
                <div class="cw-info-label">{label}</div>
                <div class="cw-info-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # Dataset Info
        st.markdown("""
        <div class="cw-card">
            <div class="cw-card-header">
                <span class="cw-card-title">Dataset — UCI Statlog German Credit</span>
                <span class="cw-badge cw-badge-neutral">Benchmark</span>
            </div>
            <p style="font-size:0.82rem;color:#475569;line-height:1.6;margin-bottom:0.75rem;">
                The German Credit dataset is a classic benchmark for binary credit risk classification,
                originally compiled by Prof. Hans Hofmann at the University of Hamburg and published
                on the <a href="https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data)"
                style="color:#10B981;text-decoration:none;font-weight:600;">UCI Machine Learning Repository</a>.
            </p>
        """, unsafe_allow_html=True)

        dataset_facts = [
            ("Records",         "1,000 applicants"),
            ("Good Credit",     "700 (70%) — target class 1"),
            ("Bad Credit",      "300 (30%) — target class 0"),
            ("Features",        "20 (mix of numeric & categorical)"),
            ("Origin",          "West Germany, 1994"),
            ("License",         "Public domain / UCI Repository"),
        ]
        for label, val in dataset_facts:
            st.markdown(f"""
            <div class="cw-info-row">
                <div class="cw-info-label">{label}</div>
                <div class="cw-info-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Assessment Workflow
        st.markdown("""
        <div class="cw-card">
            <div class="cw-card-header">
                <span class="cw-card-title">Assessment Workflow</span>
                <span class="cw-badge cw-badge-approved">End-to-End</span>
            </div>
        """, unsafe_allow_html=True)

        steps = [
            ("1", "#10B981", "Data Input",
             "Applicant profile entered via structured 3-section form with 20 financial, demographic & credit attributes."),
            ("2", "#0A1628", "Preprocessing",
             "Categorical features label-encoded using fitted LabelEncoders trained on the full dataset."),
            ("3", "#8B5CF6", "XGBoost Inference",
             "100-tree gradient boosted ensemble produces binary prediction + calibrated approval probability."),
            ("4", "#F59E0B", "SHAP Attribution",
             "TreeSHAP decomposes the prediction into additive per-feature Shapley value contributions."),
            ("5", "#10B981", "Decision Output",
             "Risk tier, probability score, approval status, and adverse action reason codes delivered to analyst."),
        ]
        for num, color, title, desc in steps:
            st.markdown(f"""
            <div style="display:flex;gap:12px;padding:0.65rem 0;border-bottom:1px solid #F1F5F9;align-items:flex-start;">
                <div style="width:24px;height:24px;background:{color};color:#fff;border-radius:50%;
                            display:flex;align-items:center;justify-content:center;font-size:0.65rem;
                            font-weight:800;flex-shrink:0;margin-top:1px;">{num}</div>
                <div>
                    <div style="font-size:0.82rem;font-weight:600;color:#0F172A;margin-bottom:2px;">{title}</div>
                    <div style="font-size:0.76rem;color:#64748B;line-height:1.5;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Regulatory Note ──
    st.markdown("""
    <div class="cw-card" style="background:#F8FAFC;border-left:4px solid #64748B;">
        <div class="cw-card-header" style="border-bottom:none;padding-bottom:0;margin-bottom:0.5rem;">
            <span class="cw-card-title">Regulatory Alignment & Limitations</span>
            <span class="cw-badge cw-badge-warning">Academic Use Only</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
            <div>
                <div style="font-size:0.75rem;font-weight:700;color:#0F172A;margin-bottom:0.4rem;">
                    Explainability Standards Addressed
                </div>
                <div style="font-size:0.78rem;color:#475569;line-height:1.6;">
                    • <strong>ECOA / Reg B:</strong> Top negative SHAP values serve as adverse action reason codes.<br>
                    • <strong>EU AI Act:</strong> High-risk AI transparency requirements via SHAP attributions.<br>
                    • <strong>GDPR Art. 22:</strong> Right to explanation for automated decisions.
                </div>
            </div>
            <div>
                <div style="font-size:0.75rem;font-weight:700;color:#0F172A;margin-bottom:0.4rem;">
                    Important Limitations
                </div>
                <div style="font-size:0.78rem;color:#475569;line-height:1.6;">
                    • Trained on 1990s German data — not suitable for real-world credit decisioning.<br>
                    • Currency in Deutsche Mark (DM); not adjusted for inflation or geography.<br>
                    • No bias/fairness audit has been performed on demographic features.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
