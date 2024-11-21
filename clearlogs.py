import os

# Emplacements courants des fichiers journaux de Windows
locations = [
    r'C:\Windows\Logs',  # Logs système de Windows
    r'C:\Windows\Temp',  # Logs temporaires
    r'C:\ProgramData\Microsoft\Windows\WER\ReportQueue',  # Logs d'erreur
    r'C:\ProgramData\Microsoft\Windows\WER\ReportArchive',  # Archives de logs
]

def scan_log_files():
    """Analyse les emplacements et calcule le nombre de fichiers journaux et leur taille totale."""
    files_to_delete = []
    total_size = 0

    print("\n--- Détails des fichiers journaux trouvés ---")
    for location in locations:
        if os.path.exists(location):
            print(f"\nAnalyse du dossier : {location}")
            for root, dirs, files in os.walk(location):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith(('.log', '.tmp', '.etl')):  # Filtrer les types de fichiers courants
                        try:
                            size = os.path.getsize(file_path)
                            files_to_delete.append((file, file_path, size))
                            total_size += size
                            print(f"  - Trouvé : {file} ({size / 1024:.2f} Ko)")
                        except Exception as e:
                            print(f"  [Erreur] Impossible d'accéder à {file_path} : {e}")
    return files_to_delete, total_size

def clear_log_files(files_to_delete):
    """Supprime les fichiers journaux spécifiés."""
    failed_files = []  # Stocke les fichiers non supprimés
    for file, file_path, size in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Supprimé : {file} ({size / 1024:.2f} Ko)")
        except Exception as e:
            print(f"Erreur avec {file_path} : {e}")
            failed_files.append((file_path, str(e)))

    return failed_files

def main():
    print("Analyse des fichiers journaux de Windows...\n")
    files_to_delete, total_size = scan_log_files()

    # Résumé
    num_files = len(files_to_delete)
    print("\n--- Résumé ---")
    print(f"Nombre de fichiers trouvés : {num_files}")
    print(f"Taille totale : {total_size / (1024 * 1024):.2f} Mo")

    if num_files > 0:
        print("\n--- Liste des fichiers journaux trouvés ---")
        for file, file_path, size in files_to_delete:
            print(f"{file_path} - {size / 1024:.2f} Ko")

        # Demande de confirmation
        confirm = input("\nVoulez-vous supprimer ces fichiers journaux ? (oui/non) : ").strip().lower()
        if confirm in ['oui', 'o', 'yes', 'y']:
            print("\nSuppression en cours...")
            failed_files = clear_log_files(files_to_delete)

            # Résumé des fichiers non supprimés
            if failed_files:
                print("\n--- Fichiers non supprimés ---")
                for file_path, error in failed_files:
                    print(f"{file_path} - Erreur : {error}")
            else:
                print("\nTous les fichiers journaux ont été supprimés avec succès.")

            print("\nSuppression terminée.")
        else:
            print("\nSuppression annulée.")
    else:
        print("Aucun fichier journal à supprimer.")

if __name__ == "__main__":
    main()
