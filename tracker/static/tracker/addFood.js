function capitalizeFirstLetter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

    function foodinfo() {
    const food_item = document.getElementById('food-name').value;
    const calories = document.getElementById('food-amount').value;

    fetch(`/food/get_food_info/${food_item}`, {})
        .then(response => response.json())
        .then(data => {
            food_api = data.food_api
            const table = document.createElement('table');
            const caption = document.createElement('caption');
            caption.textContent = `${capitalizeFirstLetter(food_api.name)}'s Nutrition details per ${food_api.serving_size_g}g`;
            table.appendChild(caption);

            const tbody = document.createElement('tbody');

            const createTableRow = (label, value) => {
                const row = document.createElement('tr');
                const labelCell = document.createElement('td');
                const valueCell = document.createElement('td');
                labelCell.textContent = label;
                valueCell.textContent = value;
                row.appendChild(labelCell);
                row.appendChild(valueCell);
                return row;
            };

            tbody.appendChild(createTableRow('Calories', food_api.calories));
            tbody.appendChild(createTableRow('Fat Total (g)', food_api.fat_total_g));
            tbody.appendChild(createTableRow('Fat Saturated (g)', food_api.fat_saturated_g));
            tbody.appendChild(createTableRow('Protein (g)', food_api.protein_g));
            tbody.appendChild(createTableRow('Sodium (mg)', food_api.sodium_mg));
            tbody.appendChild(createTableRow('Potassium (mg)', food_api.potassium_mg));
            tbody.appendChild(createTableRow('Cholesterol (mg)', food_api.cholesterol_mg));
            tbody.appendChild(createTableRow('Carbohydrates Total (g)', food_api.carbohydrates_total_g));
            tbody.appendChild(createTableRow('Fiber (g)', food_api.fiber_g));
            tbody.appendChild(createTableRow('Sugar (g)', food_api.sugar_g));

            table.appendChild(tbody);

            table.classList.add('table', 'table-bordered', 'table-striped', 'mx-auto', 'w-75');

            const foodDetailsDiv = document.getElementById('food-details');
            foodDetailsDiv.innerHTML = '';
            foodDetailsDiv.appendChild(table);

            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.classList.add('btn', 'btn-danger');
            removeButton.addEventListener('click', () => {
                foodDetailsDiv.innerHTML = '';
            });

            foodDetailsDiv.appendChild(removeButton);
        });
}