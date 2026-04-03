fruits = {"apple", "banana", "orange"}
numbers = {1, 2, 3, 4, 5}

# Set operations
fruits.add("grape")  # Add an element to the set
fruits.remove("banana")  # Remove an element from the set
fruits.discard("kiwi")  # Remove an element if it exists, do nothing if it doesn't

print(fruits)  # Output: {'apple', 'orange', 'grape'}

#Exercise 2
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(set1.union(set2))  # Output: {1, 2, 3, 4, 5, 6}
print(set1.intersection(set2))  # Output: {3, 4}        
print(set1.difference(set2))  # Output: {1, 2}

#Exercise 3
# Student grade records with tuples and sets
grades = [
    ("Alice", "Math", 85),
    ("Bob", "Science", 92),
    ("Alice", "Science", 78),
    ("Charlie", "Math", 90),
    ("Bob", "Math", 88),
    ("Alice", "English", 95),
]

students = {name for (name, _, _) in grades}
subjects = {subj for (_, subj, _) in grades}

print("Unique students:", students)
print("Unique subjects:", subjects)

# optional: group by student and subject for summary
from collections import defaultdict
student_records = defaultdict(list)
for name, subj, grade in grades:
    student_records[name].append((subj, grade))

print("\nRecords by student:")
for name, records in student_records.items():
    print(name, "->", records)


