#EXERCISE
#0.3 EXERCISES

#1. creates list_1
list_1 = [1, 2, 3, 4, 5, 6, 7, 8,9 ,10]
print("this is list_1"+ str(list_1))
#2 creates list_2
list_2 = [ 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
print("this is list_2 :"+ str(list_2))
#3 replaces first 3 elements of list_1
list_1[0:3]= ["one", "two", "three"]
#i. prints list_1 after replacing the first 3 elements
print("this is list1 after replacing the first 3 elements :"+ str(list_1))

#4 creates tuple and assigns it to the first 3 elements of list_2
#i
tuple_list2 =("eleven", "twelve", "thirteen")
list_2 [0:3]= tuple_list2
print("this is list_2 after replacing the first 3 elements:"+ str(list_2))

#5 joins the two lists into a new list in 2 different ways
#i Using .extend()
joint_1 = list_1[:] # makes copy of list_1 and saves it into joint_1
joint_1.extend(list_2) # joint_1 = list_1 + list_2
#ii Using the "+" operator
joint_2 = list_1 + list_2
#iii prints output
print("this is joint_1 (using .extend()) :" +str(joint_1))
print("this is joint_2 (using the "+" operator ):" +str(joint_2))


#6 adds new elements to joint_2 while maintaining its fixed length
def appendtolist(base_list, new_data):
    length1 = len(base_list)
    base_list = base_list + new_data # base_list + new_data
    length2 = len(base_list )
    base_list = base_list[(length2-length1):] # shifts the list to the left in a way such that the list maintains a fixed length
    return base_list

new_data = [7,8,9]

x = appendtolist(joint_2, new_data) # adds new elements to the list while maintaining a fixed length
print(x)

#1.4 EXERCISES

#1. creates list of commands
commands = ["STATUS", "ADD", "COMMIT", "PUSH"]
#2 iterates through list and prints it to the console
for x in commands :
    print(x)
#3. creates another list
responses = ["PUSH FAILED", "BANANAS", "PUSH SUCCESS", "APPLES"]
#4. assign "success" to variable text
text="SUCCESS"

#5
#i.
if("SUCCESS" in "SUCCESS"):  # compares char by char
    print("Yes")
else:
    print("No")
#ii.
if("SUCCESS" in "ijoisafjoijiojSUCCESS"): # compares char by char
    print("Yes")
else:
    print("No")
#iii.
if("SUCCESS" == "ijoisafjoijiojSUCCESS"):  # compares the whole string
    print("Yes")
else:
    print("No")

#iv.
if("SUCCESS" == text):    # compares the whole string
    print("Yes")
else:
    print("No")
#v. The if statements are either comparing the whole string (using "==" ) or the presence of a set of characters (using "in")

#6 while loop that loops over the list from step 3. Print each word unless it contains the string from step 4,
# in which case you should exit the loop and print: "This worked!"

i=0
length = len(responses)  #to find size of the list

while i < length:  #iterate through the whole list
    x = responses[i]
    if ("SUCCESS" in x ): # if "success" is encountered in x
        print("This Worked!")
        break  # leaves loop
    else:
        i+=1
        print(x)


# 2.2 EXERCISES

#1. create string containing your name
name = "maria"
#2. Encode the string to a byte array
byte_name = name.encode('utf-8')
#3.Append a non-utf-8 character
byte_name_bad = byte_name + b'\xef'

#4 Error that got detected :
#" UnicodeDecodeError: 'utf-8' codec can't decode byte 0xef in position 5: unexpected end of data"

#5
try:
    print(byte_name_bad.decode())
except:
    print("")
#6
try:
    print(byte_name.decode())
except:
    print("")