import random
import string

# function for password generation
def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special):
    # Creating pool of characters based on user preferences
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    # Ensureing at least one type of character is selected
    if not characters:
        raise ValueError("At least one character type must be selected.")

    # Generating password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# function to check for affirmative responses & user typo mistakes
def is_yes(response):
    return response.lower() in ['yes', 'y', 'ye', 'ys', 'es', 'yeah', 'yep', 'yess','1']

while True:
    # Getting user input password length
    while True:
        try:
            length = int(input("Enter Desired Password Length (minimum 8): "))
            if length < 8:
                raise ValueError("Password length must be at least 8.")
            break  # Exiting inner loop if the length is valid
        except ValueError:
            print("Invalid input! Please enter a number that is 8 or greater.")

    # Getting user preferences for character types
    use_uppercase = is_yes(input("Include uppercase letters? (yes/no): "))
    use_lowercase = is_yes(input("Include lowercase letters? (yes/no): "))
    use_digits = is_yes(input("Include digits? (yes/no): "))
    use_special = is_yes(input("Include special characters? (yes/no): "))

    # Checking if at least one type is selected
    if not (use_uppercase or use_lowercase or use_digits or use_special):
        print("You must pick at least one character type.")
        continue  # Asking for inputs again

    # Generating & displaying the password
    try:
        password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
        print(f"Generated Password: {password}")
    except ValueError as e:
        print(f"Error: {e}")

    # Ask if the user wants to generate another password
    if not is_yes(input("Would you like to generate another password? (yes/no): ")):
        print("Thank you for using my Password Generator!")
        break  # Exit outer loop
