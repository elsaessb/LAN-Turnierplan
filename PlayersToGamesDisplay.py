import tkinter as tk

from AddGameDisplay import AddGameDisplay
from AddPlayerDisplay import AddPlayerDisplay


class PlayersToGamesDisplay:
    def __init__(self, t):
        self.game_name_list = []
        for game in t.games:
            self.game_name_list.append(game.name)
        self.t = t
        self.window = tk.Tk()
        self.running = True

        self.window.columnconfigure(1, minsize=200, weight=1)
        self.window.rowconfigure(0, minsize=20, weight=1)
        self.window.title("Players and Games")

        self.players = []

        i = 0
        j = 0

        sorted_persons = sorted(self.t.persons, key=lambda x: x.id, reverse=False)

        for player in sorted_persons:
            player.clear_checkbox_list()
            fr_person = tk.Frame(self.window)
            name_of_person = player.get_name_with_id()
            lbl_name = tk.Label(fr_person, text=name_of_person)
            lbl_name.pack(side=tk.LEFT, anchor=tk.W, expand=tk.YES)
            self.players.append(lbl_name)
            fr_games = tk.Frame(self.window)
            for name in self.game_name_list:
                var = tk.BooleanVar(self.window)
                var.set(player.plays(name))

                player.checkbox_games_vars.append(var)
                player.checkbox_games_name.append(name)

                chk = tk.Checkbutton(fr_games, text=name, variable=player.checkbox_games_vars[j], onvalue=1, offvalue=0,
                                     command=self.set_invalid)
                chk.pack(side=tk.LEFT, anchor=tk.W, expand=tk.YES)
                j += 1

            j = 0
            fr_person.grid(row=i, column=0, sticky="ns")
            fr_games.grid(row=i, column=1, sticky="ns")
            i += 1

        self.valid = True

        self.fr_buttons = tk.Frame(self.window)

        self.btn_add_game = tk.Button(self.fr_buttons, text="Add Game", command=self.add_game)
        self.btn_add_game.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

        self.btn_add_player = tk.Button(self.fr_buttons, text="Add Player", command=self.add_player)
        self.btn_add_player.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

        self.btn_quit = tk.Button(self.fr_buttons, text="Okay", command=self.stop)
        self.btn_quit.grid(row=0, column=2, sticky="ns", padx=5, pady=5)

        self.fr_buttons.grid(row=i + 1, column=1, sticky="ns")

        self.window.update()

    def is_running(self):
        return self.running

    def update(self):
        self.game_name_list = []
        for game in self.t.games:
            self.game_name_list.append(game.name)
        self.players = []
        i = 0
        j = 0
        sorted_persons = sorted(self.t.persons, key=lambda x: x.id, reverse=False)

        for player in sorted_persons:
            player.clear_checkbox_list()
            fr_person = tk.Frame(self.window)
            name_of_person = player.get_name_with_id()
            lbl_name = tk.Label(fr_person, text=name_of_person)
            lbl_name.pack(side=tk.LEFT, anchor=tk.W, expand=tk.YES)
            self.players.append(lbl_name)
            fr_games = tk.Frame(self.window)
            for name in self.game_name_list:
                var = tk.BooleanVar(self.window)
                var.set(player.plays(name))

                player.checkbox_games_vars.append(var)
                player.checkbox_games_name.append(name)

                chk = tk.Checkbutton(fr_games, text=name, variable=player.checkbox_games_vars[j], onvalue=1, offvalue=0,
                                     command=self.set_invalid)
                chk.pack(side=tk.LEFT, anchor=tk.W, expand=tk.YES)
                j += 1

            j = 0
            fr_person.grid(row=i, column=0, sticky="ns")
            fr_games.grid(row=i, column=1, sticky="ns")
            i += 1

    def stop(self):
        self.running = False

    def add_game(self):
        r = AddGameDisplay(self.t, "")
        r.run()
        self.update()

    def add_player(self):
        r = AddPlayerDisplay(self.t)
        r.run()
        self.update()

    def run(self):
        while self.running:
            self.window.update()
            if not self.valid:
                self.update_selection()
        self.window.destroy()

    def set_invalid(self):
        self.valid = False

    def update_selection(self):
        for person in self.t.persons:
            for i in range(len(person.checkbox_games_vars)):
                if person.checkbox_games_vars[i].get():
                    for game in self.t.games:
                        if game.name == person.checkbox_games_name[i]:
                            person.append_game_playing(game)
                else:
                    for game in self.t.games:
                        if game.name == person.checkbox_games_name[i]:
                            if game in person.games_played:
                                person.games_played.remove(game)
        self.valid = True
