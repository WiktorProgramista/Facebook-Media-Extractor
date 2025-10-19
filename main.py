import os
import json
import re
from datetime import datetime
import filedate
import shutil
import uuid
import string
import time

# Define the regex pattern to match the JSON file names
pattern = re.compile(r'message_.*\.json')

# Directories
output_dir = 'output'
output_dir_photos = os.path.join(output_dir, "photos")
output_dir_videos = os.path.join(output_dir, "videos")
output_dir_gifs = os.path.join(output_dir, "gifs")
done_dir = 'done'
error_dir = 'error'

# Find all Facebook activity directories
def find_facebook_directories(root_dir='.'):
    facebook_dirs = []
    for item in os.listdir(root_dir):
        if item.startswith('facebook-') and os.path.isdir(item):
            facebook_dirs.append(item)
    return facebook_dirs

# Find all JSON files in the Facebook directory structure OR in current chat directory
def find_json_files(facebook_dirs):
    json_files = []
    
    # If we have Facebook directories, use the standard structure
    if facebook_dirs:
        for facebook_dir in facebook_dirs:
            # Build the path to messages directory
            messages_path = os.path.join(facebook_dir, "your_facebook_activity", "messages")
            
            if os.path.exists(messages_path):
                print(f"Found messages directory: {messages_path}")
                # Search in all subdirectories of messages (inbox, archived_threads, e2ee_cutover, etc.)
                for subdir, dirs, files in os.walk(messages_path):
                    for filename in files:
                        if pattern.match(filename):
                            json_files.append(os.path.join(subdir, filename))
            else:
                print(f"Messages directory not found: {messages_path}")
    else:
        # If no Facebook directories found, search in current directory for JSON files
        print("No Facebook directories found, searching in current directory...")
        for filename in os.listdir('.'):
            if pattern.match(filename) and os.path.isfile(filename):
                json_files.append(os.path.join('.', filename))
        
        # Also search in subdirectories of current directory
        for subdir, dirs, files in os.walk('.'):
            for filename in files:
                if pattern.match(filename):
                    full_path = os.path.join(subdir, filename)
                    if full_path not in json_files:
                        json_files.append(full_path)
    
    return json_files

# Move and rename files to the output folder
def move_to_output(old_path, media_type, title, creation_timestamp):
    # Create the filename pattern and remove char that can't be in folder name
    creation_date = datetime.fromtimestamp(creation_timestamp)
    creation_date_str = creation_date.strftime('%Y%m%d%H%M%S')
    file_extension = os.path.splitext(old_path)[1]
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = title.strip()
    # Some conversation can have a complete not printable title
    if len(title) == 0:
        title = "unknown"
    new_file_name = title + "_" + creation_date_str + "_" + str(uuid.uuid4()) + file_extension
    
    # Select the correct output directory based on media type
    if media_type == "photos":
        output_path = output_dir_photos
    elif media_type == "videos":
        output_path = output_dir_videos
    elif media_type == "gifs":
        output_path = output_dir_gifs
    else:
        output_path = output_dir
    
    # Move the new file
    new_path = os.path.join(output_path, new_file_name)
    shutil.copy(old_path, new_path)
    return new_path

# Change "created, modified and accessed" date of the provided file
def change_metadata_date(new_path, creation_timestamp):
    try:
        # Convert the Unix timestamp to a datetime object
        creation_date = datetime.fromtimestamp(creation_timestamp)
        
        # Change metadata using filedate
        file_path = filedate.File(new_path)
        file_path.set(
            created = creation_date,
            modified = creation_date,
            accessed = creation_date
        )
        print(f"Changed metadata for {os.path.basename(new_path)} to {creation_date}")
    except Exception as e:
        print(f"Warning: Could not change metadata for {new_path}: {str(e)}")

# Find media file with multiple possible locations - IMPROVED VERSION
def find_media_file(media_path, json_file_path, facebook_directories):
    filename = os.path.basename(media_path)
    
    # 1. First try the original path from JSON
    if os.path.exists(media_path):
        return media_path
    
    # 2. Try relative to JSON file directory
    json_dir = os.path.dirname(json_file_path)
    alt_path = os.path.join(json_dir, filename)
    if os.path.exists(alt_path):
        return alt_path
    
    # 3. Try in subdirectories of JSON file directory
    for root, dirs, files in os.walk(json_dir):
        for file in files:
            if file == filename:
                return os.path.join(root, file)
    
    # 4. Try in current working directory and all subdirectories
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == filename:
                return os.path.join(root, file)
    
    # 5. Try to reconstruct path based on Facebook directory structure
    if facebook_directories:
        for facebook_dir in facebook_directories:
            # Build possible path based on Facebook structure
            reconstructed_path = os.path.join(facebook_dir, media_path)
            if os.path.exists(reconstructed_path):
                return reconstructed_path
            
            # Also try without the "your_facebook_activity" part
            if "your_facebook_activity/" in media_path:
                simplified_path = media_path.replace("your_facebook_activity/", "")
                reconstructed_path = os.path.join(facebook_dir, simplified_path)
                if os.path.exists(reconstructed_path):
                    return reconstructed_path
    
    # 6. Try to find by filename only in all Facebook directories
    if facebook_directories:
        for facebook_dir in facebook_directories:
            for root, dirs, files in os.walk(facebook_dir):
                for file in files:
                    if file == filename:
                        return os.path.join(root, file)
    
    # 7. Last resort: search everywhere in current directory and subdirectories
    print(f"Searching extensively for: {filename}")
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == filename:
                found_path = os.path.join(root, file)
                print(f"Found media file at: {found_path}")
                return found_path
    
    return None

