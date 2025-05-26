import pandas as pd
import requests
df = pd.read_csv("data/myths.csv")

# Load your myths CSV
df = pd.read_csv("myths.csv")

# Check each source URL
for i, row in df.iterrows():
    url = row['source']
    try:
        r = requests.head(url, timeout=5)
        if r.status_code >= 400:
            print(f"❌ Broken link at row {i}: {url}")
    except Exception as e:
        print(f"⚠️ Error checking {url}: {e}")
      
