# CSV to Make.com Webhook Script

## Purpose

This project contains a Python script (`send_to_webhook.py`) designed to read data from a CSV file (`Master Shorts 32825 - segments.csv`), format it into a specific JSON structure, and send it to a Make.com webhook endpoint for further processing (e.g., video generation).

## Prerequisites

*   **Python 3:** Ensure you have Python 3 installed on your system.
*   **requests Library:** The script uses the `requests` library to send data to the webhook. If you don't have it installed, open your terminal or command prompt and run:
    ```bash
    pip install requests
    ```

## Setup

1.  **Clone the Repository (Optional):** If you haven't already, clone this repository to your local machine.
    ```bash
    git clone https://github.com/12TribesofIsrael/CSVMaster.git
    cd CSVMaster
    ```
2.  **Place Files:** Make sure the following files are in the same directory:
    *   `send_to_webhook.py` (this script)
    *   `Master Shorts 32825 - segments.csv` (the data source)

## How it Works

The `send_to_webhook.py` script performs the following steps:

1.  **Locates CSV:** It finds the `Master Shorts 32825 - segments.csv` file located in the same directory as the script.
2.  **Reads CSV:** It reads the CSV file row by row, skipping the header.
3.  **Formats Data:** For each valid row, it extracts the `SegmentNumber` and `FormattedText` columns. It converts this data into a JSON array where each element is an object like:
    ```json
    {
      "segmentNumber": 13,
      "formattedText": "Text content for the segment..."
    }
    ```
4.  **Sends to Webhook:** It sends the entire JSON array as a payload in a POST request to the configured Make.com webhook URL.
5.  **Outputs Response:** It prints the status code and response text received from the webhook to indicate success or failure.

## Configuration

The script contains the following configuration variables near the top:

*   `csv_file_path`: Automatically determined based on the script's location and the expected CSV filename (`Master Shorts 32825 - segments.csv`).
*   `webhook_url`: The target Make.com webhook URL (`https://hook.us2.make.com/4m9kr9bolyh9ddby34sjmzx25xjn6xpw`). You can change this if your webhook URL changes.

## Usage

1.  Navigate to the directory containing the script and the CSV file in your terminal.
2.  Run the script using Python:
    ```bash
    python send_to_webhook.py
    ```
3.  Observe the output in the terminal for status messages and the webhook response. Check your Make.com scenario history for processing details. 