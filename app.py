import time
import keyboard

from data import secret_datas
from additionals import totp_text_to_dict

LONG_PRESS_DURATION = 0.4  # Specify the duration in seconds for a long press
PRESS_INTERVAL = 0.3 # Specify the interval between key presses

#logging to console
import logging as log
log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# save button char '#'
# clear button char '-'
# underscore char ' '
keyboard_layout = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '0', '1', '2', '3'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '-', '4', '5', '6'],
    ['+', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', '#', '7', '8', '9'],
]

def find_index_of_character(character):
    try:
        for row_index, row in enumerate(keyboard_layout):
            for column_index, column in enumerate(row):
                if column == character.lower():
                    return (row_index, column_index)
        log.info(f"Character not found {character}")
        return (2, 7) # force return ' ' char position
    except Exception as e:
        log.error(e)
        # return ' ' char position 
        return (2, 7)
    
def navigate_to_character(character):
    character_index = find_index_of_character(character)
    return character_index


def move_left():
    log.debug("Moving left")
    keyboard.press_and_release('left')
    time.sleep(PRESS_INTERVAL)

def move_right():
    log.debug("Moving right")
    keyboard.press_and_release('right')
    time.sleep(PRESS_INTERVAL)

def move_up():
    log.debug("Moving up")
    keyboard.press_and_release('up')    
    time.sleep(PRESS_INTERVAL)

def move_down():
    log.debug("Moving down")
    keyboard.press_and_release('down')  
    time.sleep(PRESS_INTERVAL)
    
def zeroing_position(position):
    for i in range(position[1]):
        move_left()
    for i in range(position[0]):
        move_up()
    
def move_postition(position):
    for i in range(position[0]):
        move_down()
    for i in range(position[1]):
        move_right()

def press_enter(is_longer=False):
    if is_longer:
        log.debug("Pressing enter for uppercase")
        keyboard.press('enter')
        time.sleep(LONG_PRESS_DURATION)
        keyboard.release('enter')
    else:
        log.debug("Pressing enter for lowercase")
        keyboard.press_and_release('enter')
    time.sleep(PRESS_INTERVAL)


def move_between_two_character(char_1, char_2):
    char_1_index = find_index_of_character(char_1)
    char_2_index = find_index_of_character(char_2)
    log.info(f"char_1_index : {char_1_index} {char_1}")
    log.info(f"char_2_index : {char_2_index} {char_2}")
    
    if char_1_index[1] > 5:
        for i in range(char_1_index[1] - 6):
            move_left()
        char_1_index = (char_1_index[0], 6)
        log.debug(f"char_1_index : {char_1_index} {char_1}")
    
    if char_1_index[0] > char_2_index[0]:
        for i in range(char_1_index[0] - char_2_index[0]):
            move_up()
    else:
        for i in range(char_2_index[0] - char_1_index[0]):
            move_down()

    if char_1_index[1] > char_2_index[1]:
        for i in range(char_1_index[1] - char_2_index[1]):
            move_left()
    else:
        for i in range(char_2_index[1] - char_1_index[1]):
            move_right()
            

def press_multiple(count=3, symbol='enter'):
    for i in range(count):
        log.debug(f"Pressing {i}: {symbol}")
        keyboard.press_and_release(symbol)
        time.sleep(PRESS_INTERVAL)


def emulate_word(word):
    is_first_press = True
    start_symbol = '#' # first symbol is save button default

    for character in word:
        log.debug(f"Current character {character}")
        log.debug(f"Current start_symbol {start_symbol}")

        move_between_two_character(start_symbol, character)

        if character.islower() and is_first_press:
            press_enter(True)
        elif character.isupper() and not is_first_press:
            press_enter(True)
        else:
            press_enter()

        if is_first_press:
            is_first_press = False

        start_symbol = character.lower()

    move_between_two_character(start_symbol, "#") #move save button
    press_enter() #click save button

    

def google_authenticator():
    # use txt output https://github.com/krissrex/google-authenticator-exporter
    str_array = totp_text_to_dict()#load secrets
    
    for keywords in str_array:
        log.debug(keywords[0:2])
        # enter to add new totp screenand enter to new token field and enter to name field
        press_multiple(3, 'enter')
        
        emulate_word(keywords[0]) # emulate name
        #move to secret field
        move_down()
        press_enter()
        
        emulate_word(keywords[1]) # emulate secret

    #click to confirm button
    press_multiple(5, 'down')
    press_enter()


def save_single_secret(title, secret):
    # enter to add new totp screenand enter to new token field and enter to name field
    press_multiple(3, 'enter')
    
    emulate_word(title) # emulate name
    #move to secret field
    move_down()
    press_enter()
    
    emulate_word(secret) # emulate secret

    #click to confirm button
    press_multiple(5, 'down')
    press_enter()


def main():
    # Wait for 3 seconds to give time to switch to the flipper APP
    time.sleep(3)

    # Start the process
    # google_authenticator()
    # save_single_secret("example", "SECRETSECRET")


if __name__ == "__main__":
    main()
