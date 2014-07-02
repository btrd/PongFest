import EdgeLaser

#global player speed
Gps=10
#global ball speed
Gbs=5

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
		self.win = False

	def draw(self):
			self.game.addLine(self.x1, self.y1, self.x2, self.y2)

	def up(self):
		#On test si on va pas sortir du terrain de jeux
		if self.y1>120:
			self.y1 -= Gps
			self.y2 -= Gps
		else:
			self.y1 = 101
			self.y2 = 201

	def down(self):
		#On test si on va pas sortir du terrain de jeux
		if self.y2<480:
			self.y1 += Gps
			self.y2 += Gps
		else:
			self.y1 = 399
			self.y2 = 499

class Ball(Asset):
	def __init__(self, game,p):
		self.bs=Gbs
		Asset.__init__(self, game, 240, 290, 260, 310)
		self.v=5
		#direction de depart aleatoire
		if p == 1:
			self.dx=-self.bs
		else:
			self.dx=self.bs
		self.dy=0

	def __str__(self):
		return "x1:{self.x1};x2:{self.x2};y1:{self.y1};y2:{self.y2}"

	def draw(self):
		self.x2+=self.dx
		self.y2+=self.dy
		self.y1+=self.dy
		self.x1+=self.dx
		#test si on sort pas du cadre
		if self.x1<=5:
			self.x1 = 6
			self.x2 = 26
		if self.x2>=495:
			self.x1 = 474
			self.x2 = 494
		if self.y1<=100:
			self.y1 = 101
			self.y2 = 121
		if self.y2>=500:
			self.y1 = 479
			self.y2 = 499
		self.game.addRectangle(self.x1, self.y1, self.x2, self.y2)

	def conflict(self, p1, p2):
		if self.x1 == 6:
			#test si p1 est sur la balle
			if (self.y2>p1.y1 and self.y2<p1.y2) or (self.y1>p1.y1 and self.y1<p1.y2):
				#p1 rattrape la balle
				#centre de la balle
				yb = self.y1+10
				self.dy = (yb-p1.y1-50)*0.2
				self.dx =-self.dx+0.5
				print self.dy
			else:
				#p1 perdu
				p2.score+=1
				p2.win=True
		elif self.x2==494:
			#test si p2 est sur la balle
			if (self.y2>p2.y1 and self.y2<p2.y2) or (self.y1>p2.y1 and self.y1<p2.y2):
				#p2 rattrape la balle
				#centre de la balle
				yb = self.y1+10
				self.dy = (yb-p2.y1-50)*0.2
				self.dx =-self.dx+0.5
				print self.dy
			else:
				#p2 perdu
				p1.score+=1
				p1.win=True
		elif self.y1==101 or self.y2==499:
			#touche les bords
			print 'TODO'
			print self.dy
			self.dy=-self.dy
			print self.dy

		if not p1.win and not p2.win:
			self.draw()