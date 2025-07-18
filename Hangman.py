import random
from tkinter import *
from tkinter import messagebox
from tkinter import font as tkFont

WORDLIST_FILENAME = "dictionary.txt"

class Hangman:
    def __init__(self, master):
        self.master = master
        master.title("Hangman")
        master.geometry("1000x750")
        master.configure(bg="#FFEEF2")
        
        # Center the window
        self.center_window(master, 1000, 750)
        master.resizable(False, False)
        
        # Font configurations
        self.title_font = ("Comic Sans MS", 36, "bold")
        self.subtitle_font = ("Comic Sans MS", 14, "italic")
        self.word_font = ("Courier New", 36, "bold")  # Monospace for consistent spacing
        self.letter_font = ("Comic Sans MS", 14)
        self.button_font = ("Comic Sans MS", 14, "bold")
        self.message_font = ("Comic Sans MS", 16)
        
        # Game variables
        self.wordlist = self.loadWords()
        self.secretWord = self.chooseWord(self.wordlist).lower()
        self.lettersGuessed = []
        self.mistakeMade = 0
        self.maxGuesses = 8
        
        # Create main containers
        self.left_frame = Frame(master, bg="#FFD1DC", width=400, height=750)
        self.left_frame.pack_propagate(0)
        self.left_frame.pack(side=LEFT, fill=Y)
        
        self.right_frame = Frame(master, bg="#FFEEF2", width=600, height=750)
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Setup GUI components
        self.setup_left_panel()
        self.setup_right_panel()
        
        # Start the game
        self.updateDisplay()
    
    def center_window(self, window, width, height):
        """Center the window on the screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def loadWords(self):
        print("Loading word list from file...")
        try:
            with open(WORDLIST_FILENAME, 'r') as inFile:
                line = inFile.readline()
                wordlist = line.split()
                print("  ", len(wordlist), "words loaded.")
                return wordlist
        except:
            print("Error loading word list. Using default words.")
            return ["apple", "banana", "orange", "grape", "melon", "strawberry", "pineapple", "auscultate"]
    
    def chooseWord(self, wordlist):
        return random.choice(wordlist)
    
    def isWordGuessed(self):
        return all(letter in self.lettersGuessed for letter in self.secretWord)
    
    def getGuessedWord(self):
        # Use single spaces between letters/underscores
        displayed = []
        for letter in self.secretWord:
            if letter in self.lettersGuessed:
                displayed.append(letter)
            else:
                displayed.append("_")
        return " ".join(displayed)
    
    def getAvailableLetters(self):
        import string
        return [letter for letter in string.ascii_lowercase if letter not in self.lettersGuessed]
    
    def setup_left_panel(self):
        """Left panel with hangman drawing"""
        # Title
        title_label = Label(self.left_frame, 
                          text="Hangman Game", 
                          font=self.title_font, 
                          bg="#FFD1DC", 
                          fg="#FF5D8F")
        title_label.pack(pady=40)
        
        # Author
        author_label = Label(self.left_frame, 
                           text="by Bisma Shahid", 
                           font=self.subtitle_font, 
                           bg="#FFD1DC", 
                           fg="#FF5D8F")
        author_label.pack(pady=(0, 50))
        
        # Hangman canvas
        self.hangman_canvas = Canvas(self.left_frame, 
                                   width=350, 
                                   height=350, 
                                   bg="#FFD1DC", 
                                   highlightthickness=0)
        self.hangman_canvas.pack(pady=20)
        
        # Mistakes counter
        self.mistake_label = Label(self.left_frame, 
                                 text=f"Mistakes: {self.mistakeMade}/{self.maxGuesses}", 
                                 font=self.message_font, 
                                 bg="#FF5D8F", 
                                 fg="white",
                                 padx=20,
                                 pady=10,
                                 relief="raised",
                                 bd=3)
        self.mistake_label.pack(pady=20)
    
    def setup_right_panel(self):
        """Right panel with game controls"""
        self.right_canvas = Canvas(self.right_frame, width=600, height=750, highlightthickness=0, bg="#FFEEF2")
        self.right_canvas.pack()
        
        # Word display with proper constraints
        self.word_label = Label(self.right_canvas, 
                              text="", 
                              font=self.word_font, 
                              bg="#FFEEF2", 
                              fg="#FF5D8F",
                              wraplength=550)  # Prevents overflow
        self.right_canvas.create_window(300, 100, window=self.word_label)
        
        # Available letters grid
        letters_frame = Frame(self.right_canvas, bg="#FFEEF2")
        self.right_canvas.create_window(300, 280, window=letters_frame)
        
        Label(letters_frame, 
             text="Available Letters:", 
             font=self.letter_font, 
             bg="#FFEEF2", 
             fg="#FF5D8F").grid(row=0, column=0, columnspan=7, pady=(0, 10))
        
        # Complete alphabet grid (7x4)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letter_buttons = []
        for i, letter in enumerate(alphabet):
            btn = Button(letters_frame,
                       text=letter,
                       font=("Comic Sans MS", 14, "bold"),
                       width=3,
                       height=1,
                       bg="#FFB7C5",
                       fg="white",
                       activebackground="#FF85A1",
                       relief="raised",
                       bd=3,
                       command=lambda l=letter.lower(): self.processLetterGuess(l))
            btn.grid(row=1+i//7, column=i%7, padx=2, pady=2)
            self.letter_buttons.append(btn)
        
        # Guess entry section
        guess_frame = Frame(self.right_canvas, bg="#FFEEF2")
        self.right_canvas.create_window(300, 500, window=guess_frame)
        
        # Input box and submit button
        self.guess_entry = Entry(guess_frame, 
                                font=self.word_font, 
                                width=4, 
                                bg="white", 
                                fg="#FF5D8F", 
                                justify='center',
                                highlightthickness=2)
        self.guess_entry.grid(row=0, column=0, padx=5, pady=(0, 5))
        
        self.submit_button = Button(guess_frame,
                                  text="✓", 
                                  font=("Comic Sans MS", 18),
                                  bg="#FF9EB5",
                                  fg="white",
                                  command=self.processGuess)
        self.submit_button.grid(row=0, column=1, padx=5, pady=(0, 5))
        
        # "Or type your guess" label
        Label(guess_frame, 
             text="Or type your guess:", 
             font=self.letter_font, 
             bg="#FFEEF2", 
             fg="#FF5D8F").grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Status message
        self.status_label = Label(self.right_canvas,
                                text="", 
                                font=self.message_font, 
                                bg="#FFEEF2", 
                                fg="#FF5D8F",
                                wraplength=550)
        self.right_canvas.create_window(300, 570, window=self.status_label)
        
        # New Game button
        self.new_game_button = Button(self.right_canvas,
                                    text="New Game", 
                                    font=self.button_font,
                                    bg="#FF5D8F",
                                    fg="white",
                                    activebackground="#FF85A1",
                                    padx=25,
                                    pady=8,
                                    command=self.newGame)
        self.right_canvas.create_window(300, 650, window=self.new_game_button)
    
    def drawHangman(self):
        """Draw hangman based on mistakes"""
        self.hangman_canvas.delete("all")
        
        # Gallows
        self.hangman_canvas.create_line(50, 300, 150, 300, width=4, fill="#FF85A1")
        self.hangman_canvas.create_line(100, 300, 100, 50, width=4, fill="#FF85A1")
        self.hangman_canvas.create_line(100, 50, 200, 50, width=4, fill="#FF85A1")
        self.hangman_canvas.create_line(200, 50, 200, 80, width=4, fill="#FF85A1")
        
        # Hangman parts
        parts = [
            lambda: self.hangman_canvas.create_oval(185, 80, 215, 110, width=3, outline="#FF5D8F"),  # Head
            lambda: self.hangman_canvas.create_line(200, 110, 200, 180, width=3, fill="#FF5D8F"),     # Body
            lambda: self.hangman_canvas.create_line(200, 120, 160, 150, width=3, fill="#FF5D8F"),    # Left arm
            lambda: self.hangman_canvas.create_line(200, 120, 240, 150, width=3, fill="#FF5D8F"),    # Right arm
            lambda: self.hangman_canvas.create_line(200, 180, 170, 230, width=3, fill="#FF5D8F"),    # Left leg
            lambda: self.hangman_canvas.create_line(200, 180, 230, 230, width=3, fill="#FF5D8F"),    # Right leg
            lambda: self.hangman_canvas.create_line(190, 90, 195, 95, width=2, fill="#FF5D8F"),      # Left eye
            lambda: self.hangman_canvas.create_line(205, 90, 210, 95, width=2, fill="#FF5D8F")       # Right eye
        ]
        
        for i in range(min(self.mistakeMade, len(parts))):
            parts[i]()
    
    def show_game_message(self, won):
        """Show smaller centered win/lose message"""
        message = f"You {'won' if won else 'lost'}! The word was: {self.secretWord}"
        self.status_label.config(text=message)
        title = "Congratulations!" if won else "Game Over"
        emoji = "🎉" if won else "😢"
        color = "#4CAF50" if won else "#FF5D8F"
        
        popup = Toplevel(self.master)
        popup.title(title)
        popup.geometry("350x200")  # Smaller size
        popup.resizable(False, False)
        popup.configure(bg="#FFEEF2")
        
        # Center the popup
        self.center_window(popup, 350, 200)
        
        Label(popup, text=emoji, font=("Arial", 36), bg="#FFEEF2", fg=color).pack(pady=5)
        Label(popup, text=message, font=self.message_font, bg="#FFEEF2", fg=color, wraplength=300).pack()
        Button(popup, text="OK", font=self.button_font, bg=color, fg="white", 
              command=popup.destroy).pack(pady=10)
        
        popup.grab_set()
    
    def updateDisplay(self):
        """Update all game elements"""
        guessed_word = self.getGuessedWord()
        self.word_label.config(text=guessed_word)
        self.mistake_label.config(text=f"Mistakes: {self.mistakeMade}/{self.maxGuesses}")
        
        # Update letter buttons
        available = self.getAvailableLetters()
        for i, btn in enumerate(self.letter_buttons):
            letter = chr(97 + i)
            if letter in available:
                btn.config(state=NORMAL, bg="#FFB7C5", fg="white")
            else:
                btn.config(state=DISABLED, bg="#E0E0E0", fg="#888888")
        
        self.drawHangman()
        
        # Check game status
        if self.isWordGuessed():
            self.show_game_message(True)
            self.disable_input()
        elif self.mistakeMade >= self.maxGuesses:
            self.show_game_message(False)
            self.disable_input()
    
    def disable_input(self):
        """Disable all inputs"""
        self.guess_entry.config(state=DISABLED)
        self.submit_button.config(state=DISABLED)
        for btn in self.letter_buttons:
            btn.config(state=DISABLED)
    
    def enable_input(self):
        """Enable all inputs"""
        self.guess_entry.config(state=NORMAL)
        self.submit_button.config(state=NORMAL)
        available = self.getAvailableLetters()
        for i, btn in enumerate(self.letter_buttons):
            btn.config(state=NORMAL if chr(97+i) in available else DISABLED)
    
    def processGuess(self, event=None):
        """Process guess from entry field"""
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, END)
        
        if len(guess) != 1 or not guess.isalpha():
            self.status_label.config(text="Please enter a single letter!")
            return
        
        self.processLetterGuess(guess)
    
    def processLetterGuess(self, letter):
        """Process letter guess"""
        if letter in self.lettersGuessed:
            self.status_label.config(text=f"You already guessed: {letter}")
            return
        
        self.lettersGuessed.append(letter)
        
        if letter in self.secretWord:
            self.status_label.config(text=f"Good guess! '{letter}' is in the word!")
        else:
            self.mistakeMade += 1
            self.status_label.config(text=f"Oops! '{letter}' is not in the word.")
        
        self.updateDisplay()
    
    def newGame(self):
        """Start new game"""
        self.secretWord = self.chooseWord(self.wordlist).lower()
        self.lettersGuessed = []
        self.mistakeMade = 0
        self.status_label.config(text="")
        self.enable_input()
        self.updateDisplay()

if __name__ == "__main__":
    root = Tk()
    game = Hangman(root)
    root.mainloop()