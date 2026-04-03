for i in range(5):
    print(i)       #0,1,2,3,4

for i in range(1, 6):
    print(i)       #1,2,3,4,5 

for i in range(0, 10, 2):
    print(i)       #0,2,4,6,8           

#While loop
count = 0   
while count < 5:
    print(count)   #0,1,2,3,4
    count += 1     #count = count + 1   

  # Exercise 1
  # While Loop
count = 0
while count < 5:
    print(count)   #0,1,2,3,4
    count += 1     #count = count + 1  

#Loop control statements
for i in range(10):
    if i == 3:
        continue    #Skip the rest of the loop and move to the next iteration
    if i == 7:  
        break       #Exit the loop completely       
    print(i)       

#Nested loops
for i in range(2):
    for j in range(3):
        print(f"i: {i}, j: {j}")    

#Exercise 2
#Create a multiplication table generator
n = 5  # change this value for a different size table
print(f"\nMultiplication table for 1 through {n}:")
for i in range(1, n + 1):
    row = " ".join(str(i * j) for j in range(1, n + 1))
    print(row)

#Exercise 3
#Write a program that finds all prime numbers up to a given limit
limit = 20
print(f"\nPrime numbers up to {limit}:")
for num in range(2, limit + 1):
    for div in range(2, int(num ** 0.5) + 1):
        if num % div == 0:
            break
    else:
        print(num, end=" ")
print()