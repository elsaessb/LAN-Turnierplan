# LAN-Turnierplan
## TO-DO
Spiele löschen

Spieler löschen

Turnier exportieren/importieren überarbeiten

Punktesystem überarbeiten

## Punktesystem
| Teams               | Alle gegen Alle       |
| ------------------- | --------------------- |
| Pro Sieg 1 Punkt    | Obere Hälfte 1 Punkt  |

|% der Spiele gespielt | Siegesrate in % | Punktebonus |
|--------------------- | --------------- | ----------- |
|<40                   | <50             | nix         |
|<66                   | <50             | 0.1 * (1-Siegesrate) * Matches |
|>=66                  | <50             | 0.2 * (1-Siegesrate) * Matches |
