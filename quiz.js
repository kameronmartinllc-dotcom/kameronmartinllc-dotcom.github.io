// Type 1 Diabetes Knowledge Quiz
// Quiz data for adults and kids

const quizData = {
  adult: [
    {
      question: "What causes Type 1 Diabetes?",
      type: "multiple",
      options: [
        "Eating too much sugar",
        "An autoimmune attack on pancreatic beta cells",
        "Lack of exercise",
        "Genetic mutation that can be prevented"
      ],
      correct: 1,
      explanation: "Type 1 Diabetes is caused by an autoimmune response where the body's immune system mistakenly attacks and destroys the insulin-producing beta cells in the pancreas."
    },
    {
      question: "Type 1 Diabetes can be prevented with diet and exercise.",
      type: "boolean",
      correct: false,
      explanation: "Unlike Type 2 Diabetes, Type 1 cannot be prevented through lifestyle changes. It's an autoimmune condition with no known prevention method."
    },
    {
      question: "What is the primary hormone that people with Type 1 Diabetes cannot produce?",
      type: "multiple",
      options: [
        "Glucagon",
        "Cortisol",
        "Insulin",
        "Adrenaline"
      ],
      correct: 2,
      explanation: "People with Type 1 Diabetes cannot produce insulin because their pancreatic beta cells have been destroyed by their immune system."
    },
    {
      question: "Hypoglycemia refers to high blood sugar levels.",
      type: "boolean",
      correct: false,
      explanation: "Hypoglycemia means LOW blood sugar (typically below 70 mg/dL). Hyperglycemia refers to HIGH blood sugar levels."
    },
    {
      question: "What is a normal target blood glucose range before meals?",
      type: "multiple",
      options: [
        "40-60 mg/dL",
        "80-130 mg/dL",
        "150-200 mg/dL",
        "200-250 mg/dL"
      ],
      correct: 1,
      explanation: "The American Diabetes Association recommends a target blood glucose range of 80-130 mg/dL before meals for most people with diabetes."
    },
    {
      question: "Insulin must always be injected; it cannot be taken as a pill.",
      type: "boolean",
      correct: true,
      explanation: "Insulin is a protein that would be broken down by stomach acids if taken orally. It must be injected or delivered via an insulin pump."
    },
    {
      question: "What is HbA1c used to measure?",
      type: "multiple",
      options: [
        "Current blood sugar level",
        "Average blood sugar over 2-3 months",
        "Insulin production capacity",
        "Kidney function"
      ],
      correct: 1,
      explanation: "HbA1c (glycated hemoglobin) measures average blood glucose levels over the past 2-3 months, providing a long-term picture of glucose control."
    },
    {
      question: "Children with Type 1 Diabetes will outgrow the condition as they age.",
      type: "boolean",
      correct: false,
      explanation: "Type 1 Diabetes is a lifelong condition. While management strategies may change over time, the condition does not go away."
    },
    {
      question: "What technology continuously monitors glucose levels without finger pricks?",
      type: "multiple",
      options: [
        "Blood pressure monitor",
        "Continuous Glucose Monitor (CGM)",
        "Pulse oximeter",
        "Insulin pump"
      ],
      correct: 1,
      explanation: "A Continuous Glucose Monitor (CGM) uses a small sensor placed under the skin to measure glucose levels continuously throughout the day and night."
    },
    {
      question: "Exercise always lowers blood sugar levels in people with Type 1 Diabetes.",
      type: "boolean",
      correct: false,
      explanation: "While exercise often lowers blood sugar, intense or anaerobic exercise can sometimes raise blood sugar due to stress hormones like adrenaline."
    },
    {
      question: "What is the 'honeymoon phase' in Type 1 Diabetes?",
      type: "multiple",
      options: [
        "The first month after diagnosis when symptoms improve",
        "A temporary period where some insulin production remains",
        "The time before diagnosis when symptoms appear",
        "A vacation period from diabetes management"
      ],
      correct: 1,
      explanation: "The honeymoon phase is a temporary period after diagnosis when the pancreas still produces some insulin, requiring less exogenous insulin."
    },
    {
      question: "Ketones in urine or blood indicate the body is breaking down fat for energy.",
      type: "boolean",
      correct: true,
      explanation: "When the body lacks sufficient insulin to use glucose for energy, it breaks down fat, producing ketones. High ketone levels can lead to diabetic ketoacidosis (DKA)."
    },
    {
      question: "What is the recommended HbA1c target for most adults with Type 1 Diabetes?",
      type: "multiple",
      options: [
        "Below 5.7%",
        "Below 7%",
        "Below 9%",
        "Below 11%"
      ],
      correct: 1,
      explanation: "The American Diabetes Association recommends an HbA1c target of less than 7% for most adults with diabetes, though individual targets may vary."
    }
  ],
  kid: [
    {
      question: "What does your pancreas make that helps your body use food for energy?",
      type: "multiple",
      options: [
        "Insulin",
        "Oxygen",
        "Blood",
        "Vitamins"
      ],
      correct: 0,
      explanation: "Your pancreas makes insulin! In Type 1 Diabetes, the pancreas stops making insulin, so you need to get insulin from injections or a pump."
    },
    {
      question: "You got Type 1 Diabetes because you ate too much candy.",
      type: "boolean",
      correct: false,
      explanation: "This is NOT true! Type 1 Diabetes is NOT caused by eating sugar or candy. Your immune system attacked your pancreas by mistake - nothing you did caused it!"
    },
    {
      question: "What do we call it when your blood sugar is too LOW?",
      type: "multiple",
      options: [
        "Hyper",
        "Hypo",
        "Ketones",
        "HbA1c"
      ],
      correct: 1,
      explanation: "When your blood sugar is too low, we call it 'hypo' or hypoglycemia. This is when you might feel shaky, dizzy, or hungry."
    },
    {
      question: "If you have Type 1 Diabetes, you can still play sports and be active.",
      type: "boolean",
      correct: true,
      explanation: "Absolutely true! Kids with Type 1 Diabetes can do ANY activity - play sports, swim, dance, and more. You just need to check your blood sugar and plan ahead."
    },
    {
      question: "What should you eat or drink if your blood sugar is too low?",
      type: "multiple",
      options: [
        "Water",
        "Vegetables",
        "Juice or glucose tablets",
        "Diet soda"
      ],
      correct: 2,
      explanation: "When your blood sugar is low, you need something with fast-acting sugar like juice, glucose tablets, or candy to bring it back up quickly."
    },
    {
      question: "Only adults can get Type 1 Diabetes.",
      type: "boolean",
      correct: false,
      explanation: "False! Type 1 Diabetes can happen at any age - babies, kids, teenagers, and adults can all get it. Many people are diagnosed as children."
    },
    {
      question: "What does a continuous glucose monitor (CGM) do?",
      type: "multiple",
      options: [
        "Takes your temperature",
        "Checks your blood sugar all day and night",
        "Gives you insulin",
        "Counts your steps"
      ],
      correct: 1,
      explanation: "A CGM is a small sensor that checks your blood sugar all the time - even while you sleep! It sends the numbers to a device or phone so you can see your blood sugar without finger pricks."
    },
    {
      question: "People with Type 1 Diabetes need to avoid all sugar and carbs.",
      type: "boolean",
      correct: false,
      explanation: "False! You can eat sugar and carbs - you just need to count them and give yourself the right amount of insulin. You can enjoy treats just like anyone else!"
    },
    {
      question: "What is an insulin pump?",
      type: "multiple",
      options: [
        "A device that checks blood sugar",
        "A small device that gives insulin all day",
        "A tool for exercising",
        "A medicine you take by mouth"
      ],
      correct: 1,
      explanation: "An insulin pump is a small device you wear that gives you tiny amounts of insulin all day through a tiny tube under your skin. Some kids use pumps instead of shots!"
    },
    {
      question: "You can 'catch' Type 1 Diabetes from someone else like a cold.",
      type: "boolean",
      correct: false,
      explanation: "Definitely false! Type 1 Diabetes is NOT contagious. You can't catch it from anyone, and you can't give it to anyone else. It's safe to share food, hug, and play with anyone!"
    },
    {
      question: "What might you feel if your blood sugar is too HIGH?",
      type: "multiple",
      options: [
        "Very thirsty and needing to pee a lot",
        "Shaky and sweaty",
        "Cold and sleepy",
        "Excited and energetic"
      ],
      correct: 0,
      explanation: "When blood sugar is high, you might feel really thirsty and need to go to the bathroom a lot. You might also feel tired or have a headache."
    },
    {
      question: "Kids with Type 1 Diabetes can go to sleepovers and camp just like other kids.",
      type: "boolean",
      correct: true,
      explanation: "Yes! With proper planning and making sure adults know how to help with diabetes care, you can do sleepovers, go to camp, and do everything other kids do!"
    },
    {
      question: "Which of these has carbs that affect blood sugar?",
      type: "multiple",
      options: [
        "Bread, pasta, and fruit",
        "Water and diet soda",
        "Chicken and fish",
        "Lettuce and cucumber"
      ],
      correct: 0,
      explanation: "Foods like bread, pasta, rice, fruit, and juice have carbohydrates (carbs) that turn into sugar in your body and raise blood sugar. That's why we count carbs!"
    }
  ]
};

