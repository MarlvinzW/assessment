from tkinter import *
from tkinter import messagebox
from random import randint

"""
    MINE SWEEPER GAME
"""


class initialScreen():
    """
        initial screen
    """

    def __init__(window):
        window.root = Tk()
        window.root.title("Start Game")
        window.root.grid()
        window.finish = "N"
        """
            screen size
        """
        window.height = 8
        window.width = 8
        window.mines = 8
        window.startbutton = Button(text="Begin Mine Sweeper Game", command=lambda: initialScreen.onclick(window))
        window.startbutton.grid(column=4, row=5)
        window.root.mainloop()

    """
        cancel button
    """

    def onclick(window):
        window.finish = "Y"
        window.root.destroy()
        return window


"""
    screen for the game
"""


class gameWindow():
    def __init__(s, setup):
        s.height = setup.height
        s.width = setup.width
        s.mines = setup.mines

        s.root = Tk()
        s.root.title("Minesweeper")
        s.root.grid()
        l1 = Label(s.root, text="First:")

        s.finish = "N"
        s.maingrid = list()
        s.maingrid.append([])
        for i in range(s.height):
            s.maingrid.append([])
            for x in range(s.width):
                s.maingrid[i].append(" ")
                s.maingrid[i][x] = Button(height=0, width=3, font="TimesNewRoman 15 bold", text="*", bg="green",
                                          command=lambda i=i, x=x: gameWindow.onclick(s, i, x))
                s.maingrid[i][x].bind("<Button-3>",
                                      lambda event="<Button-3>", i=i, x=x: gameWindow.rightclick(event, s, i, x))
                s.maingrid[i][x].grid(row=i, column=x)
                s.maingrid[i][x].mine = "False"

        totals_squares = s.height * s.width
        s.scores_needed = totals_squares - s.mines
        s.score = 0

        index_list = list()
        for i in range(totals_squares):
            index_list.append(i)

        """
            storage of spaces chosen
        """
        spaces_chosen = list()
        for i in range(s.mines):
            chosen_space = randint(0, len(index_list) - 1)
            spaces_chosen.append(index_list[chosen_space])
            del index_list[chosen_space]

        for i in range(len(spaces_chosen)):
            xvalue = int(spaces_chosen[i] % s.width)
            ivalue = int(spaces_chosen[i] / s.width)

            s.maingrid[ivalue][xvalue].mine = "True"

        s.root.mainloop()

    """
        when user clicks on the grid
    """
    def onclick(s, i, x):
        color_list = ["PlaceHolder", "Green", "Black", "Blue", "Gray", "Red", "Purple", "Turquoise", "Maroon"]

        if s.maingrid[i][x]["text"] != "F" and s.maingrid[i][x]["relief"] != "sunken":
            if s.maingrid[i][x].mine == "False":
                s.score += 1

                combinationsi = [1, -1, 0, 0, 1, 1, -1, -1]
                combinationsx = [0, 0, 1, -1, 1, -1, 1, -1]

                mine_count = 0
                for combinations in range(len(combinationsi)):
                    tempi = i + combinationsi[combinations]
                    tempx = x + combinationsx[combinations]

                    if tempi < s.height and tempx < s.width and tempi >= 0 and tempx >= 0:
                        if s.maingrid[tempi][tempx].mine == "True":
                            mine_count = mine_count + 1

                if mine_count == 0:
                    mine_count = ""

                s.maingrid[i][x].configure(text=mine_count, relief="sunken", bg="gray85")

                if str(mine_count).isdigit():
                    s.maingrid[i][x].configure(fg=color_list[mine_count])

                if mine_count == "":
                    for z in range(len(combinationsi)):
                        if s.finish == "N":
                            i_value = i + int(combinationsi[z])
                            x_value = x + int(combinationsx[z])

                            if i_value >= 0 and i_value < s.height and x_value >= 0 and x_value < s.width:
                                if s.maingrid[i_value][x_value]["relief"] != "sunken":
                                    gameWindow.onclick(s, i_value, x_value)

                if s.score == s.scores_needed and s.finish == "N":
                    messagebox.showinfo("Congratulations", "You won")
                    s.finish = "Y"
                    s.root.destroy()
            else:
                s.maingrid[i][x].configure(bg="Red", text="M")
                for a in range(len(s.maingrid)):
                    for b in range(len(s.maingrid[a])):
                        if s.maingrid[a][b].mine == "True":
                            if s.maingrid[a][b]["text"] == "F":
                                s.maingrid[a][b].configure(bg="Green")
                            elif s.maingrid[a][b]["bg"] != "Red":
                                s.maingrid[a][b].configure(bg="Pink", text="M")

                        elif s.maingrid[a][b]["text"] == "F":
                            s.maingrid[a][b].configure(bg="Yellow")

                messagebox.showinfo("GAME OVER", "You lost")
                s.root.destroy()

    """
        handle mouse right click
    """

    def rightclick(event, s, i, x):
        if s.maingrid[i][x]["relief"] != "sunken":
            if s.maingrid[i][x]["text"] == "":
                s.maingrid[i][x].config(text="F")
            elif s.maingrid[i][x]["text"] == "F":
                s.maingrid[i][x].config(text="?")
            else:
                s.maingrid[i][x].config(text="")


"""
    initialise the game
"""


if __name__ == "__main__":
    setup = initialScreen()
    if setup.finish == "Y":
        game = gameWindow(setup)
    quit()

