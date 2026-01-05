// ===================================
// Admin Panel - JavaScript
// ===================================

// ===================================
// Password Protection
// ===================================
const ADMIN_PASSWORD = 'quiz2024'; // Şifreyi buradan değiştirebilirsin

function checkPassword() {
    const savedAuth = sessionStorage.getItem('adminAuth');
    if (savedAuth === 'true') return true;
    
    const password = prompt('🔐 Admin Şifresi:');
    if (password === ADMIN_PASSWORD) {
        sessionStorage.setItem('adminAuth', 'true');
        return true;
    } else {
        alert('❌ Yanlış şifre!');
        window.location.href = '/';
        return false;
    }
}

// Check password on page load
if (!checkPassword()) {
    throw new Error('Unauthorized');
}

// ===================================
// Navigation
// ===================================
const navItems = document.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('.section');

navItems.forEach(item => {
    item.addEventListener('click', () => {
        const sectionId = item.dataset.section;

        // Update nav
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');

        // Update sections
        sections.forEach(section => {
            section.classList.remove('active');
            if (section.id === sectionId) {
                section.classList.add('active');
            }
        });
    });
});

// ===================================
// Course Form
// ===================================

document.getElementById('courseForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const courseId = document.getElementById('courseId').value.toLowerCase();
    const courseName = document.getElementById('courseName').value;
    const courseIcon = document.getElementById('courseIcon').value;
    const courseColor = document.getElementById('courseColor').value;
    const courseDesc = document.getElementById('courseDesc').value;

    // Create courses.json content
    const coursesJson = {
        courses: [
            {
                id: courseId,
                name: courseName,
                icon: courseIcon,
                color: courseColor,
                description: courseDesc
            }
        ]
    };

    // Create units.json content
    const unitsJson = {
        courseId: courseId,
        courseName: courseName,
        specialModes: [
            {
                id: "mixed",
                name: "🎲 Karışık Quiz",
                description: "Tüm ünitelerden rastgele sorular",
                icon: "🎲"
            }
        ],
        units: [],
        extras: [
            {
                id: "audio",
                name: "🎧 Ses Dosyaları",
                description: "Ders anlatımları ve notlar",
                icon: "🎧"
            }
        ]
    };

    // Create audio.json content
    const audioJson = {
        files: []
    };

    // Download files
    downloadJson(coursesJson, 'courses.json');
    setTimeout(() => downloadJson(unitsJson, 'units.json'), 500);
    setTimeout(() => downloadJson(audioJson, 'audio.json'), 1000);

    // Show success message
    const output = document.getElementById('courseOutput');
    output.classList.remove('hidden');
    output.querySelector('.file-list').innerHTML = `
    <div class="file-item">✅ courses.json - Ana klasöre koy (src/data/)</div>
    <div class="file-item">✅ units.json - src/data/${courseId}/ klasörüne koy</div>
    <div class="file-item">✅ audio.json - src/data/${courseId}/ klasörüne koy</div>
  `;
});

// ===================================
// Unit Form
// ===================================

document.getElementById('unitForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const courseId = document.getElementById('unitCourseId').value;
    const unitId = parseInt(document.getElementById('unitId').value);
    const unitName = document.getElementById('unitName').value;

    // Show instructions
    alert(`Ünite eklendi!\n\nYapmanız gereken:\n1. src/data/${courseId}/units.json dosyasını aç\n2. "units" dizisine şunu ekle:\n\n{\n  "id": ${unitId},\n  "name": "${unitName}"\n}\n\n3. Ayrıca unit${unitId}.json dosyası oluştur (Sorular bölümünden)`);
});

// ===================================
// Questions Form
// ===================================

let questionCount = 1;

// Add new question
document.getElementById('addQuestion').addEventListener('click', () => {
    questionCount++;
    const container = document.getElementById('questionsContainer');

    const questionHtml = `
    <div class="question-item" data-index="${questionCount - 1}">
      <div class="question-header">
        <span>Soru ${questionCount}</span>
        <button type="button" class="btn-icon remove-question" title="Sil">🗑️</button>
      </div>
      <div class="form-group">
        <label>Soru Metni</label>
        <textarea class="q-text" rows="3" required></textarea>
      </div>
      <div class="options-grid">
        <div class="form-group">
          <label>A)</label>
          <input type="text" class="q-option" data-opt="0" required />
        </div>
        <div class="form-group">
          <label>B)</label>
          <input type="text" class="q-option" data-opt="1" required />
        </div>
        <div class="form-group">
          <label>C)</label>
          <input type="text" class="q-option" data-opt="2" required />
        </div>
        <div class="form-group">
          <label>D)</label>
          <input type="text" class="q-option" data-opt="3" required />
        </div>
        <div class="form-group">
          <label>E)</label>
          <input type="text" class="q-option" data-opt="4" required />
        </div>
      </div>
      <div class="form-group">
        <label>Doğru Cevap</label>
        <select class="q-correct" required>
          <option value="0">A</option>
          <option value="1">B</option>
          <option value="2">C</option>
          <option value="3">D</option>
          <option value="4">E</option>
        </select>
      </div>
    </div>
  `;

    container.insertAdjacentHTML('beforeend', questionHtml);
    updateQuestionNumbers();
});

