# 📋 PhonePe App Configuration & Customization Guide

## 🎛️ Configuration Options

### 1. Fraud Detection Threshold

**Location:** `phonepe_app.py`, line 68

```python
# Current setting
is_fraud = fraud_prob > 0.98  # Very strict (fewer false alarms)

# Alternatives:
is_fraud = fraud_prob > 0.90  # More sensitive (catches more fraud)
is_fraud = fraud_prob > 0.95  # Balanced
is_fraud = fraud_prob > 0.99  # Maximum strict
```

**Impact:**
- **Lower threshold (0.90):** More transactions blocked, higher false alarms
- **Higher threshold (0.99):** Fewer transactions blocked, might miss fraud
- **Default (0.98):** Best balance based on model training

---

### 2. User Initial Balance

**Location:** `phonepe_app.py`, UserProfile class

```python
# Current
self.balance = 50000 if not is_fraudster else 5000

# Options:
self.balance = 100000 if not is_fraudster else 2000  # More balance
self.balance = 25000 if not is_fraudster else 5000   # Less balance
```

---

### 3. Fraudster Behavior Patterns

**Location:** `phonepe_app.py`, UserProfile.__init__

```python
if is_fraudster:
    # High-amount pattern
    self.avg_txn_amount = random.uniform(5000, 15000)  # Change range
    self.txn_frequency = random.uniform(5, 15)         # Change frequency
    self.uses_vpn = True if random.random() > 0.3 else False  # VPN usage %
```

---

### 4. Dashboard Settings

**Location:** `dashboard_app.py`

```python
# Flask settings
app.run(
    debug=True,           # Set to False for production
    host='0.0.0.0',      # Accessible from network
    port=5001            # Change to different port if needed
)

# CORS settings
CORS(app)  # Enable/disable cross-origin requests
```

---

## 🔧 Advanced Customization

### Add New Feature to Fraud Detection

**Steps:**

1. **Add field to UserProfile:**
```python
class UserProfile:
    def __init__(self, ...):
        self.device_id = None
        self.location_history = []
```

2. **Calculate in transaction:**
```python
def process_transaction(self, ...):
    # Collect device/location data
    user_features = {
        'device_change': self._detect_device_change(),
        'location_unusual': self._check_location(),
    }
```

3. **Add to fraud score:**
```python
all_features.update({
    'device_changes_24h': user_features['device_change'],
    'location_unusual': user_features['location_unusual'],
})
```

---

### Custom User Profile Creation

```python
# Load from CSV
import pandas as pd

df = pd.read_csv('users.csv')

for idx, row in df.iterrows():
    user = UserProfile(
        user_id=row['user_id'],
        name=row['name'],
        phone=row['phone'],
        is_fraudster=row['is_fraudster']
    )
    app.users[row['user_id']] = user
```

---

### Modify Feature Calculation

**Current features (13):**
```
amount, s_txn_count_10min, s_txn_count_1h, s_avg_amount_5,
s_max_amount_5, s_amount_std_5, s_time_gap_avg, r_amount_sum_24h,
geo_distance_km, r_txn_count_1h, r_txn_count_24h,
r_unique_senders_24h, vpn_proxy_flag
```

**Add more features:**
```python
def calculate_user_features(self, user, role):
    features = {}
    
    # Existing features...
    
    # NEW FEATURES
    features['account_age_days'] = (datetime.now() - user.created_at).days
    features['first_transaction'] = 1 if not user.txn_history else 0
    features['device_change'] = self._detect_device_changes(user)
    
    return features
```

---

## 📊 Customizing Reports

### Generate Custom CSV Report

```python
def custom_report(app):
    data = []
    for txn in app.transactions:
        data.append({
            'txn_id': txn.txn_id,
            'sender_risk': 'HIGH' if txn.sender.is_fraudster else 'LOW',
            'receiver_risk': 'HIGH' if txn.receiver.is_fraudster else 'LOW',
            'fraud_score': txn.fraud_score,
            'amount': txn.amount,
            'profit_center': 'FRAUD_PREVENTED' if txn.is_flagged else 'REVENUE',
        })
    
    return pd.DataFrame(data)
```

---

### Custom Dashboard Metrics

```python
@app.route('/api/custom-metrics')
def custom_metrics():
    return jsonify({
        'avg_fraud_score': np.mean([t.fraud_score for t in phonepe.transactions]),
        'high_risk_users': sum(1 for u in phonepe.users.values() if u.is_fraudster),
        'revenue_protected': sum(t.amount for t in phonepe.transactions if t.is_flagged),
        'customer_impact': {
            'accounts_created': len(phonepe.users),
            'transactions_processed': len(phonepe.transactions),
        }
    })
```

---

## 🎯 Performance Tuning

### Optimize Feature Calculation

