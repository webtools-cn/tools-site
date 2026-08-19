
(function(){
var el=function(id){return document.getElementById(id);};
var plans={
  muscle:{name:{cn:'增肌',en:'Muscle Gain'},exercises:{beginner:[['俯卧撑','3组×10次'],['哑铃弯举','3组×12次'],['深蹲','3组×12次'],['仰卧起坐','3组×15次']],intermediate:[['卧推','4组×8次'],['引体向上','4组×8次'],['深蹲','4组×10次'],['硬拉','4组×8次'],['肩推','3组×10次'],['杠铃划船','3组×10次']],advanced:[['卧推','5组×5次'],['深蹲','5组×5次'],['硬拉','5组×5次'],['引体向上','4组×8次'],['杠铃划船','4组×8次'],['肩推','4组×8次'],['臂屈伸','3组×10次'],['弯举','3组×10次']]}},
  fatloss:{name:{cn:'减脂',en:'Fat Loss'},exercises:{beginner:[['开合跳','3组×30秒'],['高抬腿','3组×30秒'],['波比跳','3组×8次'],['平板支撑','3组×30秒']],intermediate:[['跑步','20分钟'],['跳绳','4组×2分钟'],['波比跳','4组×10次'],['深蹲跳','4组×12次'],['登山者','4组×30秒']],advanced:[['HIIT冲刺','8组×30秒'],['波比跳','5组×15次'],['壶铃摆荡','4组×15次'],['跳绳双摇','4组×1分钟'],['战绳','4组×30秒'],['深蹲跳','4组×15次']]}},
  toning:{name:{cn:'塑形',en:'Body Toning'},exercises:{beginner:[['臀桥','3组×15次'],['平板支撑','3组×20秒'],['哑铃侧平举','3组×12次'],['卷腹','3组×15次']],intermediate:[['深蹲','4组×12次'],['哑铃飞鸟','4组×12次'],['臀推','4组×12次'],['俄罗斯转体','4组×20次'],['保加利亚蹲','3组×10次']],advanced:[['深蹲','4组×15次'],['硬拉','4组×12次'],['哑铃飞鸟','4组×15次'],['臀推','4组×15次'],['面拉','3组×15次'],['悬垂举腿','3组×12次']]}}
};

el('generateBtn').addEventListener('click',function(){
  var goal=el('goal').value,level=el('level').value,days=parseInt(el('daysPerWeek').value);
  var plan=plans[goal],exSet=plan.exercises[level];
  var html='<div style="background:#0f172a;border-radius:10px;padding:16px;border:1px solid rgba(148,163,184,.1)">';
  html+='<div class="result-grid" style="margin-bottom:16px">';
  html+='<div class="result-card"><div class="result-label">🎯 训练目标</div><div class="result-value" style="font-size:1rem">'+plan.name.cn+'</div></div>';
  html+='<div class="result-card"><div class="result-label">📅 每周训练</div><div class="result-value" style="font-size:1rem">'+days+'天/周</div></div>';
  html+='<div class="result-card"><div class="result-label">⏱️ 单次时长</div><div class="result-value" style="font-size:1rem">'+el('duration').value+'分钟</div></div>';
  html+='<div class="result-card"><div class="result-label">🏅 训练水平</div><div class="result-value" style="font-size:1rem">'+el('level').selectedOptions[0].text+'</div></div>';
  html+='</div>';
  var dayNames=['周一','周二','周三','周四','周五','周六','周日'];
  for(var d=0;d<days;d++){
    html+='<div class="task-item"><div class="task-name">'+dayNames[d]+'</div><div style="margin-top:8px;color:#94a3b8;font-size:.85rem">';
    var start=d*Math.floor(exSet.length/days)+Math.min(d,exSet.length%days);
    var count=Math.floor(exSet.length/days)+(d<exSet.length%days?1:0);
    for(var e=start;e<start+count&&e<exSet.length;e++){
      html+=exSet[e][0]+': '+exSet[e][1]+'<br>';
    }
    html+='</div></div>';
  }
  html+='<p style="color:#f59e0b;font-size:.8rem;margin-top:12px">⚠️ 热身5分钟+拉伸5分钟。组间休息60-90秒。如有不适请停止训练。</p>';
  html+='</div>';
  el('planOutput').innerHTML=html;
  el('copyRow').style.display='flex';
  showToast('计划已生成 🏋️');
});

el('resetBtn').addEventListener('click',function(){
  el('goal').value='muscle';el('level').value='beginner';el('daysPerWeek').value='3';el('duration').value='45';
  el('planOutput').innerHTML='<div style="color:#94a3b8;text-align:center;padding:20px">👆 选择目标并点击"生成计划"</div>';
  el('copyRow').style.display='none';showToast('已重置 🔄');
});
})();
