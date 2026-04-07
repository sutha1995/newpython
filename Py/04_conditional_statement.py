#Exercise 1.1
age = 18

if age >= 18: 
    print("You're an adult.")
else:
    print("You're a minor.")

#Exercise 1.2
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"         
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is: {grade}")

#Exercise 2.1
user_age = 25
has_license = True

if user_age >= 18 and has_license:
    print("You are allowed to drive.")
else:
    print("You are not allowed to drive.")

