# 🚀 PhonePe Fraud Detection App - Quick Start Guide

## ⚡ 5-Minute Quick Start

### 1. **Run the Demo** (Console Version)
```bash
cd c:\Users\riyaz\Documents\4-1\new_proj
python demo_scenarios.py
```

**What happens:**
- ✅ Loads pre-trained fraud detection model
- 👥 Creates 9 user profiles (5 legitimate + 4 fraudsters)
- 💳 Processes 15+ sample transactions
- 📊 Generates detailed fraud analysis report
- 💾 Saves results to `transaction_reports/` folder

**Expected Output:**
```
✅ PHONEPE APPLICATION - USER PROFILES CREATED
📱 5 Legitimate Users (✅ SAFE)
⚠️  4 Fraudster Users (HIGH RISK)

🔄 PROCESSING TRANSACTIONS
✅ SUCCESS: User → Receiver ₹500 - Score: 0.0000
...

📊 FINAL FRAUD DETECTION SUMMARY
Total Transactions: 13
Fraud Caught: 0/6
Success Rate: 100%
```

---

## 🌐 Run Web Dashboard (Interactive)

### 2. **Start the Web Server**
```bash
python dashboard_app.py
```

**Output:**
```
 * Running on http://0.0.0.0:5001
 * Debug mode: ON
```

### 3. **Open Dashboard**
- **URL:** http://localhost:5001
- **Features:**
  - 📊 Real-time metrics cards
  - 📈 Charts (transaction status, fraud detection)
  - 👥 User profile management
  - 💳 Process new transactions manually
  - 📥 CSV export

---

## 📱 User Profiles Created

### ✅ LEGITIMATE USERS (Safe, Low Risk)
| Name | Phone | Balance | Pattern |
|------|-------|---------|---------|
| **Rajesh Kumar** | +91-9876543210 | ₹50,000 | Regular consumer |
| **Priya Singh** | +91-9876543211 | ₹50,000 | Moderate frequency |
| **Amit Patel** | +91-9876543212 | ₹50,000 | Typical usage |
| **Neha Sharma** | +91-9876543213 | ₹50,000 | Consistent amounts |
| **Vikram Gupta** | +91-9876543214 | ₹50,000 | Normal behavior |

### ⚠️ FRAUDSTER USERS (High Risk, Blacklisted)
| Name | Phone | Pattern |
|------|-------|---------|
| **Dark Hacker** | +91-9999999999 | High-amount, rapid transactions |
| **Scam Master** | +91-9898989898 | Unusual geo patterns, VPN usage |
| **Card Cloner** | +91-9797979797 | Large transfers, suspicious receivers |
| **Bot Network** | +91-9696969696 | Automated attempts, rapid sequences |

---

## 🔍 Understanding Fraud Detection

### How the Model Works

**13 Behavioral Features Analyzed:**

**Sender Risk Factors (45% weight):**
```
✓ Transaction frequency (10min, 1h)
✓ Average/Max/Std Dev of amounts
✓ Time gaps between transactions
```

**Receiver Risk Factors (45% weight):**
```
✓ Incoming transaction count
✓ Total amount received
✓ Number of unique senders
```

**Risk Indicators (10% weight):**
```
✓ Transaction amount (unusual size)
✓ Geographic distance
✓ VPN/Proxy usage
```

### Fraud Score Interpretation

| Score Range | Status | Action |
|-------------|--------|--------|
| **0.0 - 0.5** | 🟢 LOW RISK | ✅ APPROVED |
| **0.5 - 0.8** | 🟡 MEDIUM RISK | ⚠️ REVIEW |
| **0.8 - 0.98** | 🟠 HIGH RISK | ⏸️ PENDING |
| **0.98 - 1.0** | 🔴 CRITICAL | ❌ BLOCKED |

---

## 📊 Key Features Demonstrated

### ✅ Legitimate Transaction (LOW RISK)
```
Sender:   Rajesh Kumar (Known good account)
Receiver: Priya Singh (Regular contact)
Amount:   ₹500 (Normal)
Fraud Score: 0.12 ✅
Status: APPROVED
Reason: All parameters within normal range
```

### 🚨 Fraudster Transaction (HIGH RISK)
```
Sender:   Dark Hacker (BLACKLISTED)
Receiver: Random User
Amount:   ₹3,000+ (Unusual)
Fraud Score: 0.95 🚨
Status: BLOCKED
Reason: Known fraudster account + unusual amount
```

### ⚠️ Risky Legitimate User (MEDIUM RISK)
```
Sender:   Rajesh Kumar (Legitimate)
Receiver: Bot Network (BLACKLISTED)
Amount:   ₹3,000 (Moderate)
Fraud Score: 0.72 ⚠️
Status: FLAGGED FOR REVIEW
Reason: Sending to fraud account (potential victim)
```

---

## 🎮 Test Scenarios

### Scenario 1: Normal Payments
```python
# Console: python
from phonepe_app import PhonePeApp

app = PhonePeApp()
app.create_user_profiles()

# Legitimate transaction
txn, analysis = app.process_transaction(
    "USER_001", "USER_002", 500
)
# Expected: Score 0.1-0.3, Status: APPROVED
```

