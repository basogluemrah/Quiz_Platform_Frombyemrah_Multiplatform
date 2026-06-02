// ===================================
// Quiz Platform - Main Application
// ===================================

import coursesData from './data/courses.json';

// App State
const state = {
  currentView: 'home', // home, units, quiz, results, extras
  selectedCourse: null,
  selectedUnit: null, // can be number or 'mixed'
  questions: [],
  currentQuestionIndex: 0,
  answers: [],
  score: 0
};

// DOM Elements
const app = document.getElementById('app');

// Utility: Shuffle array
function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// Initialize App
async function init() {
  // Handle browser back/forward
  window.addEventListener('hashchange', handleRoute);

  // Initial route
  handleRoute();
}

// Router
function handleRoute() {
  const hash = window.location.hash.slice(1) || 'home';
  const parts = hash.split('/');

  switch (parts[0]) {
    case 'course':
      if (parts[1]) {
        state.selectedCourse = parts[1];
        showUnits();
      }
      break;
    case 'quiz':
      if (parts[1] && parts[2]) {
        state.selectedCourse = parts[1];
        state.selectedUnit = isNaN(parts[2]) ? parts[2] : parseInt(parts[2]);
        startQuiz();
      }
      break;
    case 'extras':
      if (parts[1]) {
        state.selectedCourse = parts[1];
        showExtras();
      }
      break;
    case 'notes':
      if (parts[1]) {
        state.selectedCourse = parts[1];
        showNotes();
      }
      break;
    case 'practice':
      if (parts[1]) {
        state.selectedCourse = parts[1];
        showPractice();
      }
      break;
    case 'results':
      showResults();
      break;
    default:
      showHome();
  }
}

// ===================================
// Views
// ===================================

// Home View - Course Selection
function showHome() {
  state.currentView = 'home';
  state.selectedCourse = null;
  state.selectedUnit = null;

  app.innerHTML = `
    <div class="header">
      <h1>🎓 Quiz Platformu</h1>
      <p>Sınavlarına hazırlanmak için ders seç ve teste başla!</p>
    </div>
    
    <div class="courses-grid">
      ${coursesData.courses.map(course => `
        <div class="course-card" data-course="${course.id}" style="--card-accent: ${course.color}">
          <span class="course-icon">${course.icon}</span>
          <h3 class="course-name">${course.name}</h3>
          <p class="course-info">${course.description}</p>
        </div>
      `).join('')}
    </div>
    
    <div class="admin-link-container">
      <a href="/admin.html" class="admin-link">🎛️ Admin Panel</a>
    </div>
  `;

  // Add click handlers
  document.querySelectorAll('.course-card').forEach(card => {
    card.addEventListener('click', () => {
      const courseId = card.dataset.course;
      window.location.hash = `course/${courseId}`;
    });
  });
}

