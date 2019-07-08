import os
import RPi.GPIO as GPIO
import time

num_port = 17           # numero du port sur lequel est le bouton
num_port_led = 14       # numero de port de la LED
temps = 60              # temps d'enregistrement en secondes
chemin = "/media/usb1/" # repertoire de stockage des fichiers sons
fichier = "confess"     # nom du fichier


def checkFilePath(testString, extension, currentCount):
    if os.path.exists(testString + str(currentCount).zfill(4) + extension):
        return checkFilePath(testString, extension, currentCount+1)
    else:
        return testString + str(currentCount).zfill(4) + extension




GPIO.setmode(GPIO.BCM)


# intialiser les GPIO
GPIO.setup(num_port,GPIO.IN)
GPIO.setup(num_port_led, GPIO.OUT, initial=GPIO.LOW)
input = GPIO.input(num_port)

prev_input = 0

# Boucle infinie
while True:
    # Lire l'entree du bouton
    input = GPIO.input(num_port)

    # Tester si on appuie sur le bouton
    if ((not prev_input) and input):
        # Allumer la diode
        GPIO.output(num_port_led,GPIO.HIGH)

        # Determiner le nom compket du fichier
        nomFichier = checkFilePath( chemin + fichier, '.wav', 0)

        # Lancer la commande d'enregistrement
        os.system('arecord -d '+str(temps)+' -D hw:AK5371,0 -f S16_LE -c2 -r48000 '+nomFichier)

        # Une fois que l'enregistrement  est termine, eteindre la diode
        time.sleep( temps )
        GPIO.output(num_port_led,GPIO.LOW)

    # recopie de l'entree precedente
    prev_input = input
    # effectuer une pause pour eviter l'effet rebond
    time.sleep(0.05)
