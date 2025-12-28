"""
Comprehensive Data Analysis for Uber Fleet Financial Data
==========================================================
Research Paper: Financial Analytics Framework for Ride-Sharing Fleet Operations

This script performs extensive analysis on anonymized Uber fleet data to:
1. Analyze financial performance metrics
2. Identify revenue patterns and anomalies
3. Examine driver earnings distribution
4. Study trip completion rates and cancellation patterns
5. Generate insights for fleet management optimization

All numbers generated are from actual data analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("=" * 70)
print("FINANCIAL ANALYTICS FOR RIDE-SHARING FLEET OPERATIONS")
print("Research Data Analysis Report")
print("=" * 70)

# =====================================================================
# SECTION 1: DATA LOADING
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 1: DATA LOADING AND OVERVIEW")
print("=" * 70)

# Load anonymized data
payments_df = pd.read_csv("../payments_order/payorder_anonymized.csv")
trips_df = pd.read_csv("../trip_activity/trip_activity_anonymized.csv")

print(f"\nPayments Dataset:")
print(f"  Total records: {len(payments_df)}")
print(f"  Unique transactions: {payments_df['transaction UUID'].nunique()}")
print(f"  Unique drivers: {payments_df['Driver UUID'].nunique()}")
print(f"  Unique trips: {payments_df['Trip UUID'].nunique()}")

print(f"\nTrip Activity Dataset:")
print(f"  Total records: {len(trips_df)}")
print(f"  Unique trips: {trips_df['Trip UUID'].nunique()}")
print(f"  Unique drivers: {trips_df['Driver UUID'].nunique()}")
print(f"  Unique vehicles: {trips_df['Vehicle UUID'].nunique()}")

# =====================================================================
# SECTION 2: FINANCIAL METRICS ANALYSIS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 2: FINANCIAL METRICS ANALYSIS")
print("=" * 70)

# Filter for completed trips only (trip completed order)
completed_payments = payments_df[payments_df['Description'] == 'trip completed order'].copy()

print(f"\nCompleted Trip Transactions: {len(completed_payments)}")

# Basic financial metrics
total_paid = completed_payments['Paid to you'].sum()
total_earnings = completed_payments['Paid to you : Your earnings'].sum()
total_fare = completed_payments['Paid to you : Your earnings : Fare'].sum()
total_cash_collected = completed_payments['Paid to you : Trip balance : Payouts : Cash collected'].abs().sum()

print(f"\n--- Aggregate Financial Metrics ---")
print(f"Total Net Payments to Drivers: ₹{total_paid:,.2f}")
print(f"Total Gross Earnings: ₹{total_earnings:,.2f}")
print(f"Total Fare Revenue: ₹{total_fare:,.2f}")
print(f"Total Cash Collected by Drivers: ₹{total_cash_collected:,.2f}")

# Revenue component breakdown
total_base_fare = completed_payments['Paid to you:Your earnings:Fare:Fare'].sum()
total_booking_fee = completed_payments['Paid to you:Your earnings:Fare:Booking fee'].sum()
total_surge = completed_payments['Paid to you:Your earnings:Fare:Surge'].sum()
total_wait_time = completed_payments['Paid to you:Your earnings:Fare:Wait Time at Pick-up'].sum()
total_outskirt = completed_payments['Paid to you:Your earnings:Fare:Outskirt Surcharge'].sum()
total_tips = completed_payments['Paid to you:Your earnings:Tip'].sum()
total_toll = completed_payments['Paid to you:Trip balance:Refunds:Toll'].sum()
total_cancellation = payments_df['Paid to you:Your earnings:Fare:Cancellation'].sum()

print(f"\n--- Revenue Component Breakdown ---")
print(f"Base Fare: ₹{total_base_fare:,.2f} ({100*total_base_fare/total_fare:.1f}%)")
print(f"Booking Fee: ₹{total_booking_fee:,.2f} ({100*total_booking_fee/total_fare:.1f}%)")
print(f"Surge Pricing: ₹{total_surge:,.2f} ({100*total_surge/total_fare:.1f}%)")
print(f"Wait Time Charges: ₹{total_wait_time:,.2f} ({100*total_wait_time/total_fare:.1f}%)")
print(f"Outskirt Surcharge: ₹{total_outskirt:,.2f} ({100*total_outskirt/total_fare:.1f}%)")
print(f"Tips: ₹{total_tips:,.2f}")
print(f"Toll Refunds: ₹{total_toll:,.2f}")
print(f"Cancellation Fees Earned: ₹{total_cancellation:,.2f}")

# =====================================================================
# SECTION 3: DRIVER EARNINGS ANALYSIS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 3: DRIVER EARNINGS DISTRIBUTION")
print("=" * 70)

# Aggregate earnings per driver
driver_earnings = completed_payments.groupby('Driver UUID').agg({
    'Paid to you': 'sum',
    'Paid to you : Your earnings': 'sum',
    'Trip UUID': 'count'
}).rename(columns={'Trip UUID': 'trip_count'})

print(f"\nNumber of Active Drivers: {len(driver_earnings)}")

earnings_stats = driver_earnings['Paid to you : Your earnings'].describe()
print(f"\n--- Driver Earnings Statistics ---")
print(f"Mean Earnings per Driver: ₹{earnings_stats['mean']:,.2f}")
print(f"Median Earnings per Driver: ₹{earnings_stats['50%']:,.2f}")
print(f"Std Dev: ₹{earnings_stats['std']:,.2f}")
print(f"Min: ₹{earnings_stats['min']:,.2f}")
print(f"Max: ₹{earnings_stats['max']:,.2f}")

# Earnings per trip
driver_earnings['earnings_per_trip'] = driver_earnings['Paid to you : Your earnings'] / driver_earnings['trip_count']
ept_stats = driver_earnings['earnings_per_trip'].describe()

print(f"\n--- Earnings per Trip Statistics ---")
print(f"Mean: ₹{ept_stats['mean']:,.2f}")
print(f"Median: ₹{ept_stats['50%']:,.2f}")
print(f"Std Dev: ₹{ept_stats['std']:,.2f}")

# Trip count distribution
print(f"\n--- Trip Count per Driver ---")
print(f"Mean trips: {driver_earnings['trip_count'].mean():.1f}")
print(f"Median trips: {driver_earnings['trip_count'].median():.1f}")
print(f"Max trips: {driver_earnings['trip_count'].max()}")
print(f"Min trips: {driver_earnings['trip_count'].min()}")

# Gini coefficient for earnings inequality
def gini_coefficient(data):
    """Calculate Gini coefficient for income inequality"""
    sorted_data = np.sort(data)
    n = len(sorted_data)
    cumulative = np.cumsum(sorted_data)
    return (2 * np.sum((np.arange(1, n+1) * sorted_data)) / (n * np.sum(sorted_data))) - (n + 1) / n

gini = gini_coefficient(driver_earnings['Paid to you : Your earnings'].values)
print(f"\nGini Coefficient (Earnings Inequality): {gini:.4f}")
print(f"  (0 = perfect equality, 1 = perfect inequality)")

# =====================================================================
# SECTION 4: TRIP COMPLETION ANALYSIS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 4: TRIP COMPLETION RATE ANALYSIS")
print("=" * 70)

# Trip status distribution
trip_status = trips_df['Trip status'].value_counts()
print(f"\n--- Trip Status Distribution ---")
for status, count in trip_status.items():
    percentage = 100 * count / len(trips_df)
    print(f"{status}: {count} ({percentage:.1f}%)")

completion_rate = 100 * trip_status.get('completed', 0) / len(trips_df)
rider_cancel_rate = 100 * trip_status.get('rider_cancelled', 0) / len(trips_df)
driver_cancel_rate = 100 * trip_status.get('driver_cancelled', 0) / len(trips_df)

print(f"\nCompletion Rate: {completion_rate:.1f}%")
print(f"Rider Cancellation Rate: {rider_cancel_rate:.1f}%")
print(f"Driver Cancellation Rate: {driver_cancel_rate:.1f}%")

# Product type analysis
print(f"\n--- Service Type Distribution ---")
product_counts = trips_df['Product type'].value_counts()
for product, count in product_counts.items():
    percentage = 100 * count / len(trips_df)
    print(f"{product}: {count} ({percentage:.1f}%)")

# =====================================================================
# SECTION 5: TRIP DISTANCE AND FARE ANALYSIS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 5: TRIP DISTANCE AND FARE ANALYSIS")
print("=" * 70)

# Filter completed trips
completed_trips = trips_df[trips_df['Trip status'] == 'completed'].copy()
completed_trips['Trip distance'] = pd.to_numeric(completed_trips['Trip distance'], errors='coerce')
completed_trips['Final rider fare'] = pd.to_numeric(completed_trips['Final rider fare'], errors='coerce')

# Remove zero distance trips
valid_trips = completed_trips[completed_trips['Trip distance'] > 0]

print(f"\nCompleted Trips with Valid Distance: {len(valid_trips)}")

# Distance statistics
dist_stats = valid_trips['Trip distance'].describe()
print(f"\n--- Trip Distance Statistics (km) ---")
print(f"Mean: {dist_stats['mean']:.2f} km")
print(f"Median: {dist_stats['50%']:.2f} km")
print(f"Std Dev: {dist_stats['std']:.2f} km")
print(f"Min: {dist_stats['min']:.2f} km")
print(f"Max: {dist_stats['max']:.2f} km")

# Fare statistics
fare_stats = valid_trips['Final rider fare'].describe()
print(f"\n--- Fare Statistics (₹) ---")
print(f"Mean: ₹{fare_stats['mean']:.2f}")
print(f"Median: ₹{fare_stats['50%']:.2f}")
print(f"Std Dev: ₹{fare_stats['std']:.2f}")
print(f"Min: ₹{fare_stats['min']:.2f}")
print(f"Max: ₹{fare_stats['max']:.2f}")

# Fare per km
valid_trips['fare_per_km'] = valid_trips['Final rider fare'] / valid_trips['Trip distance']
fpk_stats = valid_trips['fare_per_km'].describe()

print(f"\n--- Fare per Kilometer Statistics ---")
print(f"Mean: ₹{fpk_stats['mean']:.2f}/km")
print(f"Median: ₹{fpk_stats['50%']:.2f}/km")
print(f"Std Dev: ₹{fpk_stats['std']:.2f}/km")

# Distance category analysis
def categorize_distance(d):
    if d <= 5:
        return 'Short (≤5 km)'
    elif d <= 15:
        return 'Medium (5-15 km)'
    elif d <= 25:
        return 'Long (15-25 km)'
    else:
        return 'Very Long (>25 km)'

valid_trips['distance_category'] = valid_trips['Trip distance'].apply(categorize_distance)
dist_cat = valid_trips.groupby('distance_category').agg({
    'Trip UUID': 'count',
    'Final rider fare': 'mean',
    'fare_per_km': 'mean'
}).round(2)

print(f"\n--- Analysis by Distance Category ---")
print(dist_cat.to_string())

# =====================================================================
# SECTION 6: CASH VS DIGITAL PAYMENT ANALYSIS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 6: CASH VS DIGITAL PAYMENT PATTERNS")
print("=" * 70)

# Cash collected analysis
cash_trips = completed_payments[completed_payments['Paid to you : Trip balance : Payouts : Cash collected'] < 0]
digital_trips = completed_payments[completed_payments['Paid to you : Trip balance : Payouts : Cash collected'] == 0]

cash_count = len(cash_trips)
digital_count = len(digital_trips)
total_count = len(completed_payments)

print(f"\nPayment Mode Distribution:")
print(f"Cash Trips: {cash_count} ({100*cash_count/total_count:.1f}%)")
print(f"Digital Trips: {digital_count} ({100*digital_count/total_count:.1f}%)")

cash_fare_avg = cash_trips['Paid to you : Your earnings : Fare'].mean()
digital_fare_avg = digital_trips['Paid to you : Your earnings : Fare'].mean()

print(f"\nAverage Fare Comparison:")
print(f"Cash Trips: ₹{cash_fare_avg:.2f}")
print(f"Digital Trips: ₹{digital_fare_avg:.2f}")

# =====================================================================
# SECTION 7: TEMPORAL PATTERNS (Hour of Day Analysis)
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 7: TEMPORAL PATTERNS")
print("=" * 70)

# Parse datetime
trips_df['request_datetime'] = pd.to_datetime(trips_df['Trip request time'], errors='coerce')
trips_df['hour'] = trips_df['request_datetime'].dt.hour

# Hour-wise distribution
hourly_trips = trips_df.groupby('hour').size()
print(f"\n--- Hourly Trip Distribution ---")

# Peak hours analysis
peak_hours = hourly_trips.nlargest(5)
print(f"\nTop 5 Peak Hours:")
for hour, count in peak_hours.items():
    print(f"  {hour:02d}:00 - {hour:02d}:59: {count} trips")

off_peak = hourly_trips.nsmallest(5)
print(f"\nLowest 5 Hours:")
for hour, count in off_peak.items():
    print(f"  {hour:02d}:00 - {hour:02d}:59: {count} trips")

# Morning vs Evening
morning = trips_df[(trips_df['hour'] >= 6) & (trips_df['hour'] < 12)]
afternoon = trips_df[(trips_df['hour'] >= 12) & (trips_df['hour'] < 18)]
evening = trips_df[(trips_df['hour'] >= 18) & (trips_df['hour'] <= 23)]
night = trips_df[(trips_df['hour'] >= 0) & (trips_df['hour'] < 6)]

print(f"\n--- Time Period Distribution ---")
print(f"Morning (6AM-12PM): {len(morning)} trips ({100*len(morning)/len(trips_df):.1f}%)")
print(f"Afternoon (12PM-6PM): {len(afternoon)} trips ({100*len(afternoon)/len(trips_df):.1f}%)")
print(f"Evening (6PM-12AM): {len(evening)} trips ({100*len(evening)/len(trips_df):.1f}%)")
print(f"Night (12AM-6AM): {len(night)} trips ({100*len(night)/len(trips_df):.1f}%)")

# =====================================================================
# SECTION 8: DRIVER PERFORMANCE METRICS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 8: DRIVER PERFORMANCE METRICS")
print("=" * 70)

# Driver-level trip analysis
driver_trips = trips_df.groupby('Driver UUID').agg({
    'Trip UUID': 'count',
    'Trip status': lambda x: (x == 'completed').sum(),
    'Trip distance': lambda x: x[trips_df.loc[x.index, 'Trip status'] == 'completed'].sum(),
    'Final rider fare': lambda x: x[trips_df.loc[x.index, 'Trip status'] == 'completed'].sum()
}).rename(columns={
    'Trip UUID': 'total_trips',
    'Trip status': 'completed_trips'
})

driver_trips['completion_rate'] = 100 * driver_trips['completed_trips'] / driver_trips['total_trips']
driver_trips['avg_fare_per_trip'] = driver_trips['Final rider fare'] / driver_trips['completed_trips']

print(f"\n--- Driver Performance Distribution ---")
cr_stats = driver_trips['completion_rate'].describe()
print(f"Completion Rate:")
print(f"  Mean: {cr_stats['mean']:.1f}%")
print(f"  Median: {cr_stats['50%']:.1f}%")
print(f"  Min: {cr_stats['min']:.1f}%")
print(f"  Max: {cr_stats['max']:.1f}%")

# High performers (>80% completion rate)
high_performers = driver_trips[driver_trips['completion_rate'] >= 80]
low_performers = driver_trips[driver_trips['completion_rate'] < 60]

print(f"\nHigh Performers (≥80% completion): {len(high_performers)} drivers")
print(f"Low Performers (<60% completion): {len(low_performers)} drivers")

# =====================================================================
# SECTION 9: STATISTICAL CORRELATIONS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 9: STATISTICAL ANALYSIS")
print("=" * 70)

# Correlation between distance and fare
correlation, p_value = stats.pearsonr(
    valid_trips['Trip distance'], 
    valid_trips['Final rider fare']
)
print(f"\nPearson Correlation (Distance vs Fare): {correlation:.4f}")
print(f"P-value: {p_value:.2e}")

# Regression coefficients
slope, intercept, r_value, p_val, std_err = stats.linregress(
    valid_trips['Trip distance'], 
    valid_trips['Final rider fare']
)
print(f"\nLinear Regression (Fare = a*Distance + b):")
print(f"  Slope (a): ₹{slope:.2f} per km")
print(f"  Intercept (b): ₹{intercept:.2f} (base fare)")
print(f"  R² value: {r_value**2:.4f}")

# Coefficient of variation for fare consistency
cv_fare = (valid_trips['Final rider fare'].std() / valid_trips['Final rider fare'].mean()) * 100
cv_distance = (valid_trips['Trip distance'].std() / valid_trips['Trip distance'].mean()) * 100

print(f"\nCoefficient of Variation:")
print(f"  Fare: {cv_fare:.1f}%")
print(f"  Distance: {cv_distance:.1f}%")

# =====================================================================
# SECTION 10: KEY INSIGHTS SUMMARY
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 10: KEY INSIGHTS SUMMARY FOR RESEARCH PAPER")
print("=" * 70)

print("""
FINANCIAL METRICS:
- Total transactions analyzed: {0}
- Total driver earnings: ₹{1:,.2f}
- Average earnings per driver: ₹{2:,.2f}
- Gini coefficient: {3:.4f}

