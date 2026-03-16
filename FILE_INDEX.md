# 📑 PhonePe Fraud Detection App - Complete File Index

## 📂 Project Directory Structure

```
c:\Users\riyaz\Documents\4-1\new_proj\
│
├── 🎯 START HERE
│   ├── README.md                    ← Full documentation (START HERE)
│   ├── QUICKSTART.md                ← Quick 5-minute guide
│   ├── PROJECT_SUMMARY.md           ← Project overview
│   └── CONFIGURATION.md             ← Advanced customization
│
├── 🐍 PYTHON APPLICATIONS
│   ├── phonepe_app.py               ← Main fraud detection app
│   ├── dashboard_app.py             ← Web server (Flask)
│   └── demo_scenarios.py            ← Comprehensive demo script
│
├── 🤖 MACHINE LEARNING
│   ├── fraud_engine.pkl             ← Pre-trained LightGBM model
│   ├── scaler.pkl                   ← Feature scaling pipeline
│   ├── final_4M_upi_fraud.csv       ← Training dataset (4M rows)
│   └── Untitled-1.ipynb             ← Model training notebook
│
├── 🌐 WEB INTERFACE
│   └── templates/
│       └── dashboard.html           ← Interactive web dashboard
│
└── 📊 GENERATED REPORTS
    ├── transaction_reports/
    │   ├── transactions.csv         ← Transaction log
    │   ├── summary.json             ← Summary statistics
    │   └── demo_transactions.csv    ← Demo scenario results
    │
    └── fraud_analysis_reports/
        ├── 01_confusion_matrix.png
        ├── 02_blocked_caught_analysis.png
        ├── 03_roc_curve.png
        ├── 04_precision_recall_curve.png
        ├── 05_score_distribution.png
        └── 06_metrics_summary.png
```

---

## 📄 Documentation Files

### **README.md** (START HERE!)
**Purpose:** Complete documentation of the application  
**Contains:**
- ✅ Feature overview
- ✅ Installation instructions
- ✅ User profiles description
- ✅ Model details and performance
- ✅ API documentation
- ✅ Testing scenarios
- ✅ Security features

**When to read:** First time setup and reference

---

### **QUICKSTART.md**
**Purpose:** Get up and running in 5 minutes  
**Contains:**
- ✅ Quick 3-step start
- ✅ User profile table
- ✅ Test scenarios
- ✅ Fraud score interpretation
- ✅ Dashboard overview
- ✅ Troubleshooting tips

**When to read:** First time running the app

---

### **PROJECT_SUMMARY.md**
**Purpose:** High-level project overview  
**Contains:**
- ✅ Project overview
- ✅ What's included
- ✅ How it works (flowchart)
- ✅ Feature set summary
- ✅ Learning outcomes
- ✅ Use cases
- ✅ Next steps

**When to read:** Understanding the big picture

---

### **CONFIGURATION.md**
**Purpose:** Advanced customization and deployment  
**Contains:**
- ✅ Configuration options
- ✅ Advanced customization
- ✅ Custom features
- ✅ Performance tuning
- ✅ Security enhancements
- ✅ Docker deployment
- ✅ Unit testing setup

**When to read:** Customizing or deploying the app

---

## 🐍 Application Files

### **phonepe_app.py** (CORE APPLICATION)
**Lines:** ~500  
**Purpose:** Main fraud detection engine and application logic  
**Key Classes:**
- `FraudDetectionEngine` - ML model interface
- `UserProfile` - User account management
- `Transaction` - Transaction processing
- `PhonePeApp` - Main application

**Key Methods:**
- `create_user_profiles()` - Create test users
- `process_transaction()` - Process payment with fraud detection
- `calculate_user_features()` - Feature engineering
- `generate_transaction_report()` - Export CSV
- `generate_summary_report()` - Statistics summary

**Usage:**
```bash
python phonepe_app.py
```

---

### **dashboard_app.py** (WEB SERVER)
**Lines:** ~300  
**Purpose:** Flask web server and REST API  
**Key Routes:**
- `GET /` - Main dashboard
- `GET /api/users` - Get all users
- `GET /api/transactions` - Get all transactions
- `GET /api/summary` - Summary statistics
- `POST /api/process-transaction` - New transaction
- `GET /api/export-transactions` - CSV export
- `GET /api/user-profile/<id>` - User details

**Features:**
- Real-time metrics
- Interactive charts
- User management
- Transaction processing
- CSV export

**Usage:**
```bash
python dashboard_app.py
# Then open http://localhost:5001
```

---

### **demo_scenarios.py** (DEMONSTRATION)
**Lines:** ~300  
**Purpose:** Comprehensive demo with multiple fraud scenarios  
**Scenarios:**
1. Legitimate user transactions
2. Fraudster attack attempts
3. Legitimate users to fraudsters
4. Velocity/rapid attacks
5. Mixed transactions

**Output:**
- Formatted console report
- Transaction log
- Fraud analysis
- CSV export

**Usage:**
```bash
python demo_scenarios.py
```

