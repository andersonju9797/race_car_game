import pygame
import time
import random

display_width = 800
display_height = 600

car_speed = 25
car_width = 50
car_height = 100

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
bright_red = (200, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255)

pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Race Car')
clock = pygame.time.Clock()

# pixel_array = pygame.PixelArray(game_display)

car_img = pygame.image.load('racecar.png')
car_icon = pygame.image.load('racecar_icon.png')
pygame.display.set_icon(car_icon)

large_text = pygame.font.SysFont(None, 110)
small_text = pygame.font.SysFont(None, 48)
tiny_text = pygame.font.SysFont(None, 25)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, ic,(x,y,w,h))

    textSurf, textRect = text_objects(msg, small_text)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(textSurf, textRect)

def score(count):
    text = tiny_text.render('Score: ' + str(count), True, black)
    instructions_text = tiny_text.render('Use left and right arrow keys to move', True, black)
    pause_text = tiny_text.render('Press \'p\' to pause', True, black)
    quit_text = tiny_text.render('Press \'q\' to quit', True, black)
    game_display.blit(text, (display_width/2 - 40, display_height/2 - 50))
    game_display.blit(instructions_text, (0, 0))
    game_display.blit(pause_text, (0, 20))
    game_display.blit(quit_text, (0, 40))

def thing(thing_x, thing_y, thing_width, thing_height, color):
    pygame.draw.rect(game_display, color, [thing_x, thing_y, thing_width, thing_height])

def car(x, y):
    game_display.blit(car_img, (x, y))

def crash():
    display_message('You Crashed!')
    time.sleep(1)

    pygame.draw.rect(game_display, white, (0,0,500,50))
    instructions_text = tiny_text.render('Press any key to retry...', True, black)
    return_text = tiny_text.render('Press backspace to return to menu', True, black)
    quit_text = tiny_text.render('Press \'q\' to quit', True, black)
    game_display.blit(instructions_text, (0, 0))
    game_display.blit(return_text, (0, 20))
    game_display.blit(quit_text, (0, 40))

    pygame.display.update()

    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game()
                elif event.key == pygame.K_BACKSPACE:
                    intro_screen()
                else:
                    game_loop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()

# def is_crashed(x, y, thing_x, thing_y):

def display_message(text):
    text_surface, text_rectangle = text_objects(text, large_text)
    text_rectangle.center = (display_width/2, display_height/2)
    game_display.blit(text_surface, text_rectangle)
    pygame.display.update()

def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def intro_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game()
                if event.key == pygame.K_RETURN:
                    game_loop()
        game_display.fill(white)
        text_surface, text_rectangle = text_objects('Race Car', large_text)
        text_rectangle.center = (display_width / 2, display_height / 2)
        game_display.blit(text_surface, text_rectangle)

        instructions_text = tiny_text.render('Use left and right arrow keys to move', True, black)
        pause_text = tiny_text.render('Press \'p\' to pause', True, black)
        quit_text = tiny_text.render('Press \'q\' to quit', True, black)
        game_display.blit(instructions_text, (0, 0))
        game_display.blit(pause_text, (0, 20))
        game_display.blit(quit_text, (0, 40))

        button('start!', display_width / 2 - 100, display_height / 2 + 150, 200, 100, green, bright_green, game_loop)

        pygame.display.update()
        clock.tick(60)

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game()
                elif event.key == pygame.K_BACKSPACE:
                    intro_screen()
                elif event.key == pygame.K_p:
                    paused = False

        game_display.fill(white)
        text_surface, text_rectangle = text_objects('Paused', large_text)
        text_rectangle.center = (display_width / 2, display_height / 2)
        game_display.blit(text_surface, text_rectangle)

        instructions_text = tiny_text.render('Use left and right arrow keys to move', True, black)
        return_text = tiny_text.render('Press backspace to return to menu', True, black)
        unpause_text = tiny_text.render('Press \'p\' to unpause', True, black)
        quit_text = tiny_text.render('Press \'q\' to quit', True, black)
        game_display.blit(instructions_text, (0, 0))
        game_display.blit(return_text, (0, 20))
        game_display.blit(unpause_text, (0, 40))
        game_display.blit(quit_text, (0, 60))

        pygame.display.update()
        clock.tick(60)

def game_loop():
    x = display_width * 0.45
    y = display_height * 0.8
    speed = car_speed

    left_pressed = False
    right_pressed = False
    a_pressed = False
    d_pressed = False

    thing_width = random.randrange(100, 300)
    thing_height = random.randrange(100, 300)
    thing_start_x = random.randrange(0, display_width - thing_width)
    thing_start_y = -600
    thing_speed = 20

    things_dodged = 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_pressed = True
                elif event.key == pygame.K_RIGHT:
                    right_pressed = True
                elif event.key == pygame.K_a:
                    a_pressed = True
                elif event.key == pygame.K_d:
                    d_pressed = True
                elif event.key == pygame.K_q:
                    quit_game()
                elif event.key == pygame.K_p:
                    pause()
                    a_pressed = False
                    d_pressed = False
                    left_pressed = False
                    right_pressed = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_pressed = False
                elif event.key == pygame.K_RIGHT:
                    right_pressed = False
                elif event.key == pygame.K_a:
                    a_pressed = False
                elif event.key == pygame.K_d:
                    d_pressed = False

            print(event)

        if a_pressed or left_pressed:
            moving_left = True
        else:
            moving_left = False

        if d_pressed or right_pressed:
            moving_right = True
        else:
            moving_right = False

        if moving_left:
            x += -1 * speed
        if moving_right:
            x += speed

        game_display.fill(white)

        thing(thing_start_x, thing_start_y, thing_width, thing_height, block_color)
        thing_start_y += thing_speed
        car(x, y)
        score(things_dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_start_y > display_height:
            thing_width = random.randrange(100, 300)
            thing_height = random.randrange(100, 300)
            thing_start_y = 0 - thing_height
            thing_start_x = random.randrange(0, display_width - thing_width)
            things_dodged += 1
            thing_speed += 0.2
            speed += 0.2


        if x + car_width > thing_start_x and x < thing_start_x + thing_width - 5:
            if y < thing_start_y + thing_height and y + car_height > thing_start_y - 20:
                crash()

        pygame.display.update()
        clock.tick(60) # fps

def quit_game():
    pygame.quit()
    quit()

intro_screen()
