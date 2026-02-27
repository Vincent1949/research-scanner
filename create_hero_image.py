"""
Create a simple hero image for the Medium article
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure
fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Dark background
fig.patch.set_facecolor('#2c3e50')
ax.set_facecolor('#2c3e50')

# Main title
ax.text(5, 7, 'Research Scanner', 
        ha='center', va='center', 
        fontsize=60, fontweight='bold', 
        color='white', family='sans-serif')

# Subtitle
ax.text(5, 6, 'Universal Paper Discovery for Any Field', 
        ha='center', va='center', 
        fontsize=24, 
        color='#ecf0f1', family='sans-serif')

# Stats boxes
stats = [
    ('11 Templates', '#3498db'),
    ('6 Data Sources', '#2ecc71'),
    ('67.6% Avg Relevance', '#e74c3c'),
    ('Open Source', '#9b59b6')
]

x_positions = [1.5, 3.8, 6.1, 8.4]
for i, (stat, color) in enumerate(stats):
    # Box
    rect = patches.Rectangle((x_positions[i]-0.7, 3.5), 1.4, 1.5, 
                             linewidth=2, edgecolor=color, 
                             facecolor='#34495e', alpha=0.8)
    ax.add_patch(rect)
    
    # Text
    ax.text(x_positions[i], 4.25, stat, 
           ha='center', va='center',
           fontsize=14, fontweight='bold',
           color='white')

# Bottom tagline
ax.text(5, 2, 'From Physics to Medicine to AI', 
        ha='center', va='center', 
        fontsize=20, style='italic',
        color='#95a5a6')

ax.text(5, 1.2, 'One System. Any Domain. MIT License.', 
        ha='center', va='center', 
        fontsize=16,
        color='#7f8c8d')

# GitHub mention
ax.text(5, 0.4, 'github.com/Vincent1949/research-scanner', 
        ha='center', va='center', 
        fontsize=14, style='italic',
        color='#3498db', family='monospace')

plt.tight_layout()

# Save
output_path = 'D:/Claude/Projects/scholars-terminal/hero_image.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', 
           facecolor='#2c3e50', edgecolor='none')
print(f"[OK] Hero image saved to: {output_path}")
print(f"     Size: 1400x700px (perfect for Medium)")
print(f"     Ready to use!")

plt.close()
