"""
PhonePe-like UPI Payment Application with Integrated Fraud Detection Engine
Real-world implementation with multiple user profiles and transaction processing
"""

import os
import pickle
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import random


class FraudDetectionEngine:
    """Load and use the pre-trained fraud detection model"""
    
    def __init__(self, model_path: str = "fraud_engine.pkl", scaler_path: str = "scaler.pkl"):
        """Initialize fraud detection engine with pre-trained model"""
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print("✅ Fraud Detection Engine Loaded Successfully")
            self.model_loaded = True
        except Exception as e:
            print(f"⚠️  Warning: Could not load fraud model: {e}")
            self.model_loaded = False
    
    def calculate_fraud_score(self, features: Dict) -> Tuple[float, bool]:
        """
        Calculate fraud score for a transaction.
        Returns: (fraud_score, is_fraud_flag)
        """
        if not self.model_loaded:
            return 0.0, False
        
        try:
            # Prepare features in the order expected by the model
            feature_names = [
                'amount', 's_avg_amount_5', 's_max_amount_5', 's_amount_std_5',
                's_time_gap_avg', 'r_amount_sum_24h', 'geo_distance_km',
                's_txn_count_10min', 's_txn_count_1h', 'r_txn_count_1h',
                'r_txn_count_24h', 'r_unique_senders_24h', 'vpn_proxy_flag'
            ]
            
            # Create feature vector
            X = np.array([[features.get(name, 0) for name in feature_names]])
            
            # Log transform skewed features
            log_features = [
                'amount', 's_avg_amount_5', 's_max_amount_5', 's_amount_std_5',
                'r_amount_sum_24h', 'geo_distance_km'
            ]
            for i, name in enumerate(feature_names):
                if name in log_features:
                    X[0, i] = np.log1p(X[0, i])
            
            # Scale features
            scale_cols = [
                'amount', 's_avg_amount_5', 's_max_amount_5', 's_amount_std_5',
                's_time_gap_avg', 'r_amount_sum_24h', 'geo_distance_km',
                's_txn_count_10min', 's_txn_count_1h', 'r_txn_count_1h',
                'r_txn_count_24h', 'r_unique_senders_24h'
            ]
            scale_indices = [i for i, name in enumerate(feature_names) if name in scale_cols]
            X_scaled = X.copy()
            X_scaled[0, scale_indices] = self.scaler.transform(X[0, scale_indices].reshape(1, -1))[0]
            
            # Get fraud probability
            fraud_prob = self.model.predict(X_scaled[0, :].reshape(1, -1))[0]
            is_fraud = fraud_prob > 0.98  # Threshold from model training
            
            return float(fraud_prob), bool(is_fraud)
        except Exception as e:
            print(f"⚠️  Error calculating fraud score: {e}")
            return 0.0, False


