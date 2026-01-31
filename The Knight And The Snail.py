
import random

import pygame
from sys import exit
from random import choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('UltimatePygameIntro-main/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('UltimatePygameIntro-main/graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('UltimatePygameIntro-main/graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom =(80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('UltimatePygameIntro-main/audio/jump.mp3')
        self.jump_sound.set_volume(0.1)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 :
            self.gravity = -12
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300


    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >=len(self.player_walk):self.player_index =0
            self.image = self.player_walk[int(self.player_index)]



    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type =='fly':
            fly_1 = pygame.image.load('UltimatePygameIntro-main/graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('UltimatePygameIntro-main/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('UltimatePygameIntro-main/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('UltimatePygameIntro-main/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index =0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index =0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - int(start_time / 100)
    score_surf = text_font.render( f'Score: {current_time}' ,False,(64,64,64))
    score_rect = score_surf.get_rect(center =(400,50) )
    screen.blit(score_surf, score_rect)
    return current_time
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:screen.blit(snail_surf,obstacle_rect)
            else:screen.blit(fly_surf,obstacle_rect)

        obstacle_list =[obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []
def collision(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles :
            if player.colliderect(obstacle_rect): return False
    return True
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else : return True
def player_animation():
    global player_surf,player_index
    if player_rec.bottom < 300:
        player_surf = player_jump
    else :
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]



pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()
text_font = pygame.font.Font('UltimatePygameIntro-main/font/Pixeltype.ttf', 70)
game_active = False
start_time = 0
score = 0
background_music = pygame.mixer.Sound('UltimatePygameIntro-main/audio/music.wav')
background_music.set_volume(0.1)
background_music.play(loops= -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


Sky_screen = pygame.image.load('UltimatePygameIntro-main/graphics/Sky.png').convert()
ground_screen = pygame.image.load('UltimatePygameIntro-main/graphics/ground.png').convert()



#text
text_screen = text_font.render('My Game',False,(101, 136, 166))
text_rect = text_screen.get_rect(center = (400,100))
menu_text_screen = text_font.render('The Knight And The Snail',False, (150, 199, 255) )
menu_text_rect = menu_text_screen.get_rect(center =(400,70))
menu_instruction_screen = text_font.render('Press Space to start',False, (65, 92, 125) )
menu_instruction_rect = menu_text_screen.get_rect(center =(430,330))
#obstacles
#snail
snail_frame_1 = pygame.image.load('UltimatePygameIntro-main/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('UltimatePygameIntro-main/graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
#fly
fly_frame_1 = pygame.image.load('UltimatePygameIntro-main/graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('UltimatePygameIntro-main/graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacles_rect_list = []
#player
player_walk_1 = pygame.image.load('UltimatePygameIntro-main/graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('UltimatePygameIntro-main/graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index =0
player_jump = pygame.image.load('UltimatePygameIntro-main/graphics/Player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rec = player_surf.get_rect(midbottom =(80, 300))
player_gravity = -10
#intro screen
player_stand = pygame.image.load('UltimatePygameIntro-main/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2 )
player_stand_rect = player_stand.get_rect(center =(400,200))
#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        if game_active :
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rec.collidepoint(event.pos) : player_gravity = -12

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE and player_rec.bottom == 300:
                    player_gravity = -12
        else :
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE : game_active = True
            start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail'])))
              #   if randint(0,2):
              # e:      obstacles_rect_list.append(snail_surf.get_rect(midbottom =(randint(900,1100),300)))
              #   els
              #       obstacles_rect_list.append(fly_surf.get_rect(midbottom =(randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0 : snail_frame_index = 1
                else : snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0 : fly_frame_index = 1
                else : fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]



    if game_active :
        screen.blit(Sky_screen,(0, 0))
        screen.blit(ground_screen,(0, 300))
        pygame.draw.rect(screen, '#8ED1A2',text_rect)
        screen.blit(text_screen,text_rect)
        score = display_score()
        mouse_pos = pygame.mouse.get_pos()

        # player_gravity += 0.5
        # player_rec.y += player_gravity
        # if player_rec.bottom >= 300: player_rec.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rec)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        display_score()
        #obstical movement
        #obstacles_rect_list = obstacle_movement(obstacles_rect_list)
        #collision
        game_active = collision_sprite()
        #game_active = collision(player_rec, obstacles_rect_list)


    else :
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacles_rect_list = []
        score_message = text_font.render(f'Your Score: {score}',False,(150, 199, 255))
        score_message_rect =score_message.get_rect(center =(630,200))
        if score != 0 :screen.blit(score_message, score_message_rect)
        screen.blit(menu_text_screen, menu_text_rect)
        screen.blit(menu_instruction_screen, menu_instruction_rect)

    pygame.display.update()
    clock.tick(60)