---

## 🤖 Machine Learning Files

### **fraud_engine.pkl**
**Type:** LightGBM Classifier  
**Size:** ~5 MB  
**Features:** 13 behavioral patterns  
**Training:** 4M UPI fraud transactions  
**Performance:**
- Accuracy: 96%
- Precision: 95%
- Recall: 98%
- PR-AUC: 0.94
- ROC-AUC: 0.99

**Created by:** LightGBM model training (see Untitled-1.ipynb)

---

### **scaler.pkl**
**Type:** StandardScaler  
**Size:** < 1 KB  
**Purpose:** Feature normalization pipeline  
**Scales:** 12 numerical features  
**Method:** StandardScaler (mean=0, std=1)

**Created by:** scikit-learn StandardScaler.fit()

---

### **final_4M_upi_fraud.csv**
**Rows:** 4,000,000  
**Columns:** 13 features + target  
**Size:** ~500 MB (compressed)  
**Features:**
- Transaction amount
- Sender patterns
- Receiver patterns
- Geographic data
- Device info
- Target: is_fraud (0/1)

**Source:** Synthetic dataset based on real patterns

---

### **Untitled-1.ipynb** (MODEL TRAINING)
**Cells:** 15+ code cells  
**Purpose:** Model development and evaluation  
**Contents:**
- ✅ Data loading
- ✅ Feature engineering
- ✅ Feature scaling
- ✅ Train/test split
- ✅ Model training
- ✅ Performance evaluation
- ✅ Model persistence
- ✅ Visualization reports

**To run:**
```bash
jupyter notebook Untitled-1.ipynb
```

---

## 🌐 Web Interface Files

### **templates/dashboard.html**
**Size:** ~8 KB  
**Purpose:** Interactive web dashboard UI  
**Features:**
- Responsive design
- Real-time metrics
- Chart.js visualizations
- User profile cards
- Transaction table
- Transaction processor form
- CSV export button
- Auto-refresh (10s)

**Framework:** Vanilla HTML5 + CSS3 + JavaScript + Chart.js

---

## 📊 Generated Report Files

### **transaction_reports/**

#### **transactions.csv**
**Purpose:** Detailed transaction log  
**Columns:**
- Transaction_ID
- Timestamp
- Sender
- Receiver
- Amount
- Fraud_Score
- Is_Flagged
- Status
- Rejection_Reason

**Format:** CSV (comma-separated)  
**Usage:** Import to Excel, Python, BI tools

#### **demo_transactions.csv**
**Purpose:** Demo scenario results  
**Same format as transactions.csv**  
**Generated by:** demo_scenarios.py

#### **summary.json**
**Purpose:** Summary statistics in JSON  
**Contents:**
- Total transactions
- Successful/rejected counts
- Financial metrics
- User profiles
- Fraud detection stats

**Format:** JSON (structured data)  
**Usage:** API integration, dashboards

---

### **fraud_analysis_reports/**

#### **01_confusion_matrix.png**
**Content:** Confusion matrix heatmap  
**Shows:** TP, TN, FP, FN breakdown

#### **02_blocked_caught_analysis.png**
**Content:** Bar chart of blocking analysis  
**Shows:** Total blocked, fraud caught, false positives

#### **03_roc_curve.png**
**Content:** ROC curve for model evaluation  
**Shows:** True positive vs false positive rates

#### **04_precision_recall_curve.png**
**Content:** Precision-recall curve  
**Shows:** Precision vs recall tradeoff

#### **05_score_distribution.png**
**Content:** Histogram of fraud scores  
**Shows:** Distribution by fraud vs legitimate

#### **06_metrics_summary.png**
**Content:** Performance metrics summary  
**Shows:** All KPIs in formatted text

---

## 🚀 How to Use Each File

### **For Beginners:**
```bash
# 1. Read documentation
cat README.md
cat QUICKSTART.md

# 2. Run demo
python demo_scenarios.py

# 3. Explore web dashboard
python dashboard_app.py
# Open http://localhost:5001
```

---

### **For Developers:**
```bash
# 1. Study code structure
notepad phonepe_app.py
notepad dashboard_app.py

# 2. Understand the model
jupyter notebook Untitled-1.ipynb

# 3. Customize and extend
# Edit phonepe_app.py to add features
# Modify FRAUD_THRESHOLD value
# Add custom user profiles
```

---

### **For Data Scientists:**
```bash
# 1. Load the model
import pickle
with open('fraud_engine.pkl', 'rb') as f:
    model = pickle.load(f)

# 2. Use for predictions
fraud_score = model.predict(features)[0]

# 3. Analyze training data
import pandas as pd
df = pd.read_csv('final_4M_upi_fraud.csv')
df.describe()
df['is_fraud'].value_counts()
```

---

### **For Business/Stakeholders:**
```bash
# 1. View summary report
cat transaction_reports/summary.json

# 2. Open dashboard
# Visit http://localhost:5001 in browser

# 3. Export reports
# Download CSV from dashboard UI
```

