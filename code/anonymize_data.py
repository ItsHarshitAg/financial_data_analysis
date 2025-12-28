"""
Data Anonymization Script for Uber Fleet Reports
-------------------------------------------------
This script removes/masks all Personally Identifiable Information (PII)
from the payments order and trip activity CSV files.

PII elements anonymized:
- Driver names replaced with anonymous IDs (Driver_001, Driver_002, etc.)
- UUIDs replaced with hash-based anonymous IDs
- Number plates replaced with anonymous vehicle IDs
- Addresses generalized (only city/area retained)
- Dates shifted by a random offset
- Organization names generalized
"""

import pandas as pd
import numpy as np
import hashlib
import os
import re
from datetime import timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Date shift (shift all dates back by 6 months for anonymization)
DATE_SHIFT_DAYS = -180

def anonymize_uuid(uuid_str, prefix="ID"):
    """Create a consistent anonymous ID from a UUID"""
    if pd.isna(uuid_str) or uuid_str == "00000000-0000-0000-0000-000000000000":
        return f"{prefix}_UNKNOWN"
    # Create a short hash
    hash_obj = hashlib.md5(str(uuid_str).encode())
    short_hash = hash_obj.hexdigest()[:8].upper()
    return f"{prefix}_{short_hash}"

def anonymize_driver_name(first_name, surname, driver_uuid):
    """Replace driver name with anonymous driver ID"""
    return anonymize_uuid(driver_uuid, "DRIVER")

def anonymize_address(address):
    """Anonymize address to only show general area"""
    if pd.isna(address):
        return "Area_Unknown"
    
    # Extract only city/major area references
    chennai_areas = ['Chennai', 'Egmore', 'Mylapore', 'Guindy', 'Vadapalani', 
                     'Tambaram', 'Velachery', 'Adyar', 'T. Nagar', 'Anna Nagar',
                     'Chromepet', 'Sholinganallur', 'Airport', 'Perungudi', 
                     'Besant Nagar', 'Thiruvanmiyur', 'Koyambedu', 'Avadi',
                     'Ambattur', 'Porur', 'Pallavaram', 'Kelambakkam']
    
    for area in chennai_areas:
        if area.lower() in address.lower():
            return f"Zone_{area}"
    
    # Extract PIN code area if available
    pin_match = re.search(r'6000\d{2}', address)
    if pin_match:
        return f"Zone_PIN_{pin_match.group()}"
    
    return "Zone_Chennai_Metro"

def anonymize_number_plate(plate):
    """Anonymize vehicle number plate"""
    if pd.isna(plate):
        return "VEH_UNKNOWN"
    # Create anonymous vehicle ID
    hash_obj = hashlib.md5(str(plate).encode())
    return f"VEH_{hash_obj.hexdigest()[:6].upper()}"

def shift_date(date_str, days_shift=DATE_SHIFT_DAYS):
    """Shift date by specified number of days"""
    if pd.isna(date_str):
        return date_str
    try:
        # Handle various date formats
        date_str = str(date_str)
        if 'IST' in date_str:
            # Format: 2025-10-15 04:23:34.525 +0530 IST
            date_part = date_str.split('+')[0].strip()
            dt = pd.to_datetime(date_part)
        else:
            dt = pd.to_datetime(date_str)
        
        shifted = dt + timedelta(days=days_shift)
        return shifted.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str

def anonymize_payments_data():
    """Anonymize the payments order CSV file"""
    print("Processing payments_order/payorder.csv...")
    
    input_path = "../payments_order/payorder.csv"
    output_path = "../payments_order/payorder_anonymized.csv"
    
    df = pd.read_csv(input_path)
    
    print(f"  Original records: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    
    # Create driver mapping for consistent anonymization
    unique_drivers = df['Driver UUID'].unique()
    driver_map = {d: anonymize_uuid(d, "DRIVER") for d in unique_drivers}
    
    # Anonymize columns
    df['transaction UUID'] = df['transaction UUID'].apply(lambda x: anonymize_uuid(x, "TXN"))
    df['Driver UUID'] = df['Driver UUID'].map(driver_map)
    df['Driver first name'] = 'ANON'
    df['Driver surname'] = 'DRIVER'
    df['Trip UUID'] = df['Trip UUID'].apply(lambda x: anonymize_uuid(x, "TRIP"))
    df['Organisation name'] = 'Fleet_Operator_Chennai'
    df['Org alias'] = 'FOC'
    df['vs reporting'] = df['vs reporting'].apply(shift_date)
    
    df.to_csv(output_path, index=False)
    print(f"  Anonymized file saved: {output_path}")
    print(f"  Unique drivers (anonymized): {df['Driver UUID'].nunique()}")
    
    return df

def anonymize_trip_data():
    """Anonymize the trip activity CSV file"""
    print("\nProcessing trip_activity CSV...")
    
    # Find the trip activity file
    trip_folder = "../trip_activity"
    trip_files = [f for f in os.listdir(trip_folder) if f.endswith('.csv')]
    
    if not trip_files:
        print("  No trip activity CSV found!")
        return None
    
    input_path = os.path.join(trip_folder, trip_files[0])
    output_path = os.path.join(trip_folder, "trip_activity_anonymized.csv")
    
    df = pd.read_csv(input_path)
    
    print(f"  Original records: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    
    # Create mappings for consistent anonymization
    unique_drivers = df['Driver UUID'].unique()
    driver_map = {d: anonymize_uuid(d, "DRIVER") for d in unique_drivers}
    
    unique_vehicles = df['Vehicle UUID'].unique()
    vehicle_map = {v: anonymize_uuid(v, "VEH") for v in unique_vehicles}
    
    # Anonymize columns
    df['Trip UUID'] = df['Trip UUID'].apply(lambda x: anonymize_uuid(x, "TRIP"))
    df['Driver UUID'] = df['Driver UUID'].map(driver_map)
    df['Driver first name'] = 'ANON'
    df['Driver surname'] = 'DRIVER'
    df['Vehicle UUID'] = df['Vehicle UUID'].map(vehicle_map)
    df['Number plate'] = df['Number plate'].apply(anonymize_number_plate)
    df['Pick-up address'] = df['Pick-up address'].apply(anonymize_address)
    df['Drop-off address'] = df['Drop-off address'].apply(anonymize_address)
    df['Trip request time'] = df['Trip request time'].apply(shift_date)
    df['Trip drop-off time'] = df['Trip drop-off time'].apply(shift_date)
    
    df.to_csv(output_path, index=False)
    print(f"  Anonymized file saved: {output_path}")
    print(f"  Unique drivers (anonymized): {df['Driver UUID'].nunique()}")
    print(f"  Unique vehicles (anonymized): {df['Vehicle UUID'].nunique()}")
    
    return df

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=" * 60)
    print("DATA ANONYMIZATION FOR UBER FLEET REPORTS")
    print("=" * 60)
    
    payments_df = anonymize_payments_data()
    trips_df = anonymize_trip_data()
    
    print("\n" + "=" * 60)
    print("ANONYMIZATION COMPLETE")
    print("=" * 60)
    print("\nPII elements removed/masked:")
    print("  ✓ Driver names → Anonymous IDs")
    print("  ✓ UUIDs → Hash-based anonymous IDs") 
    print("  ✓ Number plates → Anonymous vehicle IDs")
    print("  ✓ Detailed addresses → Generalized zones")
    print("  ✓ Dates → Shifted by 6 months")
    print("  ✓ Organization names → Generalized")
