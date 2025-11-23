# Spam Mail Detection System 📧

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

A powerful, user-friendly Spam Detection System built with Python. It utilizes Machine Learning (Naive Bayes) to accurately classify SMS and Email messages as **Spam** or **Ham** (Legitimate). The project features a modern GUI, real-time email scanning capabilities, and a robust command-line interface.

## 🌟 Key Features

-   **🤖 Advanced Machine Learning**: Powered by the Multinomial Naive Bayes algorithm, achieving ~98% accuracy on the SMS Spam Collection dataset.
-   **🎨 Modern User Interface**: A sleek, dark-mode compatible GUI built with `customtkinter` for a premium user experience.
-   **📧 Real-Time Email Scanning**: Seamlessly integrates with Gmail via IMAP to fetch and scan your latest emails for potential spam.
-   **🖥️ Dual Modes**: Choose between a feature-rich GUI or a lightweight Command Line Interface (CLI).
-   **🔒 Secure Authentication**: Uses App Passwords for secure email access, ensuring your primary credentials remain safe.

## 📂 Project Structure

```text
spam-detection-system/
├── gui.py              # Main entry point for the Graphical User Interface
├── project.py          # Core logic (Model, EmailScanner) and CLI entry point
├── README.md           # Project documentation
└── requirements.txt    # List of dependencies (if created)
```

## 🛠️ Installation & Setup

### Prerequisites
-   Python 3.8 or higher installed.
-   An active internet connection (for downloading the dataset).

### Step-by-Step Guide

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/spam-detection-system.git
    cd spam-detection-system
    ```

2.  **Install Dependencies**
    Run the following command to install the required Python libraries:
    ```bash
    pip install scikit-learn pandas requests customtkinter
    ```

## 🚀 How to Use

### Option 1: Modern GUI (Recommended)
Launch the graphical interface for an intuitive experience.
```bash
python gui.py
```
-   **Check Message**: Type or paste any text into the input box and click **"Check Message"**. The system will instantly flag it as SPAM or HAM.
-   **Scan Email Inbox**: Click **"Scan Email Inbox"**. You will be prompted for your Email and App Password. The system will fetch the last 5 emails and classify them.

### Option 2: Command Line Interface (CLI)
For quick tests or server environments.
```bash
python project.py
```
Follow the on-screen menu to select your desired action.

## ⚙️ Technical Details

### The Model
The system uses a **Pipeline** consisting of:
1.  **CountVectorizer**: Converts text messages into a matrix of token counts (Bag of Words model).
2.  **MultinomialNB**: A Naive Bayes classifier suitable for classification with discrete features (e.g., word counts).

### The Dataset
The model is trained on the **UCI SMS Spam Collection Dataset**, which contains 5,574 SMS messages tagged as spam or ham. The system automatically downloads this dataset on the first run.

## 📧 Email Scanning Configuration

To use the email scanning feature with Gmail, you **must** use an App Password.

1.  Go to your [Google Account Settings](https://myaccount.google.com/).
2.  Navigate to **Security** > **2-Step Verification** (Enable it if it's off).
3.  Search for **"App Passwords"**.
4.  Create a new App Password (name it "Spam Detector").
5.  Copy the 16-character code and use it when prompted by the application.

---
*Built with ❤️ by Abhishek*
