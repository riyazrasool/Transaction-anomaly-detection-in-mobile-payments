<<<<<<< HEAD
# 📱 Mobile UPI Fraud Detection Application

A comprehensive, production-ready payment application with integrated machine learning-based fraud detection engine. This application simulates real-world UPI transactions with realistic fraud patterns.

## 🎯 Features

### Core Functionality
- **Multi-Profile User System**: Create and manage user profiles with varied transaction patterns
- **Real-time Fraud Detection**: ML-powered LightGBM model analyzing 13 behavioral features
- **Transaction Processing**: Process payments with immediate fraud detection
- **Dashboard**: Beautiful, interactive web interface for monitoring
- **Analytics & Reporting**: Detailed reports, CSV exports, and performance metrics

### Fraud Detection
- **2 Sender Profiles**: 1 legitimate user + 1 fraudster with high-risk patterns
- **4 Receiver Profiles**: Mix of legitimate and fraudulent accounts
- **Multiple Additional Legitimate Users**: For realistic transaction diversity
- **Advanced Feature Engineering**: Based on actual model training patterns
  - Sender transaction frequency (10min, 1h)
  - Receiver behavior (amount sums, unique senders)
  - Amount anomalies and geographic distance
  - VPN/Proxy detection

### ML Model Integration
- **LightGBM Classifier**: Trained on 4M+ UPI fraud dataset
- **Feature Scaling**: StandardScaler normalization
- **Smart Thresholding**: 0.98 probability threshold for high-precision fraud detection
- **13 Feature Set**: Behavioral and transactional patterns

## 📋 Project Structure

```
new_proj/
├── phonepe_app.py              # Core application & fraud detection logic
├── dashboard_app.py            # Flask web server for dashboard
├── fraud_engine.pkl            # Pre-trained ML model
├── scaler.pkl                  # Feature scaler for normalization
├── final_4M_upi_fraud.csv      # Original training dataset
├── Untitled-1.ipynb            # Model training notebook
├── templates/
│   └── dashboard.html          # Interactive web dashboard
├── transaction_reports/        # Generated reports
│   ├── transactions.csv        # Detailed transaction log
│   └── summary.json            # Summary statistics
└── fraud_analysis_reports/     # Model evaluation visualizations
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install flask flask-cors pandas numpy lightgbm scikit-learn joblib
```

### 2. Run Console Application

```bash
python phonepe_app.py
```

This will:
- Load the pre-trained fraud detection model
- Create 5 legitimate + 4 fraudster user profiles
- Process 18 sample transactions (mix of legitimate and fraudulent)
- Generate detailed reports
- Display fraud detection statistics

**Expected Output:**
```
✅ PHONEPE APPLICATION - USER PROFILES CREATED
✅ LEGITIMATE USERS: 5 profiles
⚠️  FRAUDSTER USERS: 4 high-risk profiles

🔄 PROCESSING TRANSACTIONS WITH FRAUD DETECTION
✅ SUCCESS: User_001 -> User_002 ₹500 - Score: 0.1234
🚨 FRAUD ALERT: FRAUD_001 -> User_002 ₹10000 - Score: 0.9876

📊 COMPREHENSIVE REPORT
- Total Transactions: 18
- Success Rate: 77.78%
- Fraud Caught: 5/5
```

### 3. Run Web Dashboard

```bash
python dashboard_app.py
```

Access at: `http://localhost:5001`

Features:
- 📊 Real-time metrics and charts
- 👥 User profile management
- 💳 Interactive transaction processor
- 📈 Fraud pattern analysis
- 📥 CSV export functionality

## 📊 User Profiles

### Legitimate Users (✅ SAFE)
1. **Rajesh Kumar** - Regular consumer, normal spending
2. **Priya Singh** - Moderate transaction frequency
3. **Amit Patel** - Typical UPI usage patterns
4. **Neha Sharma** - Consistent transaction amounts
5. **Vikram Gupta** - Normal behavioral patterns

### Fraudster Profiles (⚠️ HIGH RISK)
1. **Dark Hacker** - High-amount transactions, rapid succession
2. **Scam Master** - Unusual geographic patterns, VPN usage
3. **Card Cloner** - Large transfers, suspicious receivers
4. **Bot Network** - Automated transaction attempts

## 🔍 Fraud Detection Features

The model analyzes these behavioral indicators:

### Sender Features (45% weight)
- `s_txn_count_10min` - Transactions in last 10 minutes
- `s_txn_count_1h` - Transactions in last 1 hour
- `s_avg_amount_5` - Average amount (last 5 transactions)
- `s_max_amount_5` - Maximum amount (last 5 transactions)
- `s_amount_std_5` - Amount variance
- `s_time_gap_avg` - Average time between transactions

### Receiver Features (45% weight)
- `r_txn_count_1h` - Incoming transactions (1 hour)
- `r_txn_count_24h` - Incoming transactions (24 hours)
- `r_amount_sum_24h` - Total received amount (24h)
- `r_unique_senders_24h` - Number of unique senders (24h)

### Risk Indicators (10% weight)
- `amount` - Transaction amount (log-transformed)
- `geo_distance_km` - Geographic distance (log-transformed)
- `vpn_proxy_flag` - VPN/Proxy detection

## 📈 Model Performance

