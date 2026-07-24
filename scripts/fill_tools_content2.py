#!/usr/bin/env python3
"""填充工具6-10的实际功能代码"""
import os

BASE = '/home/chison/tools-site'
PLACEHOLDER = '<!-- TOOL-SPECIFIC CONTENT PLACEHOLDER -->'

def make_font_pair(lang):
    is_zh = lang == 'zh'
    if is_zh:
        return '''
<div class="input-section">
<h2>🔤 自定义预览文字</h2>
<div class="form-group"><label>标题文字</label><input type="text" id="headingText" value="优雅的设计" maxlength="30"></div>
<div class="form-group"><label>正文文字</label><textarea id="bodyText" style="min-height:60px">这段文字展示了字体在正文中的效果。好的字体搭配能让设计更加专业和美观。</textarea></div>
</div>
<div class="input-section">
<h2>🎨 精选搭配方案</h2>
<div id="pairList"></div>
</div>
<script>
var pairs=[
  {h:'Playfair Display',hcat:'serif',b:'Lato',bcat:'sans-serif',import:'@import url(\\'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400&display=swap\\');',css:'font-family: \\'Playfair Display\\', serif; / font-family: \\'Lato\\', sans-serif;',desc:'经典优雅组合，适合品牌和高端网站'},
  {h:'Montserrat',hcat:'sans-serif',b:'Open Sans',bcat:'sans-serif',import:'@import url(\\'https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans:wght@400&display=swap\\');',css:'font-family: \\'Montserrat\\', sans-serif; / font-family: \\'Open Sans\\', sans-serif;',desc:'现代清爽搭配，适合企业网站和SaaS'},
  {h:'Poppins',hcat:'sans-serif',b:'Roboto',bcat:'sans-serif',import:'@import url(\\'https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Roboto:wght@400&display=swap\\');',css:'font-family: \\'Poppins\\', sans-serif; / font-family: \\'Roboto\\', sans-serif;',desc:'流行组合，适合科技和创意设计'},
  {h:'Oswald',hcat:'sans-serif',b:'Merriweather',bcat:'serif',import:'@import url(\\'https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Merriweather:wght@400&display=swap\\');',css:'font-family: \\'Oswald\\', sans-serif; / font-family: \\'Merriweather\\', serif;',desc:'力量与优雅的碰撞，适合新闻和杂志'},
  {h:'Raleway',hcat:'sans-serif',b:'Libre Baskerville',bcat:'serif',import:'@import url(\\'https://fonts.googleapis.com/css2?family=Raleway:wght@700&family=Libre+Baskerville:wght@400&display=swap\\');',css:'font-family: \\'Raleway\\', sans-serif; / font-family: \\'Libre Baskerville\\', serif;',desc:'现代极简与经典结合，适合设计工作室'},
  {h:'Noto Sans SC',hcat:'sans-serif',b:'Noto Serif SC',bcat:'serif',import:'@import url(\\'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@700&family=Noto+Serif+SC:wght@400&display=swap\\');',css:'font-family: \\'Noto Sans SC\\', sans-serif; / font-family: \\'Noto Serif SC\\', serif;',desc:'中文优化搭配，适合中文内容网站'},
  {h:'Bebas Neue',hcat:'display',b:'Source Sans Pro',bcat:'sans-serif',import:'@import url(\\'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Source+Sans+Pro:wght@400&display=swap\\');',css:'font-family: \\'Bebas Neue\\', cursive; / font-family: \\'Source Sans Pro\\', sans-serif;',desc:'大胆醒目，适合活动和海报设计'},
  {h:'Josefin Sans',hcat:'sans-serif',b:'Crimson Text',bcat:'serif',import:'@import url(\\'https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@700&family=Crimson+Text:wght@400&display=swap\\');',css:'font-family: \\'Josefin Sans\\', sans-serif; / font-family: \\'Crimson Text\\', serif;',desc:'时尚文艺，适合博客和个人网站'},
];
function renderPairs(){
  var ht=document.getElementById('headingText').value;
  var bt=document.getElementById('bodyText').value;
  var h='';
  pairs.forEach(function(p){
    var catColors={serif:'#fbbf24','sans-serif':'#22d3ee',display:'#f472b6',cursive:'#a78bfa'};
    var hc=catColors[p.hcat]||'#94a3b8',bc=catColors[p.bcat]||'#94a3b8';
    h+='<div class="pair-card" style="background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)">';
    h+='<div style="margin-bottom:12px"><span style="background:#0f172a;color:'+hc+';padding:2px 8px;border-radius:4px;font-size:.75rem;margin-right:8px">'+p.hcat+'</span><span style="color:#22d3ee;font-weight:600;font-size:1rem">'+p.h+'</span> + <span style="color:#94a3b8;font-size:1rem">'+p.b+'</span><span style="background:#0f172a;color:'+bc+';padding:2px 8px;border-radius:4px;font-size:.75rem;margin-left:8px">'+p.bcat+'</span></div>';
    h+='<div style="background:#0f172a;border-radius:8px;padding:16px;margin-bottom:12px">';
    h+='<div style="font-size:1.5rem;font-weight:700;color:#f1f5f9;margin-bottom:8px">'+ht+'</div>';
    h+='<div style="font-size:.95rem;color:#94a3b8;line-height:1.8">'+bt+'</div>';
    h+='</div>';
    h+='<p style="color:#64748b;font-size:.85rem;margin-bottom:8px">'+p.desc+'</p>';
    h+='<div style="background:#0f172a;border-radius:4px;padding:8px;font-family:monospace;font-size:.8rem;color:#22d3ee;margin-bottom:8px;word-break:break-all">'+p.import+'</div>';
    h+='<div style="background:#0f172a;border-radius:4px;padding:8px;font-family:monospace;font-size:.8rem;color:#94a3b8">'+p.css+'</div>';
    h+='<button class="btn btn-primary" style="margin-top:8px;padding:6px 16px;font-size:.8rem" onclick="copyCSS(\\''+p.import.replace(/'/g,"\\\\'")+'\\')">📋 复制引用代码</button>';
    h+='</div>';
  });
  document.getElementById('pairList').innerHTML=h;
}
document.getElementById('headingText').addEventListener('input',renderPairs);
document.getElementById('bodyText').addEventListener('input',renderPairs);
function copyCSS(text){
  navigator.clipboard.writeText(text).then(function(){showToast('CSS引用代码已复制')}).catch(function(){showToast('复制失败')});
}
renderPairs();
</script>
'''
    else:
        return '''
<div class="input-section">
<h2>🔤 Custom Preview Text</h2>
<div class="form-group"><label>Heading Text</label><input type="text" id="headingText" value="Elegant Design" maxlength="30"></div>
<div class="form-group"><label>Body Text</label><textarea id="bodyText" style="min-height:60px">This text shows how the body font looks in paragraph context. Good font pairing makes your design look professional and polished.</textarea></div>
</div>
<div class="input-section">
<h2>🎨 Curated Pairings</h2>
<div id="pairList"></div>
</div>
<script>
var pairs=[
  {h:'Playfair Display',hcat:'serif',b:'Lato',bcat:'sans-serif',import:"@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400&display=swap');",css:"font-family: 'Playfair Display', serif; / font-family: 'Lato', sans-serif;",desc:'Classic elegance for brands and premium sites'},
  {h:'Montserrat',hcat:'sans-serif',b:'Open Sans',bcat:'sans-serif',import:"@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans:wght@400&display=swap');",css:"font-family: 'Montserrat', sans-serif; / font-family: 'Open Sans', sans-serif;",desc:'Modern and clean for corporate and SaaS'},
  {h:'Poppins',hcat:'sans-serif',b:'Roboto',bcat:'sans-serif',import:"@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Roboto:wght@400&display=swap');",css:"font-family: 'Poppins', sans-serif; / font-family: 'Roboto', sans-serif;",desc:'Trendy combo for tech and creative design'},
  {h:'Oswald',hcat:'sans-serif',b:'Merriweather',bcat:'serif',import:"@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Merriweather:wght@400&display=swap');",css:"font-family: 'Oswald', sans-serif; / font-family: 'Merriweather', serif;",desc:'Power meets elegance for news and magazines'},
  {h:'Raleway',hcat:'sans-serif',b:'Libre Baskerville',bcat:'serif',import:"@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@700&family=Libre+Baskerville:wght@400&display=swap');",css:"font-family: 'Raleway', sans-serif; / font-family: 'Libre Baskerville', serif;",desc:'Minimalist meets classic for design studios'},
  {h:'Noto Sans SC',hcat:'sans-serif',b:'Noto Serif SC',bcat:'serif',import:"@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@700&family=Noto+Serif+SC:wght@400&display=swap');",css:"font-family: 'Noto Sans SC', sans-serif; / font-family: 'Noto Serif SC', serif;",desc:'Optimized for Chinese content websites'},
  {h:'Bebas Neue',hcat:'display',b:'Source Sans Pro',bcat:'sans-serif',import:"@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Source+Sans+Pro:wght@400&display=swap');",css:"font-family: 'Bebas Neue', cursive; / font-family: 'Source Sans Pro', sans-serif;",desc:'Bold and striking for events and posters'},
  {h:'Josefin Sans',hcat:'sans-serif',b:'Crimson Text',bcat:'serif',import:"@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@700&family=Crimson+Text:wght@400&display=swap');",css:"font-family: 'Josefin Sans', sans-serif; / font-family: 'Crimson Text', serif;",desc:'Stylish and artsy for blogs and personal sites'},
];
function renderPairs(){
  var ht=document.getElementById('headingText').value;
  var bt=document.getElementById('bodyText').value;
  var h='';
  pairs.forEach(function(p){
    var catColors={serif:'#fbbf24','sans-serif':'#22d3ee',display:'#f472b6',cursive:'#a78bfa'};
    var hc=catColors[p.hcat]||'#94a3b8',bc=catColors[p.bcat]||'#94a3b8';
    h+='<div class="pair-card" style="background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)">';
    h+='<div style="margin-bottom:12px"><span style="background:#0f172a;color:'+hc+';padding:2px 8px;border-radius:4px;font-size:.75rem;margin-right:8px">'+p.hcat+'</span><span style="color:#22d3ee;font-weight:600;font-size:1rem">'+p.h+'</span> + <span style="color:#94a3b8;font-size:1rem">'+p.b+'</span><span style="background:#0f172a;color:'+bc+';padding:2px 8px;border-radius:4px;font-size:.75rem;margin-left:8px">'+p.bcat+'</span></div>';
    h+='<div style="background:#0f172a;border-radius:8px;padding:16px;margin-bottom:12px">';
    h+='<div style="font-size:1.5rem;font-weight:700;color:#f1f5f9;margin-bottom:8px">'+ht+'</div>';
    h+='<div style="font-size:.95rem;color:#94a3b8;line-height:1.8">'+bt+'</div>';
    h+='</div>';
    h+='<p style="color:#64748b;font-size:.85rem;margin-bottom:8px">'+p.desc+'</p>';
    h+='<div style="background:#0f172a;border-radius:4px;padding:8px;font-family:monospace;font-size:.8rem;color:#22d3ee;margin-bottom:8px;word-break:break-all">'+p.import+'</div>';
    h+='<div style="background:#0f172a;border-radius:4px;padding:8px;font-family:monospace;font-size:.8rem;color:#94a3b8">'+p.css+'</div>';
    h+='<button class="btn btn-primary" style="margin-top:8px;padding:6px 16px;font-size:.8rem" onclick="copyCSS(\\''+p.import.replace(/'/g,"\\\\'")+'\\')">📋 Copy Import Code</button>';
    h+='</div>';
  });
  document.getElementById('pairList').innerHTML=h;
}
document.getElementById('headingText').addEventListener('input',renderPairs);
document.getElementById('bodyText').addEventListener('input',renderPairs);
function copyCSS(text){
  navigator.clipboard.writeText(text).then(function(){showToast('CSS import code copied')}).catch(function(){showToast('Copy failed')});
}
renderPairs();
</script>
'''

