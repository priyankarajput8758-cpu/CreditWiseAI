"""
Results — CreditWise AI (legacy redirect shim)
The assessment result is now rendered inline on the prediction page.
This module is kept for backward compatibility.
"""

import streamlit as st


def render_results_page(artifacts):
    """Redirects to the prediction page which now shows results inline."""
    st.session_state['current_page'] = "New Assessment"
    st.rerun()
