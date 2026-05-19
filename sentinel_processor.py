import os
import pandas as pd
import numpy as np

class UniversalSentinelEngine:
    def __init__(self, client_type="individual"):
        self.client_type = client_type
        print("======================================================================")
        print("🛡️ PRECISION AUDIT SENTINEL: UNIVERSAL NIGERIAN FINTECH AUDIT CORE")
        print("======================================================================")

    def process_transaction_ledger(self, file_target):
        # --- PHASE 1: FAULT-TOLERANT INGESTION CHECK ---
        if not os.path.exists(file_target):
            print(f" CRITICAL ERROR: Target ledger file '{file_target}' was NOT found!")
            return

        print(f" Phase 1: Ingesting Raw Ledger Stream from: '{file_target}'")
        df_raw = pd.read_csv(file_target, dtype=str)

        # --- PHASE 2: ALIGN COLUMNS WITH NIGERIAN BANK SCHEMA ---
        print(" Phase 2: Mapping columns and converting financial streams to floats...")
        
        # Clean and combine Debit/Credit streams into a single Amount field
        for col in ['Debit', 'Credit', 'amount']:
            if col in df_raw.columns:
                df_raw[col] = df_raw[col].str.replace(r'[^\d\.]', '', regex=True)
                df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce').fillna(0.0)

        if 'amount' not in df_raw.columns:
            # If explicit amount doesn't exist, compute it from bank statement streams
            df_raw['amount'] = df_raw['Debit'] + df_raw['Credit']

        # Map dates to standard schema
        if 'Transaction Date' in df_raw.columns:
            df_raw['timestamp'] = df_raw['Transaction Date']
        else:
            df_raw['timestamp'] = '2026-05-17 17:30:00'

        # --- PHASE 3 & 4: FORENSIC TAXONOMY PARSING & RISK SCORING ---
        print(" Phase 3 & 4: Running Decision Matrix Filters and Evaluating Risk...")
        
        # Build clean taxonomic fields
        df_raw['merchant'] = 'OTHER_MERCHANT_ROUTING'
        df_raw['channel'] = 'Mobile_App'
        df_raw['user_location'] = 'LAGOS_NGR'
        df_raw['risk_score'] = 0.1500

        if 'Narration' in df_raw.columns:
            df_raw['Narration'] = df_raw['Narration'].fillna('').str.upper()
            
            # Channel Extraction
            df_raw.loc[df_raw['Narration'].str.contains('USSD'), 'channel'] = 'USSD'
            df_raw.loc[df_raw['Narration'].str.contains('POS|TERMINAL'), 'channel'] = 'POS_Terminal'
            df_raw.loc[df_raw['Narration'].str.contains('WEB|PORTAL|INTERNET'), 'channel'] = 'Web_Portal'
            
            # Merchant Routing Taxonomy
            df_raw.loc[df_raw['Narration'].str.contains('OPAY'), 'merchant'] = 'OPAY_FUND_TRANSFER'
            df_raw.loc[df_raw['Narration'].str.contains('VANGUARD'), 'merchant'] = 'VANGUARD_PHARMACY'
            
            # Advanced Risk Rule Gamma (Intercepting Fees and Accrued charges)
            df_raw.loc[df_raw['Narration'].str.contains('SMS|OTP|CHARGE|FEE|STAMP DUTY'), 'risk_score'] = 0.8200
            df_raw.loc[df_raw['Narration'].str.contains('PENDING|ACCRUED'), 'risk_score'] = 0.7500

        # High-Value Transaction Isolation Threshold
        df_raw.loc[df_raw['amount'] >= 100000, 'risk_score'] = 0.9412

        # --- PHASE 6: MATRIX CONSOLIDATION & LOCAL FILE SAVE ---
        output_matrix_name = '2026-05-17T17-30_export.csv'
        final_reporting_schema = ['timestamp', 'amount', 'merchant', 'user_location', 'channel', 'risk_score']
        
        df_final_report = df_raw[final_reporting_schema].sort_values(by='risk_score', ascending=False)
        df_final_report.to_csv(output_matrix_name, index=False)
        print(f" Success: Deep forensic asset generated and saved as {output_matrix_name}")

# --- AUTO-TRIGGER RUN EXECUTION LOOP ---
if __name__ == "__main__":
    sentinel_instance = UniversalSentinelEngine(client_type="individual")
    sentinel_instance.process_transaction_ledger('Statement (1).csv')
