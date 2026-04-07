#Exercise 5: Student Records
student_records = {
    "student_001": {
        "name": "John",
        "age": 19,
        "major": "Computer Science",
        "grades": [85, 92, 78]
    },
    "student_002": {
        "name": "Sarah",
        "age": 20,
        "major": "Biology",
        "grades": [90, 88, 95]
    },
}

# Function to add a new student
student_records["student_003"] = {
    "name": "Mike",
    "age": 18,
    "major": "Math",
    "grades": [82, 79, 91]
}

#Update John's age
student_records["student_001"]["age"] = 20

# Loop through dictionary and print student information
print("\n--- Student Information ---")
for student_id, student_info in student_records.items():
    print(f"Student ID: {student_id}, Name: {student_info['name']}, Major: {student_info['major']}")