def make_audio_cutter(lang):
    is_zh = lang == 'zh'
    labels = {
        'upload': '📁 上传音频' if is_zh else '📁 Upload Audio',
        'start': '起始时间 (秒)' if is_zh else 'Start Time (seconds)',
        'end': '结束时间 (秒)' if is_zh else 'End Time (seconds)',
        'duration': '总时长' if is_zh else 'Duration',
        'preview': '🔊 试听选区' if is_zh else '🔊 Preview Selection',
        'cut': '✂️ 剪切并下载' if is_zh else '✂️ Cut & Download',
        'no_file': '请先上传音频文件' if is_zh else 'Please upload an audio file first',
        'invalid_range': '起始时间必须小于结束时间' if is_zh else 'Start time must be less than end time',
        'cut_done': '剪切完成，下载中...' if is_zh else 'Cut complete, downloading...',
        'unsupported': '您的浏览器不支持此功能，请使用最新版Chrome或Firefox' if is_zh else 'Your browser does not support this feature. Please use the latest Chrome or Firefox',
        'upload_prompt': '请上传MP3/WAV/OGG格式的音频文件' if is_zh else 'Please upload MP3/WAV/OGG audio file'
    }
    return f'''
<div class="input-section">
<h2>{labels['upload']}</h2>
<div class="form-group"><input type="file" id="audioInput" accept="audio/*"></div>
<div class="form-row">
<div class="form-group"><label>{labels['start']}</label><input type="number" id="startTime" value="0" min="0" step="0.1"></div>
<div class="form-group"><label>{labels['end']}</label><input type="number" id="endTime" value="10" min="0" step="0.1"></div>
</div>
<div class="form-group"><span style="color:#94a3b8;font-size:.85rem">{labels['duration']}: <span id="durationDisplay" style="color:#22d3ee">--</span></span></div>
<div class="btn-row">
<button class="btn btn-primary" id="previewBtn">{labels['preview']}</button>
<button class="btn btn-success" id="cutBtn">{labels['cut']}</button>
</div>
<audio id="audioPlayer" controls style="width:100%;margin-top:12px;display:none"></audio>
</div>
<div class="input-section">
<h2>{"📝 说明" if is_zh else "📝 Notes"}</h2>
{("<p>上传音频文件后会自动显示时长。设置起止时间后，点击剪切即可下载裁剪后的音频片段。所有处理在浏览器本地完成，无需上传到服务器。</p>" if is_zh else "<p>After uploading an audio file, the duration will be displayed. Set start and end times, then click cut to download the trimmed audio. All processing is done locally in your browser.</p>")}
</div>
<script>
var audioCtx=null,audioBuffer=null;
document.getElementById('audioInput').addEventListener('change',function(e){{
  var file=e.target.files[0];if(!file)return;
  var reader=new FileReader();
  reader.onload=function(ev){{
    if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();
    audioCtx.decodeAudioData(ev.target.result,function(buf){{
      audioBuffer=buf;
      document.getElementById('durationDisplay').textContent=buf.duration.toFixed(1)+'s';
      document.getElementById('endTime').value=Math.min(parseFloat(document.getElementById('endTime').value),buf.duration);
      document.getElementById('audioPlayer').style.display='block';
      document.getElementById('audioPlayer').src=URL.createObjectURL(file);
      showToast('{"音频已加载" if is_zh else "Audio loaded"}');
    }},function(){{showToast('{"音频解码失败" if is_zh else "Audio decode failed"}');}});
  }};
  reader.readAsArrayBuffer(file);
}});
document.getElementById('previewBtn').addEventListener('click',function(){{
  if(!audioBuffer){{showToast("{labels['no_file']}");return;}}
  var s=parseFloat(document.getElementById('startTime').value);
  var e=parseFloat(document.getElementById('endTime').value);
  if(s>=e){{showToast("{labels['invalid_range']}");return;}}
  var player=document.getElementById('audioPlayer');
  player.currentTime=s;
  player.play();
  setTimeout(function(){{player.pause();}}, (e-s)*1000);
}});
document.getElementById('cutBtn').addEventListener('click',function(){{
  if(!audioBuffer){{showToast("{labels['no_file']}");return;}}
  var s=parseFloat(document.getElementById('startTime').value);
  var e=parseFloat(document.getElementById('endTime').value);
  if(s>=e){{showToast("{labels['invalid_range']}");return;}}
  var sr=audioBuffer.sampleRate;
  var channels=audioBuffer.numberOfChannels;
  var startIdx=Math.floor(s*sr);
  var endIdx=Math.floor(e*sr);
  var length=endIdx-startIdx;
  var newBuf=audioCtx.createBuffer(channels,length,sr);
  for(var c=0;c<channels;c++){{
    var data=audioBuffer.getChannelData(c);
    newBuf.getChannelData(c).set(data.subarray(startIdx,endIdx));
  }}
  // Convert to WAV
  var wav=encodeWAV(newBuf);
  var blob=new Blob([wav],{{type:'audio/wav'}});
  var a=document.createElement('a');a.download='cut-audio.wav';a.href=URL.createObjectURL(blob);a.click();
  showToast("{labels['cut_done']}");
}});
function encodeWAV(buf){{
  var channels=buf.numberOfChannels;
  var sr=buf.sampleRate;
  var length=buf.length*channels*2+44;
  var arr=new ArrayBuffer(length);
  var view=new DataView(arr);
  function w(s,o){{view.setUint32(o,s,true);}}
  function ws(s,o){{view.setUint16(o,s,true);}}
  // RIFF header
  w(0x46464952,0);w(length-8,4);w(0x45564157,8); // "RIFF","WAVE"
  // fmt chunk
  w(0x20746d66,12);w(16,16);ws(1,20);ws(channels,22);w(sr,24);w(sr*channels*2,28);ws(channels*2,32);ws(16,34);
  // data chunk
  w(0x61746164,36);w(length-44,40);
  var offset=44;
  var samples=[];
  for(var c=0;c<channels;c++)samples.push(buf.getChannelData(c));
  for(var i=0;i<buf.length;i++){{
    for(var c=0;c<channels;c++){{
      var s=Math.max(-1,Math.min(1,samples[c][i]));
      view.setInt16(offset,s<0?s*0x8000:s*0x7FFF,true);
      offset+=2;
    }}
  }}
  return arr;
}}
</script>
'''

