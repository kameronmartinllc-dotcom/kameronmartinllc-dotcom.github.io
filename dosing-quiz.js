// Insulin Dosing Practice Quiz
// Real nutrition labels database

const foodDatabase = [
    {
        name: "Cheerios Cereal",
        servingSize: "1 cup (28g)",
        servingsPerContainer: 14,
        calories: 100,
        totalCarbs: 20,
        fiber: 3,
        sugars: 1,
        protein: 3,
        portions: [0.5, 1, 1.5, 2]
    },
    {
        name: "Kraft Mac & Cheese",
        servingSize: "1 cup prepared (189g)",
        servingsPerContainer: 3,
        calories: 350,
        totalCarbs: 47,
        fiber: 2,
        sugars: 10,
        protein: 11,
        portions: [0.5, 1, 1.5, 2]
    },
    {
        name: "Apple (Medium)",
        servingSize: "1 medium apple (182g)",
        servingsPerContainer: 1,
        calories: 95,
        totalCarbs: 25,
        fiber: 4,
        sugars: 19,
        protein: 0,
        portions: [0.5, 1, 1.5, 2]
    },
    {
        name: "White Bread",
        servingSize: "2 slices (52g)",
        servingsPerContainer: 10,
        calories: 140,
        totalCarbs: 26,
        fiber: 1,
        sugars: 3,
        protein: 5,
        portions: [1, 2, 3, 4]
    },
    {
        name: "Peanut Butter",
        servingSize: "2 tbsp (32g)",
        servingsPerContainer: 15,
        calories: 190,
        totalCarbs: 7,
        fiber: 2,
        sugars: 3,
        protein: 8,
        portions: [1, 2, 3]
    },
    {
        name: "Orange Juice",
        servingSize: "8 fl oz (240mL)",
        servingsPerContainer: 8,
        calories: 110,
        totalCarbs: 26,
        fiber: 0,
        sugars: 22,
        protein: 2,
        portions: [0.5, 1, 1.5, 2]
    },
    {
        name: "Pizza (Frozen)",
        servingSize: "1/4 pizza (120g)",
        servingsPerContainer: 4,
        calories: 320,
        totalCarbs: 38,
        fiber: 2,
        sugars: 5,
        protein: 13,
        portions: [1, 2, 3]
    },
    {
        name: "Banana (Medium)",
        servingSize: "1 medium banana (118g)",
        servingsPerContainer: 1,
        calories: 105,
        totalCarbs: 27,
        fiber: 3,
        sugars: 14,
        protein: 1,
        portions: [0.5, 1, 1.5, 2]
    },
    {
        name: "Yogurt (Vanilla)",
        servingSize: "1 container (170g)",
        servingsPerContainer: 1,
        calories: 150,
        totalCarbs: 25,
        fiber: 0,
        sugars: 19,
        protein: 6,
        portions: [0.5, 1, 1.5, 2]
    },
    {
        name: "Spaghetti with Sauce",
        servingSize: "1 cup (249g)",
        servingsPerContainer: 4,
        calories: 260,
        totalCarbs: 43,
        fiber: 4,
        sugars: 9,
        protein: 9,
        portions: [0.5, 1, 1.5, 2]
    },
    {
        name: "Granola Bar",
        servingSize: "1 bar (35g)",
        servingsPerContainer: 6,
        calories: 140,
        totalCarbs: 23,
        fiber: 2,
        sugars: 8,
        protein: 3,
        portions: [1, 2, 3]
    },
    {
        name: "Chocolate Chip Cookies",
        servingSize: "3 cookies (34g)",
        servingsPerContainer: 10,
        calories: 160,
        totalCarbs: 22,
        fiber: 1,
        sugars: 11,
        protein: 2,
        portions: [1, 2, 3, 4]
    }
];

// Quiz state
let currentFood = null;
let currentPortion = 1;
let currentBG = 120;
let userSettings = {
    carbRatio: 10,
    correctionFactor: 50,
    targetBG: 100
};
let stats = {
    totalAttempts: 0,
    correctAnswers: 0
};

// Encouragement messages
const encouragementMessages = {
    correct: [
        "Excellent work! You nailed it! 🎉",
        "Perfect calculation! You're getting good at this! 🌟",
        "Outstanding! That's exactly right! 💪",
        "You've got this down! Great job! 🎯",
        "Brilliant! Your math skills are on point! ✨",
        "Spot on! You're a dosing pro! 🏆"
    ],
    close: [
        "So close! You're on the right track! 💡",
        "Almost there! Just a small adjustment needed! 👍",
        "Good effort! You're learning quickly! 📚",
        "Not bad! With practice, you'll get it perfect! 🎓",
        "You're getting warmer! Keep practicing! 🔥"
    ],
    incorrect: [
        "Don't worry, this is tricky! Let's review the calculation together. 🤔",
        "Learning from mistakes makes us better! Let's see where we can improve. 📖",
        "This is tough stuff - let's break it down step by step. 💭",
        "No worries! Even experienced people double-check their doses. 🔍",
        "Keep practicing! Each attempt helps you learn. 🌱"
    ]
};

