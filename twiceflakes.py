'''
Screw it! Impromptu coding session right now
Make an script that rains down Twice members name
should be similar to the ASCII snowterm.py
'''
import random
import sys
import time
import curses

def max_dimensions(window):
    height, width = window.getmaxyx()#This is the only Sys function
    return height - 2, width -1

def twiceflake_char(window):
    width = max_dimensions(window)[1]
    members = ["Nayeon", "Jeongyeon", "Momo", "Sana", "Jihyo", "Mina",\
	"Dahyun", "Chaeyoung", "Tzuyu"]
    twice_member = random.choice(members)
    position = random.randrange(1, width)
    return (0, position, twice_member) #twice flake char returns (height=0, width, str) 

def update_twiceflakes(prev_flake, window):
    new = {}    #new should be empty dict
    for (height, position), twice_member in prev_flake.items(): #what does this do?
        max_height = max_dimensions(window)[0]
        new_height = height + 1
        if new_height > max_height or prev_flake.get((new_height, position)):
            new_height -= 1
        new[(new_height, position)] = twice_member
    return new

def redisplay(twiceflakes, window):
    for (height, position), twiceMember in twiceflakes.items():
        max_height, max_width = max_dimensions(window)
        if height > max_height or position >= max_width:
            continue
        window.addstr(height, position, twiceMember)    #adds the string onto the screen

def draw_moon(window):
    moon = [
        '********* *       *       *  *  *********  *********   ',
        '    *      *     * *     *   *  *          *           ',
        '    *       *   *   *   *    *  *          *********   ',
        '    *        * *     * *     *  *          *           ',
        '    *         *       *      *  ********** *********   ',
    ]
    start_position = max_dimensions(window)[1] - 55
    window.attrset(curses.color_pair(1))
    for height, line in enumerate(moon, start=1):
        for position, sym in enumerate(line, start=start_position):
            if sym.strip():
                window.addstr(height, position, sym)
    window.attrset(curses.color_pair(0))


def main(window, speed):
    if curses.can_change_color():
        curses.init_color(curses.COLOR_BLACK, 0,0,0)
        curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
        curses.init_color(curses.COLOR_YELLOW, 1000, 1000, 0)
    curses.init_pair(1, curses.COLOR_YELLOW, 0)
    try:
        curses.curs_set(0)
    except Exception:
        pass  # Can't hide cursor in 2019 huh?
    window.border()
    twice_flakes = {}    #twiceflakes is an empty dict right?
    while True:
        height, width = max_dimensions(window)
        if len(twice_flakes.keys()) >= 0.95 * (height * width):  #What does this part do? Wait isn't this part clearing everything
            print(twice_flakes.key())
            twice_flakes.clear()                                 #Nope it still doesn't work. It still clears the screen
        twice_flakes = update_twiceflakes(twice_flakes, window)   #Maybe it's something to do with clearing the screen
        twiceflake = twiceflake_char(window)
        print(twiceflake)
        twice_flakes[(twiceflake[0], twiceflake[1])] = twiceflake[2] #What does this part of the code do? Why is twiceflake member str name assigned?
        window.clear()
        draw_moon(window)
        redisplay(twice_flakes, window)
        window.refresh()
        try:
            time.sleep((0.2) / (speed / 100))
        except ZeroDivisionError:
            time.sleep(0.2)


if __name__ == '__main__':
    speed = 100
    if len(sys.argv) > 1:
        try:
            speed = int(sys.argv[1])
        except ValueError:
            print(
                'Usage:\npython snowterm.py [SPEED]\n'
                'SPEED is integer representing percents.',
            )
            sys.exit(1)
    try:
        curses.wrapper(main, speed)
    except KeyboardInterrupt:
        sys.exit(0)