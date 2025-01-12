import curses
import json
from client import Client

WIDTH = 100
HEIGHT = 38

class Page:
    def __init__(self, size, position, title, elements):
        self.selected_id = 0
        self.elements = []
        
        self.window = curses.newwin(size[1], size[0], position[1], position[0])
        self.window.addstr(1, (size[0]-len(title))//2, title)
        self.window.box()
        
        self.window.refresh()
        
        for element in elements:
            if element["type"] == "Menu":
                self.elements.append(Menu(self.window, **element))
            elif element["type"] == "Input":
                self.elements.append(Input(self.window, **element))
            elif element["type"] == "Button":
                self.elements.append(Button(self.window, **element))
            
    def process(self):
        if len(self.elements) == 0: return None
        result : str = self.elements[self.selected_id].process()
        if result is None: return None
        elif result == "DOWN":
            if self.selected_id < len(self.elements)-1: self.selected_id += 1
            return None
        elif result == "UP":
            if self.selected_id > 0: self.selected_id -= 1
            return None
        elif "POST" in result:
            while "{" in result:
                start = result.index("{")
                end = result.index("}")
                result = result[:start] + str(eval(result[start+1:end])) + result[end+1:]
            return result
        else: return result

class Menu:
    def __init__(self, parent : curses.window, size, position, options, commands, **kwargs):
        self.options = options
        self.commands = commands
        
        parent_y, parent_x = parent.getbegyx()
        self.window = curses.newwin(size[1], size[0], parent_y + position[1], parent_x + position[0])
        self.window.nodelay(True)
        self.window.keypad(True)
        
        self.selected = 0
        for index, option in enumerate(self.options):
            self.window.addstr(index, 2, option)
        
    def process(self):
        self.window.addstr(self.selected, 0, "> ", curses.A_BLINK)
        
        try: key = self.window.getch()
        except: key = None
        
        if key == curses.KEY_DOWN and self.selected < len(self.options)-1:
            self.window.addstr(self.selected, 0, "  ")
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.window.addstr(self.selected, 0, "  ")
            self.selected -= 1
        elif key == 10:
            return self.commands[self.selected]
        
        self.window.refresh()
        
class Input:
    def __init__(self, parent : curses.window, size, position, label, char=None, **kwargs):
        self.label = label
        self.char = char
        self.input_string = ""
        self.input_len = size[0]-len(label)-3
        
        parent_y, parent_x = parent.getbegyx()
        parent.addstr(position[1]+1, position[0], label)
        parent.refresh()
        self.window = curses.newwin(size[1], size[0]-len(label)-1, parent_y+position[1], parent_x+position[0]+len(label)+1)
        self.window.box()
        self.window.refresh()
        
        self.window.keypad(True)
        self.window.nodelay(True)
        
    def process(self):
        try: key = self.window.getch()
        except: key = None
        
        if self.char is None: self.window.addstr(1, 1, self.input_string)
        else: self.window.addstr(1, 1, self.char*len(self.input_string))
        self.window.addstr(1, 1+len(self.input_string), "█", curses.A_BLINK)
        self.window.refresh()
        
        if key is None or key == -1: return None
        elif key == curses.KEY_BACKSPACE and len(self.input_string) > 0:
            self.input_string = self.input_string[:-1]
        elif key == 10 or key == curses.KEY_DOWN:
            self.window.addstr(1, 1+len(self.input_string), " ")
            self.window.refresh()
            return "DOWN"
        elif key == curses.KEY_UP:
            self.window.addstr(1, 1+len(self.input_string), " ")
            self.window.refresh()
            return "UP"
        elif len(chr(key)) == 1 and len(self.input_string) < self.input_len:
            self.input_string += chr(key)
    
class Button:
    def __init__(self, parent : curses.window, size, position, label, command, **kwargs):
        self.size = size
        self.label = label
        self.command = command
        
        parent_y, parent_x = parent.getbegyx()
        self.window = curses.newwin(size[1], size[0], parent_y+position[1], parent_x+position[0])
        self.window.addstr(size[1]//2, (size[0]-len(label))//2, label)
        
        self.window.box()
        self.window.refresh()
        self.window.keypad(True)
        self.window.nodelay(True)
    
    def process(self):
        self.window.addstr(self.size[1]//2, (self.size[0]-len(self.label))//2, self.label, curses.A_REVERSE)
        
        try: key = self.window.getch()
        except: key = None
        
        if key == curses.KEY_DOWN:
            self.window.addstr(self.size[1]//2, (self.size[0]-len(self.label))//2, self.label)
            self.window.refresh()
            return "DOWN"
        elif key == curses.KEY_UP:
            self.window.addstr(self.size[1]//2, (self.size[0]-len(self.label))//2, self.label)
            self.window.refresh()
            return "UP"
        elif key == 10:
            return self.command
        
class App:
    def __init__(self):
        print(f"\033[8;{HEIGHT};{WIDTH}t", end="\r")
        self.client = Client("localhost", 9091)
        self.current_page = None
        self.window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.mainLoop(self.window)
        
    def __del__(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
    
    def mainLoop(self, stdscr : curses.window):
        stdscr.clear()
        self.client.AESSend("GET homepage")
        self.current_page = Page(**json.loads(self.client.AESRecv()))
        while True:
            result = self.current_page.process()
            if not result: continue
            elif result == "EXIT": break
            elif "GET" in result or "POST" in result:
                self.client.AESSend(result)
                self.current_page = Page(**json.loads(self.client.AESRecv()))
    
if __name__ == "__main__":
    App()
