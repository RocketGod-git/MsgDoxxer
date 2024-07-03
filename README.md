# MsgDoxxer

MsgDoxxer is a Python tool designed to extract and display information from `.msg` and `.pdf` files. It helps in identifying potentially malicious content by providing detailed metadata, text, and link information.

## Features

- Extracts and displays metadata and content from `.msg` and `.pdf` files.
- Decodes and displays URIs in a human-readable format.
- Provides a warning for potentially dangerous links.
- Supports both Windows and Linux platforms.

## Installation

To install MsgDoxxer, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/RocketGod-git/MsgDoxxer
    cd msgdoxxer
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required libraries:**

    ```sh
    pip install extract-msg colorama PyMuPDF
    ```

## Usage

To run MsgDoxxer, execute the following command:

```sh
python msg_doxxer.py
```

### How It Works

1. **File Selection:**
    - A file dialog will open, allowing you to select a `.msg` or `.pdf` file.

2. **Data Extraction:**
    - For `.msg` files, the script extracts sender, recipients, subject, date, body, and attachments.
    - For `.pdf` files, the script extracts metadata, text, and links.

3. **Data Display:**
    - The extracted information is displayed in the terminal with color-coded formatting for better readability.
    - URIs are decoded and displayed in a human-readable format.
    - Warnings are provided for potentially dangerous links.

## Example Output

```
Title: Scam
Author: Scammer
Subject: You get the drift...
Keywords:
Producer:
Creation Date:
Modification Date:

Text:
Please review and sign your document
Recipient:
RocketGod (RocketGod@email.com)
View Documents
Alternately, you can access these documents by clicking the "View Document" link above.
DocuSign. The fastest way to get a signature.
This message was sent to you by Andrea ScammerVich who is using the DocuSign Electronic Signature Service.

WARNING: Be cautious of clicking any links unless you are certain of their destination.

Links:
  URI: https://f%2eg%2eb%69ng%2ecom
  Resolved URI: https://f.g.bing.com
  Kind: 2 (URI)
  XRef: 15
  Coordinates: Rect(192.28799438476562, 281.54901123046875, 288.31201171875, 295.3480224609375)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## License

This project is licensed under the GPL-3.0 license. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [extract-msg](https://pypi.org/project/extract-msg/)
- [colorama](https://pypi.org/project/colorama/)
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)

---

**Note:** This tool is intended for educational and informational purposes only. Always exercise caution when dealing with potentially malicious files and links.
