
var cards = [];
var selectedIdx = -1;
var currentTab = 'css';

function hexToRgb(h){var r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);return r+','+g+','+b;}

function rebuildGrid(){
  var cols=parseInt(document.getElementById('cols').value)||4;
  var rows=parseInt(document.getElementById('rows').value)||3;
  var gap=document.getElementById('gap').value;
  var radius=document.getElementById('radius').value;
  var color=document.getElementById('card-color').value;
  cards=[];
  for(var i=0;i<cols*rows;i++){
    cards.push({spanCol:1,spanRow:1,color:color});
  }
  selectedIdx=-1;
  renderPreview();
  updateCode();
}

function renderPreview(){
  var cols=parseInt(document.getElementById('cols').value)||4;
  var gap=document.getElementById('gap').value;
  var radius=document.getElementById('radius').value;
  var container=document.getElementById('bento-preview');
  container.style.gridTemplateColumns='repeat('+cols+',1fr)';
  container.style.gap=gap+'px';
  container.innerHTML='';
  cards.forEach(function(c,i){
    var div=document.createElement('div');
    div.className='bento-item';
    if(c.spanCol>1)div.classList.add('span-col-'+c.spanCol);
    if(c.spanRow>1)div.classList.add('span-row-'+c.spanRow);
    div.style.borderRadius=radius+'px';
    var rgb=hexToRgb(c.color);
    div.style.background='rgba('+rgb+',0.15)';
    div.style.borderColor='rgba('+rgb+',0.3)';
    div.style.color='rgba('+rgb+',1)';
    div.textContent='Card '+(i+1)+(c.spanCol>1?' ['+c.spanCol+' cols]':'')+(c.spanRow>1?' ['+c.spanRow+' rows]':'');
    div.onclick=function(){selectCard(i);};
    if(i===selectedIdx)div.classList.add('selected');
    container.appendChild(div);
  });
}

function selectCard(i){
  selectedIdx=i;
  var c=cards[i];
  document.getElementById('span-col').value=c.spanCol;
  document.getElementById('span-row').value=c.spanRow;
  document.getElementById('item-color').value=c.color;
  renderPreview();
}

function updateSpan(){
  if(selectedIdx<0)return;
  cards[selectedIdx].spanCol=parseInt(document.getElementById('span-col').value);
  cards[selectedIdx].spanRow=parseInt(document.getElementById('span-row').value);
  renderPreview();
  updateCode();
}

function updateItemColor(){
  if(selectedIdx<0)return;
  cards[selectedIdx].color=document.getElementById('item-color').value;
  renderPreview();
  updateCode();
}

function updateGap(){
  document.getElementById('gap-val').textContent=document.getElementById('gap').value+'px';
  renderPreview();
  updateCode();
}

function updateRadius(){
  document.getElementById('radius-val').textContent=document.getElementById('radius').value+'px';
  renderPreview();
  updateCode();
}

function updateColors(){
  var color=document.getElementById('card-color').value;
  cards.forEach(function(c){c.color=color;});
  renderPreview();
  updateCode();
}

function updateCode(){
  var cols=parseInt(document.getElementById('cols').value)||4;
  var gap=document.getElementById('gap').value;
  var radius=document.getElementById('radius').value;
  var out=document.getElementById('code-output');
  if(currentTab==='css'){
    var css='.bento-grid {\n  display: grid;\n  grid-template-columns: repeat('+cols+', 1fr);\n  gap: '+gap+'px;\n}\n\n';
    cards.forEach(function(c,i){
      if(c.spanCol>1||c.spanRow>1){
        css+='.bento-item-'+(i+1)+' {\n';
        if(c.spanCol>1)css+='  grid-column: span '+c.spanCol+';\n';
        if(c.spanRow>1)css+='  grid-row: span '+c.spanRow+';\n';
        css+='}\n\n';
      }
    });
    css+='.bento-item {\n  border-radius: '+radius+'px;\n  padding: 16px;\n}';
    out.textContent=css;
  } else {
    var html='<div class="bento-grid">\n';
    cards.forEach(function(c,i){
      var cls='bento-item';
      if(c.spanCol>1||c.spanRow>1)cls+=' bento-item-'+(i+1);
      html+='  <div class="'+cls+'">Card '+(i+1)+'</div>\n';
    });
    html+='</div>';
    out.textContent=html;
  }
}

function switchTab(tab){
  currentTab=tab;
  document.querySelectorAll('.tab-btn').forEach(function(b){b.classList.remove('active');});
  event.target.classList.add('active');
  updateCode();
}

function copyCode(){
  var code=document.getElementById('code-output').textContent;
  if(!code){showToast('Generate code first');return;}
  navigator.clipboard.writeText(code).then(function(){showToast('✅ Copied to clipboard');});
}

function loadExample(){
  document.getElementById('cols').value=4;
  document.getElementById('rows').value=3;
  document.getElementById('gap').value=12;
  document.getElementById('radius').value=12;
  document.getElementById('gap-val').textContent='12px';
  document.getElementById('radius-val').textContent='12px';
  cards=[
    {spanCol:2,spanRow:2,color:'#0891b2'},
    {spanCol:1,spanRow:1,color:'#0e7490'},
    {spanCol:1,spanRow:1,color:'#0e7490'},
    {spanCol:1,spanRow:2,color:'#155e75'},
    {spanCol:1,spanRow:1,color:'#0e7490'},
    {spanCol:2,spanRow:1,color:'#0891b2'},
    {spanCol:1,spanRow:1,color:'#155e75'},
    {spanCol:1,spanRow:1,color:'#0e7490'},
  ];
  selectedIdx=-1;
  renderPreview();
  updateCode();
}

function resetGrid(){
  document.getElementById('cols').value=4;
  document.getElementById('rows').value=3;
  document.getElementById('gap').value=12;
  document.getElementById('radius').value=10;
  document.getElementById('card-color').value='#0e7490';
  document.getElementById('gap-val').textContent='12px';
  document.getElementById('radius-val').textContent='10px';
  rebuildGrid();
}

function toggleFeedback(){var p=document.getElementById('feedback-panel');p.style.display=p.style.display==='none'?'block':'none';}
function showToast(msg){var t=document.getElementById('toast');t.textContent=msg;t.style.opacity='1';setTimeout(function(){t.style.opacity='0';},2000);}

window.addEventListener('load',function(){loadExample();});
document.addEventListener('keydown',function(e){
  if(e.ctrlKey&&e.key==='Enter'){copyCode();e.preventDefault();}
  if(e.ctrlKey&&e.shiftKey&&e.key==='C'){copyCode();e.preventDefault();}
});
