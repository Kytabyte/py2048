import curses

import py2048


def incurses(screen, game):
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    try:
        while not game.isover:
            screen.addstr(0, 0, repr(game))
            ch = screen.getch()
            if ch == curses.KEY_RIGHT:
                game.moveright()
            elif ch == curses.KEY_LEFT:
                game.moveleft()
            elif ch == curses.KEY_UP:
                game.moveup()
            elif ch == curses.KEY_DOWN:
                game.movedown()
            elif ch == ord('r'):
                game.reset()
            elif ch == ord('q'):
                break
    finally:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()


def terminal_run(size):
    game = py2048.Game(size)
    while True:
        curses.wrapper(incurses, game)
        if not game.isover:
            break

        print(game)
        while True:
            print("Press 'q' to quit\n"
                  "Press 'r' to start a new game")
            ch = input()
            if ch == 'r':
                game.reset()
                break
            elif ch == 'q':
                return
