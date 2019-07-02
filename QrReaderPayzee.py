# import the necessary packages
from imutils.video import VideoStream
from picamera import PiCamera
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import requests
import subprocess

def runcommand (cmd):
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    return proc.returncode, std_out, std_err

reciver = '5d1af4894f62310027c964f7'
url = 'http://192.168.43.86:3333/transactions/transaction/'


#imports raspberry hardware
pinoVerde = 18
buzzer = 23
pinoVermelho = 24

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pinoVerde,GPIO.OUT)
GPIO.setup(pinoVermelho,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

#Variavel pra n deixar que o mesmo qrcode seja lido em varios segundos
qrCodeLido = 0

#Funcoes de controle dos componentes	
def piscaSucesso():
	GPIO.output(pinoVermelho,GPIO.LOW) #apago vermelho
	GPIO.output(pinoVerde,GPIO.HIGH) #acendo verde
	GPIO.output(buzzer,GPIO.HIGH) #apito
	time.sleep(1)
	GPIO.output(buzzer,GPIO.LOW) #desapito
	GPIO.output(pinoVerde,GPIO.LOW) #apago verde
	GPIO.output(pinoVermelho,GPIO.HIGH) #acendo vermelho

def piscaFracasso():
	GPIO.output(pinoVermelho,GPIO.LOW) #apago vermelho
	GPIO.output(buzzer,GPIO.HIGH) #apito
	time.sleep(1)
	GPIO.output(pinoVermelho,GPIO.HIGH) #acendo vermelho
	time.sleep(1)
	GPIO.output(pinoVermelho,GPIO.LOW) #apago vermelho
	time.sleep(1)
	GPIO.output(pinoVermelho,GPIO.HIGH) #acendo vermelho
	GPIO.output(buzzer,GPIO.LOW) #apito

def apago():
	GPIO.output(pinoVermelho,GPIO.LOW) #apago vermelho

def acendo():
	GPIO.output(pinoVermelho,GPIO.HIGH) #acendo vermelho


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# init da camera
print("[RASPBERRY] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
csv = open(args["output"], "w")
found = set()
GPIO.output(pinoVermelho,GPIO.HIGH)
# loop over the frames from the video stream
while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)
		# loop over the detected barcodes
	for barcode in barcodes:
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
		print(barcodeData)
		if(qrCodeLido != barcodeData):
			qrCodeLido = barcodeData.replace('http://', '')
			url = url + qrCodeLido + '/' + reciver
			print('Fazendo o post para ' + url)
			apago()
			returncode = requests.post(url,json={'type':'checkout'})
			acendo()
			print(returncode)
			if(returncode == 'Response [201]'):
				piscaSucesso()
				print('Sucesso!')
			else:
				piscaFracasso()
				print('Fracasso!')

		if barcodeData not in found:
			csv.write("{},{}\n".format(datetime.datetime.now(),
				barcodeData))
			csv.flush()
			found.add(barcodeData)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# close the output CSV file do a bit of cleanup
print("[RASPBERRY] Encerrando servico")
csv.close()
cv2.destroyAllWindows()
vs.stop()
