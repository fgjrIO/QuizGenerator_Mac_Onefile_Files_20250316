"""
JavaScript code for HTML quiz templates.
"""

def get_javascript_code():
    """
    Returns the JavaScript code for the HTML quiz template.
    
    Returns:
        str: JavaScript code as a string
    """
    return """
    // Configure marked.js to use highlight.js for code blocks
    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(code, {language: lang}).value;
                } catch (err) {
                    console.error(err);
                }
            }
            return hljs.highlightAuto(code).value;
        },
        langPrefix: 'hljs language-',
        breaks: true,
        gfm: true
    });
    
    // Quiz data
    const questions = QUESTIONS_JSON_PLACEHOLDER;
    const microcourseContent = MICROCOURSE_CONTENT_PLACEHOLDER;
    let currentQuestionIndex = 0;
    let userAnswers = new Array(questions.length).fill(null);
    let questionsAnswered = new Array(questions.length).fill(false);
    let showingMicrocourse = false;
    
    // DOM elements
    const questionsContainer = document.getElementById('questionsContainer');
    const questionNav = document.getElementById('questionNav');
    const microcourseTab = document.getElementById('microcourse-tab');
    const microcourseContainer = document.getElementById('microcourseContainer');
    
    // Initialize the quiz
    function initQuiz() {
        // Set up microcourse tab if available
        if (microcourseContent && microcourseTab) {
            // Make microcourse tab active by default
            microcourseTab.classList.add('active');
            showingMicrocourse = true;
            
            // Create microcourse content
            createMicrocourseContent();
            
            // Add click handler for microcourse tab
            microcourseTab.onclick = function() {
                showMicrocourse();
            };
        }
        
        // Create navigation items
        questions.forEach((question, index) => {
            const navItem = document.createElement('div');
            navItem.className = 'nav-item';
            navItem.textContent = `Question ${index + 1}`;
            navItem.onclick = () => navigateToQuestion(index);
            questionNav.appendChild(navItem);
        });
        
        // Create question containers
        questions.forEach((question, index) => {
            const questionContainer = document.createElement('div');
            questionContainer.className = 'question-container';
            questionContainer.id = `question-${index}`;
            
            // Question header
            const questionHeader = document.createElement('div');
            questionHeader.className = 'question-header';
            
            const questionNumber = document.createElement('div');
            questionNumber.className = 'question-number';
            questionNumber.textContent = `Question ${index + 1} of ${questions.length}`;
            questionHeader.appendChild(questionNumber);
            
            questionContainer.appendChild(questionHeader);
            
            // Question text with markdown parsing
            const questionText = document.createElement('div');
            questionText.className = 'question-text markdown-content';
            questionText.innerHTML = marked.parse(question.question);
            questionContainer.appendChild(questionText);
            
            // Options (for multiple choice)
            if (question.type === 'multiple_choice') {
                const optionsList = document.createElement('ul');
                optionsList.className = 'options-list';
                optionsList.id = `options-list-${index}`;
                
                question.options.forEach((option, optionIndex) => {
                    const optionItem = document.createElement('li');
                    optionItem.className = 'option-item markdown-content';
                    optionItem.dataset.index = optionIndex;
                    optionItem.innerHTML = marked.parse(option);
                    optionItem.onclick = function() {
                        if (!questionsAnswered[index]) {
                            selectOption(index, optionIndex);
                        }
                    };
                    optionsList.appendChild(optionItem);
                });
                
                questionContainer.appendChild(optionsList);
            }
            // True/False options
            else if (question.type === 'true_false') {
                const tfContainer = document.createElement('div');
                tfContainer.className = 'true-false-container';
                tfContainer.id = `tf-container-${index}`;
                
                // Create True option
                const trueOption = document.createElement('div');
                trueOption.className = 'tf-option';
                trueOption.dataset.value = 'True';
                trueOption.innerHTML = '<span class="tf-radio"></span><span class="tf-label">True</span>';
                trueOption.onclick = function() {
                    if (!questionsAnswered[index]) {
                        selectTrueFalseOption(index, 'True');
                    }
                };
                
                // Create False option
                const falseOption = document.createElement('div');
                falseOption.className = 'tf-option';
                falseOption.dataset.value = 'False';
                falseOption.innerHTML = '<span class="tf-radio"></span><span class="tf-label">False</span>';
                falseOption.onclick = function() {
                    if (!questionsAnswered[index]) {
                        selectTrueFalseOption(index, 'False');
                    }
                };
                
                tfContainer.appendChild(trueOption);
                tfContainer.appendChild(falseOption);
                questionContainer.appendChild(tfContainer);
            }
            // Cloze (fill-in-the-blank) options
            else if (question.type === 'cloze') {
                const clozeContainer = document.createElement('div');
                clozeContainer.className = 'cloze-container';
                clozeContainer.id = `cloze-container-${index}`;
                
                // Create input field for answer
                const answerInput = document.createElement('input');
                answerInput.type = 'text';
                answerInput.className = 'cloze-input';
                answerInput.id = `cloze-input-${index}`;
                answerInput.placeholder = 'Type your answer here';
                
                // Use both onchange and oninput to ensure the answer is captured
                answerInput.oninput = function() {
                    if (!questionsAnswered[index]) {
                        userAnswers[index] = this.value.trim();
                    }
                };
                
                // Also handle Enter key press
                answerInput.onkeypress = function(e) {
                    if (e.key === 'Enter' && !questionsAnswered[index]) {
                        userAnswers[index] = this.value.trim();
                        checkAnswer(index);
                    }
                };
                
                clozeContainer.appendChild(answerInput);
                questionContainer.appendChild(clozeContainer);
            }
            
            // Feedback message
            const feedbackMessage = document.createElement('div');
            feedbackMessage.className = 'feedback-message';
            feedbackMessage.id = `feedback-${index}`;
            feedbackMessage.style.display = 'none';
            questionContainer.appendChild(feedbackMessage);
            
            // Check answer button
            const checkAnswerButton = document.createElement('button');
            checkAnswerButton.className = 'button primary-button';
            checkAnswerButton.textContent = 'Check Answer';
            checkAnswerButton.id = `check-answer-${index}`;
            checkAnswerButton.onclick = function() {
                checkAnswer(index);
            };
            questionContainer.appendChild(checkAnswerButton);
            
            // Answer section (hidden initially)
            const answerSection = document.createElement('div');
            answerSection.className = 'answer-section';
            answerSection.id = `answer-section-${index}`;
            answerSection.style.display = 'none';
            
            const answerLabel = document.createElement('div');
            answerLabel.className = 'answer-label';
            answerLabel.textContent = 'Correct Answer:';
            answerSection.appendChild(answerLabel);
            
            const answerText = document.createElement('div');
            answerText.className = 'answer-text markdown-content';
            answerText.innerHTML = marked.parse(question.correctAnswer);
            answerSection.appendChild(answerText);
            
            questionContainer.appendChild(answerSection);
            
            // Explanation toggle button (hidden initially)
            const explanationToggle = document.createElement('button');
            explanationToggle.className = 'button secondary-button explanation-toggle';
            explanationToggle.id = `explanation-toggle-${index}`;
            explanationToggle.textContent = 'Show Explanation';
            explanationToggle.style.display = 'none';
            explanationToggle.onclick = function() {
                const explanationSection = document.getElementById(`explanation-section-${index}`);
                if (explanationSection.style.display === 'block') {
                    explanationSection.style.display = 'none';
                    this.textContent = 'Show Explanation';
                } else {
                    explanationSection.style.display = 'block';
                    this.textContent = 'Hide Explanation';
                    // Apply syntax highlighting to the explanation content
                    setTimeout(applyHighlighting, 50);
                }
            };
            questionContainer.appendChild(explanationToggle);
            
            // Explanation section (hidden initially)
            const explanationSection = document.createElement('div');
            explanationSection.className = 'explanation-section';
            explanationSection.id = `explanation-section-${index}`;
            explanationSection.style.display = 'none';
            
            const explanationContent = document.createElement('div');
            explanationContent.className = 'explanation-content markdown-content';
            explanationContent.innerHTML = marked.parse(question.explanation);
            explanationSection.appendChild(explanationContent);
            
            questionContainer.appendChild(explanationSection);
            
            // Navigation buttons
            const buttonGroup = document.createElement('div');
            buttonGroup.className = 'button-group';
            buttonGroup.style.marginTop = '30px';
            
            if (index > 0) {
                const prevButton = document.createElement('button');
                prevButton.className = 'button secondary-button';
                prevButton.textContent = 'Previous Question';
                prevButton.onclick = () => navigateToQuestion(index - 1);
                buttonGroup.appendChild(prevButton);
            } else {
                // Empty div for spacing
                const spacer = document.createElement('div');
                buttonGroup.appendChild(spacer);
            }
            
            if (index < questions.length - 1) {
                const nextButton = document.createElement('button');
                nextButton.className = 'button primary-button';
                nextButton.textContent = 'Next Question';
                nextButton.onclick = () => navigateToQuestion(index + 1);
                buttonGroup.appendChild(nextButton);
            } else {
                const finishButton = document.createElement('button');
                finishButton.className = 'button primary-button';
                finishButton.textContent = 'Finish Quiz';
                finishButton.onclick = () => showResults();
                buttonGroup.appendChild(finishButton);
            }
            
            questionContainer.appendChild(buttonGroup);
            
            questionsContainer.appendChild(questionContainer);
        });
        
        // Show the microcourse first if available, otherwise show the first question
        if (microcourseContent && microcourseContainer) {
            showMicrocourse();
        } else {
            navigateToQuestion(0);
        }
    }
    
    // Create microcourse content
    function createMicrocourseContent() {
        if (!microcourseContent || !microcourseContainer) return;
        
        // Create a container for the microcourse content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'microcourse-content markdown-content';
        contentDiv.innerHTML = marked.parse(microcourseContent);
        
        // Add to the microcourse container
        microcourseContainer.appendChild(contentDiv);
        
        // Add a button to start the quiz
        const startQuizButton = document.createElement('button');
        startQuizButton.className = 'button primary-button';
        startQuizButton.textContent = 'Start Quiz';
        startQuizButton.style.marginTop = '30px';
        startQuizButton.onclick = () => navigateToQuestion(0);
        
        microcourseContainer.appendChild(startQuizButton);
    }
    
    // Show the microcourse
    function showMicrocourse() {
        if (!microcourseContainer) return;
        
        // Hide all questions
        const questionContainers = document.querySelectorAll('.question-container');
        questionContainers.forEach(container => {
            container.classList.remove('active');
        });
        
        // Show the microcourse
        microcourseContainer.style.display = 'block';
        
        // Update navigation
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.classList.remove('active');
        });
        
        // Make microcourse tab active
        if (microcourseTab) {
            microcourseTab.classList.add('active');
        }
        
        showingMicrocourse = true;
        
        // Apply syntax highlighting to the microcourse content
        setTimeout(applyHighlighting, 50);
        
        // Scroll to top
        window.scrollTo(0, 0);
    }
    
    // Select an option for multiple choice
    function selectOption(questionIndex, optionIndex) {
        const optionsList = document.getElementById(`options-list-${questionIndex}`);
        const options = optionsList.querySelectorAll('.option-item');
        
        // Remove selected class from all options
        options.forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selected class to the clicked option
        options[optionIndex].classList.add('selected');
        
        // Store the user's answer
        userAnswers[questionIndex] = optionIndex;
    }
    
    // Select an option for true/false
    function selectTrueFalseOption(questionIndex, value) {
        const tfContainer = document.getElementById(`tf-container-${questionIndex}`);
        const options = tfContainer.querySelectorAll('.tf-option');
        
        // Remove selected class from all options
        options.forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selected class to the clicked option
        const selectedOption = Array.from(options).find(option => option.dataset.value === value);
        if (selectedOption) {
            selectedOption.classList.add('selected');
        }
        
        // Store the user's answer
        userAnswers[questionIndex] = value;
    }
    
    // Check the answer
    function checkAnswer(questionIndex) {
        // For cloze questions, make sure to get the latest value from the input field
        if (questions[questionIndex].type === 'cloze') {
            const clozeInput = document.getElementById(`cloze-input-${questionIndex}`);
            if (clozeInput && clozeInput.value.trim()) {
                userAnswers[questionIndex] = clozeInput.value.trim();
            }
        }
        
        if (userAnswers[questionIndex] === null || userAnswers[questionIndex] === undefined || userAnswers[questionIndex] === '') {
            alert('Please provide an answer before checking.');
            return;
        }
        
        const question = questions[questionIndex];
        const feedbackMessage = document.getElementById(`feedback-${questionIndex}`);
        const checkAnswerButton = document.getElementById(`check-answer-${questionIndex}`);
        const answerSection = document.getElementById(`answer-section-${questionIndex}`);
        const explanationToggle = document.getElementById(`explanation-toggle-${questionIndex}`);
        
        let isCorrect = false;
        
        // Handle different question types
        if (question.type === 'multiple_choice') {
            const optionsList = document.getElementById(`options-list-${questionIndex}`);
            const options = optionsList.querySelectorAll('.option-item');
            
            // Find the correct answer index
            const correctAnswerIndex = question.options.findIndex(option => 
                option === question.correctAnswer);
            
            // Mark the user's answer as correct or incorrect
            const userAnswerIndex = userAnswers[questionIndex];
            isCorrect = userAnswerIndex === correctAnswerIndex;
            
            // Update the UI to show the result
            options.forEach((option, index) => {
                if (index === correctAnswerIndex) {
                    option.classList.add('correct');
                    option.style.borderColor = '#28a745';
                    option.style.backgroundColor = 'rgba(40, 167, 69, 0.1)';
                } else if (index === userAnswerIndex && !isCorrect) {
                    option.classList.add('incorrect');
                    option.style.borderColor = '#dc3545';
                    option.style.backgroundColor = 'rgba(220, 53, 69, 0.1)';
                }
            });
        } 
        else if (question.type === 'true_false') {
            const tfContainer = document.getElementById(`tf-container-${questionIndex}`);
            const options = tfContainer.querySelectorAll('.tf-option');
            
            // Get user's answer and correct answer
            const userAnswer = userAnswers[questionIndex];
            const correctAnswer = question.correctAnswer;
            
            isCorrect = userAnswer === correctAnswer;
            
            // Update the UI to show the result
            options.forEach(option => {
                if (option.dataset.value === correctAnswer) {
                    option.classList.add('correct');
                    option.style.borderColor = '#28a745';
                    option.style.backgroundColor = 'rgba(40, 167, 69, 0.1)';
                } else if (option.dataset.value === userAnswer && !isCorrect) {
                    option.classList.add('incorrect');
                    option.style.borderColor = '#dc3545';
                    option.style.backgroundColor = 'rgba(220, 53, 69, 0.1)';
                }
            });
        }
        else if (question.type === 'cloze') {
            const clozeInput = document.getElementById(`cloze-input-${questionIndex}`);
            
            // Get user's answer and correct answer
            const userAnswer = userAnswers[questionIndex];
            const correctAnswer = question.correctAnswer;
            
            // Case-insensitive comparison
            isCorrect = userAnswer.toLowerCase() === correctAnswer.toLowerCase();
            
            // Update the UI to show the result
            if (isCorrect) {
                clozeInput.classList.add('correct-input');
                clozeInput.style.borderColor = '#28a745';
                clozeInput.style.backgroundColor = 'rgba(40, 167, 69, 0.1)';
            } else {
                clozeInput.classList.add('incorrect-input');
                clozeInput.style.borderColor = '#dc3545';
                clozeInput.style.backgroundColor = 'rgba(220, 53, 69, 0.1)';
            }
            
            // Disable the input
            clozeInput.disabled = true;
        }
        
        // Show feedback message
        feedbackMessage.textContent = isCorrect ? 'Correct! Well done!' : 'Incorrect. See the correct answer below.';
        feedbackMessage.style.color = isCorrect ? '#28a745' : '#dc3545';
        feedbackMessage.style.fontWeight = 'bold';
        feedbackMessage.style.marginTop = '15px';
        feedbackMessage.style.display = 'block';
        
        // Show the answer section and explanation toggle
        answerSection.style.display = 'block';
        explanationToggle.style.display = 'block';
        
        // Disable the check answer button
        checkAnswerButton.disabled = true;
        checkAnswerButton.style.opacity = '0.5';
        
        // Mark this question as answered
        questionsAnswered[questionIndex] = true;
        
        // Apply syntax highlighting
        setTimeout(applyHighlighting, 50);
    }
    
    // Show quiz results
    function showResults() {
        // Hide all questions
        const questionContainers = document.querySelectorAll('.question-container');
        questionContainers.forEach(container => {
            container.classList.remove('active');
        });
        
        // Hide microcourse if showing
        if (showingMicrocourse && microcourseContainer) {
            microcourseContainer.style.display = 'none';
            showingMicrocourse = false;
            
            // Remove active class from microcourse tab
            if (microcourseTab) {
                microcourseTab.classList.remove('active');
            }
        }
        
        // Calculate results
        const answeredCount = questionsAnswered.filter(Boolean).length;
        const correctCount = questionsAnswered.reduce((count, answered, index) => {
            if (answered) {
                const question = questions[index];
                let isCorrect = false;
                
                if (question.type === 'multiple_choice') {
                    const correctAnswerIndex = question.options.findIndex(option => 
                        option === question.correctAnswer);
                    isCorrect = userAnswers[index] === correctAnswerIndex;
                } 
                else if (question.type === 'true_false') {
                    isCorrect = userAnswers[index] === question.correctAnswer;
                }
                else if (question.type === 'cloze') {
                    isCorrect = userAnswers[index].toLowerCase() === question.correctAnswer.toLowerCase();
                }
                
                if (isCorrect) {
                    return count + 1;
                }
            }
            return count;
        }, 0);
        
        const percentageCorrect = Math.round((correctCount / questions.length) * 100);
        
        // Create results container if it doesn't exist
        let resultsContainer = document.getElementById('resultsContainer');
        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'resultsContainer';
            resultsContainer.className = 'results-container';
            questionsContainer.appendChild(resultsContainer);
        } else {
            resultsContainer.innerHTML = ''; // Clear previous results
        }
        
        // Create results header
        const resultsHeader = document.createElement('div');
        resultsHeader.className = 'results-header';
        
        const resultsTitle = document.createElement('h2');
        resultsTitle.textContent = 'Quiz Results';
        resultsHeader.appendChild(resultsTitle);
        
        const resultsSummary = document.createElement('div');
        resultsSummary.className = 'results-summary';
        resultsSummary.innerHTML = `
            <div class="summary-item">
                <span class="summary-label">Total Questions:</span>
                <span class="summary-value">${questions.length}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Correct Answers:</span>
                <span class="summary-value">${correctCount}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Score:</span>
                <span class="summary-value ${percentageCorrect >= 70 ? 'passing-score' : 'failing-score'}">${percentageCorrect}%</span>
            </div>
        `;
        resultsHeader.appendChild(resultsSummary);
        
        resultsContainer.appendChild(resultsHeader);
        
        // Create results table
        const resultsTable = document.createElement('table');
        resultsTable.className = 'results-table';
        
        // Table header
        const tableHeader = document.createElement('thead');
        tableHeader.innerHTML = `
            <tr>
                <th>Question</th>
                <th>Result</th>
                <th>Concept Tested</th>
            </tr>
        `;
        resultsTable.appendChild(tableHeader);
        
        // Table body
        const tableBody = document.createElement('tbody');
        
        questions.forEach((question, index) => {
            const row = document.createElement('tr');
            
            // Question number cell
            const questionCell = document.createElement('td');
            questionCell.textContent = `Question ${index + 1}`;
            questionCell.className = 'question-cell';
            questionCell.onclick = () => navigateToQuestion(index);
            row.appendChild(questionCell);
            
            // Result cell
            const resultCell = document.createElement('td');
            if (questionsAnswered[index]) {
                let isCorrect = false;
                
                if (question.type === 'multiple_choice') {
                    const correctAnswerIndex = question.options.findIndex(option => 
                        option === question.correctAnswer);
                    isCorrect = userAnswers[index] === correctAnswerIndex;
                } 
                else if (question.type === 'true_false') {
                    isCorrect = userAnswers[index] === question.correctAnswer;
                }
                else if (question.type === 'cloze') {
                    isCorrect = userAnswers[index].toLowerCase() === question.correctAnswer.toLowerCase();
                }
                
                resultCell.className = isCorrect ? 'correct-result' : 'incorrect-result';
                resultCell.innerHTML = isCorrect ? 
                    '<span class="result-icon">✓</span> Correct' : 
                    '<span class="result-icon">✗</span> Incorrect';
            } else {
                resultCell.textContent = 'Not answered';
                resultCell.className = 'not-answered';
            }
            row.appendChild(resultCell);
            
            // Concept tested cell
            const conceptCell = document.createElement('td');
            conceptCell.textContent = question.concept_phrase || 'Not specified';
            row.appendChild(conceptCell);
            
            tableBody.appendChild(row);
        });
        
        resultsTable.appendChild(tableBody);
        resultsContainer.appendChild(resultsTable);
        
        // Add button to retake quiz
        const buttonGroup = document.createElement('div');
        buttonGroup.className = 'button-group';
        buttonGroup.style.marginTop = '30px';
        
        const retakeButton = document.createElement('button');
        retakeButton.className = 'button secondary-button';
        retakeButton.textContent = 'Retake Quiz';
        retakeButton.onclick = () => {
            // Reset quiz state
            userAnswers = new Array(questions.length).fill(null);
            questionsAnswered = new Array(questions.length).fill(false);
            
            // Reset UI
            // Reset multiple choice options
            const optionItems = document.querySelectorAll('.option-item');
            optionItems.forEach(item => {
                item.classList.remove('selected', 'correct', 'incorrect');
                item.style.borderColor = '';
                item.style.backgroundColor = '';
            });
            
            // Reset true/false options
            const tfOptions = document.querySelectorAll('.tf-option');
            tfOptions.forEach(option => {
                option.classList.remove('selected', 'correct', 'incorrect');
                option.style.borderColor = '';
                option.style.backgroundColor = '';
            });
            
            // Reset cloze inputs
            const clozeInputs = document.querySelectorAll('.cloze-input');
            clozeInputs.forEach(input => {
                input.value = '';
                input.disabled = false;
                input.classList.remove('correct-input', 'incorrect-input');
                input.style.borderColor = '';
                input.style.backgroundColor = '';
            });
            
            const feedbackMessages = document.querySelectorAll('.feedback-message');
            feedbackMessages.forEach(msg => {
                msg.style.display = 'none';
            });
            
            const answerSections = document.querySelectorAll('.answer-section');
            answerSections.forEach(section => {
                section.style.display = 'none';
            });
            
            const explanationToggles = document.querySelectorAll('.explanation-toggle');
            explanationToggles.forEach(toggle => {
                toggle.style.display = 'none';
                toggle.textContent = 'Show Explanation';
            });
            
            const explanationSections = document.querySelectorAll('.explanation-section');
            explanationSections.forEach(section => {
                section.style.display = 'none';
            });
            
            const checkAnswerButtons = document.querySelectorAll('[id^="check-answer-"]');
            checkAnswerButtons.forEach(button => {
                button.disabled = false;
                button.style.opacity = '1';
            });
            
            // Hide results and show first question
            resultsContainer.style.display = 'none';
            navigateToQuestion(0);
        };
        buttonGroup.appendChild(retakeButton);
        
        // Add button to review answers
        const reviewButton = document.createElement('button');
        reviewButton.className = 'button primary-button';
        reviewButton.textContent = 'Review Answers';
        reviewButton.onclick = () => navigateToQuestion(0);
        buttonGroup.appendChild(reviewButton);
        
        resultsContainer.appendChild(buttonGroup);
        
        // Show results container
        resultsContainer.style.display = 'block';
        
        // Update navigation
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.classList.remove('active');
        });
        
        // Add results tab to navigation if it doesn't exist
        let resultsTab = document.getElementById('results-tab');
        if (!resultsTab) {
            resultsTab = document.createElement('div');
            resultsTab.id = 'results-tab';
            resultsTab.className = 'nav-item active';
            resultsTab.textContent = 'Results';
            resultsTab.onclick = showResults;
            questionNav.appendChild(resultsTab);
        } else {
            resultsTab.classList.add('active');
        }
        
        // Scroll to top
        window.scrollTo(0, 0);
    }
    
    // Navigate to a specific question
    function navigateToQuestion(index) {
        // First, reset all state
        showingMicrocourse = false;
        
        // Hide microcourse container
        if (microcourseContainer) {
            microcourseContainer.style.display = 'none';
        }
        
        // Hide all questions first
        const questionContainers = document.querySelectorAll('.question-container');
        questionContainers.forEach(container => {
            container.classList.remove('active');
        });
        
        // Show the selected question
        const selectedQuestion = document.getElementById(`question-${index}`);
        if (selectedQuestion) {
            selectedQuestion.classList.add('active');
        }
        
        // COMPLETELY RESET ALL NAVIGATION HIGHLIGHTING
        // This is a more aggressive approach to ensure clean state
        
        // 1. First explicitly remove active class from microcourse tab and add deactivated class
        if (microcourseTab) {
            // Force remove the active class using multiple methods to ensure it's gone
            microcourseTab.className = microcourseTab.className.replace(/\bactive\b/g, '').trim();
            microcourseTab.classList.remove('active');
            
            // Set inline style to override any CSS
            microcourseTab.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
            microcourseTab.style.borderLeft = '3px solid transparent';
            
            // Add a debug class to verify our code ran
            microcourseTab.classList.add('deactivated');
            
            // Use a data attribute to mark it as explicitly deactivated
            microcourseTab.dataset.deactivated = 'true';
        }
        
        // 2. Remove active class from ALL navigation items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.className = item.className.replace(/\bactive\b/g, '').trim();
            if (item.classList.contains('active')) {
                item.classList.remove('active');
            }
        });
        
        // 3. Find and activate ONLY the specific question tab
        // First try to find by question number
        let targetQuestionTab = null;
        const questionTabs = document.querySelectorAll('#questionNav .nav-item');
        
        questionTabs.forEach(tab => {
            const itemText = tab.textContent.trim();
            const questionMatch = itemText.match(/Question (\d+)/);
            
            if (questionMatch) {
                const questionNum = parseInt(questionMatch[1]);
                if (questionNum === index + 1) {
                    targetQuestionTab = tab;
                }
            }
        });
        
        // If we found the tab, activate it
        if (targetQuestionTab) {
            targetQuestionTab.classList.add('active');
        } else if (index < questionTabs.length) {
            // Fallback: use the index directly
            questionTabs[index].classList.add('active');
        }
        
        // 4. Final verification - ensure microcourse is NOT active
        setTimeout(() => {
            if (microcourseTab && microcourseTab.classList.contains('active')) {
                console.log("WARNING: Microcourse tab is still active after deactivation attempt");
                // Force remove it one more time
                microcourseTab.className = microcourseTab.className.replace(/\bactive\b/g, '').trim();
            }
        }, 0);
        
        // Update current question index
        currentQuestionIndex = index;
        
        // Apply syntax highlighting to the newly visible question
        setTimeout(applyHighlighting, 50);
        
        // Scroll to top
        window.scrollTo(0, 0);
    }
    
    // Apply highlight.js to all code blocks
    function applyHighlighting() {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }
    
    // Initialize the quiz when the page loads
    window.onload = function() {
        initQuiz();
        
        // Apply syntax highlighting after a short delay to ensure all content is loaded
        setTimeout(applyHighlighting, 100);
        
        // Also apply highlighting when navigating between questions
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', function() {
                setTimeout(applyHighlighting, 100);
            });
        });
        
        // Apply highlighting when showing explanations
        const explanationToggles = document.querySelectorAll('.explanation-toggle');
        explanationToggles.forEach(toggle => {
            toggle.addEventListener('click', function() {
                setTimeout(applyHighlighting, 100);
            });
        });
    };
    """
