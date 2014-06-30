import EdgeLaser
import random

ps=20
bs=10

class Asset:

	def __init__(self, game, x1, y1, x2, y2):
		self.game = game

		#coin sup gauche
		self.x1 = x1
		self.y1 = y1

		#coin inf droite
		self.x2 = x2
		self.y2 = y2

class Player(Asset):
	def __init__(self, game, num):
		if num==1:
			x=5;
		else:
			x=495
		Asset.__init__(self, game, x, 250, x, 350)
		self.score = 0
		self.num = num
		self.lose = False

	def draw(self):
			self.game.addLine(self.x1, self.y1, self.x2, self.y2, EdgeLaser.LaserColor.LIME)

	def up(self):
		#On test si on va pas sortir du terrain de jeux
		if self.y1>120:
			self.y1 -= ps
			self.y2 -= ps
		else:
			self.y1 = 101
			self.y2 = 201

	def down(self):
		#On test si on va pas sortir du terrain de jeux
		if self.y2<480:
			self.y1 += ps
			self.y2 += ps
		else:
			self.y1 = 399
			self.y2 = 499

class Ball(Asset):
	def __init__(self, game):
		Asset.__init__(self, game, 240, 290, 260, 310)
		self.v=5
		#direction de depart aleatoire
		if random.randint(0,2) == 1:
			self.dx=-bs
		else:
			self.dx=bs
		self.dy=0

	def __str__(self):
		return "x1:{self.x1};x2:{self.x2};y1:{self.y1};y2:{self.y2}"

	def draw(self):
		#test si on sort pas du cadre
		self.x2+=self.dx
		self.y2+=self.dy
		self.y1+=self.dy
		self.x1+=self.dx
		self.game.addRectangle(self.x1, self.y1, self.x2, self.y2, EdgeLaser.LaserColor.LIME)

	def conflict(self, p1, p2):
		print self.x2
		if self.x1 <= 5:
			print ':1'
			#test si p1 est sur la balle
			if (self.y2>p1.y1 and self.y2<p1.y2) or (self.y1>p1.y1 and self.y1<p1.y2):
				#p1 rattrape la balle
			else:
				#p1 perdu
				p2.score+=1
		elif self.x2>=495:
			#test si p2 est sur la balle
			if (self.y2>p2.y1 and self.y2<p2.y2) or (self.y1>p2.y1 and self.y1<p2.y2):
				#p2 rattrape la balle

			else:
				#p2 perdu
				p1.score+=1
		elif self.y1<=101 or self.y1>=499:
			#touch les bords
		else:
			self.draw()