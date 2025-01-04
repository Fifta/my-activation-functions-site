// script.js

// Функція для класичної сигмоїдної активації
function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
}

// Функція для квантової активації
function quantumActivation(x, numQubits) {
    // Для простоти, просто використовуємо гіпотетичну модель
    let probOne = 0.5 + 0.25 * Math.sin(numQubits * x); // Псевдоквантова функція
    return Math.max(0, Math.min(1, probOne)); // Обмежуємо значення від 0 до 1
}

// Створення змінної для збереження графіка
let chart = null;

// Функція для оновлення графіка
function updateGraph() {
    const xValue = parseFloat(document.getElementById("xValue").value);
    const numQubits = parseInt(document.getElementById("numQubits").value);

    const xValues = [];
    const sigmoidValues = [];
    const quantumValues = [];

    // Створюємо масиви для побудови графіків
    for (let x = -Math.PI; x <= Math.PI; x += 0.1) {
        xValues.push(x);
        sigmoidValues.push(sigmoid(x));
        quantumValues.push(quantumActivation(x, numQubits));
    }

    // Якщо графік вже існує, то видаляємо попередні дані
    if (chart) {
        chart.destroy();
    }

    // Побудова графіка за допомогою Chart.js
    const ctx = document.getElementById('activationChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xValues,
            datasets: [{
                label: 'Класична сигмоїдна функція',
                data: sigmoidValues,
                borderColor: 'red',
                fill: false,
                lineTension: 0.1
            }, {
                label: 'Квантова активація',
                data: quantumValues,
                borderColor: 'blue',
                fill: false,
                lineTension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Вхідне значення X'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Активаційне значення'
                    }
                }
            }
        }
    });
}

// Оновлюємо графік при першому завантаженні сторінки
updateGraph();
