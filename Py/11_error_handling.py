#Basic exception handling
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"Result: {result}")
except ValueError:
    print("Invalid input. Please enter a valid number.")
except ZeroDivisionError:
    print("Cannot divide by zero. Please enter a non-zero number.")

#Using else and finally
try:
    file = open("data.txt", "r")
except FileNotFoundError:
    print("File not found!")
else:
    #Execute if no exceptions occur
    content = file.read()
    print("File read successfully!")
finally:
    #Always excutes
    if 'file' in locals() and not file.closed:
        file.close()
        print("Cleanup completed.")

# Raising exceptions
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")
    if age > 150:
        raise ValueError("Age cannot be greater than 150.")
    return True

try:
    validate_age(-5)
except ValueError as e:
    print(f"Validation error: {e}")