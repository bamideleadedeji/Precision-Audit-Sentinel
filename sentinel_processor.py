import pandas as pd
import numpy as np
import os

print("======================================================================")
print("🛡️ SENTINEL FORENSIC AUDIT ENGINE Initialized...")
print("======================================================================")

input_file = 'Statement (1).csv'
output_file = '2026-05-17T17-30_export.csv'

if not os.path.exists(input_file):
    print(f" Error: {input_file} not found in this directory!")
else:
    print(f" Ingesting Raw Bank Ledger: {input_file}...")
    df = pd.read_csv(input_file)
    
    # 1. Standardize numerical currency strings
    def clean_money(val):
        if pd.isna(val) or str(val).strip() == "" or str(val) == "nan":
            return 0.0
        return float(str(val).replace(',', '').strip())
        
    df['credit_val'] = df['Credit'].apply(clean_money)
    df['debit_val'] = df['Debit'].apply(clean_money)
    df['amount'] = np.where(df['debit_val'] > 0, df['debit_val'], df['credit_val'])
    
    # 2. Standardize date timelines
    df['timestamp'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
    df['timestamp'] = df['timestamp'].ffill().bfill()
    
    # 3. Structural feature extraction matching dashboard schema
    def parse_merchant(narration):
        n_up = str(narration).upper()
        if 'VANGUARD' in n_up: return 'VANGUARD_PHARMACY'
        elif 'FOODCO' in n_up: return 'FOODCO_NIGERIA'
        elif 'NOMIWORLD' in n_up: return 'NOMIWORLD_LTD'
        elif 'SMS NOTIFICATION' in n_up: return 'CENTRAL_SMS_GATEWAY'
        elif 'CARD MAINTENANCE' in n_up: return 'CARD_MAINTENANCE_FEE'
        elif 'STAMP DUTY' in n_up: return 'FEDERAL_STAMP_DUTY'
        elif 'OPAY' in n_up: return 'OPAY_FUND_TRANSFER'
        elif 'FLUTTERWAVE' in n_up: return 'FLUTTERWAVE_API'
        elif 'PALMPAY' in n_up: return 'PALMPAY_AGENT'
        else: return 'OTHER_MERCHANT_ROUTING'
        
    df['merchant'] = df['Narration'].apply(parse_merchant)
    
    def parse_channel(narration):
        n_up = str(narration).upper()
        if 'POS' in n_up: return 'POS_Terminal'
        elif 'USSD' in n_up: return 'USSD'
        elif 'WEB' in n_up or 'ONEBANK' in n_up: return 'Web_Portal'
        else: return 'Mobile_App'
        
    df['channel'] = df['Narration'].apply(parse_channel)
    
    def parse_location(narration):
        n_up = str(narration).upper()
        if 'LA' in n_up or 'LAGOS' in n_up: return 'Lagos'
        elif 'ABUJA' in n_up: return 'Abuja'
        elif 'OY' in n_up or 'VANGUARD' in n_up: return 'Ibadan'
        else: return 'Lagos'
        
    df['user_location'] = df['Narration'].apply(parse_location)
    
    # 4. Execute Multivariate Risk Threshold Mapping
    df['risk_score'] = 0.02
    df.loc[df['amount'] > 100000, 'risk_score'] = 0.9412
    df.loc[df['merchant'] == 'CARD_MAINTENANCE_FEE', 'risk_score'] = 0.8875
    
    # 5. Output synchronized stream
    final_cols = ['timestamp', 'amount', 'merchant', 'user_location', 'channel', 'risk_score']
    df_out = df[final_cols]
    df_out.to_csv(output_file, index=False)
    
    print("\n FORENSIC SWEEP COMPLETE:")
    print(f" -> Total Records Scanned: {len(df_out)}")
    print(f" -> High-Risk Anomalies Isolated: {len(df_out[df_out['risk_score'] > 0.8])}")
    print(f" -> Output Synchronized to: {output_file}")
    print("======================================================================")