# Create folders
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(output_dir_photos):
    os.makedirs(output_dir_photos)
if not os.path.exists(output_dir_videos):
    os.makedirs(output_dir_videos)
if not os.path.exists(output_dir_gifs):
    os.makedirs(output_dir_gifs)
if not os.path.exists(done_dir):
    os.makedirs(done_dir)
if not os.path.exists(error_dir):
    os.makedirs(error_dir)

# Find all Facebook directories
facebook_directories = find_facebook_directories()
print(f"Found {len(facebook_directories)} Facebook directories:")
for fb_dir in facebook_directories:
    print(f"  - {fb_dir}")

# Find all JSON files (in Facebook directories or current directory)
json_files = find_json_files(facebook_directories)
print(f"Found {len(json_files)} JSON files to process")

# Process each JSON file
for file_path in json_files:
    # Load the JSON data from the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {str(e)}")
        continue
    
    # Remove all non printable characters from the title
    title = data.get('title', 'unknown')
    printable_chars = set(string.printable)
    title = ''.join(filter(lambda x: x in printable_chars, title))
    
    # Start extracting and log data file
    print("->" + title + " extract started...")
    print("Data file : " + file_path)
    count = 0
    
    try:
        # Loop over all messages then media types (photos, videos, gifs)
        for message in data['messages']:
            # Get timestamp from message as fallback for GIFs
            message_timestamp = message.get('timestamp_ms', 0) // 1000 if 'timestamp_ms' in message else int(time.time())
            
            for media_type in ["photos", "videos", "gifs"]:
                if media_type in message:
                    for media in message[media_type]:
                        # Retrieve media uri and creation timestamp
                        path = media['uri']
                        # For gifs this value can be empty, use message timestamp as fallback
                        if 'creation_timestamp' in media:
                            creation_timestamp = media['creation_timestamp']
                        else:
                            creation_timestamp = message_timestamp
                        
                        # Find the media file in multiple possible locations
                        actual_path = find_media_file(path, file_path, facebook_directories)
                        
                        if actual_path:
                            # Move media to output folder
                            new_path = move_to_output(actual_path, media_type, title, creation_timestamp)
                            # Change metadata of the moved media
                            change_metadata_date(new_path, creation_timestamp)
                            count += 1
                            print(f"Processed {media_type}: {os.path.basename(actual_path)}")
                        else:
                            print(f"Warning: Media file not found: {path}")
        
        # Move processed conversation folder to "done" folder (only for Facebook directory structure)
        if facebook_directories:
            conversation_dir = os.path.dirname(file_path)
            if os.path.exists(conversation_dir) and any(fb_dir in conversation_dir for fb_dir in facebook_directories):
                # Create destination path in done folder
                dest_dir = os.path.join(done_dir, os.path.basename(conversation_dir))
                
                # Ensure destination doesn't already exist
                if os.path.exists(dest_dir):
                    base_name = os.path.basename(conversation_dir)
                    counter = 1
                    while os.path.exists(os.path.join(done_dir, f"{base_name}_{counter}")):
                        counter += 1
                    dest_dir = os.path.join(done_dir, f"{base_name}_{counter}")
                
                shutil.move(conversation_dir, dest_dir)
                print(f"Moved conversation folder to: {dest_dir}")
        
        print("->" + title + " extract ended with a total of " + str(count) + " media(s)")
        
    except Exception as ex:
        print("->" + title + " extract ended with error : " + str(ex))
        import traceback
        traceback.print_exc()
        
        # Move to error folder (only for Facebook directory structure)
        if facebook_directories:
            try:
                conversation_dir = os.path.dirname(file_path)
                if os.path.exists(conversation_dir) and any(fb_dir in conversation_dir for fb_dir in facebook_directories):
                    # Create destination path in error folder
                    dest_dir = os.path.join(error_dir, os.path.basename(conversation_dir))
                    
                    # Ensure destination doesn't already exist
                    if os.path.exists(dest_dir):
                        base_name = os.path.basename(conversation_dir)
                        counter = 1
                        while os.path.exists(os.path.join(error_dir, f"{base_name}_{counter}")):
                            counter += 1
                        dest_dir = os.path.join(error_dir, f"{base_name}_{counter}")
                    
                    shutil.move(conversation_dir, dest_dir)
                    print(f"Moved conversation folder to error: {dest_dir}")
            except Exception as move_error:
                print(f"Could not move to error folder: {move_error}")

print("Processing completed!")