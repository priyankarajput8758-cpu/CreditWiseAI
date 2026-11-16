"""
Analytics — CreditWise AI
Technical model diagnostics, SHAP feature importance, confusion matrix,
classification report, and local SHAP explanation for the last assessment.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from utils.styling import render_page_header, render_disclaimer, navigate_to


def render_analytics_page(artifacts):
    render_page_header("Analytics", "Model performance diagnostics & SHAP explainability")
    render_disclaimer()

    metrics = artifacts['metrics']
    cm = metrics['confusion_matrix']
    global_df = artifacts['global_importance_df']

    st.markdown("""
    <div style="margin-bottom:1.25rem;">
        <h1 style="margin-bottom:0;">Model Analytics</h1>
        <p style="color:#64748B;font-size:0.88rem;margin-top:4px;">
            XGBoost classifier evaluated on a stratified 20% holdout (200 cases).
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ──
    k1, k2, k3, k4 = st.columns(4)
    kpi_s = "background:#FFFFFF;border:1px solid #E8EDF3;border-radius:10px;padding:1.1rem 1.25rem;box-shadow:0 1px 4px rgba(15,23,42,0.04);"

    with k1:
        st.markdown(f"""
        <div style="{kpi_s}border-top:3px solid #0A1628;">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;margin-bottom:4px;">Test Accuracy</div>
            <div style="font-size:1.9rem;font-weight:800;color:#0F172A;letter-spacing:-0.03em;">{metrics['accuracy']*100:.1f}%</div>
            <div style="font-size:0.72rem;color:#64748B;">N = 200 holdout cases</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div style="{kpi_s}border-top:3px solid #10B981;">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;margin-bottom:4px;">F1 Score</div>
            <div style="font-size:1.9rem;font-weight:800;color:#0F172A;letter-spacing:-0.03em;">{metrics['f1_score']:.3f}</div>
            <div style="font-size:0.72rem;color:#64748B;">Harmonic precision/recall</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div style="{kpi_s}border-top:3px solid #8B5CF6;">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;margin-bottom:4px;">Precision</div>
            <div style="font-size:1.9rem;font-weight:800;color:#0F172A;letter-spacing:-0.03em;">{metrics['precision']*100:.1f}%</div>
            <div style="font-size:0.72rem;color:#64748B;">True positive predictive value</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div style="{kpi_s}border-top:3px solid #F59E0B;">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;margin-bottom:4px;">Recall</div>
            <div style="font-size:1.9rem;font-weight:800;color:#0F172A;letter-spacing:-0.03em;">{metrics['recall']*100:.1f}%</div>
            <div style="font-size:0.72rem;color:#64748B;">Sensitivity on approvals</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.25rem;'></div>", unsafe_allow_html=True)

    # ── Tabs ──
    tab_global, tab_local, tab_matrix = st.tabs([
        "  Global Feature Importance  ",
        "  Local SHAP Explanation  ",
        "  Confusion Matrix & Report  ",
    ])

    # ── Tab 1: Global Feature Importance ──
    with tab_global:
        st.markdown("""
        <div class="cw-card">
            <div class="cw-card-header">
                <span class="cw-card-title">Global Feature Importance — Mean |SHAP| Across Test Set</span>
                <span class="cw-badge cw-badge-neutral">TreeSHAP</span>
            </div>
            <p style="font-size:0.8rem;color:#64748B;margin-bottom:0.75rem;">
                Average marginal contribution of each attribute across all 200 holdout applicants.
                Longer bars = greater average impact on credit decisions.
            </p>
        """, unsafe_allow_html=True)

        top14 = global_df.head(14).iloc[::-1]
        # Colour gradient based on rank
        bar_colors = [f"rgba(10,22,40,{0.5 + 0.5*(i/13)})" for i in range(len(top14))]

        fig_feat = go.Figure()
        fig_feat.add_trace(go.Bar(
            x=top14['mean_abs_shap'],
            y=top14['label'],
            orientation='h',
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{v:.3f}" for v in top14['mean_abs_shap']],
            textposition='outside',
            textfont=dict(size=11, color='#64748B', family='Inter'),
            hovertemplate="<b>%{y}</b><br>Mean |SHAP|: %{x:.4f}<extra></extra>"
        ))
        fig_feat.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=20, r=60, t=10, b=40),
            height=430,
            xaxis=dict(
                title=dict(text="Mean Absolute SHAP Value", font=dict(size=12, color='#475569', family='Inter')),
                gridcolor="#F1F5F9",
                tickfont=dict(size=11, color='#64748B', family='Inter'),
                zeroline=False,
            ),
            yaxis=dict(
                tickfont=dict(size=12, color='#0F172A', family='Inter'),
                autorange=True,
            ),
            bargap=0.3,
        )
        st.plotly_chart(fig_feat, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: Local SHAP ──
    with tab_local:
        shap_res = st.session_state.get('shap_result')
        pred_res = st.session_state.get('prediction_result')
        applicant = st.session_state.get('applicant_data', {})

        if shap_res is None or pred_res is None:
            st.markdown("""
            <div class="cw-card" style="text-align:center;padding:3rem 2rem;">
                <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#94A3B8;margin-bottom:0.4rem;">Single-Case Audit</div>
                <h3 style="color:#0F172A;margin-bottom:0.4rem;">No Active Assessment</h3>
                <p style="color:#64748B;font-size:0.88rem;max-width:400px;margin:0 auto 1.25rem auto;">
                    Run a New Assessment first to see per-applicant SHAP attribution here.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Go to New Assessment", type="primary"):
                navigate_to("New Assessment")
        else:
            is_appr = pred_res['prediction'] == 1
            base_val = shap_res['base_value']
            contributions = shap_res['contributions']

            # Context strip
            badge_cls = "cw-badge-approved" if is_appr else "cw-badge-rejected"
            accent = "#10B981" if is_appr else "#EF4444"

            st.markdown(f"""
            <div class="cw-card" style="border-left:4px solid {accent};padding:1rem 1.25rem;margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
                    <div>
                        <span class="cw-badge {badge_cls}">{pred_res['status_label']} · {pred_res['approval_percentage']}%</span>
                        <div style="font-size:0.82rem;color:#64748B;margin-top:4px;">
                            {applicant.get('credit_amount',0):,} DM over {applicant.get('duration_months',0)} months
                            &nbsp;·&nbsp; Risk: <strong>{pred_res['risk_tier']}</strong>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;font-weight:700;">Base Value</div>
                        <div style="font-size:1.3rem;font-weight:700;color:#0F172A;font-family:'JetBrains Mono',monospace;">{base_val:.3f}</div>
                        <div style="font-size:0.68rem;color:#94A3B8;">Prior log-odds</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Adverse action notice
            if not is_appr:
                st.markdown("""
                <div style="background:#FEF2F2;border:1px solid #FECACA;border-left:4px solid #EF4444;
                            border-radius:0 8px 8px 0;padding:0.9rem 1.1rem;margin-bottom:1rem;">
                    <div style="font-weight:700;color:#991B1B;font-size:0.85rem;margin-bottom:6px;">
                        Adverse Action Notice
                    </div>
                    <p style="font-size:0.8rem;color:#7F1D1D;line-height:1.5;margin-bottom:0.5rem;">
                        Principal factors that pulled this applicant's score below the approval threshold:
                    </p>
                """, unsafe_allow_html=True)
                for r in shap_res['top_risk'][:3]:
                    st.markdown(f"""
                    <div style="font-size:0.8rem;color:#991B1B;margin-bottom:3px;">
                        • <strong>{r['label']} ({r['value']}):</strong>
                        contributed <strong>−{abs(r['shap_value']):.2f}</strong> to the risk score.
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # SHAP chart
            st.markdown("""
            <div class="cw-card">
                <div class="cw-card-header">
                    <span class="cw-card-title">Feature Attribution — Local SHAP Values</span>
                    <span class="cw-badge cw-badge-neutral">TreeSHAP Engine</span>
                </div>
                <p style="font-size:0.8rem;color:#64748B;margin-bottom:0.75rem;">
                    Green bars push toward approval; red bars push toward rejection.
                    Bar length = magnitude of impact.
                </p>
            """, unsafe_allow_html=True)

            top_n = st.slider("Number of features to display:", 6, 20, 12, 1,
                              key="shap_top_n_analytics")
            subset = list(reversed(contributions[:top_n]))
            y_labels = [f"{i['label']} = {i['value']}" for i in subset]
            x_vals   = [i['shap_value'] for i in subset]
            colors   = ['#10B981' if v > 0 else '#EF4444' for v in x_vals]

            fig_shap = go.Figure()
            fig_shap.add_trace(go.Bar(
                x=x_vals, y=y_labels,
                orientation='h',
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"{v:+.3f}" for v in x_vals],
                textposition='outside',
                textfont=dict(size=10, family='Inter', color='#475569'),
                hovertemplate="<b>%{y}</b><br>SHAP: %{x:.3f}<extra></extra>"
            ))
            fig_shap.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                margin=dict(l=20, r=60, t=10, b=40),
                height=max(380, top_n * 36),
                xaxis=dict(
                    title=dict(text="SHAP Value  ←  Rejection  |  Approval  →", font=dict(size=11, color='#475569', family='Inter')),
                    zeroline=True, zerolinecolor="#334155", zerolinewidth=1.5,
                    gridcolor="#F1F5F9",
                    tickfont=dict(size=11, color='#64748B', family='Inter'),
                ),
                yaxis=dict(
                    autorange=True,
                    tickfont=dict(size=11, color='#0F172A', family='Inter'),
                ),
                bargap=0.3,
            )
            st.plotly_chart(fig_shap, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)

            # Positive vs Risk columns
            pc, rc = st.columns(2)
            with pc:
                st.markdown("""
                <div class="cw-card" style="height:100%;">
                    <div class="cw-card-header">
                        <span class="cw-card-title" style="color:#065F46;">Positive Drivers</span>
                        <span class="cw-badge cw-badge-approved">Approval Boost</span>
                    </div>
                """, unsafe_allow_html=True)
                for item in shap_res['top_positive']:
                    st.markdown(f"""
                    <div class="cw-factor-positive">
                        <div>
                            <div style="font-size:0.8rem;font-weight:600;color:#065F46;">{item['label']}</div>
                            <div style="font-size:0.72rem;color:#047857;">{item['value']}</div>
                        </div>
                        <span style="font-weight:700;color:#065F46;font-size:0.88rem;">+{item['shap_value']:.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with rc:
                st.markdown("""
                <div class="cw-card" style="height:100%;">
                    <div class="cw-card-header">
                        <span class="cw-card-title" style="color:#991B1B;">Risk Factors</span>
                        <span class="cw-badge cw-badge-rejected">Adverse Action</span>
                    </div>
                """, unsafe_allow_html=True)
                for item in shap_res['top_risk']:
                    st.markdown(f"""
                    <div class="cw-factor-negative">
                        <div>
                            <div style="font-size:0.8rem;font-weight:600;color:#991B1B;">{item['label']}</div>
                            <div style="font-size:0.72rem;color:#B91C1C;">{item['value']}</div>
                        </div>
                        <span style="font-weight:700;color:#991B1B;font-size:0.88rem;">{item['shap_value']:.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Interpretation guide
            st.markdown(f"""
            <div class="cw-card" style="background:#F8FAFC;margin-top:1rem;">
                <h3 style="margin-bottom:0.5rem;font-size:0.88rem;">How to Read SHAP Values</h3>
                <div style="font-size:0.8rem;color:#475569;line-height:1.65;">
                    <strong>Base Value ({base_val:.3f}):</strong> Expected log-odds across the full training population before observing this applicant's attributes.<br>
                    <strong>Additivity:</strong> Final score = Base Value + Σ SHAP values. Applying sigmoid gives <strong>{pred_res['approval_percentage']}%</strong> approval probability.<br>
                    <strong>Regulatory:</strong> Top negative SHAP attributes serve as ECOA / GDPR Article 22 adverse action reason codes.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: Confusion Matrix & Report ──
    with tab_matrix:
        cm_col, rep_col = st.columns([1, 1])

        with cm_col:
            st.markdown("""
            <div class="cw-card">
                <div class="cw-card-header">
                    <span class="cw-card-title">Confusion Matrix</span>
                    <span class="cw-badge cw-badge-neutral">Test Set N=200</span>
                </div>
            """, unsafe_allow_html=True)

            tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
            z = [[tp, fn], [fp, tn]]
            x_labels = ['Predicted: Approved', 'Predicted: Rejected']
            y_labels = ['Actual: Approved', 'Actual: Rejected']
            annotations = []
            for yi, row in enumerate(z):
                for xi, val in enumerate(row):
                    annotations.append(dict(
                        x=x_labels[xi], y=y_labels[yi],
                        text=f"<b>{val}</b>",
                        showarrow=False,
                        font=dict(size=18, color='#0F172A', family='Inter'),
                        xref='x', yref='y'
                    ))
            fig_cm = go.Figure(data=go.Heatmap(
                z=z,
                x=x_labels,
                y=y_labels,
                colorscale=[[0, '#F0F4F8'], [0.5, '#6EE7B7'], [1, '#059669']],
                showscale=False,
                hoverongaps=False,
            ))
            fig_cm.update_layout(
                annotations=annotations,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                margin=dict(l=40, r=40, t=30, b=30),
                height=280,
                xaxis=dict(tickfont=dict(size=12, family='Inter', color='#0F172A'), side='bottom'),
                yaxis=dict(tickfont=dict(size=12, family='Inter', color='#0F172A'), autorange='reversed'),
            )
            st.plotly_chart(fig_cm, use_container_width=True, config={'displayModeBar': False})

            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.8rem;
                        color:#475569;padding-top:0.75rem;border-top:1px solid #F1F5F9;">
                <div style="background:#ECFDF5;padding:7px 10px;border-radius:6px;">
                    True Approved (TP): <strong style="color:#065F46;">{tp}</strong>
                </div>
                <div style="background:#FEF2F2;padding:7px 10px;border-radius:6px;">
                    False Approved (FP): <strong style="color:#991B1B;">{fp}</strong>
                </div>
                <div style="background:#FEF2F2;padding:7px 10px;border-radius:6px;">
                    False Rejected (FN): <strong style="color:#991B1B;">{fn}</strong>
                </div>
                <div style="background:#ECFDF5;padding:7px 10px;border-radius:6px;">
                    True Rejected (TN): <strong style="color:#065F46;">{tn}</strong>
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

        with rep_col:
            st.markdown("""
            <div class="cw-card">
                <div class="cw-card-header">
                    <span class="cw-card-title">Classification Report</span>
                    <span class="cw-badge cw-badge-neutral">Scikit-Learn</span>
                </div>
            """, unsafe_allow_html=True)

            report = metrics['report']
            report_data = [
                {"Class": "Approved (Good Risk)",   "Precision": f"{report['1']['precision']*100:.1f}%",
                 "Recall": f"{report['1']['recall']*100:.1f}%",   "F1": f"{report['1']['f1-score']:.3f}", "Support": int(report['1']['support'])},
                {"Class": "Rejected (Bad Risk)",     "Precision": f"{report['0']['precision']*100:.1f}%",
                 "Recall": f"{report['0']['recall']*100:.1f}%",   "F1": f"{report['0']['f1-score']:.3f}", "Support": int(report['0']['support'])},
                {"Class": "Macro Average",           "Precision": f"{report['macro avg']['precision']*100:.1f}%",
                 "Recall": f"{report['macro avg']['recall']*100:.1f}%","F1": f"{report['macro avg']['f1-score']:.3f}", "Support": int(report['macro avg']['support'])},
            ]
            st.dataframe(pd.DataFrame(report_data), hide_index=True, use_container_width=True)

            st.markdown(f"""
            <div style="background:#F8FAFC;border:1px solid #F1F5F9;border-radius:8px;
                        padding:0.9rem 1rem;margin-top:1rem;font-size:0.8rem;color:#475569;line-height:1.6;">
                <strong>Analysis:</strong> The model achieves <strong>{metrics['recall']*100:.1f}%</strong> recall
                on creditworthy applicants with <strong>{metrics['precision']*100:.1f}%</strong> precision —
                minimizing false rejection of prime borrowers while maintaining disciplined risk control.
            </div>
            </div>
            """, unsafe_allow_html=True)
