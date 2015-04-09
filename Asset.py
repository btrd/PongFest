import EdgeLaser
import json
import requests
import copy
from sessions import FuturesSession

#global player speed
Gps=2
#global ball speed
Gbs=3

server="http://shadok-pong.scalingo.io"
#server="http://localhost:3000"

session = FuturesSession()

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
	def __init__(self, game, side):
		if side=='left':
			x=5;
		elif side=='right':
			x=495
		else:
			print 'Error side player' + side
		Asset.__init__(self, game, x, 250, x, 350)
		self.score = 0
		self.side = side
		self.win = False

	def draw(self):
		self.game.addLine(self.x1, self.y1, self.x2, self.y2)

	def up(self):
		#On test si on va pas sortir du terrain de jeux
		if self.y1>120:
			self.y1 -= Gps
			self.y2 -= Gps
			#diffusion
			y = self.y1 + ( (self.y2 - self.y1) / 2 )
			data = {'side':self.side,'y':y}
			headers = {'Content-Type':'application/json'}
			future = session.post(server + '/api/racket', data=json.dumps(data), headers=headers)
		else:
			self.y1 = 101
			self.y2 = 201

	def down(self):
		#On test si on va pas sortir du terrain de jeux
		if self.y2<480:
			self.y1 += Gps
			self.y2 += Gps
			#diffusion
			y = self.y1 + ( (self.y2 - self.y1) / 2 )
			data = {'side':self.side,'y':y}
			headers = {'Content-Type':'application/json'}
			future = session.post(server + '/api/racket', data=json.dumps(data), headers=headers)
		else:
			self.y1 = 399
			self.y2 = 499

class Ball(Asset):
	def __init__(self, game,p):
		self.bs = Gbs
		Asset.__init__(self, game, 240, 290, 260, 310)
		self.v=5
		#direction de depart aleatoire
		if p == 1:
			self.dx = -self.bs
		else:
			self.dx = self.bs
		self.dy=0

	def __str__(self):
		return "x1:{self.x1};x2:{self.x2};y1:{self.y1};y2:{self.y2}"

	def draw(self):
		self.x2 += self.dx
		self.y2 += self.dy
		self.y1 += self.dy
		self.x1 += self.dx
		#test si on sort pas du cadre
		if self.x1 <= 5:
			self.x1 = 6
			self.x2 = 26
		if self.x2 >= 495:
			self.x1 = 474
			self.x2 = 494
		if self.y1 <= 100:
			self.y1 = 101
			self.y2 = 121
		if self.y2 >= 500:
			self.y1 = 479
			self.y2 = 499
		self.game.addRectangle(self.x1, self.y1, self.x2, self.y2)

	def conflict(self, p1, p2):
		if self.x1 == 6:
			#test si p1 est sur la balle
			if (self.y2 > p1.y1 and self.y2 < p1.y2) or (self.y1 > p1.y1 and self.y1 < p1.y2):
				#p1 rattrape la balle
				#centre de la balle
				yb = self.y1+10
				#calcul trajectoire sur y en prenant la distance par rapport au centre de la raquette
				self.dy = (yb-p1.y1-50)*0.2
				#inversion du sens de la balle + augmentation vitesse
				self.dx = -self.dx
				#calcul fictif du parcours de la balle
				self.fictif_route()
			else:
				#p1 perdu
				p2.score += 1
				p2.win=True
				self.sendScore(p1, p2)
				if p2.score >= 10:
					p1.score = 0
					p2.score = 0
		elif self.x2 == 494:
			#test si p2 est sur la balle
			if (self.y2 > p2.y1 and self.y2 < p2.y2) or (self.y1 > p2.y1 and self.y1 < p2.y2):
				#p2 rattrape la balle
				#centre de la balle
				yb = self.y1+10
				#calcul trajectoire sur y en prenant la distance par rapport au centre de la raquette
				self.dy = (yb-p2.y1-50)*0.2
				#inversion du sens de la balle + augmentation vitesse
				self.dx = -self.dx
				#calcul fictif du parcours de la balle
				self.fictif_route()
			else:
				#p2 perdu
				p1.score += 1
				p1.win = True
				self.sendScore(p1, p2)
				if p1.score >= 10:
					p1.score = 0
					p2.score = 0
		elif self.y1 == 101 or self.y2 == 499:
			#touche les bords
			self.dy = -self.dy

		if not p1.win and not p2.win:
			self.draw()

	def fictif_route(self):
		b = copy.copy(self)
		#tant qu'on est pas sur les bords
		while b.x1 > 6 and b.x2 < 494:
			#si on touche le sol ou le plafond
			if b.y1 <= 101 or b.y2 >= 499:
				b.dy = -b.dy
			b.x2 += b.dx
			b.y2 += b.dy
			b.y1 += b.dy
			b.x1 += b.dx

		print b.x1
		#diffusion
		if b.x1 < 250:
			side = "left"
		else:
			side = "right"
		y = self.y1 + ( (self.y2 - self.y1) / 2 )
		data = {'side':side,'y':y}
		headers = {'Content-Type':'application/json'}
		future = session.post(server + '/api/fictif', data=json.dumps(data), headers=headers)
	
	def sendScore(self, p1, p2):
		data = {'left':p1.score,'right':p2.score}
		headers = {'Content-Type':'application/json'}
		future = session.post(server + '/api/score', data=json.dumps(data), headers=headers)
