import subprocess
import os

def run_script(branch, script_name):
    try:
        # Prüfe, ob wir in einem Git-Repo sind
        subprocess.run(["git", "rev-parse", "--git-dir"], check=True, capture_output=True)
        
        # Wechsle Branch
        subprocess.run(["git", "checkout", branch], check=True)
        
        # Starte das Skript
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler: {e.stderr.decode().strip()}")
    finally:
        # Zurück zu main (falls Git-Repo vorhanden)
        try:
            subprocess.run(["git", "checkout", "main"], check=True)
        except:
            pass  # Falls kein Git-Repo, ignoriere

def main():
    print("Welches Programm möchtest du starten?")
    print("1 - Server")
    print("2 - Client")
    choice = input("Gib deine Auswahl ein (1 oder 2): ")

    if choice == "1":
        run_script("server", "server.py")
    elif choice == "2":
        run_script("UI", "MapUITest.py")
    else:
        print("Ungültige Eingabe. Bitte wähle 1 oder 2.")

if __name__ == "__main__":
    main()