function startQuiz() {
    // Get user settings
    const carbRatio = parseFloat(document.getElementById('carb-ratio').value);
    const correctionFactor = parseFloat(document.getElementById('correction-factor').value);
    const targetBG = parseFloat(document.getElementById('target-bg').value);

    if (!carbRatio || !correctionFactor || !targetBG) {
        alert('Please fill in all your dosing settings!');
        return;
    }

    if (carbRatio <= 0 || correctionFactor <= 0 || targetBG < 70 || targetBG > 180) {
        alert('Please enter realistic values for your settings.');
        return;
    }

    userSettings = { carbRatio, correctionFactor, targetBG };

    // Hide setup, show quiz
    document.getElementById('setup-section').style.display = 'none';
    document.getElementById('quiz-section').style.display = 'block';
    document.getElementById('stats-section').style.display = 'grid';

    generateQuestion();
}

function generateQuestion() {
    // Clear previous feedback
    document.getElementById('feedback-section').innerHTML = '';

    // Clear input fields
    document.getElementById('carbs-eating').value = '';
    document.getElementById('insulin-carbs').value = '';
    document.getElementById('insulin-correction').value = '';
    document.getElementById('total-dose').value = '';

    // Pick random food
    currentFood = foodDatabase[Math.floor(Math.random() * foodDatabase.length)];

    // Pick random portion
    const portionIndex = Math.floor(Math.random() * currentFood.portions.length);
    currentPortion = currentFood.portions[portionIndex];

    // Generate random blood glucose (80-280)
    currentBG = Math.floor(Math.random() * (280 - 80 + 1)) + 80;

    // Round to nearest 5
    currentBG = Math.round(currentBG / 5) * 5;

    // Update display
    updateScenario();
    renderNutritionLabel();
}

function updateScenario() {
    const portionText = currentPortion === 1
        ? currentFood.servingSize
        : `${currentPortion} servings (${currentPortion} × ${currentFood.servingSize})`;

    document.getElementById('scenario-text').innerHTML =
        `You're about to eat <strong>${currentFood.name}</strong> - ${portionText}`;
    document.getElementById('current-bg').textContent = currentBG;
}

function renderNutritionLabel() {
    const netCarbs = (currentFood.totalCarbs - currentFood.fiber) * currentPortion;
    const totalCarbs = currentFood.totalCarbs * currentPortion;
    const fiber = currentFood.fiber * currentPortion;
    const sugars = currentFood.sugars * currentPortion;
    const protein = currentFood.protein * currentPortion;
    const calories = Math.round(currentFood.calories * currentPortion);

    const html = `
        <div class="nutrition-label">
            <h3>Nutrition Facts</h3>
            <div class="serving-size">
                <strong>Serving Size</strong> ${currentFood.servingSize}
                <br><strong>Servings:</strong> About ${currentFood.servingsPerContainer}
            </div>
            <div class="amount-per-serving">Amount Per Serving</div>
            <div class="calories">
                <span class="calories-label">Calories</span>
                <span class="calories-value">${calories}</span>
            </div>
            <div style="font-size: 0.75rem; font-weight: 600; text-align: right; border-bottom: 5px solid #000; padding-bottom: 4px; margin-bottom: 4px;">
                % Daily Value*
            </div>
            <div class="nutrient-row major">
                <span><strong>Total Carbohydrate</strong> ${Math.round(totalCarbs)}g</span>
                <span>${Math.round((totalCarbs / 275) * 100)}%</span>
            </div>
            <div class="nutrient-row indent">
                <span>Dietary Fiber ${Math.round(fiber)}g</span>
                <span>${Math.round((fiber / 28) * 100)}%</span>
            </div>
            <div class="nutrient-row indent">
                <span>Total Sugars ${Math.round(sugars)}g</span>
                <span></span>
            </div>
            <div class="nutrient-row major" style="border-bottom: 10px solid #000;">
                <span><strong>Protein</strong> ${Math.round(protein)}g</span>
                <span></span>
            </div>
        </div>
    `;

    document.getElementById('nutrition-label').innerHTML = html;
}

