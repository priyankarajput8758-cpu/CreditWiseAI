"""
Preset applicant profiles and form choice options for the German Credit dataset.
Used for quick demoing and form population.
"""

# Categorical options mapping for UI dropdowns
FEATURE_OPTIONS = {
    'checking_status': [
        '>= 200 DM / Salary 1+ yr',
        'No checking account',
        '0 - 200 DM (Low balance)',
        '< 0 DM (Overdrawn)'
    ],
    'credit_history': [
        'Existing credits paid duly till now',
        'Critical account / other credits elsewhere',
        'Delay in paying in past',
        'All credits at this bank paid duly',
        'No credits / all paid duly'
    ],
    'purpose': [
        'Car (new)',
        'Car (used)',
        'Furniture / Equipment',
        'Radio / Television',
        'Domestic appliances',
        'Repairs',
        'Education',
        'Business',
        'Retraining',
        'Others'
    ],
    'savings_status': [
        '>= 1000 DM (High savings)',
        '500 - 1000 DM (Medium savings)',
        '100 - 500 DM (Moderate savings)',
        '< 100 DM (Minimal savings)',
        'Unknown / No savings account'
    ],
    'employment': [
        '>= 7 years',
        '4 - 7 years',
        '1 - 4 years',
        '< 1 year',
        'Unemployed'
    ],
    'personal_status': [
        'Male: Single',
        'Female: Divorced / Married',
        'Male: Married / Widowed',
        'Male: Divorced / Separated',
        'Female: Single'
    ],
    'other_debtors': [
        'None',
        'Guarantor',
        'Co-applicant'
    ],
    'property': [
        'Real estate',
        'Building society savings / Life insurance',
        'Car or other',
        'Unknown / No property'
    ],
    'other_installment_plans': [
        'None',
        'Bank',
        'Stores'
    ],
    'housing': [
        'Own',
        'Rent',
        'For free'
    ],
    'job': [
        'Management / Self-employed / Highly qualified',
        'Skilled employee / official',
        'Unskilled resident',
        'Unemployed / Unskilled non-resident'
    ],
    'telephone': [
        'Yes (registered in name)',
        'None'
    ],
    'foreign_worker': [
        'Yes',
        'No'
    ]
}

# Pre-defined profiles for live faculty demonstration
PRESET_PROFILES = {
    "Prime Applicant (High Likelihood of Approval)": {
        'name': 'Dr. Marcus Vance (Low Risk)',
        'description': 'Senior professional with high savings, real estate ownership, long employment, and established banking relationship.',
        'checking_status': '>= 200 DM / Salary 1+ yr',
        'duration_months': 12,
        'credit_history': 'Existing credits paid duly till now',
        'purpose': 'Car (new)',
        'credit_amount': 2500,
        'savings_status': '>= 1000 DM (High savings)',
        'employment': '>= 7 years',
        'installment_rate': 2,
        'personal_status': 'Male: Single',
        'other_debtors': 'None',
        'residence_since': 4,
        'property': 'Real estate',
        'age': 45,
        'other_installment_plans': 'None',
        'housing': 'Own',
        'existing_credits': 2,
        'job': 'Management / Self-employed / Highly qualified',
        'num_dependents': 1,
        'telephone': 'Yes (registered in name)',
        'foreign_worker': 'No'
    },
    "High-Risk Applicant (High Likelihood of Rejection)": {
        'name': 'Alex Novak (Elevated Risk)',
        'description': 'Short work tenure, overdrawn checking account, high loan amount requested for business, minimal savings reserve.',
        'checking_status': '< 0 DM (Overdrawn)',
        'duration_months': 48,
        'credit_history': 'Delay in paying in past',
        'purpose': 'Business',
        'credit_amount': 11800,
        'savings_status': '< 100 DM (Minimal savings)',
        'employment': '< 1 year',
        'installment_rate': 4,
        'personal_status': 'Female: Divorced / Married',
        'other_debtors': 'None',
        'residence_since': 1,
        'property': 'Unknown / No property',
        'age': 22,
        'other_installment_plans': 'Bank',
        'housing': 'Rent',
        'existing_credits': 1,
        'job': 'Unskilled resident',
        'num_dependents': 1,
        'telephone': 'None',
        'foreign_worker': 'Yes'
    },
    "Borderline / Moderate Risk Applicant": {
        'name': 'Elena Rostova (Borderline Case)',
        'description': 'Mid-level skilled employee seeking appliance loan, modest savings, moderate duration and installment load.',
        'checking_status': '0 - 200 DM (Low balance)',
        'duration_months': 24,
        'credit_history': 'Existing credits paid duly till now',
        'purpose': 'Furniture / Equipment',
        'credit_amount': 4200,
        'savings_status': '100 - 500 DM (Moderate savings)',
        'employment': '1 - 4 years',
        'installment_rate': 3,
        'personal_status': 'Female: Divorced / Married',
        'other_debtors': 'None',
        'residence_since': 2,
        'property': 'Car or other',
        'age': 29,
        'other_installment_plans': 'None',
        'housing': 'Rent',
        'existing_credits': 1,
        'job': 'Skilled employee / official',
        'num_dependents': 1,
        'telephone': 'Yes (registered in name)',
        'foreign_worker': 'Yes'
    }
}
