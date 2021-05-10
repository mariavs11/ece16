
import numpy as np

data = np.array([[1,2,3],[4,5,6],[7,8,9]])
filename = "test.csv"

# Save the data as 3 rows in a CSV text file
np.savetxt(filename, data, delimiter=",")

# Load the data as a 3x3 array and print it
data = np.genfromtxt(filename, delimiter=",")
print(data)