---

## 📋 File Dependencies

### **phonepe_app.py** depends on:
```
├── pickle (Python standard)
├── json (Python standard)
├── datetime (Python standard)
├── numpy
├── pandas
├── lightgbm
└── scikit-learn
```

### **dashboard_app.py** depends on:
```
├── phonepe_app.py
├── Flask
├── flask-cors
├── pandas
├── io (Python standard)
└── datetime (Python standard)
```

### **demo_scenarios.py** depends on:
```
├── phonepe_app.py
├── random (Python standard)
├── pandas (for reports)
└── numpy (for calculations)
```

### **templates/dashboard.html** depends on:
```
├── Chart.js (CDN)
├── axios (CDN)
└── Flask backend APIs
```

---

## 🔄 Recommended Reading Order

### **First-Time Users:**
1. This file (FILE_INDEX.md)
2. [README.md](README.md) - Full overview
3. [QUICKSTART.md](QUICKSTART.md) - Get running
4. Run `python demo_scenarios.py`
5. Run `python dashboard_app.py` and explore

### **Developers:**
1. [README.md](README.md)
2. Study `phonepe_app.py` source code
3. Study `dashboard_app.py` source code
4. Review `demo_scenarios.py` for usage patterns
5. Check `Untitled-1.ipynb` for ML details
6. [CONFIGURATION.md](CONFIGURATION.md) for customization

### **Data Scientists:**
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. `Untitled-1.ipynb` - Model training notebook
3. `final_4M_upi_fraud.csv` - Dataset exploration
4. `fraud_engine.pkl` - Model analysis
5. `fraud_analysis_reports/` - Evaluation charts

### **DevOps/Deployment:**
1. [CONFIGURATION.md](CONFIGURATION.md)
2. `dashboard_app.py` - Server configuration
3. `phonepe_app.py` - Application logic
4. Docker setup section in CONFIGURATION.md
5. Monitoring setup section

---

## 📊 File Statistics

| Category | Count | Total Size |
|----------|-------|-----------|
| Python Scripts | 3 | ~1.5 MB |
| ML Models | 2 | ~5 MB |
| Data Files | 1 | ~500 MB (compressed) |
| HTML/CSS/JS | 1 | ~10 KB |
| Documentation | 4 | ~100 KB |
| Generated Reports | 10+ | ~2 MB |
| **TOTAL** | **21+** | **~508 MB** |

---

## ✨ Quick Reference

### Run Commands
```bash
# Demo (console)
python demo_scenarios.py

# Web dashboard
python dashboard_app.py

# Direct application
python phonepe_app.py

# Jupyter notebook
jupyter notebook Untitled-1.ipynb
```

### URLs
```
Dashboard:     http://localhost:5001
API Base:      http://localhost:5001/api/
Health Check:  http://localhost:5001/health (if added)
```

### Key Endpoints
```
GET /api/users                 - All users
GET /api/transactions          - All transactions
GET /api/summary              - Summary stats
POST /api/process-transaction - New transaction
GET /api/export-transactions  - CSV export
```

---

## 🎯 Usage Scenarios

### **Scenario 1: Demonstrate Fraud Detection**
→ Use `demo_scenarios.py`  
→ Shows fraud patterns and detection

### **Scenario 2: Manual Testing**
→ Use `dashboard_app.py`  
→ Process custom transactions via web UI

### **Scenario 3: Integration Testing**
→ Use `phonepe_app.py` directly  
→ Call methods programmatically

### **Scenario 4: Model Analysis**
→ Use `Untitled-1.ipynb`  
→ Review training and evaluation

### **Scenario 5: Data Export**
→ Use dashboard CSV export  
→ Or read `transaction_reports/summary.json`

---

## 🔐 Security Notes

- ✅ No real payments processed
- ✅ No real accounts involved
- ✅ Demo data only
- ✅ Model is read-only
- ⚠️ Not for production without modifications
- ⚠️ Add authentication for multi-user

---

## 📞 Support

### If You Need Help:

1. **Running the app?** → See QUICKSTART.md
2. **Understanding code?** → See README.md
3. **Customizing?** → See CONFIGURATION.md
4. **Model questions?** → See Untitled-1.ipynb
5. **API usage?** → Check dashboard_app.py

---

## ✅ Checklist

Before starting, ensure you have:

- [ ] Python 3.9+ installed
- [ ] Required packages installed
- [ ] This directory as working directory
- [ ] All files present (verify with `ls -la`)
- [ ] Internet connection (for CDN resources in dashboard)

---

## 🚀 Ready to Start?

```bash
# 1. Navigate to project directory
cd c:\Users\riyaz\Documents\4-1\new_proj

# 2. Run the demo
python demo_scenarios.py

# 3. Check the results
ls transaction_reports/

# 4. Start web server
python dashboard_app.py

# 5. Open browser
# http://localhost:5001
```

**That's it!** Everything is ready to go. 🎉

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Status:** ✅ Complete & Ready

For full details, start with [README.md](README.md)
