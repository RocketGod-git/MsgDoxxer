# __________                  __             __     ________             .___ 
# \______   \  ____    ____  |  | __  ____ _/  |_  /  _____/   ____    __| _/ 
#  |       _/ /  _ \ _/ ___\ |  |/ /_/ __ \\   __\/   \  ___  /  _ \  / __ |  
#  |    |   \(  <_> )\  \___ |    < \  ___/ |  |  \    \_\  \(  <_> )/ /_/ |  
#  |____|_  / \____/  \___  >|__|_ \ \___  >|__|   \______  / \____/ \____ |  
#         \/              \/      \/     \/               \/              \/  
#
# MsgDoxxer for .msg and .pdf data extraction by RocketGod

import sys
import os
import urllib.parse
from tkinter import Tk, filedialog
import extract_msg
import fitz  # PyMuPDF
from colorama import init, Fore, Back

# Initialize colorama
init(autoreset=True)

# Ensure tkinter is installed
try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    if sys.platform == "linux" or sys.platform == "linux2":
        print("Please install tkinter via your package manager, e.g., 'sudo apt-get install python3-tk'")
    elif sys.platform == "darwin":
        print("Please install tkinter using Homebrew or another package manager.")
    elif sys.platform == "win32":
        print("Please ensure you have tkinter installed. It should come with Python, but you may need to repair your Python installation.")
    sys.exit(1)

# Function to extract .msg file contents
def extract_msg_file(file_path):
    msg = extract_msg.Message(file_path)
    msg_sender = msg.sender
    msg_to = msg.to
    msg_cc = msg.cc
    msg_bcc = msg.bcc
    msg_subject = msg.subject
    msg_date = msg.date
    msg_body = msg.body
    msg_attachments = msg.attachments

    attachments = [{"filename": attachment.getFilename(), "data": attachment.data} for attachment in msg_attachments]

    msg_data = {
        "Type": "MSG",
        "Sender": msg_sender,
        "To": msg_to,
        "CC": msg_cc,
        "BCC": msg_bcc,
        "Subject": msg_subject,
        "Date": msg_date,
        "Body": msg_body,
        "Attachments": attachments
    }

    return msg_data

# Function to extract .pdf file contents
def extract_pdf_file(file_path):
    doc = fitz.open(file_path)
    metadata = doc.metadata
    text = ""
    links = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
        links.extend(page.get_links())

    pdf_data = {
        "Type": "PDF",
        "Metadata": metadata,
        "Text": text,
        "Links": links
    }
    return pdf_data

# Function to resolve kind to its description
def resolve_kind(kind):
    kinds = {
        1: "GoTo",
        2: "URI",
        3: "GoToR",
        4: "Launch",
        5: "Named",
        6: "Movie"
    }
    return kinds.get(kind, "Unknown")

# Function to display the extracted file data
def display_file_data(file_data):
    print("\n" * 2)  # Pad the top for better readability
    if file_data["Type"] == "MSG":
        print(f"{Back.BLACK}{Fore.GREEN}Sender: {Fore.CYAN}{file_data['Sender']}")
        print(f"{Back.BLACK}{Fore.GREEN}To: {Fore.CYAN}{file_data['To']}")
        print(f"{Back.BLACK}{Fore.GREEN}CC: {Fore.CYAN}{file_data['CC']}")
        print(f"{Back.BLACK}{Fore.GREEN}BCC: {Fore.CYAN}{file_data['BCC']}")
        print(f"{Back.BLACK}{Fore.GREEN}Subject: {Fore.CYAN}{file_data['Subject']}")
        print(f"{Back.BLACK}{Fore.GREEN}Date: {Fore.CYAN}{file_data['Date']}")
        print(f"\n{Back.BLACK}{Fore.GREEN}Body:{Fore.RESET}\n{Back.BLACK}{Fore.WHITE}{file_data['Body']}")
        if file_data['Attachments']:
            print(f"\n{Back.BLACK}{Fore.GREEN}Attachments:{Fore.RESET}")
            for attachment in file_data['Attachments']:
                print(f"{Back.BLACK}{Fore.WHITE}  Filename: {Fore.CYAN}{attachment['filename']}")
    elif file_data["Type"] == "PDF":
        metadata = file_data["Metadata"]
        print(f"{Back.BLACK}{Fore.GREEN}Title: {Fore.CYAN}{metadata.get('title', 'N/A')}")
        print(f"{Back.BLACK}{Fore.GREEN}Author: {Fore.CYAN}{metadata.get('author', 'N/A')}")
        print(f"{Back.BLACK}{Fore.GREEN}Subject: {Fore.CYAN}{metadata.get('subject', 'N/A')}")
        print(f"{Back.BLACK}{Fore.GREEN}Keywords: {Fore.CYAN}{metadata.get('keywords', 'N/A')}")
        print(f"{Back.BLACK}{Fore.GREEN}Producer: {Fore.CYAN}{metadata.get('producer', 'N/A')}")
        print(f"{Back.BLACK}{Fore.GREEN}Creation Date: {Fore.CYAN}{metadata.get('creationDate', 'N/A')}")
        print(f"{Back.BLACK}{Fore.GREEN}Modification Date: {Fore.CYAN}{metadata.get('modDate', 'N/A')}")
        print(f"\n{Back.BLACK}{Fore.GREEN}Text:{Fore.RESET}\n{Back.BLACK}{Fore.WHITE}{file_data['Text']}")
        if file_data['Links']:
            print(f"\n{Back.BLACK}{Fore.RED}WARNING: Be cautious of clicking any links unless you are certain of their destination.{Fore.RESET}")
            print(f"\n{Back.BLACK}{Fore.GREEN}Links:{Fore.RESET}")
            for link in file_data['Links']:
                uri = link.get("uri", "N/A")
                resolved_uri = urllib.parse.unquote(uri)
                kind = link.get("kind", "N/A")
                xref = link.get("xref", "N/A")
                rect = link.get("from", "N/A")
                print(f"{Back.BLACK}{Fore.WHITE}  URI: {Fore.CYAN}{uri}")
                print(f"{Back.BLACK}{Fore.WHITE}  Resolved URI: {Fore.CYAN}{resolved_uri}")
                print(f"{Back.BLACK}{Fore.WHITE}  Kind: {Fore.CYAN}{kind} ({resolve_kind(kind)})")
                print(f"{Back.BLACK}{Fore.WHITE}  XRef: {Fore.CYAN}{xref}")
                print(f"{Back.BLACK}{Fore.WHITE}  Coordinates: {Fore.CYAN}{rect}")
                print()  # Add a blank line between links for readability
    print("\n" * 2)  # Pad the bottom for better readability

# Main function to open file dialog and process the selected file
def main():
    # Open file dialog to select a .msg or .pdf file
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.call('wm', 'attributes', '.', '-topmost', True)  # Bring file dialog to the front
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select .msg or .pdf file",
                                           filetypes=(("msg and pdf files", "*.msg *.pdf"), ("all files", "*.*")))
    root.destroy()  # Destroy the root window after file selection

    if file_path:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".msg":
            file_data = extract_msg_file(file_path)
        elif file_extension == ".pdf":
            file_data = extract_pdf_file(file_path)
        else:
            print("Unsupported file type.")
            return
        display_file_data(file_data)
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
