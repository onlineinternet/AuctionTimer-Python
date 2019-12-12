#!/usr/bin/python3
import time,os,sys,glob,tty,termios

import simpleaudio as sa
from select import select
from itertools import count
from evdev import InputDevice, categorize, ecodes

#gamepad = InputDevice('/dev/input/eventX') # modify this for your controller
#inputs = [gamepad]
#aBtn = 304 #A button mapped to G keyboard

aBtn = ecodes.KEY_B

total_bids = 30 # we use this number more than once, so name it

def getInput():
    if select(inputs, [], []) == (inputs, [] ,[]):
        print("before read_one")
        event = gamepad.read_one()
        print("after read_one")
        if event.type == ecodes.EV_KEY and event.value > 0:
            return event.code
    return None
#end getInput

def getKey():
    if select([sys.stdin], [], [], 0) == ([sys.stdin], [] ,[]):
        return sys.stdin.read(1) # return a single byte (usually a valid ASCII character) from stdin

try:
    # state variables for our script
    done = False
    bid = 0
    ticktock = 0
    timestamp = time.time()
    bidtimer = 0.0
    elapsed = 0
    
    # terminal munging
    old_settings = termios.tcgetattr(sys.stdin)                  # terminal munging - save terminal settings they way we found them
    tty.setcbreak(sys.stdin.fileno())

    ticks = [sa.WaveObject.from_wave_file(f'assets/%s.wav'%i) for i in ['tick','tock', 'tick', 'sold']]
    #ticks.append(False) # end list with our stopper
    soldwav = sa.WaveObject.from_wave_file('assets/sold.wav')
    bids = [sa.WaveObject.from_wave_file(f'assets/bid%.3i.wav'%i) for i in range(1,total_bids)]

    #sa.WaveObject.from_wave_file('assets/start.wav').play()

    # main program 'event' loop
    while done == False:
        elapsed = time.time() - timestamp;
        timestamp = time.time()
        #key = getInput()                        # fetch an input value
        key = getKey()                          # fetch an input value
        if key == 'b': #aBtn:
            bid = bid + 1
            ticktock = 0
            bids[bid].play()
        elif key == 'q':
            break
        # end if-key-is-abtn
        
        #print("bid: ",bid,", elapsed: ", elapsed, "ticktock: ",ticktock)
        if bid:
            bidtimer = bidtimer + elapsed
            if bidtimer >= 1.1: # the .3 adds some 'jitter'
                if ticktock < len(ticks):
                    ticks[ticktock].play()
                    ticktock = ticktock + 1
                else:
                    bid = 0
                bidtimer = 0.0
            # end if-bid-timer-gt-1.0

            if bid == total_bids:
                bid = 0
                bidtimer = 0.0
                ticktock = 0
            # end if-bid-is-30
        
        # end if-bid

    #end while-not-done
finally:
    print()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings) # undo terminal munging: restore original console settings

