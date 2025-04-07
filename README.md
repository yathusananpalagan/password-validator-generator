# Password Generator & Validator 🔑🔒
**Password Generator & Validator** is a Python-based tool that allows users to generate strong passwords and validate the strength of existing ones. The password generator creates passwords based on user-defined criteria, while the validator checks the strength of passwords against security guidelines to ensure they are secure and meet best practices.

## 🚀 Key Features

- 🔑 **Password Generation**: Generates secure passwords based on user preferences (length, use of uppercase, lowercase, numbers, special characters).
- 🛡️ **Password Validation**: Validates passwords by evaluating criteria such as length, character diversity, and checks against common weak passwords.
- 📊 **Strength Scoring**: Scores passwords as **Weak**, **Medium**, or **Strong** based on the evaluation.
- 🔐 **Security Guidelines**: Provides recommendations to make passwords stronger (e.g., adding more characters or mixing in symbols).
- 🧰 **Customizable Generation**: Users can specify the length of the password, include/exclude character sets like uppercase, lowercase, numbers, and special symbols.
- 🔄 **Randomized Password Creation**: Utilizes the `secrets` module to ensure passwords are randomly generated and secure.
- 📅 **Date/Time Logging**: Captures the date and time for when passwords are validated, ensuring traceability.
- 🚫 **Common Password Detection**: Checks if the password is commonly used or weak (e.g., 'password123') and flags it as insecure.
- 💾 **Log File Support**: Generates and stores logs of validated passwords and validation results in a CSV file for record-keeping or analysis.
- 🔎 **Pattern Analysis**: Analyzes passwords to check for patterns or repeated characters that weaken the security of the password.
- 🔄 **Interactive Interface**: Command-line interface (CLI) for easy password generation and validation with real-time feedback.
- 💡 **User Recommendations**: Provides real-time feedback for improving passwords (e.g., adding more variety to character sets, increasing length).
- 🕒 **Time-Efficient Processing**: Optimized password validation and generation to ensure quick response times even for complex passwords.

## 🛠️ Tools & Technologies

[![Technologies](https://skillicons.dev/icons?i=git,github,vscode,py,md,windows)](https://skillicons.dev)

## 📂 Project Structure
Here are some important files in the project structure:

- [**passwordpassword-validator-generator.py**](./password-validator-generator.py): The main Python script that handles both password generation and validation.
- [**common_passwords.txt**](./common_passwords.txt): A text file that contains a list of common passwords, used for validating weak passwords.
- [**README.md**](./README.md): This documentation file, which explains the project and how to use it.
- [**password_history.csv**](./password_history.csv): A CSV file that logs the history of validated passwords and their validation results, including timestamps.
- [**app_icon.ico**](./app_icon.ico): The icon file for the application (if you're using a GUI).
- [**requirements.txt**](./requirements.txt): A text file containing a list of required Python libraries to run the project

## 🔧 Installation

### 📝 Things Needed:

Before you begin, make sure you have the following installed on your system:
- **Python 3.x** (You can download it from [python.org](https://www.python.org/downloads/))
- **Git** (To clone the repository)
  
### Steps to Install:

1. **Clone the Repository**  
   First, clone the repository using Git. Open your terminal or command prompt and run the following command:
   
   ```bash
   git clone https://github.com/yathusananpalagan/password-validator-generator.git
   ```
2. **Navigate to the Project Folder**
   Once the repository is cloned, navigate to the project directory:

   ```bash
   cd password-validator-generator
   ```
3. **Install Dependencies**
   The project requires some Python libraries to work. You can install all the dependencies listed in the [`requirements.txt`](./requirements.txt) file using pip:
   ```bash
   pip install -r requirements.txt
   ```
## ▶️ Usage

### 1. **Starting the Application**

To begin using the password generator and validator, simply run the main Python script. You can do this by navigating to the project directory and running the following command in your terminal or command prompt:

```bash
python password-validator-generator.py
```
This will start the application and you will be prompted to either generate a new password or validate an existing one.

### 2. **Password Generation**
- Select the option to generate a new password.
- You will be prompted to enter the desired password length (recommended: 12 or more characters).
- The script will generate a random password based on the specified length, including uppercase letters, lowercase letters, digits, and symbols.

### 3. **Password Validation**
- Select the option to validate an existing password.
- Enter the password you want to validate.
- The script will check the password strength against the following criteria:
  - Length (minimum 8 characters)
  - Presence of uppercase letters, lowercase letters, digits, and symbols
  - Whether the password is common (from common_passwords.txt)
- The result will be displayed with feedback on the strength of the password. If the password is weak, suggestions will be provided to make it stronger.
- The validated password will be displayed, and it will also be logged in the password_history.csv file along with a timestamp.

### 4. **Viewing Password History** 
The history of generated passwords, along with their validation results and timestamps, will be stored in the password_history.csv file. You can open this CSV file in any spreadsheet program to view the history.

### 5. **Setting the Application Icon (Optional)**
If you are using a GUI, you can set the app_icon.ico file as the icon for the application window. Simply load the icon in your GUI application code.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🤝 Contributions

Contributions are always welcome! If you'd like to contribute to this project, feel free to submit a pull request or open an issue. Your help is greatly appreciated! 😊

## 📬 Contact

If you have any questions, feedback, or suggestions, feel free to reach out to me:

- **GitHub**: [@YathusanAnpalagan](https://github.com/yathusananpalagan)
- **LinkedIn**: [@YathusanAnpalagan](https://www.linkedin.com/in/yathusan-anpalagan-805957353/)

I'm happy to help and would love to hear your thoughts! 😊

## 🌟 Show Your Support

If you found this project useful or interesting, please consider giving it a **star** on GitHub! ⭐
<br>
Thank you for your support! 🙏

## 📚 Libraries Used

This project utilizes the following Python libraries:
- **secrets**: Provides a secure random number generator for cryptographic purposes, used for generating secure passwords.
- **re**: Regular expressions library used for validating passwords against patterns (e.g., checking length, character variety).
- **hashlib**: A module used for cryptographic hashing, useful for validating password strength by comparing hashed versions of the password.
- **time**: For timestamping and measuring the time taken for operations like password generation and validation.
- **math**: Provides mathematical operations, including logarithmic functions for estimating password strength.
- **collections.Counter**: Useful for counting the frequency of characters in passwords to identify repeating patterns.
- **csv**: Allows saving the validated passwords and validation results to CSV files for analysis.
- **os**: Used for interacting with the operating system, including creating directories and managing file paths.
- **customtkinter**: Used to create a graphical user interface (GUI) for the password generator and validator, providing an interactive and visually appealing interface.
- **string**: Provides common string constants (e.g., string.ascii_lowercase, string.digits) to easily access character sets for password generation.
