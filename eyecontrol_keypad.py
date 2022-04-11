import cv2
import numpy as np
import dlib
import math


virtual_keyboard = np.zeros((1000, 1000, 3), np.uint8)

#dictionary containing the letters, each one associated with an index.

keys_set_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T",
              5: "A", 6: "S", 7: "D", 8: "F", 9: "G",
              10: "Z", 11: "X", 12: "C", 13: "V", 14: "B",
              15: "Y", 16: "U",  17: "I", 18: "O", 19: "P",
              20: "H", 21: "J", 22: "K", 23: "L", 24: "N", 25: "M"

              }

# keys_set_2 = {
#     0: "Y", 1: "U",  2: "I", 3: "O", 4: "P",
#     5: "H", 6: "J", 7: "K", 8: "L", 9: "N", 10: "M"
#
# }


# we used the detector to detect the frontal face
detector = dlib.get_frontal_face_detector()

# it will detect the facial landmark points
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_HERSHEY_DUPLEX
font1 = cv2.FONT_ITALIC

# IT WILL CALCULATE MIDPOINTS BTW TWO POINTS OF EYE

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def blinking_ratio(eye_points, facial_landmarks):
    # to detect the left_side of a left eye
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)

    # to detect the right_side of the left eye
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)

    # to detect the mid point for the center of top in left eye
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))

    # to detect the mid point for the center of the bottom in left eye
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    # to calculate horizontal line distance
    hor_line_lenght = math.hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))

    # to calculate vertical line distance
    ver_line_lenght = math.hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    # to calculate ratio
    ratio = hor_line_lenght / ver_line_lenght

    return ratio


def get_gaze_ratio(eye_points, facial_landmarks):
    # Gaze detection
    # getting the area from the frame of the left eye only
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)],
                               np.int32)

    # cv2.polylines(frame, [left_eye_region], True, 255, 2)
    height, width, _ = frame.shape

    # create the mask to extract exactly the inside of the left eye and exclude all the white part.
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)


    # out rectangular shapes from the image, so we take all the extremes points of the eyes to get the rectangle
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])
    gray_eye = eye[min_y: max_y, min_x: max_x]

    # threshold to separate iris and pupil from the white part of the eye.
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)

    # dividing the eye into 2 parts .left_side and right_side.
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1

    elif right_side_white == 0:
        gaze_ratio = 5

    else:
        gaze_ratio = left_side_white / right_side_white
    return (gaze_ratio)


# for setting keyboards and accessing each and every icon

def letter(letter_index, text, letter_light):
    # Keys
    # Each key is simply a rectangle containing some text. So we define the sizes and we draw the rectangle.
    if letter_index == 0:
        x = 0
        y = 0
    elif letter_index == 1:
        x = 200
        y = 0
    elif letter_index == 2:
        x = 400
        y = 0

    elif letter_index == 3:
        x = 600
        y = 0
    elif letter_index == 4:
        x = 800
        y = 0

    elif letter_index == 5:
        x = 0
        y = 200
    elif letter_index == 6:
        x = 200
        y = 200
    elif letter_index == 7:
        x = 400
        y = 200

    elif letter_index == 8:
        x = 600
        y = 200
    elif letter_index == 9:
        x = 800
        y = 200

    elif letter_index == 10:
        x = 0
        y = 400
    elif letter_index == 11:
        x = 200
        y = 400
    elif letter_index == 12:
        x = 400
        y = 400

    elif letter_index == 13:
        x = 600
        y = 400
    elif letter_index == 14:
        x = 800
        y = 400
    elif letter_index == 15:
        x = 0
        y = 600

    elif letter_index == 16:
        x = 200
        y = 600

    elif letter_index == 17:
        x = 400
        y = 600
    elif letter_index == 18:
        x = 600
        y = 600
    elif letter_index == 19:
        x = 800
        y = 600

    elif letter_index == 20:
        x = 0
        y = 800
    elif letter_index == 21:
        x = 200
        y = 800

    elif letter_index == 22:
        x = 400
        y = 800
    elif letter_index == 23:
        x = 600
        y = 800
    elif letter_index == 24:
        x = 800
        y = 800
    elif letter_index == 25:
        x = 0
        y = 1000

    width = 200
    height = 200
    th = 3  # thickness


    if letter_light == True:
        cv2.rectangle(virtual_keyboard, (x + th, y + th), (x + width - th, y + height - th), (0, 250, 0), -1)

    else:
        cv2.rectangle(virtual_keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 250, 0), th)





    # Inside the rectangle now we put the letter. So we define the sizes and style of the text and we center it.
    # Text settings
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 10
    font_th = 4
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(virtual_keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)

vid = cv2.VideoCapture(0)
frames = 0
letter_index = 0

# create a white board  where we will put the letters we click from the virtual keyboard.
whiteboard = np.zeros((700, 700), np.uint8)
whiteboard[:] = (255)
blinking_frames = 0

# blinking letters
text_written_by_eyes = " "

while True:
    _, frame = vid.read()
    frames = frames + 1

    virtual_keyboard[:] = (0, 0, 0)


    new_frame = np.zeros((400, 400, 3), np.uint8)

    # change the color of the frame captured by webcam to grey
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    active_letter = keys_set_1[letter_index]
    print("active letter is -:", active_letter)




    # to detect faces from grey color frame
    faces = detector(gray)
    for face in faces:

        # to detect the landmarks of a face
        landmarks = predictor(gray, face)
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

        # Left
        # eye
        # points: (36, 37, 38, 39, 40, 41)
        # Right
        # eye
        # points: (42, 43, 44, 45, 46, 47)

        left_eye_ratio = blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio1 = (left_eye_ratio + right_eye_ratio) / 2
        print("blinking ratio", blinking_ratio1)

        if blinking_ratio1 > 5.7:
            cv2.putText(frame, "BLINKING", (50, 150), font, 7, (255, 0, 0))

            blinking_frames = blinking_frames + 1
            frames = frames - 1

            if blinking_frames == 5:
                text_written_by_eyes = text_written_by_eyes + active_letter
        else:
            blinking_frames = 0
        # threshold_eye = cv2.resize(threshold_eye,None ,fx = 5,fy = 5)
        # eye = cv2.resize(gray_eye, None,fx = 5,fy = 5)

        gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)

        gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2

        if gaze_ratio <= 1:
            cv2.putText(frame, "RIGHT", (50, 100), font1, 2, (0, 0, 255), 3)
            new_frame[:] = (0, 0, 255)
        elif 1 < gaze_ratio < 1.7:
            cv2.putText(frame, "CENTRE", (50, 100), font1, 2, (255, 0, 0), 3)
            new_frame[:] = (255, 0, 0)

        else:
            new_frame[:] = (0, 255, 0)  # red
            cv2.putText(frame, "LEFT", (50, 100), font1, 2, (0, 255, 0), 3)


        if frames == 25:
            letter_index = letter_index + 1
            frames = 0
        if letter_index == 25:
            letter_index = 0

        for i in range(25):
            if i == letter_index:
                light = True
            else:
                light = False
            letter(i, keys_set_1[i], light)
        # Finally we display the text on the board.
    cv2.putText(whiteboard, text_written_by_eyes, (10, 100), font, 4, 0, 3)

    cv2.imshow("Frame", frame)
    cv2.imshow("NEW_Frame", new_frame)
    cv2.imshow("KEYBOARD", virtual_keyboard)
    cv2.imshow("whiteboard", whiteboard)

    key = cv2.waitKey(1)
    # close the webcam when escape key is pressed
    if key == 27:
        break

vid.release()
cv2.destroyAllWindows()




