from statistics import mode

import cv2
import time
from keras.models import load_model
import numpy as np

from Test.face_classification.src.utils.datasets import get_labels
from Test.face_classification.src.utils.inference import detect_faces
from Test.face_classification.src.utils.inference import draw_text
from Test.face_classification.src.utils.inference import draw_bounding_box
from Test.face_classification.src.utils.inference import apply_offsets
from Test.face_classification.src.utils.inference import load_detection_model
from Test.face_classification.src.utils.preprocessor import preprocess_input
val=[]
def ret_exp():
    global val
    x = np.mean(val) 
    val = []
    return x

def evaluvate(text):
    if text=='happy':
        val.append(1)
    elif text =='angry':
        val.append(2)
    elif text == 'sad':
        val.append(3)
    elif text =='suprise':
        val.append(4)
    else:
        val.append(5)






def expr(video_capture=None):
    em_list = []
    # parameters for loading data and images
    detection_model_path = 'Test/face_classification/trained_models/detection_models/haarcascade_frontalface_default.xml'
    emotion_model_path = 'Test/face_classification/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
    emotion_labels = get_labels('fer2013')

    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)

    # loading models
    face_detection = load_detection_model(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)

    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]

    # starting lists for calculating modes
    emotion_window = []

    # starting video streaming
    cv2.namedWindow('window_frame')
    # video_capture = cv2.VideoCapture(0)
    while True:
        bgr_image = video_capture.read()
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = detect_faces(face_detection, gray_image)

        for face_coordinates in faces:

            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)
            em_list.append(emotion_text)
            evaluvate(emotion_text)
            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            
            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))                
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
            else:
                color = emotion_probability * np.asarray((0, 255, 0))

            color = color.astype(int)
            color = color.tolist()
        

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                      color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.stop()
    cv2.destroyAllWindows()
   

