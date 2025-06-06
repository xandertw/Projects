import random

def guess_the_number():

    secret_number = random.randint(1, 100)
    attempts = 7
    print("Welcome to 'Guess the Number'!")
    print("I have selected a number between 1 and 100.")
    print(f"You have {attempts} attempts to guess it.")

    while attempts > 0:
        try:

            guess = int(input("Enter your guess: "))


            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100.")
                continue

            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You've guessed the number: {secret_number}")
                break


            attempts -= 1
            print(f"You have {attempts} attempts left.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

    if attempts == 0:
        print(f"Sorry, you've run out of attempts. The number was: {secret_number}")


guess_the_number()