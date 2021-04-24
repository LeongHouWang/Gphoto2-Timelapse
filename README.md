#DSLR Timelapse

This is a project that utilizes Gphoto2 installed in a raspberry pi model B 3+ to control my old DSLR (Canon 550D) to take timelapse photos.

The project is written in Python

The intention is to store the photos into a local/network drive to avoid damaging the SD card.

Gphoto2 and libgphoto2 is pre-requisite. Python for gphoto2 is also needed.

These are the websites I followed:

https://pimylifeup.com/raspberry-pi-dslr-camera-control/
https://maskaravivek.medium.com/how-to-control-and-capture-images-from-dslr-using-raspberry-pi-fdfa9d600ec1

2021.04.20 Somehow killing running application on the gphoto2 is required before commanding to capture image. Use "pkill -f gphoto2" before using gphoto2

2021.04.24 Successfully run an 11-hours Timelapase photo shooting. Commented the code to remove all the photo in the folder before starting. Instead it will increment the photo name from the previous shooting.
