import tkinter as tk

from Game import Game


class AddGameDisplay:
    def __init__(self, t, sel_game):
        if sel_game != "":
            self.window = tk.Tk()
            self.window.title("Add Game")
            self.running = True
            self.t = t
            self.selected_game = sel_game
            self.entry = ""

            self.text_error = tk.StringVar(self.window)
            self.text_error.set("--")

            self.window.columnconfigure(0, minsize=200, weight=1)
            self.window.rowconfigure(0, minsize=20, weight=1)
            self.window.title("Add Game")

            self.lbl_matches = tk.Label(self.window, textvariable=self.text_error)
            self.lbl_games = tk.Label(self.window, text="Game " + self.selected_game + " not in Games List.\nWhat Type "
                                                                                       "is it (AvA, XvX, 1v1, 2v2)?")

            self.lbl_matches.grid(row=2, column=0, sticky="ew")
            self.lbl_games.grid(row=0, column=0, sticky="ew")

            self.entries = []
            for i in range(1):
                self.entries.append(tk.Entry(self.window))

            self.entries[0].grid(row=1, column=0, sticky="ns")

            self.btn_set_result = tk.Button(self.window, text="Add Game", command=self.set_result)
            self.btn_set_result.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

            self.window.update()
        else:
            self.window = tk.Tk()
            self.running = True
            self.t = t
            self.new_game = Game("", "", self.t)
            self.entry = 0

            self.lbl_game = tk.Label(self.window, text="Enter Gamename")
            self.lbl_type = tk.Label(self.window, text="Enter Gametype")

            self.lbl_game.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
            self.lbl_type.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

            self.entries = []
            for i in range(2):
                self.entries.append(tk.Entry(self.window))
                self.entries[i].grid(row=1, column=i, sticky="ns", padx=5, pady=5)

            self.btn_set_result = tk.Button(self.window, text="Add Game", command=self.set_result_new_game)
            self.btn_set_result.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

            self.window.update()

    def is_running(self):
        return self.running

    def run(self):
        while self.running:
            self.window.update()
        self.window.destroy()
        return self.entry

    def set_result(self):
        self.entry = self.entries[0].get()
        if self.entry == "":
            self.text_error.set("Please Enter a Gametype")
        if self.entry == "AvA" or self.entry == "1v1" or self.entry == "2v2":
            self.running = False
        else:
            self.text_error.set("'" + self.entry + "' is not a valid Gametype")

    def set_result_new_game(self):
        name = self.entries[0].get()
        _type = self.entries[1].get()
        print(name + " " + _type)
        if _type == "AvA" or _type == "1v1" or _type == "2v2":
            self.new_game = Game(name, _type, self.t)
            self.t.append_game(self.new_game)
            self.running = False
        else:
            print("'" + _type + "' is not a valid Gametype")
