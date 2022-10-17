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
        self.rect = pygame.rect.Rect(*pos, 10, 800)
        self.disks: list[Disk] = []

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 122), self.rect)


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


def point_collision(rect: pygame.Rect, point: pygame.Vector2):
    return (
        point.x >= rect.x
        and point.x <= rect.x + rect.width
        and point.y >= rect.y
        and point.y <= rect.y + rect.height
    )


def rect_collision(rect1: pygame.Rect, rect2: pygame.Rect):
    return (
        point_collision(rect1, pygame.Vector2(rect2.topleft))
        or point_collision(rect1, pygame.Vector2(rect2.topright))
        or point_collision(rect1, pygame.Vector2(rect2.bottomleft))
        or point_collision(rect1, pygame.Vector2(rect2.bottomright))
        or point_collision(rect2, pygame.Vector2(rect1.topleft))
        or point_collision(rect2, pygame.Vector2(rect1.topright))
        or point_collision(rect2, pygame.Vector2(rect1.bottomleft))
        or point_collision(rect2, pygame.Vector2(rect1.bottomright))
        or (
            (
                rect1.top <= rect2.top
                and rect1.bottom >= rect2.bottom
                and rect1.left <= rect2.left
                and rect1.right >= rect2.right
            )
            or (
                rect2.top <= rect1.top
                and rect2.bottom >= rect1.bottom
                and rect2.left <= rect1.left
                and rect2.right >= rect1.right
            )
            or (
                rect1.top <= rect2.top
                and rect1.bottom >= rect2.bottom
                and rect1.left >= rect2.left
                and rect1.right <= rect2.right
            )
            or (
                rect2.top <= rect1.top
                and rect2.bottom >= rect1.bottom
                and rect2.left >= rect1.left
                and rect2.right <= rect1.right
            )
            or (
                rect1.top >= rect2.top
                and rect1.bottom <= rect2.bottom
                and rect1.left <= rect2.left
                and rect1.right >= rect2.right
            )
            or (
                rect2.top >= rect1.top
                and rect2.bottom <= rect1.bottom
                and rect2.left <= rect1.left
                and rect2.right >= rect1.right
            )
            or (
                rect1.top >= rect2.top
                and rect1.bottom <= rect2.bottom
                and rect1.left >= rect2.left
                and rect1.right <= rect2.right
            )
            or (
                rect2.top >= rect1.top
                and rect2.bottom <= rect1.bottom
                and rect2.left >= rect1.left
                and rect2.right <= rect1.right
            )
        )
    )


def get_hovering(mouse_pos: pygame.Vector2, towers: list[Tower]):
    for t in towers:
        for d in t.disks:
            if point_collision(d.rect, mouse_pos):
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
                    (t1.rect.x + (t1.rect.w / 2)) - (size_scale / 2),
                    screen.get_height() - pos_scale,
                ),
                size_scale,
            )
        )
    return towers


def get_tower(edit: Disk, mouse_pos: pygame.Vector2, towers: list[Tower]):
    pass


def grab_disk(disk: None | Disk, tower: None | Tower):
    if (
        disk is not None
        and edit is None
        and disk == max(tower.disks, key=lambda x: x.value)
    ):
        return disk


def move_disk(edit: None | Disk, tower: None | Tower, mouse_pos: pygame.Vector2):
    if edit is not None:
        pass


def stat_rect(screen: pygame.Surface, color: tuple[int, int, int]):
    pygame.draw.rect(screen, color, (0, 0, 50, 50))


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

            if event.type == pygame.MOUSEBUTTONUP:
                edit = None

        if edit is not None:
            edit.rect.center = mouse_pos

        screen.fill((0, 0, 0))

        for t in towers:
            t.draw(screen)
            for d in t.disks:
                d.draw(screen)

        if disk is not None:
            highlight(screen, disk)

        if edit is not None:
            if start_tower is not None:
                print(start_tower.rect.top)
                stat_rect(screen, RED)
                if rect_collision(edit.rect, start_tower.rect):
                    stat_rect(screen, GREEN)

        pygame.display.flip()
    pygame.quit()
