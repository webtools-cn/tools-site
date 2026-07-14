/* ===================================================================
 * 密码生成器 - Chrome 扩展 popup 逻辑
 * 复用工具站 free-toolbase.com/password-generator/ 的核心算法
 * 纯前端，零依赖，数据完全本地处理
 * =================================================================== */
(function () {
  'use strict';

  // ========== 常量 ==========
  const UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const LOWER = 'abcdefghijklmnopqrstuvwxyz';
  const DIGITS = '0123456789';
  const SYMBOLS = '!@#$%^&*()_+-=[]{}|;:,.<>?';
  const SIMILAR = 'l1I0O';

  // ========== DOM 引用 ==========
  const els = {
    passwordText: document.getElementById('passwordText'),
    strengthFill: document.getElementById('strengthFill'),
    strengthValue: document.getElementById('strengthValue'),
    btnGenerate: document.getElementById('btnGenerate'),
    btnCopy: document.getElementById('btnCopy'),
    btnClearHistory: document.getElementById('btnClearHistory'),
    lengthSlider: document.getElementById('lengthSlider'),
    lengthNumber: document.getElementById('lengthNumber'),
    cbUpper: document.getElementById('cbUpper'),
    cbLower: document.getElementById('cbLower'),
    cbDigits: document.getElementById('cbDigits'),
    cbSymbols: document.getElementById('cbSymbols'),
    cbExcludeSimilar: document.getElementById('cbExcludeSimilar'),
    historyList: document.getElementById('historyList'),
    historySection: document.getElementById('historySection'),
  };

  let currentPassword = '';
  let history = [];
  const MAX_HISTORY = 10;

  // ========== 密码学安全随机 ==========
  function secureRandomInt(max) {
    const array = new Uint32Array(1);
    crypto.getRandomValues(array);
    return array[0] % max;
  }

  function shuffleArray(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = secureRandomInt(i + 1);
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  // ========== 熵值计算 ==========
  function calculateEntropy(length, charsetSize) {
    if (!length || !charsetSize) return 0;
    return Math.round(length * Math.log2(charsetSize) * 10) / 10;
  }

  function getStrengthLevel(entropy) {
    if (entropy < 40) return { label: '弱', class: 'weak', pct: Math.min(33, (entropy / 40) * 33), color: '#ef4444' };
    if (entropy < 60) return { label: '中等', class: 'medium', pct: 33 + Math.min(33, ((entropy - 40) / 20) * 33), color: '#f59e0b' };
    if (entropy < 80) return { label: '强', class: 'strong', pct: 66 + Math.min(34, ((entropy - 60) / 20) * 34), color: '#10b981' };
    return { label: '极强', class: 'strong', pct: 100, color: '#10b981' };
  }

  // ========== 获取有效字符集 ==========
  function getCharset() {
    let charset = '';
    if (els.cbUpper.checked) charset += UPPER;
    if (els.cbLower.checked) charset += LOWER;
    if (els.cbDigits.checked) charset += DIGITS;
    if (els.cbSymbols.checked) charset += SYMBOLS;

    if (els.cbExcludeSimilar.checked) {
      charset = charset.split('').filter(c => !SIMILAR.includes(c)).join('');
    }

    return charset;
  }

  // ========== 生成单个密码 ==========
  function generatePassword(length, charset) {
    if (!charset || charset.length === 0) return '';

    // 确保每类字符至少出现一次（如果选了的话）
    const required = [];
    if (els.cbUpper.checked && UPPER.split('').some(c => charset.includes(c))) required.push(UPPER);
    if (els.cbLower.checked && LOWER.split('').some(c => charset.includes(c))) required.push(LOWER);
    if (els.cbDigits.checked && DIGITS.split('').some(c => charset.includes(c))) required.push(DIGITS);
    if (els.cbSymbols.checked && SYMBOLS.split('').some(c => charset.includes(c))) required.push(SYMBOLS);

    const result = [];
    for (const set of required) {
      const valid = set.split('').filter(c => charset.includes(c));
      if (valid.length > 0) result.push(valid[secureRandomInt(valid.length)]);
    }

    while (result.length < length) {
      result.push(charset[secureRandomInt(charset.length)]);
    }

    return shuffleArray(result).join('');
  }

  // ========== 更新密码显示（带动画）==========
  function updatePasswordDisplay(password) {
    els.passwordText.innerHTML = password.split('').map((c, i) =>
      `<span class="char" style="animation-delay:${i * 0.01}s">${c.replace(/</g, '&lt;')}</span>`
    ).join('');
  }

  // ========== 生成并显示 ==========
  function generate() {
    const length = parseInt(els.lengthSlider.value, 10);
    const charset = getCharset();

    if (!charset) {
      els.passwordText.innerHTML = '<span style="color:#ef4444;font-size:11px">请至少选择一种字符类型</span>';
      els.strengthFill.style.width = '0%';
      els.strengthFill.style.background = 'transparent';
      els.strengthValue.textContent = '--';
      els.strengthValue.className = 'strength-value';
      currentPassword = '';
      return;
    }

    currentPassword = generatePassword(length, charset);
    updatePasswordDisplay(currentPassword);

    // 计算熵值
    const entropy = calculateEntropy(currentPassword.length, charset.length);
    const strength = getStrengthLevel(entropy);

    els.strengthFill.style.width = strength.pct + '%';
    els.strengthFill.style.background = strength.color;
    els.strengthValue.textContent = `${entropy} bits - ${strength.label}`;
    els.strengthValue.className = 'strength-value ' + strength.class;

    // 添加到历史记录
    addHistory(currentPassword, entropy, strength.label);
  }

  // ========== 历史记录 ==========
  function addHistory(password, entropy, label) {
    // 去重：如果已经在顶部就不重复添加
    if (history.length > 0 && history[0].password === password) return;

    history.unshift({ password, entropy, label, time: Date.now() });
    if (history.length > MAX_HISTORY) {
      history = history.slice(0, MAX_HISTORY);
    }
    renderHistory();
  }

  function renderHistory() {
    if (history.length === 0) {
      els.historyList.innerHTML = '<div class="history-empty">暂无历史记录，点击生成开始</div>';
      return;
    }

    els.historyList.innerHTML = history.map((item, i) => `
      <div class="history-item">
        <span class="pw" data-pw="${encodeURIComponent(item.password)}">${escapeHtml(truncate(item.password, 28))}</span>
        <button class="cpy-btn" data-pw="${encodeURIComponent(item.password)}">复制</button>
      </div>
    `).join('');

    // 绑定历史项点击复制
    els.historyList.querySelectorAll('.pw').forEach(el => {
      el.addEventListener('click', () => {
        copyToClipboard(decodeURIComponent(el.dataset.pw), el.nextElementSibling);
      });
    });
    els.historyList.querySelectorAll('.cpy-btn').forEach(btn => {
      btn.addEventListener('click', () => copyToClipboard(decodeURIComponent(btn.dataset.pw), btn));
    });
  }

  function clearHistory() {
    history = [];
    renderHistory();
  }

  function truncate(str, len) {
    return str.length > len ? str.slice(0, len) + '…' : str;
  }

  function escapeHtml(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // ========== 复制功能 ==========
  async function copyToClipboard(text, btn) {
    if (!text) return;
    let success = false;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try { await navigator.clipboard.writeText(text); success = true; } catch (e) {}
    }
    if (!success) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { success = document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
    }

    // 找到按钮元素（支持传入null）
    const targetBtn = btn || els.btnCopy;
    const original = targetBtn.textContent;
    targetBtn.textContent = success ? '✅ 已复制' : '❌ 失败';
    if (targetBtn.classList) targetBtn.classList.add('success');
    setTimeout(() => {
      targetBtn.textContent = original;
      if (targetBtn.classList) targetBtn.classList.remove('success');
    }, 1500);
  }

  // ========== 事件绑定 ==========

  // 生成按钮
  els.btnGenerate.addEventListener('click', generate);

  // 复制按钮
  els.btnCopy.addEventListener('click', () => {
    if (!currentPassword) { generate(); return; }
    copyToClipboard(currentPassword, els.btnCopy);
  });

  // 清空历史
  els.btnClearHistory.addEventListener('click', clearHistory);

  // 长度滑块
  els.lengthSlider.addEventListener('input', () => {
    els.lengthNumber.value = els.lengthSlider.value;
    generate();
  });

  // 长度数字输入
  els.lengthNumber.addEventListener('change', () => {
    let v = Math.max(4, Math.min(64, parseInt(els.lengthNumber.value, 10) || 16));
    els.lengthNumber.value = v;
    els.lengthSlider.value = v;
    generate();
  });

  // 字符集复选框
  [els.cbUpper, els.cbLower, els.cbDigits, els.cbSymbols, els.cbExcludeSimilar].forEach(cb => {
    cb.addEventListener('change', generate);
  });

  // 键盘快捷键
  document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT') return;
    if (e.code === 'Space' || e.code === 'Enter') {
      e.preventDefault();
      generate();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'c' && currentPassword) {
      e.preventDefault();
      copyToClipboard(currentPassword, els.btnCopy);
    }
  });

  // 底部链接在新标签打开
  document.getElementById('siteLink').addEventListener('click', function (e) {
    const url = this.href;
    if (chrome && chrome.tabs && chrome.tabs.create) {
      e.preventDefault();
      chrome.tabs.create({ url: url });
    }
  });

  // ========== 初始化 ==========
  renderHistory();
  generate();

})();
