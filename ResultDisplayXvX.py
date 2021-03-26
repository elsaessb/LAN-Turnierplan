import tkinter as tk

from Game import Game
from Match import Match


class ResultDisplayXvX:
    def __init__(self, t, sel_game, num_matches, matches_list):
        self.window = tk.Tk()
        self.running = True
        self.t = t
        self.selected_game = sel_game
        self.num_matches = num_matches
        self.OptionsList = []
        if len(matches_list) == 0:
            self.btn_set_result = tk.Button(self.window, text="Okay", command=self.press_okay)
            self.btn_set_result.grid(row=1, column=0, sticky="n", padx=5, pady=5)
            self.lbl_games = tk.Label(self.window,
                                      text="No Matches generated for \n" + self.selected_game)

            self.lbl_games.grid(row=0, column=0, sticky="ew")
        else:
            self.variable = tk.StringVar(self.window)
            new_matches_list = []
            for game in self.t.games:
                if game.name == self.selected_game:
                    for match_name in matches_list:
                        match = game.get_match_from_string(match_name)
                        result = ""
                        if match.team1_score != match.team2_score:
                            result = "##" + match_name + "##"
                            print(result)
                        else:
                            result = match_name

                        new_matches_list.append(result)

            self.OptionsList = new_matches_list
            self.variable.set(self.OptionsList[0])
            self.selected_match = self.OptionsList[0]

            self.window.columnconfigure(1, minsize=200, weight=1)
            self.window.rowconfigure(0, minsize=20, weight=1)
            self.window.title("Add Match Result")

            self.entries = []
            for i in range(2):
                self.entries.append(tk.Entry(self.window))

            temp = 0
            for entry in self.entries:
                entry.grid(row=1, column=temp)
                temp += 1

            match = Match([], [], Game("", "", self.t))

            for game in self.t.games:
                if game.name == self.selected_game:

                    match = game.get_match_from_string(self.selected_match.replace('#', ''))

            self.entries[0].delete(0, tk.END)
            self.entries[0].insert(0, match.team1_score)
            self.entries[1].delete(0, tk.END)
            self.entries[1].insert(0, match.team2_score)

            self.opt = tk.OptionMenu(self.window, self.variable, *self.OptionsList, command=self.set_selection)
            self.opt.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

            self.btn_set_result = tk.Button(self.window, text="set Result", command=self.set_result)
            self.btn_set_result.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.window.update()

    def is_running(self):
        return self.running

    def run(self):
        while self.running:
            self.window.update()
        self.window.destroy()

    def set_selection(self, selection):
        self.selected_match = selection
        match = Match([], [], Game("", "", self.t))

        for game in self.t.games:
            if game.name == self.selected_game:
                match = game.get_match_from_string(self.selected_match.replace('#', ''))
        self.entries[0].delete(0, tk.END)
        self.entries[0].insert(0, match.team1_score)
        self.entries[1].delete(0, tk.END)
        self.entries[1].insert(0, match.team2_score)

    def set_result(self):
        scoreT1 = self.entries[0].get()
        scoreT2 = self.entries[1].get()
        if scoreT1 == "":
            print("Ergebniss Team1 leer")
        if scoreT2 == "":
            print("Ergebniss Team2 leer")

        for game in self.t.games:
            if game.name == self.selected_game:
                match = game.get_match_from_string(self.selected_match.replace('#', ''))
                if match != -1:
                    match.set_winner_XvX(scoreT1, scoreT2)
                    game.write_match(match)

                else:
                    print("Match " + self.selected_match + " not found")

        self.running = False

    def press_okay(self):
        self.running = False