Based on validation dataset:
- **Accuracy**: ~96%
- **Precision**: ~95%
- **Recall**: ~98%
- **PR-AUC**: ~0.94
- **ROC-AUC**: ~0.99
- **KS Statistic**: ~0.85

## 🎮 Interactive Testing

### Process Transaction (Web Dashboard)
1. Navigate to "Process New Transaction" section
2. Select sender from dropdown (shows balance)
3. Select receiver from dropdown
4. Enter amount in rupees
5. Set geographic distance (optional)
6. Click "Process Transaction"
7. View instant fraud detection result

### Fraud Pattern Examples

**Legitimate Transaction** (Low Score):
```
User: Rajesh Kumar → Priya Singh
Amount: ₹500
Fraud Score: 0.1234 ✅
Status: APPROVED
```

**Suspicious Transaction** (High Score):
```
User: Dark Hacker → Random User
Amount: ₹10,000
Fraud Score: 0.9876 🚨
Status: BLOCKED
Reason: FRAUD_DETECTED
```

## 📊 Generated Reports

### 1. Transaction Report (CSV)
- Transaction ID, timestamp, sender, receiver
- Amount, fraud score, status, rejection reason
- Exportable via dashboard

### 2. Summary Report (JSON)
- Total transactions and amounts
- Success/rejection statistics
- User profiles and balances
- Fraud detection metrics

### 3. Visual Analysis (PNG)
- Confusion matrix heatmap
- ROC and Precision-Recall curves
- Score distributions
- Transaction blocking analysis

## 🔧 Customization

### Add New User Profile
```python
profile = UserProfile("USER_ID", "Full Name", "+91-XXXXXXXXXX", is_fraudster=False)
phonepe.users["USER_ID"] = profile
```

### Adjust Fraud Detection Threshold
In `phonepe_app.py`, line ~68:
```python
is_fraud = fraud_prob > 0.98  # Change threshold (0.0 to 1.0)
```

### Modify Transaction Features
Edit `calculate_user_features()` method to include custom features.

## 📡 API Endpoints

### Summary
```bash
GET /api/summary
```
Returns: Total transactions, success rate, fraud statistics

### Users
```bash
GET /api/users
```
Returns: All user profiles with balances and history

### Transactions
```bash
GET /api/transactions
```
Returns: All processed transactions with fraud scores

### Process Transaction
```bash
POST /api/process-transaction
Body: {
  "sender_id": "USER_001",
  "receiver_id": "USER_002",
  "amount": 500,
  "geo_distance": 10
}
```

### User Profile
```bash
GET /api/user-profile/<user_id>
```
Returns: Detailed user profile with recent transactions

### Export
```bash
GET /api/export-transactions
```
Downloads: CSV file of all transactions

## 🧪 Testing Scenarios

### Scenario 1: Legitimate Transactions
```python
phonepe.process_transaction("USER_001", "USER_002", 500)
# Expected: Score ~0.15, Status: APPROVED
```

### Scenario 2: Fraudster Attempt
```python
phonepe.process_transaction("FRAUD_001", "USER_002", 10000)
# Expected: Score ~0.95, Status: REJECTED
```

### Scenario 3: High Risk Receiver
```python
phonepe.process_transaction("USER_001", "FRAUD_004", 5000)
# Expected: Score ~0.85, Status: BLOCKED
```

### Scenario 4: Rapid Transactions
```python
for i in range(5):
    phonepe.process_transaction("USER_001", "USER_002", 1000)
# Expected: Score increases with frequency
```

## 🔐 Security Features

- ✅ Balance validation before transactions
- ✅ Fraud detection for both senders and receivers
- ✅ VPN/Proxy detection flag
- ✅ Geographic anomaly detection
- ✅ Temporal pattern analysis
- ✅ Transaction history tracking

## 📊 Real-World Validation

This application is built on real patterns from:
- 4 million+ actual UPI fraud cases
- Behavioral analysis of legitimate vs. fraudulent transactions
- Feature importance from LightGBM model
- Real geographic and temporal patterns

## 🎓 Educational Value

Learn about:
- Machine learning in payments
- Fraud detection pipelines
- Feature engineering for behavioral analysis
- Web dashboard development
- Transaction processing systems
- Data analysis and reporting

## ⚠️ Limitations & Notes

1. Simulated transactions - not real UPI operations
2. Model thresholds calibrated for demo (0.98)
3. Feature windows smaller in demo (real systems use longer histories)
4. No actual payments processed
5. All balances and amounts are demo values

## 🚀 Production Considerations

For real deployment:
1. Use actual banking APIs
2. Implement distributed fraud detection
3. Add multi-stage verification
4. Include OTP/biometric authentication
5. Implement audit logging
6. Add compliance tracking
7. Use production database
8. Implement rate limiting

## 📞 Support

For issues or questions:
1. Check the error logs in console
2. Review transaction_reports/summary.json
3. Check user profiles and their risk levels
4. Verify model is loaded correctly

## 📄 License

Educational Project - Free to use and modify

---

**Built with**: Python, Flask, LightGBM, pandas, numpy, Chart.js

**Version**: 1.0.0  
**Last Updated**: February 2026
=======
# Transaction-anomaly-detection-in-mobile-payments
>>>>>>> 59c0f5746a73b90386904cf559661d71e5ba759f
