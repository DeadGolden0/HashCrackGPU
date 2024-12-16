import argparse
import torch
from gpu_worker import hash_passwords_on_gpu
from utils import split_wordlist, cleanup_temp_files, assemble_results

def main():
    parser = argparse.ArgumentParser(description="HashCrack GPU: Multi-GPU hash cracking tool.")
    parser.add_argument("hash", type=str, help="Le hash à casser.")
    parser.add_argument("wordlist", type=str, help="Chemin vers le fichier wordlist.")
    parser.add_argument("--algo", type=str, choices=["sha256", "sha512"], default="sha512", help="Algorithme de hash (par défaut : sha512).")
    parser.add_argument("--salt", type=str, help="Sel optionnel à ajouter avant les mots de passe.")
    parser.add_argument("--progress", action="store_true", help="Afficher une barre de progression.")
    args = parser.parse_args()

    num_gpus = torch.cuda.device_count()
    print(f"🌟 Détection de {num_gpus} GPU(s) disponibles. Préparation...")

    # Diviser la wordlist
    chunks = split_wordlist(args.wordlist, num_gpus)
    print(f"✅ Wordlist divisée en {len(chunks)} chunks pour les GPU.")

    # Lancer les processus GPU
    processes = []
    result_queue = torch.multiprocessing.Queue()

    for gpu_id, chunk_path in enumerate(chunks):
        process = torch.multiprocessing.Process(
            target=hash_passwords_on_gpu,
            args=(gpu_id, args.hash, chunk_path, args.algo, args.salt, result_queue, args.progress)
        )
        processes.append(process)
        process.start()
        print(f"🚀 [GPU {gpu_id}] Traitement démarré avec {chunk_path}...")

    # Attendre la fin des processus
    for process in processes:
        process.join()

    # Rassembler les résultats
    cracked_password = assemble_results(result_queue)

    if cracked_password:
        print(f"🎉 Succès ! Le mot de passe correspondant au hash est : {cracked_password}")
    else:
        print("😔 Échec. Aucun mot de passe correspondant trouvé.")

    # Nettoyage
    cleanup_temp_files(chunks)
    print("✅ Nettoyage terminé.")

if __name__ == "__main__":
    main()
