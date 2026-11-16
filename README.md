# CreditWise AI – Transparent Credit Assessment & Decisioning

> **Institutional Fintech Platform & Academic Mini-Project**  
> **Topic:** Explainable AI (XAI) in Automated Credit Risk Underwriting  
> **Tech Stack:** Python, Streamlit, XGBoost, TreeSHAP, Scikit-learn, Pandas, Plotly

---

## Executive Summary

Algorithmic credit decision systems powered by gradient-boosted trees (such as **XGBoost**) offer high predictive accuracy when assessing loan applicant default risk. However, they traditionally function as **"black-box"** systems. This opacity poses critical hurdles under contemporary regulatory frameworks (such as the **EU AI Act**, **GDPR Article 22**, and the U.S. **Equal Credit Opportunity Act / ECOA Adverse Action Notices**), which mandate that individuals receive transparent, mathematically grounded reasons for credit denials.

**CreditWise AI** demonstrates how **SHAP (SHapley Additive exPlanations)** decomposes complex XGBoost ensemble predictions into exact, additive feature-level attributions based on cooperative game theory.

> **Academic Demonstration Disclaimer:**  
> This project uses the historical **Statlog German Credit dataset** from the UCI Machine Learning Repository. In this prototype, historical **credit-risk classifications** (*Good Risk* vs. *Bad Risk*) are mapped to **Likely Approved** and **Likely Rejected** categories solely for educational demonstration purposes. It does not represent live lending decisions of any commercial bank.

---

## Key Features

- **Institutional SaaS Fintech Interface:** Inter typography, persistent deep forest navy sidebar (`#091E16`), warm off-white canvas (`#F8FAFC`), crisp 1px borders, Lucide vector SVG icons, and zero emojis.
- **Trained Machine Learning Model:** Real **XGBoost Classifier** (100 trees, regularized tree depth, log-loss optimization) trained on an 80% split with an independent 20% holdout test set (75.5% test accuracy, confusion matrix, precision/recall metrics).
- **No Dummy / Hardcoded Predictions:** All predictions, probabilities, and SHAP values are calculated in real time using the trained model and `shap.TreeExplainer`.
- **Game-Theoretic SHAP Attributions:**
  - Interactive horizontal contribution bar chart with color-coded drivers (**Emerald Green** for positive factors boosting approval, **Muted Coral/Red** for elevated risk factors).
  - Clear separation of Positive Approval Drivers vs. Primary Adverse Risk Factors.
  - Population Base Value (prior expected log-odds) and feature additivity explanation.
  - Global Feature Importance ranking across the entire test population.
- **5 Dedicated Modules:**
  1. `Overview`: Real-time KPIs, benchmark distribution donut chart, end-to-end pipeline tracker, and session audit history ledger.
  2. `Loan Assessment`: Two-column underwriting intake form with preset selectors and in-place post-submission decision card.
  3. `Explainability`: Dedicated SHAP local decision attribution audit.
  4. `Model Analytics`: Confusion matrix heatmap, Scikit-Learn classification breakdown, and global feature importance.
  5. `About Project`: Regulatory mandates, theoretical foundation (Why XGBoost & Why SHAP), and structured future research roadmap.
- **Preset Demonstration Profiles:** Includes one-click demo presets (**Prime Profile / Low-Risk**, **Subprime / High-Risk**, and **Borderline Profile**) for seamless demonstration.
- **Persistent Session State:** Inputs, active predictions, and SHAP explanations remain preserved across all navigation pages.

---

## Project Architecture & File Structure

```
MiniProject/
├── .streamlit/
│   └── config.toml          # Custom theme configuration (cream & forest green)
├── data/
│   └── german_credit.csv    # Preprocessed German Credit benchmark with human-readable labels
├── model/
│   ├── __init__.py
│   └── pipeline.py          # Data ingestion, XGBoost training, caching, inference & SHAP
├── utils/
│   ├── __init__.py
│   ├── icons.py             # Vector Lucide-style SVG icon components (no emojis)
│   ├── styling.py           # Fintech CSS design system, top app bar, and card components
│   └── presets.py           # Quick-load applicant profiles for live demonstration
├── views/
│   ├── __init__.py
│   ├── home.py              # Page 1: Overview Dashboard, KPIs, Distribution & Ledger
│   ├── prediction.py        # Page 2: Loan Assessment Form with in-place decision outcome
│   ├── explanation.py       # Page 3: SHAP Local Attribution Audit & Interpretation Guide
│   ├── analytics.py         # Page 4: Model Analytics, Confusion Matrix & Global Importance
│   └── about.py             # Page 5: Academic Documentation, Regulatory Scope & Roadmap
├── app.py                   # Main Application Entrypoint & Persistent Left Navigation Router
├── requirements.txt         # Python package dependencies
└── README.md                # Comprehensive documentation & presentation guide
```

