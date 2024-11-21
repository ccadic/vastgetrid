import os

# Emplacements courants des fichiers temporaires
locations = [
    os.getenv('TEMP'),  # Dossier temporaire utilisateur
    r'C:\Windows\Temp',  # Dossier temporaire Windows
]

def scan_temp_files():
    """Analyse les emplacements et calcule le nombre de fichiers et leur taille totale."""
    files_to_delete = []
    total_size = 0

    for location in locations:
        if os.path.exists(location):
            print(f"Analyse du dossier : {location}")
            for root, dirs, files in os.walk(location):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        files_to_delete.append(file_path)
                        total_size += size
                    except Exception as e:
                        print(f"Erreur avec {file_path} : {e}")

    return files_to_delete, total_size

def clear_temp_files(files_to_delete):
    """Supprime les fichiers spécifiés."""
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Supprimé : {file_path}")
        except Exception as e:
            print(f"Erreur avec {file_path} : {e}")

def main():
    print("Analyse des fichiers temporaires...")
    files_to_delete, total_size = scan_temp_files()

    # Résumé
    num_files = len(files_to_delete)
    print("\n--- Résumé ---")
    print(f"Nombre de fichiers trouvés : {num_files}")
    print(f"Taille totale : {total_size / (1024 * 1024):.2f} Mo")

    # Demande de confirmation
    if num_files > 0:
        confirm = input("\nVoulez-vous supprimer ces fichiers ? (oui/non) : ").strip().lower()
        if confirm in ['oui', 'o', 'yes', 'y']:
            print("\nSuppression en cours...")
            clear_temp_files(files_to_delete)
            print("\nSuppression terminée.")
        else:
            print("\nSuppression annulée.")
    else:
        print("Aucun fichier temporaire à supprimer.")

if __name__ == "__main__":
    main()