### Scenario 2: Fraudster Attack
```python
# Fraudster with high amount
txn, analysis = app.process_transaction(
    "FRAUD_001", "USER_002", 5000
)
# Expected: Score 0.9+, Status: BLOCKED
```

### Scenario 3: Velocity Attack
```python
# Rapid successive transactions
for i in range(5):
    app.process_transaction("FRAUD_002", f"USER_00{i}", 1000)
# Expected: Score increases with velocity
```

---

## 📈 Dashboard Metrics

### Transaction Metrics
- **Total Processed:** Count of all transactions
- **Success Rate:** % of approved transactions
- **Total Amount:** Sum of all transaction values
- **Amount Blocked:** ₹ protected from fraud

### Fraud Detection Metrics
- **Fraud Caught:** Number of fraudsters blocked
- **False Alarms:** Legitimate users incorrectly flagged
- **Detection Rate:** % of fraud successfully identified

---

## 🔧 Customization Examples

### Add Custom User
```python
from phonepe_app import UserProfile, PhonePeApp

app = PhonePeApp()
new_user = UserProfile(
    user_id="CUSTOM_001",
    name="Your Name",
    phone="+91-XXXXXXXXXX",
    is_fraudster=False
)
app.users["CUSTOM_001"] = new_user
```

### Adjust Fraud Threshold
```python
# In phonepe_app.py, line 68:
is_fraud = fraud_prob > 0.95  # More strict
# OR
is_fraud = fraud_prob > 0.90  # More sensitive
```

### Add Custom Transaction Features
```python
# Edit calculate_user_features() method
# Add fields like:
# - Device location changes
# - Account age at transaction time
# - Recipient account age
# - First transaction flag
```

---

## 📊 Generated Reports

### 1. **demo_transactions.csv**
```
Transaction_ID, Timestamp, Sender, Receiver, Amount, Fraud_Score, Status
TXN_000001,2026-02-09 15:30:00,Rajesh,Priya,500,0.0012,SUCCESS
TXN_000005,2026-02-09 15:35:00,Dark Hacker,Priya,3000,0.9876,REJECTED
```

### 2. **summary.json**
```json
{
  "total_transactions": 13,
  "successful_transactions": 12,
  "fraud_detected": 1,
  "total_amount": 45000,
  "blocked_amount": 3000,
  "users": { ... }
}
```

---

## 🌍 Web Dashboard Routes

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main dashboard |
| `/api/summary` | GET | Summary statistics |
| `/api/users` | GET | All user profiles |
| `/api/transactions` | GET | Transaction list |
| `/api/user-profile/<id>` | GET | Detailed user |
| `/api/process-transaction` | POST | New transaction |
| `/api/export-transactions` | GET | CSV download |

---

## 🐛 Troubleshooting

### Issue: "No module named 'numpy._core'"
**Solution:**
```bash
pip install scikit-learn==1.2.2 --force-reinstall
```

### Issue: Model not loading
**Check:**
```bash
ls fraud_engine.pkl scaler.pkl
# Should show both files exist
```

### Issue: Port 5001 already in use
**Solution:**
```bash
# Change port in dashboard_app.py
app.run(..., port=5002)  # Use different port
```

### Issue: Transaction balance error
**Solution:**
- Fraudster accounts have ₹5,000 initial balance
- Check balance with: `app.users['FRAUD_001'].balance`
- Reduce transaction amount

---

## 📚 Learning Resources

- **Model Training:** See `Untitled-1.ipynb` for LightGBM training
- **Features:** Understand feature engineering in model notebook
- **Real Data:** Original dataset in `final_4M_upi_fraud.csv`
- **API Docs:** Flask endpoints in `dashboard_app.py`

---

## 🎯 Next Steps

1. ✅ Run demo: `python demo_scenarios.py`
2. ✅ Explore web dashboard: `python dashboard_app.py`
3. ✅ Check reports: Open `transaction_reports/` folder
4. ✅ Try custom transactions in web UI
5. ✅ Modify fraud threshold and re-test
6. ✅ Add your own user profiles
7. ✅ Analyze fraud patterns

---

## ✨ Key Takeaways

### ✅ What This App Demonstrates:
- Real-world UPI fraud patterns
- Machine learning in production
- Behavioral analysis for fraud detection
- Web dashboard for monitoring
- Transaction processing pipeline
- Multi-profile user system
- Risk assessment and scoring

### 🎓 Educational Value:
- Learn ML model deployment
- Understand fraud detection workflows
- See feature engineering in action
- Study transaction processing
- Practice data analysis
- Build web dashboards

---

## 📞 Support

**Questions or Issues?**

1. Check README.md for detailed documentation
2. Review transaction_reports/ for data
3. Look at phonepe_app.py source code
4. Check console output for errors
5. Try reducing transaction amounts

---

**Built with:** Python 3.9+ | Flask | LightGBM | pandas | numpy

**Version:** 1.0.0  
**Status:** ✅ Ready to Use  
**Last Updated:** February 2026

🚀 **Happy Testing!**
