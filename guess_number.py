import pygame
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import time 

# Function to play sound effects using Pygame
def play_sound(file_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)    # Load the sound file
    sound.play()

# Function to start the game
# This validates the range input and initiates the guessing game.
def start_game():
    try:
        # Get the number range from the user inputs (lower and upper bounds)
        low = int(low_entry.get())
        high = int(high_entry.get())

        if low >= high:
            messagebox.showwarning("Invalid range", "The lower bound must be less than the upper bound.")
            return
        
        # Close the range selection window and begin the game with the specified range
        range_window.destroy()
        guess_number(low, high)

    except ValueError:   # If the user input is not a valid number, show a warning
        messagebox.showwarning("Invalid input", "Please enter valid numbers for the range.")

# Function for the main guessing game logic
def guess_number(low, high):
    guess = (low + high) // 2    # Start with a middle guess between the range
    guess_count = 0   # Keep track of the number of guesses
    start_time = time.time()  
    emoji_states = ["🙂", "😐", "😕", "🙁", "😖", "😩"]  # Different emoji states for feedback
    guesses = []  # List to store all the guesses made by the game

    # Function to update the guess based on user feedback
    def update_guess():
        nonlocal low, high, guess, guess_count
        guess_count += 1 
        guesses.append(guess)

        # If the feedback is 's' (the number is smaller), update the range
        if feedback.get() == 's':
            high = guess - 1   # Adjust the upper bound
            play_sound('mind-reader\\number-guessing-challenge\\sounds\\wrong_guess.wav') 
            root.configure(bg='red')  # Change window background to red for incorrect guess
            emoji_label.config(bg='red')  # Change emoji background to red
        elif feedback.get() == 'b':  # Adjust the lower bound
            low = guess + 1
            play_sound('mind-reader\\number-guessing-challenge\\sounds\\wrong_guess.wav') 
            root.configure(bg='red')  
            emoji_label.config(bg='red')  
        # If the feedback is 'c' (correct guess), finish the game
        elif feedback.get() == 'c':
            play_sound('mind-reader\\number-guessing-challenge\\sounds\\correct_guess.wav')
            root.configure(bg='green')   # Change window background to green for correct guess
            emoji_label.config(bg='green', text="😄")  # Change emoji to happy face
            
            end_time = time.time()  # End the timer
            total_time = round(end_time - start_time, 2)  # Calculate the total time taken
            
            # Plot the guesses made during the game using Matplotlib
            plt.plot(range(1, guess_count + 1), guesses, marker='o')
            plt.title("Guessing Game Progress")  
            plt.xlabel("Guess Number")
            plt.ylabel("Guessed Number")
            plt.grid()
            plt.axhline(y=(low + high) // 2, color='r', linestyle='--', label='Actual Number')
            plt.legend()
            plt.show() 
            
            # Show a message box with the result of the game
            messagebox.showinfo("Congratulations", f"Your number is {guess}!\n"
                                                   f"It took you {guess_count} guesses.\n"
                                                   f"Time taken: {total_time} seconds.")
            root.destroy()     # Close the game window
            return
        else:   
            # Show a warning if the input is not valid
            messagebox.showwarning("Invalid input", "Please enter 's', 'b', or 'c' only.")
        
        # Calculate the new guess based on the updated range
        guess = (low + high) // 2
        guess_label.config(text=f"Is your number {guess}?")
        
        # Clear the feedback input for the next guess
        feedback.delete(0, tk.END)

        # Update the emoji state based on the number of guesses
        if guess_count <= len(emoji_states):
            emoji_label.config(text=emoji_states[min(guess_count, len(emoji_states) - 1)])

    # GUI for the game
    root = tk.Tk()   # Create the main window
    root.title("Number Guessing Game")
    root.configure(bg='lightgray')   # Set the initial background color
    
    # Label to display the current guess
    guess_label = tk.Label(root, text=f"Is your number {guess}?", font=('Arial', 14), bg='lightgray')
    guess_label.pack(pady=20)

    # Label to ask for feedback
    feedback_label = tk.Label(root, text="Enter 's' (smaller), 'b' (bigger), 'c' (correct):", font=('Arial', 12), bg='lightgray')
    feedback_label.pack(pady=10)
    
    feedback = tk.Entry(root, font=('Arial', 12))
    feedback.pack(pady=5)

    # Emoji label to show feedback as emoji
    emoji_label = tk.Label(root, text="🙂", font=('Segoe UI Emoji', 50), bg='lightgray')  
    emoji_label.pack(pady=10)

    # Button to submit feedback and update the guess
    submit_button = tk.Button(root, text="Submit", command=update_guess, font=('Arial', 12))
    submit_button.pack(pady=10)

    # Start the GUI loop for the game
    root.mainloop()

# Function to move focus to the next widget on pressing Enter
def focus_next(event, next_widget):
    next_widget.focus()

# GUI for selecting the number range
range_window = tk.Tk()
range_window.title("Select Range")

# Label and entry for the lower bound
low_label = tk.Label(range_window, text="Enter the lower bound:", font=('Arial', 12))
low_label.pack(pady=10)

low_entry = tk.Entry(range_window, font=('Arial', 12))
low_entry.pack(pady=5)
low_entry.bind("<Return>", lambda event: focus_next(event, high_entry))   # Move focus to next entry when Enter is pressed

# Label and entry for the upper bound
high_label = tk.Label(range_window, text="Enter the upper bound:", font=('Arial', 12))
high_label.pack(pady=10)

high_entry = tk.Entry(range_window, font=('Arial', 12))
high_entry.pack(pady=5)

# Button to start the game
start_button = tk.Button(range_window, text="Start Game", command=start_game, font=('Arial', 12))
start_button.pack(pady=20)

# Start the GUI loop for the range selection
range_window.mainloop()
