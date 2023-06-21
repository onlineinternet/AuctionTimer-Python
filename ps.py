#!/usr/bin/python3
import time, os, sys, tty, termios
import simpleaudio as sa
from select import select

# Function to read a single character from stdin without waiting for the Enter key
def getKey():
    if select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)

# Function to load bid, tick-tock, and sold sounds into WaveObjects
def load_sounds():
    bids = [sa.WaveObject.from_wave_file(f'assets/bid{str(i).zfill(3)}.wav') for i in range(1, 31)]
    tick_tock_sounds = [sa.WaveObject.from_wave_file(f'assets/{name}.wav') for name in ['tick', 'tock']]
    sold_sound = sa.WaveObject.from_wave_file("assets/sold.wav")
    return bids, tick_tock_sounds, sold_sound

# Function to set the terminal to non-blocking mode and save the current terminal settings
def set_terminal_mode():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    return old_settings

# Function to restore the original terminal settings
def restore_terminal_mode(old_settings):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def main():
    old_terminal_settings = set_terminal_mode()
    bids, tick_tock_sounds, sold_sound = load_sounds()
    total_bids = 30

    bid = 0
    tick_tock_index = 0
    bid_timer = 0.0
    last_timestamp = time.time()
    done = False

    try:
        # Main event loop
        while not done:
            # Calculate elapsed time since the last iteration
            elapsed = time.time() - last_timestamp
            last_timestamp = time.time()

            # Get the user's input
            key = getKey()

            # Process user input
            if key == 'b':
                # If a tick or tock sound is playing, reset tick_tock_index
                if tick_tock_index > 0:
                    tick_tock_index = 0

                # Increment the bid count and play the corresponding bid sound
                bid = (bid + 1) % total_bids
                bids[bid].play()

            # Exit the loop if the user presses 'q'
            elif key == 'q':
                done = True

            # Update the bid timer and play tick-tock sounds
            if bid:
                bid_timer += elapsed
                if bid_timer >= 1.1:
                    if tick_tock_index < len(tick_tock_sounds):
                        tick_tock_sounds[tick_tock_index].play()
                        tick_tock_index += 1
                    else:
                        # Play the "sold" sound and reset bid and tick_tock_index
                        sold_sound.play()
                        bid = 0
                        tick_tock_index = 0

                    # Reset the bid timer
                    bid_timer = 0.0
    finally:
        # Restore the original terminal settings upon exiting the loop
        restore_terminal_mode(old_terminal_settings)

if __name__ == "__main__":
    main()
