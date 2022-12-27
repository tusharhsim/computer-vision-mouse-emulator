import cv2
import math
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)

width = 1920#cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = 1080#cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
last_x, last_y = 0,0
i=0
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print(1)
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
      for hand_landmarks in results.multi_hand_landmarks:
        WRIST = [int(hand_landmarks.landmark[0].x * width), int(hand_landmarks.landmark[0].y * height)]
        THUMB_CMC = [int(hand_landmarks.landmark[1].x * width), int(hand_landmarks.landmark[1].y * height)]
        THUMB_MCP = [int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)]
        THUMB_IP = [int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)]
        THUMB_TIP = [int(hand_landmarks.landmark[4].x * width), int(hand_landmarks.landmark[4].y * height)]
        INDEX_FINGER_MCP = [int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)]
        INDEX_FINGER_PIP = [int(hand_landmarks.landmark[6].x * width), int(hand_landmarks.landmark[6].y * height)]
        INDEX_FINGER_DIP = [int(hand_landmarks.landmark[7].x * width), int(hand_landmarks.landmark[7].y * height)]
        INDEX_FINGER_TIP = [int(hand_landmarks.landmark[8].x * width), int(hand_landmarks.landmark[8].y * height)]
        MIDDLE_FINGER_MCP = [int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)]
        MIDDLE_FINGER_PIP = [int(hand_landmarks.landmark[10].x * width), int(hand_landmarks.landmark[10].y * height)]
        MIDDLE_FINGER_DIP = [int(hand_landmarks.landmark[11].x * width), int(hand_landmarks.landmark[11].y * height)]
        MIDDLE_FINGER_TIP = [int(hand_landmarks.landmark[12].x * width), int(hand_landmarks.landmark[12].y * height)]
        RING_FINGER_MCP = [int(hand_landmarks.landmark[13].x * width), int(hand_landmarks.landmark[13].y * height)]
        RING_FINGER_PIP = [int(hand_landmarks.landmark[14].x * width), int(hand_landmarks.landmark[14].y * height)]
        RING_FINGER_DIP = [int(hand_landmarks.landmark[15].x * width), int(hand_landmarks.landmark[15].y * height)]
        RING_FINGER_TIP = [int(hand_landmarks.landmark[16].x * width), int(hand_landmarks.landmark[16].y * height)]
        PINKY_MCP = [int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height)]
        PINKY_PIP = [int(hand_landmarks.landmark[18].x * width), int(hand_landmarks.landmark[18].y * height)]
        PINKY_DIP = [int(hand_landmarks.landmark[19].x * width), int(hand_landmarks.landmark[19].y * height)]
        PINKY_TIP = [int(hand_landmarks.landmark[20].x * width), int(hand_landmarks.landmark[20].y * height)]

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if abs(math.degrees(math.atan2(INDEX_FINGER_TIP[1]-THUMB_MCP[1], INDEX_FINGER_TIP[0]-THUMB_MCP[0]) - math.atan2(THUMB_TIP[1]-THUMB_MCP[1], THUMB_TIP[0]-THUMB_MCP[0])))>70:
          print(abs(math.degrees(math.atan2(INDEX_FINGER_TIP[1]-THUMB_MCP[1], INDEX_FINGER_TIP[0]-THUMB_MCP[0]) - math.atan2(THUMB_TIP[1]-THUMB_MCP[1], THUMB_TIP[0]-THUMB_MCP[0]))))
        #print(abs(math.degrees(math.atan2(THUMB_TIP[1]-PINKY_MCP[1], THUMB_TIP[0]-PINKY_MCP[0]) - math.atan2(PINKY_TIP[1]-PINKY_MCP[1], PINKY_TIP[0]-PINKY_MCP[0]))))
        #print(INDEX_FINGER_TIP[1] > INDEX_FINGER_PIP[1] and MIDDLE_FINGER_TIP[1] > MIDDLE_FINGER_PIP[1] and RING_FINGER_TIP[1] > RING_FINGER_PIP[1])
        cv2.imshow('arhsim', image)
    except:
      cv2.imshow('arhsim', image)
      #print(2)
      continue

    last_x = INDEX_FINGER_TIP[0]
    last_y = INDEX_FINGER_TIP[1]

    if cv2.waitKey(5) & 0xFF == 27:
      break

  cap.release()
  cv2.destroyAllWindows()