class UserProfile:
    """Represents a user profile with transaction history"""
    
    def __init__(self, user_id: str, name: str, phone: str, is_fraudster: bool = False):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.is_fraudster = is_fraudster
        self.balance = 50000 if not is_fraudster else 5000
        self.created_at = datetime.now() - timedelta(days=random.randint(30, 365))
        
        # Transaction history for feature calculation
        self.txn_history = []
        self.total_amount_sent = 0
        self.total_amount_received = 0
        
        # Fraud behavior patterns (if fraudster)
        if is_fraudster:
            self.avg_txn_amount = random.uniform(5000, 15000)  # Unusual amounts
            self.txn_frequency = random.uniform(5, 15)  # High frequency
            self.uses_vpn = True if random.random() > 0.3 else False
        else:
            self.avg_txn_amount = random.uniform(500, 3000)  # Normal amounts
            self.txn_frequency = random.uniform(1, 3)  # Normal frequency
            self.uses_vpn = False
    
    def get_profile_summary(self) -> Dict:
        """Get profile summary"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'phone': self.phone,
            'balance': self.balance,
            'is_fraudster': self.is_fraudster,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'total_transactions': len(self.txn_history),
            'total_sent': self.total_amount_sent,
            'total_received': self.total_amount_received,
        }


class Transaction:
    """Represents a single transaction"""
    
    def __init__(self, txn_id: str, sender: UserProfile, receiver: UserProfile, 
                 amount: float, geo_distance_km: float = 0):
        self.txn_id = txn_id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.geo_distance_km = geo_distance_km
        self.timestamp = datetime.now()
        self.fraud_score = 0.0
        self.is_flagged = False
        self.status = "PENDING"
        self.rejection_reason = None
    
    def __repr__(self) -> str:
        return f"Txn({self.txn_id}): {self.sender.name} -> {self.receiver.name} ₹{self.amount}"


class PhonePeApp:
    """Main PhonePe application with fraud detection"""
    
    def __init__(self):
        self.users: Dict[str, UserProfile] = {}
        self.transactions: List[Transaction] = []
        self.fraud_engine = FraudDetectionEngine()
        self.txn_counter = 0
    
    def create_user_profiles(self):
        """Create test user profiles with varied characteristics"""
        
        # Real/Legitimate Users
        legitimate_users = [
            ("USER_001", "Rajesh Kumar", "+91-9876543210", False),
            ("USER_002", "Priya Singh", "+91-9876543211", False),
            ("USER_003", "Amit Patel", "+91-9876543212", False),
            ("USER_004", "Neha Sharma", "+91-9876543213", False),
            ("USER_005", "Vikram Gupta", "+91-9876543214", False),
        ]
        
        # Fraudster Users (based on fraud patterns from model)
        fraudster_users = [
            ("FRAUD_001", "Dark Hacker", "+91-9999999999", True),
            ("FRAUD_002", "Scam Master", "+91-9898989898", True),
            ("FRAUD_003", "Card Cloner", "+91-9797979797", True),
            ("FRAUD_004", "Bot Network", "+91-9696969696", True),
        ]
        
        all_users = legitimate_users + fraudster_users
        
        for user_id, name, phone, is_fraudster in all_users:
            profile = UserProfile(user_id, name, phone, is_fraudster)
            self.users[user_id] = profile
        
        print("\n" + "="*70)
        print("📱 PHONEPE APPLICATION - USER PROFILES CREATED")
        print("="*70)
        
        print("\n✅ LEGITIMATE USERS:")
        for user_id in ["USER_001", "USER_002", "USER_003", "USER_004", "USER_005"]:
            user = self.users[user_id]
            print(f"  • {user.name:20} | {user.phone} | Balance: ₹{user.balance:,}")
        
        print("\n⚠️  FRAUDSTER USERS (High Risk):")
        for user_id in ["FRAUD_001", "FRAUD_002", "FRAUD_003", "FRAUD_004"]:
            user = self.users[user_id]
            print(f"  • {user.name:20} | {user.phone} | Balance: ₹{user.balance:,}")
    
    def calculate_user_features(self, user: UserProfile, role: str = "sender") -> Dict:
        """
        Calculate user features for fraud detection based on transaction history
        role: 'sender' or 'receiver'
        """
        now = datetime.now()
        
        # Get transaction history windows
        txns_10min = [t for t in user.txn_history if (now - t.timestamp).total_seconds() < 600]
        txns_1h = [t for t in user.txn_history if (now - t.timestamp).total_seconds() < 3600]
        txns_24h = [t for t in user.txn_history if (now - t.timestamp).total_seconds() < 86400]
        
        features = {}
        
        if role == "sender":
            # Sender features
            features['s_txn_count_10min'] = len(txns_10min)
            features['s_txn_count_1h'] = len(txns_1h)
            features['s_avg_amount_5'] = np.mean([t.amount for t in txns_1h[-5:]]) if txns_1h else 0
            features['s_max_amount_5'] = max([t.amount for t in txns_1h[-5:]]) if txns_1h else 0
            features['s_amount_std_5'] = np.std([t.amount for t in txns_1h[-5:]]) if len(txns_1h) > 1 else 0
            
            # Time gap average
            if len(txns_1h) > 1:
                time_gaps = [(txns_1h[i].timestamp - txns_1h[i+1].timestamp).total_seconds() 
                            for i in range(len(txns_1h)-1)]
                features['s_time_gap_avg'] = np.mean(time_gaps) if time_gaps else 0
            else:
                features['s_time_gap_avg'] = 0
        
        else:  # receiver
            # Receiver features
            features['r_txn_count_1h'] = len(txns_1h)
            features['r_txn_count_24h'] = len(txns_24h)
            features['r_amount_sum_24h'] = sum([t.amount for t in txns_24h]) if txns_24h else 0
            
            # Unique senders in 24h
            unique_senders = set([t.sender.user_id for t in txns_24h])
            features['r_unique_senders_24h'] = len(unique_senders)
        
        return features
    
    def process_transaction(self, sender_id: str, receiver_id: str, 
                          amount: float, geo_distance_km: float = 10) -> Tuple[Transaction, Dict]:
        """
        Process a transaction with fraud detection
        Returns: (transaction, fraud_analysis_dict)
        """
        self.txn_counter += 1
        txn_id = f"TXN_{self.txn_counter:06d}"
        
        if sender_id not in self.users or receiver_id not in self.users:
            return None, {"error": "Invalid sender or receiver"}
        
        sender = self.users[sender_id]
        receiver = self.users[receiver_id]
        
        # Check balance
        if sender.balance < amount:
            return None, {"error": f"Insufficient balance. Available: ₹{sender.balance}"}
        
        # Create transaction
        txn = Transaction(txn_id, sender, receiver, amount, geo_distance_km)
        
        # Calculate fraud detection features
        sender_features = self.calculate_user_features(sender, "sender")
        receiver_features = self.calculate_user_features(receiver, "receiver")
        
        # Combine features
        all_features = {
            'amount': amount,
            'geo_distance_km': geo_distance_km,
            'vpn_proxy_flag': 1 if sender.uses_vpn else 0,
        }
        all_features.update(sender_features)
        all_features.update(receiver_features)
        
        # Get fraud score
        fraud_score, is_fraud_flag = self.fraud_engine.calculate_fraud_score(all_features)
        txn.fraud_score = fraud_score
        txn.is_flagged = is_fraud_flag
        
        # Create detailed analysis
        fraud_analysis = {
            'fraud_score': fraud_score,
            'is_flagged': is_fraud_flag,
            'features': all_features,
            'sender_risk': 'HIGH' if sender.is_fraudster else 'LOW',
            'receiver_risk': 'HIGH' if receiver.is_fraudster else 'LOW',
        }
        
        # Process based on fraud flag
        if is_fraud_flag:
            txn.status = "REJECTED"
            txn.rejection_reason = "FRAUD_DETECTED"
            fraud_analysis['action'] = "TRANSACTION BLOCKED"
            print(f"🚨 FRAUD ALERT: {txn} - Score: {fraud_score:.4f}")
        else:
            # Process successful transaction
            sender.balance -= amount
            receiver.balance += amount
            txn.status = "SUCCESS"
            fraud_analysis['action'] = "TRANSACTION APPROVED"
            print(f"✅ SUCCESS: {txn} - Score: {fraud_score:.4f}")
        
        # Record in history
        sender.txn_history.append(txn)
        receiver.txn_history.append(txn)
        sender.total_amount_sent += amount
        receiver.total_amount_received += amount
        
        self.transactions.append(txn)
        
        return txn, fraud_analysis
    
    def generate_transaction_report(self) -> pd.DataFrame:
        """Generate report of all transactions"""
        data = []
        for txn in self.transactions:
            data.append({
                'Transaction_ID': txn.txn_id,
                'Timestamp': txn.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'Sender': txn.sender.name,
                'Receiver': txn.receiver.name,
                'Amount': txn.amount,
                'Fraud_Score': round(txn.fraud_score, 4),
                'Is_Flagged': txn.is_flagged,
                'Status': txn.status,
                'Reason': txn.rejection_reason or 'N/A',
            })
        
        return pd.DataFrame(data)
    
    def generate_summary_report(self) -> str:
        """Generate comprehensive summary report"""
        total_txns = len(self.transactions)
        successful_txns = sum(1 for t in self.transactions if t.status == "SUCCESS")
        rejected_txns = sum(1 for t in self.transactions if t.status == "REJECTED")
        
        total_amount = sum(t.amount for t in self.transactions)
        blocked_amount = sum(t.amount for t in self.transactions if t.is_flagged)
        
        # Fraud detection accuracy (based on actual fraudster transactions)
        fraudster_txns = [t for t in self.transactions if t.sender.is_fraudster or t.receiver.is_fraudster]
        caught_fraud = sum(1 for t in fraudster_txns if t.is_flagged)
        false_alarms = sum(1 for t in self.transactions if t.is_flagged and not (t.sender.is_fraudster or t.receiver.is_fraudster))
        
        report = f"""
{'='*80}
📊 PHONEPE FRAUD DETECTION SYSTEM - COMPREHENSIVE REPORT
{'='*80}

