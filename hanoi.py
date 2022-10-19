from dis import dis
import pygame
import random

pygame.init()

WHITE = (255, 255, 255)


class Tower:
    def __init__(self, pos: pygame.Vector2, index: int):
        self.rect = pygame.rect.Rect(*pos, 10, 600)
        self.disks: list[Disk] = []
        self.index = index

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 122), self.rect)

    def debug(self):
        for d in self.disks:
            print(d.value)


class Disk:
    def __init__(self, value: int, rect: pygame.Rect) -> None:
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.value = value
        self.rect = rect
        self.last = self.rect.center

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


def get_hovering(mouse_pos: pygame.Vector2, towers: list[Tower]):
    for t in towers:
        for d in t.disks:
            if d.rect.collidepoint(mouse_pos):
                return d, t


def highlight(screen: pygame.Surface, rect: pygame.Rect):
    pygame.draw.rect(screen, WHITE, rect, 1)


def reset(screen: pygame.Surface, disk_count: int):
    center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    y = screen.get_height() - 600
    towers: list[Tower] = []
    towers.append(Tower(pygame.Vector2(center.x - 505, y), 0))
    towers.append(Tower(pygame.Vector2(center.x - 5, y), 1))
    towers.append(Tower(pygame.Vector2(center.x + 495, y), 2))

    for i in range(disk_count, 0, -1):
        scale = (i + 1) * 50
        set_disk(Disk(i, pygame.Rect(0, 0, scale, 50)), towers[0])
    return towers


def get_tower(edit: Disk, towers: list[Tower]):
    for t in towers:
        if edit.rect.colliderect(t.rect):
            return t


def grab_disk(disk: None | Disk, tower: None | Tower):
    if disk is not None and disk == min(tower.disks, key=lambda x: x.value):
        return disk


def set_disk(edit: Disk, tower: Tower, start_tower: None | Tower = None):
    if start_tower:
        start_tower.disks.remove(edit)
    edit.rect.center = tower.rect.center
    if tower.disks:
        edit.rect.bottom = tower.disks[-1].rect.top
    else:
        edit.rect.bottom = tower.rect.bottom
    tower.disks.append(edit)
    edit.last = edit.rect.center


def find_move(test_disk: Disk, start_tower: Tower, towers: list[Tower]):
    for t in towers:
        if test_move(test_disk, t, start_tower):
            return True
    return False


def test_move(test_disk: Disk, tower: Tower, start_tower: Tower):
    if (
        len(tower.disks) == 0
        or test_disk.value < min(tower.disks, key=lambda x: x.value).value
    ):
        set_disk(test_disk, tower, start_tower)
        return True
    return False


def debug(disk: Disk, start_index: int, move_index: int):
    resolve_index = [0, 1, 2]
    if move_index < 0:
        move_index = resolve_index[move_index]
    print(f"Disk {disk.value} moved from tower {start_index} to tower {move_index}.")


def move_one(towers: list[Tower], left: bool):
    for i, t in enumerate(towers):
        for d in t.disks:
            if d.value == 1:
                if left:
                    set_disk(d, towers[(i - 1) % 3], t)
                    # debug(d, i, (i - 1) % 3)
                else:
                    set_disk(d, towers[(i + 1) % 3], t)
                    # debug(d, i, (i % 3))
                return


def move_two(towers: list[Tower]):
    for t in towers:
        for d in t.disks:
            if d.value == 2:
                find_move(d, t, towers)
                return


def move_three(towers: list[Tower]):
    for t in towers:
        for d in t.disks:
            if d.value == 3:
                find_move(d, t, towers)
                return


def move_big(towers: list[Tower]):
    for t in towers:
        for d in t.disks:
            if d.value > 3 and d == min(t.disks, key=lambda x: x.value):
                if find_move(d, t, towers):
                    return


def print_towers(towers: list[Tower]):
    for i, t in enumerate(towers):
        print(f"tower {i} has:")
        t.debug()


def solve(disk_count: int, towers: list[Tower], move: tuple(int, int)):
    solve(disk_count, towers, move)
    if towers[0].disks[0].value == disk_count:
        set_disk(towers[0].disks[0], towers[2], towers[0])
    


def win(screen: pygame.Surface, tower: Tower, disk_count: int):
    if len(tower.disks) == disk_count:
        pygame.draw.circle(
            screen, (0, 255, 0), (screen.get_width() / 2, screen.get_height() / 2), 250
        )
        return True
    return False


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Towers of Hanoi")
    running = True

    edit: Disk = None

    disk_count = 20

    solve = False

    towers: list[Tower] = reset(screen, disk_count)

    while running:
        # clock.tick(60)
        for event in pygame.event.get():
            mouse_pos = pygame.Vector2(*pygame.mouse.get_pos())
            if (x := get_hovering(mouse_pos, towers)) is not None:
                disk, start_tower = x
            else:
                disk = None
                start_tower = None
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                running = False
            if keys[pygame.K_LSHIFT]:
                towers = reset(screen, disk_count)
            if keys[pygame.K_SPACE]:
                solve = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                edit = grab_disk(disk, start_tower)

            if event.type == pygame.MOUSEBUTTONUP and edit is not None:
                tower = get_tower(edit, towers)
                if tower is not None:
                    test_move(edit, tower, start_tower)
                else:
                    edit.rect.center = edit.last
                edit = None

        if edit is not None:
            edit.rect.center = mouse_pos

        screen.fill((0, 0, 0))

        if solve:
            if not len(towers[2].disks) == disk_count:
                if disk_count % 2 == 1:
                    move_one(towers, True)
                    move_two(towers)
                    move_one(towers, True)
                    move_three(towers)
                    move_one(towers, True)
                    move_two(towers)
                    move_one(towers, True)
                    move_big(towers)
                else:
                    move_one(towers, False)
                    move_two(towers)
                    move_one(towers, False)
                    move_three(towers)
                    move_one(towers, False)
                    move_two(towers)
                    move_one(towers, False)
                    move_big(towers)

        for t in towers:
            t.draw(screen)
            for d in t.disks:
                d.draw(screen)

        if disk is not None:
            highlight(screen, disk.rect)

        win(screen, towers[2], disk_count)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
