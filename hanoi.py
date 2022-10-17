import pygame
import random

pygame.init()

WHITE = (255, 255, 255)


class Tower:
    def __init__(self, pos: pygame.Vector2) -> None:
        self.rect = pygame.rect.Rect(*pos, 10, 600)
        self.disks: list[Disk] = []

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 122), self.rect)


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
    towers.append(Tower(pygame.Vector2(center.x - 500, y)))
    towers.append(Tower(pygame.Vector2(center.x - 50, y)))
    towers.append(Tower(pygame.Vector2(center.x + 450, y)))

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


def solve(disk_count):
    pass


def main():
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Towers of Hanoi")
    running = True

    edit: Disk = None

    disk_count = 3

    towers: list[Tower] = reset(screen, disk_count)

    while running:
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                edit = grab_disk(disk, start_tower)

            if event.type == pygame.MOUSEBUTTONUP and edit is not None:
                tower = get_tower(edit, towers)
                if tower is not None:
                    if (
                        len(tower.disks) == 0
                        or edit.value < min(tower.disks, key=lambda x: x.value).value
                    ):
                        set_disk(edit, tower, start_tower)
                    else:
                        edit.rect.center = edit.last
                else:
                    edit.rect.center = edit.last
                edit = None

        if edit is not None:
            edit.rect.center = mouse_pos

        screen.fill((0, 0, 0))

        for t in towers:
            t.draw(screen)
            for d in t.disks:
                d.draw(screen)

        if disk is not None:
            highlight(screen, disk.rect)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
