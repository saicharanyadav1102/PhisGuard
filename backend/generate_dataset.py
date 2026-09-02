import pandas as pd
import numpy as np

# Generate 500 Safe URLs (Alexa Top 500)
safe_data = {
    'url': [f'http://safe-site-{i}.com' for i in range(500)],
    'redirect_count': np.random.choice([0, 1], size=500, p=[0.9, 0.1]),
    'roi_discrepancy': np.random.uniform(0.0, 0.1, 500),
    'iframe_ratio': np.random.uniform(0.0, 0.2, 500),
    'domain_age_days': np.random.randint(1000, 7000, 500),
    'ssl_active': np.random.choice([1, 0], size=500, p=[0.99, 0.01]),
    'label': np.zeros(500, dtype=int)
}

# Generate 500 Phishing URLs (PhishTank style)
phish_data = {
    'url': [f'http://phish-site-{i}.tk' for i in range(500)],
    'redirect_count': np.random.randint(2, 10, 500),
    'roi_discrepancy': np.random.uniform(0.5, 1.0, 500),
    'iframe_ratio': np.random.uniform(0.4, 1.0, 500),
    'domain_age_days': np.random.randint(1, 30, 500),
    'ssl_active': np.random.choice([1, 0], size=500, p=[0.2, 0.8]),
    'label': np.ones(500, dtype=int)
}

df_safe = pd.DataFrame(safe_data)
df_phish = pd.DataFrame(phish_data)

df = pd.concat([df_safe, df_phish]).sample(frac=1).reset_index(drop=True)
df.to_csv('data/phishing_dataset.csv', index=False)
print("Generated 1000 synthetic records mimicking PhishTank and Alexa Top 500.")
