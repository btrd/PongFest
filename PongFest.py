import EdgeLaser
import time
import Asset

game = EdgeLaser.LaserGame('PongFest')
font = EdgeLaser.LaserFont('lcd.elfc')

game.setResolution(500).setDefaultColor(EdgeLaser.LaserColor.LIME)

p1 = Asset.Player(game,1)
p2 = Asset.Player(game,2)

goal = True

while game.isStopped():
	game.receiveServerCommands()

while not game.isStopped():
	game.receiveServerCommands()
	if goal:
		b = Asset.Ball(game)
		goal = False

	#afficher le score
	font.render(game, ("%d"%p1.score), 0, 10, EdgeLaser.LaserColor.LIME, 7)
	font.render(game, ("%d"%p2.score), 430, 10, EdgeLaser.LaserColor.LIME, 7)

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

	#ligne de separation
	game.addLine(0, 100, 500, 100, EdgeLaser.LaserColor.LIME)
	game.addLine(0, 500, 500, 500, EdgeLaser.LaserColor.LIME)
	#affichage des joueurs
	p1.draw()
	p2.draw()
	b.conflict(p1,p2)

	game.refresh()
	time.sleep(0.05)