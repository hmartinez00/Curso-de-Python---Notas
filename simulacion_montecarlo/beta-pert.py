import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
 # Define the parameters of the beta-pert distribution
alpha = 4
beta = 4
minimum = 0
maximum = 1
 # Generate x values from 0 to 1
x = np.linspace(0, 1, 1000)
 # Calculate the y values using the beta-pert distribution
y = beta.pdf(x, alpha, beta, loc=minimum, scale=maximum-minimum)
 # Plot the beta-pert distribution
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.title('Beta-PERT Distribution')
plt.grid(True)
# plt.show()

# Save the plot as a PNG file
plt.savefig('beta_pert_distribution.png')

# Display a message once the file is saved
print("Plot saved as beta_pert_distribution.png")