import threading
import cv2

class VideoStream:

        def __init__(self,src = 0):

            self.stream = cv2.VideoCapture(src)
            self.stream.set(3,640)
            self.stream.set(4,480)
            self.grabbed, self.frame = self.stream.read()
            self.stopped = False

        def start(self):
            threading.Thread(target = self.update, args = (), daemon = True).start()
            return self

        def read(self):
            return self.grabbed, self.frame

        def update(self):
            while not self.stopped:
                if not self.grabbed:
                    self.stop()
                else:
                    self.grabbed, self.frame = self.stream.read()

        def stop(self):
            self.stopped = True
            self.stream.release()
        
