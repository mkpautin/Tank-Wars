from data_classes import Cell, Brick, Mirror, Stone, Water

def get_stage():
    return [
        [Cell(True)] * 16,
        [Cell(True)] + [Brick(), Brick(), Brick()] + [Cell(True)] * 8 + [Brick(), Brick(), Brick()] + [Cell(True)],
        [Cell(True)] + [Brick()] + [Cell(True)] * 12 + [Brick()] + [Cell(True)],
        [Cell(True)] + [Brick()] + [Cell(True)] * 4 + [Water(), Water(), Water(), Water()] + [Cell(True)] * 4 + [Brick()] + [Cell(True)],
        [Cell(True)] * 6 + [Brick(), Brick(), Brick(), Brick()] + [Cell(True)] * 6,
        [Cell(True)] * 16,
        [Cell(True)] * 16,
        [Cell(True)] * 3 + [Mirror(False, "se")] + [Cell(True)] * 3 + [Stone()] * 2 + [Cell(True)] * 3 + [Mirror(False, "ne")] + [Cell(True)] * 3,
        [Cell(True)] * 7 + [Stone()] * 2 + [Cell(True)] * 7,
        [Cell(True)] * 16,
        [Cell(True)] * 16,
        [Cell(True)] * 6 + [Brick(), Brick(), Brick(), Brick()] + [Cell(True)] * 6,
        [Cell(True)] + [Brick()] + [Cell(True)] * 4 + [Water(), Water(), Water(), Water()] + [Cell(True)] * 4 + [Brick()] + [Cell(True)],
        [Cell(True)] + [Brick()] + [Cell(True)] * 12 + [Brick()] + [Cell(True)],
        [Cell(True)] + [Brick(), Brick(), Brick()] + [Cell(True)] * 8 + [Brick(), Brick(), Brick()] + [Cell(True)],
        [Cell(True)] * 16
    ]

def get_player_spawn() -> tuple[int, int]:
    return (0,15)

def get_enemy_spawns() -> list[tuple[int, int]]:
    return [(2,2), (13,2)]