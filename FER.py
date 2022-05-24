from keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import cv2

model = load_model("./expression_analysis/model")
class_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
face_classifier = cv2.CascadeClassifier('./expression_analysis/haarcascade_frontalface_default.xml')

def scoring_expression(expression_weights):
    score = 0
    angry = expression_weights[0]
    if angry < 0.1:
        score += 10
    elif angry < 0.3:
        score += 5
    elif angry < 0.5:
        score += 1
    else:
        score -= 10
    disgust = expression_weights[1]
    if disgust < 0.1:
        score += 10
    elif disgust < 0.3:
        score += 5
    elif disgust < 0.5:
        score += 1
    else:
        score -= 7
    fear = expression_weights[2]
    if fear < 0.25:
        score += 10
    elif fear < 0.4:
        score += 5
    elif fear < 0.6:
        score += 1
    happy = expression_weights[3]
    if happy < 0.1:
        score -= 5
    elif happy <0.3:
        score += 3
    elif happy < 0.5:
        score += 7
    elif happy < 0.7:
        score += 10
    elif happy < 0.85:
        score += 5
    else:
        score -= 5
    neutral = expression_weights[4]
    if neutral < 0.1:
        score -= 5
    elif neutral < 0.3:
        score += 5
    elif neutral < 0.5:
        score += 7
    elif neutral < 0.8:
        score += 10
    else:
        score += 5
    sad = expression_weights[5]
    if sad < 0.2:
        score += 10
    elif sad < 0.3:
        score += 5
    elif sad < 0.5:
        score += 1
    elif sad < 0.7:
        score -= 3
    else:
        score -=7
    surprise = expression_weights[6]
    if surprise < 0.3:
        score += 10
    elif surprise < 0.5:
        score += 5
    else:
        score += 1
    return round(score/7, 2)

def face_detector(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return (0, 0, 0, 0), np.zeros((48, 48), np.uint8), img
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]

    try:
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation  =  cv2.INTER_AREA)
    except:
        return (x,w,y,h), np.zeros((48,48), np.uint8), img
    return (x,w,y,h), roi_gray, img


def analyze_face(video_file):
    labels= []
    cap = cv2.VideoCapture(video_file)
    c = 0
    expression_matrix = {}
    frame_cnt = 0
    total_frames = 0
    while True:
        c += 1
        ret, frame = cap.read()
        total_frames+=1
        if not ret:
            break
        if c % 10 == 0:
            rect, face, image = face_detector(frame)
            if np.sum([face]) != 0.0:
                roi = face.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # make a prediction on the ROI, then lookup the class
                preds = model.predict(roi)[0]
                labels.append(class_labels[preds.argmax()])  
                expression_matrix[frame_cnt]=preds.tolist()
                frame_cnt += 1

    cap.release()
    cv2.destroyAllWindows()
    expression_weights = np.mean(np.array(list(expression_matrix.values())), axis=0)
    score = scoring_expression(expression_weights)
    most_common_label = max(labels, key = labels.count)
    print(most_common_label)
    return score*10, expression_matrix, expression_weights, total_frames

#print(analyze_face("./test_interviews/test1.mp4"))