import cv2
import pyautogui
import mediapipe as mp
from math import degrees, atan2

pyautogui.PAUSE = 0
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#webcam input
screen_width = 1920
screen_height = 1080

cam_width = 1280
cam_height = 720

top_left_margin = 40
bottom_right_margin = 160

x_factor = screen_width / (screen_width - (bottom_right_margin + top_left_margin))
y_factor = screen_height / (screen_height - (bottom_right_margin + top_left_margin))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

noise_filter = 1.4
lx, ly = 0,0
flag = 0

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
        THUMB_MCP = [hand_landmarks.landmark[2].x * screen_width, hand_landmarks.landmark[2].y * screen_height]
        THUMB_TIP = [hand_landmarks.landmark[4].x * screen_width, hand_landmarks.landmark[4].y * screen_height]
        INDEX_FINGER_MCP = [hand_landmarks.landmark[5].x * screen_width, hand_landmarks.landmark[5].y * screen_height]
        INDEX_FINGER_PIP = [hand_landmarks.landmark[6].x * screen_width, hand_landmarks.landmark[6].y * screen_height]
        INDEX_FINGER_TIP = [hand_landmarks.landmark[8].x * screen_width, hand_landmarks.landmark[8].y * screen_height]
        MIDDLE_FINGER_MCP= [hand_landmarks.landmark[9].x * screen_width, hand_landmarks.landmark[9].y * screen_height]
        MIDDLE_FINGER_PIP = [hand_landmarks.landmark[10].x * screen_width, hand_landmarks.landmark[10].y * screen_height]
        MIDDLE_FINGER_TIP = [hand_landmarks.landmark[12].x * screen_width, hand_landmarks.landmark[12].y * screen_height]
        RING_FINGER_MCP = [hand_landmarks.landmark[13].x * screen_width, hand_landmarks.landmark[13].y * screen_height]
        RING_FINGER_PIP = [hand_landmarks.landmark[14].x * screen_width, hand_landmarks.landmark[14].y * screen_height]
        RING_FINGER_TIP = [hand_landmarks.landmark[16].x * screen_width, hand_landmarks.landmark[16].y * screen_height]

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.rectangle(image, (top_left_margin, top_left_margin), (cam_width-bottom_right_margin, cam_height-bottom_right_margin), (255,255,255), 3)

        current_x = (INDEX_FINGER_TIP[0] - top_left_margin) * x_factor
        current_y = (INDEX_FINGER_TIP[1] - top_left_margin) * y_factor

        mod_x = lx + (current_x - lx)/noise_filter
        mod_y = ly + (current_y - ly)/noise_filter

        pyautogui.moveTo(mod_x, mod_y)

        l_click_angle = abs(degrees(atan2(INDEX_FINGER_TIP[1]-THUMB_MCP[1], INDEX_FINGER_TIP[0]-THUMB_MCP[0]) - atan2(THUMB_TIP[1]-THUMB_MCP[1], THUMB_TIP[0]-THUMB_MCP[0])))
        r_click_angle = abs(degrees(atan2(INDEX_FINGER_TIP[1]-INDEX_FINGER_MCP[1], INDEX_FINGER_TIP[0]-INDEX_FINGER_MCP[0]) - atan2(MIDDLE_FINGER_TIP[1]-INDEX_FINGER_MCP[1], MIDDLE_FINGER_TIP[0]-INDEX_FINGER_MCP[0])))

        drag = RING_FINGER_TIP[1] < RING_FINGER_PIP[1]

        if not drag:
          if flag == 1:
            pyautogui.mouseUp()
            flag = 0
          if l_click_angle > 69 and r_click_angle > 30:
            pyautogui.doubleClick()
          elif r_click_angle < 30:
            pyautogui.click(button='right')
        else:
          if flag == 0:
            pyautogui.mouseDown()
            flag = 1

        cv2.imshow('arhsim', image)
        lx, ly = mod_x, mod_y

    except:
      cv2.imshow('arhsim', image)
      print(1)
      continue

    if l_click_angle > 120 and INDEX_FINGER_TIP[1] > INDEX_FINGER_MCP[1]:
      print('gesture exit')
      break

    if cv2.waitKey(1) & 0xFF == 27:
      break

  cap.release()
  cv2.destroyAllWindows()
