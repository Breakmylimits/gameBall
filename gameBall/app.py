import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np
import time

def main():
    st.title("Game Ball")

    # Create a video capture object
    cap = cv2.VideoCapture(0)
    hd = HandDetector(detectionCon=0.5)

    width, height = 640, 480
    cap.set(3, width)
    cap.set(4, height)

    ball = cv2.imread('ball (2).png', cv2.IMREAD_UNCHANGED)
    box = cv2.imread('box.png', cv2.IMREAD_UNCHANGED)
    gameover = cv2.imread('over.jpg', cv2.IMREAD_UNCHANGED)

    ball = cv2.resize(ball, (40, 40))
    box = cv2.resize(box, (120, 26))
    gameover = cv2.resize(gameover, (width, height))
    gameover_display_time = None

    position = [50, 50]
    speedx, speedy = 2, 2
    score = 0

    
    # Define text properties
    posiText = (250, 50)  # Text position (x, y)
    font = cv2.FONT_HERSHEY_SIMPLEX  # Font type
    font_scale = 0.8  # Font size
    color = (191, 112, 243)  # Text color (BGR)
    thickness = 2  # Text thickness
    # Define the video stream placeholder
    
   
    # Define the video stream placeholder
    stframe = st.empty()

    # Create a button to stop the stream
    stop_button = st.button("Stop", key="stop_button")


    # Initialize a flag for stopping the stream
    stop_stream = False
 

    while not stop_stream:
        # Read frame from the video capture object
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to grab frame")
            break
        frame = cv2.flip(frame, 1)

        text = 'Score: ' + str(score)
        cv2.putText(frame, text, posiText, font, font_scale, color, thickness)


        frame = cvzone.overlayPNG(frame, ball, position)

    # Find hands in the image
        hand, frame = hd.findHands(frame, flipType=True)

        if position[1] < 50:
            speedy = -speedy
            position[0] -= 10

        if hand :
            bbox = hand[0]['bbox']
            x, y, w, h = bbox
            h1, w1, c = box.shape
            x1 = x - h1 // 2
            x1 = np.clip(x1, 5, 510)
            frame = cvzone.overlayPNG(frame, box, [x1, 447])

            if x1 - 10 < position[0] < x1 + w1 and 380 < position[1] < 380 + h1:
                speedy = -speedy
                position[0] += 30
                score += 1

        if position[1] > 400:
        
            if gameover_display_time is None:
                gameover_display_time = time.time()

            # Check if 3 seconds have passed
            if time.time() - gameover_display_time < 3:
                frame = gameover
                cvzone.putTextRect(gameover, 'Final score: ' + str(score), [150, 190], 1.9, 2, colorR=(0, 0, 0))
                cvzone.putTextRect(gameover, 'Wait 3 seconds to start a new game. ', [50, 305], 1.82, 2, colorR=(0, 0, 0))
               
            else:
                # After 3 seconds, hide the gameover screen and reset the game
                position=[50,50]
                speedx=2
                speedy=2
                score=0

                gameover=cv2.resize(gameover,(width,height))
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                gameover_display_time = None
          
     
           

        else:
            if position[0] >= 560 or position[0] <= 20:
                speedx = -speedx

            position[0] += speedx
            position[1] += speedy

   

        

   
      

    

        # Convert the image from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



        # Show the frame in the Streamlit app
        stframe.image(frame_rgb, channels='RGB', use_column_width=True)

        
        

        
        
          

        # Update stop_stream flag based on button state
        stop_stream = stop_button

    # Release the video capture object and close all OpenCV windows
    cap.release()
 

if __name__ == "__main__":
    main()
