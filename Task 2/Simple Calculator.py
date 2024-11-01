
print("\nWelcome, This is my Simple Calculator :D")

# Function for addition
def add(x, y):
    print(x, "+", y, "=", x + y)  # Print the result of the addition
    return

# Function for subtraction
def sub(x, y):
    print(x, "-", y, "=", x - y)  # Result of the subtraction
    return

# Function for multiplication
def multi(x, y):
    print(x, "x", y, "=", x * y)  # Result of the multiplication
    return

# Function for division
def div(x, y):
    print(x, "/", y, "=", x / y)  # Result of the division
    return

while True:
    print("\nPick an Operation:", "1. Addition", "2. Subtraction", "3. Multiplication", "4. Division", "5. Exit",
          sep="\n", end="\n")
    choice = input()

    if choice == '5':
        print("Goodbye~Then!")
        break  # Break the loop and end the program
    elif choice in ('1', '2', '3', '4'):
        x = float(input("\n\nPlease, Enter The First Number: "))
        y = float(input("\nPlease, Enter The Second Number: "))

        # Perform the corresponding operation based on user input
        if choice == '1':
            add(x, y)
        elif choice == '2':
            sub(x, y)
        elif choice == '3':
            multi(x, y)
        elif choice == '4':
            div(x, y)
    # If the user enters an invalid choice
    else:
        print("Invalid Choice. Pick Again.")

    # Ask if user wants to perform another operation
    another_operation = input("\nWould you like to perform another operation? (yes/no): ").lower()  # To ensure that the answer is consistent

    # Simple string matching for variations of 'yes'
    if another_operation not in ('yes', 'y', 'ye', 'ys', 'es', 'yeah', 'yep','yess'):
        print("Goodbye~Then!")
        break
