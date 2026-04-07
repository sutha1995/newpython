student = {
    "name" : "Alice",
    "age" : 20,
    "grade" : "A",
    "courses" : ["Math", "Science", "English"]
}

#Accessing and modifying
print(student["name"])  # Output: Alice
print(student.get("age"))  # Output: 20
student["age"] = 21       #Modify value
student["email"] = "alice@email.com" #Add new key-value

print(student.get("email"))

#Exercise 2 (Iterating Dictionaries)
keys = student.keys()     #Get all keys
values = student.values() #Get all values
items = student.items()   #Get all key-value

print(keys)
print(values)
print(items)

#Exercise 3
for key in student:
    print(f"{key}: {student[key]}")

for key, value in student.items():
    print(f"{key}: {value}")

#Exercise 4 (Nested Dictionaries)
company = {
    "employess" : {
        "john" : {"age": 30, "department": "IT"},
        "jane" : {"age": 25, "department": "HR"}
    },
    "departments" : ["IT", "HR", "Finance"]
}

print (company["employess"].items())
print(company["departments"])
