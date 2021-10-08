import pygame

class Animation():
    
    def __init__(self, frames):
        ## list of frames for the animation
        self.frames = frames
        ## index for which frame we are on
        self.index = 0

    def drawFirstFrame(self, screen, x, y, reverse):
        if reverse:
            screen.blit(pygame.transform.flip(self.frames[0], True, False), (x, y))
        else:
            screen.blit(self.frames[0], (x, y))
            
    ## draws 1 frame each call, if animation is finished, resets index and returns true, else returns false
    def draw(self, screen, x, y, reverse):
        if reverse:
            screen.blit(pygame.transform.flip(self.frames[self.index], True, False), (x, y))
        else:
            screen.blit(self.frames[self.index], (x, y))
        self.index+=1
        if self.index == len(self.frames):
            self.index = 0
            return True
        else:
            return False