#Insane Space Rescue (Modified Mail Pilot)
#Silviu Popovici
#5/12/2015

#extended original game to include:
#An AI system - an alien ship that follows your movements and actively tries to shoot you
#A 2-player mode
#A stand alone windows application

#credit for sounds and art - opengameart.org

    
import pygame, random, sys
pygame.init()

#Global variable player2 that tells game whether it's 2 player mode or not
player2 = 0

screen = pygame.display.set_mode((640, 480))

#The "homing" alien ship that uses basic ai to "follow" the players movements and try to shoot the player
class NPCPlane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("homing.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.dx = 0
        self.rect.centerx = 300
        self.rect.centery = 50

              
    def update(self,value1):
         
        self.dx = value1
        

        self.rect.centerx += self.dx
        
#The lasers that enemy ship fires
class EnemyShot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("shot3.gif").convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = 1200
        self.rect.centery = 1200
        


        
        if not pygame.mixer:
            print "problem with sound"
        else:
            pygame.mixer.init()
            self.sndShot = pygame.mixer.Sound("enemy.ogg")

    def update(self, value):
        self.dy = value
        self.rect.centery += self.dy




#A larger laser 
class LaserShot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("shot2.gif").convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = 1200
        self.rect.centery = 1200
        self.dy = 12


        
        if not pygame.mixer:
            print "problem with sound"
        else:
            pygame.mixer.init()
            self.sndShot = pygame.mixer.Sound("shot.ogg")

    def update(self):
        self.rect.centery -= self.dy
        
#the standard projectile
class Shot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("shot.gif").convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = 1200
        self.rect.centery = 1200
        self.dy = 15

        
        if not pygame.mixer:
            print "problem with sound"
        else:
            pygame.mixer.init()
            self.sndShot = pygame.mixer.Sound("shot.ogg")

    def update(self):
        self.rect.centery -= self.dy

#player 2's ship
class Plane2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("plane4.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

        if player2 == 1:
            self.rect.centerx = 150
            self.rect.centery = 200
        else:
            self.rect.centerx = 1111111
            self.rect.centery = 2000000            
        
        
    def update(self):
        if player2 == 0:
            self.rect.centerx += 1000
            self.rect.centery += 1000
    


#The main player's ship
class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("plane.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        if not pygame.mixer:
            print "problem with sound"
        else:
            pygame.mixer.init()
            self.sndYay = pygame.mixer.Sound("heal.ogg")
            self.sndThunder = pygame.mixer.Sound("thunder.ogg")
            self.sndEngine = pygame.mixer.Sound("music.ogg")
            self.sndEngine.play(-1)
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, mousey)
        
#The crates the player can pick up              
class Island(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("crate.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dy = 5
    
    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()
            
    def reset(self):
        self.rect.bottom = -50
        #self.rect.top = 0
        self.rect.centerx = random.randrange(0, screen.get_width())

#The aliens that attack the players      
class Cloud(pygame.sprite.Sprite):
    def __init__(self, d):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Cloud.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset(d)

    def update(self,d):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset(d)
    
    def reset(self, x):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10) + x
        self.dx = random.randrange(-2, 2)

#An alternate looking alien
class Cloud2(pygame.sprite.Sprite):
    def __init__(self, d):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Cloud2.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset(d)

    def update(self,d):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset(d)
    
    def reset(self, x):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10) + x
        self.dx = random.randrange(-2, 2)

        
#Space background    
class Ocean(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("space.gif")
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()
        
    def update(self):
        self.rect.bottom += self.dy
        if self.rect.bottom >= 1440:
            self.reset() 
    
    def reset(self):
        self.rect.top = -960

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 1500
        self.score = 0
        self.hits = 0
        self.xtra = 0
        self.player2lives = 1500
        self.font = pygame.font.SysFont("None", 25)
        
    def update(self):
        global player2
        if player2 == 0:
            self.text = "HP: %d, Score: %d, Aliens Destroyed: %d" % (self.lives, self.score, self.hits)
        else:
            self.text = "HP: %d, Score: %d, Aliens Destroyed: %d, Player 2 HP: %d" % (self.lives, self.score, self.hits, self.player2lives)
            
        self.image = self.font.render(self.text, 1, (255, 50, 0))
        self.rect = self.image.get_rect()
    
def game():
    #Variables for shot reload times, difficulty, and sprite creation
    global player2
    medic = 0
    difficulty = 1
    pygame.display.set_caption("Insane Space Rescue")
    harder = 0
    updateShot = 100
    updateShot2 = 100
    updateEnemyShot = 100
    player2updateshot = 100
    shotspeed = 1
    enemyspeed = 15
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    plane = Plane()
    plane2 = NPCPlane()
    plane3 = Plane2()
    island = Island()
    cloud1 = Cloud(difficulty)
    cloud2 = Cloud(difficulty)
    cloud3 = Cloud(difficulty)
    cloud4 = Cloud(difficulty)
    cloud5 = Cloud(difficulty)
    cloud6 = Cloud(difficulty)
    cloud7 = Cloud2(difficulty)
    cloud8 = Cloud2(difficulty)
    ocean = Ocean()
    shot = Shot()
    shot2 = Shot()
    shot3 = Shot()
    shot4 = LaserShot()
    shot5 = LaserShot()
    shot6 = EnemyShot()
    shot7 = EnemyShot()
    shot8 = EnemyShot()
    shot9 = Shot()
    shot10 = Shot()
    shot11 = LaserShot()
    scoreboard = Scoreboard()

    player2Sprites = pygame.sprite.Group(plane3)
    homingSprite = pygame.sprite.Group(plane2)
    shotSprite = pygame.sprite.Group(shot,shot2,shot3,shot4,shot5,shot9,shot10,shot11)
    planeSprites = pygame.sprite.Group(plane)
    friendSprites = pygame.sprite.Group(ocean)
    islandSprite = pygame.sprite.Group(island)
    cloudSprites = pygame.sprite.Group(cloud1, cloud2, cloud3,cloud4,cloud5,cloud6, cloud7, cloud8)
    scoreSprite = pygame.sprite.Group(scoreboard)
    enemyshotsprite = pygame.sprite.Group(shot6,shot7,shot8)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        
        clock.tick(30)
        pygame.mouse.set_visible(False)
        updateShot+=2
        updateShot2 +=2
        player2updateshot +=2
        updateEnemyShot += shotspeed
        key_pressed = pygame.key.get_pressed()
        
        #Handle controls for shooting and player 2 movement
        if pygame.mouse.get_pressed()[0] and updateShot > 60:
                shot.sndShot.play()
                shot.rect.centerx = plane.rect.centerx - 20
                shot.rect.centery = plane.rect.centery + 3 
                shot2.rect.centerx = plane.rect.centerx + 20
                shot2.rect.centery = plane.rect.centery + 3
                shot3.rect.centerx = plane.rect.centerx 
                shot3.rect.centery = plane.rect.centery - 6
                
                updateShot = 0

        if pygame.mouse.get_pressed()[2] and updateShot2 > 60:
                shot.sndShot.play()
                shot4.rect.centerx = plane.rect.centerx - 28
                shot4.rect.centery = plane.rect.centery + 5 
                shot5.rect.centerx = plane.rect.centerx + 28
                shot5.rect.centery = plane.rect.centery + 5
                            
                updateShot2 = 0

        if key_pressed[pygame.K_SPACE] and player2updateshot > 60:
                shot9.rect.centerx = plane3.rect.centerx - 20
                shot9.rect.centery = plane3.rect.centery + 3 
                shot10.rect.centerx = plane3.rect.centerx + 20
                shot10.rect.centery = plane3.rect.centery + 3
                shot11.rect.centerx = plane3.rect.centerx 
                shot11.rect.centery = plane3.rect.centery - 6
                
                player2updateshot = 0

        # Player 2 movement controls    
        if key_pressed[pygame.K_w] and plane3.rect.centery > 20 and player2 == 1:
                   plane3.rect.centery -= 12
        if key_pressed[pygame.K_a] and plane3.rect.centerx > 20 and player2 == 1:
                   plane3.rect.centerx -= 12
        if key_pressed[pygame.K_d] and plane3.rect.centerx < 620 and player2 == 1:
                   plane3.rect.centerx += 12
        if key_pressed[pygame.K_s] and plane3.rect.centery < 460 and player2 == 1:
                   plane3.rect.centery += 12

        #Controls enemy ship firing
        if updateEnemyShot > 100:
            #shot6.sndShot.play()
            shot6.rect.centerx = plane2.rect.centerx - 32
            shot6.rect.centery = plane2.rect.centery + 3 
            shot7.rect.centerx = plane2.rect.centerx + 32
            shot7.rect.centery = plane2.rect.centery + 3
            shot8.rect.centerx = plane2.rect.centerx 
            shot8.rect.centery = plane2.rect.centery - 6
            updateEnemyShot = 0
            
        

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                
            

        #When certain scores are reached make the aliens faster       
        if scoreboard.score > 300 and scoreboard.score <= 600:
            difficulty = 2
        elif scoreboard.score > 600 and scoreboard.score <=900:
            difficulty = 5
        elif scoreboard.score > 900 and scoreboard.score <=1500:
            difficulty = 8
        elif scoreboard.score > 1500 and scoreboard.score <= 1800:
            difficulty = 10
        elif scoreboard.score > 1800 and scoreboard.score <= 2000:
            difficulty = 11
        elif scoreboard.score > 2000 and scoreboard.score <= 2500:
            difficulty = 12
        elif scoreboard.score > 2500 and scoreboard.score <= 4000:
            difficulty = 14
        elif scoreboard.score > 4000 and scoreboard.score <= 5000:
            difficulty = 16
        elif scoreboard.score > 5000:
            difficulty  = 22
            
        
        #check collisions for player 1
        hit = pygame.sprite.spritecollide(shot,cloudSprites, False) or pygame.sprite.spritecollide(shot2,cloudSprites, False) or pygame.sprite.spritecollide(shot3,cloudSprites, False) or pygame.sprite.spritecollide(shot4,cloudSprites, False)or pygame.sprite.spritecollide(shot5,cloudSprites, False)
        if hit:
             for theCloud in hit:
                scoreboard.hits+=1
                scoreboard.score +=20
                theCloud.reset(difficulty)
     
        
        if plane.rect.colliderect(island.rect):
            plane.sndYay.play()
            island.reset()
            scoreboard.score += 500
            scoreboard.lives += 130

        hitClouds = pygame.sprite.spritecollide(plane, cloudSprites, False)
        if hitClouds:
            plane.sndThunder.play()
            scoreboard.lives -= 120
            if scoreboard.lives <= 0:
                diifculty = 0
                keepGoing = False
            for theCloud in hitClouds:
                theCloud.reset(difficulty)

        hit3 = pygame.sprite.spritecollide(shot6,planeSprites, False) or pygame.sprite.spritecollide(shot7,planeSprites, False) or pygame.sprite.spritecollide(shot8,planeSprites, False)
        if hit3:
            plane.sndThunder.play()
            scoreboard.lives -= 25 + difficulty
            if scoreboard.lives <= 0:
                diifculty = 0
                keepGoing = False

        #deal with collisions for player2
        hit4 = pygame.sprite.spritecollide(shot9,cloudSprites, False) or pygame.sprite.spritecollide(shot10,cloudSprites, False) or pygame.sprite.spritecollide(shot11,cloudSprites, False)
        if hit4:
             for theCloud in hit4:
                scoreboard.hits+=1
                scoreboard.score +=20
                theCloud.reset(difficulty)

        if plane3.rect.colliderect(island.rect):
            plane.sndYay.play()
            island.reset()
            scoreboard.score += 500
            scoreboard.player2lives += 130

        hitClouds2 = pygame.sprite.spritecollide(plane3, cloudSprites, False)
        if hitClouds2:
            plane.sndThunder.play()
            scoreboard.player2lives -= 120
            for theCloud in hitClouds2:
                theCloud.reset(difficulty)

        hit5 = pygame.sprite.spritecollide(shot6,player2Sprites, False) or pygame.sprite.spritecollide(shot7,player2Sprites, False) or pygame.sprite.spritecollide(shot8,player2Sprites, False)
        if hit5:
            plane.sndThunder.play()
            scoreboard.player2lives -= 25 + difficulty
     
          
 

        
        #If it's 2 player mode and player 2 dies, player 2 disappears
        if player2 == 1 and scoreboard.player2lives <= 0:
            player2 = 0
            plane3.update()
            
            
        #Update the homing ship's movements
        if plane2.rect.centerx < plane.rect.centerx:
            homingSprite.update(2)
        if plane2.rect.centerx > plane.rect.centerx:
            homingSprite.update(-2)
            

 
        

        #Update and draw all sprites
        enemyshotsprite.update(enemyspeed)
        shotSprite.update()
        planeSprites.update()
        friendSprites.update()
        islandSprite.update()
        cloudSprites.update(difficulty)
        scoreSprite.update()
        player2Sprites.update()

        
        friendSprites.draw(screen)
        islandSprite.draw(screen)
        cloudSprites.draw(screen)
        scoreSprite.draw(screen)
        homingSprite.draw(screen)
        planeSprites.draw(screen)
        shotSprite.draw(screen)
        enemyshotsprite.draw(screen)

        if player2 == 1:
            player2Sprites.draw(screen)
      
        pygame.display.flip()
    
    plane.sndEngine.stop()
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score
    
def instructions(score):
    pygame.display.set_caption("Insane Space Rescue!")

    plane = Plane()
    ocean = Ocean()
    
    
    allSprites = pygame.sprite.Group(ocean,plane)
    insFont = pygame.font.SysFont(None, 30)
    insLabels = []
    global player2
    instructions = (
    "Insane Space Rescue.   Last score: %d" % score ,
    "",
    "Instructions: Rescue stranded colonists from space crates",
    "",
    "--Fly over a crate to pick up colonists",
    "--The colonists will heal some of your HP upon rescue",
    "--Aliens will damage your ship if they hit",    
    "--An Alien Ship is also trying to shoot you",
    "--Its shield cannot be damaged by your technology",
    "",
    "CONTROLS: Steer with mouse",
    "LEFT CLICK - Fire main cannon",
    "RIGHT CLICK - Fire secondary cannons",
    "PLAYER2- W,A,S,D Movement and SPACE to fire cannon",
    "",
    "PRESS ENTER TO BEGIN OR Press Q for 2 player mode",
    "",
    ""
  
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 20, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                    donePlaying = True
                elif event.key == pygame.K_RETURN:
                    keepGoing = False
                    donePlaying = False
                elif event.key == pygame.K_q:
                    keepGoing = False
                    donePlaying = False
                    player2 = 1
                    
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    plane.sndEngine.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
    
    
