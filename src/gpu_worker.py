import hashlib
import torch
from tqdm import tqdm

def hash_passwords_on_gpu(gpu_id, hash_to_crack, wordlist_path, algorithm="sha512", salt=None, result_queue=None, show_progress=False):
    """
    Attempt to crack a hash using a wordlist on a specific GPU.
    
    :param gpu_id: GPU ID to use.
    :param hash_to_crack: The hash to crack.
    :param wordlist_path: Path to the wordlist file.
    :param algorithm: Hashing algorithm (sha256, sha512).
    :param salt: Optional salt to prepend or append to passwords.
    :param result_queue: Multiprocessing queue to store the result.
    :param show_progress: Whether to show a progress bar.
    """
    try:
        torch.cuda.set_device(gpu_id)
        print(f"🚀 [GPU {gpu_id}] Initialisation...")

        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()

            # Optionnel : Barre de progression
            iterator = tqdm(lines, desc=f"GPU {gpu_id}", unit="password") if show_progress else lines

            for line in iterator:
                password = line.strip()

                # Appliquer le sel si nécessaire
                if salt:
                    password = salt + password

                # Calcul du hash
                password_tensor = torch.tensor(list(password.encode()), device=f'cuda:{gpu_id}')
                hashed_password = hashlib.new(algorithm, password_tensor.cpu().numpy()).hexdigest()

                if hashed_password == hash_to_crack:
                    result_queue.put(password)  # Mettre le résultat dans la queue
                    return

        result_queue.put(None)

    except Exception as e:
        print(f"❌ [GPU {gpu_id}] Erreur : {e}")
        result_queue.put(None)
