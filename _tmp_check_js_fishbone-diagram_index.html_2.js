
(function(){
var el=function(id){return document.getElementById(id);};
var toastTimer=null;
function showToast(msg){var t=el('toast');t.textContent=msg;t.style.opacity='1';clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.style.opacity='0';},2000);}

var templates={
  '5m1e':[{name:'人员',causes:['培训不足','责任心不强','沟通不畅']},{name:'机器',causes:['设备老化','维护不及时','精度不足']},{name:'材料',causes:['来料不良','规格不符','供应不稳定']},{name:'方法',causes:['流程不标准','操作不规范','缺少SOP']},{name:'测量',causes:['量具不准','标准不统一','未定期校准']},{name:'环境',causes:['温湿度不达标','照明不足','现场5S差']}],
  '4p':[{name:'产品',causes:['质量不稳定','功能不足','包装不好']},{name:'价格',causes:['定价过高','折扣不够','性价比低']},{name:'渠道',causes:['覆盖不足','配送慢','经销商少']},{name:'促销',causes:['广告少','活动无趣','品牌认知低']}],
  '4s':[{name:'服务',causes:['响应慢','态度差','专业性不足']},{name:'速度',causes:['排队太久','处理流程长','系统卡顿']},{name:'安全',causes:['数据泄露','支付风险','隐私问题']},{name:'售后',causes:['退换难','维修慢','投诉无门']}],
  'custom':[{name:'类别1',causes:['原因A']},{name:'类别2',causes:['原因B']},{name:'类别3',causes:['原因C']},{name:'类别4',causes:['原因D']}]
};

var currentTemplate='5m1e';
var categories=JSON.parse(JSON.stringify(templates['5m1e']));

function renderCategories(){
  var html='';
  categories.forEach(function(cat,i){
    html+='<div class="cat-block"><div class="cat-header"><span class="cat-name">📌 '+cat.name+'</span><button class="btn btn-sm btn-danger" data-action="removeCat" data-idx="'+i+'">✕</button></div>';
    html+='<div class="cat-causes">';
    cat.causes.forEach(function(c,j){
      html+='<span class="cause-tag">'+c+'<span class="remove" data-action="removeCause" data-cat="'+i+'" data-idx="'+j+'">✕</span></span>';
    });
    html+='</div>';
    html+='<div class="cause-input-row"><input type="text" placeholder="添加原因..." data-cat="'+i+'" class="cause-input"><button class="btn btn-sm btn-primary" data-action="addCause" data-cat="'+i+'">+</button></div>';
    html+='</div>';
  });
  html+='<button class="btn btn-sm btn-secondary" id="addCatBtn" style="margin-top:8px">+ 添加类别</button>';
  el('categoriesContainer').innerHTML=html;
  bindCatEvents();
}

function bindCatEvents(){
  document.querySelectorAll('[data-action="removeCat"]').forEach(function(btn){
    btn.addEventListener('click',function(){
      if(categories.length<=2){showToast('至少保留2个类别');return;}
      categories.splice(parseInt(this.dataset.idx),1);
      renderCategories();
    });
  });
  document.querySelectorAll('[data-action="removeCause"]').forEach(function(btn){
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      categories[parseInt(this.dataset.cat)].causes.splice(parseInt(this.dataset.idx),1);
      renderCategories();
    });
  });
  document.querySelectorAll('[data-action="addCause"]').forEach(function(btn){
    btn.addEventListener('click',function(){
      var catIdx=parseInt(this.dataset.cat);
      var input=document.querySelector('.cause-input[data-cat="'+catIdx+'"]');
      var val=input.value.trim();
      if(!val){showToast('请输入原因内容');return;}
      categories[catIdx].causes.push(val);
      input.value='';
      renderCategories();
    });
  });
  var addCatBtn=el('addCatBtn');
  if(addCatBtn){
    addCatBtn.addEventListener('click',function(){
      var name=prompt('类别名称：');
      if(!name||!name.trim())return;
      categories.push({name:name.trim(),causes:[]});
      renderCategories();
    });
  }
  document.querySelectorAll('.cause-input').forEach(function(inp){
    inp.addEventListener('keydown',function(e){
      if(e.key==='Enter'){
        var catIdx=parseInt(this.dataset.cat);
        var val=this.value.trim();
        if(!val)return;
        categories[catIdx].causes.push(val);
        this.value='';
        renderCategories();
      }
    });
  });
}

function drawDiagram(){
  var canvas=el('diagramCanvas');
  var ctx=canvas.getContext('2d');
  var w=canvas.width,h=canvas.height;
  ctx.clearRect(0,0,w,h);

  var cx=w-120,cy=h/2;
  var spineLen=w-280;

  // 脊骨
  ctx.strokeStyle='#334155';
  ctx.lineWidth=4;
  ctx.beginPath();ctx.moveTo(80,cy);ctx.lineTo(cx,cy);ctx.stroke();

  // 鱼头
  ctx.fillStyle='#ef4444';
  ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx-40,cy-30);ctx.lineTo(cx-40,cy+30);ctx.closePath();ctx.fill();
  ctx.fillStyle='#fff';
  ctx.font='bold 14px sans-serif';
  ctx.textAlign='center';
  var title=el('problemTitle').value||'问题';
  ctx.fillText(title,cx-20,cy+5);

  // 类别分支
  var n=categories.length;
  var colors=['#06b6d4','#10b981','#f59e0b','#8b5cf6','#ec4899','#f97316','#14b8a6','#6366f1'];
  var spacing=h/(n+1);

  categories.forEach(function(cat,i){
    var y=spacing*(i+1);
    var color=colors[i%colors.length];
    var spineX=80+spineLen*((i+1)/(n+1));

    // 分支骨
    ctx.strokeStyle=color;
    ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(spineX,cy);ctx.lineTo(spineX+60,y);ctx.stroke();

    // 类别名称
    ctx.fillStyle=color;
    ctx.font='bold 13px sans-serif';
    ctx.textAlign='left';
    ctx.fillText(cat.name,spineX+64,y+5);

    // 子原因
    ctx.font='11px sans-serif';
    ctx.fillStyle='#475569';
    var subSpacing=100;
    cat.causes.forEach(function(cause,j){
      var sx=spineX+70+subSpacing*j;
      ctx.fillText('• '+cause,sx,y+22);
    });
  });
}

function exportPNG(){
  var canvas=el('diagramCanvas');
  var link=document.createElement('a');
  link.download='fishbone-diagram.png';
  link.href=canvas.toDataURL('image/png');
  link.click();
  showToast('图片已导出 ✅');
}

function resetAll(){
  categories=JSON.parse(JSON.stringify(templates['5m1e']));
  currentTemplate='5m1e';
  el('problemTitle').value='客户满意度下降';
  document.querySelectorAll('.template-btn').forEach(function(b){b.classList.remove('active');});
  document.querySelector('[data-template="5m1e"]').classList.add('active');
  renderCategories();
  drawDiagram();
  showToast('已重置');
}

document.querySelectorAll('.template-btn').forEach(function(btn){
  btn.addEventListener('click',function(){
    document.querySelectorAll('.template-btn').forEach(function(b){b.classList.remove('active');});
    this.classList.add('active');
    currentTemplate=this.dataset.template;
    categories=JSON.parse(JSON.stringify(templates[currentTemplate]));
    renderCategories();
    drawDiagram();
  });
});

el('drawBtn').addEventListener('click',drawDiagram);
el('exportBtn').addEventListener('click',exportPNG);
el('resetBtn').addEventListener('click',resetAll);

el('problemTitle').addEventListener('input',drawDiagram);
renderCategories();
drawDiagram();
})();
