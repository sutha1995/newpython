#Exercise 1
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, 3.14, True]
empty_list = []

#Accessing list elements
print(fruits[0])  # Output: apple   
print(fruits[-1]) # Output: orange
print(numbers[1:4])  # Output: [2, 3, 4]
print(numbers[:3])   # Output: [1, 2, 3]
print(numbers[2:])   # Output: [3, 4, 5]

#CRUD operations
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, 3.14, True]
empty_list = []

fruits.append("grape")  # Add an element to the end of the list
fruits.insert(1, "kiwi")  # Insert an element at a specific index
fruits.remove("banana")  # Remove an element by value
popped = fruits.pop()  # Remove and return the last element
fruits.sort()  # Sort the list in place
fruits.reverse()  # Reverse the order of the list

# List operations
len(fruits) #Length
"apple" in fruits #Membership
fruits + ["mango"] #Concatenation
fruits * 2  # Repetition

print(fruits)  # Output: ['orange', 'kiwi', 'apple']
print(len(fruits))  # Output: 3

