import os
import tkinter as tk

from Game import Game
from PlayersToGamesDisplay import PlayersToGamesDisplay
from ResultDisplayAvA import ResultDisplayAvA
from ResultDisplayXvX import ResultDisplayXvX


class Display:
    def __init__(self, t):
        self.window = tk.Tk()
        self.t = t
        self.OptionsList = []
        self.list_of_matches = []

        self.variable = tk.StringVar(self.window)
        self.OptionsList = self.get_games_from_turnier()
        if len(self.OptionsList) == 0:
            self.OptionsList.append("No Games")
        self.variable.set(self.OptionsList[0])
        self.selected_game = self.OptionsList[0]
        self.selected_match = ""
        self.num_matches = 0

        self.score_string = ""
        for person in self.t.persons:
            self.score_string += person.get_name_with_id() + "\t" + str(person.score) + "\n"

        self.persons_vName = tk.StringVar(self.window)
        self.persons_vName.set(self.score_string)

        self.matches_list = tk.StringVar(self.window)
        self.matches_list.set("Not enough Players")

        self.window.columnconfigure(1, minsize=200, weight=1)
        self.window.rowconfigure(0, minsize=20, weight=1)
        self.window.title("Tournament Generator")

        self.fr_buttons = tk.Frame(self.window)
        self.btn_load_tournament = tk.Button(self.fr_buttons, text="Load Tournament", command=self.load_last_turnier)
        self.btn_generate_matches = tk.Button(self.fr_buttons, text="Generate Matches", command=self.generate_matches)
        self.btn_result = tk.Button(self.fr_buttons, text="set Result", command=self.set_result_for_match)
        self.btn_players_to_games = tk.Button(self.fr_buttons, text="change Tournament", command=self.players_to_games)

        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.btn_load_tournament.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_generate_matches.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_result.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        self.btn_players_to_games.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.fr_games = tk.Frame(self.window)
        self.lbl_matches = tk.Label(self.fr_games, textvariable=self.matches_list, font="Courier", justify=tk.LEFT)
        self.lbl_games = tk.Label(self.fr_games, text="Games", font="Courier")

        self.fr_games.grid(row=0, column=2, sticky="ns")
        self.lbl_matches.grid(row=1, column=0, sticky="ew")
        self.lbl_games.grid(row=0, column=0, sticky="ew")

        self.fr_score = tk.Frame(self.window)
        self.lbl_score = tk.Label(self.fr_score, textvariable=self.persons_vName, font="Courier")
        self.lbl_score_head = tk.Label(self.fr_score, text="Leaderboard", font="Courier")

        self.fr_score.grid(row=0, column=1, sticky="ns")
        self.lbl_score.grid(row=1, column=0, sticky="w")
        self.lbl_score_head.grid(row=0, column=0, sticky="ew")

        self.opt = tk.OptionMenu(self.fr_buttons, self.variable, *self.OptionsList, command=self.set_selection)
        self.opt.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

    def run(self):
        self.window.mainloop()

    def load_last_turnier(self):
        self.t.load_last_turnier()
        self.t.save_current_turnier()

        for game in self.t.games:
            self.set_selection(game.name)

        self.set_selection(self.t.games[0].name)
        self.update_dropdown()
        self.refresh_score()

    def get_games_from_turnier(self):
        game_list = []
        for game in self.t.games:
            game_list.append(game.name)

        game_list.sort()
        return game_list

    def generate_matches(self):
        self.t.generate_matches()
        self.get_matches_for_game()
        self.refresh_score()

    def update_dropdown(self):
        self.OptionsList = self.get_games_from_turnier()
        self.variable.set(self.OptionsList[0])
        self.opt.destroy()
        self.opt = tk.OptionMenu(self.fr_buttons, self.variable, *self.OptionsList, command=self.set_selection)
        self.opt.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

    def set_selection(self, selection):
        self.selected_game = selection
        self.get_matches_for_game()

    def set_match(self, selection):
        self.selected_match = selection

    def set_result_for_match(self):
        for game in self.t.games:
            if game.name == self.selected_game:
                if game.type == "AvA":
                    r = ResultDisplayAvA(self.t, self.selected_game, self.num_matches, self.list_of_matches)
                    r.run()
                else:
                    r = ResultDisplayXvX(self.t, self.selected_game, self.num_matches, self.list_of_matches)
                    r.run()

        self.get_matches_for_game()
        self.refresh_score()

    def players_to_games(self):
        r = PlayersToGamesDisplay(self.t)
        r.run()
        self.t.save_current_turnier()
        self.update_dropdown()

    def get_matches_for_game(self):
        self.list_of_matches = []
        filename = "save/matches/" + self.selected_game + ".txt"
        current_game = Game("", "", self)
        for game in self.t.games:
            if game.name == self.selected_game:
                current_game = game

        if os.path.exists(filename):

            matches_text = current_game.name + ":\n"

            if len(current_game.matches) == 0:
                matches_text += "Not enough Players\n\n"
            else:
                longest_match = ""
                for match in current_game.matches:
                    if match.team2 != []:
                        team1string = ""
                        for person in match.team1:
                            team1string += person.get_name_with_id() + " "

                        team2string = ""
                        for person in match.team2:
                            team2string += person.get_name_with_id() + " "

                        current_match = team1string + "gegen " + team2string

                        if len(current_match) > len(longest_match):
                            longest_match = current_match

                for match in current_game.matches:
                    if match.team2 != []:
                        team1string = ""
                        for person in match.team1:
                            team1string += person.get_name_with_id() + " "

                        team2string = ""
                        for person in match.team2:
                            team2string += person.get_name_with_id() + " "

                        winner = ""
                        if match.team1_score == match.team2_score:
                            winner = "-"
                        elif match.team1_score > match.team2_score:
                            winner = team1string
                        elif match.team1_score < match.team2_score:
                            winner = team2string

                        current_match = team1string + "gegen " + team2string
                        tab_spaces = "\t"
                        len_longest = len(longest_match)

                        len_current = len(current_match)

                        len_added = 8 - len_current % 8

                        sum_len_longest = len_longest + (8 - len_longest % 8)
                        sum_len_current = len_current + len_added
                        num_tabs = int((sum_len_longest - sum_len_current) / 8)

                        for i in range(num_tabs):
                            tab_spaces += "\t"
                            len_added += 8

                        matches_text += team1string + "gegen " + team2string + tab_spaces \
                                        + "| winner = " + winner + "\n"

                        self.list_of_matches.append(current_match)
                    else:
                        team1string = ""
                        for person in match.team1:
                            if person != match.team1[len(match.team1) - 1]:
                                team1string += person.Vorname + "(" + person.id + ") gegen "
                            else:
                                team1string += person.Vorname + "(" + person.id + ")"

                        if match.winner == []:
                            matches_text += team1string + "| winner = - \n"
                        else:
                            matches_text += team1string + "| winner = "
                            for name in match.winner:
                                matches_text += self.t.get_person_from_id(name).get_name_with_id() + " "

                            matches_text += "\n"

                        current_match = team1string
                        self.list_of_matches.append(current_match)

            self.matches_list.set(matches_text)
            self.num_matches = len(current_game.matches)

        else:
            matches_text = self.selected_game + ":\nNo Matches found\n"
            self.matches_list.set(matches_text)

        self.refresh_score()

    def refresh_score(self):
        p = self.t.calculate_score()
        self.score_string = ""
        for person in p:
            if person.winrate == 1.0:
                self.score_string += person.get_name_with_id() + "\t" + "%.1f" % person.score + "\t" + "%05.1f" % \
                                     (person.winrate * 100) + "%\n"
            else:
                self.score_string += person.get_name_with_id() + "\t" + "%.1f" % person.score + "\t" + "%05.2f" % \
                                     (person.winrate * 100) + "%\n"

        self.persons_vName.set(self.score_string)
