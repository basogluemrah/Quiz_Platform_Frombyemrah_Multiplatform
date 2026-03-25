const fs = require('fs');
let data = fs.readFileSync('src/data/ai/practice.json', 'utf8');

// The answers look like: <strong>Cevap:</strong> Some Text<br><br>
// Or at the end of the section: <strong>Cevap:</strong> Some Text"

data = data.replace(/<strong>Cevap:<\/strong>\s*([^\<]+)(<br>|")/g, '<strong style="color: #10b981;">Cevap: <span style="font-weight: normal;">$1</span></strong>$2');

fs.writeFileSync('src/data/ai/practice.json', data);
