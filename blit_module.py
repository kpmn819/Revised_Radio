#!/usr/bin/python3
# adds blitRotate
# blit_em accepts angle and all blit surfaces
import pygame, os
from pygame.locals import *
import pygame.font




pygame.init()
# some classes for background and sprites are shown here
# but are not used in the program
class Background(pygame.sprite.Sprite):
    def __init__(self,image_file,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

#BackGround = Background(radio, [0,0])

class OverlaySprites(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect  = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
#needle_sp = OverlaySprites('Needle.png',0,[400,200])

def blitRotate(surf, image, pos, originPos, angle):
    # and to call the whole shebang this is all you need
    # pos is a tuple (x,y)
    '''blitRotate(display, image, pos, (w/2, h), angle)'''

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    #pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)

def blit_em(radio,needle,mask,eye_now,angle):
    display.blit(radio,(0,0))
    # throws everything on the screen
    #display.blit(needle, (414,190))
    # some weirdness with rotate y is inverted and - angle is cw + angle ccw
    w, h = needle.get_size()
    blitRotate(display, needle, (425,461), (w/2, h),angle)
    display.blit(mask, (239,411))
    display.blit(eye_now, (371, 26))
    pygame.display.flip()  


def font_process(size, message, color, x, y):
    ''' combines everthing needed to blit fonts to the screeen,
    called from various methods that use fonts'''
    # attempt to combine all font operations into one call that
    # renders and blits the text
    
    black = (0,0,0)
    d_shadow = 3
    # create a font object from a system font
    font = pygame.font.SysFont('FreeSans', size, True, False)
    # render font on a new surface font.render(text, antialias, bkgnd = none)
    render_message = font.render(message, True, color)
    # render drop shadow in black
    if d_shadow:
        render_ds = font.render(message, True, black)
        render_ds_rect = render_message.get_rect()
    # attempt to center works
    # create a rectangular object for the text surface object
    render_msg_rect = render_message.get_rect()
    
    # center in x, use y from call
    #render_msg_rect.center = (image_centerx, y) # (x,y) x = screen center
    render_msg_rect.center = (x, y) # (x,y) x = screen center
    # blit drop shadow then text to image
    if d_shadow:
        #render_ds_rect.center = (image_centerx + d_shadow, y + d_shadow)
        render_ds_rect.center = (x + d_shadow, y + d_shadow)
        display.blit(render_ds, render_ds_rect)
    display.blit(render_message, render_msg_rect)
    pygame.display.flip()  
#============VARIABLES==============
os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
screen_width=841
screen_height=640
bgColor = (255, 255, 255)
size=(screen_width, screen_height)
display = pygame.display.set_mode(size)
progress = True
pygame.display.set_caption('Internet Radio')


