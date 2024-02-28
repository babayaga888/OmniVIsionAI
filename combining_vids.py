# import os
# import time
# from moviepy.editor import concatenate_videoclips, VideoFileClip

# # Function to get all video files in a folder with a specific extension
# def get_video_files(folder_path, extension=".avi"):
#     video_files = [f for f in os.listdir(folder_path) if f.endswith(extension)]
#     video_files.sort()  # Sort files based on name or timestamp
#     return video_files

# # Function to concatenate all video files in a folder
# def concatenate_all_videos(folder_path, extension=".mp4", stability_check_timeout=10):
#     video_files = get_video_files(folder_path, extension)
    
#     if not video_files:
#         print("No video files found in the folder.")
#         return

#     # Load and concatenate all video clips
#     clips = []
#     for file in video_files:
#         try:
#             file_path = os.path.join(folder_path, file)

#             # Check stability for a certain timeout
#             start_time = os.path.getmtime(file_path)
#             timeout = time.time() + stability_check_timeout

#             while time.time() < timeout:
#                 time.sleep(2)
#                 end_time = os.path.getmtime(file_path)

#                 if start_time == end_time:
#                     break
#                 else:
#                     print(f"File {file} is still being modified. Waiting for stability...")

#             else:
#                 print(f"Skipping file {file} due to stability timeout.")
#                 continue

#             clip = VideoFileClip(file_path)
#             clips.append(clip)

#         except Exception as e:
#             print(f"Error loading file {file}: {e}")

#     if not clips:
#         print("No valid video clips found in the folder.")
#         return

#     # Concatenate valid video clips
#     final_clip = concatenate_videoclips(clips)
#     output = final_clip.write_videofile('yawa.mp4')
    

#     print(f"Concatenated video saved to {output}")

# # Specify the folder path where your videos are stored
# folder_path = "C:/Users/PC/Desktop/v0.10/ipcamerarecordings/Section A"

# # Continuously concatenate videos from the folder with a stability check timeout of 10 seconds
# concatenate_all_videos(folder_path, stability_check_timeout=10)
