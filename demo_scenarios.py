"""
PhonePe Fraud Detection - Quick Start Test Script
Demonstrates different fraud scenarios and patterns
"""

from phonepe_app import PhonePeApp
import random

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def run_scenario(app, scenario_name, transactions):
    """Run a specific fraud scenario"""
    print_section(scenario_name)
    
    for sender_id, receiver_id, amount, description in transactions:
        print(f"\n📌 {description}")
        txn, analysis = app.process_transaction(sender_id, receiver_id, amount, 10)
        
        if txn:
            print(f"   Transaction: {txn.txn_id}")
            print(f"   Sender: {txn.sender.name:20} | Receiver: {txn.receiver.name:20}")
            print(f"   Amount: ₹{amount:>6,.0f} | Fraud Score: {analysis['fraud_score']:>6.4f}")
            print(f"   Sender Risk: {analysis['sender_risk']:>4} | Receiver Risk: {analysis['receiver_risk']:>4}")
            print(f"   Status: {analysis['action']}")
        else:
            print(f"   ❌ Error: {analysis.get('error', 'Unknown')}")

def main():
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║          🏦 PhonePe Fraud Detection Engine - Comprehensive Demo           ║
    ║                                                                            ║
    ║  Real-world UPI payment application with ML-powered fraud detection      ║
    ║  Built on 4M+ fraud cases with behavioral pattern analysis               ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize app
    app = PhonePeApp()
    app.create_user_profiles()
    
    # ============================================================================
    # SCENARIO 1: Normal Legitimate Transactions
    # ============================================================================
    legitimate_txns = [
        ("USER_001", "USER_002", 500, "Normal UPI payment - Regular user paying friend"),
        ("USER_002", "USER_003", 1500, "Utility bill payment - Moderate amount"),
        ("USER_003", "USER_001", 2000, "Salary contribution - Monthly payment"),
        ("USER_004", "USER_005", 800, "Small purchase - Online shopping"),
    ]
    run_scenario(app, "SCENARIO 1: Legitimate User Transactions", legitimate_txns)
    
    # ============================================================================
    # SCENARIO 2: Fraudster Attempting High-Value Theft
    # ============================================================================
    fraudster_txns = [
        ("FRAUD_001", "USER_002", 3000, "⚠️  Fraudster sending amount - Bot attack pattern"),
        ("FRAUD_002", "USER_003", 4000, "⚠️  Known fraudster attempting transfer - Unusual amount"),
        ("FRAUD_003", "USER_005", 4500, "⚠️  Card cloner attempting theft - Very suspicious"),
    ]
    run_scenario(app, "SCENARIO 2: Known Fraudsters Attempting Attacks", fraudster_txns)
    
    # ============================================================================
    # SCENARIO 3: Legitimate User Paying Fraudster (Risky)
    # ============================================================================
    risky_legitimate_txns = [
        ("USER_001", "FRAUD_004", 3000, "⚠️  Legitimate user → Known fraudster - Scam victim?"),
        ("USER_004", "FRAUD_001", 5000, "⚠️  Legitimate user → Fraudster account - Payment to scammer"),
    ]
    run_scenario(app, "SCENARIO 3: Legitimate Users Sending to Fraudsters", risky_legitimate_txns)
    
    # ============================================================================
    # SCENARIO 4: Rapid Transaction Attempts (Velocity Fraud)
    # ============================================================================
    print_section("SCENARIO 4: Rapid Transaction Attempts (Velocity Attack)")
    print("\n📌 Simulating rapid-fire transactions from same sender...")
    
    for i in range(3):
        sender_id = "FRAUD_002"
        receiver_id = ["USER_001", "USER_002", "USER_003"][i]
        amount = 1000 + i * 500
        
        print(f"\n   Attempt {i+1}/3:")
        txn, analysis = app.process_transaction(sender_id, receiver_id, amount, 10)
        if txn:
            print(f"   Transaction: {txn.txn_id}")
            print(f"   Fraud Score: {analysis['fraud_score']:.4f}")
            print(f"   Status: {analysis['action']}")
        else:
            print(f"   Error: {analysis.get('error', 'Unknown error')}")
    
    # ============================================================================
    # SCENARIO 5: Mixed Legitimate Transactions
    # ============================================================================
    mixed_txns = [
        ("USER_001", "USER_004", 1200, "Normal friend payment - Low risk"),
        ("USER_005", "USER_002", 3000, "Vendor payment - Regular commerce"),
        ("USER_003", "USER_005", 2500, "Rental payment - Known pattern"),
    ]
    run_scenario(app, "SCENARIO 5: More Legitimate Transactions", mixed_txns)
    
    # ============================================================================
    # FINAL SUMMARY AND ANALYSIS
    # ============================================================================
    print_section("FINAL FRAUD DETECTION SUMMARY")
    
    total_txns = len(app.transactions)
    successful = sum(1 for t in app.transactions if t.status == "SUCCESS")
    rejected = sum(1 for t in app.transactions if t.status == "REJECTED")
    
    fraudster_txns = [t for t in app.transactions if t.sender.is_fraudster or t.receiver.is_fraudster]
    caught = sum(1 for t in fraudster_txns if t.is_flagged)
    
    print(f"\n📊 TRANSACTION STATISTICS")
    print(f"   Total Transactions Processed:  {total_txns}")
    print(f"   Successful Transactions:       {successful}")
    print(f"   Rejected (Fraud Detected):     {rejected}")
    print(f"   Success Rate:                  {(successful/total_txns*100):.2f}%")
    
    print(f"\n🔒 FRAUD DETECTION PERFORMANCE")
    print(f"   Known Fraudster Transactions:  {len(fraudster_txns)}")
    print(f"   Fraud Caught:                  {caught}/{len(fraudster_txns)}")
    print(f"   Detection Rate:                {(caught/len(fraudster_txns)*100 if fraudster_txns else 0):.2f}%")
    
    total_amount = sum(t.amount for t in app.transactions)
    blocked_amount = sum(t.amount for t in app.transactions if t.is_flagged)
    
    print(f"\n💰 FINANCIAL IMPACT")
    print(f"   Total Amount Processed:        ₹{total_amount:,.2f}")
    print(f"   Amount Blocked (Protected):    ₹{blocked_amount:,.2f}")
    print(f"   Percentage Protected:          {(blocked_amount/total_amount*100 if total_amount > 0 else 0):.2f}%")
    
    print(f"\n👥 USER STATISTICS")
    for user_id, user in sorted(app.users.items()):
        user_txns = [t for t in app.transactions if t.sender == user]
        risk = "⚠️  HIGH RISK" if user.is_fraudster else "✅ SAFE"
        print(f"   {user.name:20} {risk:15} | Balance: ₹{user.balance:>8,.0f} | Sent: ₹{sum(t.amount for t in user_txns):>8,.0f}")
    
    # ============================================================================
    # DETAILED TRANSACTION LOG
    # ============================================================================
    print_section("DETAILED TRANSACTION LOG")
    
    print(f"\n{'TXN_ID':<10} {'SENDER':<20} {'→':<1} {'RECEIVER':<20} {'AMOUNT':>8} {'SCORE':>8} {'STATUS':<12}")
    print("-" * 80)
    
    for txn in app.transactions:
        status_icon = "✅" if txn.status == "SUCCESS" else "❌"
        print(f"{txn.txn_id:<10} {txn.sender.name:<20} → {txn.receiver.name:<20} ₹{txn.amount:>7,.0f} {txn.fraud_score:>8.4f} {status_icon} {txn.status:<10}")
    
    # ============================================================================
    # FRAUD PATTERNS IDENTIFIED
    # ============================================================================
    print_section("FRAUD PATTERNS ANALYSIS")
    
    print("\n🚨 KEY FRAUD INDICATORS DETECTED:")
    
    high_amount_txns = [t for t in app.transactions if t.amount > 8000]
    if high_amount_txns:
        print(f"\n   • HIGH AMOUNT TRANSACTIONS ({len(high_amount_txns)}):")
        for t in high_amount_txns:
            print(f"     - {t.txn_id}: {t.sender.name} → {t.receiver.name}, ₹{t.amount:,} [Score: {t.fraud_score:.4f}]")
    
    from collections import defaultdict
    sender_counts = defaultdict(list)
    for t in app.transactions:
        sender_counts[t.sender.user_id].append(t)
    
    rapid_txns = {uid: txns for uid, txns in sender_counts.items() if len(txns) > 2}
    if rapid_txns:
        print(f"\n   • RAPID TRANSACTION ATTEMPTS ({len(rapid_txns)} users):")
        for uid, txns in rapid_txns.items():
            user = app.users[uid]
            print(f"     - {user.name}: {len(txns)} transactions")
    
    fraud_users = [u for u in app.users.values() if u.is_fraudster]
    if fraud_users:
        print(f"\n   • KNOWN FRAUDSTER ACCOUNTS ({len(fraud_users)}):")
        for u in fraud_users:
            user_txns = [t for t in app.transactions if t.sender == u or t.receiver == u]
            blocked = sum(1 for t in user_txns if t.is_flagged)
            print(f"     - {u.name}: {len(user_txns)} transactions, {blocked} blocked")
    
    # Save comprehensive report
    print_section("SAVING REPORTS")
    
    import os
    os.makedirs("transaction_reports", exist_ok=True)
    
    df = app.generate_transaction_report()
    df.to_csv("transaction_reports/demo_transactions.csv", index=False)
    print("\n✅ Transaction report saved: transaction_reports/demo_transactions.csv")
    
    print("\n" + "="*80)
    print("  ✨ Demo Complete! Check transaction_reports/ for detailed analysis")
    print("="*80)

if __name__ == "__main__":
    main()
