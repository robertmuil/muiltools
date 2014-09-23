'''
Created on Aug 9, 2013


'''
import sys

# Be safe and define a maximum of frames we're trying to walk up
MAX_FRAMES = 20

def save_to_interactive(dct):
    """
    Will save the variables given in dct to the interactive namespace
    if called, for example, from within a debugging session.
    
    http://stackoverflow.com/a/18125590/480534

    @author: Lukas Graf (http://stackoverflow.com/users/1599111/lukas-graf)
    """
    n = 0
    # Walk up the stack looking for '__name__'
    # with a value of '__main__' in frame globals
    for n in range(MAX_FRAMES):
        cur_frame = sys._getframe(n)
        name = cur_frame.f_globals.get('__name__')
        if name == '__main__':
            # Yay - we're in the stack frame of the interactive interpreter!
            # So we update its frame globals with the dict containing our data
            cur_frame.f_globals.update(dct)
            break

if __name__ == '__main__':
    pass