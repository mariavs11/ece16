import matplotlib.pyplot as plt
import numpy as np

x = [1,2,3,4]  # x data vector (as a list)
y = [1,4,9,16] # y data vector (as a list)
plt.clf()      # clear any existing plot
plt.plot(x,y)  # write the data onto the figure buffer
plt.show()     # show the figure


a = np.array([[1,2,3,4],[1,4,9,16]])  # row 1 acts like values in the x-axis and row 2 like values in the y-axis
plt.clf()
plt.plot(a)
plt.show()

plt.clf()
a = np.array([[1,2,3,4],[1,4,9,16]])
x = a[0,:] #index from a to get [1,2,3,4]
y = a[1,:] #index from a to get [1,4,9,16]
plt.title("First plot!")
plt.xlabel("x") # labels the plot at the x-axis
plt.ylabel("y") # labels the plot at the y-axis
plt.plot(x,x) # array x will contain the values for both axes
plt.plot(x,y) # array x determines the values in the x-axis, array y determined the values in the y-axis
plt.show() # plots on the same figure


plt.clf()
plt.subplot(211)
plt.plot([1,2,3,4],[1,4,9,16])
plt.subplot(212)
plt.plot([1,2,3,4],[4,2,1,6])
plt.show()





