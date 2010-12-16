#!/usr/bin/env python

import pygame
import Image
from pygame.locals import *
import sys

import opencv
#this is important for capturing/displaying images
from opencv import highgui 

class MotionDetect:
    def __init__(self):
        #Change this to make image more/less motion-sensible
        self.sensitivity = 150
        #Change this to make motion detection more/less precise
        self.resolution = 20
        self.image_rgb_before = [[(0, 0, 0) for col in range(0, self.resolution)] for row in range(0, self.resolution)]
        self.image_rgb_now = [[(0, 0, 0) for col in range(0, self.resolution)] for row in range(0, self.resolution)]

    def detect(self, img):
        w = img.get_width()
        h = img.get_height()
        for i in range(0, self.resolution):
            for j in range(0, self.resolution):
                x = 10 + w / self.resolution * i
                y = 10 + h / self.resolution * j
                self.image_rgb_before[i][j] = self.image_rgb_now[i][j]
                self.image_rgb_now[i][j] = img.get_at((x, y))
                dif = [ abs(self.image_rgb_now[i][j][x] - self.image_rgb_before[i][j][x]) for x in range(0, 3)]
                sum_dif = dif[0] + dif[1] + dif[2]
                if sum_dif > self.sensitivity:
                    print "Achtung", "!" * (sum_dif/2)

def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im) 

if __name__ =="__main__":
    motiondetector = MotionDetect()

    camera = highgui.cvCreateCameraCapture(0)

    fps = 30.0
    pygame.init()
    window = pygame.display.set_mode((640,480))
    pygame.display.set_caption("WebCam Demo")
    screen = pygame.display.get_surface()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or event.type == KEYDOWN:
                sys.exit(0)
        im = get_image()
        pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
        screen.blit(pg_img, (0,0))
        motiondetector.detect(pg_img)
        pygame.display.flip()
        pygame.time.delay(int(1000 * 1.0/fps))
