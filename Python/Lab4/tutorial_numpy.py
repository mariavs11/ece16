import numpy as np

#Initializing arrays
array1= np.array([0, 10, 4, 12])
array1substracted = array1 -20 # does not change array1 elements
#print(array1) # prints [-20 -10 -16 -8]
#print(array1.shape) # prints (4, )

array2 = np.array([[0, 10, 4, 12], [1, 20, 3, 41]])
#print(array2)
array2_new1 = array2[0:1,2:] # creates row 1 for array2_new
array2_new2 = array2[1:2,:2] # creates row 2 for array2_new
array2_new = np.vstack((array2_new1, array2_new2)) # stacks vertically the two vectors
#print(array2_new)


#Question 3
#print(array1)

a = np.hstack((array1,array1))# stack horizontally
array3= np.vstack((a,a,a,a)) # stacks vertically
#print(array3)

#Question 4

array4a= np.arange(-3,16,6) # array that starts at -7 with a step of -2 and that stops at 15
#print(array4a)
array4b = np.arange(-7,-20, -2)
#print(array4b)

#Question 5
array5 = np.linspace(0,100,49,True) # returns 49 numbers from 0 to 100 evenly spaced
#
#print(array5)
# Unlike arange, linspace does not define a step size, instead it returns
# X numbers evenly spaced within a range

# Question 6
array6 = np.array([[12, 3, 1, 2],[0,0, 1, 2 ],[4 ,2 ,3 ,1 ]])
'''
print(array6[0])     # [12 3 1 2]
print(array6[1, 0])  # 0
print(array6[:, 1])  # [3 0 2]
print(array6[2, :2]) # [4 2]
print(array6[2, 2:]) # [3 1]
print(array6[:, 2])  # [1 1 3]
print(array6[1, 3])  # 2
'''
#Question 7
string7 = "1,2,3,4"
string7 = string7.split(",") # returns a list
array6_1 = np.array(string7,int)
array6= np.array(string7,int)
for x in range(99):
    array6 = np.vstack((array6,array6_1))
print(array6.shape) # prints (100,4)