// Quiz functionality
class DiabetesQuiz {
  constructor(quizType) {
    this.quizType = quizType; // 'adult' or 'kid'
    this.questions = quizData[quizType];
    this.currentQuestion = 0;
    this.score = 0;
    this.answers = [];
    this.quizComplete = false;
  }

  init() {
    this.renderQuestion();
    this.updateProgress();
  }

  renderQuestion() {
    const question = this.questions[this.currentQuestion];
    const quizContainer = document.getElementById('quiz-container');

    let optionsHTML = '';

    if (question.type === 'multiple') {
      optionsHTML = question.options.map((option, index) => `
        <button class="quiz-option" onclick="quiz.selectAnswer(${index})">
          ${option}
        </button>
      `).join('');
    } else if (question.type === 'boolean') {
      optionsHTML = `
        <button class="quiz-option" onclick="quiz.selectAnswer(true)">True</button>
        <button class="quiz-option" onclick="quiz.selectAnswer(false)">False</button>
      `;
    }

    quizContainer.innerHTML = `
      <div class="quiz-question-container">
        <div class="question-number">Question ${this.currentQuestion + 1} of ${this.questions.length}</div>
        <h3 class="quiz-question">${question.question}</h3>
        <div class="quiz-options">
          ${optionsHTML}
        </div>
      </div>
    `;
  }

