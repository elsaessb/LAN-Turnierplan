class Match:
    def __init__(self, team1, team2, game):
        self.team1 = team1
        self.team2 = team2

        for person in self.team1:
            person.match_count += 1

        for person in self.team2:
            person.match_count += 1

        self.game = game
        self.winner = []
        self.team1_score = 0
        self.team2_score = 0

    def set_winner_XvX(self, team1_score, team2_score):
        self.team1_score = team1_score
        self.team2_score = team2_score

    def set_winner_AvA(self, winner):
        self.winner = winner

    def get_team1_vorname(self):
        name_list = []
        for person in self.team1:
            name_list.append(person.get_name_with_id())

        return name_list

    def get_team2_vorname(self):
        name_list = []
        for person in self.team2:
            name_list.append(person.get_name_with_id())

        return name_list