// Remove question
document.getElementById('questionsContainer').addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-question')) {
        const items = document.querySelectorAll('.question-item');
        if (items.length > 1) {
            e.target.closest('.question-item').remove();
            questionCount--;
            updateQuestionNumbers();
        } else {
            alert('En az bir soru olmalı!');
        }
    }
});

function updateQuestionNumbers() {
    const items = document.querySelectorAll('.question-item');
    items.forEach((item, index) => {
        item.querySelector('.question-header span').textContent = `Soru ${index + 1}`;
        item.dataset.index = index;
    });
}

// Submit questions
document.getElementById('questionForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const courseId = document.getElementById('qCourseId').value;
    const unitId = parseInt(document.getElementById('qUnitId').value);
    const unitName = document.getElementById('qUnitName').value;

    const questions = [];
    const items = document.querySelectorAll('.question-item');

    items.forEach((item, index) => {
        const questionText = item.querySelector('.q-text').value;
        const options = [];
        item.querySelectorAll('.q-option').forEach(opt => {
            options.push(opt.value);
        });
        const correct = parseInt(item.querySelector('.q-correct').value);

        questions.push({
            id: index + 1,
            question: questionText,
            options: options,
            correct: correct
        });
    });

    const unitJson = {
        unitId: unitId,
        unitName: unitName,
        questions: questions
    };

    downloadJson(unitJson, `unit${unitId}.json`);

    alert(`✅ unit${unitId}.json indirildi!\n\nDosyayı şuraya koy:\nsrc/data/${courseId}/unit${unitId}.json`);
});

// ===================================
// Media Form
// ===================================

let mediaCount = 1;

document.getElementById('addMedia').addEventListener('click', () => {
    mediaCount++;
    const container = document.getElementById('mediaContainer');

    const mediaHtml = `
    <div class="media-item" data-index="${mediaCount - 1}">
      <div class="question-header">
        <span>Dosya ${mediaCount}</span>
        <button type="button" class="btn-icon remove-media" title="Sil">🗑️</button>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Başlık</label>
          <input type="text" class="m-title" placeholder="Ders Anlatımı" required />
        </div>
        <div class="form-group">
          <label>Tür</label>
          <select class="m-type" required>
            <option value="audio">🎧 Ses</option>
            <option value="video">🎬 Video</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label>Dosya Adı (public/audio/ içindeki)</label>
        <input type="text" class="m-filename" placeholder="ders_anlatimi.mp3" required />
      </div>
      <div class="form-group">
        <label>Açıklama</label>
        <input type="text" class="m-desc" placeholder="Ders hakkında kısa açıklama" />
      </div>
    </div>
  `;

    container.insertAdjacentHTML('beforeend', mediaHtml);
});

document.getElementById('mediaContainer').addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-media')) {
        const items = document.querySelectorAll('.media-item');
        if (items.length > 1) {
            e.target.closest('.media-item').remove();
            mediaCount--;
        } else {
            alert('En az bir dosya olmalı!');
        }
    }
});

document.getElementById('mediaForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const courseId = document.getElementById('mediaCourseId').value;
    const files = [];
    const items = document.querySelectorAll('.media-item');

    items.forEach((item, index) => {
        const title = item.querySelector('.m-title').value;
        const type = item.querySelector('.m-type').value;
        const filename = item.querySelector('.m-filename').value;
        const desc = item.querySelector('.m-desc').value;

        files.push({
            id: index + 1,
            title: title,
            type: type,
            icon: type === 'video' ? '🎬' : '🎧',
            filename: filename,
            description: desc || title
        });
    });

    const audioJson = { files: files };

    downloadJson(audioJson, 'audio.json');

    alert(`✅ audio.json indirildi!\n\nDosyayı şuraya koy:\nsrc/data/${courseId}/audio.json\n\nAyrıca medya dosyalarını şuraya koy:\npublic/audio/`);
});

// ===================================
// Utility Functions
// ===================================

function downloadJson(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
