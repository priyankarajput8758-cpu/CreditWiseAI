"""
Machine Learning & Explainable AI pipeline for the Loan Approval Prototype.
Handles dataset loading, XGBoost training, evaluation, inference, and SHAP explanations.
"""

import os
import urllib.request
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_score, recall_score, f1_score
import streamlit as st

DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "german_credit.csv")

FEATURE_LABELS = {
    'checking_status': 'Checking Account Status',
    'duration_months': 'Loan Duration (Months)',
    'credit_history': 'Credit History Record',
    'purpose': 'Loan Purpose',
    'credit_amount': 'Credit Amount (DM)',
    'savings_status': 'Savings Account Balance',
    'employment': 'Employment Tenure',
    'installment_rate': 'Installment Rate (% of Income)',
    'personal_status': 'Personal Status & Sex',
    'other_debtors': 'Other Debtors / Guarantors',
    'residence_since': 'Present Residence (Years)',
    'property': 'Property Ownership',
    'age': 'Applicant Age (Years)',
    'other_installment_plans': 'Other Installment Plans',
    'housing': 'Housing Type',
    'existing_credits': 'Existing Bank Credits',
    'job': 'Employment Classification',
    'num_dependents': 'Number of Dependents',
    'telephone': 'Telephone Registration',
    'foreign_worker': 'Foreign Worker Status'
}

RAW_MAPPINGS = {
    'checking_status': {
        'A11': '< 0 DM (Overdrawn)',
        'A12': '0 - 200 DM (Low balance)',
        'A13': '>= 200 DM / Salary 1+ yr',
        'A14': 'No checking account'
    },
    'credit_history': {
        'A30': 'No credits / all paid duly',
        'A31': 'All credits at this bank paid duly',
        'A32': 'Existing credits paid duly till now',
        'A33': 'Delay in paying in past',
        'A34': 'Critical account / other credits elsewhere'
    },
    'purpose': {
        'A40': 'Car (new)',
        'A41': 'Car (used)',
        'A42': 'Furniture / Equipment',
        'A43': 'Radio / Television',
        'A44': 'Domestic appliances',
        'A45': 'Repairs',
        'A46': 'Education',
        'A47': 'Vacation',
        'A48': 'Retraining',
        'A49': 'Business',
        'A410': 'Others'
    },
    'savings_status': {
        'A61': '< 100 DM (Minimal savings)',
        'A62': '100 - 500 DM (Moderate savings)',
        'A63': '500 - 1000 DM (Medium savings)',
        'A64': '>= 1000 DM (High savings)',
        'A65': 'Unknown / No savings account'
    },
    'employment': {
        'A71': 'Unemployed',
        'A72': '< 1 year',
        'A73': '1 - 4 years',
        'A74': '4 - 7 years',
        'A75': '>= 7 years'
    },
    'personal_status': {
        'A91': 'Male: Divorced / Separated',
        'A92': 'Female: Divorced / Married',
        'A93': 'Male: Single',
        'A94': 'Male: Married / Widowed',
        'A95': 'Female: Single'
    },
    'other_debtors': {
        'A101': 'None',
        'A102': 'Co-applicant',
        'A103': 'Guarantor'
    },
    'property': {
        'A121': 'Real estate',
        'A122': 'Building society savings / Life insurance',
        'A123': 'Car or other',
        'A124': 'Unknown / No property'
    },
    'other_installment_plans': {
        'A141': 'Bank',
        'A142': 'Stores',
        'A143': 'None'
    },
    'housing': {
        'A151': 'Rent',
        'A152': 'Own',
        'A153': 'For free'
    },
    'job': {
        'A171': 'Unemployed / Unskilled non-resident',
        'A172': 'Unskilled resident',
        'A173': 'Skilled employee / official',
        'A174': 'Management / Self-employed / Highly qualified'
    },
    'telephone': {
        'A191': 'None',
        'A192': 'Yes (registered in name)'
    },
    'foreign_worker': {
        'A201': 'Yes',
        'A202': 'No'
    }
}

def load_or_download_dataset():
    """Loads the preprocessed German Credit dataset, or downloads and cleans it from UCI."""
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        return df

    # Download from UCI if local copy is missing
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"
    columns = [
        'checking_status', 'duration_months', 'credit_history', 'purpose',
        'credit_amount', 'savings_status', 'employment', 'installment_rate',
        'personal_status', 'other_debtors', 'residence_since', 'property',
        'age', 'other_installment_plans', 'housing', 'existing_credits',
        'job', 'num_dependents', 'telephone', 'foreign_worker', 'target'
    ]
    raw_df = pd.read_csv(url, sep=' ', header=None, names=columns)
    
    # 1: Good Risk -> 1 (Approved), 2: Bad Risk -> 0 (Rejected)
    raw_df['target'] = raw_df['target'].apply(lambda x: 1 if x == 1 else 0)

    clean_df = raw_df.copy()
    for col, mapping in RAW_MAPPINGS.items():
        clean_df[col] = clean_df[col].map(mapping).fillna(clean_df[col])

    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
    clean_df.to_csv(DATASET_PATH, index=False)
    return clean_df

