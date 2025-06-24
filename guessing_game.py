import random

print("Program started")

print("Setting up welcome message")
print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

print("Generating random number...")
secret_number = random.randint(1, 100)
print(f"Secret number is: {secret_number}")  # You'll see the answer for debugging

guess_count = 0
max_attempts = 10
print(f"Initial guess_count: {guess_count}, max_attempts: {max_attempts}")

while guess_count < max_attempts:
    print(f"--- Start of loop iteration {guess_count + 1} ---")
    try:
        guess = int(input(f"Attempt {guess_count + 1}/{max_attempts}. Enter your guess: "))
        print(f"User entered: {guess}")
    except ValueError:
        print("Error: Invalid input - not a number")
        continue
    
    guess_count += 1
    print(f"Updated guess_count: {guess_count}")
    
    if guess == secret_number:
        print("Condition: guess == secret_number is True")
        print(f"Congratulations! You guessed the number in {guess_count} attempts!")
        break
    elif guess < secret_number:
        print("Condition: guess < secret_number is True")
        print("Too low! Try a higher number.")
    else:
        print("Condition: guess > secret_number is True")
        print("Too high! Try a lower number.")
    
    if guess_count == max_attempts:
        print("Condition: guess_count == max_attempts is True")
        print(f"Game over! You've used all {max_attempts} attempts.")
        print(f"The secret number was {secret_number}.")
    
    print(f"--- End of loop iteration {guess_count} ---")

print("Program finished")