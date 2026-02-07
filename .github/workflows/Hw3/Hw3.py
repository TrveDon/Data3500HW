#3.4
for row in range (2):
    for col in range (7):
        print('@',end='')
    print()
#
#3.9
#
x = input('Enter a Five Digit Number: ')
for digit in x:
    print(digit)
#
#3.11
#
calc =[]
for Tank in range (3):
    print(f"Tank {Tank + 1}")
    GalUsed = int(input("Enter Gallons Used: "))
    Miles = int(input('Enter Miles Driven: '))
    Milepergal = Miles / GalUsed
    print ('The MPG for this tank was: ', Milepergal)
    calc.append(Milepergal)
MPGAverage = sum(calc) / len(calc)
print("Average MPG: ", MPGAverage)
#
#3.12
#
Pal = input("Enter a Five Digit Number: ")
if Pal == Pal[::-1]:
    print ("This is a Palindrome")
else: 
    print('This is not a Palindrome')
#
#3.14
#
pi = 0
sign = 1 
z = 1
#displays 3.14
while abs(pi-3.14) > 0.0001:
    pi += sign * (4/z)
    sign *= -1
    z += 2 
print(pi)
print("Terms Used", (z+1)//2)
#Displays 3.141
while abs(pi-3.141) > 0.00001:
    pi += sign * (4/z)
    sign *= -1
    z += 2 
print(pi)
print("Terms Used", (z+1)//2)