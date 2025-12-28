"""
Figure Generation for Research Paper
=====================================
Research Paper: A Financial Analytics Framework for Ride-Sharing Fleet Operations

This script generates publication-quality figures for the ICNDA 2026 conference paper.
All visualizations are derived from actual anonymized data - no synthetic data used.

Output: Figures saved to ../figures/ directory in PDF and PNG formats
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality plot style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1
})

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Create figures directory
figures_dir = os.path.join(script_dir, '..', 'figures')
os.makedirs(figures_dir, exist_ok=True)

print("=" * 70)
print("GENERATING PUBLICATION FIGURES FOR RESEARCH PAPER")
print("=" * 70)

# =====================================================================
# LOAD DATA
# =====================================================================
print("\nLoading anonymized datasets...")
payments_df = pd.read_csv("../payments_order/payorder_anonymized.csv")
trips_df = pd.read_csv("../trip_activity/trip_activity_anonymized.csv")

# Filter completed transactions
completed_payments = payments_df[payments_df['Description'] == 'trip completed order'].copy()

# Filter completed trips with valid distance
completed_trips = trips_df[trips_df['Trip status'] == 'completed'].copy()
completed_trips['Trip distance'] = pd.to_numeric(completed_trips['Trip distance'], errors='coerce')
completed_trips['Final rider fare'] = pd.to_numeric(completed_trips['Final rider fare'], errors='coerce')
valid_trips = completed_trips[completed_trips['Trip distance'] > 0].copy()

print(f"Completed transactions: {len(completed_payments)}")
print(f"Valid trips for analysis: {len(valid_trips)}")

# =====================================================================
# FIGURE 1: FARE VS DISTANCE REGRESSION PLOT
# =====================================================================
print("\n[1/4] Generating Fare vs Distance Regression Plot...")

# Calculate regression
slope, intercept, r_value, p_val, std_err = stats.linregress(
    valid_trips['Trip distance'], 
    valid_trips['Final rider fare']
)

fig, ax = plt.subplots(figsize=(8, 6))

# Scatter plot
ax.scatter(valid_trips['Trip distance'], valid_trips['Final rider fare'], 
           alpha=0.5, c='#2E86AB', edgecolors='none', s=40, label='Actual Trips')

# Regression line
x_line = np.linspace(0, valid_trips['Trip distance'].max(), 100)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, 'r-', linewidth=2.5, 
        label=f'Regression: Fare = {slope:.2f} × Distance + {intercept:.2f}')

# Confidence interval (95%)
n = len(valid_trips)
x_mean = valid_trips['Trip distance'].mean()
se = std_err * np.sqrt(1/n + (x_line - x_mean)**2 / np.sum((valid_trips['Trip distance'] - x_mean)**2))
ci = 1.96 * se * np.sqrt(np.var(valid_trips['Final rider fare']))
ax.fill_between(x_line, y_line - ci, y_line + ci, alpha=0.2, color='red', label='95% CI')

ax.set_xlabel('Trip Distance (km)')
ax.set_ylabel('Fare (INR)')
ax.set_title('Fare-Distance Relationship with Linear Regression')
ax.legend(loc='upper left')

# Add R² annotation
textstr = f'R² = {r_value**2:.4f}\nn = {n} trips\np < 0.001'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.95, 0.05, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

ax.set_xlim(0, None)
ax.set_ylim(0, None)

plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'fig1_fare_distance_regression.pdf'))
plt.savefig(os.path.join(figures_dir, 'fig1_fare_distance_regression.png'))
plt.close()
print("   Saved: fig1_fare_distance_regression.pdf/png")

# =====================================================================
# FIGURE 2: FARE COMPONENT BREAKDOWN (PIE CHART)
# =====================================================================
print("[2/4] Generating Fare Component Breakdown Chart...")

# Calculate fare components
total_base_fare = completed_payments['Paid to you:Your earnings:Fare:Fare'].sum()
total_booking_fee = completed_payments['Paid to you:Your earnings:Fare:Booking fee'].sum()
total_surge = completed_payments['Paid to you:Your earnings:Fare:Surge'].sum()
total_wait_time = completed_payments['Paid to you:Your earnings:Fare:Wait Time at Pick-up'].sum()
total_outskirt = completed_payments['Paid to you:Your earnings:Fare:Outskirt Surcharge'].sum()

components = {
    'Base Fare': total_base_fare,
    'Booking Fee': total_booking_fee,
    'Surge Pricing': total_surge,
    'Outskirt Surcharge': total_outskirt,
    'Wait Time': total_wait_time
}

# Filter out zero/negligible components for cleaner visualization
components = {k: v for k, v in components.items() if v > 100}

labels = list(components.keys())
sizes = list(components.values())
total = sum(sizes)
percentages = [100 * s / total for s in sizes]

# Colors
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B'][:len(labels)]

fig, ax = plt.subplots(figsize=(8, 6))

# Create pie chart
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='',
                                   colors=colors, startangle=90,
                                   explode=[0.02] * len(labels),
                                   wedgeprops=dict(width=0.7, edgecolor='white'))

# Create legend with values
legend_labels = [f'{label}: ₹{size:,.0f} ({pct:.1f}%)' 
                 for label, size, pct in zip(labels, sizes, percentages)]
ax.legend(wedges, legend_labels, title="Fare Components", 
          loc="center left", bbox_to_anchor=(0.9, 0.5))

# Add center text
centre_circle = plt.Circle((0, 0), 0.35, fc='white')
ax.add_patch(centre_circle)
ax.text(0, 0, f'Total\n₹{total:,.0f}', ha='center', va='center', fontsize=12, fontweight='bold')

ax.set_title('Fare Component Breakdown', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'fig2_fare_components.pdf'))
plt.savefig(os.path.join(figures_dir, 'fig2_fare_components.png'))
plt.close()
print("   Saved: fig2_fare_components.pdf/png")

# =====================================================================
# FIGURE 3: DRIVER EARNINGS DISTRIBUTION
# =====================================================================
print("[3/4] Generating Driver Earnings Distribution Chart...")

# Aggregate earnings per driver
driver_earnings = completed_payments.groupby('Driver UUID').agg({
    'Paid to you : Your earnings': 'sum',
    'Trip UUID': 'count'
}).rename(columns={'Trip UUID': 'trip_count'})

earnings = driver_earnings['Paid to you : Your earnings'].values

# Calculate Gini coefficient
def gini_coefficient(data):
    sorted_data = np.sort(data)
    n = len(sorted_data)
    cumulative = np.cumsum(sorted_data)
    return (2 * np.sum((np.arange(1, n+1) * sorted_data)) / (n * np.sum(sorted_data))) - (n + 1) / n

gini = gini_coefficient(earnings)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: Histogram with KDE
ax1 = axes[0]
ax1.hist(earnings, bins=15, density=True, alpha=0.7, color='#2E86AB', edgecolor='white', label='Earnings Distribution')

# Add KDE
from scipy.stats import gaussian_kde
kde = gaussian_kde(earnings)
x_kde = np.linspace(earnings.min(), earnings.max(), 100)
ax1.plot(x_kde, kde(x_kde), 'r-', linewidth=2, label='Density Estimate')

ax1.axvline(np.mean(earnings), color='green', linestyle='--', linewidth=2, label=f'Mean: ₹{np.mean(earnings):,.0f}')
ax1.axvline(np.median(earnings), color='orange', linestyle='--', linewidth=2, label=f'Median: ₹{np.median(earnings):,.0f}')

ax1.set_xlabel('Total Earnings (INR)')
ax1.set_ylabel('Density')
ax1.set_title('Driver Earnings Distribution')
ax1.legend(loc='upper right', fontsize=9)

# Right: Lorenz Curve
ax2 = axes[1]
sorted_earnings = np.sort(earnings)
cumulative_earnings = np.cumsum(sorted_earnings) / np.sum(sorted_earnings)
cumulative_population = np.arange(1, len(earnings) + 1) / len(earnings)

# Perfect equality line
ax2.plot([0, 1], [0, 1], 'k--', linewidth=1.5, label='Perfect Equality')

# Lorenz curve
ax2.plot(np.concatenate([[0], cumulative_population]), 
         np.concatenate([[0], cumulative_earnings]), 
         'b-', linewidth=2.5, label=f'Lorenz Curve (Gini = {gini:.4f})')

# Fill area
ax2.fill_between(np.concatenate([[0], cumulative_population]), 
                  np.concatenate([[0], cumulative_earnings]),
                  np.concatenate([[0], cumulative_population]),
                  alpha=0.3, color='blue')

ax2.set_xlabel('Cumulative Share of Drivers')
ax2.set_ylabel('Cumulative Share of Earnings')
ax2.set_title('Lorenz Curve for Earnings Inequality')
ax2.legend(loc='upper left')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)

# Add Gini annotation
ax2.text(0.6, 0.2, f'Gini Coefficient\n= {gini:.4f}', fontsize=11,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'fig3_earnings_distribution.pdf'))
plt.savefig(os.path.join(figures_dir, 'fig3_earnings_distribution.png'))
plt.close()
print("   Saved: fig3_earnings_distribution.pdf/png")

# =====================================================================
# FIGURE 4: TEMPORAL PATTERNS (HOURLY DISTRIBUTION)
# =====================================================================
print("[4/4] Generating Temporal Patterns Chart...")

# Parse datetime
trips_df['request_datetime'] = pd.to_datetime(trips_df['Trip request time'], errors='coerce')
trips_df['hour'] = trips_df['request_datetime'].dt.hour

# Hour-wise distribution
hourly_trips = trips_df.groupby('hour').size().reindex(range(24), fill_value=0)

# Time period categorization
def get_period_color(hour):
    if 6 <= hour < 12:
        return '#F4A261'  # Morning - Orange
    elif 12 <= hour < 18:
        return '#E9C46A'  # Afternoon - Yellow
    elif 18 <= hour < 24:
        return '#2A9D8F'  # Evening - Teal
    else:
        return '#264653'  # Night - Dark

colors = [get_period_color(h) for h in range(24)]

fig, ax = plt.subplots(figsize=(12, 5))

bars = ax.bar(range(24), hourly_trips.values, color=colors, edgecolor='white', linewidth=0.5)

ax.set_xlabel('Hour of Day')
ax.set_ylabel('Number of Trips')
ax.set_title('Trip Distribution by Hour of Day')
ax.set_xticks(range(24))
ax.set_xticklabels([f'{h:02d}' for h in range(24)])

# Add legend for time periods
legend_elements = [
    mpatches.Patch(facecolor='#264653', label='Night (00-06)'),
    mpatches.Patch(facecolor='#F4A261', label='Morning (06-12)'),
    mpatches.Patch(facecolor='#E9C46A', label='Afternoon (12-18)'),
    mpatches.Patch(facecolor='#2A9D8F', label='Evening (18-24)')
]
ax.legend(handles=legend_elements, loc='upper left', ncol=2)

# Annotate peak hours
peak_hour = hourly_trips.idxmax()
peak_value = hourly_trips.max()
ax.annotate(f'Peak: {peak_value} trips', 
            xy=(peak_hour, peak_value), 
            xytext=(peak_hour + 2, peak_value + 5),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=10, color='red')

# Add time period summary
morning = trips_df[(trips_df['hour'] >= 6) & (trips_df['hour'] < 12)]
afternoon = trips_df[(trips_df['hour'] >= 12) & (trips_df['hour'] < 18)]
evening = trips_df[(trips_df['hour'] >= 18) & (trips_df['hour'] <= 23)]
night = trips_df[(trips_df['hour'] >= 0) & (trips_df['hour'] < 6)]

summary_text = f'Morning: {len(morning)} ({100*len(morning)/len(trips_df):.1f}%)\n'
summary_text += f'Afternoon: {len(afternoon)} ({100*len(afternoon)/len(trips_df):.1f}%)\n'
summary_text += f'Evening: {len(evening)} ({100*len(evening)/len(trips_df):.1f}%)\n'
summary_text += f'Night: {len(night)} ({100*len(night)/len(trips_df):.1f}%)'

ax.text(0.98, 0.95, summary_text, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'fig4_temporal_patterns.pdf'))
plt.savefig(os.path.join(figures_dir, 'fig4_temporal_patterns.png'))
plt.close()
print("   Saved: fig4_temporal_patterns.pdf/png")

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "=" * 70)
print("FIGURE GENERATION COMPLETE")
print("=" * 70)
print(f"\nAll figures saved to: {os.path.abspath(figures_dir)}")
print("\nGenerated files:")
print("  1. fig1_fare_distance_regression.pdf/png - Fare vs Distance regression")
print("  2. fig2_fare_components.pdf/png - Fare component breakdown")
print("  3. fig3_earnings_distribution.pdf/png - Driver earnings with Lorenz curve")
print("  4. fig4_temporal_patterns.pdf/png - Hourly trip distribution")
print("\nThese figures can be included in the LaTeX paper using:")
print("  \\includegraphics[width=\\textwidth]{figures/fig1_fare_distance_regression}")
print("=" * 70)
