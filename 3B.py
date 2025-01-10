import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Seed for reproducibility
np.random.seed(0)

# Example data
mu = 90  # Mean of distribution
sigma = 25  # Standard deviation of distribution
x = mu + sigma * np.random.randn(5000)  # Generate random data
num_bins = 25

# Create figure and axis
fig, ax = plt.subplots()

# Plot histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=True, alpha=0.6, color='g')

# Add a 'best fit' line
y = stats.norm.pdf(bins, mu, sigma)  # Compute PDF
ax.plot(bins, y, '--', color='blue', label='Best Fit Line')

# Set labels and title
ax.set_xlabel('Example Data')
ax.set_ylabel('Probability Density')
sTitle = (
    f'Histogram with {len(x)} entries into {num_bins} bins:\n'
    f'$\\mu={mu}$, $\\sigma={sigma}$'
)
ax.set_title(sTitle)

# Add a legend
ax.legend()

# Adjust layout
fig.tight_layout()

# Save figure
sPathFig = 'C:/Users/Rohsn Chimbaikar/PycharmProjects/Data-Science_Practicals/Processed Data/DU-Histogram.png'
fig.savefig(sPathFig)

# Show plot
plt.show()
