import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Визначення рівнів корисності для різних оцінок
utility = dict(вкрай_погано=0, погано=2, посередньо=5, чудово=8)

# Можливі результати для кожного рішення
outcomes = {
    "ліс": {"дощ": "вкрай_погано", "сухо": "чудово"},
    "дім": {"дощ": "погано", "сухо": "посередньо"}
}

def expected_utility(decision, rain_probability):
    dry_probability = 1 - rain_probability
    outcome_rain = outcomes[decision]["дощ"]
    outcome_dry = outcomes[decision]["сухо"]

    # Обчислення очікуваної корисності
    return rain_probability * utility[outcome_rain] + dry_probability * utility[outcome_dry]

# Налаштування ймовірностей та обчислення корисності для кожного варіанту
rain_probabilities = np.linspace(0, 1, 100)
utility_forest = [expected_utility("ліс", p) for p in rain_probabilities]
utility_home = [expected_utility("дім", p) for p in rain_probabilities]

# Побудова графіка та налаштування його зовнішнього вигляду
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4)
forest_line, = plt.plot(rain_probabilities, utility_forest, 'm', label="Ліс")
home_line, = plt.plot(rain_probabilities, utility_home, 'b', label="Дім")
plt.xlabel('Імовірність дощу')
plt.ylabel('Корисність')
plt.title('Рішення про пікнік')
plt.legend()
plt.grid(True)

# Створення слайдера для регулювання ймовірності дощу
ax_slider = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor='lightgoldenrodyellow')
rain_slider = Slider(ax_slider, 'Імовірність дощу', 0, 1, valinit=0.64)

# Текст для відображення рішення та значень корисності
decision_text = plt.text(0.5, 0.15, '', ha='center', color='red', transform=fig.transFigure)
utility_forest_text = plt.text(0.5, 0.1, '', ha='center', color='m', transform=fig.transFigure)
utility_home_text = plt.text(0.5, 0.05, '', ha='center', color='b', transform=fig.transFigure)

# Функція оновлення для зміни графіка та текстових полів
def update(val):
    rain_prob = rain_slider.val
    expected_forest = expected_utility("ліс", rain_prob)
    expected_home = expected_utility("дім", rain_prob)

    forest_line.set_ydata([expected_utility("ліс", p) for p in rain_probabilities])
    home_line.set_ydata([expected_utility("дім", p) for p in rain_probabilities])

    decision = f"Сидимо вдома :) - {expected_home:.2f}" if expected_home > expected_forest else f"Йдемо в ліс :) - {expected_forest:.2f}"
    decision_text.set_text(f'Рішення: {decision}')
    utility_forest_text.set_text(f'Очікувана корисність (Ліс): {expected_forest:.2f}')
    utility_home_text.set_text(f'Очікувана корисність (Дім): {expected_home:.2f}')
    
    fig.canvas.draw_idle()

# Прив’язка функції оновлення до зміни значення слайдера
rain_slider.on_changed(update)

# Початкове оновлення графіка
update(0.64)

plt.show()