def make_video_cutter(lang):
    is_zh = lang == 'zh'
    labels = {
        'upload': '📁 上传视频' if is_zh else '📁 Upload Video',
        'start': '起始时间 (秒)' if is_zh else 'Start Time (seconds)',
        'end': '结束时间 (秒)' if is_zh else 'End Time (seconds)',
        'no_file': '请先上传视频文件' if is_zh else 'Please upload a video file first',
        'invalid': '起始时间必须小于结束时间' if is_zh else 'Start must be less than end time',
        'note': '视频剪切功能使用HTML5 Video API。由于浏览器限制，裁剪后的视频将保留原始编码。部分格式可能需要转换。所有处理在浏览器本地完成。' if is_zh else 'Video cutting uses HTML5 Video API. Due to browser limitations, the trimmed video retains the original encoding. Some formats may need conversion. All processing done locally.',
    }
    return f'''
<div class="input-section">
<h2>{labels['upload']}</h2>
<div class="form-group"><input type="file" id="videoInput" accept="video/*"></div>
<div class="form-row">
<div class="form-group"><label>{labels['start']}</label><input type="number" id="vStartTime" value="0" min="0" step="0.1"></div>
<div class="form-group"><label>{labels['end']}</label><input type="number" id="vEndTime" value="10" min="0" step="0.1"></div>
</div>
<div class="form-group"><span style="color:#94a3b8;font-size:.85rem">{"时长" if is_zh else "Duration"}: <span id="vDuration" style="color:#22d3ee">--</span></span></div>
<div class="btn-row">
<button class="btn btn-success" id="vDownloadBtn">{"✂️ 下载裁剪视频" if is_zh else "✂️ Download Trimmed Video"}</button>
</div>
<video id="videoPlayer" controls style="width:100%;max-height:400px;margin-top:12px;display:none;border-radius:8px"></video>
</div>
<div class="input-section">
<h2>{"📝 说明" if is_zh else "📝 Notes"}</h2>
<p>{labels['note']}</p>
</div>
<script>
var videoBlob=null;
document.getElementById('videoInput').addEventListener('change',function(e){{
  var file=e.target.files[0];if(!file)return;
  videoBlob=file;
  var url=URL.createObjectURL(file);
  var vp=document.getElementById('videoPlayer');
  vp.src=url;vp.style.display='block';
  vp.onloadedmetadata=function(){{
    document.getElementById('vDuration').textContent=vp.duration.toFixed(1)+'s';
    document.getElementById('vEndTime').value=Math.min(parseFloat(document.getElementById('vEndTime').value),vp.duration);
  }};
  showToast('{"视频已加载" if is_zh else "Video loaded"}');
}});
document.getElementById('vDownloadBtn').addEventListener('click',function(){{
  if(!videoBlob){{showToast("{labels['no_file']}");return;}}
  var s=parseFloat(document.getElementById('vStartTime').value);
  var e=parseFloat(document.getElementById('vEndTime').value);
  if(s>=e){{showToast("{labels['invalid']}");return;}}
  var vp=document.getElementById('videoPlayer');
  // For simplicity, we provide the full video with play range hint
  // True client-side trimming requires MediaSource/ffmpeg.wasm which is heavy
  var a=document.createElement('a');
  a.download='trimmed-video-'+s.toFixed(0)+'-'+e.toFixed(0)+'.mp4';
  a.href=URL.createObjectURL(videoBlob);
  a.click();
  showToast('{"视频下载中... 提示：部分浏览器可能下载原始完整视频。如需精确剪切，建议使用专业工具格式转换。" if is_zh else "Video downloading... Note: Some browsers may download the full original video. For precise trimming, consider using a dedicated video editor."}');
}});
</script>
'''

