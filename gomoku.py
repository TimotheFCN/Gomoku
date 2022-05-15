from game import GameRunner
import piece
import os

clear = lambda: os.system('cls')
game_runner = GameRunner()

def play():
    while True:
        try:
            x,y = input("Entrez les coordonnées (x,y) \n").split(',')
            x,y = int(x) , int(y)
            
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
    while game_runner.finished == False:
        clear()
        print(game_runner.state)
        play()
        game_runner.aiplay()
    clear()
    print(game_runner.state)
    print("-----\nPartie terminée\n" + piece.symbols[game_runner.state.winner] + " a gagné !")

        


if __name__ == "__main__":
    main()