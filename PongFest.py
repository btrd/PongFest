import EdgeLaser
import time
import Asset
import random
import argparse
import datetime


def printText(text, t):
    text_size = font.size(text,4)
    offset_x = (Asset.RESOLUTION - text_size) / 2
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).total_seconds() < t:
        font.render(game, text, offset_x, 250, coeff=4)
        game.refresh()
        time.sleep(0.1)
    return

parser = argparse.ArgumentParser()
parser.add_argument("-H","--host",default=EdgeLaser.HOST)
parser.add_argument("-P", "--port", type=int, default=EdgeLaser.PORT)

args=parser.parse_args()

game = EdgeLaser.LaserGame('PongFest',args.host,args.port)
font = EdgeLaser.LaserFont('lcd.elfc')



game.setResolution(Asset.RESOLUTION).setDefaultColor(EdgeLaser.LaserColor.LIME)

while True:
    while game.isStopped():
        game.receiveServerCommands()
        time.sleep(0.5)

    game_mode="GAME"

    #creation des joueurs
    p1 = Asset.Player(game,'left')
    p2 = Asset.Player(game,'right')

    #premiere balle de match
    b = Asset.Ball(game,random.randint(1,2))

    while not game.isStopped():
        game.receiveServerCommands()

        #ligne de separation
        #game.addLine(0, 100, 500, 100)
        #game.addLine(0, 500, 500, 500)

        if game_mode=="GAME":

            if p1.win:
                b = Asset.Ball(game,1)
                p1.win = False

                game_mode = "SCORE"
            elif p2.win:
                b = Asset.Ball(game,2)
                p2.win = False

                game_mode = "SCORE"

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

        elif game_mode == "SCORE" :

            game.refresh()

            printText("{} - {}".format(p1.score, p2.score),2)

            if p1.score < 1 and p2.score < 1:
                printText("CONNECT",2)
                printText("TO", 1)
                printText("PONG.PW",3)

            game_mode="GAME"
