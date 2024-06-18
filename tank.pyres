import pyxel
from typing import Literal
from dataclasses import dataclass

Directions = Literal["north", "south", "east", "west"]

@dataclass
class Tank:
    r: int
    c: int
    facing: Directions = "east"

class App:
    def __init__(self):
        self.screen_height = 100
        self.screen_width = 100
        self.fps = 60
        self.mytank = Tank(0, 0)

        pyxel.init(self.screen_width, self.screen_height, fps=self.fps)
        pyxel.load("tank.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_mytank()

    def update_mytank(self):
        if pyxel.btnp(pyxel.KEY_W, hold=1, repeat=1):
            self.move(self.mytank, "north")
        elif pyxel.btnp(pyxel.KEY_S, hold=1, repeat=1):
            self.move(self.mytank, "south")
        elif pyxel.btnp(pyxel.KEY_D, hold=1, repeat=1):
            self.move(self.mytank, "east")
        elif pyxel.btnp(pyxel.KEY_A, hold=1, repeat=1):
            self.move(self.mytank, "west")

    def draw(self):
        self.clear_screen()
        self.draw_tank(self.mytank)

    def clear_screen(self):
        pyxel.cls(0)

    def draw_tank(self, tank: Tank):
        if tank.facing == "north":
            pyxel.blt(tank.c, tank.r, 0, 0, 0, 16, 16)
            
        elif tank.facing == "east":
            pyxel.blt(tank.c, tank.r, 0, 16, 0, 16, 16)
            
        elif tank.facing == "west":
            pyxel.blt(tank.c, tank.r, 0, 48, 0, 16, 16)
            
        else:
            pyxel.blt(tank.c, tank.r, 0, 32, 0, 16, 16)

    def in_bounds(self, r: int, c: int):
        if 0 <= r < self.screen_height-15 and 0 <= c < self.screen_width-15:
            return True
        return False
    
    def move(self, tank: Tank, direction: Directions):
        tank.facing = direction
        if direction == "north":
            if self.in_bounds(tank.r - 1, tank.c):
                tank.r -= 1
        elif direction == "south":
            if self.in_bounds(tank.r + 1, tank.c):
                tank.r += 1
        elif direction == "east":
            if self.in_bounds(tank.r, tank.c + 1):
                tank.c += 1
        else:
            if self.in_bounds(tank.r, tank.c - 1):
                tank.c -= 1
    
App()
