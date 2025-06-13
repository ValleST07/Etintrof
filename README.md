# Etintrof

> Ein 2–4 Spieler Battle Royale Spiel mit Echtzeit-Client-Server-Architektur, entwickelt in Python mit Pygame.

## 📜 Projektbeschreibung

**Etintrof** ist ein dynamisches Multiplayer-Battle-Royale-Spiel für 2 bis 4 Spieler. Das Gameplay ist inspiriert von Spielen wie *Brawl Stars* und wird vollständig in Python mit der **Pygame**-Engine realisiert. Der Fokus liegt auf einer zentralisierten Server-Logik und einer clientseitigen Echtzeitvisualisierung.

## 🎮 Spielprinzip

- **Spielmodus:** Battle Royale (2–4 Spieler)
- **Karte:** 50 x 50 Felder (1 Spieler = 1 Feld)
- **Blocktypen:**
  - `0 = Boden` – begehbar & beschießbar
  - `1 = Mauer` – weder begeh- noch beschießbar
  - `2 = Wasser` – nicht begehbar, aber beschießbar
- **Kamera:** zentriert immer auf den eigenen Spieler
- **UI-Elemente:** Lebensanzeige, Schussstatus, etc.

## 🧱 Technischer Aufbau

### 🖥️ Client (PC)

- Anmelde-UI zur Spielverbindung
- Erfassen und Senden von Eingaben:
  - Bewegung: `WASD`
  - Schussrichtung: Mausbewegung, Linksklick
- Echtzeit-Visualisierung: Spielfeld, Spieler, Projektile, UI
- Empfang von Spieldaten vom Server

### 🖧 Server

- Verarbeitet Spieleraktionen und aktualisiert den Spielzustand
- Projektil- & Kollisionsmanagement
- Berechnet Treffer, Leben, Positionen
- Versendet Spielinformationen an alle Clients

## 🔁 Datenkommunikation

- **Client → Server:**
  - Bewegungsrichtung
  - Mausposition (Schussrichtung)
  - Mausklick (Schuss)
- **Server → Client:**
  - Position und Orientierung aller Spieler und Projektile
  - Lebensstände & Schussstatus

## 👥 Team & Aufgabenverteilung

| Name      | Bereich |
|-----------|---------|
| Paul      | Client  |
| Valentin  | Client  |
| Felix     | Server  |
| Georg     | Server  |

## 🚧 Projektstruktur & Meilensteine

### ✅ Planungsphase

- Definition der Spielmechaniken
- Architektur- und UI-Design
- Aufgabenverteilung

### 🔨 Implementierungsphase

- **Server:** Spiel- und Kollisionslogik, Netzwerkkommunikation
- **Client:** Anmeldung, Eingabeverarbeitung, Visualisierung

### 🔍 Integration & Testing

- End-to-End-Tests der Kommunikation
- Performance-Optimierung

### 📦 Abschluss

- Projektdokumentation
- Präsentation des Spiels

## 🗂️ Backlog

### Client

- [ ] Visualisierung
- [ ] Senden der Eingaben
- [ ] Anmelde-UI

### Server

- [ ] Netzwerkkommunikation
- [ ] Spiellogik
- [ ] Datenversand an Clients

## 🧾 Lizenz

Dieses Projekt ist derzeit **nicht lizenziert**. Eine passende Lizenz kann noch ergänzt werden.
