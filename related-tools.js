// Related Tools Loader - cross-recommendation
(function() {
  'use strict';
  var s = document.getElementById('related-tools-section');
  if (!s) return;
  var p = window.location.pathname;
  var en = p.indexOf('/en/') !== -1;
  p = p.replace(/\/en\//g, '/');
  var slug = p.split('/').filter(Boolean).pop() || '';
  if (!slug) { s.innerHTML = ''; return; }
  // Use relative path so it works with any domain
  var depth = en ? '../../' : '../';
  var u = depth + 'related-tools.json';
  fetch(u).then(function(r) {
    if (!r.ok) throw new Error('not found');
    return r.json();
  }).then(function(d) {
    var data = en ? d.en : d.cn;
    var t = data[slug];
    if (!t || !t.related || !t.related.length) { s.innerHTML = ''; return; }
    var h = '<div class="related-tools-inner"><h3 class="related-tools-title">'
      + (en ? '🔗 You May Also Like' : '🔗 相关工具推荐')
      + '</h3><div class="related-tools-grid">';
    t.related.forEach(function(r) {
      var link = en ? '../../en/' + r.slug + '/' : '../' + r.slug + '/';
      h += '<a href="' + link + '" class="related-tool-card">'
        + '<span class="related-tool-icon">' + (r.icon || '🔧') + '</span>'
        + '<span class="related-tool-name">' + r.name + '</span></a>';
    });
    h += '</div></div>';
    s.innerHTML = h;
  }).catch(function() { s.innerHTML = ''; });
})();