FARE STRUCTURE:
- Base fare contribution: {4:.1f}%
- Booking fee contribution: {5:.1f}%
- Surge pricing contribution: {6:.1f}%
- Average fare: ₹{7:.2f}
- Average fare per km: ₹{8:.2f}

TRIP PATTERNS:
- Trip completion rate: {9:.1f}%
- Rider cancellation rate: {10:.1f}%
- Driver cancellation rate: {11:.1f}%
- Average trip distance: {12:.2f} km

PAYMENT MODES:
- Cash payment ratio: {13:.1f}%
- Digital payment ratio: {14:.1f}%

REGRESSION MODEL:
- Fare = ₹{15:.2f} * Distance + ₹{16:.2f}
- R² = {17:.4f}

DRIVER PERFORMANCE:
- Total active drivers: {18}
- High performers (≥80%): {19}
- Mean completion rate: {20:.1f}%
""".format(
    len(completed_payments),
    total_earnings,
    earnings_stats['mean'],
    gini,
    100*total_base_fare/total_fare,
    100*total_booking_fee/total_fare,
    100*total_surge/total_fare,
    fare_stats['mean'],
    fpk_stats['mean'],
    completion_rate,
    rider_cancel_rate,
    driver_cancel_rate,
    dist_stats['mean'],
    100*cash_count/total_count,
    100*digital_count/total_count,
    slope,
    intercept,
    r_value**2,
    len(driver_earnings),
    len(high_performers),
    cr_stats['mean']
))

print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
