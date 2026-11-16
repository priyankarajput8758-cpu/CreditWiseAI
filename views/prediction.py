"""
New Assessment — CreditWise AI
Well-structured multi-section loan intake form with preset profiles
and inline result display after submission.
"""

from datetime import datetime
import streamlit as st
from utils.presets import FEATURE_OPTIONS, PRESET_PROFILES
from utils.styling import render_page_header, render_disclaimer, navigate_to
from model.pipeline import predict_applicant, explain_applicant


def _safe_index(opts, val, default=0):
    try:
        return opts.index(val) if val in opts else default
    except Exception:
        return default


def render_prediction_page(artifacts):
    render_page_header("New Assessment", "Submit applicant profile for AI credit risk evaluation")
    render_disclaimer()

    preset_names = list(PRESET_PROFILES.keys())

    # ── Preset Profile Cards ──
    st.markdown("""
    <div class="cw-card" style="padding:1.1rem 1.4rem;margin-bottom:1.25rem;">
        <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;
                    color:#64748B;margin-bottom:0.75rem;">
            Quick Load — Demo Profiles
        </div>
        <div style="font-size:0.8rem;color:#94A3B8;margin-bottom:0.5rem;">
            Select a preset to auto-populate the form below.
        </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    preset_meta = [
        ("Low Risk · Prime",     "#10B981", "Expected: Approved"),
        ("High Risk · Subprime", "#EF4444", "Expected: Rejected"),
        ("Moderate · Borderline","#F59E0B", "Expected: May vary"),
    ]
    for i, (pkey, col) in enumerate(zip(preset_names, [p1, p2, p3])):
        label, color, hint = preset_meta[i]
        with col:
            st.markdown(f"""
            <div style="border:1px solid {color}22;background:{color}08;border-radius:8px;
                        padding:0.6rem 0.9rem;margin-bottom:0.4rem;">
                <div style="font-size:0.78rem;font-weight:700;color:{color};">{label}</div>
                <div style="font-size:0.7rem;color:#94A3B8;margin-top:2px;">{hint}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Load Profile {i+1}", key=f"preset_{i}", use_container_width=True, type="secondary"):
                st.session_state['applicant_data'] = PRESET_PROFILES[pkey].copy()
                st.toast(f"Loaded: {label}")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Ensure valid applicant_data
    if not isinstance(st.session_state.get('applicant_data'), dict):
        st.session_state['applicant_data'] = PRESET_PROFILES[preset_names[0]].copy()
    cur = st.session_state['applicant_data']

    # ── Assessment Form ──
    with st.form("cw_assessment_form", clear_on_submit=False):

        # ─── Section 1: Personal & Demographics ───
        st.markdown("""
        <div class="cw-form-section">
            <span class="cw-form-section-num">1</span>
            Personal & Demographic Details
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age (Years)", min_value=18, max_value=90,
                                  value=int(cur.get('age', 35)), step=1,
                                  help="Applicant age at date of application")
        with c2:
            personal_status = st.selectbox(
                "Personal Status & Gender",
                FEATURE_OPTIONS['personal_status'],
                index=_safe_index(FEATURE_OPTIONS['personal_status'], cur.get('personal_status'))
            )
        with c3:
            housing = st.selectbox(
                "Housing Type",
                FEATURE_OPTIONS['housing'],
                index=_safe_index(FEATURE_OPTIONS['housing'], cur.get('housing'))
            )

        c4, c5, c6 = st.columns(3)
        with c4:
            job = st.selectbox(
                "Employment Classification",
                FEATURE_OPTIONS['job'],
                index=_safe_index(FEATURE_OPTIONS['job'], cur.get('job'), default=1)
            )
        with c5:
            num_dep_raw = cur.get('num_dependents', 1)
            num_dependents = st.selectbox(
                "Number of Dependents",
                [1, 2],
                index=0 if num_dep_raw == 1 else 1
            )
        with c6:
            foreign_worker = st.selectbox(
                "Foreign Worker",
                FEATURE_OPTIONS['foreign_worker'],
                index=_safe_index(FEATURE_OPTIONS['foreign_worker'], cur.get('foreign_worker', 'Yes'))
            )

        # ─── Section 2: Loan Requirements & Finances ───
        st.markdown("""
        <div class="cw-form-section">
            <span class="cw-form-section-num">2</span>
            Loan Requirements & Financial Position
        </div>
        """, unsafe_allow_html=True)

        f1, f2, f3 = st.columns(3)
        with f1:
            credit_amount = st.number_input(
                "Credit Amount (DM)", min_value=250, max_value=20000,
                value=int(cur.get('credit_amount', 3000)), step=100,
                help="Loan principal requested"
            )
        with f2:
            duration_months = st.number_input(
                "Loan Duration (Months)", min_value=4, max_value=72,
                value=int(cur.get('duration_months', 24)), step=1
            )
        with f3:
            installment_rate = st.select_slider(
                "Installment Rate (% of Income)",
                options=[1, 2, 3, 4],
                value=int(cur.get('installment_rate', 2))
            )

        f4, f5, f6 = st.columns(3)
        with f4:
            savings_status = st.selectbox(
                "Savings Account Balance",
                FEATURE_OPTIONS['savings_status'],
                index=_safe_index(FEATURE_OPTIONS['savings_status'], cur.get('savings_status'))
            )
        with f5:
            employment = st.selectbox(
                "Employment Tenure",
                FEATURE_OPTIONS['employment'],
                index=_safe_index(FEATURE_OPTIONS['employment'], cur.get('employment'))
            )
        with f6:
            other_installment_plans = st.selectbox(
                "Other Installment Plans",
                FEATURE_OPTIONS['other_installment_plans'],
                index=_safe_index(FEATURE_OPTIONS['other_installment_plans'],
                                  cur.get('other_installment_plans', 'None'))
            )

        # ─── Section 3: Credit History & Collateral ───
        st.markdown("""
        <div class="cw-form-section">
            <span class="cw-form-section-num">3</span>
            Credit History & Collateral
        </div>
        """, unsafe_allow_html=True)

        h1, h2, h3 = st.columns(3)
        with h1:
            checking_status = st.selectbox(
                "Checking Account Status",
                FEATURE_OPTIONS['checking_status'],
                index=_safe_index(FEATURE_OPTIONS['checking_status'], cur.get('checking_status'))
            )
        with h2:
            credit_history = st.selectbox(
                "Credit History Record",
                FEATURE_OPTIONS['credit_history'],
                index=_safe_index(FEATURE_OPTIONS['credit_history'], cur.get('credit_history'))
            )
        with h3:
            purpose = st.selectbox(
                "Loan Purpose",
                FEATURE_OPTIONS['purpose'],
                index=_safe_index(FEATURE_OPTIONS['purpose'], cur.get('purpose'))
            )

        h4, h5, h6 = st.columns(3)
        with h4:
            property_type = st.selectbox(
                "Property / Collateral",
                FEATURE_OPTIONS['property'],
                index=_safe_index(FEATURE_OPTIONS['property'], cur.get('property'))
            )
        with h5:
            other_debtors = st.selectbox(
                "Co-Applicants / Guarantors",
                FEATURE_OPTIONS['other_debtors'],
                index=_safe_index(FEATURE_OPTIONS['other_debtors'], cur.get('other_debtors', 'None'))
            )
        with h6:
            existing_credits = st.number_input(
                "Existing Bank Credits", min_value=1, max_value=4,
                value=int(cur.get('existing_credits', 1)), step=1
            )

        h7, h8, _ = st.columns(3)
        with h7:
            residence_since = st.select_slider(
                "Years at Present Residence",
                options=[1, 2, 3, 4],
                value=int(cur.get('residence_since', 2))
            )
        with h8:
            telephone = st.selectbox(
                "Telephone Registered",
                FEATURE_OPTIONS['telephone'],
                index=_safe_index(FEATURE_OPTIONS['telephone'],
                                  cur.get('telephone', 'Yes (registered in name)'))
            )

        st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

        # ─── Submit Button ───
        submit = st.form_submit_button(
            "Run AI Credit Assessment",
            use_container_width=True
        )

        if submit:
            submission = {
                'age': age,
                'personal_status': personal_status,
                'housing': housing,
                'job': job,
                'num_dependents': num_dependents,
                'foreign_worker': foreign_worker,
                'credit_amount': credit_amount,
                'duration_months': duration_months,
                'savings_status': savings_status,
                'employment': employment,
                'installment_rate': installment_rate,
                'other_installment_plans': other_installment_plans,
                'checking_status': checking_status,
                'credit_history': credit_history,
                'purpose': purpose,
                'property': property_type,
                'other_debtors': other_debtors,
                'existing_credits': existing_credits,
                'residence_since': residence_since,
                'telephone': telephone,
            }
            st.session_state['applicant_data'] = submission

            with st.spinner("Running XGBoost model & computing SHAP attributions…"):
                pred = predict_applicant(artifacts, submission)
                shap = explain_applicant(artifacts, submission)
                st.session_state['prediction_result'] = pred
                st.session_state['shap_result'] = shap

                # Log to history
                if 'assessment_history' not in st.session_state:
                    st.session_state['assessment_history'] = []
                case_id = f"APP-{len(st.session_state['assessment_history']) + 101:03d}"
                ts = datetime.now().strftime("%H:%M:%S")
                st.session_state['assessment_history'].insert(0, {
                    "Case ID": case_id,
                    "Time": ts,
                    "Principal": f"{credit_amount:,} DM",
                    "Duration": f"{duration_months} mo",
                    "Recommendation": pred['status_label'],
                    "Probability": f"{pred['approval_percentage']}%",
                    "Risk Tier": pred['risk_tier'],
                })
            st.rerun()

    # ── Inline Result Display ──
    pr = st.session_state.get('prediction_result')
    if pr is not None:
        shap_r = st.session_state.get('shap_result')
        is_appr = pr['prediction'] == 1

        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

        # Decision banner
        banner_cls = "cw-decision-approved" if is_appr else "cw-decision-rejected"
        badge_cls  = "cw-badge-approved" if is_appr else "cw-badge-rejected"
        badge_lbl  = "Likely Approved" if is_appr else "Likely Rejected"
        h_color    = "#065F46" if is_appr else "#991B1B"
        prob_color = "#10B981" if is_appr else "#EF4444"

        st.markdown(f"""
        <div class="{banner_cls}">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
                <div>
                    <span class="cw-badge {badge_cls}" style="margin-bottom:0.5rem;display:inline-flex;">
                        {badge_lbl}
                    </span>
                    <h1 style="color:{h_color}!important;font-size:2rem!important;margin:0.3rem 0 0.2rem 0;">
                        {pr['status_label']}
                    </h1>
                    <div style="font-size:0.85rem;color:{h_color}opacity(.7);">
                        Risk Tier: <strong>{pr['risk_tier']}</strong>
                    </div>
                </div>
                <div style="text-align:center;min-width:120px;">
                    <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.07em;
                                color:{h_color};font-weight:700;margin-bottom:4px;">
                        Approval Probability
                    </div>
                    <div style="font-size:2.8rem;font-weight:800;color:{h_color};
                                letter-spacing:-0.04em;line-height:1;">
                        {pr['approval_percentage']}%
                    </div>
                </div>
            </div>
            <div class="cw-prob-bar-wrap" style="margin-top:1rem;">
                <div class="cw-prob-bar-labels">
                    <span>Approval likelihood</span>
                    <span>{pr['approval_percentage']}%</span>
                </div>
                <div class="cw-prob-bar-track">
                    <div class="cw-prob-bar-fill"
                         style="width:{pr['approval_percentage']}%;background:{prob_color};"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Key factors + action
        r1, r2 = st.columns([3, 2])

        with r1:
            factor_title = "Top Positive Factors" if is_appr else "Principal Risk Factors"
            factor_items = (shap_r['top_positive'][:4] if is_appr else shap_r['top_risk'][:4]) if shap_r else []

            st.markdown(f"""
            <div class="cw-card" style="margin-bottom:0;">
                <div class="cw-card-header">
                    <span class="cw-card-title">{factor_title}</span>
                    <span class="cw-badge cw-badge-neutral">Local SHAP</span>
                </div>
            """, unsafe_allow_html=True)

            for item in factor_items:
                cls = "cw-factor-positive" if item['shap_value'] > 0 else "cw-factor-negative"
                sign = "+" if item['shap_value'] > 0 else ""
                fc = "#065F46" if item['shap_value'] > 0 else "#991B1B"
                st.markdown(f"""
                <div class="{cls}">
                    <div>
                        <div style="font-size:0.82rem;font-weight:600;color:#0F172A;">{item['label']}</div>
                        <div style="font-size:0.73rem;color:#64748B;margin-top:1px;">{item['value']}</div>
                    </div>
                    <div style="font-size:0.88rem;font-weight:700;color:{fc};white-space:nowrap;">
                        {sign}{item['shap_value']:.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with r2:
            st.markdown("""
            <div class="cw-card" style="margin-bottom:0;">
                <div class="cw-card-header">
                    <span class="cw-card-title">Next Steps</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <p style="font-size:0.82rem;color:#64748B;margin-bottom:1rem;">
                Dive deeper into the AI explanation or start a new application.
            </p>
            """, unsafe_allow_html=True)

            if st.button("View Full SHAP Explanation →", type="primary", use_container_width=True):
                navigate_to("Explainability")

            st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

            if st.button("View Assessment History", type="secondary", use_container_width=True):
                navigate_to("Assessment History")

            st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

            if st.button("Back to Overview", type="secondary", use_container_width=True):
                navigate_to("Overview")

            st.markdown("</div>", unsafe_allow_html=True)
