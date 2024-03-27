"""
    Check the get method of a dict
"""

qwe = dict()

qwe["qwe"] = 1

if qwe.get("asd"):
    print("It is a type safe")
else:
    print(f"It is a type safe (from else) : {qwe.get('asd')}")

if qwe.get("qwe"):
    print("It isads a type safe")
else:
    print("It is aasdsad type safe (from else)")

print("\n\nTest3: check if I can compare the None value to string\n")

if qwe.get("asd") == "qwe":
    print("It is a type safe")
else:
    print(f"It is a type safe (from else) : {qwe.get('asd')}")