// Units View - Unit Selection
async function showUnits() {
  state.currentView = 'units';

  // Show loading
  app.innerHTML = `
    <div class="loading">
      <div class="loading-spinner"></div>
      <p>Üniteler yükleniyor...</p>
    </div>
  `;

  try {
    // Load units data
    const unitsData = await import(`./data/${state.selectedCourse}/units.json`);
    const course = coursesData.courses.find(c => c.id === state.selectedCourse);

    app.innerHTML = `
      <div class="units-container">
        <button class="back-button" id="backToHome">
          ← Ana Sayfa
        </button>
        
        <div class="header">
          <h1>${course.icon} ${course.name}</h1>
          <p>Test olmak istediğin üniteyi seç</p>
        </div>
        
        <!-- Karışık Quiz - Özel Mod -->
        ${unitsData.specialModes ? `
          <div class="special-modes">
            ${unitsData.specialModes.map(mode => `
              <div class="special-mode-card" data-mode="${mode.id}">
                <span class="mode-icon">${mode.icon}</span>
                <div class="mode-info">
                  <h3 class="mode-name">${mode.name}</h3>
                  <p class="mode-desc">${mode.description}</p>
                </div>
              </div>
            `).join('')}
          </div>
        ` : ''}
        
        <h2 class="section-title">📚 Üniteler</h2>
        <div class="units-grid">
          ${unitsData.units.map(unit => `
            <div class="unit-card" data-unit="${unit.id}">
              <span class="unit-number">${unit.id}</span>
              <span class="unit-name">${unit.name}</span>
            </div>
          `).join('')}
        </div>
        
        <!-- Ekstralar - Ses Dosyaları -->
        ${unitsData.extras ? `
          <h2 class="section-title">📦 Ekstralar</h2>
          <div class="extras-grid">
            ${unitsData.extras.map(extra => `
              <div class="extra-card" data-extra="${extra.id}">
                <span class="extra-icon">${extra.icon}</span>
                <div class="extra-info">
                  <h3 class="extra-name">${extra.name}</h3>
                  <p class="extra-desc">${extra.description}</p>
                </div>
              </div>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `;

    // Add click handlers
    document.getElementById('backToHome').addEventListener('click', () => {
      window.location.hash = 'home';
    });

    // Special modes (mixed quiz)
    document.querySelectorAll('.special-mode-card').forEach(card => {
      card.addEventListener('click', () => {
        const modeId = card.dataset.mode;
        window.location.hash = `quiz/${state.selectedCourse}/${modeId}`;
      });
    });

    // Unit cards
    document.querySelectorAll('.unit-card').forEach(card => {
      card.addEventListener('click', () => {
        const unitId = card.dataset.unit;
        window.location.hash = `quiz/${state.selectedCourse}/${unitId}`;
      });
    });

    // Extras
    document.querySelectorAll('.extra-card').forEach(card => {
      card.addEventListener('click', () => {
        const extraId = card.dataset.extra;
        if (extraId === 'notes') {
          window.location.hash = `notes/${state.selectedCourse}`;
        } else if (extraId === 'practice') {
          window.location.hash = `practice/${state.selectedCourse}`;
        } else {
          window.location.hash = `extras/${state.selectedCourse}`;
        }
      });
    });

  } catch (error) {
    console.error('Error loading units:', error);
    app.innerHTML = `
      <div class="error">
        <p>Üniteler yüklenirken hata oluştu.</p>
        <button class="btn btn-primary" onclick="window.location.hash='home'">Ana Sayfaya Dön</button>
      </div>
    `;
  }
}

// Extras View - Audio Files
async function showExtras() {
  state.currentView = 'extras';

  const course = coursesData.courses.find(c => c.id === state.selectedCourse);

  // Show loading
  app.innerHTML = `
    <div class="loading">
      <div class="loading-spinner"></div>
      <p>Dosyalar yükleniyor...</p>
    </div>
  `;

  try {
    // Load audio files data
    const audioData = await import(`./data/${state.selectedCourse}/audio.json`);
    const files = audioData.files || [];

    app.innerHTML = `
      <div class="extras-container">
        <button class="back-button" id="backToCourse">
          ← Geri Dön
        </button>
        
        <div class="header">
          <h1>🎧 Ses ve Video Dosyaları</h1>
          <p>${course.name} ders anlatımları</p>
        </div>
        
        <div class="media-list">
          ${files.length > 0 ? files.map(file => `
            <div class="media-card">
              <div class="media-header">
                <span class="media-icon">${file.icon}</span>
                <div class="media-info">
                  <h3 class="media-title">${file.title}</h3>
                  <p class="media-desc">${file.description}</p>
                </div>
              </div>
              <div class="media-player">
                ${file.type === 'video' ? `
                  <video controls class="video-player">
                    <source src="/audio/${file.filename}" type="video/mp4">
                    Tarayıcınız video oynatmayı desteklemiyor.
                  </video>
                ` : `
                  <audio controls class="audio-player">
                    <source src="/audio/${file.filename}" type="audio/mp4">
                    Tarayıcınız ses oynatmayı desteklemiyor.
                  </audio>
                `}
              </div>
            </div>
          `).join('') : `
            <div class="audio-empty">
              <span class="empty-icon">📁</span>
              <p>Henüz dosya eklenmemiş.</p>
              <p class="empty-hint">Dosyalar yakında eklenecek!</p>
            </div>
          `}
        </div>
      </div>
    `;

    document.getElementById('backToCourse').addEventListener('click', () => {
      window.location.hash = `course/${state.selectedCourse}`;
    });

  } catch (error) {
    console.error('Error loading audio files:', error);

    app.innerHTML = `
      <div class="extras-container">
        <button class="back-button" id="backToCourse">
          ← Geri Dön
        </button>
        
        <div class="header">
          <h1>🎧 Ses Dosyaları</h1>
          <p>${course.name} ders anlatımları</p>
        </div>
        
        <div class="audio-list">
          <div class="audio-empty">
            <span class="empty-icon">📁</span>
            <p>Henüz ses dosyası eklenmemiş.</p>
            <p class="empty-hint">Ses dosyaları yakında eklenecek!</p>
          </div>
        </div>
      </div>
    `;

    document.getElementById('backToCourse').addEventListener('click', () => {
      window.location.hash = `course/${state.selectedCourse}`;
    });
  }
}

// Notes View - Study Notes
async function showNotes() {
  state.currentView = 'notes';
  const course = coursesData.courses.find(c => c.id === state.selectedCourse);

  app.innerHTML = `
    <div class="loading">
      <div class="loading-spinner"></div>
      <p>Ders notları yükleniyor...</p>
    </div>
  `;

  try {
    const notesData = await import(`./data/${state.selectedCourse}/notes.json`);
    const sections = notesData.sections || [];

    app.innerHTML = `
      <div class="extras-container">
        <button class="back-button" id="backToCourse">
          ← Geri Dön
        </button>
        
        <div class="header">
          <h1>📖 Ders Notları</h1>
          <p>${course.name} - Kapsamlı Ders Notu</p>
        </div>
        
        <div class="notes-list">
          ${sections.map((section, idx) => `
            <div class="notes-section">
              <button class="notes-section-header" data-section="${idx}">
                <span class="notes-section-icon">${section.icon || '📄'}</span>
                <span class="notes-section-title">${section.title}</span>
                <span class="notes-toggle">▼</span>
              </button>
              <div class="notes-section-content" id="notes-content-${idx}" style="display: none;">
                ${section.content.replace(/\n/g, '<br>')}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    document.getElementById('backToCourse').addEventListener('click', () => {
      window.location.hash = `course/${state.selectedCourse}`;
    });

    // Accordion toggle
    document.querySelectorAll('.notes-section-header').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = btn.dataset.section;
        const content = document.getElementById(`notes-content-${idx}`);
        const toggle = btn.querySelector('.notes-toggle');
        if (content.style.display === 'none') {
          content.style.display = 'block';
          toggle.textContent = '▲';
        } else {
          content.style.display = 'none';
          toggle.textContent = '▼';
        }
      });
    });

  } catch (error) {
    console.error('Error loading notes:', error);
    app.innerHTML = `
      <div class="extras-container">
        <button class="back-button" id="backToCourse">← Geri Dön</button>
        <div class="header">
          <h1>📖 Ders Notları</h1>
          <p>${course.name}</p>
        </div>
        <div class="audio-empty">
          <span class="empty-icon">📁</span>
          <p>Henüz ders notu eklenmemiş.</p>
          <p class="empty-hint">Ders notları yakında eklenecek!</p>
        </div>
      </div>
    `;
    document.getElementById('backToCourse').addEventListener('click', () => {
      window.location.hash = `course/${state.selectedCourse}`;
    });
  }
}

