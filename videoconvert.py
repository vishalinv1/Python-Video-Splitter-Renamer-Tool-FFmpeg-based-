import subprocess
import os
import glob
import shutil
import re

def split_video_into_segments(input_file, output_folder):
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Run ffmpeg command to split the video into 2-minute segments
        subprocess.run([
            'ffmpeg', '-i', input_file, '-c', 'copy', '-map', '0', '-segment_time', '120', '-f', 'segment', '-reset_timestamps', '1',
            f"{output_folder}/{os.path.splitext(os.path.basename(input_file))[0]}_part%03d{os.path.splitext(input_file)[1]}"
        ], check=True)
        
        # Remove segments with duration less than 50 seconds
        part_files = glob.glob(f"{output_folder}/{os.path.splitext(os.path.basename(input_file))[0]}_part*{os.path.splitext(input_file)[1]}")
        
        for part_file in part_files:
            result = subprocess.run([
                'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', part_file
            ], capture_output=True, text=True)
            duration = float(result.stdout.strip())
            if duration < 50:
                os.remove(part_file)
                print(f"Removed {part_file} due to short duration ({duration} seconds)")
            else:
                print(f"Kept {part_file} with duration {duration} seconds")
        
        print(f"Successfully split {input_file} into 2-minute segments")
    except FileNotFoundError:
        print("ffmpeg is not installed or not found in PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def rename_videos_sequentially(directory='.', extensions=None):
    """
    Rename video files sequentially only when there are name conflicts.
    Preserves original names when possible.
    
    Args:
        directory (str): Directory containing video files
        extensions (list): List of video file extensions to consider (e.g., ['.mp4', '.avi'])
                          If None, use common video extensions
    """
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    
    # Get all video files in the directory
    video_files = []
    for ext in extensions:
        video_files.extend(glob.glob(os.path.join(directory, f'*{ext}')))
    
    if not video_files:
        print(f"No video files found in {directory}")
        return
    
    # Sort files to ensure consistent ordering
    video_files.sort()
    
    print(f"Found {len(video_files)} video files to process")
    
    # Track filenames already processed to avoid conflicts
    processed_filenames = set()
    next_number = 1  # For sequential numbering when needed
    
    # Create a temporary directory for the renaming process
    temp_dir = os.path.join(directory, "temp_rename")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    try:
        # First move all files to temp dir with unique temp names
        temp_files = []
        for i, file_path in enumerate(video_files):
            file_name = os.path.basename(file_path)
            ext = os.path.splitext(file_name)[1].lower()
            temp_name = f"temp_{i}{ext}"
            temp_path = os.path.join(temp_dir, temp_name)
            os.rename(file_path, temp_path)
            # Store original name and temp path
            original_name = os.path.splitext(file_name)[0]
            temp_files.append((temp_path, original_name, ext))
        
        # Then move back with conflict resolution
        for temp_path, original_name, ext in temp_files:
            # Try to use original name first if not already taken
            target_name = original_name + ext
            target_path = os.path.join(directory, target_name)
            
            # If the name exists in our processed set, use a numbered name instead
            if target_name.lower() in processed_filenames:
                # Find next available number
                while True:
                    numbered_name = f"{next_number}{ext}"
                    numbered_path = os.path.join(directory, numbered_name)
                    if numbered_name.lower() not in processed_filenames:
                        target_name = numbered_name
                        target_path = numbered_path
                        next_number += 1
                        break
                    next_number += 1
                print(f"Renamed duplicate to: {target_name}")
            else:
                print(f"Kept original name: {target_name}")
            
            # Move the file and track the name
            os.rename(temp_path, target_path)
            processed_filenames.add(target_name.lower())
            
    except Exception as e:
        print(f"Error during renaming: {e}")
    finally:
        # Clean up temp directory if empty
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)

if __name__ == "__main__":
    # Define the video file extensions to look for
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
    
    # Find all video files in the current directory
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(ext))
    
    if not video_files:
        print("No video files found in the current directory.")
    else:
        output_folder = "output_videos"
        for input_file in video_files:
            split_video_into_segments(input_file, output_folder)
            os.remove(input_file)
            print(f"Deleted original video file: {input_file}")
        
        # After processing all videos, rename the output files sequentially
        print("\nRenaming all output videos sequentially...")
        rename_videos_sequentially(output_folder)
        print("Video renaming complete!")