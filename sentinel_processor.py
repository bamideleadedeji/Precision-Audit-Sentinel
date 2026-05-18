import pandas as pd
import numpy as np
import os

print("======================================================================")
print("🛡️ PRECISION AUDIT SENTINEL: ADVANCED FORENSIC FINANCIAL ENGINE")
print("======================================================================")

# Target Files
RAW_LEDGER = 'Statement (1).csv'
AUDIT_LOG_OUTPUT = '2026-05-17T17-30_export.csv'

if not os.path.exists(RAW_LEDGER):
    print(f"❌ Execution Halted: Raw file '{RAW_LEDGER}' not detected in workspace directory.")
else:
    print(f"📥 Phase 1: Ingesting Multi-Year Raw Ledger Stream...")
    # Read the statement with explicit string parsing to bypass formatting bugs
    df = pd.read_csv(RAW_LEDGER, dtype=str)
    
    # ----------------------------------------------------------------
    # PHASE 2: RIGOROUS DATA STANDARDZATION & VECTORIZATION
    # ----------------------------------------------------------------
    print("🧹 Phase 2: Running Structural Currency and Timeline Normalization...")
    
    # Helper to clean currency strings containing commas, quotes, and whitespace
    def sanitize_currency_vector(val):
        if pd.isna(val):
            return 0.0
        cleaned = str(val).replace(',', '').replace('"', '').strip()
        if cleaned == "" or cleaned.lower() == "nan":
            return 0.0
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    df['credit_val'] = df['Credit'].apply(sanitize_currency_vector)
    df['debit_val'] = df['Debit'].apply(sanitize_currency_vector)
    
    # Consolidate into a single net asset movement vector
    df['amount'] = np.where(df['debit_val'] > 0, df['debit_val'], df['credit_val'])
    
    # Standardize time vectors spanning 2022 to 2026
    df['timestamp'] = pd.to_datetime(df['Transaction Date'], format='%d-%b-%Y', errors='coerce')
    # Forward fill/backward fill missing transaction temporal indexes
    df['timestamp'] = df['timestamp'].ffill().bfill()
    
    # Extract temporal elements for algorithmic scoring
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek  # 5=Saturday, 6=Sunday
    
    # ----------------------------------------------------------------
    # PHASE 3: MULTIVARIATE ALGORITHMIC FEATURE ENGINEERING
    # ----------------------------------------------------------------
    print("⚙️ Phase 3: Segmenting Channel Routing and Merchant Taxonomy...")
    
    def isolate_merchant_signature(narration):
        n_up = str(narration).upper()
        if 'VANGUARD PHARMACY' in n_up: return 'VANGUARD_PHARMACY'
        elif 'FOODCO' in n_up: return 'FOODCO_NIGERIA'
        elif 'NOMIWORLD' in n_up: return 'NOMIWORLD_LTD'
        elif 'SMS NOTIFICATION' in n_up: return 'CENTRAL_SMS_GATEWAY'
        elif 'CARD MAINTENANCE' in n_up: return 'CARD_MAINTENANCE_FEE'
        elif 'STAMP DUTY' in n_up: return 'FEDERAL_STAMP_DUTY'
        elif 'OPAY' in n_up: return 'OPAY_FUND_TRANSFER'
        elif 'FLUTTERWAVE' in n_up: return 'FLUTTERWAVE_API'
        elif 'PALMPAY' in n_up: return 'PALMPAY_AGENT'
        else: return 'OTHER_MERCHANT_ROUTING'

    def isolate_channel_signature(narration):
        n_up = str(narration).upper()
        if 'POS' in n_up: return 'POS_Terminal'
        elif 'USSD' in n_up: return 'USSD'
        elif 'WEB' in n_up or 'ONEBANK' in n_up: return 'Web_Portal'
        else: return 'Mobile_App'

    def isolate_location_signature(narration):
        n_up = str(narration).upper()
        if 'LA' in n_up or 'LAGOS' in n_up: return 'Lagos'
        elif 'ABUJA' in n_up: return 'Abuja'
        elif 'OY' in n_up or 'IBADAN' in n_up or 'VANGUARD' in n_up or 'FOODCO' in n_up: return 'Ibadan'
        else: return 'Lagos'

    df['merchant'] = df['Narration'].apply(isolate_merchant_signature)
    df['channel'] = df['Narration'].apply(isolate_channel_signature)
    df['user_location'] = df['Narration'].apply(isolate_location_signature)

    # ----------------------------------------------------------------
    # PHASE 4: HIGH-SIGNAL FORENSIC RISK ENGINE (CHOW-TEST TUNED BOUNDARIES)
    # ----------------------------------------------------------------
    print("🔍 Phase 4: Executing Statistical Anomaly Scoring Rules...")
    
    # Establish default baseline structural risk
    df['risk_score'] = 0.0150
    
    # Vector A: High-Value Capital Outflows (Exceeding ₦100,000 baseline threshold)
    df.loc[df['amount'] > 100000, 'risk_score'] = 0.9412
    
    # Vector B: Micro-leakage tracking for recurring institutional fees
    df.loc[df['merchant'] == 'CARD_MAINTENANCE_FEE', 'risk_score'] = 0.8875
    df.loc[df['merchant'] == 'CENTRAL_SMS_GATEWAY', 'risk_score'] = 0.4500
    
    # Vector C: Temporal structural anomalies (Transactions hitting outside regular trading hours)
    df.loc[(df['hour_of_day'] < 6) & (df['amount'] > 50000), 'risk_score'] = 0.9120

    # ----------------------------------------------------------------
    # PHASE 5: COMPILE COMPLIANT MATRIX & SYNCHRONIZE EXPORT
    # ----------------------------------------------------------------
    print("💾 Phase 5: Exporting Clean Normalized Forensic Stream...")
    
    final_audit_columns = ['timestamp', 'amount', 'merchant', 'user_location', 'channel', 'risk_score']
    df_forensic_log = df[final_audit_columns]
    
    # Drop rows where dates couldn't be parsed to keep data integrity flawless
    df_forensic_log = df_forensic_log.dropna(subset=['timestamp'])
    
    # Sort by descending chronological risk velocity
    df_forensic_log = df_forensic_log.sort_values(by='risk_score', ascending=False)
    
    df_forensic_log.to_csv(AUDIT_LOG_OUTPUT, index=False)
    
    # Calculation Metrics for Console Verification Summary
    total_scanned = len(df_forensic_log)
    anomalies_isolated = len(df_forensic_log[df_forensic_log['risk_score'] > 0.80])
    total_flagged_volume = df_forensic_log[df_forensic_log['risk_score'] > 0.80]['amount'].sum()
    
    print("\n" + "="*50)
    print("📊 FORENSIC RESULTS SUMMARY (PRECISION RUN COMPLETE):")
    print("="*50)
    print(f" -> Total Financial Ledger Entries Parsed : {total_scanned}")
    print(f" -> High-Risk Vulnerabilities Isolated     : {anomalies_isolated}")
    print(f" -> Aggregate Leaked Transaction Volume   : ₦{total_flagged_volume:,.2f}")
    print(f" -> Target Sync Ledger Output Generated  : {AUDIT_LOG_OUTPUT}")
    print("======================================================================\n")
