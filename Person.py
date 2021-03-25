class Person:
    def __init__(self, _id, vorname, nachname):
        self.id = _id
        self.Vorname = vorname
        self.Nachname = nachname
        self.games_played = []
        self.score = 0
        self.match_count = 0
        self.checkbox_games_vars = []
        self.checkbox_games_name = []
        self.winrate = 0.0

    def append_game_playing(self, game):
        if game not in self.games_played:
            self.games_played.append(game)

    def clear_checkbox_list(self):
        self.checkbox_games_name.clear()
        self.checkbox_games_vars.clear()

    def plays(self, gamename):
        result = False
        for game in self.games_played:
            if game.name == gamename:
                result = True

        return result

    def key_sort_score(self):
        return self.score

    def get_name_with_id(self):
        if len(self.Vorname) <= 4:
            string = self.Vorname + "(" + self.id + ")\t"
        else:
            string = self.Vorname + "(" + self.id + ")"
        return string
