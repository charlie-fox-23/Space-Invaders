from re import X
import pygame
from pygame.constants import QUIT

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Space Invaders!")

#colors

white = (255,255,255)
green = (0,255,0)

clock = pygame.time.Clock()

class Spaceship:
  def __init__(self,x,y,image_path,scale_size):
    original_image = pygame.image.load(image_path)
    self.image = pygame.transform.scale(original_image,scale_size)
    self.x = x
    self.y = y
    self.speed = 5
  def draw(self):
    screen.blit(self.image,(self.x, self.y))
  def move_left(self):
    self.x -=self.speed
    if self.x <0:
      self.x = 0
  def move_right(self):
    self.x +=self.speed
    if self.x >screen_width-self.image.get_width():
      self.x = screen_width-self.image.get_width()

class Bullet:
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.speed = 10
    self.fired = False
  def draw(self):
    if self.fired:
      pygame.draw.rect(screen,green,(self.x,self.y,2,10))
  def fire(self,x,y):
    self.fired = True
    self.x = x
    self.y = y
  def move(self):
    if self.fired:
      self.y-=self.speed
      if self.y < 0 :
        self.fired = False
#we need to scale the images
spaceship_scale_size = (50,50)
enemy_scale_size = (50,50)

spaceship = Spaceship(screen_width//2,screen_height-69,"spaceship.png",spaceship_scale_size)
bullet = Bullet(0,0)

class Enemy:
  def __init__(self,x,y,image_path,scale_size):
    original_image = pygame.image.load(image_path)
    self.image = pygame.transform.scale(original_image,scale_size)
    self.x = x
    self.y = y
  def draw(self):
    screen.blit(self.image,(self.x, self.y))

number_of_enemies = 5
enemies = []
enemy_image_path = "enemy.png"

for i in range(number_of_enemies):
  enemy_x = i*(screen_width//number_of_enemies)+(screen_width//number_of_enemies-enemy_scale_size[0])//2
  enemies.append(Enemy(enemy_x,50,"enemy.png",enemy_scale_size))

def draw_enemies(enemies):
  for enemy in enemies :
    enemy.draw()

def is_colision(bullet,enemy):
  if bullet.y < enemy.y + enemy.image.get_height():
    if bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width() :
      return True
  return False

running = True
while running :
  screen.fill((0,0,0))
  for event in pygame.event.get():
    if event.type ==pygame.QUIT:
      running =  False

  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    spaceship.move_left()
  if keys[pygame.K_RIGHT]:
    spaceship.move_right()
  if keys[pygame.K_SPACE] and not bullet.fired :
    bullet.fire(spaceship.x + spaceship.image.get_width()//2,spaceship.y)

  bullet.move()
  bullet.draw()

  spaceship.draw()

  for enemy in enemies[:]:
    if bullet.fired and is_colision(bullet,enemy):
      bullet.fired = False
      enemies.remove(enemy)

  draw_enemies(enemies)
  pygame.display.update()
  clock.tick(30)
pygame.quit()