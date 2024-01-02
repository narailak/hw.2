import cv2
import mediapipe as mp
import time
import pyfirmata

time.sleep(2.0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

def check_user_input(input):
    try:
        val = int(input)
        bv = True
    except ValueError:
        try:
            val = float(input)
            bv = True
        except ValueError:
            bv = False
    return bv

cport = input('Enter the camera port: ')
while not check_user_input(cport):
    print('Please enter a number not a string')
    cport = input('Enter the camera port: ')

comport = input('Enter the Arduino board COM port: ')
while not check_user_input(comport):
    print('Please enter a number not a string')
    comport = input('Enter the Arduino board COM port: ')

board = pyfirmata.Arduino('COM' + comport)
led_1 = board.get_pin('d:13:o')
led_2 = board.get_pin('d:12:o')
led_3 = board.get_pin('d:11:o')
led_4 = board.get_pin('d:10:o')
led_5 = board.get_pin('d:9:o')

def led(fingers, led_1, led_2, led_3, led_4, led_5):
        if 'Thumb' in fingers:
            led_1.write(1)
        else:
            led_1.write(0)
        
        if 'Index' in fingers:
            led_2.write(1)
        else:
            led_2.write(0)
        
        if 'Middle' in fingers:
            led_3.write(1)
        else:
            led_3.write(0)
        
        if 'Ring' in fingers:
            led_4.write(1)
        else:
            led_4.write(0)
        
        if 'Pinky' in fingers:
            led_5.write(1)
        else:
            led_5.write(0)
            
            


video = cv2.VideoCapture(int(cport))
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        success, img = video.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        fingers = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 4:
                        id4 = int(id)
                        cx4 = cx
                    if id == 3:
                        id3 = int(id)
                        cx3 = cx
                    if id == 7:
                        id7 = int(id)
                        cy7 = cy
                    if id == 8:
                        id8 = int(id)
                        cy8 = cy
                    if id == 10:
                        id10 = int(id)
                        cy10 = cy
                    if id == 12:
                        id12 = int(id)
                        cy12 = cy
                    if id == 15:
                        id15 = int(id)
                        cy15 = cy
                    if id == 16:
                        id16 = int(id)
                        cy16 = cy
                    if id == 19:
                        id19 = int(id)
                        cy19 = cy
                    if id == 20:
                        id20 = int(id)
                        cy20 = cy
                        
                if cx3 < cx4: fingers.append ('Thumb')
                if cy8 < cy7: fingers.append ('Index')
                if cy12 < cy10: fingers.append ('Middle')
                if cy16 < cy15: fingers.append ('Ring')
                if cy20 < cy19: fingers.append ('Pinky')
                
                mp_draw.draw_landmarks(img, handLms, mp_hand.HAND_CONNECTIONS)
        led(fingers, led_1, led_2, led_3, led_4, led_5)
        cv2.putText(img, str(str(fingers)), (55, 395), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (255, 0, 255), 2)
        cv2.imshow("Image", img)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

video.release()
cv2.destroyAllWindows()