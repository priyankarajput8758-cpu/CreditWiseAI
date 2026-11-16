"""
Overview Dashboard — CreditWise AI
Premium fintech dashboard with session KPIs, risk distribution chart,
recent activity chart, and assessment history snapshot.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styling import render_page_header, render_disclaimer, kpi_card, navigate_to


def render_home_page(artifacts):
    render_page_header("Overview", "Credit risk assessment dashboard")
    render_disclaimer()

    history = st.session_state.get('assessment_history', [])
    metrics = artifacts['metrics']

    # ── Compute live session KPIs ──
    total = len(history)
    approved = sum(1 for h in history if 'Approved' in h.get('Recommendation', ''))
    rejected = total - approved
    approval_rate = round((approved / total * 100), 1) if total > 0 else 0

    # ── Page title row ──
    col_title, col_cta = st.columns([4, 1])
    with col_title:
        st.markdown("""
        <div style="margin-bottom:1rem;">
            <h1 style="margin-bottom:0;">Welcome back</h1>
            <p style="color:#64748B;font-size:0.9rem;margin-top:4px;">
                Here's your credit assessment overview for this session.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_cta:
        st.markdown("<div style='padding-top:0.6rem;'>", unsafe_allow_html=True)
        if st.button("+ New Assessment", type="primary", use_container_width=True):
            navigate_to("New Assessment")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── KPI Row ──
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(kpi_card(
            "Total Applications",
            str(total) if total > 0 else "—",
            subtext="This session",
            accent="#0A1628"
        ), unsafe_allow_html=True)

    with k2:
        st.markdown(kpi_card(
            "Approved",
            str(approved) if total > 0 else "—",
            subtext="Good credit risk",
            accent="#10B981"
        ), unsafe_allow_html=True)

    with k3:
        st.markdown(kpi_card(
            "Rejected",
            str(rejected) if total > 0 else "—",
            subtext="Elevated risk",
            accent="#EF4444"
        ), unsafe_allow_html=True)

    with k4:
        st.markdown(kpi_card(
            "Approval Rate",
            f"{approval_rate}%" if total > 0 else "—",
            subtext="Session average",
            accent="#8B5CF6"
        ), unsafe_allow_html=True)

    st.markdown("<div style='height:1.25rem;'></div>", unsafe_allow_html=True)

    # ── Charts Row ──
    chart_left, chart_right = st.columns([1, 1])

    with chart_left:
        st.markdown("""
        <div class="cw-card" style="margin-bottom:0;">
            <div class="cw-card-header">
                <span class="cw-card-title">Credit Risk Distribution</span>
                <span class="cw-badge cw-badge-neutral">Training Dataset</span>
            </div>
            <p style="font-size:0.8rem;color:#64748B;margin-bottom:0.75rem;">
                Class balance in the 1,000-record German Credit benchmark.
            </p>
        """, unsafe_allow_html=True)

        fig_donut = go.Figure(data=[go.Pie(
            labels=['Good Risk (Approved)', 'Bad Risk (Rejected)'],
            values=[700, 300],
            hole=0.65,
            marker=dict(
                colors=['#10B981', '#EF4444'],
                line=dict(color='#FFFFFF', width=3)
            ),
            textinfo='percent',
            hoverinfo='label+value+percent',
            textfont=dict(size=13, family='Inter'),
        )])

        fig_donut.add_annotation(
            text="<b>70%</b><br><span style='font-size:11px;'>Approved</span>",
            x=0.5, y=0.5,
            font=dict(size=14, color='#0F172A', family='Inter'),
            showarrow=False,
            align='center'
        )

        fig_donut.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10),
            height=230,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom", y=-0.18,
                xanchor="center", x=0.5,
                font=dict(size=11, family='Inter', color='#475569')
            )
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_right:
        st.markdown("""
        <div class="cw-card" style="margin-bottom:0;">
            <div class="cw-card-header">
                <span class="cw-card-title">Session Assessment Activity</span>
                <span class="cw-badge cw-badge-neutral">Live Session</span>
            </div>
            <p style="font-size:0.8rem;color:#64748B;margin-bottom:0.75rem;">
                Approval probability scores from your session assessments.
            </p>
        """, unsafe_allow_html=True)

        if history:
            probs = [float(h['Probability'].replace('%', '')) for h in history]
            labels = [h['Case ID'] for h in history]
            colors_bar = ['#10B981' if p >= 50 else '#EF4444' for p in probs]

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=labels[::-1],
                y=probs[::-1],
                marker=dict(color=colors_bar[::-1], line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>Approval Prob: %{y:.1f}%<extra></extra>",
            ))
            fig_bar.add_hline(y=50, line_dash="dot", line_color="#94A3B8", line_width=1.5)
            fig_bar.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                margin=dict(l=10, r=10, t=10, b=40),
                height=230,
                xaxis=dict(tickfont=dict(size=11, family='Inter', color='#64748B'), tickangle=-30),
                yaxis=dict(
                    title=dict(text="Approval Probability (%)", font=dict(size=11, color='#64748B')),
                    range=[0, 105],
                    gridcolor="#F1F5F9",
                    tickfont=dict(size=11, family='Inter', color='#64748B'),
                ),
                bargap=0.35,
                showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("""
            <div class="cw-empty-state" style="padding:2.5rem 1rem;">
                <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#94A3B8;margin-bottom:0.4rem;">Activity Chart</div>
                <p style="font-size:0.85rem;color:#64748B;margin:0;">
                    Run your first assessment to see score trends here.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1.25rem;'></div>", unsafe_allow_html=True)

    # ── Recent Assessments ──
    st.markdown("""
    <div class="cw-card">
        <div class="cw-card-header">
            <span class="cw-card-title">Recent Assessments</span>
        </div>
    """, unsafe_allow_html=True)

    if history:
        df = pd.DataFrame(history[:5])
        st.dataframe(df, hide_index=True, use_container_width=True)
        if len(history) > 5:
            if st.button("View Full History →", type="secondary"):
                navigate_to("Assessment History")
    else:
        st.markdown("""
        <div class="cw-empty-state" style="padding:2.5rem 1rem;">
            <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#94A3B8;margin-bottom:0.4rem;">Audit Ledger</div>
            <p style="font-size:0.88rem;color:#64748B;margin-bottom:0.75rem;">
                No assessments in this session yet.
            </p>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("Start First Assessment", type="primary", use_container_width=True):
                navigate_to("New Assessment")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Model Health Strip ──
    m = metrics
    st.markdown(f"""
    <div class="cw-card" style="margin-bottom:0;">
        <div class="cw-card-header">
            <span class="cw-card-title">Model Health · XGBoost Classifier</span>
            <span class="cw-badge cw-badge-approved">Production Ready</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;">
            <div style="text-align:center;padding:0.75rem;background:#F8FAFC;border-radius:8px;border:1px solid #F1F5F9;">
                <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;font-weight:700;margin-bottom:4px;">Test Accuracy</div>
                <div style="font-size:1.5rem;font-weight:800;color:#0F172A;letter-spacing:-0.02em;">{m['accuracy']*100:.1f}%</div>
            </div>
            <div style="text-align:center;padding:0.75rem;background:#F8FAFC;border-radius:8px;border:1px solid #F1F5F9;">
                <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;font-weight:700;margin-bottom:4px;">F1 Score</div>
                <div style="font-size:1.5rem;font-weight:800;color:#0F172A;letter-spacing:-0.02em;">{m['f1_score']:.3f}</div>
            </div>
            <div style="text-align:center;padding:0.75rem;background:#F8FAFC;border-radius:8px;border:1px solid #F1F5F9;">
                <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;font-weight:700;margin-bottom:4px;">Precision</div>
                <div style="font-size:1.5rem;font-weight:800;color:#0F172A;letter-spacing:-0.02em;">{m['precision']*100:.1f}%</div>
            </div>
            <div style="text-align:center;padding:0.75rem;background:#F8FAFC;border-radius:8px;border:1px solid #F1F5F9;">
                <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;color:#64748B;font-weight:700;margin-bottom:4px;">Recall</div>
                <div style="font-size:1.5rem;font-weight:800;color:#0F172A;letter-spacing:-0.02em;">{m['recall']*100:.1f}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
