import json
import requests
import csv
import os # Import os to construct file path relative to script

# --- Configuration ---
# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__)) 
# Construct the full path to the CSV file relative to the script's location
csv_file_path = os.path.join(script_dir, 'Master Shorts 32825 - segments.csv') 
webhook_url = 'https://hook.us2.make.com/4m9kr9bolyh9ddby34sjmzx25xjn6xpw'
# --- End Configuration ---

def read_csv_and_format_json(file_path):
    """Reads the CSV file and formats it into the desired JSON structure."""
    data = []
    try:
        print(f"Attempting to read CSV file from: {file_path}")
        # Explicitly check if file exists
        if not os.path.exists(file_path):
            print(f"Error: CSV file not found at the specified path: {file_path}")
            # Check current working directory and script directory for context
            print(f"Current Working Directory: {os.getcwd()}")
            print(f"Script Directory: {os.path.dirname(os.path.abspath(__file__))}")
            # List files in script directory for debugging
            try:
                print(f"Files in script directory: {os.listdir(os.path.dirname(os.path.abspath(__file__)))}")
            except Exception as list_e:
                print(f"Could not list files in script directory: {list_e}")
            return None

        with open(file_path, mode='r', encoding='utf-8') as infile:
            # Use csv.reader to handle potential commas within quoted fields
            reader = csv.reader(infile)
            
            try:
                header = next(reader) # Read header row
                print(f"CSV Header found: {header}")
            except StopIteration:
                print("Error: CSV file is empty.")
                return None
                
            # Find column indices (more robust than assuming order)
            try:
                 segment_col = header.index('SegmentNumber')
                 text_col = header.index('FormattedText')
                 print(f"Found 'SegmentNumber' at index {segment_col}, 'FormattedText' at index {text_col}")
            except ValueError:
                 print("Error: CSV header missing 'SegmentNumber' or 'FormattedText'.")
                 print(f"Please ensure the first row contains exactly these column names.")
                 return None

            line_num = 1 # Start counting after header
            for row in reader:
                 line_num += 1
                 # Basic check for empty rows or incorrect number of columns
                 if not row:
                     print(f"Skipping empty row at line {line_num}")
                     continue
                 if len(row) <= max(segment_col, text_col):
                     print(f"Skipping row {line_num} due to insufficient columns ({len(row)} found). Content: {row}")
                     continue

                 try:
                    segment_str = row[segment_col].strip()
                    text_str = row[text_col].strip()

                    # Check if segment number is empty before converting
                    if not segment_str:
                         print(f"Skipping row {line_num} due to empty SegmentNumber. Content: {row}")
                         continue

                    segment_number = int(segment_str)                    
                    data.append({
                        "segmentNumber": segment_number,
                        "formattedText": text_str
                    })
                 except ValueError:
                    print(f"Skipping row {line_num} due to conversion error (SegmentNumber '{segment_str}' not an integer?). Content: {row}")
                 except IndexError:
                    print(f"Skipping row {line_num} due to index error (likely missing columns). Content: {row}")

    except FileNotFoundError:
        # This specific error should be caught by the os.path.exists check earlier,
        # but keeping it here as a fallback.
        print(f"Error: CSV file not found at {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred reading the CSV on line {line_num}: {e}")
        return None
        
    if not data:
        print("Warning: No valid data rows were processed from the CSV.")
        
    return data

# --- Main script execution ---
payload_data = read_csv_and_format_json(csv_file_path)

if payload_data:
    print(f"Successfully prepared data with {len(payload_data)} segments.")
    # print("First few segments:", json.dumps(payload_data[:3], indent=2)) # Optional: Uncomment to preview data

    # Define headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    try:
        print(f"Sending data to webhook: {webhook_url}")
        response = requests.post(webhook_url, headers=headers, json=payload_data)

        # Check the response
        print(f"Response Status Code: {response.status_code}")
        try:
            # Try to print the response body (Make.com webhooks usually respond with 'Accepted')
            print(f"Response Body: {response.text}")
        except Exception as e:
            print(f"Could not read response body: {e}")

        if response.status_code == 200 and response.text.strip().lower() == 'accepted':
            print("--- Success: Webhook received the data. ---")
        else:
            print("--- Warning: Webhook might have encountered an issue or returned an unexpected response. ---")
            print("--- Please check Make.com scenario history for details. ---")


    except requests.exceptions.RequestException as e:
        print(f"Error sending request to webhook: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during the request: {e}")
else:
    print("--- Error: Could not prepare data from CSV. Aborting webhook send. ---")
    print("--- Please check the CSV file path, format, and content based on earlier messages. ---")

print("Script finished.") 