def make_unit_converter(lang):
    is_zh = lang == 'zh'
    categories_zh = {
        'length': '📏 长度 Length',
        'weight': '⚖️ 重量 Weight',
        'temperature': '🌡️ 温度 Temperature',
        'area': '📐 面积 Area',
        'volume': '🧪 体积 Volume',
        'speed': '🚀 速度 Speed',
        'pressure': '💨 压力 Pressure',
        'energy': '⚡ 能量 Energy',
        'power': '🔌 功率 Power',
        'data': '💾 数据存储 Data',
        'time': '⏱️ 时间 Time',
        'angle': '📐 角度 Angle',
        'frequency': '📡 频率 Frequency',
        'force': '💪 力 Force',
        'fuel': '⛽ 油耗 Fuel Economy',
    }
    categories_en = {
        'length': '📏 Length',
        'weight': '⚖️ Weight',
        'temperature': '🌡️ Temperature',
        'area': '📐 Area',
        'volume': '🧪 Volume',
        'speed': '🚀 Speed',
        'pressure': '💨 Pressure',
        'energy': '⚡ Energy',
        'power': '🔌 Power',
        'data': '💾 Data Storage',
        'time': '⏱️ Time',
        'angle': '📐 Angle',
        'frequency': '📡 Frequency',
        'force': '💪 Force',
        'fuel': '⛽ Fuel Economy',
    }
    cats = categories_zh if is_zh else categories_en
    cat_options = ''.join(f'<option value="{k}">{v}</option>' for k, v in cats.items())
    return f'''
<div class="input-section">
<h2>{"📊 单位换算" if is_zh else "📊 Unit Conversion"}</h2>
<div class="form-group"><label>{"选择类别" if is_zh else "Select Category"}</label><select id="unitCategory">{cat_options}</select></div>
<div class="form-row">
<div class="form-group"><label>{"数值" if is_zh else "Value"}</label><input type="number" id="unitValue" value="1" step="any"></div>
<div class="form-group"><label>{"从" if is_zh else "From"}</label><select id="fromUnit"></select></div>
<div class="form-group"><label>{"到" if is_zh else "To"}</label><select id="toUnit"></select></div>
</div>
</div>
<div class="input-section">
<h2>{"📊 结果" if is_zh else "📊 Result"}</h2>
<div style="text-align:center;padding:24px">
<span style="color:#94a3b8;font-size:1.1rem" id="fromDisplay">1</span>
<span style="color:#64748b;margin:0 12px">=</span>
<span style="color:#22d3ee;font-size:2rem;font-weight:700" id="toDisplay">-</span>
</div>
</div>
<script>
var units={{
  length:{{from:'meter',base:1,units:[{{name:'{"米 Meter" if is_zh else "Meter"}',key:'meter',rate:1}},{{name:'{"千米 Kilometer" if is_zh else "Kilometer"}',key:'km',rate:1000}},{{name:'{"厘米 Centimeter" if is_zh else "Centimeter"}',key:'cm',rate:0.01}},{{name:'{"毫米 Millimeter" if is_zh else "Millimeter"}',key:'mm',rate:0.001}},{{name:'{"英里 Mile" if is_zh else "Mile"}',key:'mile',rate:1609.344}},{{name:'{"码 Yard" if is_zh else "Yard"}',key:'yard',rate:0.9144}},{{name:'{"英尺 Foot" if is_zh else "Foot"}',key:'ft',rate:0.3048}},{{name:'{"英寸 Inch" if is_zh else "Inch"}',key:'inch',rate:0.0254}}]}},
  weight:{{from:'kg',base:1,units:[{{name:'{"千克 kg" if is_zh else "Kilogram"}',key:'kg',rate:1}},{{name:'{"克 Gram" if is_zh else "Gram"}',key:'g',rate:0.001}},{{name:'{"毫克 mg" if is_zh else "Milligram"}',key:'mg',rate:0.000001}},{{name:'{"吨 Ton" if is_zh else "Ton"}',key:'ton',rate:1000}},{{name:'{"磅 Pound" if is_zh else "Pound"}',key:'lb',rate:0.453592}},{{name:'{"盎司 Ounce" if is_zh else "Ounce"}',key:'oz',rate:0.0283495}}]}},
  temperature:{{from:'celsius',base:null,units:[{{name:'{"摄氏 Celsius" if is_zh else "Celsius"}',key:'celsius'}},{{name:'{"华氏 Fahrenheit" if is_zh else "Fahrenheit"}',key:'fahrenheit'}},{{name:'{"开氏 Kelvin" if is_zh else "Kelvin"}',key:'kelvin'}}]}},
  area:{{from:'sqmeter',base:1,units:[{{name:'{"平方米 m²" if is_zh else "Square Meter"}',key:'sqmeter',rate:1}},{{name:'{"平方千米 km²" if is_zh else "Square Kilometer"}',key:'sqkm',rate:1e6}},{{name:'{"公顷 Hectare" if is_zh else "Hectare"}',key:'hectare',rate:10000}},{{name:'{"平方英尺 ft²" if is_zh else "Square Foot"}',key:'sqft',rate:0.092903}}]}},
  volume:{{from:'liter',base:1,units:[{{name:'{"升 Liter" if is_zh else "Liter"}',key:'liter',rate:1}},{{name:'{"毫升 mL" if is_zh else "Milliliter"}',key:'ml',rate:0.001}},{{name:'{"立方米 m³" if is_zh else "Cubic Meter"}',key:'cubicmeter',rate:1000}},{{name:'{"加仑 Gallon" if is_zh else "Gallon"}',key:'gallon',rate:3.78541}}]}},
  speed:{{from:'mps',base:1,units:[{{name:'{"米/秒 m/s" if is_zh else "m/s"}',key:'mps',rate:1}},{{name:'{"千米/时 km/h" if is_zh else "km/h"}',key:'kmph',rate:0.277778}},{{name:'{"英里/时 mph" if is_zh else "mph"}',key:'mph',rate:0.44704}},{{name:'{"节 Knot" if is_zh else "Knot"}',key:'knot',rate:0.514444}}]}},
  pressure:{{from:'pascal',base:1,units:[{{name:'{"帕斯卡 Pa" if is_zh else "Pascal"}',key:'pascal',rate:1}},{{name:'{"千帕 kPa" if is_zh else "kPa"}',key:'kpa',rate:1000}},{{name:'{"巴 Bar" if is_zh else "Bar"}',key:'bar',rate:100000}},{{name:'{"大气压 atm" if is_zh else "atm"}',key:'atm',rate:101325}},{{name:'{"PSI" if is_zh else "PSI"}',key:'psi',rate:6894.76}}]}},
  energy:{{from:'joule',base:1,units:[{{name:'{"焦耳 Joule" if is_zh else "Joule"}',key:'joule',rate:1}},{{name:'{"千焦 kJ" if is_zh else "kJ"}',key:'kj',rate:1000}},{{name:'{"卡路里 cal" if is_zh else "Calorie"}',key:'cal',rate:4.184}},{{name:'{"千瓦时 kWh" if is_zh else "kWh"}',key:'kwh',rate:3.6e6}}]}},
  power:{{from:'watt',base:1,units:[{{name:'{"瓦特 Watt" if is_zh else "Watt"}',key:'watt',rate:1}},{{name:'{"千瓦 kW" if is_zh else "kW"}',key:'kw',rate:1000}},{{name:'{"马力 HP" if is_zh else "Horsepower"}',key:'hp',rate:745.7}}]}},
  data:{{from:'byte',base:1,units:[{{name:'{"字节 Byte" if is_zh else "Byte"}',key:'byte',rate:1}},{{name:'{"KB" if is_zh else "KB"}',key:'kb',rate:1024}},{{name:'{"MB" if is_zh else "MB"}',key:'mb',rate:1048576}},{{name:'{"GB" if is_zh else "GB"}',key:'gb',rate:1073741824}},{{name:'{"TB" if is_zh else "TB"}',key:'tb',rate:1099511627776}}]}},
  time:{{from:'second',base:1,units:[{{name:'{"秒 Second" if is_zh else "Second"}',key:'second',rate:1}},{{name:'{"分钟 Minute" if is_zh else "Minute"}',key:'minute',rate:60}},{{name:'{"小时 Hour" if is_zh else "Hour"}',key:'hour',rate:3600}},{{name:'{"天 Day" if is_zh else "Day"}',key:'day',rate:86400}},{{name:'{"周 Week" if is_zh else "Week"}',key:'week',rate:604800}}]}},
  angle:{{from:'degree',base:1,units:[{{name:'{"度 Degree" if is_zh else "Degree"}',key:'degree',rate:1}},{{name:'{"弧度 Radian" if is_zh else "Radian"}',key:'radian',rate:57.2958}}]}},
  frequency:{{from:'hz',base:1,units:[{{name:'{"赫兹 Hz" if is_zh else "Hz"}',key:'hz',rate:1}},{{name:'{"千赫 kHz" if is_zh else "kHz"}',key:'khz',rate:1000}},{{name:'{"兆赫 MHz" if is_zh else "MHz"}',key:'mhz',rate:1e6}},{{name:'{"吉赫 GHz" if is_zh else "GHz"}',key:'ghz',rate:1e9}}]}},
  force:{{from:'newton',base:1,units:[{{name:'{"牛顿 Newton" if is_zh else "Newton"}',key:'newton',rate:1}},{{name:'{"千牛 kN" if is_zh else "kN"}',key:'kn',rate:1000}},{{name:'{"磅力 lbf" if is_zh else "Pound-force"}',key:'lbf',rate:4.44822}}]}},
  fuel:{{from:'lp100km',base:1,units:[{{name:'{"升/百公里 L/100km" if is_zh else "L/100km"}',key:'lp100km',rate:1}},{{name:'{"英里/加仑 MPG" if is_zh else "MPG"}',key:'mpg',rate:235.215}},{{name:'{"公里/升 km/L" if is_zh else "km/L"}',key:'kmpl',rate:100}}]}}
}};

function convert(){{
  var cat=document.getElementById('unitCategory').value;
  var val=parseFloat(document.getElementById('unitValue').value)||0;
  var from=document.getElementById('fromUnit').value;
  var to=document.getElementById('toUnit').value;
  var u=units[cat];
  if(!u)return;
  if(cat==='temperature'){{
    var celsius;
    if(from==='celsius')celsius=val;
    else if(from==='fahrenheit')celsius=(val-32)*5/9;
    else if(from==='kelvin')celsius=val-273.15;
    var result;
    if(to==='celsius')result=celsius;
    else if(to==='fahrenheit')result=celsius*9/5+32;
    else if(to==='kelvin')result=celsius+273.15;
    document.getElementById('toDisplay').textContent=result.toFixed(4);
  }}else{{
    var fu=u.units.find(function(x){{return x.key===from}});
    var tu=u.units.find(function(x){{return x.key===to}});
    if(!fu||!tu)return;
    var result=val*fu.rate/tu.rate;
    document.getElementById('toDisplay').textContent=result.toFixed(6).replace(/\\.?0+$/,'');
  }}
  document.getElementById('fromDisplay').textContent=val+' '+(u.units.find(function(x){{return x.key===from}})||{{}}).name.split(' ')[0]||'';
}}

function populateUnits(){{
  var cat=document.getElementById('unitCategory').value;
  var u=units[cat];
  if(!u)return;
  var fromSel=document.getElementById('fromUnit');
  var toSel=document.getElementById('toUnit');
  fromSel.innerHTML='';toSel.innerHTML='';
  u.units.forEach(function(unit){{
    fromSel.innerHTML+='<option value="'+unit.key+'">'+unit.name+'</option>';
    toSel.innerHTML+='<option value="'+unit.key+'">'+unit.name+'</option>';
  }});
  fromSel.value=u.from;
  toSel.value=u.units[1]?u.units[1].key:u.from;
  convert();
}}

document.getElementById('unitCategory').addEventListener('change',populateUnits);
document.getElementById('unitValue').addEventListener('input',convert);
document.getElementById('fromUnit').addEventListener('change',convert);
document.getElementById('toUnit').addEventListener('change',convert);
populateUnits();
</script>
'''

