def a():
    c=input("Enter the temperature in Celsius: ")
    f=9/5*float(c)+32
    print("The temperature in Fahrenheit is: ", f)
def b():
    c=input("Enter the temperature in Fahrenheit: ")
    f=5/9*(float(c)-32)
    print("The temperature in Celsius is: ", f)
def c():
    c=input("Enter the temperature in Celsius: ")
    k=float(c)+273.15
    print("The temperature in Kelvin is: ", k)
def d():
    c=input("Enter the temperature in Kelvin: ")
    k=float(c)-273.15
    print("The temperature in Celsius is: ", k)
def e():
    c=input("Enter the temperature in Fahrenheit: ")
    k=5/9*(float(c)-32)+273.15
    print("The temperature in Kelvin is: ", k)
def f():
    c=input("Enter the temperature in Kelvin: ")
    k=9/5*(float(c)-273.15)+32
    print("The temperature in Fahrenheit is: ", k)
while(True):
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Fahrenheit to Kelvin")
    print("6. Kelvin to Fahrenheit")
    print("7. Exit")
    choice=input("Enter your choice: ")
    if choice=='1':
        a()
    elif choice=='2':
        b()
    elif choice=='3':
        c()
    elif choice=='4':
        d()
    elif choice=='5':
        e()
    elif choice=='6':
        f()
    elif choice=='7':
        print("   Thank You   ")
        break
    else:
        print("Invalid choice. Please try again.")
    