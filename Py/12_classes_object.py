#Basic class definition
class Person:
    #Class attribute (shared by all instances)
    species = "Homo sapiens"

    #Constructor method
    def __init__(self, name, age):
        #Instance attributes
        self.name = name
        self.age = age

    #Instance method
    def introduce(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old."
    
    #Method with parameters
    def celebrate_birthday(self):
        self.age += 1
        return f"Happy birthday {self.name}! You are now {self.age}."
    

# Creating objects (instances)
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

# Accessing attributes
print(person1.name)  # Output: Alice
print(person1.age)   # Output: 25

# Calling methods
print(person1.introduce())  # Output: Hi, I'm Alice and I'm 25 years old.
print(person2.celebrate_birthday())  # Output: Happy birthday Bob! You are now 31.

# Class attributes
print(Person.species)  # Output: Homo sapiens
print(person1.species)  # Output: Homo sapiens

class BankAccount
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            return f"Deposited ${amount}. New balance: ${self.balance}"
        else:
            return "Invalid deposit amount."
        
    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance