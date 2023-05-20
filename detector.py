import cv2
import imutils
import time
from person import Person
from kafkaProducer import KafkaProducer

class Detector:
    
    def detect(self):
        producer = KafkaProducer()
        # Initializing the HOG person
        # detector
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture("video.mp4")
        ts = time.time() + 2
        while cap.isOpened():
            # Reading the video stream
            ret, image = cap.read()
            i=0
            if ret:
                image = imutils.resize(image, 
                                    width=min(800, image.shape[1]))
        
                if time.time() > ts:
                    ts = time.time() + 2
                    # Detecting all the regions 
                    # in the Image that has a 
                    # pedestrians inside it
                    (regions, _) = hog.detectMultiScale(image,
                                                        winStride=(4, 4),
                                                        padding=(4, 4),
                                                        scale=1.05)
            
                    # Drawing the regions in the 
                    # Image
                    for (x, y, w, h) in regions:
                        i = i + 1
                        cv2.rectangle(image, (x, y),
                                    (x + w, y + h), 
                                    (0, 0, 255), 2)
                    person = Person(time.time(), i)
                    producer.send(person)

                # Showing the output Image
                try:
                    cv2.imshow("Image", image)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                except:
                    print("Additional configs need to be done to run GUI within Docker container")
            else:
                break
        
        cap.release()
        cv2.destroyAllWindows()