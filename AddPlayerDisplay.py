import tkinter as tk
from Person import Person


class AddPlayerDisplay:
    def __init__(self, t):
        self.window = tk.Tk()
        self.running = True
        self.t = t
        self.max_id = "0"

        for person in self.t.persons:
            if int(person.id) > int(self.max_id):
                self.max_id = person.id
        self.new_player = Person(str((int(self.max_id) + 1)), "", "")
        self.entry = 0

        self.lbl_game = tk.Label(self.window, text="Enter Vorname")
        self.lbl_type = tk.Label(self.window, text="Enter Nachname")

        self.lbl_game.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        self.lbl_type.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

        self.entries = []
        for i in range(2):
            self.entries.append(tk.Entry(self.window))
            self.entries[i].grid(row=1, column=i, sticky="ns", padx=5, pady=5)

        self.btn_set_result = tk.Button(self.window, text="Add Player", command=self.set_result_new_player)
        self.btn_set_result.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.window.update()

    def is_running(self):
        return self.running

    def run(self):
        while self.running:
            self.window.update()
        self.window.destroy()
        return self.entry

    def set_result_new_player(self):
        vName = self.entries[0].get()
        nName = self.entries[1].get()
        print(str(self.max_id) + " " + vName + " " + nName)
        if vName != "" and nName != "":
            self.new_player = Person(str((int(self.max_id) + 1)), vName, nName)
            self.t.append_person(self.new_player)
            self.running = False
        else:
            print("'" + vName + " " + nName + "' is not a valid Name")
