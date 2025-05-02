function updatePeopleOptions() {
    const tableSelect = document.getElementById('tableSelect');
    const peopleSelect = document.getElementById('peopleSelect');

    // Отримуємо вибраний столик і його місткість
    const selectedOption = tableSelect.options[tableSelect.selectedIndex];
    const capacity = selectedOption.getAttribute('data-capacity');

    // Очищаємо попередні опції
    peopleSelect.innerHTML = '<option value="" disabled selected>Виберіть кількість людей</option>';

    // Додаємо нові опції залежно від місткості
    for (let i = 1; i <= capacity; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `${i} Людей`;
        peopleSelect.appendChild(option);
    }
}