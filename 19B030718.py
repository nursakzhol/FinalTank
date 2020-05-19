from time import sleep
from pygame import mixer
import pygame
import random
from pygame.locals import *
import sys

pygame.init()


class Window():
    weight = 800
    height = 600
    fps = 60


screen = pygame.display.set_mode((Window.weight, Window.height))
font = pygame.font.SysFont(None, 36)
wall = pygame.image.load('img/wall.png')
power = pygame.image.load('img/power.png')
walls = pygame.image.load('img/walls.png')
walls2 = pygame.transform.rotate(walls, 90)
bg = pygame.image.load('img/bg.png')
menuu = pygame.image.load('img/menu.png')
gameover = pygame.image.load('img/gameover.png')
instrutionn = pygame.image.load('img/instruction.png')


def drawtext(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def menu():
    screen = pygame.display.set_mode((Window.weight, Window.height))
    playsound('335571__magntron__gamemusic.mp3')
    while True:

        screen.blit(menuu, (0, 0))
        drawtext('Main menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(50, 100, 200, 50)
        button2 = pygame.Rect(50, 200, 200, 50)
        button3 = pygame.Rect(50, 300, 200, 50)

        if button1.collidepoint((mx, my)):
            if click:
                instrut_win()
        if button2.collidepoint((mx, my)):
            if click:
                multiplayer()
        if button3.collidepoint((mx, my)):
            if click:
                multiplayerai()

        drawtext('Single Player', font, (255, 255, 255), screen, 70, 110)
        drawtext('MultiPlayer', font, (255, 255, 255), screen, 70, 210)
        drawtext('Multiplayer AI', font, (255, 255, 255), screen, 70, 310)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        clock = pygame.time.Clock()
        playtime = 0

        pygame.display.update()
        milliseconds = clock.tick(Window.fps)
        seconds = milliseconds / 1000.0  # seconds passed since last frame (float)
        playtime += seconds


def playsound(sound):
    pygame.mixer.music.load('sounds/' + sound)
    pygame.mixer.music.play(-1)


def playsound1(sound):
    mixer.init()
    sound = mixer.Sound('sounds/' + sound)
    sound.play()


class snaryad():
    def __init__(self, x, y, facing):
        self.x = int(x)
        self.y = int(y)
        self.facing = facing

    def draw(self, screen):
        cl = random.randrange(0, 255)
        rd = random.randrange(0, 255)
        gd = random.randrange(0, 255)
        pygame.draw.circle(screen, (cl, rd, gd), (self.x, self.y), 5)

    def bull_move(self):
        for bullet in self:
            if bullet.x <= 1000 and bullet.x >= 0 and bullet.y >= 0 and bullet.y <= 800:
                if bullet.facing == "right":
                    bullet.x += 10
                if bullet.facing == "left":
                    bullet.x -= 10
                if bullet.facing == "up":
                    bullet.y -= 10
                if bullet.facing == "down":
                    bullet.y += 10
            else:
                self.pop(self.index(bullet))

    def bull_add(self, instance, x, y, n):

        self.n = n
        bull_x = self.x + 20
        bull_y = self.y + 20
        if len(instance) < n:
            instance.append(snaryad(bull_x, bull_y, self.facing))
            playsound1('344310__musiclegends__laser-shoot.wav')


# class Walls(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.x = 0
#         self.y = 0
#         self.width = 0
#         self.height = 0
#         self.img = None
#
#     def draw(self, screen, x, y, width, height, img):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.hitbox = (self.x, self.y, self.width, self.height)
#         self.img = img
#         screen.blit(self.img, (self.x, self.y))
#         pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
#
#     def collide(self, rect):
#         if self.hitbox[0] + self.hitbox[2] > rect[0] and self.hitbox[0] < rect[0] + rect[2] and self.hitbox[1] + self.hitbox[3] >= rect[1] and self.hitbox[1] < rect[1] + rect[3]:
#             return True
#         return False
def instrut_win():
    screen.blit(instrutionn, (0, 0))

    hoop = True
    while hoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                if event.key == pygame.K_SPACE:
                    game()
            screen.blit(instrutionn, (0, 0))
            pygame.display.update()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, facing, healthwin, img):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.facing = facing
        self.healthwin = healthwin
        self.font = pygame.font.Font(None, 30)
        self.img = img
        self.orig = img
        self.text = self.font.render(str("Life: "), True, (255, 0, 0))
        self.health = 3
        self.score = 0
        self.stop = 0
        self.speed = 120

    def drawwin(self):
        screen.blit(self.img, (self.x, self.y))
        text2 = self.font.render(str(self.health), True, (255, 0, 0))
        screen.blit(self.text, (self.healthwin, 20))
        screen.blit(text2, (self.healthwin + 100, 20))

    def transform(self, facing, angel):
        self.img = pygame.transform.rotate(self.orig, angel)
        self.facing = facing

    def update(self, seconds):
        self.hitbox = (self.x, self.y, 41, 45)
        if self.facing == "right":
            self.x += self.speed * seconds
        if self.facing == "left":
            self.x -= self.speed * seconds
        if self.facing == "up":
            self.y -= self.speed * seconds
        if self.facing == "down":
            self.y += self.speed * seconds
        if self.stop == "stop":
            self.x = 0
            self.y = 0

        if self.x < 0:
            self.x = Window.weight
        elif self.x > Window.weight:
            self.x = 0
        elif self.y > Window.height:
            self.y = 0
        elif self.y < 0:
            self.y = Window.height

    def collide(self, rect):
        if self.hitbox[0] + self.hitbox[2] >= rect[0] and self.hitbox[0] <= rect[0] + rect[2] and self.hitbox[1] + \
                self.hitbox[3] >= rect[1] and self.hitbox[1] <= rect[1] + rect[3]:
            return True
        return False


class saw(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 61, 31)

    def draw(self, screen):
        screen.blit(power, (self.x, self.y))


def collision(bullets, player2):
    for bullet in bullets:
        if bullet.x >= player2.x and bullet.x <= player2.x + 125 and bullet.y >= player2.y and bullet.y <= player2.y + 57 and player2.facing == "right":
            player2.health -= 1
            bullets.pop(bullets.index(bullet))
            playsound1('138481__justinvoke__bullet-blood-4.wav')
        if bullet.x >= player2.x and bullet.x <= player2.x + 125 and bullet.y >= player2.y and bullet.y <= player2.y + 57 and player2.facing == "left":
            player2.health -= 1
            bullets.pop(bullets.index(bullet))
            playsound1('138481__justinvoke__bullet-blood-4.wav')
        if bullet.x >= player2.x and bullet.x <= player2.x + 57 and bullet.y >= player2.y and bullet.y <= player2.y + 120 and player2.facing == "up":
            player2.health -= 1
            bullets.pop(bullets.index(bullet))
            playsound1('138481__justinvoke__bullet-blood-4.wav')
        if bullet.x >= player2.x and bullet.x <= player2.x + 57 and bullet.y >= player2.y and bullet.y <= player2.y + 120 and player2.facing == "down":
            player2.health -= 1
            bullets.pop(bullets.index(bullet))
            playsound1('138481__justinvoke__bullet-blood-4.wav')


def game_over():
    screen.blit(gameover, (0, 0))

    pygame.display.update()
    sleep(5)
    menu()


def draw_object():
    for x in objects:
        x.draw(screen)


objects = []
bullets = []
bullets2 = []


def game():
    sleep(2)
    saww = saw(random.randrange(0, 600), random.randrange(0, 600))

    playsound('background.wav')
    pygame.time.set_timer(USEREVENT + 1, random.randrange(5000, 20000))

    foodx = round(random.randrange(0, Window.weight - 20) / 10.0) * 10.0
    foody = round(random.randrange(0, Window.height - 20) / 10.0) * 10.0
    n = 1
    f = 1
    d = 0

    frame_count = 0
    playtime = 0
    player1 = Tank(600, 600, 'up', 650, pygame.image.load("img/tank1.png"))
    player2 = Tank(100, 100, 'up', 0, pygame.image.load("img/tank2.png"))
    mainloop = True
    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                menu()
            if event.type == USEREVENT + 1:
                objects.append(saw(random.randrange(0, 700), random.randrange(0, 500)))
                print('regregreg')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                    menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
                    elif event.key == pygame.K_RIGHT:
                        player1.transform("right", -90)
                    elif event.key == pygame.K_LEFT:
                        player1.transform("left", 90)
                    elif event.key == pygame.K_UP:
                        player1.transform("up", 0)
                    elif event.key == pygame.K_DOWN:
                        player1.transform("down", 180)
                    elif event.key == pygame.K_a:
                        player2.transform("left", 90)
                    elif event.key == pygame.K_d:
                        player2.transform("right", -90)
                    elif event.key == pygame.K_w:
                        player2.transform("up", 0)
                    elif event.key == pygame.K_s:
                        player2.transform("down", 180)
                    elif event.key == pygame.K_1:
                        player1.transform("stop", 0)
                    elif event.key == pygame.K_KP1:
                        player2.transform("stop", 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player1.facing == "up":
                    snaryad.bull_add(player1, bullets, 27, -5, n)

                if event.key == pygame.K_RETURN and player1.facing == "right":
                    snaryad.bull_add(player1, bullets, 120, 27, n)
                    # playsound1('344310__musiclegends__laser-shoot.wav')
                if event.key == pygame.K_RETURN and player1.facing == "down":
                    snaryad.bull_add(player1, bullets, 27, 120, n)
                    # playsound1('344310__musiclegends__laser-shoot.wav')
                if event.key == pygame.K_RETURN and player1.facing == "left":
                    snaryad.bull_add(player1, bullets, -5, 27, n)
                    # playsound1('344310__musiclegends__laser-shoot.wav')
                if event.key == pygame.K_SPACE and player2.facing == "up":
                    snaryad.bull_add(player2, bullets2, 27, -5, f)
                    # playsound1('344310__musiclegends__laser-shoot.wav')
                if event.key == pygame.K_SPACE and player2.facing == "right":
                    snaryad.bull_add(player2, bullets2, 120, 27, f)
                    # playsound1('344310__musiclegends__laser-shoot.wav')
                if event.key == pygame.K_SPACE and player2.facing == "down":
                    snaryad.bull_add(player2, bullets2, 27, 120, f)
                    # playsound1('344310__musiclegends__laser-shoot.wav')
                if event.key == pygame.K_SPACE and player2.facing == "left":
                    snaryad.bull_add(player2, bullets2, -5, 27, f)
                    # playsound1('344310__musiclegends__laser-shoot.wav')

        screen.blit(bg, (0, 0))

        clock = pygame.time.Clock()
        milliseconds = clock.tick(Window.fps)
        seconds = milliseconds / 1000.0  # seconds passed since last frame (float)
        playtime += seconds

        start_time = 90

        total_seconds = frame_count // Window.fps
        minutes = total_seconds // 60
        secondss = total_seconds % 60
        output_string = "Time: {0:02}:{1:02}".format(minutes, secondss)

        text = font.render(output_string, True, (255, 0, 0))
        screen.blit(text, [150, 20])

        total_seconds = start_time - (frame_count // Window.fps)
        if total_seconds < 0:
            total_seconds = 0

        frame_count += 1

        draw_object()
        player1.drawwin()
        player2.drawwin()

        snaryad.bull_move(bullets)
        snaryad.bull_move(bullets2)
        collision(bullets, player2)
        collision(bullets2, player1)

        for bullet in bullets:
            bullet.draw(screen)
        for bullet in bullets2:
            bullet.draw(screen)

        player1.update(seconds)
        player2.update(seconds)

        screen.blit(wall, (foodx, foody))

        for bullet in bullets:
            if bullet.x >= foodx and bullet.x <= foodx + 60 and bullet.y >= foody and bullet.y <= foody + 30:
                bullets.pop(bullets.index(bullet))
                foodx = round(random.randrange(0, Window.weight - 20) / 10.0) * 10.0
                foody = round(random.randrange(0, Window.height - 20) / 10.0) * 10.0
                playsound1('138481__justinvoke__bullet-blood-4.wav')

        for bullet in bullets2:
            if (bullet.x >= foodx and bullet.x <= foodx + 60 and bullet.y >= foody and bullet.y <= foody + 30):
                foodx = round(random.randrange(0, Window.weight - 20) / 10.0) * 10.0
                foody = round(random.randrange(0, Window.height - 20) / 10.0) * 10.0
                playsound1('138481__justinvoke__bullet-blood-4.wav')

        if foodx + 50 >= player2.x and foodx - 10 <= player2.x + 100 and foody + 20 >= player2.y and foody + 30 <= player2.y + 57:
            player2.health -= 1
            foodx = round(random.randrange(0, Window.weight - 20) / 10.0) * 10.0
            foody = round(random.randrange(0, Window.height - 20) / 10.0) * 10.0
            playsound1('138481__justinvoke__bullet-blood-4.wav')

        if foodx + 50 >= player1.x and foodx - 10 <= player1.x + 100 and foody + 20 >= player1.y and foody + 30 <= player1.y + 57:
            player1.health -= 1
            foodx = round(random.randrange(0, Window.weight - 20) / 10.0) * 10.0
            foody = round(random.randrange(0, Window.height - 20) / 10.0) * 10.0
            playsound1('138481__justinvoke__bullet-blood-4.wav')

        if secondss == d + 5:
            player1.speed = 120
            n = 1
        for kok in objects:
            if kok.x + 50 >= player2.x and kok.x - 10 <= player2.x + 100 and kok.y + 20 >= player2.y and kok.y + 30 <= player2.y + 57:
                d = secondss
                f = 10
                player2.speed = 250
                objects.pop(objects.index(kok))
                playsound1('138481__justinvoke__bullet-blood-4.wav')

            if kok.x + 50 >= player1.x and kok.x - 10 <= player1.x + 100 and kok.y + 20 >= player1.y and kok.y + 30 <= player1.y + 57:
                d = secondss
                n = 10
                player1.speed = 250
                objects.pop(objects.index(kok))
                # playsound1('Sound_19349.mp3')
                playsound1('138481__justinvoke__bullet-blood-4.wav')
        if secondss == d + 5:
            player2.speed = 120
            n = 1

        if player1.collide(player2.hitbox):
            player1.transform("stop", 0)
            player2.transform("stop", 0)

        if player1.health <= 0 or player2.health <= 0:
            game_over()

        pygame.display.update()


import json
from operator import itemgetter, attrgetter, methodcaller
from time import sleep
import uuid
import pygame
from threading import Thread
import pika

IP = '34.254.177.17'
PORT = 5672
VHOST = 'dar-tanks'
USER = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()
screen1 = pygame.display.set_mode((800, 600))
bg1 = pygame.image.load('img/bg.png')
font1 = pygame.font.SysFont(None, 16)
gameover1 = pygame.image.load('img/gameover.png')


class TankRpcClient():

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VHOST,
                credentials=pika.PlainCredentials(
                    username=USER,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True
                                           )
        self.callback_queue = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=self.callback_queue
        )

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events(time_limit=1)

    def check_server_status(self):
        self.call('tank.request.healthcheck')
        return self.response['status'] == '200'

    def obtain_tocken(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def shoot(self, token):
        message = {
            'token': token
        }
        self.call('tank.request.fire', message)


class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VHOST,
                credentials=pika.PlainCredentials(
                    username=USER,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True
                                           )
        event_listener = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=event_listener,
            routing_key='event.state.' + room_id
        )
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print(self.response)

    def run(self):
        self.channel.start_consuming()


def draw_tank(x, y, width, heigth, direction):
    for i in range(2):
        tank1 = pygame.image.load(f'tank{i}.png')
        screen1.blit(tank1, (x, y))


def draw_tankR(x, y, width, heigth, direction):
    tank1 = pygame.image.load('img/tank1.png')
    tankR = pygame.transform.rotate(tank1, -90)
    screen1.blit(tankR, (x, y))


def draw_tankL(x, y, width, heigth, direction):
    tank1 = pygame.image.load('img/tank1.png')
    tankL = pygame.transform.rotate(tank1, 90)
    screen1.blit(tankL, (x, y))


def draw_tankU(x, y, width, heigth, direction):
    tank1 = pygame.image.load('img/tank1.png')
    tankL = pygame.transform.rotate(tank1, 0)
    screen1.blit(tankL, (x, y))


def draw_tankD(x, y, width, heigth, direction):
    tank1 = pygame.image.load('img/tank1.png')
    tankL = pygame.transform.rotate(tank1, 180)
    screen1.blit(tankL, (x, y))


def draw_tank2(x, y, width, heigth, direction):
    for i in range(2):
        tank1 = pygame.image.load(f'tank{i}.png')
        screen1.blit(tank1, (x, y))


def draw_tankR2(x, y, width, heigth, direction):
    tank1 = pygame.image.load('img/tank2.png')
    tankR = pygame.transform.rotate(tank1, -90)
    screen1.blit(tankR, (x, y))


def draw_tankL2(x, y, width, heigth, direction):
    tank1 = pygame.image.load('img/tank2.png')
    tankL = pygame.transform.rotate(tank1, 90)
    screen1.blit(tankL, (x, y))


def draw_tankU2(x, y, width, heigth, direction):
    tank1 = pygame.image.load('img/tank2.png')
    tankL = pygame.transform.rotate(tank1, 0)
    screen1.blit(tankL, (x, y))


def draw_tankD2(x, y, width, heigth, direction):
    tank1 = pygame.image.load('img/tank2.png')
    tankL = pygame.transform.rotate(tank1, 180)
    screen1.blit(tankL, (x, y))


def draw_bullet(owner, x, y, width, height, direction):
    bullet = pygame.image.load('img/bullet.png')
    screen1.blit(bullet, (x, y))


def draw_bullet1(owner, x, y, width, height, direction):
    bullet = pygame.image.load('img/bullet.png')
    bullet1 = pygame.transform.rotate(bullet, 90)
    screen1.blit(bullet1, (x, y))


def draw_bullet2(owner, x, y, width, height, direction):
    bullet = pygame.image.load('img/bullet2.png')
    screen1.blit(bullet, (x, y))


def draw_bullet12(owner, x, y, width, height, direction):
    bullet = pygame.image.load('img/bullet2.png')
    bullet1 = pygame.transform.rotate(bullet, 90)
    screen1.blit(bullet1, (x, y))


def playsound1(sound):
    pygame.mixer.init()
    sound = pygame.mixer.Sound('sounds/' + sound)
    sound.play()


client = TankRpcClient()


def game_over1():
    client.response = 0
    client.connection.close()
    over = True
    while over:
        screen1.blit(gameover1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    over = False  # exit game
                if event.key == pygame.K_r:
                    multiplayerai()

        pygame.display.update()


def game_over2():
    room = 6
    client.response = 0
    client.connection.close()
    over = True
    while over:
        screen1.blit(gameover1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    over = False  # exit game
                if event.key == pygame.K_r:
                    multiplayer()

        pygame.display.update()


UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'

MOVE_KEYS = {
    pygame.K_w: UP,
    pygame.K_s: DOWN,
    pygame.K_a: LEFT,
    pygame.K_d: RIGHT
}


def multiplayerai():
    shoot = False
    moveRight = True
    moveLeft = False
    moveUp = False
    moveDown = False
    mainloop = True
    client = TankRpcClient()
    client.check_server_status()
    client.obtain_tocken('room-7')
    event_client = TankConsumerClient('room-7')
    event_client.start()

    while mainloop:
        screen1.blit(bg1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                mainloop = False
                client.channel.stop_consuming()
                client.connection.close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False  # exit game
                    client.channel.stop_consuming()
                    client.connection.close()

        if moveRight:
            client.turn_tank(client.token, MOVE_KEYS[pygame.K_d])
        if moveLeft:
            client.turn_tank(client.token, MOVE_KEYS[pygame.K_a])
        if moveUp:
            client.turn_tank(client.token, MOVE_KEYS[pygame.K_w])
        if moveDown:
            client.turn_tank(client.token, MOVE_KEYS[pygame.K_s])

        if shoot:
            client.shoot(client.token)

        try:
            tanks = event_client.response['gameField']['tanks']

            for tank in tanks:
                tank_id = tank['id']
                tank_x = tank['x']
                tank_y = tank['y']
                tank_width = tank['width']
                tank_height = tank['height']
                tank_direction = tank['direction']
                tank_health = tank['health']
                tank_score = tank['score']

                if tank_id == client.tank_id:
                    if tank_direction == 'RIGHT':
                        draw_tankR(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'LEFT':
                        draw_tankL(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'UP':
                        draw_tankU(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'DOWN':
                        draw_tankD(tank_x, tank_y, tank_width, tank_height, tank_direction)
                else:
                    if tank_direction == 'RIGHT':
                        draw_tankR2(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'LEFT':
                        draw_tankL2(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'UP':
                        draw_tankU2(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'DOWN':
                        draw_tankD2(tank_x, tank_y, tank_width, tank_height, tank_direction)

            bullets = event_client.response['gameField']['bullets']
            # if bullets:
            #     playsound1('344310__musiclegends__laser-shoot.wav')
            for bullet in bullets:
                bullet_owner = bullet['owner']
                bullet_x = bullet['x']
                bullet_y = bullet['y']
                bullet_width = bullet['width']
                bullet_height = bullet['height']
                bullet_direction = bullet['direction']
                if bullet_owner == client.tank_id:
                    if bullet_direction == 'UP' or bullet_direction == 'DOWN':
                        draw_bullet(client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)
                    if bullet_direction == 'LEFT' or bullet_direction == 'RIGHT':
                        draw_bullet1(client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)
                else:
                    if bullet_direction == 'UP' or bullet_direction == 'DOWN':
                        draw_bullet2(client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)
                    if bullet_direction == 'LEFT' or bullet_direction == 'RIGHT':
                        draw_bullet12(client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)

            remainingTime = event_client.response['remainingTime']
            text = font1.render('Remaining Time: {}'.format(remainingTime), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (320, 15)
            screen1.blit(text, textRect)
            if remainingTime == 110:
                shoot = True
            if remainingTime == 100:
                moveUp = True
                shoot = True
                moveRight = False
            if remainingTime == 90:
                moveUp = False
                moveRight = False
                moveLeft = True
            if remainingTime == 80:
                moveUp = False
                moveRight = False
                moveLeft = False
                moveDown = True
            if remainingTime == 70:
                moveDown = False
                moveRight = True
            if remainingTime == 60:
                moveRight = False
                moveUp = True
            if remainingTime == 50:
                moveUp = False
                moveLeft = True
            if remainingTime == 40:
                moveLeft = False
                moveDown = True
            if remainingTime == 30:
                moveDown = False
                moveRight = True
            if remainingTime == 20:
                moveRight = False
                moveUp = True
            if remainingTime == 10:
                moveUp = False
                moveDown = True
            if remainingTime == 0:
                game_over1()
            hit = event_client.response['hits']
            if hit:
                playsound1('138481__justinvoke__bullet-blood-4.wav')
            winner = event_client.response['winners']
            if winner:
                game_over1()
            kicked = event_client.response['kicked']
            kickedme = kicked['tankId']

            # if kicked:
            #     game_over()
            loser = event_client.response['losers']
            # if loser:
            #     game_over()
            for tank in tanks:
                tank_id = tank['id']
                if tank_id == client.tank_id:
                    tank_x1 = tank['x']
                    tank_y1 = tank['y']
                    tank_direction1 = tank['direction']
                else:
                    tank_x2 = tank['x']
                    tank_y2 = tank['y']
                    tank_direction2 = tank['direction']

            if tank_direction1 == tank_direction2:
                shoot = True
                print('sadasffs')

        except:
            pass

        g = len(tanks) - 1
        f = g
        t = 0
        try:

            for tank in tanks:
                if client.tank_id == tank['id']:
                    text = font1.render("tankid: " + tank['id'] + "           " + "health: " + str(
                        tank['health']) + "               " + "score: " + str(tank['score']), 1, (255, 0, 0))
                    textRect = text.get_rect(center=(640, 50))
                    screen1.blit(text, textRect)

                else:
                    text = font1.render("tankid: " +
                                        tank['id'] + "           " + "health: " + str(
                        tank['health']) + "               " + "score: " + str(tank['score']), 1,
                                        (0, 0, 0))
                    textRect = text.get_rect(center=(640, 80 + (10 * t)))
                    screen1.blit(text, textRect)
                    t += 1
                    if f == 0:
                        t = 0
                        f = g
                    f -= 1
        except:
            pass
        pygame.display.update()
        pygame.display.flip()


import json
from operator import itemgetter, attrgetter, methodcaller
from time import sleep
import uuid
import pygame
from threading import Thread
import pika

IP = '34.254.177.17'
PORT = 5672
VHOST = 'dar-tanks'
USER = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()
screen2 = pygame.display.set_mode((800, 600))
bg2 = pygame.image.load('img/bg.png')
font2 = pygame.font.SysFont(None, 16)
gameover2 = pygame.image.load('img/gameover.png')


class TankRpcClient():

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VHOST,
                credentials=pika.PlainCredentials(
                    username=USER,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True
                                           )
        self.callback_queue = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=self.callback_queue
        )

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events(time_limit=1)

    def check_server_status(self):
        self.call('tank.request.healthcheck')
        return self.response['status'] == '200'

    def obtain_tocken(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def shoot(self, token):
        message = {
            'token': token
        }
        self.call('tank.request.fire', message)


class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VHOST,
                credentials=pika.PlainCredentials(
                    username=USER,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True
                                           )
        event_listener = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=event_listener,
            routing_key='event.state.' + room_id
        )
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print(self.response)

    def run(self):
        self.channel.start_consuming()


UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'

MOVE_KEYS = {
    pygame.K_w: UP,
    pygame.K_s: DOWN,
    pygame.K_a: LEFT,
    pygame.K_d: RIGHT
}


def multiplayer():
    global tanks
    # print('input room')
    # room = input()
    mainloop = True
    client = TankRpcClient()
    client.check_server_status()
    client.obtain_tocken('room-5')
    event_client = TankConsumerClient('room-5')
    event_client.start()
    m = 15
    while mainloop:
        screen2.blit(bg2, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                mainloop = False
                client.channel.stop_consuming()
                client.connection.close()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False  # exit game
                    client.channel.stop_consuming()
                    client.connection.close()

                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token, MOVE_KEYS[event.key])
                if event.key == pygame.K_SPACE:
                    client.shoot(client.token)
                    playsound1('344310__musiclegends__laser-shoot.wav')
        try:
            tanks = event_client.response['gameField']['tanks']

            for tank in tanks:
                tank_id = tank['id']
                tank_x = tank['x']
                tank_y = tank['y']
                tank_width = tank['width']
                tank_height = tank['height']
                tank_direction = tank['direction']
                tank_health = tank['health']
                tank_score = tank['score']

                if tank_id == client.tank_id:
                    if tank_direction == 'RIGHT':
                        draw_tankR(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'LEFT':
                        draw_tankL(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'UP':
                        draw_tankU(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'DOWN':
                        draw_tankD(tank_x, tank_y, tank_width, tank_height, tank_direction)
                else:
                    if tank_direction == 'RIGHT':
                        draw_tankR2(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'LEFT':
                        draw_tankL2(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'UP':
                        draw_tankU2(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    if tank_direction == 'DOWN':
                        draw_tankD2(tank_x, tank_y, tank_width, tank_height, tank_direction)

            bullets = event_client.response['gameField']['bullets']
            # if bullets:
            #     playsound1('344310__musiclegends__laser-shoot.wav')
            for bullet in bullets:
                bullet_owner = bullet['owner']
                bullet_x = bullet['x']
                bullet_y = bullet['y']
                bullet_width = bullet['width']
                bullet_height = bullet['height']
                bullet_direction = bullet['direction']
                if bullet_owner == client.tank_id:
                    if bullet_direction == 'UP' or bullet_direction == 'DOWN':
                        draw_bullet(client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)
                    if bullet_direction == 'LEFT' or bullet_direction == 'RIGHT':
                        draw_bullet1(client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)
                else:
                    if bullet_direction == 'UP' or bullet_direction == 'DOWN':
                        draw_bullet2(client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)
                    if bullet_direction == 'LEFT' or bullet_direction == 'RIGHT':
                        draw_bullet12(client.tank_id, bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction)

            remainingTime = event_client.response['remainingTime']
            text = font2.render('Remaining Time: {}'.format(remainingTime), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (320, 15)
            screen2.blit(text, textRect)
            if remainingTime == 0:
                game_over2()
            hit = event_client.response['hits']
            if hit:
                playsound1('138481__justinvoke__bullet-blood-4.wav')
            winner = event_client.response['winners']
            if winner:
                game_over2()
            kicked = event_client.response['kicked']
            kickedme = kicked['tankId']

            # if kicked:
            #     game_over()
            loser = event_client.response['losers']
            # if loser:
            #     game_over()

        except:
            pass

        g = len(tanks) - 1
        f = g
        t = 0
        try:

            for tank in tanks:
                if client.tank_id == tank['id']:
                    text = font2.render("tankid: " + tank['id'] + "           " + "health: " + str(
                        tank['health']) + "               " + "score: " + str(tank['score']), 1, (255, 0, 0))
                    textRect = text.get_rect(center=(640, 50))
                    screen2.blit(text, textRect)

                else:
                    text = font2.render("tankid: " +
                                        tank['id'] + "           " + "health: " + str(
                        tank['health']) + "               " + "score: " + str(tank['score']), 1,
                                        (0, 0, 0))
                    textRect = text.get_rect(center=(640, 80 + (10 * t)))
                    screen2.blit(text, textRect)
                    t += 1
                    if f == 0:
                        t = 0
                        f = g
                    f -= 1
        except:
            pass
        pygame.display.update()
        pygame.display.flip()


menu()