// Practice View - Fill in the blank & Real World
async function showPractice() {
  state.currentView = 'practice';
  const course = coursesData.courses.find(c => c.id === state.selectedCourse);

  app.innerHTML = `
    <div class="loading">
      <div class="loading-spinner"></div>
      <p>Pratik soruları yükleniyor...</p>
    </div>
  `;

  try {
    const practiceData = await import(`./data/${state.selectedCourse}/practice.json`);
    const sections = practiceData.sections || [];

    app.innerHTML = `
      <div class="extras-container">
        <button class="back-button" id="backToCourse">
          ← Geri Dön
        </button>
        
        <div class="header">
          <h1>✍️ Pratik Soruları</h1>
          <p>${course.name} - Boşluk Doldurma ve Vaka Analizleri</p>
        </div>
        
        <div class="notes-list">
          ${sections.map((section, idx) => `
            <div class="notes-section">
              <button class="notes-section-header" data-section="${idx}">
                <span class="notes-section-icon">${section.icon || '📝'}</span>
                <span class="notes-section-title">${section.title}</span>
                <span class="notes-toggle">▼</span>
              </button>
              <div class="notes-section-content" id="practice-content-${idx}" style="display: none;">
                ${section.content}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    document.getElementById('backToCourse').addEventListener('click', () => {
      window.location.hash = `course/${state.selectedCourse}`;
    });

    // Accordion toggle
    document.querySelectorAll('.notes-section-header').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = btn.dataset.section;
        const content = document.getElementById(`practice-content-${idx}`);
        const toggle = btn.querySelector('.notes-toggle');
        if (content.style.display === 'none') {
          content.style.display = 'block';
          toggle.textContent = '▲';
        } else {
          content.style.display = 'none';
          toggle.textContent = '▼';
        }
      });
    });

  } catch (error) {
    console.error('Error loading practice:', error);
    app.innerHTML = `
      <div class="extras-container">
        <button class="back-button" id="backToCourse">← Geri Dön</button>
        <div class="header">
          <h1>✍️ Pratik Soruları</h1>
          <p>${course.name}</p>
        </div>
        <div class="audio-empty">
          <span class="empty-icon">📁</span>
          <p>Bu ders için henüz pratik sorusu eklenmemiş.</p>
        </div>
      </div>
    `;
    document.getElementById('backToCourse').addEventListener('click', () => {
      window.location.hash = `course/${state.selectedCourse}`;
    });
  }
}

