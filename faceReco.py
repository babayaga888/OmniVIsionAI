from keras_facenet import FaceNet
import os
from PIL import Image as Img
from numpy import asarray
from numpy import expand_dims
from mtcnn.mtcnn import MTCNN  # Import MTCNN
# from matplotlib import pyplot
# from keras.models import load_model
import numpy as np
import tensorflow as tf
import pickle
import cv2
# from retinaface import RetinaFace
import re
from functools import wraps
from retinaface import RetinaFace

model = FaceNet()
# detector = MTCNN()  # Initialize the MTCNN detector

def memoize(function):
    cache = {}
    @wraps(function)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)

        if key not in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]
    return wrapper


class Face_embeddings:
    def __init__(self, folder, database):
        self.folder = folder
        self.database = database
    @memoize
    def align_face(self, image):
        results = RetinaFace.detect_faces(image)
        if isinstance(results, dict):
            for  face_info in results.values():
                x1, y1, x2, y2 = face_info['facial_area'][:4]
       

                # x1, y1 = abs(x1), abs(y1)
                # x2, y2 = x1 + width, y1 + height

                aligned_face = image[y1:y2, x1:x2]

                print("Aligned face dimensions:", aligned_face.shape if aligned_face is not None else None)
                return aligned_face

    @memoize
    def face_embedding(self):
        for folder in os.listdir(self.folder):
            if not os.path.isdir(os.path.join(self.folder, folder)):
                continue
            folder_path = os.path.join(self.folder, folder)
            for filename in os.listdir(folder_path):
                path = os.path.join(folder_path, filename)
                gbr1 = cv2.imread(path)

                if gbr1 is not None:
                    # Convert BGR to RGB
                    rgb_image = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)

                    # Align the face using MTCNN
                    aligned_face = self.align_face(rgb_image)
                    if aligned_face is not None:
                        # Resize aligned face
                        aligned_face = cv2.resize(aligned_face, (160, 160))

                        # Expand dimensions for FaceNet input
                        aligned_face = expand_dims(aligned_face, axis=0)

                        # Generate face embedding using FaceNet
                        signature = model.embeddings(aligned_face)

                        self.database[os.path.splitext(filename)[0]] = signature
                    else:
                        print(f"Error: No face detected in the image at {path}")
                else:
                    print("Error: Unable to load the image at", path)


    @memoize
    def pickle_dump(self, folder_name):
        # Create the folder if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # Full file path inside the created folder
        file_path = os.path.join(folder_name, "data.pkl")
        # Save the 'database' dictionary to a file inside the folder using pickle
        with open(file_path, "wb") as myfile:
            pickle.dump(self.database, myfile)
    @memoize
    def pickle_load(self, folder_name):
        # Full file path inside the specified folder
        file_path = os.path.join(folder_name, "data.pkl")
        # Load the 'database' dictionary from the file using pickle
        with open(file_path, "rb") as myfile:
            self.database = pickle.load(myfile)




# import os
# import re
@memoize
def rename_database(original_database, new_database):
    for key, value in original_database.items():
        # Extract the name part by removing the number in parentheses
        name_parts = key.rsplit(' ', 1)  # Split only at the last space
        if len(name_parts) == 2:
            name, number = name_parts
            new_key = name
            new_database[new_key] = value
        else:
            print(f"Invalid key format: {key}")





# if __name__ == "__main__":
#     directory_path = "/path/to/your/directory"  # Replace this with the actual directory path
#     base_name = "germel"  # Replace this with the base name of the files you want to rename
#     rename_files(directory_path, base_name)