  selectAnswer(answer) {
    if (this.quizComplete) return;

    const question = this.questions[this.currentQuestion];
    const isCorrect = question.type === 'multiple'
      ? answer === question.correct
      : answer === question.correct;

    this.answers.push({
      question: question.question,
      userAnswer: answer,
      correct: isCorrect,
      explanation: question.explanation
    });

    if (isCorrect) {
      this.score++;
    }

    this.showFeedback(isCorrect, question.explanation);
  }

  showFeedback(isCorrect, explanation) {
    const quizContainer = document.getElementById('quiz-container');
    const feedbackClass = isCorrect ? 'correct' : 'incorrect';
    const feedbackIcon = isCorrect ? '✓' : '✗';
    const feedbackTitle = isCorrect ? 'Correct!' : 'Incorrect';

    quizContainer.innerHTML = `
      <div class="quiz-feedback ${feedbackClass}">
        <div class="feedback-icon">${feedbackIcon}</div>
        <h3>${feedbackTitle}</h3>
        <p class="feedback-explanation">${explanation}</p>
        <button class="quiz-btn next-btn" onclick="quiz.nextQuestion()">
          ${this.currentQuestion < this.questions.length - 1 ? 'Next Question' : 'See Results'}
        </button>
      </div>
    `;
  }

