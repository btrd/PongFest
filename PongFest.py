import EdgeLaser
import time
import Asset
import random

game = EdgeLaser.LaserGame('PongFest')
font = EdgeLaser.LaserFont('lcd.elfc')

game.setResolution(500).setDefaultColor(EdgeLaser.LaserColor.LIME)

while True:
	while game.isStopped():
		game.receiveServerCommands()
        time.sleep(0.5)

	#creation des joueurs
	p1 = Asset.Player(game,'left')
	p2 = Asset.Player(game,'right')

	#premiere balle de match
	b = Asset.Ball(game,random.randint(1,2))

	while not game.isStopped():
		game.receiveServerCommands()

		#ligne de separation
		game.addLine(0, 100, 500, 100)
		game.addLine(0, 500, 500, 500)
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