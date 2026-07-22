#!/usr/bin/env python3
"""Build mime-types tool - MIME type reference and lookup"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/tools-site/_gen'))
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

# Tool HTML - CN
tool_html_cn = '''
<div class="mime-layout">
  <div class="form-group">
    <label>搜索 MIME 类型或文件扩展名</label>
    <input type="text" id="searchInput" placeholder="输入搜索关键词，如 image、text、application、.html、json..." oninput="searchMime()" autocomplete="off">
  </div>
  <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap">
    <button class="btn btn-primary" onclick="searchMime()">🔍 搜索</button>
    <button class="btn" style="background:#1e293b;color:#94a3b8" onclick="clearSearch()">清空</button>
    <label style="color:#94a3b8;font-size:.85rem;display:flex;align-items:center;gap:4px">
      显示 <select id="limitSelect" onchange="searchMime()" style="background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:4px;padding:2px 6px;font-size:.8rem">
        <option value="20">20</option>
        <option value="50" selected>50</option>
        <option value="100">100</option>
        <option value="0">全部</option>
      </select> 条
    </label>
  </div>
  <div class="mime-table-wrapper" style="overflow-x:auto;border:1px solid rgba(148,163,184,.1);border-radius:8px;max-height:500px;overflow-y:auto">
    <table class="mime-table" style="width:100%;border-collapse:collapse;font-size:.83rem">
      <thead>
        <tr style="background:#1e293b;position:sticky;top:0">
          <th style="padding:10px 12px;text-align:left;color:#f1c40f;border-bottom:1px solid rgba(148,163,184,.2);min-width:200px">MIME 类型</th>
          <th style="padding:10px 12px;text-align:left;color:#f1c40f;border-bottom:1px solid rgba(148,163,184,.2);min-width:100px">扩展名</th>
          <th style="padding:10px 12px;text-align:left;color:#f1c40f;border-bottom:1px solid rgba(148,163,184,.2);min-width:80px">分类</th>
          <th style="padding:10px 12px;text-align:left;color:#f1c40f;border-bottom:1px solid rgba(148,163,184,.2)">描述</th>
        </tr>
      </thead>
      <tbody id="mimeTableBody"></tbody>
    </table>
  </div>
  <div style="margin-top:12px;color:#64748b;font-size:.82rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px">
    <span>总计: <span id="totalCount" style="color:#e2e8f0">0</span> 条 | 显示: <span id="shownCount" style="color:#e2e8f0">0</span> 条</span>
    <span><span id="matchedCount" style="color:#22d3ee">0</span> 条匹配搜索结果</span>
  </div>
</div>
<style>
.mime-table tr:hover td{background:rgba(6,182,212,.05)}
.mime-table td{padding:8px 12px;border-bottom:1px solid rgba(148,163,184,.06);color:#e2e8f0;vertical-align:top}
.mime-table .ext{color:#22d3ee;font-family:'Consolas','Monaco','Courier New',monospace;font-size:.8rem}
.mime-table .cat-tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:500}
.cat-image{background:rgba(16,185,129,.15);color:#10b981}
.cat-text{background:rgba(59,130,246,.15);color:#3b82f6}
.cat-application{background:rgba(139,92,246,.15);color:#8b5cf6}
.cat-audio{background:rgba(236,72,153,.15);color:#ec4899}
.cat-video{background:rgba(249,115,22,.15);color:#f97316}
.cat-message{background:rgba(6,182,212,.15);color:#22d3ee}
.cat-model{background:rgba(168,85,247,.15);color:#a855f7}
.cat-font{background:rgba(34,197,94,.15);color:#22c55e}
.cat-multipart{background:rgba(234,179,8,.15);color:#eab308}
.btn{padding:8px 20px;border:none;border-radius:6px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn:hover{opacity:.85;transform:translateY(-1px)}
input[type="text"]{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}
input[type="text"]:focus{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}
</style>
'''

# Tool HTML - EN
tool_html_en = '''
<div class="mime-layout">
  <div class="form-group">
    <label>Search MIME type or file extension</label>
    <input type="text" id="searchInput" placeholder="Search keyword, e.g. image, text, application, .html, json..." oninput="searchMime()" autocomplete="off">
  </div>
  <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap">
    <button class="btn btn-primary" onclick="searchMime()">🔍 Search</button>
    <button class="btn" style="background:#1e293b;color:#94a3b8" onclick="clearSearch()">Clear</button>
    <label style="color:#94a3b8;font-size:.85rem;display:flex;align-items:center;gap:4px">
      Show <select id="limitSelect" onchange="searchMime()" style="background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:4px;padding:2px 6px;font-size:.8rem">
        <option value="20">20</option>
        <option value="50" selected>50</option>
        <option value="100">100</option>
        <option value="0">All</option>
      </select> entries
    </label>
  </div>
  <div class="mime-table-wrapper" style="overflow-x:auto;border:1px solid rgba(148,163,184,.1);border-radius:8px;max-height:500px;overflow-y:auto">
    <table class="mime-table" style="width:100%;border-collapse:collapse;font-size:.83rem">
      <thead>
        <tr style="background:#1e293b;position:sticky;top:0">
          <th style="padding:10px 12px;text-align:left;color:#f1c40f;border-bottom:1px solid rgba(148,163,184,.2);min-width:200px">MIME Type</th>
          <th style="padding:10px 12px;text-align:left;color:#f1c40f;border-bottom:1px solid rgba(148,163,184,.2);min-width:100px">Extension</th>
          <th style="padding:10px 12px;text-align:left;color:#f1c40f;border-bottom:1px solid rgba(148,163,184,.2);min-width:80px">Category</th>
          <th style="padding:10px 12px;text-align:left;color:#f1c40f;border-bottom:1px solid rgba(148,163,184,.2)">Description</th>
        </tr>
      </thead>
      <tbody id="mimeTableBody"></tbody>
    </table>
  </div>
  <div style="margin-top:12px;color:#64748b;font-size:.82rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px">
    <span>Total: <span id="totalCount" style="color:#e2e8f0">0</span> | Showing: <span id="shownCount" style="color:#e2e8f0">0</span></span>
    <span><span id="matchedCount" style="color:#22d3ee">0</span> matches</span>
  </div>
</div>
<style>
.mime-table tr:hover td{background:rgba(6,182,212,.05)}
.mime-table td{padding:8px 12px;border-bottom:1px solid rgba(148,163,184,.06);color:#e2e8f0;vertical-align:top}
.mime-table .ext{color:#22d3ee;font-family:'Consolas','Monaco','Courier New',monospace;font-size:.8rem}
.mime-table .cat-tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:500}
.cat-image{background:rgba(16,185,129,.15);color:#10b981}
.cat-text{background:rgba(59,130,246,.15);color:#3b82f6}
.cat-application{background:rgba(139,92,246,.15);color:#8b5cf6}
.cat-audio{background:rgba(236,72,153,.15);color:#ec4899}
.cat-video{background:rgba(249,115,22,.15);color:#f97316}
.cat-message{background:rgba(6,182,212,.15);color:#22d3ee}
.cat-model{background:rgba(168,85,247,.15);color:#a855f7}
.cat-font{background:rgba(34,197,94,.15);color:#22c55e}
.cat-multipart{background:rgba(234,179,8,.15);color:#eab308}
.btn{padding:8px 20px;border:none;border-radius:6px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn:hover{opacity:.85;transform:translateY(-1px)}
input[type="text"]{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}
input[type="text"]:focus{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}
</style>
'''

# Tool JS
tool_js = '''
var MIME_DB = [
  {mime:"text/plain",ext:".txt",cat:"text",desc:"Plain text file"},
  {mime:"text/html",ext:".html .htm",cat:"text",desc:"HTML document"},
  {mime:"text/css",ext:".css",cat:"text",desc:"Cascading Style Sheets"},
  {mime:"text/javascript",ext:".js",cat:"text",desc:"JavaScript file"},
  {mime:"text/csv",ext:".csv",cat:"text",desc:"Comma-Separated Values"},
  {mime:"text/markdown",ext:".md .markdown",cat:"text",desc:"Markdown document"},
  {mime:"text/xml",ext:".xml",cat:"text",desc:"XML document"},
  {mime:"text/yaml",ext:".yaml .yml",cat:"text",desc:"YAML document"},
  {mime:"text/json",ext:".json",cat:"text",desc:"JSON data"},
  {mime:"text/calendar",ext:".ics",cat:"text",desc:"Calendar file (iCal)"},
  {mime:"text/vcard",ext:".vcf",cat:"text",desc:"vCard contact"},
  {mime:"text/x-php",ext:".php",cat:"text",desc:"PHP source code"},
  {mime:"image/jpeg",ext:".jpg .jpeg",cat:"image",desc:"JPEG image"},
  {mime:"image/png",ext:".png",cat:"image",desc:"PNG image"},
  {mime:"image/gif",ext:".gif",cat:"image",desc:"GIF image"},
  {mime:"image/webp",ext:".webp",cat:"image",desc:"WebP image"},
  {mime:"image/svg+xml",ext:".svg",cat:"image",desc:"SVG vector image"},
  {mime:"image/bmp",ext:".bmp",cat:"image",desc:"Bitmap image"},
  {mime:"image/avif",ext:".avif",cat:"image",desc:"AVIF image"},
  {mime:"image/tiff",ext:".tiff .tif",cat:"image",desc:"TIFF image"},
  {mime:"image/x-icon",ext:".ico",cat:"image",desc:"Icon file"},
  {mime:"image/vnd.microsoft.icon",ext:".ico",cat:"image",desc:"Windows icon"},
  {mime:"application/json",ext:".json",cat:"application",desc:"JSON (application)"},
  {mime:"application/pdf",ext:".pdf",cat:"application",desc:"PDF document"},
  {mime:"application/zip",ext:".zip",cat:"application",desc:"ZIP archive"},
  {mime:"application/gzip",ext:".gz",cat:"application",desc:"GZip archive"},
  {mime:"application/x-tar",ext:".tar",cat:"application",desc:"TAR archive"},
  {mime:"application/x-7z-compressed",ext:".7z",cat:"application",desc:"7-Zip archive"},
  {mime:"application/x-rar-compressed",ext:".rar",cat:"application",desc:"RAR archive"},
  {mime:"application/x-bzip2",ext:".bz2",cat:"application",desc:"BZip2 archive"},
  {mime:"application/epub+zip",ext:".epub",cat:"application",desc:"EPUB ebook"},
  {mime:"application/msword",ext:".doc",cat:"application",desc:"Word document"},
  {mime:"application/vnd.openxmlformats-officedocument.wordprocessingml.document",ext:".docx",cat:"application",desc:"Word OpenXML document"},
  {mime:"application/vnd.ms-excel",ext:".xls",cat:"application",desc:"Excel spreadsheet"},
  {mime:"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",ext:".xlsx",cat:"application",desc:"Excel OpenXML spreadsheet"},
  {mime:"application/vnd.ms-powerpoint",ext:".ppt",cat:"application",desc:"PowerPoint presentation"},
  {mime:"application/vnd.openxmlformats-officedocument.presentationml.presentation",ext:".pptx",cat:"application",desc:"PowerPoint OpenXML"},
  {mime:"application/xml",ext:".xml",cat:"application",desc:"XML (application)"},
  {mime:"application/octet-stream",ext:".bin",cat:"application",desc:"Binary file"},
  {mime:"application/x-www-form-urlencoded",ext:"",cat:"application",desc:"URL-encoded form data"},
  {mime:"application/xhtml+xml",ext:".xhtml",cat:"application",desc:"XHTML document"},
  {mime:"application/x-sh",ext:".sh",cat:"application",desc:"Shell script"},
  {mime:"application/x-csh",ext:".csh",cat:"application",desc:"C Shell script"},
  {mime:"application/x-perl",ext:".pl .pm",cat:"application",desc:"Perl script"},
  {mime:"application/x-python",ext:".py",cat:"application",desc:"Python script"},
  {mime:"application/x-java",ext:".java",cat:"application",desc:"Java source"},
  {mime:"application/x-dart",ext:".dart",cat:"application",desc:"Dart source"},
  {mime:"application/typescript",ext:".ts",cat:"application",desc:"TypeScript source"},
  {mime:"application/wasm",ext:".wasm",cat:"application",desc:"WebAssembly binary"},
  {mime:"application/manifest+json",ext:".webmanifest",cat:"application",desc:"Web App Manifest"},
  {mime:"application/vnd.apple.mpegurl",ext:".m3u8",cat:"application",desc:"Apple HLS playlist"},
  {mime:"application/vnd.google-earth.kml+xml",ext:".kml",cat:"application",desc:"Google Earth KML"},
  {mime:"application/vnd.google-earth.kmz",ext:".kmz",cat:"application",desc:"Google Earth KMZ"},
  {mime:"application/vnd.api+json",ext:"",cat:"application",desc:"JSON API"},
  {mime:"application/ld+json",ext:".jsonld",cat:"application",desc:"JSON-LD data"},
  {mime:"application/x-ns-proxy-autoconfig",ext:".pac",cat:"application",desc:"Proxy auto-config"},
  {mime:"audio/mpeg",ext:".mp3",cat:"audio",desc:"MP3 audio"},
  {mime:"audio/ogg",ext:".ogg .oga",cat:"audio",desc:"OGG audio"},
  {mime:"audio/wav",ext:".wav",cat:"audio",desc:"WAV audio"},
  {mime:"audio/webm",ext:".webm",cat:"audio",desc:"WebM audio"},
  {mime:"audio/aac",ext:".aac",cat:"audio",desc:"AAC audio"},
  {mime:"audio/flac",ext:".flac",cat:"audio",desc:"FLAC audio"},
  {mime:"audio/midi",ext:".mid .midi",cat:"audio",desc:"MIDI audio"},
  {mime:"audio/x-m4a",ext:".m4a",cat:"audio",desc:"M4A audio"},
  {mime:"audio/opus",ext:".opus",cat:"audio",desc:"Opus audio"},
  {mime:"video/mp4",ext:".mp4",cat:"video",desc:"MP4 video"},
  {mime:"video/webm",ext:".webm",cat:"video",desc:"WebM video"},
  {mime:"video/ogg",ext:".ogv",cat:"video",desc:"OGG video"},
  {mime:"video/x-msvideo",ext:".avi",cat:"video",desc:"AVI video"},
  {mime:"video/x-matroska",ext:".mkv",cat:"video",desc:"Matroska video"},
  {mime:"video/mpeg",ext:".mpeg .mpg",cat:"video",desc:"MPEG video"},
  {mime:"video/quicktime",ext:".mov",cat:"video",desc:"QuickTime video"},
  {mime:"video/x-flv",ext:".flv",cat:"video",desc:"Flash video"},
  {mime:"video/3gpp",ext:".3gp",cat:"video",desc:"3GPP video"},
  {mime:"video/3gpp2",ext:".3g2",cat:"video",desc:"3GPP2 video"},
  {mime:"font/ttf",ext:".ttf",cat:"font",desc:"TrueType font"},
  {mime:"font/otf",ext:".otf",cat:"font",desc:"OpenType font"},
  {mime:"font/woff",ext:".woff",cat:"font",desc:"WOFF font"},
  {mime:"font/woff2",ext:".woff2",cat:"font",desc:"WOFF2 font"},
  {mime:"multipart/form-data",ext:"",cat:"multipart",desc:"Multipart form data"},
  {mime:"multipart/alternative",ext:"",cat:"multipart",desc:"Multipart alternative"},
  {mime:"message/rfc822",ext:".eml",cat:"message",desc:"Email message"},
  {mime:"model/gltf+json",ext:".gltf",cat:"model",desc:"glTF 3D model"},
  {mime:"model/gltf-binary",ext:".glb",cat:"model",desc:"glTF binary 3D model"},
  {mime:"model/obj",ext:".obj",cat:"model",desc:"Wavefront 3D object"},
  {mime:"model/stl",ext:".stl",cat:"model",desc:"STL 3D model"},
  {mime:"model/usd",ext:".usd",cat:"model",desc:"Universal Scene Description"},
  {mime:"model/usda",ext:".usda",cat:"model",desc:"USD ASCII"},
  {mime:"model/usdz",ext:".usdz",cat:"model",desc:"USDZ 3D model"},
  {mime:"image/heic",ext:".heic",cat:"image",desc:"HEIC image (iOS)"},
  {mime:"image/heif",ext:".heif",cat:"image",desc:"HEIF image"},
  {mime:"text/richtext",ext:".rtx",cat:"text",desc:"Rich text"},
  {mime:"text/tab-separated-values",ext:".tsv",cat:"text",desc:"Tab-separated values"},
  {mime:"text/x-python",ext:".py",cat:"text",desc:"Python (text)"},
  {mime:"text/x-java-source",ext:".java",cat:"text",desc:"Java source (text)"},
  {mime:"text/x-ruby",ext:".rb",cat:"text",desc:"Ruby source"},
  {mime:"text/x-rust",ext:".rs",cat:"text",desc:"Rust source"},
  {mime:"text/x-go",ext:".go",cat:"text",desc:"Go source"},
  {mime:"text/x-swift",ext:".swift",cat:"text",desc:"Swift source"},
  {mime:"text/x-kotlin",ext:".kt .kts",cat:"text",desc:"Kotlin source"},
  {mime:"text/x-sql",ext:".sql",cat:"text",desc:"SQL script"},
  {mime:"text/x-dockerfile",ext:"Dockerfile",cat:"text",desc:"Dockerfile"},
  {mime:"text/x-makefile",ext:"Makefile",cat:"text",desc:"Makefile"},
  {mime:"application/x-bat",ext:".bat .cmd",cat:"application",desc:"Batch file"},
  {mime:"application/x-powershell",ext:".ps1",cat:"application",desc:"PowerShell script"},
  {mime:"application/x-latex",ext:".tex .ltx",cat:"application",desc:"LaTeX document"},
  {mime:"application/vnd.ms-fontobject",ext:".eot",cat:"font",desc:"Embedded OpenType font"},
  {mime:"application/vnd.oasis.opendocument.text",ext:".odt",cat:"application",desc:"OpenDocument text"},
  {mime:"application/vnd.oasis.opendocument.spreadsheet",ext:".ods",cat:"application",desc:"OpenDocument spreadsheet"},
  {mime:"application/vnd.oasis.opendocument.presentation",ext:".odp",cat:"application",desc:"OpenDocument presentation"},
  {mime:"application/rtf",ext:".rtf",cat:"application",desc:"Rich Text Format"},
  {mime:"application/xhtml+xml",ext:".xhtml",cat:"application",desc:"XHTML file"},
  {mime:"application/x-bibtex",ext:".bib",cat:"application",desc:"BibTeX bibliography"},
  {mime:"application/x-tex",ext:".tex",cat:"application",desc:"TeX document"},
  {mime:"application/x-lzh-compressed",ext:".lzh .lha",cat:"application",desc:"LZH archive"},
  {mime:"application/x-cpio",ext:".cpio",cat:"application",desc:"CPIO archive"},
  {mime:"application/x-shockwave-flash",ext:".swf",cat:"application",desc:"Flash animation"},
  {mime:"application/vnd.android.package-archive",ext:".apk",cat:"application",desc:"Android app package"},
  {mime:"application/x-msdownload",ext:".exe .dll",cat:"application",desc:"Windows executable"},
  {mime:"application/x-msi",ext:".msi",cat:"application",desc:"Windows installer"},
  {mime:"application/x-deb",ext:".deb",cat:"application",desc:"Debian package"},
  {mime:"application/x-rpm",ext:".rpm",cat:"application",desc:"RPM package"},
  {mime:"application/x-appimage",ext:".AppImage",cat:"application",desc:"AppImage"},
  {mime:"application/x-iso9660-image",ext:".iso",cat:"application",desc:"ISO disk image"},
  {mime:"application/x-sqlite3",ext:".sqlite .db",cat:"application",desc:"SQLite database"},
  {mime:"application/x-httpd-php",ext:".php",cat:"application",desc:"PHP (application)"},
  {mime:"application/x-javascript",ext:".js",cat:"application",desc:"JavaScript (application)"},
  {mime:"application/dart",ext:".dart",cat:"application",desc:"Dart (application)"},
  {mime:"application/graphql",ext:"",cat:"application",desc:"GraphQL query"},
  {mime:"application/protobuf",ext:".proto",cat:"application",desc:"Protocol Buffers"},
  {mime:"application/xml+svg",ext:".svg",cat:"application",desc:"SVG (application)"},
  {mime:"image/x-portable-pixmap",ext:".ppm",cat:"image",desc:"Portable Pixmap"},
  {mime:"image/x-portable-graymap",ext:".pgm",cat:"image",desc:"Portable Graymap"},
  {mime:"image/x-portable-bitmap",ext:".pbm",cat:"image",desc:"Portable Bitmap"},
  {mime:"image/x-portable-anymap",ext:".pnm",cat:"image",desc:"Portable Anymap"},
  {mime:"image/x-xbitmap",ext:".xbm",cat:"image",desc:"X BitMap"},
  {mime:"image/x-xpixmap",ext:".xpm",cat:"image",desc:"X PixMap"},
  {mime:"audio/x-caf",ext:".caf",cat:"audio",desc:"Core Audio Format"},
  {mime:"audio/x-aiff",ext:".aiff .aif",cat:"audio",desc:"Audio Interchange File Format"},
  {mime:"audio/x-wav",ext:".wav",cat:"audio",desc:"WAV (old)"},
  {mime:"video/x-ms-wmv",ext:".wmv",cat:"video",desc:"Windows Media Video"},
  {mime:"video/x-ms-asf",ext:".asf",cat:"video",desc:"Advanced Systems Format"},
  {mime:"video/x-sgi-movie",ext:".movie",cat:"video",desc:"SGI Movie"},
  {mime:"font/collection",ext:".ttc",cat:"font",desc:"TrueType font collection"},
  {mime:"application/x-font-ttf",ext:".ttf",cat:"font",desc:"TrueType (legacy)"},
  {mime:"application/x-font-otf",ext:".otf",cat:"font",desc:"OpenType (legacy)"},
  {mime:"application/x-font-type1",ext:".pfa .pfb .afm",cat:"font",desc:"PostScript Type 1 font"},
  {mime:"image/vnd.dxf",ext:".dxf",cat:"image",desc:"AutoCAD DXF"},
  {mime:"image/vnd.dwg",ext:".dwg",cat:"image",desc:"AutoCAD DWG"}
];

function getCatClass(cat) {
  return 'cat-' + cat;
}
function getCatLabel(cat) {
  var labels = {image:'Image',text:'Text',application:'Application',audio:'Audio',video:'Video',font:'Font',multipart:'Multipart',message:'Message',model:'3D Model'};
  return labels[cat] || cat;
}
function renderTable(data) {
  var tbody = document.getElementById('mimeTableBody');
  var html = '';
  for (var i = 0; i < data.length; i++) {
    var item = data[i];
    html += '<tr>' +
      '<td style="font-family:Consolas,Monaco,monospace;font-size:.82rem;color:#e2e8f0;word-break:break-all">' + escapeHtml(item.mime) + '</td>' +
      '<td class="ext">' + escapeHtml(item.ext || '-') + '</td>' +
      '<td><span class="cat-tag ' + getCatClass(item.cat) + '">' + getCatLabel(item.cat) + '</span></td>' +
      '<td style="color:#94a3b8;font-size:.8rem">' + escapeHtml(item.desc) + '</td>' +
      '</tr>';
  }
  if (data.length === 0) {
    html = '<tr><td colspan="4" style="text-align:center;padding:40px;color:#64748b">No matching MIME types found</td></tr>';
  }
  tbody.innerHTML = html;
}
function searchMime() {
  var query = document.getElementById('searchInput').value.toLowerCase().trim();
  var limit = parseInt(document.getElementById('limitSelect').value);
  var filtered = [];
  if (query === '') {
    filtered = MIME_DB;
  } else {
    for (var i = 0; i < MIME_DB.length; i++) {
      var item = MIME_DB[i];
      if (item.mime.toLowerCase().indexOf(query) !== -1 ||
          item.ext.toLowerCase().indexOf(query) !== -1 ||
          item.desc.toLowerCase().indexOf(query) !== -1 ||
          item.cat.indexOf(query) !== -1) {
        filtered.push(item);
      }
    }
  }
  document.getElementById('totalCount').textContent = MIME_DB.length;
  document.getElementById('matchedCount').textContent = filtered.length;
  var shown = filtered;
  if (limit > 0 && filtered.length > limit) {
    shown = filtered.slice(0, limit);
  }
  document.getElementById('shownCount').textContent = shown.length;
  renderTable(shown);
}
function clearSearch() {
  document.getElementById('searchInput').value = '';
  searchMime();
}
function escapeHtml(str) {
  var div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
window.onload = searchMime;
'''

# FAQs CN
faqs_cn = [
    ('什么是 MIME 类型？', 'MIME（Multipurpose Internet Mail Extensions）类型是一种标准标识符，用于表示文件的格式和内容类型。它在HTTP协议中通过Content-Type头部传递，帮助浏览器正确解析和显示文件。'),
    ('MIME 类型和文件扩展名有什么关系？', 'MIME 类型和文件扩展名都是标识文件格式的方式。扩展名（如 .html、.jpg）是操作系统层面的标识，而 MIME 类型（如 text/html、image/jpeg）是网络传输层面的标准标识。服务器通过 MIME 类型告诉浏览器如何解析接收到的数据。'),
    ('如何查找某个文件的正确 MIME 类型？', '你可以在此工具中搜索文件扩展名（如 .pdf、.docx）或关键词（如 image、text），即可找到对应的 MIME 类型。同时也可以反向查找某个 MIME 类型对应哪些扩展名。'),
    ('为什么有些 MIME 类型以 text/ 开头，有些以 application/ 开头？', 'MIME 类型分为多个类别：text/ 表示可读的文本类型，application/ 表示二进制或需要应用程序处理的类型，image/、audio/、video/ 分别表示图像、音频和视频文件。每个类别都有其标准前缀。'),
    ('MIME 类型配置错误会有什么影响？', '如果服务器配置了错误的 MIME 类型，浏览器可能无法正确解析文件，导致文件直接下载而非显示、显示乱码、或安全策略阻止加载。正确配置 MIME 类型是网站正常运行的重要环节。'),
]

faqs_en = [
    ('What is a MIME type?', 'MIME (Multipurpose Internet Mail Extensions) type is a standard identifier that indicates the format and content type of a file. It is transmitted via the Content-Type header in HTTP protocol, helping browsers correctly parse and display files.'),
    ('How are MIME types related to file extensions?', 'Both MIME types and file extensions identify file formats. Extensions (.html, .jpg) are used at the OS level, while MIME types (text/html, image/jpeg) are the standard at the network transmission level. Servers use MIME types to tell browsers how to interpret received data.'),
    ('How do I find the correct MIME type for a file?', 'You can search by file extension (e.g., .pdf, .docx) or keyword (e.g., image, text) in this tool to find the corresponding MIME type. You can also reverse-lookup which extensions belong to a MIME type.'),
    ('Why do some MIME types start with text/ and others with application/?', 'MIME types are categorized: text/ for readable text, application/ for binary or application-specific data, image/, audio/, video/ for media files. Each category has its standard prefix.'),
    ('What happens if a MIME type is misconfigured?', 'Incorrect MIME type configuration can cause browsers to fail parsing files properly - files may download instead of display, show garbled content, or be blocked by security policies. Correct MIME type configuration is essential for proper website operation.'),
]

# SEO CN
seo_cn = '''
<h2>MIME 类型查询表 - 免费在线 MIME 类型参考大全</h2>
<p>MIME 类型查询表（MIME Types Reference）是一款免费在线的 MIME 类型参考工具，收录了超过120种常见的 MIME 类型及其对应的文件扩展名、分类和描述。支持关键词搜索，快速查找你需要的内容类型。适用于 Web 开发者、系统管理员和 IT 从业人员。</p>
<h3>核心功能</h3>
<ul>
<li>完整收录：收录120+种常见 MIME 类型，覆盖 text、image、application、audio、video、font 等分类</li>
<li>智能搜索：支持按 MIME 类型名称、文件扩展名、描述关键词模糊搜索</li>
<li>分类浏览：按类别（文本、图像、应用、音频、视频、字体等）分类展示</li>
<li>彩色标签：每个分类使用不同颜色标签，一目了然</li>
<li>完全离线：纯前端实现，无需网络也可使用</li>
</ul>
<h3>适用场景</h3>
<ul>
<li>Web 服务器配置：配置 Nginx/Apache 的 MIME 类型映射</li>
<li>开发调试：检查 HTTP Content-Type 头部是否正确</li>
<li>文件上传验证：验证上传文件的 MIME 类型</li>
<li>教学参考：学习 MIME 类型标准和分类体系</li>
</ul>
'''

seo_en = '''
<h2>MIME Types Reference - Free Online MIME Type Lookup</h2>
<p>MIME Types Reference is a free online tool cataloging 120+ common MIME types with their file extensions, categories, and descriptions. Search by keyword to quickly find the content type you need. Ideal for web developers, system administrators, and IT professionals.</p>
<h3>Key Features</h3>
<ul>
<li>Comprehensive: 120+ common MIME types covering text, image, application, audio, video, font and more</li>
<li>Smart search: Fuzzy search by MIME type, file extension, or description keyword</li>
<li>Category browsing: Color-coded categories for easy scanning</li>
<li>Fully offline: Pure frontend, works without internet</li>
</ul>
'''

cn_path, en_path = builder.build_bilingual(
    slug='mime-types',
    title_cn='MIME 类型查询表',
    title_en='MIME Types Reference',
    desc_cn='免费在线 MIME 类型查询表，收录120+种常见 MIME 类型。支持按名称、扩展名、关键词搜索。涵盖 text/image/application/audio/video/font 全分类。纯前端本地处理。',
    desc_en='Free online MIME types reference with 120+ common MIME types. Search by name, extension, or keyword. Covers text, image, application, audio, video, and font categories. Pure frontend.',
    icon='📄',
    cat_cn='开发工具',
    cat_en='Developer Tools',
    cat_anchor='developer-tools',
    tool_html_cn=tool_html_cn,
    tool_html_en=tool_html_en,
    tool_js=tool_js,
    faqs_cn=faqs_cn,
    faqs_en=faqs_en,
    seo_cn=seo_cn,
    seo_en=seo_en,
)

print(f"✅ Created: {cn_path}")
print(f"✅ Created: {en_path}")
