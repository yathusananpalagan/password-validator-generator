import customtkinter as ctk
import string
import secrets
import re
import hashlib
import time
import math
from collections import Counter
import csv
import os

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")
def load_common_passwords():
    try:
        with open("common_passwords.txt", "r", encoding="utf-8") as file:
            return set(line.strip().lower() for line in file if line.strip())
    except FileNotFoundError:
        return set()

COMMON_PASSWORDS = load_common_passwords()
EXTENDED_SPECIALS = "!@#$%^&*()_+-=[]{};':\"\\|,.<>/?äöüéèàâîôùçê"

class PassValidatorGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Validator & Generator")
        self.geometry("1280x720")
        self.bind("<Configure>", self.on_resize)

        # Set window icon
        self.iconbitmap("app_icon.ico")

        # Custom Font
        self.font_style = ("Roboto", 14)

        # List to store history
        self.history_data = []

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand = True, padx = 20, pady = 20)

        self.validator_tab = self.tabview.add("Validator")
        self.generator_tab = self.tabview.add("Generator")
        self.history_tab = self.tabview.add("History")

        self.build_validator_tab()
        self.build_generator_tab()
        self.build_history_tab()

    def build_validator_tab(self):
        # Section Title
        title = ctk.CTkLabel(self.validator_tab, text="🔍 Password Strength Checker", font=("Roboto", 20, "bold"))
        title.pack(pady=(20, 10))

        # Entry Frame
        input_frame = ctk.CTkFrame(self.validator_tab, fg_color="transparent")
        input_frame.pack(pady=10)

        self.validate_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g. S3cur3P@sswörd!", width=400, font=self.font_style)
        self.validate_entry.pack(pady=10)

        # Bind the event to trigger validation on typing
        self.validate_entry.bind("<KeyRelease>", self.validate_password)

        # Validation result frame
        self.result_frame = ctk.CTkFrame(self.validator_tab, fg_color="transparent")
        self.result_frame.pack(pady=(20, 10), fill="both", expand=True)

        # Strength bar
        self.strength_bar = ctk.CTkProgressBar(self.validator_tab, height=20)
        self.strength_bar.pack(pady=(10, 0), padx=100, fill="x")
        self.strength_bar.set(0)
    
    def validate_password(self, event = None):
        if hasattr(self, "_validate_after_id"):
            self.after_cancel(self._validate_after_id)

        self._validate_after_id = self.after(200, self._perform_validation)

    def _perform_validation(self):
        # Clear previous result labels
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        password = self.validate_entry.get()
        feedback, score = self.get_password_feedback(password)

        score = max(score,0)

        for line in feedback:
            if "✅" in line:
                color = "green"
            elif "🟡" in line:
                color = "yellow"
            else:
                color = "red"

            label = ctk.CTkLabel(self.result_frame, text=line, text_color=color, font=self.font_style, anchor="w")
            label.pack(anchor="w", padx=10)

        # Calculate the percentage and round it
        percentage = round(score * 100 / 13)  # Divide by 13 because the max score is 13

        # Set progress bar value (score out of 5)
        self.strength_bar.set(percentage / 100.0)

        # Show percentage score next to the progress bar
        percentage_score = f"Strength: {percentage}%"
        if not hasattr(self, 'strength_percentage_label'):  # Check if the label already exists
            self.strength_percentage_label = ctk.CTkLabel(self.validator_tab, text=percentage_score, font=self.font_style)
            self.strength_percentage_label.pack(pady=(10, 0), padx=100, fill="x")
        else:
            # Update the existing label's text
            self.strength_percentage_label.configure(text=percentage_score)

        # Update progress bar color based on score
        if percentage <= 40:
            self.strength_bar.configure(progress_color="red")
            # Update percentage label color
            self.strength_percentage_label.configure(text_color="red")
        elif percentage <= 70:
            self.strength_bar.configure(progress_color="yellow")
            # Update percentage label color
            self.strength_percentage_label.configure(text_color="yellow")
        else:
            self.strength_bar.configure(progress_color="green")
            # Update percentage label color
            self.strength_percentage_label.configure(text_color="green")

        # Store the password and its validation results in the history
        self.history_data.append({
            "password": password,
            "score": percentage,
            "hashed_password": hashlib.sha256(password.encode()).hexdigest(),
            "strength": "Strong" if percentage > 70 else "Medium" if percentage > 40 else "Weak",
            "date": time.strftime("%Y-%m-%d %H:%M:%S")
        })

        self.log_password_to_file(
            password=password,
            score=percentage,
            strength="Strong" if percentage > 70 else "Medium" if percentage > 40 else "Weak",
            hashed_pw=hashlib.sha256(password.encode()).hexdigest()
        )

        # Update the history display
        self.update_history_tab()
    
    def get_password_feedback(self, password):
        feedback = []
        score = 0

        checks = [
            self.check_length,
            self.check_uppercase,
            self.check_lowercase,
            self.check_digits,
            self.check_symbols,
            self.check_repeats,
            self.check_sequences,
            self.check_common_passwords,
            self.check_entropy,
        ]

        for check in checks:
            result, pts = check(password)
            feedback.append(result)
            score += pts

        # Final summary
        if score >= 13:
            feedback.insert(0, "✅ Strong Password")
        elif score >= 7:
            feedback.insert(0, "🟡 Medium Password")
        else:
            feedback.insert(0, "❌ Weak Password")

        return feedback, score
    
    def build_generator_tab(self):

        self.length_label = ctk.CTkLabel(self.generator_tab, text="Password Length",font=self.font_style)
        self.length_label.pack(pady = (20,5))

        self.length_slider = ctk.CTkSlider(self.generator_tab, from_=8, to=32, number_of_steps=24,command=self.update_length_label)
        self.length_slider.set(12)
        self.length_slider.pack(pady = 5)

        self.length_display = ctk.CTkLabel(self.generator_tab, text=f"Length: {int(self.length_slider.get())}")
        self.length_display.pack(pady=(0, 10))

        # Options
        self.uppercase_var = ctk.BooleanVar(value=True)
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.digits_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)
        self.special_chars_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(self.generator_tab, text="Include Uppercase", variable=self.uppercase_var).pack(anchor="w", padx=20)
        ctk.CTkCheckBox(self.generator_tab, text="Include Lowercase", variable=self.lowercase_var).pack(anchor="w", padx=20)
        ctk.CTkCheckBox(self.generator_tab, text="Include Digits", variable=self.digits_var).pack(anchor="w", padx=20)
        ctk.CTkCheckBox(self.generator_tab, text="Include Symbols", variable=self.symbols_var).pack(anchor="w", padx=20)
        ctk.CTkCheckBox(self.generator_tab, text="Include Special Characters", variable=self.special_chars_var).pack(anchor="w", padx=20)

        # Output
        self.generated_password = ctk.CTkEntry(self.generator_tab, width = 400)
        self.generated_password.pack(pady = 10)
        self.generated_password.configure(state = "readonly")

        button_frame = ctk.CTkFrame(self.generator_tab, fg_color="transparent")
        button_frame.pack(pady = 10)

        # Generate Button
        self.generate_button = ctk.CTkButton(button_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(side = "left", padx=10)

        # Copy Button
        self.copy_button = ctk.CTkButton(button_frame, text="Copy Password", command=self.copy_password)
        self.copy_button.pack(side = "left", padx=10)

        self.copy_confirmation_label = ctk.CTkLabel(self.generator_tab, text="", font=self.font_style, text_color="green")
        self.copy_confirmation_label.pack(pady=(10, 0))

    def copy_password(self):
        self.clipboard_clear()
        self.clipboard_append(self.generated_password.get())
        self.update()  # Keeps clipboard content even after the app is closed

        # Show the "Copied to Clipboard" label
        self.copy_confirmation_label.configure(text="Copied to Clipboard!", text_color="green")

        # Hide the message after 2 seconds
        self.after(2000, self.hide_copy_confirmation)
    
    def hide_copy_confirmation(self):
        # Reset the label text after 2 seconds
        self.copy_confirmation_label.configure(text="")
    
    def update_length_label(self, value):
        self.length_display.configure(text=f"Length: {int(float(value))}")

    def generate_password(self):
        length = int(self.length_slider.get())
        char_pool = ''
        password = []

        if self.uppercase_var.get():
            char_pool += string.ascii_uppercase
        if self.lowercase_var.get():
            char_pool += string.ascii_lowercase
        if self.digits_var.get():
            char_pool += string.digits
        if self.symbols_var.get():
            char_pool += string.punctuation
        if self.special_chars_var.get():
            char_pool += "äöüéèàâîôùçêîî"
        
        if not char_pool:
            self.generated_password.configure(state="normal")
            self.generated_password.delete(0, ctk.END)
            self.generated_password.insert(0, "Select at least one option")
            self.generated_password.configure(state="readonly")
            return

        # Use secrets for secure random choice
        if self.uppercase_var.get():
            password.append(secrets.choice(string.ascii_uppercase))
        if self.lowercase_var.get():
            password.append(secrets.choice(string.ascii_lowercase))
        if self.digits_var.get():
            password.append(secrets.choice(string.digits))
        if self.symbols_var.get():
            password.append(secrets.choice(string.punctuation))
        if self.special_chars_var.get():
            password.append(secrets.choice("äöüéèàâîôùçêîî"))

        # Fill the rest randomly
        while len(password) < length:
            password.append(secrets.choice(char_pool))

        secrets.SystemRandom().shuffle(password)
        password = ''.join(password)    

        # Update the field safely
        self.generated_password.configure(state="normal")
        self.generated_password.delete(0, ctk.END)
        self.generated_password.insert(0, password)
        self.generated_password.configure(state="readonly")

    def build_history_tab(self):
        # Title
        title = ctk.CTkLabel(self.history_tab, text="📜 Password Strength History", font=("Roboto", 20, "bold"))
        title.pack(pady=(20, 10))

        # Outer container to center contents
        self.history_container = ctk.CTkFrame(self.history_tab, fg_color="transparent")
        self.history_container.pack(expand=True, fill="both", padx=20)

        # Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.history_container, width=1000, height=500)
        self.scrollable_frame.pack(pady=10, anchor="center")

        # Table Headers
        headers = ["Date", "Password", "Strength", "Score", "Hashed Password"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Roboto", 14, "bold"))
            label.grid(row=0, column=col, padx=10, pady=10)

    def update_history_tab(self):
        # Clear existing entries from scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        # Show most recent first
        history_reversed = list(reversed(self.history_data))

        for row, data in enumerate(history_reversed[:100], start=1):
            ctk.CTkLabel(self.scrollable_frame, text=data["date"], font=("Roboto", 12)).grid(row=row, column=0, padx=10, pady=5)
            ctk.CTkLabel(self.scrollable_frame, text="********", font=("Roboto", 12)).grid(row=row, column=1, padx=10, pady=5)
            ctk.CTkLabel(self.scrollable_frame, text=data["strength"], font=("Roboto", 12), text_color="green" if data["strength"] == "Strong" else "yellow" if data["strength"] == "Medium" else "red").grid(row=row, column=2, padx=10, pady=5)
            ctk.CTkLabel(self.scrollable_frame, text=f"{data['score']}%", font=("Roboto", 12)).grid(row=row, column=3, padx=10, pady=5)
            ctk.CTkLabel(self.scrollable_frame, text=data["hashed_password"], font=("Roboto", 12)).grid(row=row, column=4, padx=10, pady=5)

    # Individual check methods below

    def calculate_entropy(self, password):
        # Identify the frequency of each character in the password
        char_count = Counter(password)
        
        # Pool size is the number of unique characters
        pool_size = len(char_count)
        
        # If only one character repeats (like 'aaaa...')
        if pool_size == 1:
            return 0  # Very low entropy (not complex)

        # If the password is very long, but made up of just a few characters (like 'aaaaaaabbb')
        # We reduce entropy for such cases as well.
        total_chars = len(password)
        char_frequencies = [freq / total_chars for freq in char_count.values()]
        
        # Entropy calculation:
        # Entropy = sum( - p(x) * log2(p(x)) ) for each unique character.
        # Where p(x) is the frequency of the character in the password.
        entropy = -sum(f * math.log2(f) for f in char_frequencies)
        
        # Apply penalty for high frequency of repetition (repetition reduces complexity)
        # If the password is made of a lot of the same characters, reduce entropy.
        repetition_factor = sum([freq / total_chars for freq in char_count.values() if freq > 1])
        entropy -= repetition_factor * 0.5  # Apply penalty for repetition
        
        # If entropy is negative, set it to 0 (minimum entropy value)
        entropy = max(0, entropy)
        
        return entropy * 20
    def has_repeated_characters(self, password):
        # Check for repeated sequences (e.g., "aaaa", "1111")
        return any(password[i:i+4] == password[i] * 4 for i in range(len(password) - 3))
    
    def has_sequential_characters(self, password):
        # Check for sequential patterns (e.g., "abcd", "1234")
        # We will consider alphanumeric and special character sequences.
        for i in range(len(password) - 3):  # Check for sequences of 4 or more characters
            if self.is_sequential(password[i:i+4]):
                return True
        return False
    def is_sequential(self, sequence):
        # Check if a sequence of characters is sequential (like '1234' or 'abcd')
        return all(ord(sequence[i]) + 1 == ord(sequence[i + 1]) for i in range(len(sequence) - 1))

    def check_length(self, password):
        length = len(password)
        if length >= 15:
            return "✅ Length 15+ characters", 3
        elif length >= 11:
            return "🟡 Length 11-14 characters", 2
        elif length >= 8:
            return "🟡 Length 8-10 characters", 1
        return "❌ Length must be at least 8 characters", 0

    def check_uppercase(self, password):
        uppercase_count = len(re.findall(r"[A-Z]", password))
        if uppercase_count >= 3:
            return "✅ Contains 3+ uppercase letters", 2
        elif uppercase_count >= 1:
            return "🟡 Contains 1+ uppercase letter", 1
        return "❌ Missing uppercase letter", 0

    def check_lowercase(self, password):
        lowercase_count = len(re.findall(r"[a-z]", password))
        if lowercase_count >= 3:
            return "✅ Contains 3+ lowercase letters", 2
        elif lowercase_count >= 1:
            return "🟡 Contains 1+ lowercase letter", 1
        return "❌ Missing lowercase letter", 0

    def check_digits(self, password):
        digit_count = len(re.findall(r"\d", password))
        if digit_count >= 3:
            return "✅ Contains 3+ digits", 2
        elif digit_count >= 1:
            return "🟡 Contains 1+ digit", 1
        return "❌ Missing digit", 0

    def check_symbols(self, password):
        symbol_count = sum(1 for char in password if char in EXTENDED_SPECIALS)
        if symbol_count >= 3:
            return "✅ Contains 3+ special characters", 2
        elif symbol_count >= 1:
            return "🟡 Contains 1+ special character", 1
        return "❌ Missing special character", 0

    def check_repeats(self, password):
        if self.has_repeated_characters(password):
            return "❌ Contains repeated characters (e.g., 'aaaa')", -2
        return "✅ No repeated characters", 0

    def check_sequences(self, password):
        if self.has_sequential_characters(password):
            return "❌ Contains sequential characters (e.g., '1234', 'abcd')", -2
        return "✅ No sequential characters", 0

    def check_entropy(self, password):
        entropy = self.calculate_entropy(password)
        if entropy >= 80:
            return "✅ High entropy (complex password)", 2
        elif entropy >= 50:
            return "🟡 Medium entropy", 0
        else:
            return "❌ Low entropy (password could be easily guessed)", -2

    def check_common_passwords(self, password):
        if password.lower() in COMMON_PASSWORDS:
            return "❌ Common password found in leaked lists", -3
        return "✅ Not a common password", 0

    def on_resize(self, event):
        # Adjust width of scrollable_frame based on window width
        new_width = min(self.winfo_width() - 100, 1100)
        self.scrollable_frame.configure(width=new_width)
    
    def log_password_to_file(self, password, score, strength, hashed_pw):
        log_file = "password_history.csv"
        is_new_file = not os.path.exists(log_file)

        # Mask password with same number of bullets
        masked_pw = "•" * len(password)

        with open(log_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if is_new_file:
                writer.writerow(["Timestamp", "Password", "Score", "Strength", "Hashed"])
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), masked_pw, score, strength, hashed_pw])

if __name__ == "__main__":
    app = PassValidatorGeneratorApp()
    app.mainloop()