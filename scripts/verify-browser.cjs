// Run with Playwright installed, or set QUIZ_PLAYWRIGHT_PATH to its package directory.
const { chromium } = require(process.env.QUIZ_PLAYWRIGHT_PATH || 'playwright');
const assert = require('node:assert/strict');
const base = process.env.QUIZ_TEST_URL || 'http://localhost:3000';
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`${base}/#course/mesut_nlp_vize`);
    assert.equal(await page.locator('[data-extra="practice"]').count(), 0);
    await page.locator('[data-extra="classics"]').click();
    assert.equal(await page.locator('.notes-section').count(), 6);
    await page.locator('.notes-section-header').first().click();
    assert.match(await page.locator('#practice-content-0').innerText(), /Kısa cevap:/);
    await page.goto(`${base}/#presentations/mesut_nlp_vize`);
    assert.equal(await page.locator('.notes-section').count(), 5);
    assert.equal(await page.locator('a[download]').count(), 0);
    await page.goto(`${base}/#narration/mesut_nlp_vize`);
    await page.waitForFunction(() => [...document.querySelectorAll('audio')].length === 5 && [...document.querySelectorAll('audio')].every(a => a.readyState >= 1));
    assert.ok(await page.locator('audio').evaluateAll(es => es.every(e => e.duration > 60 && e.duration < 180 && !e.error)));
    await page.goto(`${base}/#quiz/mesut_nlp_vize/0`);
    await page.locator('.option-button').nth(1).click();
    await page.locator('#nextBtn').click();
    await page.reload();
    assert.equal((await page.locator('.progress-text').textContent()).trim(), '2 / 3');
    await page.evaluate(() => navigator.serviceWorker.ready);
    await page.reload();
    await context.setOffline(true);
    await page.reload();
    assert.equal((await page.locator('.progress-text').textContent()).trim(), '2 / 3');
    await page.locator('.option-button').nth(2).click();
    await page.locator('#nextBtn').click();
    await page.locator('.option-button').nth(1).click();
    await page.locator('#nextBtn').click();
    await page.waitForSelector('.results-score');
    assert.equal(await page.locator('.results-score').textContent(), '%100');
    await page.reload();
    assert.equal(await page.locator('.results-score').textContent(), '%100');
    assert.deepEqual(errors, []);
    console.log('PASS: mobile course routes, 6 short classics, 5 summaries, 5 playable audio files, refresh, offline quiz and results');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
