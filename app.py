from flask import Flask, render_template, jsonify, request
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from scipy.optimize import minimize


# Функція для класичної сигмоїдної активації
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# Функція для квантової активації
def quantum_activation(x, num_qubits=1, shots=1024):
    if num_qubits < 1:
        raise ValueError("Кількість кубітів має бути >= 1.")

    # Створюємо квантове коло
    qc = QuantumCircuit(num_qubits, 1)
    for i in range(num_qubits):
        qc.rx(x, i)  # Поворот RX для кожного кубіта
    qc.measure(num_qubits - 1, 0)  # Вимірюємо останній кубіт

    # Виконуємо симуляцію
    simulator = Aer.get_backend('aer_simulator')
    transpiled_circuit = transpile(qc, simulator)
    result = simulator.run(transpiled_circuit, shots=shots).result()
    counts = result.get_counts()

    # Розрахунок ймовірності стану |1⟩
    prob_one = counts.get('1', 0) / sum(counts.values())
    return prob_one


# Генерація значень активації
def generate_activation_values(x_values, activation_fn, kwargs):
    return [activation_fn(x, **kwargs) for x in x_values]


# Ініціалізація Flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    x_values = np.linspace(-np.pi, np.pi, 100)

    # Отримуємо параметри з фронтенду
    num_qubits = int(request.json.get('num_qubits', 1))
    x_offset = float(request.json.get('x_offset', 0))

    # Обчислення функцій
    sigmoid_values = generate_activation_values(x_values, sigmoid, {})
    quantum_values = generate_activation_values(x_values, quantum_activation, {'num_qubits': num_qubits})

    return jsonify({
        'sigmoid_values': sigmoid_values,
        'quantum_values': quantum_values,
        'x_values': x_values.tolist()
    })


if __name__ == '__main__':
    app.run(debug=True)
