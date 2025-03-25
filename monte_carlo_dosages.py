# Monte Carlo Dosage optimization - Demo
#
#  shows another Monte Carlo based simulation approach for an existing dataset
#  using randomness
#
#  (c) 2025 - Prof. Dr. Markus Graf
#  Faculty of Informatics, University of Applied Sciences Heilbronn
#
#  Gnu GPL 3.0
#

import numpy as np
import matplotlib.pyplot as plt
import json

class Patient:
    def __init__(self, id):
        self.id = id
        self.dosage_received = 0
        self.therapeutic_effect = 0.0
        self.side_effect = 0.0

    def set_data(self, dosage, therapeutic_effect, side_effect):
        self.dosage_received = dosage
        self.therapeutic_effect = therapeutic_effect
        self.side_effect = side_effect

    def to_dict(self):
        return {
            'id': self.id,
            'dosage_received': self.dosage_received,
            'therapeutic_effect': self.therapeutic_effect,
            'side_effect': self.side_effect
        }

    @staticmethod
    def from_dict(data):
        patient = Patient(data['id'])
        patient.set_data(data['dosage_received'], data['therapeutic_effect'], data['side_effect'])
        return patient


# Monte-Carlo-Simulation
def monte_carlo_simulation(patients, n_simulations=10000):
    optimal_dosage = None
    max_effectiveness = -np.inf

    for _ in range(n_simulations):
        # Zufällige Auswahl eines Patienten
        patient = np.random.choice(patients)
        dosage = patient.dosage_received
        therapeutic_effect = patient.therapeutic_effect
        side_effect = patient.side_effect

        # Bewertung der Effektivität (therapeutische Wirkung - Nebenwirkungen)
        effectiveness = therapeutic_effect - side_effect

        # Aktualisierung der optimalen Dosierung
        if effectiveness > max_effectiveness:
            max_effectiveness = effectiveness
            optimal_dosage = dosage

    return optimal_dosage, max_effectiveness

if __name__ == '__main__':
    patients = []
    with open("data/patient_dosage_linear.json", 'r') as file:
        data = json.load(file)
        patients = [Patient.from_dict(item) for item in data]

    optimal_dosage, max_effectiveness = monte_carlo_simulation(patients)

    print(f"Optimale Dosierung: {optimal_dosage:.2f} mg")
    print(f"Maximale Effektivität: {max_effectiveness:.2f}")

    # Visualisierung der Ergebnisse
    dosages = [patient.dosage_received for patient in patients]
    effectiveness = [patient.therapeutic_effect - patient.side_effect for patient in patients]

    plt.figure(figsize=(10, 6))
    plt.scatter(dosages, effectiveness, alpha=0.5, label='Effektivität')
    plt.axvline(optimal_dosage, color='r', linestyle='--', label=f'Optimale Dosierung: {optimal_dosage:.2f} mg')
    plt.xlabel('Dosierung (mg)')
    plt.ylabel('Effektivität (therapeutische Wirkung - Nebenwirkungen)')
    plt.title('Monte-Carlo-Simulation zur Dosierungsoptimierung')
    plt.legend()
    plt.show()