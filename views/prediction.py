"""
Page 2: Loan Assessment View
Professional loan underwriting intake form organized into logical sections with clean controls,
preset profile selectors, and a dedicated post-submission result section.
"""

from datetime import datetime
import streamlit as st
import pandas as pd
from utils.presets import FEATURE_OPTIONS, PRESET_PROFILES
from utils.styling import render_top_navigation, render_academic_disclaimer
from model.pipeline import predict_applicant, explain_applicant

def safe_index(options_list, target_val, default=0):
    """Safely retrieves the index of a value in options_list without raising ValueError."""
    try:
        if target_val in options_list:
            return options_list.index(target_val)
        return default
    except (ValueError, KeyError, TypeError):
        return default

def render_prediction_page(artifacts):
    """Renders the Loan Assessment form and post-submission results."""
    render_top_navigation("Loan Assessment")
    render_academic_disclaimer()

    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 style="margin-bottom: 0.2rem;">Loan Applicant Assessment</h1>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 0;">
            Submit applicant demographic, financial, and credit history attributes to generate an AI credit decision.
        </p>
    </div>
    """, unsafe_allow_html=True)

    preset_names = list(PRESET_PROFILES.keys())

    # Demo Presets Segmented Selector
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.85rem 1.1rem; margin-bottom: 1.5rem;">
        <span style="font-size: 0.8rem; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">
            Benchmark Presets (Click to Auto-Fill):
        </span>
    </div>
    """, unsafe_allow_html=True)

    p_col1, p_col2, p_col3 = st.columns(3)
    preset_short_names = [
        "Prime Profile (Low Risk)",
        "Subprime Profile (High Risk)",
        "Borderline Profile (Moderate)"
    ]

    for i, p_key in enumerate(preset_names):
        col = p_col1 if i == 0 else (p_col2 if i == 1 else p_col3)
        with col:
            if st.button(preset_short_names[i], key=f"btn_preset_{i}", use_container_width=True, type="secondary"):
                st.session_state['applicant_data'] = PRESET_PROFILES[p_key].copy()
                st.toast(f"Loaded: {preset_short_names[i]}")
                st.rerun()

    # Ensure applicant_data is always a valid dictionary
    if st.session_state.get('applicant_data') is None or not isinstance(st.session_state.get('applicant_data'), dict):
        st.session_state['applicant_data'] = PRESET_PROFILES[preset_names[0]].copy()

    current_data = st.session_state['applicant_data']

    # Two-Column Structured Form
    with st.form("loan_underwriting_form"):
        # Section 1: Personal & Demographic
        st.markdown("""
        <div style="font-size: 0.95rem; font-weight: 600; color: #0F172A; padding-bottom: 0.4rem; border-bottom: 1px solid #E2E8F0; margin-bottom: 1rem;">
            1. Personal & Demographic Details
        </div>
        """, unsafe_allow_html=True)

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            age = st.number_input(
                "Age of Applicant (Years)",
                min_value=18,
                max_value=90,
                value=int(current_data.get('age', 35)),
                step=1,
                help="Applicant age at date of application"
            )
            personal_status = st.selectbox(
                "Personal Status & Gender",
                options=FEATURE_OPTIONS['personal_status'],
                index=safe_index(FEATURE_OPTIONS['personal_status'], current_data.get('personal_status', FEATURE_OPTIONS['personal_status'][0]))
            )
            housing = st.selectbox(
                "Housing Accommodation",
                options=FEATURE_OPTIONS['housing'],
                index=safe_index(FEATURE_OPTIONS['housing'], current_data.get('housing', FEATURE_OPTIONS['housing'][0]))
            )

        with col_p2:
            job = st.selectbox(
                "Employment Classification",
                options=FEATURE_OPTIONS['job'],
                index=safe_index(FEATURE_OPTIONS['job'], current_data.get('job', FEATURE_OPTIONS['job'][1]), default=1)
            )
            num_dep_raw = current_data.get('num_dependents', 1)
            num_dependents = st.selectbox(
                "Number of Dependents Liable for Maintenance",
                options=[1, 2],
                index=0 if num_dep_raw == 1 else 1
            )
            foreign_worker = st.selectbox(
                "Foreign Worker Status",
                options=FEATURE_OPTIONS['foreign_worker'],
                index=safe_index(FEATURE_OPTIONS['foreign_worker'], current_data.get('foreign_worker', 'Yes'))
            )

        # Section 2: Financial Standing & Requirements
        st.markdown("""
        <div style="font-size: 0.95rem; font-weight: 600; color: #0F172A; padding-bottom: 0.4rem; border-bottom: 1px solid #E2E8F0; margin-top: 1.25rem; margin-bottom: 1rem;">
            2. Loan Requirements & Liquidity Position
        </div>
        """, unsafe_allow_html=True)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            credit_amount = st.number_input(
                "Requested Credit Amount (DM)",
                min_value=250,
                max_value=20000,
                value=int(current_data.get('credit_amount', 3000)),
                step=100,
                help="Loan principal requested in Deutsche Mark"
            )
            duration_months = st.number_input(
                "Loan Duration (Months)",
                min_value=4,
                max_value=72,
                value=int(current_data.get('duration_months', 24)),
                step=1
            )
            savings_status = st.selectbox(
                "Total Savings & Bond Balance",
                options=FEATURE_OPTIONS['savings_status'],
                index=safe_index(FEATURE_OPTIONS['savings_status'], current_data.get('savings_status', FEATURE_OPTIONS['savings_status'][0]))
            )

        with col_f2:
            employment = st.selectbox(
                "Current Employment Tenure",
                options=FEATURE_OPTIONS['employment'],
                index=safe_index(FEATURE_OPTIONS['employment'], current_data.get('employment', FEATURE_OPTIONS['employment'][0]))
            )
            installment_rate = st.slider(
                "Installment Rate (% of Disposable Income)",
                min_value=1,
                max_value=4,
                value=int(current_data.get('installment_rate', 2))
            )
            other_installment_plans = st.selectbox(
                "Existing Installment Contracts",
                options=FEATURE_OPTIONS['other_installment_plans'],
                index=safe_index(FEATURE_OPTIONS['other_installment_plans'], current_data.get('other_installment_plans', 'None'))
            )

        # Section 3: Credit History & Collateral
        st.markdown("""
        <div style="font-size: 0.95rem; font-weight: 600; color: #0F172A; padding-bottom: 0.4rem; border-bottom: 1px solid #E2E8F0; margin-top: 1.25rem; margin-bottom: 1rem;">
            3. Credit History & Banking Records
        </div>
        """, unsafe_allow_html=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            checking_status = st.selectbox(
                "Checking Account Status",
                options=FEATURE_OPTIONS['checking_status'],
                index=safe_index(FEATURE_OPTIONS['checking_status'], current_data.get('checking_status', FEATURE_OPTIONS['checking_status'][0]))
            )
            credit_history = st.selectbox(
                "Historical Credit Repayment Record",
                options=FEATURE_OPTIONS['credit_history'],
                index=safe_index(FEATURE_OPTIONS['credit_history'], current_data.get('credit_history', FEATURE_OPTIONS['credit_history'][0]))
            )
            purpose = st.selectbox(
                "Declared Loan Purpose",
                options=FEATURE_OPTIONS['purpose'],
                index=safe_index(FEATURE_OPTIONS['purpose'], current_data.get('purpose', FEATURE_OPTIONS['purpose'][0]))
            )
            property_type = st.selectbox(
                "Collateral / Property Ownership",
                options=FEATURE_OPTIONS['property'],
                index=safe_index(FEATURE_OPTIONS['property'], current_data.get('property', FEATURE_OPTIONS['property'][0]))
            )

        with col_c2:
            other_debtors = st.selectbox(
                "Co-Applicants / Guarantors",
                options=FEATURE_OPTIONS['other_debtors'],
                index=safe_index(FEATURE_OPTIONS['other_debtors'], current_data.get('other_debtors', 'None'))
            )
            existing_credits = st.number_input(
                "Existing Credits at This Bank",
                min_value=1,
                max_value=4,
                value=int(current_data.get('existing_credits', 1)),
                step=1
            )
            residence_since = st.slider(
                "Years at Present Residence",
                min_value=1,
                max_value=4,
                value=int(current_data.get('residence_since', 3))
            )
            telephone = st.selectbox(
                "Telephone Landline Registration",
                options=FEATURE_OPTIONS['telephone'],
                index=safe_index(FEATURE_OPTIONS['telephone'], current_data.get('telephone', 'Yes (registered in name)'))
            )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Primary Action Button
        submit_btn = st.form_submit_button("Analyse Application", use_container_width=True)

        if submit_btn:
            applicant_submission = {
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
                'telephone': telephone
            }

            st.session_state['applicant_data'] = applicant_submission

            with st.spinner("Processing application through XGBoost model & computing SHAP attributions..."):
                pred_result = predict_applicant(artifacts, applicant_submission)
                shap_result = explain_applicant(artifacts, applicant_submission)

                st.session_state['prediction_result'] = pred_result
                st.session_state['shap_result'] = shap_result

                # Add to recent session assessment history
                if 'assessment_history' not in st.session_state:
                    st.session_state['assessment_history'] = []

                case_id = f"APP-{len(st.session_state['assessment_history']) + 101}"
                timestamp_str = datetime.now().strftime("%H:%M:%S")

                st.session_state['assessment_history'].insert(0, {
                    "Case ID": case_id,
                    "Timestamp": timestamp_str,
                    "Principal": f"{credit_amount:,} DM",
                    "Tenure": f"{duration_months} mo",
                    "Recommendation": pred_result['status_label'],
                    "Probability": f"{pred_result['approval_percentage']}%",
                    "Risk Tier": pred_result['risk_tier']
                })
                st.rerun()

    # DEDICATED IN-PLACE RESULT SECTION (Displayed after assessment)
    if st.session_state.get('prediction_result') is not None:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        res = st.session_state['prediction_result']
        shap_res = st.session_state.get('shap_result')
        is_approved = (res['prediction'] == 1)

        st.markdown("""
        <div class="saas-card" style="border-top: 3px solid {};">
            <div class="saas-card-header">
                <h3 class="saas-card-title">Assessment Decision Outcome</h3>
                <span class="{}">{}</span>
            </div>
        """.format(
            "#10B981" if is_approved else "#EF4444",
            "badge-approved" if is_approved else "badge-rejected",
            "Likely Approved" if is_approved else "Likely Rejected"
        ), unsafe_allow_html=True)

        res_col1, res_col2 = st.columns([1, 1])

        with res_col1:
            st.markdown(f"""
            <div style="padding: 0.5rem 0;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748B; font-weight: 600;">Calibrated Recommendation</div>
                <div style="font-size: 2rem; font-weight: 700; color: {'#065F46' if is_approved else '#991B1B'}; margin: 0.2rem 0;">
                    {res['status_label']}
                </div>
                <div style="font-size: 0.85rem; color: #475569;">
                    Assigned Risk Tier: <strong>{res['risk_tier']}</strong>
                </div>
                <div style="margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
                        <span>Approval Probability</span>
                        <strong>{res['approval_percentage']}%</strong>
                    </div>
                    <div style="width: 100%; height: 8px; background: #E2E8F0; border-radius: 4px; overflow: hidden;">
                        <div style="width: {res['approval_percentage']}%; height: 100%; background: {'#10B981' if is_approved else '#EF4444'};"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with res_col2:
            if not is_approved:
                st.markdown("""
                <div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; padding: 12px 14px;">
                    <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: #991B1B; margin-bottom: 8px;">
                        Principal Reasons for Rejection (Adverse Action Factors)
                    </div>
                """, unsafe_allow_html=True)
                if shap_res and shap_res['top_risk']:
                    for r_item in shap_res['top_risk'][:3]:
                        st.markdown(f"""
                        <div style="font-size: 0.82rem; margin-bottom: 6px; color: #991B1B; line-height: 1.4;">
                            • <strong>{r_item['label']}:</strong> {r_item['value']} 
                            <span style="font-weight: 600; color: #B91C1C;">(Pulling score down by {r_item['shap_value']:.2f})</span>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("""
                    <div style="margin-top: 10px;">
                """, unsafe_allow_html=True)
                if st.button("Inspect Full SHAP Explanation Chart →", type="primary", use_container_width=True):
                    st.session_state['current_page'] = "Explainability"
                    st.rerun()
                st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px; padding: 12px 14px;">
                    <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: #065F46; margin-bottom: 8px;">
                        Top Positive Factors Driving Approval
                    </div>
                """, unsafe_allow_html=True)
                if shap_res and shap_res['top_positive']:
                    for p_item in shap_res['top_positive'][:3]:
                        st.markdown(f"""
                        <div style="font-size: 0.82rem; margin-bottom: 6px; color: #065F46; line-height: 1.4;">
                            • <strong>{p_item['label']}:</strong> {p_item['value']} 
                            <span style="font-weight: 600; color: #047857;">(+{p_item['shap_value']:.2f} boost)</span>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("""
                    <div style="margin-top: 10px;">
                """, unsafe_allow_html=True)
                if st.button("Deep Dive into SHAP Explainability →", type="primary", use_container_width=True):
                    st.session_state['current_page'] = "Explainability"
                    st.rerun()
                st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
