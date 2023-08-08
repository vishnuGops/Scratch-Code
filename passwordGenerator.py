import random
import string


def generate_password(length=12, use_digits=True, use_special_chars=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def main():
    print("Welcome to the Password Generator!")
    length = int(input("Enter the desired password length: "))
    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_special_chars = input(
        "Include special characters? (y/n): ").lower() == 'y'

    password = generate_password(length, use_digits, use_special_chars)

    print("Generated Password:", password)


if __name__ == "__main__":
    main()
