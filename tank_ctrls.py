from __future__ import annotations
import pyxel
from random import choice
from data_classes import Cell, Brick, Stone, Mirror, Water, Tank, Bullet, State, Directions
from stage1 import get_stage, get_player_spawn, get_enemy_spawns

class App:
    def __init__(self):
        self.screen_height = 16*8
        self.screen_width = 16*8
        self.fps = 60
        self.cs, self.rs = get_player_spawn()
        self.state = self.init_state()

        pyxel.init(self.screen_width, self.screen_height, fps=self.fps)
        pyxel.load("stage.pyxres")
        pyxel.run(self.update, self.draw)

    def init_state(self):
        return State(
            Tank(self.rs*8, self.cs*8),
            [],
            get_stage(),
            get_enemy_spawns(),
            0,
            [],
            is_game_over=False
        )

    def update(self):
        if not self.state.is_game_over:
            self.update_mybullets()
            self.update_player_tank()
            self.update_enemy_tanks()
            self.update_tick()
            self.update_game_over_win()
        else:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = self.init_state()

    def draw(self):
        self.clear_screen()
        if self.state.is_game_over:
            self.draw_game_over()
        else:
            self.draw_player_tank()
            self.draw_enemy_tanks()
            self.draw_stage()
            self.draw_bullets()

    def update_game_over_win(self):
        if self.state.did_win():
            self.state.is_game_over = True

    def update_player_tank(self):
        player = self.state.player
        if pyxel.btnp(pyxel.KEY_W, hold=1, repeat=1):
            player.facing = "north"
            self.move(player, "north")
        elif pyxel.btnp(pyxel.KEY_S, hold=1, repeat=1):
            player.facing = "south"
            self.move(player, "south")
        elif pyxel.btnp(pyxel.KEY_D, hold=1, repeat=1):
            player.facing = "east"
            self.move(player, "east")
        elif pyxel.btnp(pyxel.KEY_A, hold=1, repeat=1):
            player.facing = "west"
            self.move(player, "west")

    def update_mybullets(self):
        player = self.state.player
        if player.bullet:
            for _ in range(2):
                if player.bullet:
                    self.move(player.bullet, player.bullet.facing)
                    if self.did_hit(player.bullet, player):
                        self.state.is_game_over = True
                    for enemy in self.state.enemies:
                        if self.did_hit(player.bullet, enemy):
                            player.bullet = None
                            self.state.enemies.remove(enemy)
                            break
                    if player.bullet and (not self.in_bounds(player.bullet.r, player.bullet.c, player.bullet.max_x, player.bullet.max_y) or player.bullet.speed == 0):
                        player.bullet = None
                
        else:
            if pyxel.btnp(pyxel.KEY_SPACE):
                r, c = player.head
                player.bullet = Bullet(r, c, player.facing)
                self.move(player.bullet, player.bullet.facing)

        for _ in range(2):
            for bullet in self.state.enemy_bullets:
                self.move(bullet, bullet.facing)
                if self.did_hit(bullet, self.state.player):
                    self.state.is_game_over = True
                if player.bullet:
                    if self.did_hit(player.bullet, bullet) or self.did_hit(bullet, player.bullet):
                        player.bullet = None
                        self.state.enemy_bullets.remove(bullet)
                        continue
                if not self.in_bounds(bullet.r, bullet.c, bullet.max_x, bullet.max_y) or bullet.speed == 0:
                    self.state.enemy_bullets.remove(bullet)
                    continue
                for bullet2 in self.state.enemy_bullets:
                    if bullet != bullet2:
                        if self.did_hit(bullet, bullet2) or self.did_hit(bullet2, bullet):
                            self.state.enemy_bullets.remove(bullet)
                            self.state.enemy_bullets.remove(bullet2)

    def update_enemy_tanks(self):
        state = self.state
        if state.enemies_to_spawn > 0 and state.tick % 300 == 0:
            self.spawn_enemy_tank()
            state.enemies_to_spawn -= 2

        for tank in state.enemies:
            self.move_enemy_tank(tank)


    def update_tick(self):
        self.state.tick += 1

    def did_hit(self, bullet: Bullet, particle: Tank | Bullet):
        if self.in_collision(bullet, particle):
            return True
        return False

    def spawn_enemy_tank(self):
        state = self.state
        for spawn in state.enemy_spawn:
            x, y = spawn
            x *= 8
            y *= 8
            state.enemies.append(
                Tank(y, x, 1)
            )

    def move_enemy_tank(self, tank: Tank):
        if tank.move_timer == 0:
            if self.state.tick % 60 == 0:
                move = choice(["m", "d", "s"])
                if move == "m":
                    
                    tank.move_timer = 30
                    self.move(tank, tank.facing)
                    
                elif move == "d":
                    directions: list[Directions] = ["north", "south", "east", "west"]
                    tank.facing = choice([d for d in directions if d != tank.facing])
                else:
                    r, c  = tank.head
                    self.state.enemy_bullets.append(Bullet(r, c, tank.facing))
        
        else:
            tank.move_timer -= 1
            self.move(tank, tank.facing)

    def clear_screen(self):
        pyxel.cls(0)

    def draw_player_tank(self):
        tank = self.state.player
        if tank.facing == "north":
            pyxel.blt(tank.c, tank.r, 0, 0, 24, 8, 8, 0)
            
        elif tank.facing == "east":
            pyxel.blt(tank.c, tank.r, 0, 0, 16, 8, 8, 0)
            
        elif tank.facing == "west":
            pyxel.blt(tank.c, tank.r, 0, 8, 24, 8, 8, 0)
            
        else:
            pyxel.blt(tank.c, tank.r, 0, 8, 16, 8, 8, 0)

    def draw_enemy_tanks(self):
        enemies = self.state.enemies
        for tank in enemies:
            if tank.facing == "north":
                pyxel.blt(tank.c, tank.r, 0, 16, 24, 8, 8, 0)
            
            elif tank.facing == "east":
                pyxel.blt(tank.c, tank.r, 0, 16, 16, 8, 8, 0)
                
            elif tank.facing == "west":
                pyxel.blt(tank.c, tank.r, 0, 24, 24, 8, 8, 0)
                
            else:
                pyxel.blt(tank.c, tank.r, 0, 24, 16, 8, 8, 0)

    def draw_bullets(self):
        player = self.state.player
        if player.bullet:
            pyxel.rect(player.bullet.c, player.bullet.r, 1, 1, 7)

        for bullet in self.state.enemy_bullets:
            pyxel.rect(bullet.c, bullet.r, 1, 1, 7)

    def draw_stage(self):
        stage_len = len(self.state.stage)
        for row in range(stage_len):
            for col in range(stage_len):
                cell = self.state.stage[row][col]
                if isinstance(cell, Brick):
                    uv = (0,0) if cell.hits > 1 else (40,0)
                    u,v = uv
                    pyxel.blt(col*8, row*8, 0, u, v, 8, 8, 0)
                elif isinstance(cell, Stone):
                    pyxel.blt(col*8, row*8, 0, 8, 0, 8, 8, 0)
                elif isinstance(cell, Mirror):
                    pyxel.blt(col*8, row*8, 0, 0 if cell.orientation == "ne" else 8, 8, 8, 8, 0)
                elif isinstance(cell, Water):
                    pyxel.blt(col*8, row*8, 0, 32, 0 , 8, 8, 0)

    def draw_game_over(self):
        if self.state.did_win():
            pyxel.text(self.screen_width / 2 - 17, self.screen_height / 2 - 2, "YOU WIN", 7)
        else:
            pyxel.text(self.screen_width / 2 - 17, self.screen_height / 2 - 2, "YOU LOSE", 7)


    def in_collision(self, particle1: Bullet, particle2: Tank | Bullet):
        r, c = particle1.center
        if particle2.c <= c <= particle2.right and particle2.r <= r <= particle2.bottom:
            return True
        return False

    def in_bounds(self, r: float, c: float, max_x: float, max_y: float):
        if 0 <= r < self.screen_height-max_y and 0 <= c < self.screen_width-max_x:
            return True
        return False
    
    def movable(self, particle: Tank | Bullet, r: float , c: float):
        stage = self.state.stage
        x = int(c//8)
        y = int(r//8)
        cell = stage[y][x]
        if isinstance(particle, Bullet):
            if isinstance(cell, Mirror):
                cell.change_direction(particle)
                return True
            elif isinstance(cell, Water):
                return True
            elif isinstance(cell, Brick):
                cell.hits -= 1
                if cell.hits == 0:
                    stage[y][x] = Cell(True)
                return False
            else:
                return cell.passable
        else:
            return cell.passable
        

    def move(self, particle: Tank | Bullet, direction: Directions):
        if isinstance(particle, Tank):
            if direction == "north":
                if self.in_bounds(particle.r - 1, particle.c, particle.max_x, particle.max_y) and self.movable(particle, particle.r-1, particle.c) and self.movable(particle, particle.r-1, particle.right):
                    particle.r -= 1
            elif direction == "south":
                if self.in_bounds(particle.r + 1, particle.c, particle.max_x, particle.max_y) and self.movable(particle, particle.bottom + 1, particle.c) and self.movable(particle, particle.bottom+1, particle.right):
                    particle.r += 1

            elif direction == "east":
                if self.in_bounds(particle.r, particle.c + 1, particle.max_x, particle.max_y) and self.movable(particle, particle.r, particle.right + 1) and self.movable(particle, particle.bottom, particle.right + 1):
                    particle.c += 1
            else:
                if self.in_bounds(particle.r, particle.c - 1, particle.max_x, particle.max_y) and self.movable(particle, particle.r, particle.c - 1) and self.movable(particle, particle.bottom, particle.c - 1):
                    particle.c -= 1

        else:
            r, c = particle.head
            if direction == "north":
                if self.in_bounds(r - 1, c, particle.max_x, particle.max_y) and self.movable(particle, r - 1, c):
                    particle.r -= 1
                else:
                    particle.speed = 0
            elif direction == "south":
                if self.in_bounds(r + 1, c, particle.max_x, particle.max_y) and self.movable(particle, r + 1, c):
                    particle.r += 1
                else:
                    particle.speed = 0
            elif direction == "east":
                if self.in_bounds(r, c + 1, particle.max_x, particle.max_y) and self.movable(particle, r, c + 1):
                    particle.c += 1
                else:
                    particle.speed = 0
            else:
                if self.in_bounds(r, c-1, particle.max_x, particle.max_y) and self.movable(particle, r, c-1):
                    particle.c -= 1
                else:
                    particle.speed = 0

         
App()