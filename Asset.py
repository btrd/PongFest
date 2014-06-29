import EdgeLaser

v=20

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
		self.sco = 0
		self.num = num
		self.lose = False

	def draw(self):
			self.game.addLine(self.x1, self.y1, self.x2, self.y2, EdgeLaser.LaserColor.LIME)

	def up(self):
		if self.y1>120:
			self.y1 -= v
			self.y2 -= v
		else:
			self.y1 = 100
			self.y2 = 200

	def down(self):
		if self.y2<480:
			self.y1 += v
			self.y2 += v
		else:
			self.y1 = 400
			self.y2 = 500