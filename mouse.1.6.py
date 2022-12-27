import cv2
import pyautogui
import mediapipe as mp
from math import degrees, atan2

pyautogui.PAUSE = 0
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)

cam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #640
cam_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #480
width = 2507.75#1920
height = 1570.9#1080
noise_filter = 3
boundary = 150
lx, ly = 0,0
flag = 0
#print(cam_width, cam_height)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
      for hand_landmarks in results.multi_hand_landmarks:
        THUMB_MCP = [hand_landmarks.landmark[2].x * width, hand_landmarks.landmark[2].y * height]
        THUMB_TIP = [hand_landmarks.landmark[4].x * width, hand_landmarks.landmark[4].y * height]
        INDEX_FINGER_MCP = [hand_landmarks.landmark[5].x * width, hand_landmarks.landmark[5].y * height]
        INDEX_FINGER_PIP = [hand_landmarks.landmark[6].x * width, hand_landmarks.landmark[6].y * height]
        INDEX_FINGER_TIP = [hand_landmarks.landmark[8].x * width, hand_landmarks.landmark[8].y * height]
        MIDDLE_FINGER_MCP= [hand_landmarks.landmark[9].x * width, hand_landmarks.landmark[9].y * height]
        MIDDLE_FINGER_PIP = [hand_landmarks.landmark[10].x * width, hand_landmarks.landmark[10].y * height]
        MIDDLE_FINGER_TIP = [hand_landmarks.landmark[12].x * width, hand_landmarks.landmark[12].y * height]
        RING_FINGER_MCP = [hand_landmarks.landmark[13].x * width, hand_landmarks.landmark[13].y * height]
        RING_FINGER_PIP = [hand_landmarks.landmark[14].x * width, hand_landmarks.landmark[14].y * height]
        RING_FINGER_TIP = [hand_landmarks.landmark[16].x * width, hand_landmarks.landmark[16].y * height]

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.rectangle(image, (0, 0), (cam_width-boundary, cam_height-boundary), (255,255,255), 2)

        current_x = int(lx + (INDEX_FINGER_TIP[0]-lx)/noise_filter)
        current_y = int(ly + (INDEX_FINGER_TIP[1]-ly)/noise_filter)

        pyautogui.moveTo(current_x, current_y)

        l_click_angle = abs(degrees(atan2(INDEX_FINGER_TIP[1]-THUMB_MCP[1], INDEX_FINGER_TIP[0]-THUMB_MCP[0]) - atan2(THUMB_TIP[1]-THUMB_MCP[1], THUMB_TIP[0]-THUMB_MCP[0])))
        r_click_angle = abs(degrees(atan2(INDEX_FINGER_TIP[1]-INDEX_FINGER_MCP[1], INDEX_FINGER_TIP[0]-INDEX_FINGER_MCP[0]) - atan2(MIDDLE_FINGER_TIP[1]-INDEX_FINGER_MCP[1], MIDDLE_FINGER_TIP[0]-INDEX_FINGER_MCP[0])))

        drag = RING_FINGER_TIP[1] < RING_FINGER_PIP[1]

        if not drag:
          if flag == 1:
            pyautogui.mouseUp()
            flag = 0
          if l_click_angle > 60 and r_click_angle > 30:
            pyautogui.click()
          elif r_click_angle < 30:
            pyautogui.click(button='right')
        else:
          if flag == 0:
            pyautogui.mouseDown()
            flag = 1

        cv2.imshow('arhsim', image)
        lx, ly = current_x, current_y

    except:
      cv2.imshow('arhsim', image)
      continue

    if l_click_angle > 120:
      print('gesture exit')
      break

    if cv2.waitKey(1) & 0xFF == 27:
      break
  cap.release()
  cv2.destroyAllWindows()
