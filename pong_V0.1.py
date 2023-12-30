import pygame
pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 700 , 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG BY Lakshya")


font = pygame.font.SysFont("comicsans",50)
FPS = 60
winning_score = 5

paddle_width, paddle_height = 20, 100
ball_radius = 7
# color

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
board_color = (0,230,118)
yellow = (255,234,0)
orange = (230,74,25)
liblue = (41, 121, 255)

old_blue = (33, 150, 243)

class Paddle:
    Color = orange
    vel = 5

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x 
        self.y = self.original_y = y 
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win,self.Color,(self.x, self.y, self.width, self.height))    
        
    def move(self, up = True):
        if up:
            self.y -= self.vel

        else:
            self.y += self.vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y        

class Ball:
    ball_v= 5
    color = green

    def __init__(self, x, y , radius):
        self.x = self.original_x = x 
        self.y = self.original_y =  y 
        self.radius = radius
        self.x_vel = self.ball_v 
        self.y_vel = 0


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y),self.radius)    

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel   

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0 
        self.x_vel *= -1

def hit_sound():
        pygame.mixer.music.load("hit.mp3")
        pygame.mixer.music.play()
        


def draw(win, paddles, ball , l_score ,r_score):
    win.fill(black)

    left_score_text = font.render(f'{l_score}', 1 , yellow)
    right_score_text = font.render(f'{r_score}', 1 , yellow)
    win.blit(left_score_text,(WIDTH//4 - left_score_text.get_width()//2,20))
    win.blit(right_score_text,(WIDTH*(3/4) - right_score_text.get_width()//2,20))
    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 ==1 :
            continue
        pygame.draw.rect(win, orange,(WIDTH//2-5, i, 10,HEIGHT//20))    
    
    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y +ball.radius >=HEIGHT:
        ball.y_vel *= -1
        hit_sound()

    elif ball.y -ball.radius <=0:
        ball.y_vel *= -1
        hit_sound()
        
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y  
                reduction_factor = (left_paddle.height/2)/ball.ball_v
                y_vel = difference_in_y/reduction_factor
                ball.y_vel = y_vel*-1
                hit_sound()
                

    else:
        if ball.y >= right_paddle.y and ball.y <=right_paddle.y + paddle_height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *=-1
                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y  
                reduction_factor = (right_paddle.height/2)/ball.ball_v
                y_vel = difference_in_y/reduction_factor
                ball.y_vel = y_vel *-1
                hit_sound()
               

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y-left_paddle.vel>=0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.vel+left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_KP_8] and right_paddle.y-right_paddle.vel>=0:
        right_paddle.move(up=True)
    if keys[pygame.K_KP_5] and right_paddle.y + right_paddle.vel+right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def home_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        window.fill(black)
        screen_text = '''PONG'''
        text = font.render(screen_text,1 ,yellow )
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 -50))
        screen_text = 'Press Enter To Play'
        text = font.render(screen_text,1 ,blue)
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 ))
     
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
               

    pygame.quit()
    quit()                 
def win_screen(win_text):
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        window.fill(black)
        
        text = font.render(win_text,1 ,yellow )
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 -50))
        screen_text = 'Press Enter To Play Again'
        text = font.render(screen_text,1 ,blue)
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
    pygame.quit()
    quit()                 

        

def gameloop():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10,HEIGHT//2-paddle_height//2,paddle_width, paddle_height)
    right_paddle = Paddle(WIDTH-10- paddle_width,HEIGHT//2-paddle_height//2,paddle_width, paddle_height)
    
    ball = Ball(WIDTH//2, HEIGHT//2 ,ball_radius)

    l_score = 0
    r_score = 0

    while run:
        clock.tick(FPS)
        draw(window,[left_paddle, right_paddle],ball, l_score ,r_score)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)    
    
        ball.move()    
        handle_collision(ball, left_paddle,right_paddle)

        if ball.x < 0:
            r_score +=1
            ball.reset()
        elif ball.x > WIDTH:
            l_score +=1
            ball.reset()  


        win = False
        if l_score >= winning_score:
            win = True
            win_text = "Left Player Won!"
            
        elif r_score >= winning_score:
            win = True
            win_text = "Left Player Won!"
            

        if win:
            win_screen(win_text)
           
    pygame.quit()
if __name__ == '__main__': 
    home_screen()
            
    



