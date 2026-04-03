#Exercise 1

single_quote = 'Hello'
double_quote = "World"
triple_quote = """Multi-line string"""

#Exercise 2

text = "Python Programming"

print(text[0])      #first character
print(text[-1])     #last character
print(text[0:6])    #slice 0 to 5
print(text[:6])     #from start to 5
print(text[7:])     #7 to end

#Exercise 3

name = " bob the builder "

print(len(name))                        #Length
print(name.strip())                     #Removes whitespace
print(name.upper())                     #Uppercase
print(name.lower())                     #Lowercase
print(name.title())                     #Title case
print(name.replace("bob", "jane"))      #Replace

#Exercise 4

name = "Jane Doe"
age = 30

message_1 = f"My name is {name} and I am {age} years old."          #f-strings
message_2 = "My name is {} and I am {} years old".format(name, age) #str.format
message_3 = "My name is %s and I am %d years old." % (name, age)    #%-formatting

print(message_1)
print(message_2)
print(message_3)