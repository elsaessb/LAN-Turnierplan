import os
import tkinter as tk


class ResultDisplayAvA:
    def __init__(self, t, sel_game, num_matches, matches_list):
        self.window = tk.Tk()
        self.window.title("set Result for " + sel_game)
        self.running = True
        self.t = t
        self.selected_game = sel_game
        self.num_matches = num_matches
        self.OptionsList = []

        self.variable = tk.StringVar(self.window)
        new_matches_list = []
        for game in self.t.games:
            if game.name == self.selected_game:
                for match_name in matches_list:
                    match = game.get_match_from_string(match_name)
                    result = ""
                    if match.winner != []:
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
        #self.window.title("Add Match Result")

        self.entries = []
        for i in range(1):
            self.entries.append(tk.Entry(self.window))

        temp = 0
        for entry in self.entries:
            entry.grid(row=1, column=temp)
            temp += 1

        for game in self.t.games:
            if game.name == self.selected_game:
                match = game.get_match_from_string(self.selected_match.replace('#', ''))

        self.entries[0].delete(0, tk.END)
        self.entries[0].insert(0, match.winner)

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
        for game in self.t.games:
            if game.name == self.selected_game:
                match = game.get_match_from_string(self.selected_match.replace('#', ''))
        self.entries[0].delete(0, tk.END)
        self.entries[0].insert(0, match.team1_score)

    def set_result(self):
        scoreT1 = self.entries[0].get()

        words = scoreT1.split(",")

        if scoreT1 == "":
            print("Ergebniss leer")

        for game in self.t.games:
            if game.name == self.selected_game:
                match = game.get_match_from_string(self.selected_match.replace('#', ''))
                if match != -1:
                    match.set_winner_AvA(words)
                    game.write_match(match)

                else:
                    print("Match " + self.selected_match + " not found")

        self.running = False
