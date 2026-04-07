#Functions
#Functions with parameters
def greet_person(name):
    print(f"Hello, {name}!")    

greet_person("Alice")

#Functions with return values
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(result)  # Output: 8

#Default parameters
def greet_with_title(name, title="Mr."):
    return f"Hello, {title} {name}!"

print(greet_with_title("Smith"))  # Output: Hello, Mr. Smith!
print(greet_with_title("Johnson", "Dr."))  # Output: Hello, Dr. Johnson!

#args
# *args - variable number of arguments
def sum_all(*args):
    return sum(args)    

print(sum_all(1, 2, 3, 4, 5))  # Output: 15

#kwargs
# **kwargs - keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="New York")

# Combining *args and **kwargs
def flexible_function(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

flexible_function(1, 2, 3, name="Alice", age=25)

# Lambda functions (anonymous functions)
square = lambda x: x ** 2
print(square(5))  # Output: 25

add = lambda x, y: x + y
print(add(3, 4))  # Output: 7

#Exercise 1: Prime Number Checker
# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Test the prime function
print(is_prime(2))   # True
print(is_prime(3))   # True
print(is_prime(4))   # False
print(is_prime(17))  # True
print(is_prime(18))  # False

# Exercise 2: Temperature Converter (Celsius to Fahrenheit)
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

# Test the temperature converter
print(celsius_to_fahrenheit(0))    # 32.0
print(celsius_to_fahrenheit(100))  # 212.0
print(celsius_to_fahrenheit(25))   # 77.0