---

## 📊 Dataset: UCI Statlog German Credit Data

The model is trained on the benchmark **German Credit dataset** (1,000 applicants, 20 features) obtained from the **UCI Machine Learning Repository**:

### Feature Breakdown
1. **Liquidity & Cash Position:** Checking account status, liquid savings/bond status.
2. **Loan Requirements:** Duration (months), credit amount (DM), installment rate (% of disposable income), loan purpose.
3. **Credit History:** Historical repayment track record, existing loans at this bank, other installment plans (stores/banks).
4. **Demographic & Collateral Profile:** Age, personal status & sex, employment tenure, housing (own/rent/free), property collateral, guarantor/co-applicant presence, telephone, foreign worker status.

### Target Mapping
- **Good Credit Risk (Original Class 1):** Mapped to **Likely Approved (Class 1)**.
- **Bad Credit Risk (Original Class 2):** Mapped to **Likely Rejected (Class 0)**.

---

## 🛠️ Installation & Setup Instructions

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.14
- Recommended: Virtual environment (`venv` or `conda`)

### Step 1: Open Terminal in the Project Directory
```powershell
cd "c:\Users\Priyanka rajput\OneDrive\Desktop\MiniProject"
```

### Step 2: (Optional but Recommended) Activate Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Launch the Streamlit Dashboard
```powershell
streamlit run app.py
```
The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 🎓 Faculty Demonstration Walkthrough Guide

When presenting this mini-project to your college evaluators, follow this recommended 5-step flow:

1. **Page 1 (Home / Overview):**
   - Highlight the **Problem Statement**: Standard banking models are opaque black boxes.
   - Show the **4-step Visual Workflow**: Applicant Data ➔ XGBoost ➔ TreeSHAP ➔ Transparent Decision.
   - Click **"Start Applicant Assessment Now"**.

2. **Page 2 (Applicant Prediction):**
   - Point out the clean 3-section categorization: *Personal Information*, *Financial Position*, and *Credit History*.
   - Click the **"🟢 Prime Profile"** preset button. Explain that this represents an applicant with high savings, stable job, and clean checking balance.
   - Click **"Run AI Credit Assessment"**.

3. **Page 3 (Prediction Results):**
   - Show the **Likely Approved** banner and high approval probability (e.g., 90%+).
   - Review the **Model Performance Snapshot** (74% test accuracy, Confusion Matrix).
   - Click **"Inspect Full SHAP Explanation Waterfall ➔"**.

4. **Page 4 (SHAP Explanation):**
   - Explain the **Base Value** (the average expected approval probability across the training population).
   - Show the **Horizontal Contribution Bar Chart**:
     - **Green bars** indicate features that pulled the score *up* (e.g., checking status, high savings, low loan tenure).
     - **Red bars** indicate any risk factors pulling the score down.
   - Switch to the **"Global Model Feature Importance"** tab to show that the model globally prioritizes checking balance, duration, and credit amount.

5. **Test a High-Risk Case:**
   - Return to **Applicant Prediction** and click **"🔴 High-Risk Profile"** (overdrawn checking, large business loan, 48-month tenure).
   - Run assessment to demonstrate the **Likely Rejected** decision, showing how SHAP immediately pinpoints the exact risk drivers (Adverse Action Reasons).

6. **Page 5 (About the Project):**
   - Conclude by presenting the mathematical foundation of **Shapley values** and reviewing the **Planned Future Enhancements**.

---

## 🔮 Planned Future Enhancements

The following extensions are planned for subsequent research versions:

1. **LIME Integration:** Implement Local Interpretable Model-agnostic Explanations as a secondary explanation framework to contrast surrogate linear approximations against SHAP.
2. **Counterfactual Explanations (DiCE):** Implement Diverse Counterfactual Explanations to answer *what-if* questions (e.g., *"How much does the applicant need to reduce their loan request to achieve approval?"*).
3. **Demographic Fairness Auditing:** Compute algorithmic fairness metrics (Demographic Parity, Equalized Odds, Disparate Impact Ratio) across sensitive attributes such as gender and age.
4. **Explanation Stability Testing:** Measure the perturbation invariance and consistency of generated explanations across model retraining and noise injection.
5. **Real-World Evaluation & Regulatory Alignment:** Map top negative SHAP attributes directly into standardized regulatory adverse action reason codes used by consumer credit bureaus.

---

## 📜 License & Acknowledgments
- Dataset source: **UCI Machine Learning Repository (Statlog German Credit Data)**.
- Built with open-source Python data science tools: `streamlit`, `xgboost`, `shap`, `scikit-learn`, `pandas`, `plotly`.
