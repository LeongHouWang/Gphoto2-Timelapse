#DSLR Timelapse

This is a project that utilizes Gphoto2 installed in a raspberry pi model B 3+ to control my old DSLR (Canon 550D) to take timelapse photos.

The project is written in Python

The intention is to store the photos into a local/network drive to avoid damaging the SD card. The commented code in main which runs set_target can be used to set to store the image in the camera's SD card, but since I used WinSCP to download the photos, I set the target to raspberryPi.

Gphoto2 and libgphoto2 are pre-requisite. gphoto2 for python is also needed.

These are the websites I followed and referred:

https://pimylifeup.com/raspberry-pi-dslr-camera-control/
https://maskaravivek.medium.com/how-to-control-and-capture-images-from-dslr-using-raspberry-pi-fdfa9d600ec1
https://github.com/carolinedunn/timelapse

2021.04.20 Somehow killing running application on the gphoto2 is required before commanding the camera to capture image. Use "pkill -f gphoto2" before using gphoto2. Add a line to run this command in Python during intialization.

2021.04.24 Successfully ran an 11-hours Timelapase photo shooting. Commented the code to remove all the photo in the folder before starting. Instead it will increment the photo name from the previous shooting(it uses a simple counter to count how many photos are already in the folder and then add this number during naming the newly taken photo).