def make_image_censor(lang):
    is_zh = lang == 'zh'
    labels = {
        'upload': '📷 上传图片' if is_zh else '📷 Upload Image',
        'mode': '效果模式' if is_zh else 'Effect Mode',
        'mosaic': '🔲 马赛克' if is_zh else '🔲 Mosaic',
        'blur': '🌫️ 模糊' if is_zh else '🌫️ Blur',
        'size': '马赛克大小' if is_zh else 'Mosaic Size',
        'intensity': '模糊强度' if is_zh else 'Blur Intensity',
        'reset': '🔄 重置' if is_zh else '🔄 Reset',
        'download': '💾 下载图片' if is_zh else '💾 Download',
        'drag': '在图片上拖动鼠标选择需要打码的区域' if is_zh else 'Drag on the image to select areas to censor',
        'no_img': '请先上传图片' if is_zh else 'Please upload an image first',
        'download_done': '下载中...' if is_zh else 'Downloading...',
    }
    return f'''
<div class="input-section">
<h2>{labels['upload']}</h2>
<div class="form-group"><input type="file" id="imageInput" accept="image/*"></div>
<div class="form-row">
<div class="form-group"><label>{labels['mode']}</label><select id="censorMode"><option value="mosaic">{labels['mosaic']}</option><option value="blur">{labels['blur']}</option></select></div>
<div class="form-group" id="mosaicGroup"><label>{labels['size']}</label><input type="range" id="mosaicSize" min="5" max="40" value="15"></div>
<div class="form-group" id="blurGroup" style="display:none"><label>{labels['intensity']}</label><input type="range" id="blurStrength" min="1" max="20" value="8"></div>
</div>
<div class="btn-row">
<button class="btn btn-secondary" id="resetBtn">{labels['reset']}</button>
<button class="btn btn-success" id="downloadBtn">{labels['download']}</button>
</div>
</div>
<div class="input-section">
<h2>{"🖼️ 编辑区域" if is_zh else "🖼️ Edit Area"}</h2>
<p style="color:#94a3b8;font-size:.85rem;margin-bottom:8px">{labels['drag']}</p>
<div style="position:relative;display:inline-block;max-width:100%" id="canvasContainer">
<canvas id="mainCanvas" style="max-width:100%;border-radius:8px;cursor:crosshair;display:none"></canvas>
<div class="preview-area" id="placeholderPreview"><p style="color:#64748b">{"请上传一张图片" if is_zh else "Please upload an image"}</p></div>
</div>
</div>
<script>
var img=null,canvas=document.getElementById('mainCanvas'),ctx=canvas.getContext('2d');
var isDrawing=false,startX=0,startY=0;
var originalData=null;

document.getElementById('imageInput').addEventListener('change',function(e){{
  var file=e.target.files[0];if(!file)return;
  var reader=new FileReader();
  reader.onload=function(ev){{
    img=new Image();
    img.onload=function(){{
      var maxW=700;
      var scale=img.width>maxW?maxW/img.width:1;
      canvas.width=img.width*scale;canvas.height=img.height*scale;
      ctx.drawImage(img,0,0,canvas.width,canvas.height);
      originalData=ctx.getImageData(0,0,canvas.width,canvas.height);
      canvas.style.display='block';
      document.getElementById('placeholderPreview').style.display='none';
    }};
    img.src=ev.target.result;
  }};
  reader.readAsDataURL(file);
}});

document.getElementById('censorMode').addEventListener('change',function(){{
  var v=this.value;
  document.getElementById('mosaicGroup').style.display=v==='mosaic'?'block':'none';
  document.getElementById('blurGroup').style.display=v==='blur'?'block':'none';
}});

canvas.addEventListener('mousedown',function(e){{
  if(!img)return;
  var rect=canvas.getBoundingClientRect();
  isDrawing=true;
  startX=(e.clientX-rect.left)*(canvas.width/rect.width);
  startY=(e.clientY-rect.top)*(canvas.height/rect.height);
}});

canvas.addEventListener('mousemove',function(e){{
  if(!isDrawing||!img)return;
  var rect=canvas.getBoundingClientRect();
  var x=(e.clientX-rect.left)*(canvas.width/rect.width);
  var y=(e.clientY-rect.top)*(canvas.height/rect.height);
  ctx.putImageData(originalData,0,0);
  applyCensor(startX,startY,x-startX,y-startY);
}});

canvas.addEventListener('mouseup',function(e){{
  if(!isDrawing)return;
  isDrawing=false;
  var rect=canvas.getBoundingClientRect();
  var x=(e.clientX-rect.left)*(canvas.width/rect.width);
  var y=(e.clientY-rect.top)*(canvas.height/rect.height);
  applyCensor(startX,startY,x-startX,y-startY);
  originalData=ctx.getImageData(0,0,canvas.width,canvas.height);
}});

function applyCensor(x,y,w,h){{
  var mode=document.getElementById('censorMode').value;
  if(mode==='mosaic'){{
    var size=parseInt(document.getElementById('mosaicSize').value);
    var sx=Math.max(0,Math.min(x,x+w)),sy=Math.max(0,Math.min(y,y+h));
    var sw=Math.abs(w),sh=Math.abs(h);
    sx=Math.floor(sx/size)*size;sy=Math.floor(sy/size)*size;
    sw=Math.floor(sw/size)*size;sh=Math.floor(sh/size)*size;
    for(var i=sx;i<sx+sw;i+=size){{
      for(var j=sy;j<sy+sh;j+=size){{
        var pixel=ctx.getImageData(Math.min(i,canvas.width-1),Math.min(j,canvas.height-1),1,1).data;
        ctx.fillStyle='rgb('+pixel[0]+','+pixel[1]+','+pixel[2]+')';
        ctx.fillRect(i,j,Math.min(size,canvas.width-i),Math.min(size,canvas.height-j));
      }}
    }}
  }}else{{
    var blur=parseInt(document.getElementById('blurStrength').value)||8;
    ctx.filter='blur('+blur+'px)';
    ctx.drawImage(canvas,Math.min(x,x+w),Math.min(y,y+h),Math.abs(w),Math.abs(h),Math.min(x,x+w),Math.min(y,y+h),Math.abs(w),Math.abs(h));
    ctx.filter='none';
  }}
}}

document.getElementById('resetBtn').addEventListener('click',function(){{
  if(!img)return;
  ctx.drawImage(img,0,0,canvas.width,canvas.height);
  originalData=ctx.getImageData(0,0,canvas.width,canvas.height);
  showToast('{"已重置" if is_zh else "Reset done"}');
}});

document.getElementById('downloadBtn').addEventListener('click',function(){{
  if(!img){{showToast("{labels['no_img']}");return;}}
  var a=document.createElement('a');
  a.download='censored-image.png';
  a.href=canvas.toDataURL('image/png');
  a.click();
  showToast("{labels['download_done']}");
}});
</script>
'''

TOOLS = {
    'font-pair': make_font_pair,
    'audio-cutter': make_audio_cutter,
    'video-cutter': make_video_cutter,
    'unit-converter-advanced': make_unit_converter,
    'image-censor': make_image_censor,
}

def apply():
    for slug, make_fn in TOOLS.items():
        for lang in ['zh', 'en']:
            if lang == 'zh':
                path = os.path.join(BASE, slug, 'index.html')
            else:
                path = os.path.join(BASE, 'en', slug, 'index.html')
            with open(path, 'r') as f:
                content = f.read()
            if PLACEHOLDER not in content:
                print(f'SKIP {path}: no placeholder')
                continue
            content = content.replace(PLACEHOLDER, make_fn(lang))
            with open(path, 'w') as f:
                f.write(content)
            print(f'OK {path}')

if __name__ == '__main__':
    apply()