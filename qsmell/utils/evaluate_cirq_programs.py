import os
import subprocess
import pandas as pd
from pathlib import Path

# Configuration des chemins
PROJECT_DIR = "/Users/vincent/Documents/École/H25/LOG8490/Rapport de recherche/qsmell-cirq/qsmell/utils"
PROGRAMS_DIR = os.path.join(PROJECT_DIR, "programs")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")

# Liste des programmes Cirq
PROGRAMS = [
    "basic_arithmetic.py",
    "bb84.py",
    "bernstein_vazirani.py",
    "deutsch_jozsa.py",
    "grover.py",
    "hhl.py",
    "hidden_shift_algorithm.py",
    "phase_estimator.py",
    "qaoa.py",
    "quantum_fourier_transform.py",
    "quantum_teleportation.py",
    "qubit_characterizations_example.py",
    "shor.py",
    "simon.py",
    "superdense_coding.py"
]

# Détecteurs QSmell
SMELLS = ["CG", "IM", "IQ", "IdQ", "LC", "LPQ", "NC", "ROC", "AQ"]

# Créer le dossier des résultats s'il n'existe pas
os.makedirs(RESULTS_DIR, exist_ok=True)

# Étape 1 : Exécuter QSmell pour chaque programme et détecteur (directement sur les fichiers .py)
def run_qsmell():
    results = []
    for program in PROGRAMS:
        program_name = Path(program).stem
        program_path = os.path.join(PROGRAMS_DIR, program)
        
        program_results = {"Program": program_name}
        
        for smell in SMELLS:
            # Exécuter QSmell pour le fichier Python
            output_file = os.path.join(RESULTS_DIR, f"{program_name}_{smell}.csv")
            cmd = [
                "qsmell",
                "--smell-metric", smell,
                "--input-file", program_path,
                "--output-file", output_file
            ]
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                # Lire la valeur du smell
                df = pd.read_csv(output_file)
                value = df["value"].iloc[0]
                program_results[smell] = value
                print(f"QSmell exécuté pour {program} ({smell}): value={value}")
            except (subprocess.CalledProcessError, FileNotFoundError, IndexError) as e:
                print(f"Erreur pour {program} ({smell}): {e}")
                program_results[smell] = None
        
        results.append(program_results)
    
    return results

# Étape 2 : Consolider les résultats
def consolidate_results(results):
    df = pd.DataFrame(results)
    output_file = os.path.join(RESULTS_DIR, "qsmell_results.csv")
    df.to_csv(output_file, index=False)
    print(f"Résultats consolidés dans {output_file}")

# Exécution
if __name__ == "__main__":
    print("Étape 1 : Exécution de QSmell sur les fichiers .py")
    results = run_qsmell()
    
    print("\nÉtape 2 : Consolidation des résultats")
    consolidate_results(results)