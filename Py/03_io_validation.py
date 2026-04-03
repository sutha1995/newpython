name = input("Enter your name: ")
height = float(input("Enter your height: ")) #Convert to float

#Input validation
while True:
    try:
        age = int(input("Enter your age: "))
        if age > 0:
            break
        else:
            print("Age must be positive!")
    except ValueError:
        print("Please enter a valid number!")

#Output validation
print(f"Hello {name}!")
print(f"You are {age} years old and {height} centimeters tall.")

#Exercise 1
number1 = float(input("Please enter number 1: "))
number2 = float(input("Please enter number 2: "))
