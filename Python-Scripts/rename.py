import re
import sys
import os
import glob

def format_filename(filename):
    # Remove NVR-1-Front
    filename_no_prefix = re.sub(r"^(NVR-1-Front-|NVR-0-Garage-)", "", filename)

    # Extract front date and time
    first_timestamp = re.search(r"(\d{14})", filename_no_prefix).group(1)

    # Format Date and Time to match YYYY-MM-DD_HH_MM_SS
    formatted_first_timestamp = re.sub(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})", r"\1-\2-\3_\4_\5_", first_timestamp)

    # Combine the formatted timestamps
    filename_final = f"{formatted_first_timestamp}.mp4"
    return filename_final


def process_directory(directory):
    # Use glob to get all files in the directory
    for filepath in glob.glob(os.path.join(directory, "*.mp4")):
        filename = os.path.basename(filepath)
        formatted_filename = format_filename(filename)
        
        new_filepath = os.path.join(directory, formatted_filename)
        
        # Print the original and formatted filenames
        print(f"Renaming: {filename} -> {formatted_filename}")
        
        # Rename the file
        os.rename(filepath, new_filepath)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a valid directory.")
        sys.exit(1)
    
    process_directory(directory)

if __name__ == "__main__":
    main()