"""
PhonePe Dashboard - Flask Web Application
Real-time fraud detection dashboard and transaction monitoring
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import pandas as pd
import io
from phonepe_app import PhonePeApp

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize the PhonePe application
phonepe = PhonePeApp()
phonepe.create_user_profiles()

# Run initial simulation
def run_initial_simulation():
    """Run some initial transactions for demo"""
    transactions = [
        ("USER_001", "USER_002", 500),
        ("USER_002", "USER_003", 1500),
        ("FRAUD_001", "USER_002", 10000),
        ("USER_001", "FRAUD_002", 5000),
        ("USER_003", "USER_001", 2000),
        ("FRAUD_003", "USER_005", 15000),
        ("USER_004", "USER_005", 800),
        ("USER_001", "USER_004", 1200),
    ]
    
    for sender_id, receiver_id, amount in transactions:
        phonepe.process_transaction(sender_id, receiver_id, amount, 10)

# Run initial simulation on startup
run_initial_simulation()


@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/users')
def get_users():
    """Get all users"""
    users_data = []
    for user_id, user in phonepe.users.items():
        users_data.append({
            'user_id': user.user_id,
            'name': user.name,
            'phone': user.phone,
            'balance': float(user.balance),
            'is_fraudster': user.is_fraudster,
            'total_txns': len(user.txn_history),
            'total_sent': float(user.total_amount_sent),
            'total_received': float(user.total_amount_received),
        })
    return jsonify(users_data)


@app.route('/api/transactions')
def get_transactions():
    """Get all transactions"""
    txn_data = []
    for txn in phonepe.transactions:
        txn_data.append({
            'txn_id': txn.txn_id,
            'timestamp': txn.timestamp.isoformat(),
            'sender': txn.sender.name,
            'sender_id': txn.sender.user_id,
            'receiver': txn.receiver.name,
            'receiver_id': txn.receiver.user_id,
            'amount': float(txn.amount),
            'fraud_score': float(txn.fraud_score),
            'is_flagged': txn.is_flagged,
            'status': txn.status,
            'geo_distance': float(txn.geo_distance_km),
        })
    return jsonify(txn_data)


@app.route('/api/summary')
def get_summary():
    """Get summary statistics"""
    total_txns = len(phonepe.transactions)
    successful_txns = sum(1 for t in phonepe.transactions if t.status == "SUCCESS")
    rejected_txns = sum(1 for t in phonepe.transactions if t.status == "REJECTED")
    
    total_amount = sum(t.amount for t in phonepe.transactions)
    blocked_amount = sum(t.amount for t in phonepe.transactions if t.is_flagged)
    
    fraudster_txns = [t for t in phonepe.transactions if t.sender.is_fraudster or t.receiver.is_fraudster]
    caught_fraud = sum(1 for t in fraudster_txns if t.is_flagged)
    
    return jsonify({
        'total_transactions': total_txns,
        'successful_transactions': successful_txns,
        'rejected_transactions': rejected_txns,
        'success_rate': (successful_txns/total_txns*100) if total_txns > 0 else 0,
        'total_amount': float(total_amount),
        'blocked_amount': float(blocked_amount),
        'percentage_blocked': (blocked_amount/total_amount*100) if total_amount > 0 else 0,
        'fraud_detected_count': caught_fraud,
        'false_alarms': sum(1 for t in phonepe.transactions if t.is_flagged and not (t.sender.is_fraudster or t.receiver.is_fraudster)),
    })


@app.route('/api/process-transaction', methods=['POST'])
def process_transaction():
    """Process a new transaction"""
    data = request.json
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    amount = float(data.get('amount', 0))
    geo_distance = float(data.get('geo_distance', 10))
    
    txn, analysis = phonepe.process_transaction(sender_id, receiver_id, amount, geo_distance)
    
    if txn is None:
        return jsonify({'error': analysis.get('error', 'Unknown error')}), 400
    
    return jsonify({
        'txn_id': txn.txn_id,
        'status': txn.status,
        'fraud_score': float(txn.fraud_score),
        'is_flagged': txn.is_flagged,
        'message': analysis.get('action', ''),
    })


@app.route('/api/export-transactions')
def export_transactions():
    """Export transactions as CSV"""
    df = phonepe.generate_transaction_report()
    
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )


@app.route('/api/fraud-patterns')
def get_fraud_patterns():
    """Get fraud pattern analysis"""
    patterns = {
        'high_amount_transactions': [],
        'rapid_transactions': [],
        'suspicious_receivers': [],
        'high_risk_senders': [],
    }
    
    # High amount transactions
    for txn in phonepe.transactions:
        if txn.amount > 8000:
            patterns['high_amount_transactions'].append({
                'txn_id': txn.txn_id,
                'sender': txn.sender.name,
                'receiver': txn.receiver.name,
                'amount': float(txn.amount),
                'is_flagged': txn.is_flagged,
            })
    
    # Rapid transactions (multiple in short time)
    from collections import defaultdict
    sender_txn_count = defaultdict(int)
    for txn in phonepe.transactions:
        sender_txn_count[txn.sender.user_id] += 1
    
    for user_id, count in sender_txn_count.items():
        if count > 2:
            user = phonepe.users[user_id]
            patterns['rapid_transactions'].append({
                'user_id': user_id,
                'user_name': user.name,
                'transaction_count': count,
            })
    
    # High risk senders (fraudsters)
    for user_id, user in phonepe.users.items():
        if user.is_fraudster:
            user_txns = [t for t in phonepe.transactions if t.sender == user]
            patterns['high_risk_senders'].append({
                'user_id': user_id,
                'user_name': user.name,
                'total_attempts': len(user_txns),
                'blocked_count': sum(1 for t in user_txns if t.is_flagged),
            })
    
    return jsonify(patterns)


@app.route('/api/user-profile/<user_id>')
def get_user_profile(user_id):
    """Get detailed user profile"""
    if user_id not in phonepe.users:
        return jsonify({'error': 'User not found'}), 404
    
    user = phonepe.users[user_id]
    user_txns = [t for t in phonepe.transactions if t.sender == user or t.receiver == user]
    
    return jsonify({
        'user_id': user.user_id,
        'name': user.name,
        'phone': user.phone,
        'balance': float(user.balance),
        'is_fraudster': user.is_fraudster,
        'created_at': user.created_at.isoformat(),
        'total_transactions': len(user_txns),
        'total_sent': float(user.total_amount_sent),
        'total_received': float(user.total_amount_received),
        'avg_transaction_amount': float(user.avg_txn_amount),
        'uses_vpn': user.uses_vpn,
        'recent_transactions': [
            {
                'txn_id': t.txn_id,
                'timestamp': t.timestamp.isoformat(),
                'type': 'sent' if t.sender == user else 'received',
                'counterparty': t.receiver.name if t.sender == user else t.sender.name,
                'amount': float(t.amount),
                'status': t.status,
            }
            for t in sorted(user_txns, key=lambda x: x.timestamp, reverse=True)[:10]
        ]
    })


if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5001)