// Quiz View
async function startQuiz() {
  state.currentView = 'quiz';
  state.currentQuestionIndex = 0;
  state.answers = [];
  state.score = 0;

  // Show loading
  app.innerHTML = `
    <div class="loading">
      <div class="loading-spinner"></div>
      <p>Sorular yükleniyor...</p>
    </div>
  `;

  try {
    // Check if mixed or all mode
    if (state.selectedUnit === 'mixed' || state.selectedUnit === 'all') {
      // Load all units and combine questions
      const unitsData = await import(`./data/${state.selectedCourse}/units.json`);
      let allQuestions = [];

      for (const unit of unitsData.units) {
        try {
          const unitData = await import(`./data/${state.selectedCourse}/unit${unit.id}.json`);
          // Add unit info to each question
          const questionsWithUnit = unitData.questions.map(q => ({
            ...q,
            unitId: unit.id,
            unitName: unit.name
          }));
          allQuestions = allQuestions.concat(questionsWithUnit);
        } catch (e) {
          console.warn(`Could not load unit ${unit.id}`);
        }
      }

      if (state.selectedUnit === 'mixed') {
        // Shuffle and take 20 random questions (or all if less)
        state.questions = shuffleArray(allQuestions).slice(0, 20);
      } else {
        // Shuffle and take all questions
        state.questions = shuffleArray(allQuestions);
      }
    } else {
      // Load specific unit
      const questionsData = await import(`./data/${state.selectedCourse}/unit${state.selectedUnit}.json`);
      state.questions = questionsData.questions;
    }

    showQuestion();

  } catch (error) {
    console.error('Error loading questions:', error);
    app.innerHTML = `
      <div class="error">
        <p>Sorular yüklenirken hata oluştu.</p>
        <button class="btn btn-primary" onclick="window.location.hash='home'">Ana Sayfaya Dön</button>
      </div>
    `;
  }
}

// Show current question
function showQuestion() {
  const question = state.questions[state.currentQuestionIndex];
  const progress = ((state.currentQuestionIndex + 1) / state.questions.length) * 100;
  const selectedAnswer = state.answers[state.currentQuestionIndex];
  const isAnswered = selectedAnswer !== undefined;

  const letters = ['A', 'B', 'C', 'D', 'E'];
  const isMixed = state.selectedUnit === 'mixed' || state.selectedUnit === 'all';

  app.innerHTML = `
    <div class="quiz-container">
      <div class="quiz-header">
        <button class="back-button" id="backToUnits">
          ← ${window.location.hash === '#results' ? 'Sonuçlara Dön' : (isMixed ? 'Çıkış' : 'Ünitelere Dön')}
        </button>
        <div class="quiz-progress">
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${progress}%"></div>
          </div>
          <span class="progress-text">${state.currentQuestionIndex + 1} / ${state.questions.length}</span>
        </div>
      </div>
      
      <div class="question-card">
        ${isMixed && question.unitName ? `<span class="question-unit">📚 ${question.unitName}</span>` : ''}
        <span class="question-number">Soru ${state.currentQuestionIndex + 1}</span>
        <p class="question-text">${question.question}</p>
      </div>
      
      <div class="options-list">
        ${question.options.map((option, index) => {
    let className = 'option-button';
    if (isAnswered) {
      if (index === question.correct) {
        className += ' correct';
      } else if (index === selectedAnswer && selectedAnswer !== question.correct) {
        className += ' incorrect';
      }
    } else if (index === selectedAnswer) {
      className += ' selected';
    }

    return `
            <button class="${className}" data-index="${index}" ${isAnswered ? 'disabled' : ''}>
              <span class="option-letter">${letters[index]}</span>
              <span class="option-text">${option}</span>
            </button>
          `;
  }).join('')}
      </div>
      
      <div class="quiz-actions">
        <button class="btn btn-secondary" id="prevBtn" ${state.currentQuestionIndex === 0 ? 'disabled' : ''}>
          ← Önceki
        </button>
        <button class="btn btn-primary" id="nextBtn" ${!isAnswered ? 'disabled' : ''}>
          ${state.currentQuestionIndex === state.questions.length - 1 ? (window.location.hash === '#results' ? 'Sonuçlara Dön' : 'Sonuçları Gör') : 'Sonraki →'}
        </button>
      </div>
    </div>
  `;

  // Add event listeners
  document.getElementById('backToUnits').addEventListener('click', () => {
    if (window.location.hash === '#results') {
      showResults();
    } else {
      if (confirm('Testten çıkmak istediğinize emin misiniz? İlerlemeniz kaybolacak.')) {
        window.location.hash = `course/${state.selectedCourse}`;
      }
    }
  });

  if (!isAnswered) {
    document.querySelectorAll('.option-button').forEach(btn => {
      btn.addEventListener('click', () => selectAnswer(parseInt(btn.dataset.index)));
    });
  }

  document.getElementById('prevBtn').addEventListener('click', () => {
    if (state.currentQuestionIndex > 0) {
      state.currentQuestionIndex--;
      showQuestion();
    }
  });

  document.getElementById('nextBtn').addEventListener('click', () => {
    if (state.currentQuestionIndex < state.questions.length - 1) {
      state.currentQuestionIndex++;
      showQuestion();
    } else {
      if (window.location.hash === '#results') {
        showResults();
      } else {
        calculateScore();
        window.location.hash = 'results';
      }
    }
  });
}

