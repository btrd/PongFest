import EdgeLaser
import time
import Asset

game = EdgeLaser.LaserGame('PongFest')

game.setResolution(500).setDefaultColor(EdgeLaser.LaserColor.LIME)

p1 = Asset.Player(game,1)
p2 = Asset.Player(game,2)

while game.isStopped():
	game.receiveServerCommands()

while not game.isStopped():
	game.receiveServerCommands()

	#afficher le score

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

	game.addLine(0, 100, 500, 100, EdgeLaser.LaserColor.LIME)
	p1.draw()
	p2.draw()
	game.refresh()
	time.sleep(0.05)