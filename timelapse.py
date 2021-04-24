import logging
import os
from os import system
import datetime
from time import sleep
import subprocess
import sys

import gphoto2 as gp

tlminutes = 420 #set this to the number of minutes you wish to run your timelapse camera
seconds_interval = 120 #number of seconds delay between each photo taken
# fps = 30 #frames per second timelapse video
numphotos = int((tlminutes*60)/seconds_interval) #number of photos to take
print("number of photos to take = ", numphotos)

def capture_image_from_dslr():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    #callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.Camera()
    camera.init()
    print('Capturing image')
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    target = os.path.join('/home/pi/Pictures', file_path.name)
    print('Copying image to', target)
    camera_file = camera.file_get(
        file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    #subprocess.call(['xdg-open', target])
    camera.exit()
    return 0

def get_target():
    # use Python logging
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    #callback_obj = gp.check_result(gp.use_python_logging())
    # open camera connection
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    # get configuration tree
    config = gp.check_result(gp.gp_camera_get_config(camera))
    # find the capture target config item
    capture_target = gp.check_result(
        gp.gp_widget_get_child_by_name(config, 'capturetarget'))
    # print current setting
    value = gp.check_result(gp.gp_widget_get_value(capture_target))
    print('Current setting:', value)
    # print possible settings
    for n in range(gp.check_result(gp.gp_widget_count_choices(capture_target))):
        choice = gp.check_result(gp.gp_widget_get_choice(capture_target, n))
        print('Choice:', n, choice)
    # clean up
    gp.check_result(gp.gp_camera_exit(camera))
    return 0

def set_target():
    # use Python logging
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    #callback_obj = gp.check_result(gp.use_python_logging())
    # get user value
    if len(sys.argv) != 2:
        print('One command line parameter required')
        return 1
    try:
        value = int(sys.argv[1])
    except:
        print('Integer parameter required')
        return 1
    # open camera connection
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    # get configuration tree
    config = gp.check_result(gp.gp_camera_get_config(camera))
    # find the capture target config item
    capture_target = gp.check_result(
        gp.gp_widget_get_child_by_name(config, 'capturetarget'))
    # check value in range
    count = gp.check_result(gp.gp_widget_count_choices(capture_target))
    if value < 0 or value >= count:
        print('Parameter out of range')
        return 1
    # set value
    value = gp.check_result(gp.gp_widget_get_choice(capture_target, value))
    gp.check_result(gp.gp_widget_set_value(capture_target, value))
    # set config
    gp.check_result(gp.gp_camera_set_config(camera, config))
    # clean up
    gp.check_result(gp.gp_camera_exit(camera))
    return 0



    
# def make_video():
#     dateraw = datetime.datetime.now()
#     datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
#     print("Please standby as your timelapse video is created.")    
#     system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/Pictures/TimeLapse/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/pi/Videos/{}.mp4'.format(fps, datetimeformat))
#     #system('rm /home/pi/Pictures/*.jpg')
#     print('Timelapse video is complete. Video saved as /home/pi/Videos/{}.mp4'.format(datetimeformat))

# def make_video2():
#     OUT_FILE = 'time_lapse.mp4'
#     WORK_DIR = '/home/pi/Pictures/TimeLapse'
#     template = os.path.join(WORK_DIR, 'frame%04d.jpg')
#     subprocess.check_call(['ffmpeg', '-r', '25',
#                            '-i', template, '-c:v', 'h264', OUT_FILE])

def count_image():
    # for root, dirs, files in os.walk('/home/pi/Pictures/TimeLapse'):
    #     # for subdir in dirs:
    #     #     dirpath = os.path.join(root,subdir)
    #     #     print(dirpath)
    #     print(files)
    path, dirs, files = next(os.walk('/home/pi/Pictures/TimeLapse'))
    print(len(files))

def time_lapse():
    dateraw = datetime.datetime.now()
    datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
    print("RPi started taking photos for your timelapse at: " + datetimeformat)
    
    path, dirs, files = next(os.walk('/home/pi/Pictures/TimeLapse'))
    previous_photo_count = len(files)

    #Initializing camera
    camera = gp.Camera()
    camera.init()

    #system('rm /home/pi/Pictures/TimeLapse/*.jpg') #delete all photos in the Pictures folder before timelapse start

    for i in range(numphotos):
        print('Capturing image')
        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        #target = os.path.join('/home/pi/Pictures/TimeLapse', 'frame%04d.jpg')
        target=('/home/pi/Pictures/TimeLapse/frame{0:04d}.jpg'.format((i+previous_photo_count)))
        print('Copying image to', target)
        camera_file = camera.file_get(
        file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        #camera_file.save(target % i)
        camera_file.save(target)
        sleep(seconds_interval)
    print("Done taking photos.")
    # print("Please standby as your timelapse video is created.")
  
if __name__ == "__main__":
    system('pkill -f gphoto2') #clear any running application linking to the Gphoto2 program before running this python script
    sleep(1) #delay for one second
    #sys.exit(capture_image_from_dslr())
    #sys.exit(get_target())
    #sys.exit(set_target())
    sys.exit(time_lapse())
    #sys.exit(count_image())
    
