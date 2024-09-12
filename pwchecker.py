passwordchecker.py


import re
import hashlib
import requests

# Function to check the strength of the password
def check_password_strength(password):
    score = 0
    # Check length of password
    if len(password) >= 8:
        score += 1
    # Check for uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
    # Check for lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
    # Check for digits
    if re.search(r"\d", password):
        score += 1
    # Check for special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    # Evaluate the password strength
    strength = "Very Weak"
    if score == 5:
        strength = "Very Strong"
    elif score == 4:
        strength = "Strong"
    elif score == 3:
        strength = "Moderate"
    elif score == 2:
        strength = "Weak"

    return strength

# Function to check if the password has been compromised in a data breach
def check_password_breach(password):
    # Hash the password using SHA-1
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # Send only the first 5 characters of the hash to the API
    first5_char = sha1_password[:5]
    remaining_chars = sha1_password[5:]

    # Query the "Have I Been Pwned" API
    url = f"https://api.pwnedpasswords.com/range/{first5_char}"
    response = requests.get(url)

    # Check if the response contains the hash
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == remaining_chars:
            return f"Warning: Your password has been found in a data breach {count} times!"
    return "Good news: Your password has not been found in any data breaches."

# Main function to run the tool
def main():
    password = input("Enter a password to check: ")
    strength = check_password_strength(password)
    print(f"Password strength: {strength}")
    
    # Check if the password has been compromised
    breach_check = check_password_breach(password)
    print(breach_check)

if __name__ == "__main__":
    main()
