import pygame
import random

pygame.init()

BLUE = (0, 0, 200)
PINK = (200, 0, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)


class Tower:
    def __init__(self, pos: pygame.Vector2) -> None:
        self.pos = pos
        self.w = 10
        self.h = 800
        self.disks: list[Disk] = []

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 122), (*self.pos, self.w, self.h))


class Disk:
    def __init__(
        self, value: int, color: tuple[int, int, int], pos: pygame.Vector2, width: int
    ) -> None:
        self.start_pos = pos
        self.color = color
        self.value = value
        self.rect = pygame.rect.Rect(*self.start_pos, width, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


def get_hovering(mouse_pos, towers: list[Tower]):
    for t in towers:
        for d in t.disks:
            if (
                mouse_pos[0] >= d.rect.x
                and mouse_pos[0] <= d.rect.x + d.rect.width
                and mouse_pos[1] >= d.rect.y
                and mouse_pos[1] <= d.rect.y + d.rect.height
            ):
                return d, t
    return None


def rc():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def highlight(screen, disk: Disk):
    pygame.draw.rect(
        screen, WHITE, (*disk.rect.topleft, disk.rect.width, disk.rect.height), 1
    )


def reset(screen: pygame.Surface, disk_count: int):
    towers: list[Tower] = []
    towers.append(Tower(pygame.Vector2(center.x - 500, screen.get_height() - 600)))
    towers.append(Tower(pygame.Vector2(center.x - 50, screen.get_height() - 600)))
    towers.append(Tower(pygame.Vector2(center.x + 450, screen.get_height() - 600)))

    for i in range(disk_count):
        t1 = towers[0]
        pos_scale = (i + 1) * 50
        size_scale = abs((i - (disk_count + 1)) * 50)
        t1.disks.append(
            Disk(
                i,
                rc(),
                pygame.Vector2(
                    (t1.pos.x + (t1.w / 2)) - (size_scale / 2),
                    screen.get_height() - pos_scale,
                ),
                size_scale,
            )
        )
    return towers


if __name__ == "__main__":
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Towers of Hanoi")
    running = True
    center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    edit: Disk = None

    disk_count = 10

    towers: list[Tower] = reset(screen, disk_count)

    while running:
        for event in pygame.event.get():
            mouse_pos = pygame.Vector2(*pygame.mouse.get_pos())
            if (x := get_hovering(mouse_pos, towers)) is not None:
                h_disk, h_tower = x
            else:
                h_disk = None
                h_tower = None
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                running = False
            if keys[pygame.K_LSHIFT]:
                towers = reset(screen, disk_count)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    h_disk is not None
                    and edit is None
                    and h_disk == max(h_tower.disks, key=lambda x: x.value)
                ):
                    edit = h_disk
            if event.type == pygame.MOUSEBUTTONUP:
                edit = None

        if edit is not None:
            edit.rect.center = mouse_pos

        screen.fill((0, 0, 0))

        for t in towers:
            t.draw(screen)
            for d in t.disks:
                d.draw(screen)

        if h_disk is not None:
            highlight(screen, h_disk)

        pygame.display.flip()
    pygame.quit()
