"""
Page 1: Overview Dashboard View
Institutional fintech overview dashboard featuring real-time KPIs,
actual credit-risk distribution, end-to-end processing pipeline, and session audit history.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styling import render_top_navigation, render_academic_disclaimer
from utils.icons import get_svg_icon

def render_home_page(artifacts):
    """Renders the Overview Dashboard page."""
    render_top_navigation("Overview")
    render_academic_disclaimer()

    metrics = artifacts['metrics']
    acc_formatted = f"{metrics['accuracy']*100:.1f}%"

    # Top Welcome Section with Action Button
    t_col1, t_col2 = st.columns([3, 1])
    with t_col1:
        st.markdown("""
        <div style="margin-bottom: 1.25rem;">
            <h1 style="margin-bottom: 0.25rem;">Welcome to CreditWise AI</h1>
            <p style="color: #64748B; font-size: 0.95rem; margin-top: 0;">
                Intelligent credit assessment with transparent AI explanations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with t_col2:
        st.markdown("<div style='text-align: right; padding-top: 0.5rem;'>", unsafe_allow_html=True)
        if st.button("New Loan Assessment", use_container_width=True, type="primary"):
            st.session_state['current_page'] = "Loan Assessment"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # 4 Primary KPI Cards
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Dataset Records</div>
            <div class="kpi-value">1,000</div>
            <div class="kpi-subtext">UCI Statlog German Credit benchmark</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Prediction Model</div>
            <div class="kpi-value">XGBoost</div>
            <div class="kpi-subtext">Regularized Gradient Boosted Trees</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Explainability</div>
            <div class="kpi-value">TreeSHAP</div>
            <div class="kpi-subtext">Game-theoretic Shapley attributions</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Model Accuracy</div>
            <div class="kpi-value">{acc_formatted}</div>
            <div class="kpi-subtext">Measured on 20% holdout test set</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # Main Dashboard Grid: Credit-Risk Distribution & Pipeline Workflow
    g_left, g_right = st.columns([1, 1])

    with g_left:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div class="saas-card-header">
                <h3 class="saas-card-title">Credit-Risk Benchmark Distribution</h3>
                <span class="badge-neutral">Historical Dataset</span>
            </div>
            <p style="font-size: 0.84rem; color: #64748B; margin-bottom: 0.5rem;">
                Actual class balance in the 1,000 German Credit applicants:
            </p>
        """, unsafe_allow_html=True)

        # Plotly Donut Chart
        labels = ['Good Credit Risk (Approved)', 'Bad Credit Risk (Rejected)']
        values = [700, 300]
        colors = ['#10B981', '#EF4444']

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.6,
            marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='percent',
            hoverinfo='label+value+percent'
        )])

        fig_pie.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10),
            height=240,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=11))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with g_right:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div class="saas-card-header">
                <h3 class="saas-card-title">Automated Underwriting Architecture</h3>
                <span class="badge-neutral">End-to-End Pipeline</span>
            </div>
            <p style="font-size: 0.84rem; color: #64748B; margin-bottom: 0.6rem;">
                How applicant telemetry flows from raw attributes to explainable credit outcomes:
            </p>
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <strong style="font-size: 0.85rem; color: #0F172A;">1. Data Preprocessing & Validation</strong>
                        <div style="font-size: 0.75rem; color: #64748B;">Standardizes numerical scales and encodes categorical attributes.</div>
                    </div>
                    <span class="badge-neutral">Active</span>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <strong style="font-size: 0.85rem; color: #0F172A;">2. XGBoost Ensemble Inference</strong>
                        <div style="font-size: 0.75rem; color: #64748B;">Computes margin score across 100 gradient-boosted decision trees.</div>
                    </div>
                    <span class="badge-neutral">Active</span>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <strong style="font-size: 0.85rem; color: #0F172A;">3. TreeSHAP Attribution Audit</strong>
                        <div style="font-size: 0.75rem; color: #64748B;">Decomposes marginal prediction into additive feature payoffs.</div>
                    </div>
                    <span class="badge-neutral">Active</span>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <strong style="font-size: 0.85rem; color: #0F172A;">4. Transparent Underwriting Decision</strong>
                        <div style="font-size: 0.75rem; color: #64748B;">Provides risk tiers, probability gauges, and adverse action factors.</div>
                    </div>
                    <span class="badge-neutral">Active</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # Recent Assessments Section
    st.markdown("""
    <div class="saas-card">
        <div class="saas-card-header">
            <h3 class="saas-card-title">Recent Session Assessments</h3>
            <span class="badge-neutral">Audit Ledger</span>
        </div>
    """, unsafe_allow_html=True)

    history = st.session_state.get('assessment_history', [])

    if history:
        df_hist = pd.DataFrame(history)
        st.dataframe(df_hist, hide_index=True, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; color: #64748B;">
            <p style="margin-bottom: 0.8rem; font-size: 0.9rem;">
                No assessments executed in the current session yet.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
        with col_c2:
            if st.button("Start First Assessment", use_container_width=True, type="secondary"):
                st.session_state['current_page'] = "Loan Assessment"
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