@st.cache_resource(show_spinner="Training XGBoost model and computing SHAP explainer...")
def initialize_ai_pipeline():
    """
    Trains the XGBoost classifier, fits LabelEncoders, computes test evaluation metrics,
    and sets up the SHAP TreeExplainer. Cached for instant responsiveness.
    """
    df = load_or_download_dataset()
    X = df.drop('target', axis=1)
    y = df['target']

    # Encode categorical features
    label_encoders = {}
    X_encoded = X.copy()
    categorical_cols = X_encoded.select_dtypes(include=['object', 'string']).columns

    for col in categorical_cols:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col])
        label_encoders[col] = le

    # 80/20 Stratified train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.20, random_state=42, stratify=y
    )

    # Train XGBoost Classifier
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=42,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    # Initialize SHAP TreeExplainer
    explainer = shap.TreeExplainer(model)
    test_shap_values = explainer(X_test)

    # Compute global feature importance (mean absolute SHAP)
    mean_abs_shap = np.mean(np.abs(test_shap_values.values), axis=0)
    global_importance_df = pd.DataFrame({
        'feature': X_encoded.columns,
        'label': [FEATURE_LABELS.get(c, c) for c in X_encoded.columns],
        'mean_abs_shap': mean_abs_shap
    }).sort_values(by='mean_abs_shap', ascending=False).reset_index(drop=True)

    artifacts = {
        'model': model,
        'explainer': explainer,
        'label_encoders': label_encoders,
        'feature_names': list(X.columns),
        'categorical_cols': list(categorical_cols),
        'X_train': X_train,
        'X_test': X_test,
        'y_test': y_test,
        'metrics': {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'confusion_matrix': cm,
            'report': report,
            'total_test_samples': len(y_test)
        },
        'global_importance_df': global_importance_df,
        'base_value': float(explainer.expected_value)
    }
    return artifacts

def encode_applicant_features(artifacts, applicant_dict):
    """Encodes a single applicant dict into a model-ready dataframe with strict numeric dtypes."""
    encoded_row = {}
    label_encoders = artifacts['label_encoders']

    for col in artifacts['feature_names']:
        val = applicant_dict.get(col, None)
        if col in artifacts['categorical_cols']:
            le = label_encoders[col]
            str_val = str(val) if val is not None else ""
            if str_val in le.classes_:
                encoded_row[col] = int(le.transform([str_val])[0])
            else:
                encoded_row[col] = 0
        else:
            try:
                encoded_row[col] = float(val) if val is not None else 0.0
            except (ValueError, TypeError):
                encoded_row[col] = 0.0

    df_applicant = pd.DataFrame([encoded_row], columns=artifacts['feature_names'])
    return df_applicant

def predict_applicant(artifacts, applicant_dict):
    """
    Runs model inference for a single applicant.
    Returns prediction category, approval probability, and formatted metrics.
    """
    encoded_df = encode_applicant_features(artifacts, applicant_dict)
    model = artifacts['model']

    prediction = int(model.predict(encoded_df)[0])
    probabilities = model.predict_proba(encoded_df)[0]
    prob_approved = float(probabilities[1])
    prob_rejected = float(probabilities[0])

    if prediction == 1:
        status_label = "Likely Approved"
        risk_tier = "Low Credit Risk" if prob_approved >= 0.75 else "Moderate Risk (Approved)"
        badge_class = "pill-approved"
    else:
        status_label = "Likely Rejected"
        risk_tier = "High Credit Risk" if prob_rejected >= 0.70 else "Borderline Rejected"
        badge_class = "pill-rejected"

    return {
        'prediction': prediction,
        'status_label': status_label,
        'prob_approved': prob_approved,
        'prob_rejected': prob_rejected,
        'approval_percentage': round(prob_approved * 100, 1),
        'rejection_percentage': round(prob_rejected * 100, 1),
        'risk_tier': risk_tier,
        'badge_class': badge_class,
        'encoded_df': encoded_df
    }

def explain_applicant(artifacts, applicant_dict):
    """
    Calculates exact SHAP values for the specified applicant using the TreeExplainer.
    Returns structured contributions and human-friendly interpretations.
    """
    encoded_df = encode_applicant_features(artifacts, applicant_dict)
    explainer = artifacts['explainer']
    
    # Calculate SHAP explanation
    shap_explanation = explainer(encoded_df)
    shap_vals = shap_explanation.values[0]
    base_val = float(explainer.expected_value)

    contributions = []
    for col, s_val in zip(artifacts['feature_names'], shap_vals):
        raw_val = applicant_dict.get(col, '')
        direction = "positive" if s_val > 0 else ("negative" if s_val < 0 else "neutral")
        contributions.append({
            'feature': col,
            'label': FEATURE_LABELS.get(col, col),
            'value': str(raw_val),
            'shap_value': float(s_val),
            'abs_shap': float(abs(s_val)),
            'direction': direction
        })

    # Sort by absolute magnitude of impact
    contributions_sorted = sorted(contributions, key=lambda x: x['abs_shap'], reverse=True)
    
    positive_drivers = [c for c in contributions_sorted if c['shap_value'] > 0]
    risk_drivers = [c for c in contributions_sorted if c['shap_value'] < 0]

    return {
        'base_value': base_val,
        'contributions': contributions_sorted,
        'top_positive': positive_drivers[:4],
        'top_risk': risk_drivers[:4],
        'all_shap_values': shap_vals,
        'encoded_df': encoded_df
    }
