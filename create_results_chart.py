"""
Simple bar chart generator for Research Scanner results
Run this, it creates results_chart.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Your actual test data
domains = [
    'AI & ML',
    'Physics\n(Quantum)',
    'Biology\n(Genetics)',
    'Medical\n(Cardiac)',
    'Astronomy',
    'Aerospace',
    'Geology',
    'Archaeology'
]

percentages = [97.7, 96.0, 86.7, 74.0, 70.0, 44.0, 42.4, 34.4]
papers = [44, 50, 98, 50, 50, 50, 99, 93]

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Color gradient - green for good, yellow for okay, red for needs work
colors = []
for p in percentages:
    if p >= 85:
        colors.append('#2ecc71')  # Green
    elif p >= 60:
        colors.append('#f39c12')  # Orange
    else:
        colors.append('#e74c3c')  # Red

# Create horizontal bar chart
bars = ax.barh(domains, percentages, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

# Add percentage labels at end of bars
for i, (bar, pct, num) in enumerate(zip(bars, percentages, papers)):
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
            f'{pct}%  ({num} papers)',
            ha='left', va='center', fontsize=11, fontweight='bold')

# Add average line
avg = 67.6
ax.axvline(avg, color='#34495e', linestyle='--', linewidth=2, label=f'Average: {avg}%')

# Styling
ax.set_xlabel('Relevance (%)', fontsize=14, fontweight='bold')
ax.set_title('Research Scanner v1.0 - Relevance by Domain', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(0, 105)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.legend(fontsize=12, loc='lower right')

# Add color legend
green_patch = mpatches.Patch(color='#2ecc71', label='Excellent (≥85%)')
orange_patch = mpatches.Patch(color='#f39c12', label='Good (60-84%)')
red_patch = mpatches.Patch(color='#e74c3c', label='Needs Work (<60%)')
ax.legend(handles=[green_patch, orange_patch, red_patch], 
         loc='lower right', fontsize=10)

# Tight layout
plt.tight_layout()

# Save
output_path = 'D:/Claude/Projects/scholars-terminal/results_chart.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"[OK] Chart saved to: {output_path}")
print(f"     Size: High resolution (300 DPI)")
print(f"     Ready for Medium!")

# Also save a version for web (smaller file)
output_web = 'D:/Claude/Projects/scholars-terminal/results_chart_web.png'
plt.savefig(output_web, dpi=150, bbox_inches='tight', facecolor='white')
print(f"[OK] Web version saved to: {output_web}")

plt.close()