  nextQuestion() {
    this.currentQuestion++;

    if (this.currentQuestion < this.questions.length) {
      this.renderQuestion();
      this.updateProgress();
    } else {
      this.showResults();
    }
  }

  updateProgress() {
    const progress = ((this.currentQuestion) / this.questions.length) * 100;
    document.getElementById('quiz-progress-bar').style.width = `${progress}%`;
    document.getElementById('quiz-progress-text').textContent =
      `${this.currentQuestion} / ${this.questions.length} completed`;
  }

  showResults() {
    this.quizComplete = true;
    const percentage = Math.round((this.score / this.questions.length) * 100);
    const quizContainer = document.getElementById('quiz-container');

    let performanceMessage = '';
    let performanceClass = '';

    if (percentage >= 90) {
      performanceMessage = "Outstanding! You really know your stuff!";
      performanceClass = "excellent";
    } else if (percentage >= 70) {
      performanceMessage = "Great job! You have a solid understanding!";
      performanceClass = "good";
    } else if (percentage >= 50) {
      performanceMessage = "Not bad! Keep learning and you'll improve!";
      performanceClass = "okay";
    } else {
      performanceMessage = "Keep studying! There's more to learn!";
      performanceClass = "needs-improvement";
    }

    quizContainer.innerHTML = `
      <div class="quiz-results ${performanceClass}">
        <h2>Quiz Complete!</h2>
        <div class="score-display">
          <div class="score-percentage">${percentage}%</div>
          <div class="score-fraction">${this.score} out of ${this.questions.length} correct</div>
        </div>
        <p class="performance-message">${performanceMessage}</p>
        <div class="results-actions">
          <button class="quiz-btn retake-btn" onclick="restartQuiz()">
            <i class="fas fa-redo"></i> Retake Quiz
          </button>
          <button class="quiz-btn review-btn" onclick="quiz.showReview()">
            <i class="fas fa-list"></i> Review Answers
          </button>
        </div>
      </div>
    `;

    // Update progress bar to 100%
    document.getElementById('quiz-progress-bar').style.width = '100%';
    document.getElementById('quiz-progress-text').textContent =
      `${this.questions.length} / ${this.questions.length} completed`;
  }

  showReview() {
    const quizContainer = document.getElementById('quiz-container');

    const reviewHTML = this.answers.map((answer, index) => {
      const resultClass = answer.correct ? 'correct' : 'incorrect';
      const resultIcon = answer.correct ? '✓' : '✗';

      return `
        <div class="review-item ${resultClass}">
          <div class="review-header">
            <span class="review-number">Question ${index + 1}</span>
            <span class="review-result">${resultIcon}</span>
          </div>
          <p class="review-question">${answer.question}</p>
          <p class="review-explanation">${answer.explanation}</p>
        </div>
      `;
    }).join('');

    quizContainer.innerHTML = `
      <div class="quiz-review">
        <h2>Review Your Answers</h2>
        <div class="review-list">
          ${reviewHTML}
        </div>
        <button class="quiz-btn retake-btn" onclick="restartQuiz()">
          <i class="fas fa-redo"></i> Retake Quiz
        </button>
      </div>
    `;
  }
}

// Global quiz instance
let quiz;

function startQuiz(type) {
  document.getElementById('quiz-selector').style.display = 'none';
  document.getElementById('quiz-interface').style.display = 'block';

  // Update title based on quiz type
  const title = type === 'adult' ? 'Adult Knowledge Quiz' : 'Kids Knowledge Quiz';
  document.getElementById('quiz-title').textContent = title;

  quiz = new DiabetesQuiz(type);
  quiz.init();
}

function restartQuiz() {
  const currentType = quiz.quizType;
  quiz = new DiabetesQuiz(currentType);
  quiz.init();
}

function backToSelector() {
  document.getElementById('quiz-selector').style.display = 'flex';
  document.getElementById('quiz-interface').style.display = 'none';
  document.getElementById('quiz-progress-bar').style.width = '0%';
  document.getElementById('quiz-progress-text').textContent = '0 / 0 completed';
}
