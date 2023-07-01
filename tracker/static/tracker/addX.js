function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }
    return null;
}

function searchExercise() {
    const exerciseName = document.getElementById('exercise-search').value;
    const minutes = document.getElementById('exercise-minutes').value
    const resultsContainer = document.getElementById('exercise-results');
    resultsContainer.innerHTML = '';

    fetch(`/exercise/search/${exerciseName}/${minutes}`, {})
        .then(response => response.json())
        .then(data => {
            const exerciseList = data.x_api;

            exerciseList.forEach(exercise => {
                const activity = document.createElement('div');
                activity.classList.add('exercise-item');

                console.log(exercise.total_calories);

                const radioInput = document.createElement('input');
                radioInput.type = 'radio';
                radioInput.name = 'exercise';
                radioInput.value = exercise.name;

                radioInput.setAttribute('data-duration', exercise.duration_minutes);
                radioInput.setAttribute('data-calories', exercise.total_calories);

                radioInput.classList.add('x_name');
                activity.appendChild(radioInput);

                const nameLabel = document.createElement('label');
                nameLabel.textContent = exercise.name;
                activity.appendChild(nameLabel);

                resultsContainer.appendChild(activity);
                document.getElementById('add-x-btn').style.display = 'block';
            });
        });
}

function getSelectedExercise() {
    let selectedExerciseValue = null;

    document.querySelectorAll('.x_name').forEach(exercise => {
        if (exercise.checked) {
            selectedExerciseValue = exercise.value;
        }
    });

    return selectedExerciseValue;
}

function getSelectedCalories() {
    // dataset.calories
    let selectedExerciseCalorie = null;

    document.querySelectorAll('.x_name').forEach(exercise => {
        if (exercise.checked) {
            selectedExerciseCalorie = exercise.dataset.calories;
        }
    });

    return selectedExerciseCalorie;
}

function getSelectedDuration() {
    // dataset.duration
    let selectedExerciseDuration = null;

    document.querySelectorAll('.x_name').forEach(exercise => {
        if (exercise.checked) {
            selectedExerciseDuration = exercise.dataset.duration;
        }
    });

    return selectedExerciseDuration;
}

function submitExercise() {
    const exerciseName = getSelectedExercise();
    const minutes = document.getElementById('exercise-minutes').value;

    if (!exerciseName) {
        alert('Please select an exercise.');
        return;
    }

    if (minutes <= 0) {
        alert('Please enter a valid number of minutes.');
        return;
    }

    var url = window.location.href;
    var segments = url.split("/");
    var exerciseType = segments[segments.length - 1];

    console.log(exerciseType)
    var duration = getSelectedDuration()
    var calories = getSelectedCalories()

    console.log(`calories burned: ${calories}, duration: ${duration}`)

    fetch(`/exercise/add_exercise/${exerciseType}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                exerciseName: exerciseName,
                exerciseType: exerciseType,
                minutes: minutes,
                calories: calories
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.getElementById('exercise-link').click()

        });
}