📈 TRANSACTION SUMMARY
{'-'*80}
Total Transactions Processed:     {total_txns}
Successful Transactions:          {successful_txns}
Rejected Transactions:            {rejected_txns}
Success Rate:                     {(successful_txns/total_txns*100 if total_txns > 0 else 0):.2f}%

💰 FINANCIAL IMPACT
{'-'*80}
Total Amount Processed:           ₹{total_amount:,.2f}
Amount Blocked (Fraud):           ₹{blocked_amount:,.2f}
Percentage Blocked:               {(blocked_amount/total_amount*100 if total_amount > 0 else 0):.2f}%

🔒 FRAUD DETECTION PERFORMANCE
{'-'*80}
Known Fraudster Transactions:     {len(fraudster_txns)}
Fraud Caught:                     {caught_fraud}
False Alarms (Legitimate Blocked): {false_alarms}
Fraud Detection Rate:             {(caught_fraud/len(fraudster_txns)*100 if fraudster_txns else 0):.2f}%

👥 USER STATISTICS
{'-'*80}
"""
        
        for user_id, user in sorted(self.users.items()):
            user_txns = [t for t in self.transactions if t.sender == user or t.receiver == user]
            sent = sum(t.amount for t in user_txns if t.sender == user and t.status == "SUCCESS")
            received = sum(t.amount for t in user_txns if t.receiver == user and t.status == "SUCCESS")
            
            risk_badge = "⚠️  [HIGH RISK]" if user.is_fraudster else "✅ [SAFE]"
            report += f"{user.name:20} {risk_badge:15} | Balance: ₹{user.balance:>8,.0f} | Sent: ₹{sent:>8,.0f} | Received: ₹{received:>8,.0f}\n"
        
        report += f"{'='*80}\n"
        
        return report


def run_simulation():
    """Run PhonePe application simulation"""
    
    app = PhonePeApp()
    app.create_user_profiles()
    
    print("\n" + "="*70)
    print("🔄 PROCESSING TRANSACTIONS WITH FRAUD DETECTION")
    print("="*70 + "\n")
    
    # Legitimate user transactions
    legitimate_transactions = [
        ("USER_001", "USER_002", 500),
        ("USER_002", "USER_003", 1500),
        ("USER_003", "USER_001", 2000),
        ("USER_004", "USER_005", 800),
        ("USER_001", "USER_004", 1200),
        ("USER_005", "USER_002", 3000),
    ]
    
    # Fraudster transactions (high risk patterns)
    fraudster_transactions = [
        ("FRAUD_001", "USER_002", 10000),  # High amount from fraudster
        ("USER_001", "FRAUD_002", 5000),   # Payment to fraudster
        ("FRAUD_003", "USER_005", 15000),  # High amount from fraudster
        ("FRAUD_004", "USER_003", 8000),   # Payment to fraudster
        ("USER_004", "FRAUD_001", 12000),  # High amount to fraudster
    ]
    
    # Mixed transactions
    mixed_transactions = [
        ("USER_002", "USER_004", 1000),
        ("USER_001", "FRAUD_004", 3000),   # Legitimate to fraudster (risky)
        ("FRAUD_002", "USER_003", 7000),   # Fraudster to legitimate (suspicious)
        ("USER_003", "USER_005", 2500),
    ]
    
    all_txns = legitimate_transactions + fraudster_transactions + mixed_transactions
    random.shuffle(all_txns)
    
    for sender_id, receiver_id, amount in all_txns:
        geo_distance = random.uniform(5, 500)  # Distance in km
        txn, analysis = app.process_transaction(sender_id, receiver_id, amount, geo_distance)
        print(f"   Fraud Score: {analysis.get('fraud_score', 0):.4f} | Status: {analysis.get('action', 'PENDING')}")
    
    # Generate and display reports
    print("\n" + app.generate_summary_report())
    
    # Transaction detail report
    print("\n" + "="*80)
    print("📋 DETAILED TRANSACTION LOG")
    print("="*80 + "\n")
    txn_df = app.generate_transaction_report()
    print(txn_df.to_string(index=False))
    
    # Save reports
    os.makedirs("transaction_reports", exist_ok=True)
    
    # Save transaction report as CSV
    txn_df.to_csv("transaction_reports/transactions.csv", index=False)
    print("\n✅ Transaction report saved to: transaction_reports/transactions.csv")
    
    # Save summary report as JSON
    summary_data = {
        'total_transactions': len(app.transactions),
        'successful_transactions': sum(1 for t in app.transactions if t.status == "SUCCESS"),
        'rejected_transactions': sum(1 for t in app.transactions if t.status == "REJECTED"),
        'total_amount': float(sum(t.amount for t in app.transactions)),
        'blocked_amount': float(sum(t.amount for t in app.transactions if t.is_flagged)),
        'users': {user_id: user.get_profile_summary() for user_id, user in app.users.items()},
    }
    
    with open("transaction_reports/summary.json", "w") as f:
        json.dump(summary_data, f, indent=2, default=str)
    print("✅ Summary report saved to: transaction_reports/summary.json")


if __name__ == "__main__":
    run_simulation()