// Select an answer
function selectAnswer(index) {
  state.answers[state.currentQuestionIndex] = index;
  showQuestion();
}

// Calculate final score
function calculateScore() {
  state.score = 0;
  state.questions.forEach((question, index) => {
    if (state.answers[index] === question.correct) {
      state.score++;
    }
  });
}

// Results View
function showResults() {
  state.currentView = 'results';

  const totalQuestions = state.questions.length;
  const correctAnswers = state.score;
  const incorrectAnswers = totalQuestions - correctAnswers;
  const percentage = Math.round((correctAnswers / totalQuestions) * 100);

  let emoji, message;
  if (percentage >= 80) {
    emoji = '🎉';
    message = 'Harika! Mükemmel bir performans!';
  } else if (percentage >= 60) {
    emoji = '👍';
    message = 'İyi iş! Biraz daha pratik yapabilirsin.';
  } else if (percentage >= 40) {
    emoji = '📚';
    message = 'Daha fazla çalışman gerekiyor.';
  } else {
    emoji = '💪';
    message = 'Vazgeçme! Tekrar dene.';
  }

  app.innerHTML = `
    <div class="results-container">
      <div class="results-card">
        <span class="results-icon">${emoji}</span>
        <div class="results-score">%${percentage}</div>
        <p class="results-text">${message}</p>
        
        <div class="results-stats">
          <div class="stat-item">
            <div class="stat-value">${totalQuestions}</div>
            <div class="stat-label">Toplam Soru</div>
          </div>
          <div class="stat-item">
            <div class="stat-value correct">${correctAnswers}</div>
            <div class="stat-label">Doğru</div>
          </div>
          <div class="stat-item">
            <div class="stat-value incorrect">${incorrectAnswers}</div>
            <div class="stat-label">Yanlış</div>
          </div>
        </div>
      </div>
      
      <div class="results-actions">
        <button class="btn btn-secondary" id="reviewBtn">
          Cevapları İncele
        </button>
        <button class="btn btn-primary" id="retryBtn">
          Tekrar Dene
        </button>
      </div>
      
      <div style="display: flex; flex-direction: column; align-items: center; gap: 0.5rem; margin-top: 2rem;">
        <button class="back-button" id="backToUnitsBtn">
          ← Ünitelere Geri Dön
        </button>
        <button class="back-button" id="homeBtn">
          ← Ana Sayfaya Dön
        </button>
      </div>
    </div>
  `;

  document.getElementById('reviewBtn').addEventListener('click', () => {
    state.currentQuestionIndex = 0;
    showQuestion();
  });

  document.getElementById('retryBtn').addEventListener('click', () => {
    window.location.hash = `quiz/${state.selectedCourse}/${state.selectedUnit}`;
  });

  document.getElementById('backToUnitsBtn').addEventListener('click', () => {
    if (state.selectedCourse) {
      window.location.hash = `course/${state.selectedCourse}`;
    } else {
      window.location.hash = 'home';
    }
  });

  document.getElementById('homeBtn').addEventListener('click', () => {
    window.location.hash = 'home';
  });
}

// Start the app
init();
