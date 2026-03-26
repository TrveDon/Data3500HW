list = ['Blue','White','Red']
msg = "My Favorite colors are: "
msg += ', '.join(list)
print(msg)

adrs =input("Enter Your Address: ")
adrs.strip()
adrs.replace(" ",'')
adrs.replace(".",'')
adrs.replace(",",'')
print("Address:", adrs, adrs.isalnum())
