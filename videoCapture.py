import cv2
from PIL import Image
from numpy import asarray, expand_dims
import numpy as np
from keras_facenet import FaceNet

database = {}

model = FaceNet()

class FaceRecognition:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(
             "haarcascade_frontalface_default.xml")
        self.body_cascade = cv2.CascadeClassifier(
            "haarcascade_fullbody.xml")
        self.detection = False
        self.detection_stopped_time = None
        self.timer_started = False
        self.SECONDS_TO_RECORD_AFTER_DETECTION = 5

        # Initialize your face recognition model here (model not provided in the code)
       

    def detect_face(self, gbr1):
        wajah = self.face_cascade.detectMultiScale(gbr1, 1.1, 4)

        if len(wajah) > 0:
            x1, y1, width, height = wajah[0]
        else:
            x1, y1, width, height = 1, 1, 10, 10

        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr)
        gbr_array = asarray(gbr)

        face = gbr_array[y1:y2, x1:x2]

        face = Image.fromarray(face)
        face = face.resize((160, 160))
        face = asarray(face)

        face = face.astype('float32')
        mean, std = face.mean(), face.std()
        face = (face - mean) / std

        face = expand_dims(face, axis=0)
        signature = model.embeddings(face)  # Assuming you have the face recognition model defined

        return gbr1, x1, y1, x2, y2, signature

    def process_video(self):
        while True:
            _, gbr1 = self.cap.read()
            gbr1, x1, y1, x2, y2, signature = self.detect_face(gbr1)

            min_dist = 100
            identity = ' '
            for key, value in database.items():
                dist = np.linalg.norm(value - signature)
                if dist < min_dist:
                    min_dist = dist
                    identity = key

            cv2.putText(gbr1, identity, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.rectangle(gbr1, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.imshow('res', gbr1)

            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()
        self.cap.release()