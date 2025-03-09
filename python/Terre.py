import pygame as pg
from turtle import Vec2D
from math import sqrt
from random import randrange

# Constantes :
Gmm = 5  # = G x m_1 x m_2
FPS = 60  # les fps tabernak
p_c = (255, 0, 0, 255)  # Couleur de la planète au centre
WIND = 1000
print("\n" +
      " Garder Q pour faire pause \n" +
      " W pour switcher mode vecteur / mode graphique \n" +
      " Fleches directionnelles pour changer l'orientation // l'intensité du meteor\n" +
      " Z pour faire suivre le bleu sur son vecteur directeur\n" +
      " A pour afficher la position du bleu")

f = pg.display.set_mode(size=(WIND, WIND))
pg.display.set_caption("tutute")
fpsClock = pg.time.Clock()
o = pg.sprite.Group()


def carr(x, y, teh=10, c=(255, 0, 0)):  # Tracer un carré à partir d'un point en haut à gauche
    pg.draw.rect(f, c, (x, y, teh, teh))


def dist(a: tuple, z: tuple):  # Distance entre a et b
    return sqrt((a[0] - z[0]) ** 2 + (a[1] - z[1]) ** 2)


class Obej(pg.sprite.Sprite):  # Les météorites

    def __init__(self):
        super().__init__()
        self.v = Vec2D(randrange(100), randrange(100))  # Son vecteur d'origine
        self.x = randrange(WIND)  # X d'origine
        self.y = randrange(int(WIND/2))  # Y d'origine
        self.isshow = False  # Es ce qu'on montre son vecteur ?
        self.g = Vec2D(0, 0)  # Vecteur gravitationel
        self.c = (randrange(255), 10, 10)  # Couleur principale
        self.pos = [(self.x, self.y)]  # Liste qui contiendra les position des queues

    def fd(self):  # Suivre son instinct
        global le
        u = self.v * 0.01  # ralentissement cosmique
        self.x += u[0]
        self.y += u[1]
        self.pos.append((self.x, self.y))
        if self.y>800:
            self.v=self.v.rotate(180)
            self.attraction()
           

    def show(self):  # Montrer ses vecteurs
        u = self.g
        pg.draw.line(f,(255,255,0),(self.x+5,self.y+5),(self.x+u[0]*10+5,self.y+u[1]*10+5))
        u = self.v * (1 / 10)
        pg.draw.line(f,self.c,(self.x+5,self.y+5),(self.x+u[0]*5+5,self.y+u[1]*5+5))

    def attraction(self):  # Actualiser le vecteur gravitationnel
        #WIND/2 = centre de la fenètre
        self.g = Vec2D( 0, self.y) * (Gmm / dist((0, self.y), (self.x, self.y)))


# on crée 10 mététorites
le = 0  # on les compte
for bubu in range(10):
    m = Obej()
    o.add(m)
    le += 1
# on rajoute le joueur :
g = Obej()
o.add(g)

# La boucle de jeu
b = True
try:
    while b:
        # Actualiser:
        pg.display.flip()

        # Appliquer les images de fond sur la fenetre
        s = pg.Surface((WIND, WIND))  # piqué sur stackoverflow pour avoir un fond avec un alpha
        if g.isshow:
            s.set_alpha(250)
        else:
            s.set_alpha(50)
            
        s.fill((0, 0, 0))
        f.blit(s, (0, 0))
        pg.draw.rect(f,p_c,(0,800,1000,1000))# Sol

        for bubu in o:
            bubu.attraction()
            if g.isshow:
                bubu.show()

        p = pg.key.get_pressed()  # SI la touche est appuyée

        for bubu in o:
            if not p[pg.K_q]:
                bubu.v += bubu.g
                bubu.fd()
                if not g.isshow:
                    for i in bubu.pos:
                        carr(i[0], i[1], c=bubu.c)
            carr(bubu.x, bubu.y, c=(255, 255, 255))
            if len(bubu.pos) > 50:
                bubu.pos.pop(0)
        if p[pg.K_a]:
            carr(g.x, g.y, 10, c=(0, 0, 255))
        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False  # la boucle n'est plus vraie dons on arrete de trourner
                print(" Fin du jeu")
            elif event.type == pg.KEYDOWN:
                if event.dict['key'] == pg.K_z:
                    g.fd()
                if event.dict['key'] == pg.K_w:
                    g.isshow = not g.isshow
                if event.dict['key'] == pg.K_RIGHT:
                    g.v = g.v.rotate(30)
                if event.dict['key'] == pg.K_LEFT:
                    g.v = g.v.rotate(-30)
                if event.dict['key'] == pg.K_UP:
                    g.v = g.v * (11 / 10)
                if event.dict['key'] == pg.K_DOWN:
                    g.v = g.v * (9 / 10)

        fpsClock.tick(FPS)
except:
    pg.quit()
    raise
pg.quit()
