import os
import math
from collections import Counter
import pandas as pd
from urllib.parse import urlparse

def get_url_entropy(url):
    s = url.lower()
    prob = [n/len(s) for n in Counter(s).values()]
    entropy = -sum([p * math.log2(p) for p in prob]) 
    return entropy

def extract_structural_features(url): 
    parsed = urlparse(url)
    return {
        'url_len': len(url), 
        'dot_count': url.count('.'),
        'is_ip': int(parsed.hostname.replace('.', '').isdigit()) if parsed.hostname else 0, 
        'entropy': get_url_entropy(url),
        'subdomain_count': len(parsed.hostname.split('.'))-2 if parsed.hostname else 0
    }

def process_raw_dataset(input_csv, output_csv): 
    df = pd.read_csv(input_csv)
    print(f"Processing {len(df)} records...")

    features = []
    for url in df['url']: 
        features.append(extract_structural_features(url))

    f_df = pd.DataFrame(features)
    final_df = pd.concat([df, f_df], axis=1) 
    final_df.to_csv(output_csv, index=False) 
    print("Feature extraction complete.")

if __name__ == "__main__":
    print("Preprocess script ready.")
