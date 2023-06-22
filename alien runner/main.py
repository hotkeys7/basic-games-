import pygame
from sys import exit
pygame.init()
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk = pygame.image.load("player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("player_walk_2.png").convert_alpha()
        self.player_walker = [player_walk, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("jump.png").convert_alpha()

        self.image = self.player_walker[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 285))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("jump.mp3")
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 370:
            self.rect.bottom = 370

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(player_walker):
                self.player_index = 0
            self.image = self.player_walker[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly1 = pygame.image.load("Fly1.png").convert_alpha()
            fly2 = pygame.image.load("Fly2.png").convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 210
        else:
            snail1 = pygame.image.load("snail1.png").convert_alpha()
            snail2 = pygame.image.load("snail2.png").convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 335

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
def display_Score():
    current_time = int((pygame.time.get_ticks() / 1000) - start_time)
    score_surf = test_font.render(f"{current_time}", False, "Pink")
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.y == 335:
                screen.blit(snail, obstacle_rect)
            else:
                screen.blit(fly, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, True):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    global player_surf, player_index

    if play_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walker):
            player_index =0
        player_surf = player_walker[int(player_index)]

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("                   R                U                   N")
clock = pygame.time.Clock()
test_font = pygame.font.Font("UnifrakturMaguntia-Regular.ttf", 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("music.wav")
bg_music.play(loops = -1)


player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

sky = pygame.image.load("sky-with-hills.png").convert()
ground = pygame.image.load("ground.png").convert()


snail1 = pygame.image.load("snail1.png").convert_alpha()
snail2 = pygame.image.load("snail2.png").convert_alpha()
snail_frames = [snail1, snail2]
snail_index = 0
snail = snail_frames[snail_index]

fly1 = pygame.image.load("Fly1.png").convert_alpha()
fly2 = pygame.image.load("Fly2.png").convert_alpha()
fly_frames = [fly1, fly2]
fly_index = 0
fly = fly_frames[fly_index]

obstacle_rect_list = []

player_walk = pygame.image.load("player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("player_walk_2.png").convert_alpha()
player_walker = [player_walk, player_walk2]
player_index = 0
player_jump = pygame.image.load("jump.png").convert_alpha()


player_surf = player_walker[player_index]
play_rect = player_surf.get_rect(topleft = (80, 285))
player_gravity = -23

play_stand = pygame.image.load("player_stand.png").convert_alpha()
play_stand = pygame.transform.rotozoom(play_stand, 0, 2)
play_stand_rect = play_stand.get_rect(center = (400, 200))

game_name = test_font.render("Alien Runner", False, "Pink")
game_name_rect = game_name.get_rect(center = (400, 50))

game_message = test_font.render("Press space to run", False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 320))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and play_rect.bottom >= 300:
                    player_gravity = -23

            if event.type == pygame.MOUSEMOTION:
                if play_rect.collidepoint(event.pos):
                    print("PLAYYERRR")

            if event.type == pygame.MOUSEBUTTONDOWN and play_rect.bottom >= 300:
                player_gravity = -23

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 700
                start_time = int((pygame.time.get_ticks() / 1000) - start_time)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail","snail"])))

            if event.type == snail_timer:
                if snail_index == 0:
                    snail_index = 1
                    snail = snail_frames[snail_index]
                else:
                    snail_index = 0
                    snail = snail_frames[snail_index]

            if event.type == fly_timer:
                if fly_index == 0:
                    fly_index = 1
                    fly = fly_frames[fly_index]
                else:
                    fly_index = 0
                    fly = fly_frames[fly_index]



    if game_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 370))

        pygame.draw.line(screen, "Gold", (0, 0), pygame.mouse.get_pos(), 10)

        score = display_Score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(play_stand, play_stand_rect)
        obstacle_rect_list.clear()
        play_rect.topleft = (80, 285)
        player_gravity = 0

        score_message = test_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    mouse_pos = pygame.mouse.get_pos()
    if play_rect.collidepoint((mouse_pos)):
        print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)