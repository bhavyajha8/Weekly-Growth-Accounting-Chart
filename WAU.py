import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'C:/Users/Bhavya Jha/OneDrive/Desktop/Active_users.csv'  # Adjust this to your actual CSV file path if not an image
data = pd.read_csv(file_path)

# Initialize lists to store results
weeks = data.columns
new_users = []
retained_users = []
resurrected_users = []
churned_users = []
quick_ratios = []
retention_rates = []

# Calculate user categories for each week
for i in range(1, len(weeks)):
    current_week = set(data[weeks[i]].dropna())
    previous_week = set(data[weeks[i - 1]].dropna())
    
    new = len(current_week - previous_week)
    retained = len(current_week & previous_week)
    resurrected = len(current_week - previous_week & set(data[weeks[:i]].stack().unique()))
    churned = len(previous_week - current_week)
    
    new_users.append(new)
    retained_users.append(retained)
    resurrected_users.append(resurrected)
    churned_users.append(churned)
    
    quick_ratio = (new + resurrected) / churned if churned > 0 else float('inf')
    quick_ratios.append(quick_ratio)
    
    retention_rate = retained / len(previous_week) if len(previous_week) > 0 else 0
    retention_rates.append(retention_rate)

# Create a DataFrame for results
results = pd.DataFrame({
    'week': weeks[1:],
    'new_users': new_users,
    'retained_users': retained_users,
    'resurrected_users': resurrected_users,
    'churned_users': churned_users,
    'quick_ratio': quick_ratios,
    'retention_rate': retention_rates
})

# Plot the results
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot bars
ax1.bar(results['week'], results['new_users'], label='New Users', color='blue')
ax1.bar(results['week'], results['resurrected_users'], bottom=results['new_users'], label='Resurrected Users', color='red')
ax1.bar(results['week'], results['churned_users'], bottom=[i+j for i,j in zip(results['new_users'], results['resurrected_users'])], label='Churned Users', color='green')

# Plot quick ratio and retention rate
ax2 = ax1.twinx()
ax2.plot(results['week'], results['quick_ratio'], label='Quick Ratio', color='orange', marker='o')
ax2.plot(results['week'], results['retention_rate'], label='Retention Rate', color='purple', marker='x')

# Labels and legend
ax1.set_xlabel('Week')
ax1.set_ylabel('Number of Users')
ax2.set_ylabel('Quick Ratio / Retention Rate')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.title('Weekly Growth Accounting')
plt.show()

# Save the results to a CSV file
results.to_csv('weekly_growth_accounting.csv', index=False)