function checkAnswer() {
    const userCarbsEating = parseFloat(document.getElementById('carbs-eating').value);
    const userInsulinCarbs = parseFloat(document.getElementById('insulin-carbs').value);
    const userInsulinCorrection = parseFloat(document.getElementById('insulin-correction').value) || 0;
    const userTotalDose = parseFloat(document.getElementById('total-dose').value);

    if (!userCarbsEating || !userInsulinCarbs || userTotalDose === null || userTotalDose === undefined) {
        alert('Please fill in all fields before checking your answer!');
        return;
    }

    // Calculate correct answer
    const correctCarbs = Math.round((currentFood.totalCarbs - currentFood.fiber) * currentPortion);
    const correctInsulinCarbs = parseFloat((correctCarbs / userSettings.carbRatio).toFixed(1));

    const bgDifference = currentBG - userSettings.targetBG;
    const correctInsulinCorrection = bgDifference > 0
        ? parseFloat((bgDifference / userSettings.correctionFactor).toFixed(1))
        : 0;

    const correctTotalDose = parseFloat((correctInsulinCarbs + correctInsulinCorrection).toFixed(1));

    // Check how close they are
    const doseDifference = Math.abs(userTotalDose - correctTotalDose);
    const carbsDifference = Math.abs(userCarbsEating - correctCarbs);

    // Update stats
    stats.totalAttempts++;

    let feedbackType = '';
    let message = '';

    if (doseDifference <= 0.3 && carbsDifference <= 2) {
        // Correct!
        stats.correctAnswers++;
        feedbackType = 'correct';
        message = encouragementMessages.correct[Math.floor(Math.random() * encouragementMessages.correct.length)];
    } else if (doseDifference <= 1 && carbsDifference <= 5) {
        // Close
        feedbackType = 'close';
        message = encouragementMessages.close[Math.floor(Math.random() * encouragementMessages.close.length)];
    } else {
        // Incorrect
        feedbackType = 'incorrect';
        message = encouragementMessages.incorrect[Math.floor(Math.random() * encouragementMessages.incorrect.length)];
    }

    displayFeedback(feedbackType, message, {
        userCarbsEating,
        userInsulinCarbs,
        userInsulinCorrection,
        userTotalDose,
        correctCarbs,
        correctInsulinCarbs,
        correctInsulinCorrection,
        correctTotalDose
    });

    updateStats();
}

function displayFeedback(type, message, data) {
    const icon = type === 'correct' ? '🎉' : type === 'close' ? '💡' : '📖';

    let explanation = `
        <div class="explanation">
            <h4>Step-by-Step Solution:</h4>

            <div class="step">
                <strong>1. Calculate Net Carbs</strong><br>
                Total Carbs (${Math.round(currentFood.totalCarbs * currentPortion)}g) - Fiber (${Math.round(currentFood.fiber * currentPortion)}g) = <strong>${data.correctCarbs}g</strong>
                ${data.userCarbsEating != data.correctCarbs ? `<br><span style="color: var(--warning);">You calculated: ${data.userCarbsEating}g</span>` : '<br><span style="color: var(--success);">✓ You got this right!</span>'}
            </div>

            <div class="step">
                <strong>2. Calculate Insulin for Carbs</strong><br>
                ${data.correctCarbs}g ÷ ${userSettings.carbRatio} (your carb ratio) = <strong>${data.correctInsulinCarbs} units</strong>
                ${Math.abs(data.userInsulinCarbs - data.correctInsulinCarbs) > 0.3 ? `<br><span style="color: var(--warning);">You calculated: ${data.userInsulinCarbs} units</span>` : '<br><span style="color: var(--success);">✓ You got this right!</span>'}
            </div>

            <div class="step">
                <strong>3. Calculate Correction Dose</strong><br>
                Current BG (${currentBG}) - Target BG (${userSettings.targetBG}) = ${currentBG - userSettings.targetBG}mg/dL difference<br>
                ${currentBG - userSettings.targetBG > 0
                    ? `${currentBG - userSettings.targetBG} ÷ ${userSettings.correctionFactor} (your ISF) = <strong>${data.correctInsulinCorrection} units</strong>`
                    : 'No correction needed (BG is at or below target) = <strong>0 units</strong>'
                }
                ${Math.abs(data.userInsulinCorrection - data.correctInsulinCorrection) > 0.3 ? `<br><span style="color: var(--warning);">You calculated: ${data.userInsulinCorrection} units</span>` : '<br><span style="color: var(--success);">✓ You got this right!</span>'}
            </div>

            <div class="step">
                <strong>4. Total Dose</strong><br>
                ${data.correctInsulinCarbs} (carbs) + ${data.correctInsulinCorrection} (correction) = <strong>${data.correctTotalDose} units</strong>
                ${Math.abs(data.userTotalDose - data.correctTotalDose) > 0.3 ? `<br><span style="color: var(--warning);">You calculated: ${data.userTotalDose} units (difference of ${Math.abs(data.userTotalDose - data.correctTotalDose).toFixed(1)} units)</span>` : '<br><span style="color: var(--success);">✓ Perfect!</span>'}
            </div>
        </div>
    `;

    const html = `
        <div class="feedback ${type}">
            <div class="feedback-icon">${icon}</div>
            <h3>${message}</h3>
            <p><strong>The correct dose is ${data.correctTotalDose} units</strong></p>
            ${explanation}
        </div>
    `;

    document.getElementById('feedback-section').innerHTML = html;
}

function updateStats() {
    document.getElementById('total-attempts').textContent = stats.totalAttempts;
    document.getElementById('correct-count').textContent = stats.correctAnswers;

    const accuracy = stats.totalAttempts > 0
        ? Math.round((stats.correctAnswers / stats.totalAttempts) * 100)
        : 0;
    document.getElementById('accuracy').textContent = accuracy + '%';
}

function nextQuestion() {
    generateQuestion();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
