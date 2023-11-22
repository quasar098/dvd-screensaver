# noinspection PyPackageRequirements
import pygame
import win32api
import win32con
# noinspection PyPackageRequirements
import win32gui
import ctypes
from ctypes import wintypes

NOSIZE = 1
NOMOVE = 2
TOPMOST = -1
NOT_TOPMOST = -2

pygame.init()

colors = [(255, 131, 0), (255, 250, 1), (255, 0, 139), (0, 38, 255), (255, 38, 0), (190, 0, 255), (0, 255, 255)]

# noinspection PyBroadException
pic_width, pic_height = 320, 144
screen_width, screen_height = 1920, 1080
taskbar_height = 0  # if you dont want it over the taskbar change it to 40

flags = 0
flags |= pygame.NOFRAME
screen = pygame.display.set_mode([pic_width, pic_height], flags)
FRAMERATE = pygame.display.get_current_refresh_rate()


hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(128, 128, 128), 0, win32con.LWA_COLORKEY)

screen.fill([128, 128, 128])
pygame.display.flip()

surf = pygame.transform.scale(pygame.image.load("./dvd.png").convert_alpha(), [pic_width, pic_height])
surfs = []
for col in colors:
    surf_copy = surf.copy()
    for x in range(surf_copy.get_width()):
        for y in range(surf_copy.get_height()):
            pos = [x, y]
            c = surf_copy.get_at(pos)
            c.r = int(c.a*col[0]/255)
            c.g = int(c.a*col[1]/255)
            c.b = int(c.a*col[2]/255)
            surf_copy.set_at(pos, c)
    surfs.append(surf_copy)
color_index = 0

clock = pygame.time.Clock()
position = [0, 0]
prev_delta = [1, 1]
delta = [1, 1]
SPEED = 300

running = True
while running:
    screen.fill([128, 128, 128])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # code here
    screen.blit(surfs[color_index % len(surfs)], [0, 0])
    if position[0] > screen_width-pic_width:
        delta[0] = -1
    if position[1] > screen_height-pic_height-taskbar_height:
        delta[1] = -1
    if position[0] < 0:
        delta[0] = 1
    if position[1] < 0:
        delta[1] = 1
    if tuple(delta) != tuple(prev_delta):
        color_index += 1
        prev_delta = delta.copy()
    position[0] += delta[0]*SPEED/FRAMERATE
    position[1] += delta[1]*SPEED/FRAMERATE

    user32 = ctypes.WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [
        wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT
    ]
    user32.SetWindowPos(hwnd, -1, *[int(pos) for pos in position], 0, 0, 0x0001)

    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()
