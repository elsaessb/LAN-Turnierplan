import os

from Match import Match


class Game:
    def __init__(self, name, _type, t, points=1):
        self.name = name
        self.type = _type
        self.t = t
        self.matches = []
        self.points = points

    def append_match(self, match):
        for mat in self.matches:
            if mat.team1 == match.team1 and mat.team2 == match.team2 and mat.game == match.game:
                return False

        self.matches.append(match)
        return True

    def clear_matches(self):
        filename = "save/matches/" + self.name + ".txt"
        if os.path.exists(filename):
            f = open(filename, "w+")
            f.truncate(0)
            f.close()
            self.matches = []

    def load_matches(self):
        filename = "save/matches/" + self.name + ".txt"
        if os.path.exists(filename):
            f = open(filename, "r")
            data = f.read()

            lines = data.split(";\n")
            if len(self.matches) != len(lines) - 1:
                for line in lines:
                    words = line.split(",")
                    teams = [[], []]
                    team = 0
                    team1score = 0
                    team2score = 0
                    winner = ""
                    stop = False
                    if len(words) >= 5:
                        for i in range(len(words) - 1):
                            if words[i] == "versus":
                                team = 1
                            elif words[i] == "result":
                                team1score = words[len(words) - 2]
                                team2score = words[len(words) - 1]
                                stop = True
                            elif words[i] == "winner":
                                winner = words[len(words) - 1]
                                stop = True
                            elif not stop:
                                person = self.t.get_person_from_id(words[i])
                                teams[team].append(person)

                        match = Match(teams[0], teams[1], self)
                        match.set_winner_AvA(winner)
                        match.set_winner_XvX(team1score, team2score)

                        if match not in self.matches:
                            self.matches.append(match)

            f.close()
        else:
            print("ERROR: File " + filename + " not found")

    def write_matches(self):
        if not os.path.exists("save/matches/"):
            os.makedirs("save/matches")
        filename = "save/matches/" + self.name + ".txt"
        f = open(filename, "a")

        if self.matches != []:
            for match in self.matches:
                if match.game.type != "AvA":
                    teamNames1 = ""
                    for person in match.team1:
                        teamNames1 += person.id + ","

                    teamNames2 = ""
                    for person in match.team2:
                        teamNames2 += "," + person.id

                    message = teamNames1 + "versus" + teamNames2 + ",result," + str(match.team1_score) + "," + str(
                        match.team2_score) + ";\n"
                    f.write(message)

                if match.game.type == "AvA":
                    teamNames1 = ""
                    for person in match.team1:
                        teamNames1 += person.id + ","

                    message = teamNames1 + "winner," + str(match.winner) + ";\n"
                    f.write(message)
        else:
            print("Game " + self.name + " has no Matches")
        f.close()

    def write_match(self, match):
        filename = "save/matches/" + self.name + ".txt"
        f = open(filename, "r")

        data = f.read()

        f.close()
        search_string = ""
        if self.type != "AvA":
            for person in match.team1:
                search_string += person.id + ","

            search_string += "versus,"

            for person in match.team2:
                search_string += person.id + ","

            search_string += "result,"
            pos_match = data.find(search_string)
            pos_endl = data.find(";", pos_match)
            pos_score = data.find(",", pos_match + len(search_string) - 1)

            old_string = data[pos_match:pos_endl + 1]
            new_string = data[pos_match:pos_score + 1] + match.team1_score + "," + match.team2_score + ";"
            new_data = data.replace(old_string, new_string)

        else:
            for person in match.team1:
                search_string += person.id + ","

            search_string += "winner,"
            pos_match = data.find(search_string)
            pos_endl = data.find(";", pos_match)
            pos_score = data.find(",", pos_match + len(search_string) - 1)

            old_string = data[pos_match:pos_endl + 1]
            new_string = data[pos_match:pos_score + 1] + match.winner + ";"
            new_data = data.replace(old_string, new_string)

        f = open(filename, "w")
        f.write(new_data)
        f.close()

    def get_match_from_string(self, match_string):

        if self.type != "AvA":
            teams_string = match_string.split(" gegen ")
            team1 = teams_string[0].split(" ")
            for player in team1:
                if player == "":
                    team1.remove(player)

            team2 = teams_string[1].split(" ")
            for player in team2:
                if player == "":
                    team2.remove(player)

            for match in self.matches:
                if team1 == match.get_team1_vorname() and team2 == match.get_team2_vorname():
                    return match

        else:
            teams_string = match_string.split(" gegen ")
            for team in teams_string:
                if team == "":
                    teams_string.remove(team)

            team1 = []
            for team in teams_string:
                team1.append(team)

            for match in self.matches:
                if team1 == match.get_team1_vorname():
                    return match

        return -1
