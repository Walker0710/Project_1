import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('GaltonFamilies.csv')

# Create height intervals for all data first
df['father_interval'] = (df['father'] // 2) * 2
df['mother_interval'] = (df['mother'] // 2) * 2
df['child_interval'] = (df['childHeight'] // 2) * 2

# Get unique fathers and mothers by family ID
unique_parents = df.groupby('family').agg({
    'father': 'first',
    'mother': 'first'
}).reset_index()

# Create height intervals for unique parents
unique_parents['father_interval'] = (unique_parents['father'] // 2) * 2
unique_parents['mother_interval'] = (unique_parents['mother'] // 2) * 2

# Calculate mean child height for each parent height interval
father_child = df.groupby('father_interval')['childHeight'].agg(['mean', 'count']).reset_index()
mother_child = df.groupby('mother_interval')['childHeight'].agg(['mean', 'count']).reset_index()

# Create a figure with two subplots side by side
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Create interval labels
father_child['interval_label'] = father_child['father_interval'].astype(str) + '-' + (father_child['father_interval'] + 2).astype(str)
mother_child['interval_label'] = mother_child['mother_interval'].astype(str) + '-' + (mother_child['mother_interval'] + 2).astype(str)

# Plot father's height intervals vs average child height
ax1.bar(father_child['interval_label'], father_child['mean'], alpha=0.8)
ax1.set_xlabel("Father's Height Intervals (inches)")
ax1.set_ylabel("Average Child Height (inches)")
ax1.set_title("Father's Height vs Average Child Height")
ax1.tick_params(axis='x', rotation=45)

# Plot mother's height intervals vs average child height
ax2.bar(mother_child['interval_label'], mother_child['mean'], alpha=0.8, color='orange')
ax2.set_xlabel("Mother's Height Intervals (inches)")
ax2.set_ylabel("Average Child Height (inches)")
ax2.set_title("Mother's Height vs Average Child Height")
ax2.tick_params(axis='x', rotation=45)

# Add number of samples in each bar
for i, v in enumerate(father_child['mean']):
    ax1.text(i, v, f'n={father_child["count"][i]}', ha='center', va='bottom')
for i, v in enumerate(mother_child['mean']):
    ax2.text(i, v, f'n={mother_child["count"][i]}', ha='center', va='bottom')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Instead of plt.show(), save to file
plt.savefig('height_comparison_bars.png')

# Create frequency distributions first
# Create height intervals for children
df['child_interval'] = (df['childHeight'] // 2) * 2
child_freq = df.groupby('child_interval')['childHeight'].count().reset_index()
child_freq.columns = ['interval', 'frequency']
child_freq['interval_label'] = child_freq['interval'].astype(str) + '-' + (child_freq['interval'] + 2).astype(str)

# Get frequency distributions for unique parents
father_freq = unique_parents.groupby('father_interval').size().reset_index(name='frequency')
mother_freq = unique_parents.groupby('mother_interval').size().reset_index(name='frequency')

# Create interval labels
father_freq['interval_label'] = father_freq['father_interval'].astype(str) + '-' + (father_freq['father_interval'] + 2).astype(str)
mother_freq['interval_label'] = mother_freq['mother_interval'].astype(str) + '-' + (mother_freq['mother_interval'] + 2).astype(str)

# Now create ogive plots
fig2, (ax3, ax4, ax5) = plt.subplots(1, 3, figsize=(18, 6))

# Calculate cumulative frequencies
father_cum = father_freq.sort_values('father_interval')
mother_cum = mother_freq.sort_values('mother_interval')
child_cum = child_freq.sort_values('interval')

# Calculate cumulative frequencies for children (remove duplicate line)
# child_cum = child_freq.sort_values('interval')  # Remove this duplicate line

# Calculate cumulative percentages
father_cum['cumulative_count'] = father_cum['frequency'].cumsum()
mother_cum['cumulative_count'] = mother_freq['frequency'].cumsum()
child_cum['cumulative_count'] = child_freq['frequency'].cumsum()

father_cum['cumulative_percentage'] = (father_cum['cumulative_count'] / father_cum['frequency'].sum()) * 100
mother_cum['cumulative_percentage'] = (mother_cum['cumulative_count'] / mother_cum['frequency'].sum()) * 100
child_cum['cumulative_percentage'] = (child_cum['cumulative_count'] / child_cum['frequency'].sum()) * 100

# Plot father's height ogive (unique families)
ax3.plot(father_cum['father_interval'], father_cum['cumulative_percentage'], 
         marker='o', linestyle='-', linewidth=2, color='blue')
ax3.set_xlabel("Father's Height (inches)")
ax3.set_ylabel("Cumulative Percentage (%)")
ax3.set_title("Ogive for Father's Height Distribution\n(Unique Families)")
ax3.grid(True)

# Plot mother's height ogive (unique families)
ax4.plot(mother_cum['mother_interval'], mother_cum['cumulative_percentage'], 
         marker='o', linestyle='-', linewidth=2, color='orange')
ax4.set_xlabel("Mother's Height (inches)")
ax4.set_ylabel("Cumulative Percentage (%)")
ax4.set_title("Ogive for Mother's Height Distribution\n(Unique Families)")
ax4.grid(True)

# Plot child's height ogive
ax5.plot(child_cum['interval'], child_cum['cumulative_percentage'], 
         marker='o', linestyle='-', linewidth=2, color='green')
ax5.set_xlabel("Child Height (inches)")
ax5.set_ylabel("Cumulative Percentage (%)")
ax5.set_title("Ogive for Child Height Distribution")
ax5.grid(True)

# Adjust layout and save the second figure
plt.tight_layout()
plt.savefig('height_comparison_ogive.png')

# Create third figure for frequency distributions
fig3, (ax5, ax6, ax7) = plt.subplots(1, 3, figsize=(18, 6))

# Plot frequency distributions
ax5.bar(child_freq['interval_label'], child_freq['frequency'], alpha=0.8, color='green')
ax5.set_xlabel("Child Height Intervals (inches)")
ax5.set_ylabel("Frequency")
ax5.set_title("Child Height Distribution")
ax5.tick_params(axis='x', rotation=45)

ax6.bar(father_freq['interval_label'], father_freq['frequency'], alpha=0.8, color='blue')
ax6.set_xlabel("Father's Height Intervals (inches)")
ax6.set_ylabel("Frequency")
ax6.set_title("Father Height Distribution (Unique Families)")
ax6.tick_params(axis='x', rotation=45)

ax7.bar(mother_freq['interval_label'], mother_freq['frequency'], alpha=0.8, color='orange')
ax7.set_xlabel("Mother's Height Intervals (inches)")
ax7.set_ylabel("Frequency")
ax7.set_title("Mother Height Distribution (Unique Families)")
ax7.tick_params(axis='x', rotation=45)

# Add frequency numbers on top of each bar
for i, v in enumerate(child_freq['frequency']):
    ax5.text(i, v, str(v), ha='center', va='bottom')
for i, v in enumerate(father_freq['frequency']):
    ax6.text(i, v, str(v), ha='center', va='bottom')
for i, v in enumerate(mother_freq['frequency']):
    ax7.text(i, v, str(v), ha='center', va='bottom')

# Adjust layout and save the third figure
plt.tight_layout()
plt.savefig('height_frequency_distributions.png')
