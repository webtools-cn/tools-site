
function calculate(){
  const cigPerDay=parseFloat(document.getElementById('cigPerDay').value)||0;
  const cigPerPack=parseFloat(document.getElementById('cigPerPack').value)||20;
  const pricePerPack=parseFloat(document.getElementById('pricePerPack').value)||0;
  const smokedYears=parseFloat(document.getElementById('smokedYears').value)||0;
  const investReturn=parseFloat(document.getElementById('investReturn').value)||8;
  const investYears=parseFloat(document.getElementById('investYears').value)||20;

  if(cigPerDay<=0||pricePerPack<=0){showToast('pleaseFill in');return;}

  const dailyCost=cigPerDay/cigPerPack*pricePerPack;
  const monthlyCost=dailyCost*30;
  const yearlyCost=dailyCost*365;
  const totalSpent=yearlyCost*smokedYears;

  // opportunity cost: monthly cigarette money invested
  const r=investReturn/100/12;
  const months=investYears*12;
  const monthlyInvest=monthlyCost;
  const futureValue=monthlyInvest*((Math.pow(1+r,months)-1)/r);
  const totalCost=totalSpent+futureValue;

  document.getElementById('dailyCost').textContent='$'+dailyCost.toFixed(2);
  document.getElementById('monthlyCost').textContent='$'+monthlyCost.toFixed(0);
  document.getElementById('yearlyCost').textContent='$'+yearlyCost.toFixed(0);
  document.getElementById('totalSpent').textContent='$'+totalSpent.toFixed(0);
  document.getElementById('opportunityCost').textContent='$'+futureValue.toFixed(0);
  document.getElementById('totalCost').textContent='$'+totalCost.toFixed(0);

  // Milestones
  const milestones={m1m:1/12, m1y:1, m5y:5, m10y:10, m20y:20, m30y:30};
  for(const [id, yrs] of Object.entries(milestones)){
    const m=Math.min(yrs*12, months);
    const val=monthlyInvest*((Math.pow(1+r, m)-1)/r);
    document.getElementById(id).textContent='$'+val.toFixed(0);
  }

  document.getElementById('resultCard').style.display='block';
  document.getElementById('resultCard').scrollIntoView({behavior:'smooth'});
}

function clearAll(){
  document.getElementById('cigPerDay').value='20';
  document.getElementById('cigPerPack').value='20';
  document.getElementById('pricePerPack').value='';
  document.getElementById('smokedYears').value='0';
  document.getElementById('investReturn').value='8';
  document.getElementById('investYears').value='20';
  document.getElementById('resultCard').style.display='none';
}

function copyResult(){
  const lines=[
    '🚬 Smoking Cost Report',
    'Daily Cost: '+document.getElementById('dailyCost').textContent,
    'Monthly Cost: '+document.getElementById('monthlyCost').textContent,
    'Yearly Cost: '+document.getElementById('yearlyCost').textContent,
    'Total spent smoking so far: '+document.getElementById('totalSpent').textContent,
    'If invested instead: '+document.getElementById('investYears').value+'years would yield: '+document.getElementById('opportunityCost').textContent,
    ' Total cost: '+document.getElementById('totalCost').textContent,
    '',
    '📅 Cigarette money could buy:',
    '1 month: '+document.getElementById('m1m').textContent+' ≈ a nice dinner',
    '1 year: '+document.getElementById('m1y').textContent+' ≈ a new smartphone',
    '5 years: '+document.getElementById('m5y').textContent+' ≈ a car down payment',
    '10 years: '+document.getElementById('m10y').textContent+' ≈ one year of college tuition',
    '20 years: '+document.getElementById('m20y').textContent+' ≈ a condo in a small city',
    '30years: '+document.getElementById('m30y').textContent+' Early retirement fund'
  ];
  navigator.clipboard.writeText(lines.join('\n')).then(()=>showToast('✅ Copied to clipboard'));
}

function showToast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2000);
}

function fillExample(){
  var vals = [["cigPerDay", "20"], ["cigPerPack", "20"], ["pricePerPack", "20"], ["smokedYears", "5"], ["investReturn", "8"], ["investYears", "20"]];
  for(var i=0;i<vals.length;i++){
    var el = document.getElementById(vals[i][0]);
    if(el){el.value = vals[i][1];}
  }
  calculate();
  var t=document.getElementById('toast');
  if(t){t.textContent='Example filled & calculated';t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000)}
}
