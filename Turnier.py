from AddGameDisplay import AddGameDisplay
from Game import Game
from Person import Person
from Match import Match
import os
import random


class Turnier:
    def __init__(self):
        self.games = []
        self.persons = []
        self.loaded = False
        self.load_last_turnier()

    def append_game(self, game):
        if game not in self.games:
            self.games.append(game)

    def append_person(self, person):
        if person not in self.persons:
            self.persons.append(person)

    def person_plays(self, _id, vName, nName, played_game):
        for person in self.persons:
            if person.id == _id and person.Vorname == vName and person.Nachname == nName:
                for game in self.games:
                    if game.name == played_game:
                        person.append_game_playing(game)

    def print_person_to_games(self):
        message = ""
        for person in self.persons:
            message += person.Vorname + ","
            for game in person.games_played:
                message += game.name + ","
            print(message)
            message = ""

    def save_current_turnier(self):
        if os.path.exists("turnier_tmp.txt"):
            os.remove("turnier_tmp.txt")
        f = open("turnier_tmp.txt", "a")

        message = ""
        sorted_persons = sorted(self.persons, key=lambda x: x.id, reverse=False)
        for person in sorted_persons:
            message += person.id + "," + person.Vorname + ',' + person.Nachname
            for game in person.games_played:
                message += "," + game.name
            message += ';\n'
            f.write(message)
            message = ""

        f.close()
        self.save_games()

    def save_games(self):
        if os.path.exists("games.txt"):
            os.remove("games.txt")
        f = open("games.txt", "a")

        message = ""
        for game in self.games:
            message += game.name + ',' + game.type + ';\n'
            f.write(message)
            message = ""

        f.close()

    def load_games(self):
        f = open("games.txt", "r")
        gameExists = False
        data = f.read()
        lines = data.split(";\n")
        for line in lines:
            words = line.split(',')
            if len(words) == 2:
                for game in self.games:
                    if words[0] == game.name:
                        gameExists = True

                if not gameExists:
                    self.append_game(Game(words[0], words[1], self))

                # filename = words[0] + ".txt"
                # if os.path.exists(filename):
                #    os.remove(filename)

        f.close()

    def load_last_turnier(self):

        self.load_games()

        idTxt = ""
        vName = ""
        nName = ""

        f = open("turnier_tmp.txt", "r")
        data = f.read()
        lines = data.split(";\n")
        for line in lines:
            words = line.split(',')
            gameExists = False
            personExists = False
            alreadyPlays = False

            if len(words) > 2:
                idTxt = words[0]
                vName = words[1]
                nName = words[2]
                for person in self.persons:
                    if idTxt == person.id and vName == person.Vorname and nName == person.Nachname:
                        personExists = True

                if not personExists:
                    self.append_person(Person(idTxt, vName, nName))

            if len(words) > 3:
                for word in words:
                    if word != idTxt and word != vName and word != nName:
                        for game in self.games:
                            if word == game.name:
                                gameExists = True

                        for person in self.persons:
                            if idTxt == person.id and vName == person.Vorname and nName == person.Nachname:
                                alreadyPlays = person.plays(word)

                        if not alreadyPlays:
                            if gameExists:
                                self.person_plays(idTxt, vName, nName, word)
                            else:
                                r = AddGameDisplay(self, word)
                                _type = r.run()
                                self.append_game(Game(word, _type, self))
                                self.person_plays(idTxt, vName, nName, word)

                        gameExists = False
        f.close()
        for game in self.games:
            game.load_matches()
        self.save_games()

    def write_match_team(self, gamename, team1, team2):
        for game in self.games:
            if game.name == gamename:
                game.append_match(Match(team1, team2, game))

    def generate_matches(self):
        for game in self.games:
            game.clear_matches()

        for game in self.games:
            if game.type == "AvA":
                playing_persons = []
                for person in self.persons:
                    if person.plays(game.name):
                        playing_persons.append(person)

                team1 = []
                if len(playing_persons) >= 2:
                    for person in playing_persons:
                        team1.append(person)
                    self.write_match_team(game.name, team1, [])

            if game.type == "1v1":
                team1 = []
                team2 = []
                playing_persons = []
                for person in self.persons:
                    if person.plays(game.name):
                        playing_persons.append(person)

                if len(playing_persons) >= 2:
                    for p1 in range(len(playing_persons) - 1):
                        for p2 in range(p1 + 1, len(playing_persons)):
                            team1.append(playing_persons[p1])
                            team2.append(playing_persons[p2])
                            self.write_match_team(game.name, team1, team2)
                            team1 = []
                            team2 = []

            elif game.type == "2v2":
                teams = []
                playing_persons = []
                for person in self.persons:
                    if person.plays(game.name):
                        playing_persons.append(person)

                if len(playing_persons) >= 4:
                    if len(playing_persons) % 2 == 1:
                        raise ValueError("Eine Person zu wenig für " + game.name)
                    random.shuffle(playing_persons)
                    for playerNr in range(0, len(playing_persons), 2):
                        teams.append([playing_persons[playerNr], playing_persons[playerNr + 1]])

                    for p1 in range(len(teams) - 1):
                        for p2 in range(p1 + 1, len(teams)):
                            team1 = teams[p1]
                            team2 = teams[p2]
                            self.write_match_team(game.name, team1, team2)

            game.write_matches()

    def get_person_from_id(self, _id):
        for person in self.persons:
            if person.id == _id:
                return person

        raise SyntaxError("Keine Person hat ID '" + _id + "'")

    def calculate_score(self):
        tmp_persons = self.persons
        for person in tmp_persons:
            person.score = 0
            for game in self.games:
                for match in game.matches:
                    if game.type != "AvA":
                        if match.team1_score > match.team2_score:
                            if person in match.team1:
                                person.score += game.points * 1
                        elif match.team1_score < match.team2_score:
                            if person in match.team2:
                                person.score += game.points * 1
                    elif game.type == "AvA":
                        if match.winner == person.id:
                            person.score += game.points * 1

        new_persons_by_id = sorted(tmp_persons, key=lambda x: x.id, reverse=False)
        new_persons = sorted(new_persons_by_id, key=lambda x: (x.key_sort_score()), reverse=True)
        return new_persons
