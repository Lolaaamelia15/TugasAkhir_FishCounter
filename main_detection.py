# Import module 
from MyLibrary.connection import Connection
from MyLibrary.detection import Detections
from MyLibrary.servo import Servo
from MyLibrary.buzzer import Buzzer
from MyLibrary.lcd import LCD
from time import sleep
import cProfile 

detection = Detections(model='ssd_mobilenet_v2_fpnlite_metadata2.tflite', cameraId=0)
servo = Servo(pin=13)
buzzer = Buzzer(pin=17)
lcd = LCD()

while(True):
    try:
        if Connection.internetReady():
            success, response_json = Connection.getData("http://147.139.170.233:8080/status.php")
            
            if not success:
                continue

            hitung_status = response_json['hitung']
            
            if hitung_status == 'true':
                jumlah_value = int(response_json['jumlah'])
                harga_value = int(response_json['harga'])
                
                jumlah_ikan = 0

                if not detection.cameraReady():
                    print("re-initialize camera")
                    detection.initialize()
                    sleep(1)

                percobaanPertama = True

                while (jumlah_ikan < jumlah_value):
                    servo.close()             # Matikan servo
                    if(percobaanPertama):
                        sleep(5)
                        percobaanPertama = False
                    else :
                        sleep(15)
                    
                    jumlah_ikan += detection.count(interval=25, total_terdetect=jumlah_ikan) # call hitung
                    lcd.jumlah(jumlah_ikan)
                    print("Total ikan yang terdeteksi : {}".format(jumlah_ikan))
                    servo.open()                # Hidupkan servo
                    sleep(5) # waktu untuk mengeluarkan ikan
                
                detection.clearCamera()
                servo.close()
                print("Total ikan yang terdeteksi : {}".format(jumlah_ikan))
                buzzer.turn_on_buzzer()
                lcd.tampil(jumlah_value=jumlah_value,harga_satuan=harga_value)
# 
                Connection.resetData("http://147.139.170.233:8080/transaksi.php")

    except KeyboardInterrupt:
        # servo.stop()
        # buzzer.stop()
        break 

    finally:
        sleep(5)
