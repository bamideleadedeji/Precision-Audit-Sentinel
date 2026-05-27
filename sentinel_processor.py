import os
import re
import io
import pandas as pd
from pypdf import PdfReader

# Force the processor to read your fresh PDF file dynamically
PDF_INPUT_PATH = "client_dejifolakemi_enterprises.pdf"
CSV_OUTPUT_PATH = "client_dejifolakemi_enterprises_extracted_ledger.csv"

class UniversalSentinelEngine:
    def __init__(self):
        print("======================================================================")
        print("🛡️ UNIVERSAL PRECISION AUDIT SENTINEL: INSTITUTIONAL RECOVERY CORE")
        print("======================================================================")
        
        # Extended Taxonomic Dictionary for Nigerian Bank Charges Mapping
        self.charge_keywords = ['SMS', 'OTP', 'CHARGE', 'FEE', 'STAMP DUTY', 'VAT', 
                                'MAINTENANCE', 'ALERT', 'TOKEN', 'LEVY', 'COMMISSION']
        
        # Expanded Channel Extraction Rules
        self.channel_map = {
            'USSD': ['USSD', '*966#', '*737#', '*894#', '*901#', '*329#'],
            'POS_Terminal': ['POS', 'TERMINAL', 'MERCHANT', 'HOTEL', 'STORE', 'SUPERMARKET'],
            'Web_Portal': ['WEB', 'PORTAL', 'INTERNET', 'NETGATE', 'PAYSTACK', 'FLUTTERWAVE', 'QUICKTELLER'],
            'Mobile_App': ['MOBILE', 'APP', 'ONEBANK', 'OPAY', 'PALMPAY', 'TRANSFER', 'MOBILE_FX']
        }

    def convert_pdf_to_dataframe(self, pdf_path):
        """
        Scrapes raw un-structured PDF statements line-by-line 
        and matches layout patterns to form a structured table.
        """
        print(f" Extracting text layers from PDF: {pdf_path}")
        reader = PdfReader(pdf_path)
        raw_rows = []
        
        # Basic regex to catch columns (Date, Description, Numbers)
        for page in reader.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split('\n'):
                line_str = line.strip()
                if line_str:
                    raw_rows.append(line_str)
                    
        # Construct dynamic layout matrix from text rows
        parsed_data = []
        for row in raw_rows:
            # Look for a date pattern at the start (e.g., DD-MM-YYYY or DD-MMM-YYYY)
            date_match = re.match(r'^(\d{1,2}[-/\s][A-Za-z0-9]{3,4}[-/\s]\d{2,4})', row)
            if date_match:
                date_part = date_match.group(1)
                remaining = row[len(date_part):].strip()
                
                # Try to extract trailing currency/balance numbers safely
                numbers = re.findall(r'[\"\']?[\d,]+\.\d{2}[\"\']?', remaining)
                if numbers:
                    narration = remaining
                    for num in numbers:
                        narration = narration.replace(num, '')
                    narration = narration.strip().strip(',').strip('|').strip()
                    
                    # Assume last numbers are Debit/Credit stream structures
                    debit_val = numbers[0] if len(numbers) > 1 else "0.0"
                    credit_val = numbers[1] if len(numbers) > 2 else ("0.0" if len(numbers) == 1 else numbers[0])
                    
                    parsed_data.append({
                        'Transaction Date': date_part,
                        'Narration': narration,
                        'Debit': debit_val,
                        'Credit': credit_val
                    })
        
        return pd.DataFrame(parsed_data)

    def normalize_dataframe_schema(self, df_raw):
        """
        Fuzzy Mapping Layer: Dynamically matches arbitrary bank naming systems 
        and normalizes column taxonomy with zero structural friction.
        """
        df_norm = pd.DataFrame()
        columns_lower = {col.lower(): col for col in df_raw.columns}
        
        # 1. Map Time Matrix
        date_keys = ['transaction date', 'txn date', 'date', 'value date', 'timestamp']
        matched_date_col = next((columns_lower[k] for k in date_keys if k in columns_lower), None)
        if matched_date_col:
            df_norm['timestamp'] = df_raw[matched_date_col]
        else:
            df_norm['timestamp'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

        # 2. Map Narration Matrix
        desc_keys = ['narration', 'description', 'remarks', 'transaction details', 'particulars']
        matched_desc_col = next((columns_lower[k] for k in desc_keys if k in columns_lower), None)
        if matched_desc_col:
            df_norm['Narration'] = df_raw[matched_desc_col].fillna('').astype(str).str.upper()
        else:
            df_norm['Narration'] = 'UNKNOWN_TRANSACTION_NARRATION'

        # 3. Map Financial Volume Streams
        debit_keys = ['debit', 'withdrawal', 'amount (dr)', 'paid out', 'dr']
        credit_keys = ['credit', 'deposit', 'amount (cr)', 'paid in', 'cr']
        amt_keys = ['amount', 'value', 'transaction amount']
        
        matched_deb = next((columns_lower[k] for k in debit_keys if k in columns_lower), None)
        matched_cre = next((columns_lower[k] for k in credit_keys if k in columns_lower), None)
        matched_amt = next((columns_lower[k] for k in amt_keys if k in columns_lower), None)

        # Helper function to sanitize messy number formatting
        def clean_numeric_stream(series):
            return pd.to_numeric(series.astype(str).str.replace(r'[^\d\.]', '', regex=True), errors='coerce').fillna(0.0)

        if matched_deb or matched_cre:
            deb_stream = clean_numeric_stream(df_raw[matched_deb]) if matched_deb else 0.0
            cre_stream = clean_numeric_stream(df_raw[matched_cre]) if matched_cre else 0.0
            df_norm['amount'] = deb_stream + cre_stream
        elif matched_amt:
            df_norm['amount'] = clean_numeric_stream(df_raw[matched_amt])
        else:
            df_norm['amount'] = 0.0

        return df_norm

    def process_audit_pipeline(self, file_path):
        if not os.path.exists(file_path):
            print(f" CRITICAL INFRASTRUCTURE ERROR: Input file '{file_path}' not found!")
            return

        # Phase 1: Dynamic Ingestion Route Sorting
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            df_raw = self.convert_pdf_to_dataframe(file_path)
        elif ext == '.csv':
            print(f" Ingesting structured raw CSV ledger: {file_path}")
            df_raw = pd.read_csv(file_path, dtype=str)
        else:
            print(f" Unsupported file signature format: '{ext}'")
            return

        if df_raw.empty:
            print(" Data structure parsing completed with an empty matrix array.")
            return

        # Phase 2: Schema Normalization Layer
        df_processed = self.normalize_dataframe_schema(df_raw)

        # Phase 3 & 4: Regulatory Risk Core Engine Evaluator
        print(" Evaluating matrix rows against CBN regulatory cost-recovery profiles...")
        df_processed['merchant'] = 'OTHER_MERCHANT_ROUTING'
        df_processed['channel'] = 'Mobile_App'
        df_processed['user_location'] = 'LAGOS_NGR'
        df_processed['risk_score'] = 0.1500  # Safe Baseline

        for idx, row in df_processed.iterrows():
            narration = row['Narration']
            
            # Extract channel infrastructure dynamically
            for channel_name, patterns in self.channel_map.items():
                if any(p in narration for p in patterns):
                    df_processed.at[idx, 'channel'] = channel_name
                    break
            
            # Match specific institutions inside narration strings
            if 'OPAY' in narration:
                df_processed.at[idx, 'merchant'] = 'OPAY_FUND_TRANSFER'
            elif 'PALMPAY' in narration:
                df_processed.at[idx, 'merchant'] = 'PALMPAY_FINTECH'
            elif 'VANGUARD' in narration:
                df_processed.at[idx, 'merchant'] = 'VANGUARD_PHARMACY'
                
            # Direct CBN Compliance Breach Interception
            if any(word in narration for word in self.charge_keywords):
                df_processed.at[idx, 'risk_score'] = 0.8200  # Regulatory Charge Flag
                df_processed.at[idx, 'merchant'] = 'SYSTEMIC_BANK_CHARGE'

        # Isolate anomalous high-volume single transfers (₦100,000+)
        df_processed.loc[df_processed['amount'] >= 100000, 'risk_score'] = 0.9412

        # Phase 6: Consolidate Reporting Output Schema
        output_matrix_name = '2026-05-17T17-30_export.csv'
        reporting_schema = ['timestamp', 'amount', 'merchant', 'user_location', 'channel', 'risk_score']
        
        df_final_report = df_processed[reporting_schema].sort_values(by='risk_score', ascending=False)
        df_final_report.to_csv(output_matrix_name, index=False)
        print(f" Universal Compliance Ledger successfully generated: {output_matrix_name}")

if __name__ == "__main__":
    # The universal engine auto-scans for ANY file named 'Statement' in your working repository
    engine = UniversalSentinelEngine()
    
    target_statement = None
    for file in os.listdir('.'):
        if file.startswith('Statement (1)'):
            target_statement = file
            break
            
    if target_statement:
        engine.process_audit_pipeline(target_statement)
    else:
        print(" Operational Alert: Place your client's raw ledger file as 'Statement (1).csv' or 'Statement (1).pdf' inside the workspace directory.")
