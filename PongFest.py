import EdgeLaser
import time
import Asset
import random

game = EdgeLaser.LaserGame('PongFest')
font = EdgeLaser.LaserFont('lcd.elfc')

game.setResolution(500).setDefaultColor(EdgeLaser.LaserColor.LIME)

#creation des joueurs
p1 = Asset.Player(game,1)
p2 = Asset.Player(game,2)

#premiere balle de match
b = Asset.Ball(game,random.randint(1,2))

while game.isStopped():
	game.receiveServerCommands()

while not game.isStopped():
	game.receiveServerCommands()

	if p1.score == 5:
		#afficher le score
		font.render(game, "P1", 200, 100, EdgeLaser.LaserColor.LIME, 10)
		font.render(game, "WIN", 150, 300, EdgeLaser.LaserColor.LIME, 10)
	elif p2.score == 5:
		#afficher le score
		font.render(game, "P2", 200, 100, EdgeLaser.LaserColor.LIME, 10)
		font.render(game, "WIN", 150, 300, EdgeLaser.LaserColor.LIME, 10)
	else:
		#ligne de separation
		game.addLine(0, 100, 500, 100)
		game.addLine(0, 500, 500, 500)
		#afficher le score
		font.render(game, ("%d"%p1.score), 0, 10, EdgeLaser.LaserColor.LIME, 7)
		font.render(game, ("%d"%p2.score), 430, 10, EdgeLaser.LaserColor.LIME, 7)

		if p1.win:
			b = Asset.Ball(game,1)
			p1.win = False
		elif p2.win:
			b = Asset.Ball(game,2)
			p2.win = False

		#mouvements des joueurs
		if game.player1_keys:
			if game.player1_keys.yp :
				p1.up()
			if game.player1_keys.yn :
				p1.down()
		if game.player2_keys:
			if game.player2_keys.yp :
				p2.up()
			if game.player2_keys.yn :
				p2.down()

		b.conflict(p1,p2)

		#affichage des joueurs
		p1.draw()
		p2.draw()

	game.refresh()
	time.sleep(0.02)