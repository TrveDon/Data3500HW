num1 = int(input("Enter a number: "))
num2 = int(input("Enter another number: "))

diglist = []

for i in range(num1):
    diglist.append([])
for i in range(1, num1 +1):
    for j in range(1, num2 +1):
        diglist[i-1].append(i*j)

for i in range(num1):
    for j in range(num2):
        print(diglist[i][j], end="   ")
    print()

dict = {}

dict['age'] = int(input("Enter your age: "))
dict["fav color"] = input("Enter your favorite color: ")
dict["Mult Table"] = diglist

for key in dict.keys():
    print(key, dict[key])

import json
with open("person-2.json") as file:
    person = json.load(file)
print(person["age"])
person["age"] += 1
print(person["age"])
with open("person-2.json", "w") as file:
	json.dump(person, file, indent=4)