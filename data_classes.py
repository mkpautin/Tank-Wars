from __future__ import annotations
from typing import Literal
from dataclasses import dataclass

Directions = Literal["north", "south", "east", "west"]

@dataclass
class Cell:
    passable: bool
 
@dataclass
class Brick(Cell):
    hits: int = 2
    passable: bool = False

    def is_passable(self):
        if self.hits == 0:
            self.passable = True

@dataclass
class Stone(Cell):
    passable: bool = False

@dataclass
class Mirror(Cell):
    orientation: Literal["ne", "se"]
    passable = False

    def change_direction(self, bullet: Bullet):
        if self.orientation == "ne":
            if bullet.facing == "north":
                bullet.facing = "east"
            elif bullet.facing == "south":
                bullet.facing = "west"
            elif bullet.facing == "east":
                bullet.facing = "north"
            else:
                bullet.facing = "south"

        else:
            if bullet.facing == "north":
                bullet.facing = "west"
            elif bullet.facing == "south":
                bullet.facing = "east"
            elif bullet.facing == "east":
                bullet.facing = "south"
            else:
                bullet.facing = "north"

@dataclass
class Water(Cell):
    passable: bool = False

@dataclass
class Bullet:
    r: float
    c: float
    facing: Directions
    speed: int = 2
    max_x: float = 0
    max_y: float = 0

    @property
    def head(self):
        if self.facing == "north":
            return (self.r, self.c + 0.5)
        elif self.facing == "south":
            return (self.bottom , self.c + 0.5)
        elif self.facing == "east":
            return (self.r + 0.5, self.right)
        else:
            return (self.r + 0.5, self.c)

    @property
    def right(self):
        return self.c + 1
    
    @property
    def bottom(self):
        return self.r + 1
    
    @property
    def center(self):
        return (self.r + 0.5, self.c + 0.5)

@dataclass
class Tank:
    r: float
    c: float
    speed: int = 1
    bullet: Bullet | None = None
    facing: Directions = "north"
    max_x: int = 7
    max_y: int = 7
    move_timer: int = 0

    @property
    def head(self):
        if self.facing == "north":
            return (self.r, self.c + 4)
        elif self.facing == "south":
            return (self.r + 8, self.c + 4)
        elif self.facing == "east":
            return (self.r + 4, self.c + 8)
        else:
            return (self.r + 4, self.c)
        
    @property
    def right(self):
        return self.c + self.max_x
    
    @property
    def bottom(self):
        return self.r + self.max_y
        
@dataclass
class State:
    player: Tank
    enemies: list[Tank]
    stage: list[list[Cell]]
    enemy_spawn: list[tuple[int, int]]
    tick: int
    enemy_bullets: list[Bullet]
    enemies_to_spawn: int = 16
    is_game_over: bool = False

    def did_win(self):
        if not self.enemies and self.enemies_to_spawn == 0:
            return True
        else:
            return False
        