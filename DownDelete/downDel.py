import os 
import shutil

folder = "c:\\Users\\Dimi\\Downloads"

for filename in os.listdir(folder):
    if filename.endswith(".mp3"):
        file_path = os.path.join(folder, filename)
        try:
            shutil.move(file_path, "c:\\Users\\Dimi\\Music")

        except Exception as e:
            print(f"Error moving file {file_path}: {e}")

    elif filename.endswith(".mp4"):
        file_path = os.path.join(folder, filename)
        try:
            shutil.move(file_path, "c:\\Users\\Dimi\\Videos")

        except Exception as e:
            print(f"Error moving file {file_path}: {e}")

    elif filename.endswith(".pdf"):
        file_path = os.path.join(folder, filename)
        try:
            shutil.move(file_path, "c:\\Users\\Dimi\\Documents")

        except Exception as e:
            print(f"Error moving file {file_path}: {e}")

    elif filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        file_path = os.path.join(folder, filename)
        try:
            shutil.move(file_path, "c:\\Users\\Dimi\\Pictures")

        except Exception as e:
            print(f"Error moving file {file_path}: {e}")

    else:
        delete_path = os.path.join(folder, filename)
        try:
            os.remove(delete_path)

        except Exception as e:
            print(f"Error deleting file {delete_path} or it's a folder: {e}")
        