```python
# SLOW VERSION
for window_size in [1, 5, 10, 24]:
    features[f's_txn_count_{window_size}'] = self._slow_calculation(window_size)

# FAST VERSION (cache results)
from functools import lru_cache

@lru_cache(maxsize=1000)
def calculate_user_features(self, user_id, timestamp):
    # Calculate once, cache results
    pass
```

### Optimize Model Loading

```python
# Load model once at startup
class FraudDetectionEngine:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = FraudDetectionEngine()
        return cls._instance
```

---

## 🔐 Security Enhancements

### Add Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/process-transaction', methods=['POST'])
@limiter.limit("5 per minute")
def process_transaction():
    # Process transaction
    pass
```

---

### Add Authentication

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "admin": "secure_password_123"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/api/transactions')
@auth.login_required
def get_transactions():
    # Return transactions only if authenticated
    pass
```

---

### Audit Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
handler = RotatingFileHandler('fraud_app.log', maxBytes=10000, backupCount=10)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Log all transactions
app.logger.info(f"Transaction {txn.txn_id}: {txn.sender.user_id} → {txn.receiver.user_id}, Score: {txn.fraud_score}")
```

---

## 🌐 Deployment Configuration

### Docker Setup

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY phonepe_app.py dashboard_app.py ./
COPY templates/ templates/
COPY fraud_engine.pkl scaler.pkl ./

EXPOSE 5001

CMD ["python", "dashboard_app.py"]
```

**requirements.txt:**
```
flask==2.3.0
flask-cors==4.0.0
pandas==1.5.0
numpy==1.24.0
lightgbm==4.0.0
scikit-learn==1.2.2
joblib==1.3.0
```

---

### Environment Variables

```python
# Use .env file
from dotenv import load_dotenv
import os

load_dotenv()

FRAUD_THRESHOLD = float(os.getenv('FRAUD_THRESHOLD', '0.98'))
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False') == 'True'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
PORT = int(os.getenv('PORT', '5001'))
```

---

## 📈 Data Analysis Enhancements

### Export for BI Tools

```python
def export_to_parquet(app):
    df = app.generate_transaction_report()
    df.to_parquet('transactions.parquet', compression='snappy')

def export_to_database(app):
    import sqlite3
    conn = sqlite3.connect('fraud_detection.db')
    df = app.generate_transaction_report()
    df.to_sql('transactions', conn, if_exists='append', index=False)
    conn.close()
```

---

### Real-time Dashboarding

```python
# With Plotly Dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

dash_app = Dash(__name__)

@dash_app.callback(
    Output('fraud-chart', 'figure'),
    Input('refresh-interval', 'n_intervals')
)
def update_chart(n):
    df = phonepe.generate_transaction_report()
    fig = go.Figure(data=[
        go.Bar(x=df['timestamp'], y=df['fraud_score'])
    ])
    return fig
```

---

## 🧪 Testing Configuration

### Unit Tests

```python
# test_phonepe.py
import unittest

class TestPhonePeApp(unittest.TestCase):
    def setUp(self):
        self.app = PhonePeApp()
        self.app.create_user_profiles()
    
    def test_legitimate_transaction(self):
        txn, analysis = self.app.process_transaction(
            "USER_001", "USER_002", 500
        )
        self.assertLess(txn.fraud_score, 0.5)
        self.assertFalse(txn.is_flagged)
    
    def test_fraudster_transaction(self):
        txn, analysis = self.app.process_transaction(
            "FRAUD_001", "USER_002", 3000
        )
        self.assertGreater(txn.fraud_score, 0.5)

if __name__ == '__main__':
    unittest.main()
```

---

## 🔍 Monitoring & Metrics

### Health Check Endpoint

```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': phonepe.fraud_engine.model_loaded,
        'total_users': len(phonepe.users),
        'transactions_processed': len(phonepe.transactions),
        'uptime_seconds': time.time() - app.start_time,
    })
```

---

### Performance Metrics

```python
import time

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'avg_processing_time': [],
            'fraud_detection_time': [],
        }
    
    def record_processing_time(self, duration):
        self.metrics['avg_processing_time'].append(duration)
    
    def get_average_time(self):
        return np.mean(self.metrics['avg_processing_time'])
```

---

## 🎓 Learning Path

1. **Start:** Run `python demo_scenarios.py`
2. **Understand:** Read feature explanations in README
3. **Customize:** Modify user profiles and thresholds
4. **Extend:** Add new features to fraud detection
5. **Deploy:** Use Docker configuration for production
6. **Monitor:** Set up health checks and logging
7. **Optimize:** Tune performance and accuracy

---

**Version:** 1.0.0  
**Last Updated:** February 2026

For more information, see:
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [phonepe_app.py](phonepe_app.py) - Source code
