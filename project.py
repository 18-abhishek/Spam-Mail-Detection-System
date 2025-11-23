import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import io
import requests
import os

class SpamDetector:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.data = None

    def load_data(self, url="https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"):
        """Loads the SMS Spam Collection dataset."""
        print(f"Downloading dataset from {url}...")
        try:
            # Disable SSL verification to avoid certificate errors
            response = requests.get(url, verify=False)
            response.raise_for_status()
            
            import zipfile
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                with z.open('SMSSpamCollection') as f:
                    self.data = pd.read_csv(f, sep='\t', names=['label', 'message'])
            
            print(f"Data loaded successfully. Shape: {self.data.shape}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def train(self):
        """Trains the Naive Bayes model."""
        if self.data is None:
            print("No data to train on.")
            return

        X = self.data['message']
        y = self.data['label']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a pipeline with CountVectorizer and MultinomialNB
        self.model = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())
        ])

        print("Training model...")
        self.model.fit(X_train, y_train)
        
        print("Evaluating model...")
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, predictions))

    def predict(self, message):
        """Predicts if a message is spam or ham."""
        if self.model is None:
            return "Model not trained."
        return self.model.predict([message])[0]

import imaplib
import email
from email.header import decode_header
import getpass

class EmailScanner:
    def __init__(self, imap_server="imap.gmail.com"):
        self.imap_server = imap_server
        self.mail = None

    def connect(self, username, password):
        """Connects to the IMAP server."""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(username, password)
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def fetch_emails(self, limit=10):
        """Fetches the most recent emails."""
        if not self.mail:
            return []
        
        try:
            self.mail.select("inbox")
            status, messages = self.mail.search(None, "ALL")
            email_ids = messages[0].split()
            
            # Get the last 'limit' emails
            latest_email_ids = email_ids[-limit:]
            
            emails = []
            for e_id in reversed(latest_email_ids):
                status, msg_data = self.mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                if "attachment" not in content_disposition:
                                    if content_type == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        break
                        else:
                            body = msg.get_payload(decode=True).decode()
                            
                        emails.append({"subject": subject, "body": body})
            return emails
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []

    def close(self):
        if self.mail:
            self.mail.close()
            self.mail.logout()

def main():
    detector = SpamDetector()
    
    if detector.load_data():
        detector.train()
        
        print("\n" + "="*50)
        print("SPAM DETECTION SYSTEM READY")
        print("="*50)
        
        while True:
            print("\nSelect an option:")
            print("1. Check single message")
            print("2. Scan Email Inbox")
            print("3. Exit")
            
            choice = input("Enter choice (1-3): ")
            
            if choice == '1':
                user_input = input("\nEnter a message to check: ")
                if not user_input.strip():
                    continue
                prediction = detector.predict(user_input)
                result = "SPAM 🚨" if prediction == 'spam' else "NOT SPAM (Ham) ✅"
                print(f"Result: {result}")
                
            elif choice == '2':
                print("\n--- Email Login ---")
                print("Note: For Gmail, use your App Password, not your regular password.")
                username = input("Email: ")
                password = getpass.getpass("App Password: ")
                
                scanner = EmailScanner()
                if scanner.connect(username, password):
                    print("\nScanning recent emails...")
                    emails = scanner.fetch_emails(limit=5)
                    
                    print(f"\n{'STATUS':<15} | {'SUBJECT':<50}")
                    print("-" * 70)
                    
                    for mail in emails:
                        content = f"{mail['subject']} {mail['body']}"
                        prediction = detector.predict(content)
                        status = "SPAM 🚨" if prediction == 'spam' else "HAM ✅"
                        print(f"{status:<15} | {mail['subject'][:45]}...")
                    
                    scanner.close()
                
            elif choice == '3':
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
