from game import GameRunner
import piece
import string
import os

clear = lambda: os.system('cls')
game_runner = GameRunner()

def play():
    while True:
        try:
            y,x = input("Entrez les coordonnées (y,x) \n").split(',')
            y = string.ascii_lowercase.index( y.lower() ) + 1
            x = int(x)
        except:
            print("Saisie incorrecte.")
            continue
        else: 
            if game_runner.play(x,y):
                break
            else:
                print("Coup invalide.")
                continue



def main():
    isAiFirst = input("Voulez-vous commencer ? (y/n) \n").lower() == 'n'
    clear()
    if isAiFirst:
        game_runner.restart(-1)
        game_runner.aiplay()
    while game_runner.finished == False:
        print(game_runner.state)
        play()
        clear()
        game_runner.aiplay()
    clear()
    print(game_runner.state)
    print("-----\nPartie terminée\n" + piece.symbols[game_runner.state.winner] + " a gagné !")
    print("Temps total de reflexion de l'IA: " + str(game_runner.total_time))

        


if __name__ == "__main__":
    main()