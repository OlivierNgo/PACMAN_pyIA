import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ])
# attention, on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM
            
GUM = PlacementsGUM()   
            

PacManPos = [5,5]

# Initialisation des fantômes avec la direction courante (0, 1) signifiant vers la droite
Ghosts = [
    [LARGEUR // 2, HAUTEUR // 2, "pink", (0, 1)],
    [LARGEUR // 2, HAUTEUR // 2, "orange", (0, 1)],
    [LARGEUR // 2, HAUTEUR // 2, "cyan", (0, 1)],
    [LARGEUR // 2, HAUTEUR // 2, "red", (0, 1)]
]
        

# Ajout d'une variable de score global  
SCORE = 0

##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info
   


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
   
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################



      
def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x, y):
    L = []
    if TBL[x][y-1] != 1: L.append((0, -1))
    if TBL[x][y+1] != 1: L.append((0, 1))
    if TBL[x+1][y] != 1: L.append((1, 0))
    if TBL[x-1][y] != 1: L.append((-1, 0))
    return L

def DetectorDifferentPath(moves):
    if len(moves) == 2:
        dx1, dy1 = moves[0]
        dx2, dy2 = moves[1]
        if (dx1 == -dx2 and dy1 == 0 and dy2 == 0) or (dy1 == -dy2 and dx1 == 0 and dx2 == 0):
            return True
    return False
   

# Widget pour afficher le score
score_label = tk.Label(Frame1, text="Score : 0", font=("Arial", 16), foreground="yellow", background="black")
score_label.place(x=20, y=475)

def init_distance_map():
    # Crée un tableau de la même taille que TBL, initialisé avec des valeurs infinies (np.inf)
    distance_map = np.full(TBL.shape, np.inf)
    
    # Parcourt chaque case du tableau TBL
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 1:  # Si la case est un mur
                distance_map[x][y] = np.inf  # Assigne une valeur infinie
            elif GUM[x][y] == 1:  # Si la case contient une Pac-gomme
                distance_map[x][y] = 0  # Assigne une valeur de 0
            else:  # Si la case est vide
                distance_map[x][y] = LARGEUR * HAUTEUR  # Assigne une grande valeur
    return distance_map  # Retourne la carte des distances initialisée

def IAPacman():
    global PacManPos, Ghosts, GUM, SCORE
    distance_map = compute_distance_map()  # Calcule la carte des distances

    # Trouver le mouvement optimal en fonction de la carte des distances
    x, y = PacManPos  # Position actuelle de Pac-Man
    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]  # Liste des voisins (haut, bas, gauche, droite)
    next_move = min(neighbors, key=lambda pos: distance_map[pos[0]][pos[1]] if 0 <= pos[0] < LARGEUR and 0 <= pos[1] < HAUTEUR else np.inf)  # Choisit le voisin avec la plus petite distance

    # Vérifier la position suivante
    next_x, next_y = next_move  # Coordonnées de la prochaine position de Pac-Man
    if GUM[next_x][next_y] == 1:  # Si la prochaine position contient une Pac-gomme
        GUM[next_x][next_y] = 0  # Supprime la Pac-gomme de la liste
        SCORE += 100  # Augmente le score de 100 points
        score_label.config(text=f"Score: {SCORE}")  # Met à jour le texte du widget Label avec le nouveau score

    PacManPos = [next_x, next_y]  # Met à jour la position de Pac-Man

    # Détection de collision avec les fantômes
    for F in Ghosts:
        if [next_x, next_y] == [F[0], F[1]]:
            print("Collision détectée! Le jeu est terminé.")
            # Arrête le jeu ou réinitialise la position
            return

    # Affiche la carte des distances pour chaque case (optionnel)
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            info = distance_map[x][y]
            if info == np.inf:
                info = "+∞"
            elif info == LARGEUR * HAUTEUR:
                info = ""
            SetInfo1(x, y, info)  # Utilise la fonction SetInfo1 pour afficher les distances




def update_distance_map(distance_map):
    updated = False  # Initialisation d'un booléen pour vérifier si une mise à jour a eu lieu
    
    # Parcourt chaque case du tableau distance_map
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] != 1:  # Si la case n'est pas un mur
                current_distance = distance_map[x][y]  # Distance actuelle de la case
                
                # Liste des voisins (haut, bas, gauche, droite)
                neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                
                # Trouve la distance minimale parmi les voisins (ajoute 1 pour chaque voisin valide)
                min_distance = min([distance_map[nx][ny] + 1 for nx, ny in neighbors if 0 <= nx < LARGEUR and 0 <= ny < HAUTEUR and distance_map[nx][ny] != np.inf], default=np.inf)
                
                # Si la nouvelle distance calculée est inférieure à la distance actuelle
                if min_distance < current_distance:
                    distance_map[x][y] = min_distance  # Met à jour la distance
                    updated = True  # Indique qu'une mise à jour a eu lieu
    return updated  # Retourne True si des mises à jour ont été effectuées, sinon False


def compute_distance_map():
    distance_map = init_distance_map()  # Initialise la carte des distances
    while update_distance_map(distance_map):  # Continue de mettre à jour jusqu'à ce qu'aucune mise à jour ne soit nécessaire
        pass
    return distance_map  # Retourne la carte des distances finalisée


 
   
def IAGhosts():
    global Ghosts
    for F in Ghosts:
        x, y, color, choix_direction = F
        possible_moves = GhostsPossibleMove(x, y)

        # Détecter si le fantôme est dans un couloir
        if DetectorDifferentPath(possible_moves):
            # Si le fantôme peut continuer dans sa direction courante, il le fait
            if choix_direction in possible_moves:
                F[0] += choix_direction[0]
                F[1] += choix_direction[1]
            else:
                # Si la direction courante n'est pas possible, choisir une nouvelle direction parmi les mouvements possibles
                new_direction = random.choice(possible_moves)
                F[0] += new_direction[0]
                F[1] += new_direction[1]
                F[3] = new_direction
        else:
            # Si le fantôme est à un embranchement, choisir une nouvelle direction aléatoire
            new_direction = random.choice(possible_moves)
            F[0] += new_direction[0]
            F[1] += new_direction[1]
            F[3] = new_direction

        # Détection de collision avec Pac-Man
        if [F[0], F[1]] == PacManPos:
            print("Collision détectée! Le jeu est terminé.")
            # Arrête le jeu ou réinitialise la position
            break

      
  
 

 
#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
   global iteration
   
   if not PAUSE_FLAG : 
      iteration += 1
      if iteration % 2 == 0 :   IAPacman()
      else:                     IAGhosts()
   
   Affiche(PacmanColor = "yellow", message = "message")  
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()

 
   
   
    
   
   