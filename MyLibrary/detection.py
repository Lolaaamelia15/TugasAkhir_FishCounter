import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

class Detections(object):
    def __init__(self, model: str, cameraId: int = 0) -> None:
        self.__model = model
        self.__cameraId = cameraId
        # self.__cameraId = "video1.mp4"
        self.__cameraId = 0
        self.__width = 640
        self.__height = 480
        self.__num_threads = 4
        self.__enable_edgetpu = False

        # Initialize the object detection model
        self.__base_options = core.BaseOptions(
        file_name=self.__model, use_coral=self.__enable_edgetpu, num_threads=self.__num_threads)
        self.__detection_options = processor.DetectionOptions(
        max_results=100, score_threshold=0.3)
        self.__options = vision.ObjectDetectorOptions(
            base_options=self.__base_options, detection_options=self.__detection_options)
        self.__detector = vision.ObjectDetector.create_from_options(self.__options)

        # Initialize First
        self.initialize()
    
    def initialize(self):
        # Start capturing video input from the camera
        self.__cap = cv2.VideoCapture(self.__cameraId)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.__width)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__height)

    def cameraReady(self) -> bool:
        return self.__cap.isOpened()

    def count(self, interval, total_terdetect, showPreview = True):
        # Continuously capture images from the camera and run inference
        
        # Variables to calculate FPS
        counter, fps = 0, 0
        start_time = round(time.time())

        # Visualization parameters
        row_size = 20  # pixels
        left_margin = 24  # pixels
        text_color = (0, 0, 255)  # red
        font_size = 1
        font_thickness = 1
        fps_avg_frame_count = 10

        last_camera_open_time = round(time.time())
        Maxjumlah = 0
        while True:
            current_time = round(time.time())
            #Reopen the camera every 30 seconds
            diff = current_time - last_camera_open_time
            print("Waktu : {}".format(diff))
            
            if diff > interval:
                if 'self.__cap' in locals():
                    self.__cap.release()
                break

                # cap = cv2.VideoCapture(0)
                # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                # cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

            success, image = self.__cap.read()
            if not success:
                sys.exit(
                    'ERROR: Unable to read from webcam. Please verify your webcam settings.'
                )

            counter += 1
            image = cv2.flip(image, 1)

            # Convert the image from BGR to RGB as required by the TFLite model.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Create a TensorImage object from the RGB image.
            input_tensor = vision.TensorImage.create_from_array(rgb_image)

            # Run object detection estimation using the model.
            detection_result = self.__detector.detect(input_tensor)
            jumlahIkan = len(detection_result.detections)
            if jumlahIkan > Maxjumlah:
                Maxjumlah = jumlahIkan

            # Calculate the FPS
            if counter % fps_avg_frame_count == 0:
                end_time = time.time()
                fps = fps_avg_frame_count / (end_time - start_time)
                start_time = time.time()

            # Show the FPS
            fps_text = 'FPS = {:.1f}'.format(fps)

            if showPreview:
                # Draw keypoints and edges on input image
                image = utils.visualize(image, detection_result)

                text_location = (left_margin, row_size)
                cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                            font_size, text_color, font_thickness)
                
                # Show the number of detected fish
                jumlahIkan_text = 'Jumlah Ikan = {}'.format(jumlahIkan)
                jumlahIkan_location = (left_margin, row_size * 2)
                cv2.putText(image, jumlahIkan_text, jumlahIkan_location, cv2.FONT_HERSHEY_PLAIN,
                            font_size, text_color, font_thickness)
                
                totalIkan_text = 'Total Ikan = {}'.format(total_terdetect)
                totalIkan_location = (left_margin, row_size * 3)
                cv2.putText(image, totalIkan_text, totalIkan_location, cv2.FONT_HERSHEY_PLAIN,
                            font_size, text_color, font_thickness)
                cv2.imshow('object_detector', image)
            else:
                print(fps_text)

            # Stop the program if the ESC key is pressed.
            if cv2.waitKey(1) == 27:
                break
        
        print("Jumlah ikan yang terdeteksi: {}".format(Maxjumlah))
        cv2.destroyAllWindows()
        return Maxjumlah

    def clearCamera(self):
        self.__cap.release()
        cv2.destroyAllWindows()