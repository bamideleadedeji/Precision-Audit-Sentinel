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
            print(" Available files in this workspace are:")
            print(os.listdir('.'))
            return

        print(f" Phase 1: Ingesting Raw Ledger Stream from: '{file_target}'")
        df_raw = pd.read_csv(file_target, dtype=str)

        # --- PHASE 2: CURRENCY AND STRING DESERIALIZATION ---
        print("扫 Phase 2: Converting Financial Columns into Numeric Floats...")
        # Clean currency characters if present
        if 'amount' in df_raw.columns:
            df_raw['amount'] = df_raw['amount'].str.replace(r'[^\d\.]', '', regex=True)
            df_raw['amount'] = pd.to_numeric(df_raw['amount'], errors='coerce').fillna(0.0)
        else:
            df_raw['amount'] = 0.0

        # --- PHASE 3 & 4: FORENSIC TAXONOMY PARSING & RISK SCORING ---
        print(" Phase 3 & 4: Running Decision Matrix Filters and Evaluating Risk...")
        
        # Ensure structural tracking columns exist
        if 'merchant' not in df_raw.columns:
            df_raw['merchant'] = 'OTHER_MERCHANT_ROUTING'
        if 'channel' not in df_raw.columns:
            df_raw['channel'] = 'Mobile_App'
        if 'user_location' not in df_raw.columns:
            df_raw['user_location'] = 'LAGOS_NGR'
        if 'timestamp' not in df_raw.columns:
            df_raw['timestamp'] = '2026-05-17 17:30:00'

        # Default standard baseline risk
        df_raw['risk_score'] = 0.1500

        # High-Value Risk Thresholds
        df_raw.loc[df_raw['amount'] >= 100000, 'risk_score'] = 0.9412

        # Advanced Token / Accrued Regulation Filters (Rule Gamma)
        if 'narration' in df_raw.columns:
            df_raw['narration'] = df_raw['narration'].fillna('').str.upper()
            df_raw.loc[df_raw['narration'].str.contains('SMS|OTP|CHARGE|FEE'), 'risk_score'] = 0.8200
            df_raw.loc[df_raw['narration'].str.contains('PENDING|ACCRUED'), 'risk_score'] = 0.7500

        # --- PHASE 6: MATRIX CONSOLIDATION & LOCAL FILE SAVE ---
        output_matrix_name = '2026-05-17T17-30_export.csv'
        final_reporting_schema = ['timestamp', 'amount', 'merchant', 'user_location', 'channel', 'risk_score']
        
        # Intercept columns that exist to prevent out-of-bounds key errors
        available_schema = [col for col in final_reporting_schema if col in df_raw.columns]
        df_final_report = df_raw[available_schema].sort_values(by='risk_score', ascending=False)
        
        df_final_report.to_csv(output_matrix_name, index=False)
        print(f" Success: Audit asset generated and saved as {output_matrix_name}")

# --- AUTO-TRIGGER RUN EXECUTION LOOP ---
if __name__ == "__main__":
    sentinel_instance = UniversalSentinelEngine(client_type="individual")
    sentinel_instance.process_transaction_ledger('Statement (1).csv')
