
  var presetSelect = document.getElementById('presetSelect');
  var widthVal = document.getElementById('widthVal');
  var heightVal = document.getElementById('heightVal');
  var applyBtn = document.getElementById('applyBtn');
  var bgColor = document.getElementById('bgColor');
  var contentText = document.getElementById('contentText');
  var previewEl = document.getElementById('previewEl');
  var cssOutput = document.getElementById('cssOutput');
  var resultSection = document.getElementById('resultSection');

  function updateAspect() {
    var w = parseFloat(widthVal.value) || 16;
    var h = parseFloat(heightVal.value) || 9;
    var ratio = w / h;
    var bg = bgColor.value;
    var text = contentText.value || w + ':' + h;

    previewEl.style.aspectRatio = w + ' / ' + h;
    previewEl.style.background = bg;
    previewEl.textContent = text;
    previewEl.style.width = '100%';

    cssOutput.textContent = '.element {\n  aspect-ratio: ' + w + ' / ' + h + ';\n}';
    resultSection.classList.add('show');
  }

  presetSelect.addEventListener('change', function() {
    if (this.value === 'custom') return;
    var parts = this.value.split('/');
    widthVal.value = parts[0];
    heightVal.value = parts[1];
    contentText.value = this.value;
    updateAspect();
  });

  applyBtn.addEventListener('click', updateAspect);
  bgColor.addEventListener('input', updateAspect);
  contentText.addEventListener('input', updateAspect);

  document.getElementById('copyBtn').addEventListener('click', function() {
    navigator.clipboard.writeText(cssOutput.textContent).then(function() {
      var btn = document.getElementById('copyBtn');
      btn.textContent = '✅ AlreadyCopy';
      setTimeout(function(){ btn.textContent = 'Copycode'; }, 2000);
    });
  });

  // Initial update
  updateAspect();