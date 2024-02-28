import cv2
import os
import time
import datetime
from PIL import Image
from numpy import asarray, expand_dims
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
import numpy as np
import pickle
from faceReco import Face_embeddings, rename_database
# from deep_sort_realtime.deepsort_tracker import DeepSort
# import dlib
import tensorflow as tf
from tensorflow.python.client import device_lib
from retinaface import RetinaFace

# cuda = tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None)
# print(cuda)

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)
print("TensorFlow version:", tf.__version__)

# if tf.test.gpu_device_name():
#     print("GPU device found:", tf.test.gpu_device_name())
# else:
#     print("No GPU support detected. TensorFlow will run on CPU.")


database = {}
file_path = r'C:\Users\PC\Desktop\V0.4\DataSetOmniVisionAI-2'
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5
max_distance = 0.9
video_writers = {}
fps_start_time = time.time()
fps_frame_count = 0
frame_rate = 0
correct_recognition = 0
total_frames = 0
new_database = {}

cap = cv2.VideoCapture(0)

detection_started_time = None
detection_threshold_seconds = 5

# detector = MTCNN()





#shape_predictor_path = r'C:\Users\User\projects\cctvSofty\v.0.2 - Copy\shape_predictor_68_face_landmarks.dat'

# predictor = dlib.shape_predictor(shape_predictor_path)

# tracker = DeepSort(max_age=5,max_cosine_distance=0.7)

# detector = SSD

frame_size = (int(cap.get(3)), int(cap.get(4)))
#frame_size = (460, 259)

fourcc = cv2.VideoWriter.fourcc(*'MJPG')

facenet = FaceNet()



facenet_model = Face_embeddings(file_path, database)


facenet_model.pickle_dump('embeddings')

facenet_model.face_embedding()

facenet_model.pickle_load('embeddings')



rename_database(database, new_database)


# for folder in os.listdir(file_path):
#     if not os.path.isdir(os.path.join(file_path, folder)):
#         continue
#     folder_path = os.path.join(file_path, folder)
#     face_embeddings = Face_embeddings(folder_path, database)
#     face_embeddings.face_embedding()

# # Save the database to a file
# face_embeddings.pickle_dump('embeddings')

# # Load the database from a file
# face_embeddings.pickle_load('embeddings')

def start_recording(identity):
    global video_writers, frame_size, fourcc

    # Create a folder with the person's name if it doesn't exist
    folder_name = f"recordings/{identity}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Start recording
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{folder_name}/{identity}_{current_time}.avi"
    video_writer = cv2.VideoWriter(file_name, fourcc, 10.0, frame_size)
    video_writers[identity] = video_writer
   

 

while True:
    _, frame = cap.read()

    #frame_resize = cv2.resize(frame,(600,00))
    if frame is not None and frame.shape[0]>0 and frame.shape[1]>0:
        results = RetinaFace.detect_faces(frame)
       
        print('result: ', results)

        fps_frame_count += 1

        if time.time() - fps_start_time >= 1.0:
                frame_rate = fps_frame_count / (time.time() - fps_start_time)
                fps_frame_count = 0
                fps_start_time = time.time()
        cv2.putText(frame, f'FPS: {frame_rate:.2f}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA) 
        if isinstance(results, dict):
            for face_info in results.values():
                facial_area = face_info['facial_area']
                x1, y1, x2, y2 = facial_area
                keypoints = face_info['landmarks']  # Get facial keypoints

                # x1, y1 = abs(x1), abs(y1)
                # x2, y2 = x1 + width, y1 + height

                print(y1, y2, x1, x2)

                gbr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gbr = Image.fromarray(gbr)
                gbr_array = np.array(gbr, dtype=None, copy=False, order=None)

                
                
                face = gbr_array[y1:y2, x1:x2]
                print("Aligned face dimensions:", face.shape if face is not None else None)

                face = Image.fromarray(face)
                face = face.resize((160, 160))
                face = np.array(face, dtype=None, copy=False, order=None) 

                face = expand_dims(face, axis=0)
                signature = facenet.embeddings(face)

                min_dist = 100 #the original minimum distance is 100
                identity = ''

                # detection_info = [
                #     ([result['box'][0], result['box'][1], result['box'][0] + result['box'][2], result['box'][1] + result['box'][3]],
                #     result['confidence'], 'face')
                #     for result in results
                # ]

                # tracks = tracker.update_tracks(detection_info, frame=frame)

                for key, value in new_database.items():
                    dist = np.linalg.norm(value - signature)
                    if dist < min_dist:
                        min_dist = dist
                        identity = key
                        # If the minimum distance is greater than the threshold (max_distance), mark it as stranger
                    if min_dist > max_distance:
                        identity = 'stranger'

                # # If the minimum distance is greater than the threshold (max_distance), mark it as unknown
                # if min_dist > max_distance:
                #     identity = 'stranger'
                


                total_frames += 1

                if identity != '' and identity != 'stranger':
                    correct_recognition += 1

                recognition_accuracy = (correct_recognition / total_frames) * 100
                cv2.putText(frame, f'Accuracy: {recognition_accuracy:.2f}%', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                # Draw the text on top of the bounding box
                text_position = (x1, y1 - 10)
                cv2.putText(frame, identity, text_position, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Draw facial keypoints if available
                # if keypoints is not None:
                #     for key, point in keypoints.items():
                #         cv2.circle(frame, point, 2, (255, 255, 0), -1)  # Draw red circles for keypoints

                # Start recording for recognized faces or unknown faces
                # if identity != '':
                #     start_recording(identity)
                if identity != '':
                    if identity not in video_writers:
                        # Start recording for recognized faces or unknown faces
                            start_recording(identity)
                    
                    # Write frame to the video if recording is active
                    if identity == 'stranger' or identity != '':
                        video_writers[identity].write(frame)
                else:
                    # Stop recording for this identity if it was recording
                    if identity in video_writers:
                        video_writers[identity].release()
                        del video_writers[identity]
                

                cv2.imshow('res', frame)

                # Write frame to the video if recording is active
                # for identity in video_writers:
                #     if identity == 'stranger' or identity in results:
                #         video_writers[identity].write(frame)
            
        else:
            print('No image')
    


        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release video writers
for identity in video_writers:
    video_writers[identity].release()
# for identity, video_writer in video_writers.items():
#     video_writer.release()

# Release the capture
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()