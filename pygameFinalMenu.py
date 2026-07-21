import pygame
import sys
import os

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

from pygame_markdown import MarkdownRenderer

# GLOBAL VARIABLES

SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]

N_ROWS = 2
N_COLS = 3

NAVY = (10, 10, 100)
LIGHT = (40, 40, 200)
DARK = (20, 20, 100)
EMPTY = (0,0,0,0)
TAN = (236, 222, 201)
DARK_BROWN = (40, 27, 13)

SCREEN_SHOW_TIME = 800

HOVERING = 32



class InteractionGame(object):
    def __init__(self):
        # PYGAME INITIALIZATION INFO

        pygame.init()

        # Initializing screen information
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Start Menu Example")
        # Creating a data structure to store the information of images
        contents = os.listdir("images/")
        self._images = {}
        for i in range(0, N_COLS * N_ROWS):
            self._images[i] = pygame.image.load("images/" + contents[i]).convert_alpha()
        # Initializing kinect information
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body)

        # Initializing "global" variables that require pygame to be intitalized
        self.SCREEN_WIDTH = self._screen.get_width()
        self.SCREEN_HEIGHT = self._screen.get_height()
        self.ROW_HEIGHT = self.SCREEN_HEIGHT / N_ROWS
        self.COL_WIDTH = self.SCREEN_WIDTH / N_COLS
        self.HAND_TRACKER_SIZE = self.SCREEN_WIDTH / 64
        # clock is used to determine the framerate
        self._clock = pygame.time.Clock()
        self._done = False
        self._bodies = None
        self._hands = {}
        self._state = "main"
        self._count = 0
        self._score = [[0 for x in range(N_COLS)] for y in range(N_ROWS)]


        # SELF FRAME_SURFACE is the surface that contains the body information from the Kinect
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), pygame.SRCALPHA, 32)
        self._frame_surface = self._frame_surface.convert_alpha()

        # stores the conversion rate between kinect surface and screen surface
        self._kinect_to_frame_x =  self._kinect.color_frame_desc.Width / self.SCREEN_WIDTH
        self._kinect_to_frame_y = self._kinect.color_frame_desc.Height / self.SCREEN_HEIGHT

        # creates empty dicts, and populates them with the coordinates used to insert the images.
        # screen pos dict is for rendering the images, kinect pos dict is scaled up, to determine if kinect data colides with specific boxes
        self._screen_pos_dict = {}
        self._kinect_pos_dict = {}
        dict_count = 0
        for i in range (0, N_ROWS):
            for j in range (0, N_COLS):
                width_len = round((j + 1) * self.COL_WIDTH) - round(j * self.COL_WIDTH)
                height_len = round((i + 1) * self.ROW_HEIGHT) - round(i * self.ROW_HEIGHT)
                self._screen_pos_dict[dict_count] = pygame.Rect(round(j * self.COL_WIDTH), round(i * self.ROW_HEIGHT), width_len, height_len)
                self._kinect_pos_dict[dict_count] = pygame.Rect(round(self._kinect_to_frame_x * j * self.COL_WIDTH), round(self._kinect_to_frame_y * i * self.ROW_HEIGHT), round(self._kinect_to_frame_x * width_len), round(self._kinect_to_frame_y * height_len))
                dict_count = dict_count + 1
        #print(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        #print(self._screen_pos_dict)
        #print(self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height)
        #print(self._kinect_pos_dict)


    # detect_hand is used to convert kinect data into the x and y positions of a hand coordinate.
    def detect_hand(self, joints, jointPoints, joint):
        jointState = joints[joint].TrackingState

        if (jointState == PyKinectV2.TrackingState_NotTracked): 
            return

        final_x = jointPoints[joint].x
        final_y = jointPoints[joint].y
   
        
        return(final_x, final_y)


    # draw_hand is used to draw circles at the position of the hands
    def draw_hand(self, hand_coords, color):
        try:
            pygame.draw.circle(self._frame_surface, color, (hand_coords[0], hand_coords[1]), self.HAND_TRACKER_SIZE)
        except: # need to catch it due to possible invalid positions (with inf)
            pass
    
    # draw_hands calls draw_hand for every hand in the list of coordinates.
    def draw_hands(self, hands_list):
        for i, j in hands_list.items():
            #if(hands_list[i][0])
            self.draw_hand(j[0], SKELETON_COLORS[i])
            self.draw_hand(j[1], SKELETON_COLORS[i])

    # the code that renders the main menu, and handles interactions between the kinect data and the different images
    def start_menu(self):
        loop_num = 0 # This is a bad coding practice lol it exists because there are two ways to think about the images 
                     # present on this screen: as a x by y grid and as a linear x by 1 line.
        for i in range(0, N_ROWS):
            for j in range(0, N_COLS):
                if(self._images[loop_num].get_height() > self._images[loop_num].get_width()): # determine the shorter side of the image and evenly scale the contents so that side is the same as the box's size
                    scalar = self.COL_WIDTH / self._images[loop_num].get_width()
                else:
                    scalar = self.ROW_HEIGHT / self._images[loop_num].get_height()
                final_width = round(scalar * self._images[loop_num].get_width())
                final_height = round(scalar * self._images[loop_num].get_height())
                new_img = pygame.transform.smoothscale(self._images[loop_num], (final_width, final_height))
                for k, l in self._hands.items():
                    for m in l:
                        if(self._kinect_pos_dict[loop_num].collidepoint(m)): #if a hand overlaps with an image increase the score
                            self._score[i][j] +=1
                            new_img.fill((HOVERING, HOVERING, HOVERING), special_flags=pygame.BLEND_RGB_ADD)
                self._screen.blit(new_img, (self._screen_pos_dict[loop_num].left, self._screen_pos_dict[loop_num].top), (round((final_width - self.COL_WIDTH)/2), round((final_height - self.ROW_HEIGHT)/2), self._screen_pos_dict[loop_num].width, self._screen_pos_dict[loop_num].height))
                loop_num += 1

    # the code that renders each specific image page.
    def creature_page(self, page_num):
        self._screen.fill(NAVY)
        pygame.draw.rect(self._screen, TAN, pygame.Rect(self.SCREEN_WIDTH * 0.0125, self.SCREEN_HEIGHT * 0.0125, self.SCREEN_WIDTH * 0.975, self.SCREEN_HEIGHT * 0.975))
        
        # This code renders the page specific image and makes sure it won't go off the edge
        img_rect = self._images[page_num].get_rect()
        if img_rect.width < img_rect.height:
            scalar = (self.SCREEN_HEIGHT * 0.95) / img_rect.height
        else:
            scalar = (self.SCREEN_WIDTH * 0.45) / img_rect.width
        final_width = round(scalar * img_rect.width)
        final_height = round(scalar * img_rect.height)
        new_img = pygame.transform.smoothscale(self._images[page_num], (final_width, final_height))
        img_rect = new_img.get_rect()
        img_rect.center = (self.SCREEN_WIDTH * 0.25, self.SCREEN_HEIGHT * 0.5)
        self._screen.blit(new_img, img_rect)

        # This code renders the text box from a markdown file
        pygame_events = pygame.event.get()          # These do not matter but md.display requires them so I am forced to
        mouse_x, mouse_y = pygame.mouse.get_pos()   # grab them
        mouse_pressed = pygame.mouse.get_pressed()
        contents = os.listdir("text/")
        md = MarkdownRenderer()
        md.set_markdown(mdfile_path="text/" + contents[page_num])
        md.set_area(self._screen, self.SCREEN_WIDTH * 0.5125, self.SCREEN_HEIGHT * 0.05, self.SCREEN_WIDTH * 0.4625, self.SCREEN_HEIGHT * 0.9)
        md.set_font(font_text='Verdana', font_code='Helvetica')
        md.set_color_background(r=44, g=44, b=44)
        md.set_font_sizes(h1=32, h2=28, h3=24, text=20, code=20, quote=20)
        md.display(pygame_events, mouse_x, mouse_y, mouse_pressed)



    # Logic for the main screen of the game. 
    def interactive_screen(self):
        while not self._done:
            for event in pygame.event.get(): # This handles events: pressing the x on the game and pressing the q key
                if event.type == pygame.QUIT:
                    self._done = True
                    #sys.exit()  # NOT USED because when the game is closed using sys.exit it will not close the kinect connection
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self._done = True


            #mouse = pygame.mouse.get_pos()

            # This code handles pykinect and hand tracking
            self._frame_surface.fill(EMPTY)
            self._hands = {}

            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count): # NW: loop through all bodies that are visible and draw them on screen.
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self._hands[i] = (self.detect_hand(joints, joint_points, PyKinectV2.JointType_HandLeft), self.detect_hand(joints, joint_points, PyKinectV2.JointType_HandRight))
                    #self.draw_hand(joints, joint_points, SKELETON_COLORS[i], PyKinectV2.JointType_HandLeft)
                    #self.draw_hand(joints, joint_points, SKELETON_COLORS[i], PyKinectV2.JointType_HandRight)


            # This code handles self._state, which is what tracks the current state the software is in
            #print(self._screen_pos_dict)
            for i in range(N_ROWS):
                for j in range(N_COLS):
                    if self._score[i][j] > 250:
                        for k in range(N_ROWS):
                            for l in range(N_COLS):
                                self._score[k][l] = 0
                        self._state = "screen" + str(N_COLS * i + j)

                        contents = os.listdir("sounds/") #this code plays the sound effects when switching screens
                        pygame.mixer.music.load("sounds/" + contents[N_COLS * i + j])
                        pygame.mixer.music.play()
            if(self._count >= SCREEN_SHOW_TIME):
                self._state = "main"
                self._count = 0

            if (self._state == "main"):
                self.start_menu()
            for i in range(N_ROWS * N_COLS):
                if (self._state == "screen" + str(i)):
                    self._count += 1
                    self.creature_page(i)


            # this code deals with the rendering of hands, and adds them to the main screen.
            self.draw_hands(self._hands)
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), self._screen.get_height()))
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None

            # This code ensures the information renders updates

            pygame.display.update()

            pygame.display.flip()

            self._clock.tick(60)
            print(self._clock.get_fps())
        
        # This code runs when the game is quit
        self._kinect.close()
        pygame.quit()




# this code runs the game

__main__ = "Kinect v2 Body Game"
game = InteractionGame()
game.interactive_screen()
