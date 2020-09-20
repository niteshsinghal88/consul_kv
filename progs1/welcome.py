#print ("Welcome Nitesh")

name1 = "Nitesh"
name2 = "Singhal"
print('Hi, I will count my childres', 1+1)
print("Hi, roosters", 100 - 25 * 3 % 4)
print("2 + 2 * 2 / 2 * 2 = ", 2 + 2 * 2 / 2 * 2)
print('It is true that 3 + 2 > 7 - 5 ?', 3 + 2 > 7 - 5)
print('Hi I am {0}, {1}'. format(name1,name2))

##List
TTname = ["nitesh", "Amit", "Ankit", "Arti"]

#print (TTname[-3])

## For Loop
for name in TTname:
    print("Student name is {0}".format(name))
x = 0
for x in range(10):
    x = x+10
    print("The value of x is {0}".format(x))