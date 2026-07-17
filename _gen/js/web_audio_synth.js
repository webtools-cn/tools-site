var audioCtx=null;
var oscillators=[];
var analyser=null;
function loadExample(){
document.getElementById('waveform').value='sawtooth';
document.getElementById('frequency').value='440';
document.getElementById('detune').value='0';
document.getElementById('gain').value='0.5';
document.getElementById('filterType').value='lowpass';
document.getElementById('filterFreq').value='2000';
document.getElementById('filterQ').value='1';
document.getElementById('attack').value='0.05';
document.getElementById('decay').value='0.1';
document.getElementById('sustain').value='0.7';
document.getElementById('release').value='0.3';
}
function clearInput(){
stopAll();
document.getElementById('frequency').value='440';
document.getElementById('detune').value='0';
document.getElementById('gain').value='0.5';
document.getElementById('output').textContent='等待生成...';
}
function initAudio(){
if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();
if(audioCtx.state==='suspended')audioCtx.resume();
}
function playNote(){
initAudio();
stopAll();
var wave=document.getElementById('waveform').value;
var freq=parseFloat(document.getElementById('frequency').value)||440;
var det=parseFloat(document.getElementById('detune').value)||0;
var vol=parseFloat(document.getElementById('gain').value)||0.5;
var fType=document.getElementById('filterType').value;
var fFreq=parseFloat(document.getElementById('filterFreq').value)||2000;
var fQ=parseFloat(document.getElementById('filterQ').value)||1;
var atk=parseFloat(document.getElementById('attack').value)||0.05;
var dec=parseFloat(document.getElementById('decay').value)||0.1;
var sus=parseFloat(document.getElementById('sustain').value)||0.7;
var rel=parseFloat(document.getElementById('release').value)||0.3;
var osc=audioCtx.createOscillator();
var gainNode=audioCtx.createGain();
var filter=audioCtx.createBiquadFilter();
osc.type=wave;
osc.frequency.value=freq;
osc.detune.value=det;
filter.type=fType;
filter.frequency.value=fFreq;
filter.Q.value=fQ;
var now=audioCtx.currentTime;
gainNode.gain.setValueAtTime(0,now);
gainNode.gain.linearRampToValueAtTime(vol,now+atk);
gainNode.gain.linearRampToValueAtTime(vol*sus,now+atk+dec);
gainNode.gain.linearRampToValueAtTime(0,now+atk+dec+rel+0.5);
osc.connect(filter);
filter.connect(gainNode);
analyser=audioCtx.createAnalyser();
analyser.fftSize=2048;
gainNode.connect(analyser);
analyser.connect(audioCtx.destination);
osc.start(now);
osc.stop(now+atk+dec+rel+1);
oscillators.push({osc:osc,gain:gainNode});
osc.onended=function(){
oscillators=oscillators.filter(function(o){return o.osc!==osc});
};
drawWaveform();
generateCode();
showToast('播放中');
}
function playChord(){
initAudio();
stopAll();
var wave=document.getElementById('waveform').value;
var vol=parseFloat(document.getElementById('gain').value)||0.3;
var fType=document.getElementById('filterType').value;
var fFreq=parseFloat(document.getElementById('filterFreq').value)||2000;
var fQ=parseFloat(document.getElementById('filterQ').value)||1;
var baseFreq=parseFloat(document.getElementById('frequency').value)||440;
var intervals=[1,1.2599,1.4983];
var atk=parseFloat(document.getElementById('attack').value)||0.05;
var dec=parseFloat(document.getElementById('decay').value)||0.1;
var sus=parseFloat(document.getElementById('sustain').value)||0.7;
var rel=parseFloat(document.getElementById('release').value)||0.3;
analyser=audioCtx.createAnalyser();
analyser.fftSize=2048;
analyser.connect(audioCtx.destination);
intervals.forEach(function(ratio){
var osc=audioCtx.createOscillator();
var gainNode=audioCtx.createGain();
var filter=audioCtx.createBiquadFilter();
osc.type=wave;
osc.frequency.value=baseFreq*ratio;
filter.type=fType;
filter.frequency.value=fFreq;
filter.Q.value=fQ;
var now=audioCtx.currentTime;
gainNode.gain.setValueAtTime(0,now);
gainNode.gain.linearRampToValueAtTime(vol,now+atk);
gainNode.gain.linearRampToValueAtTime(vol*sus,now+atk+dec);
gainNode.gain.linearRampToValueAtTime(0,now+atk+dec+rel+0.5);
osc.connect(filter);
filter.connect(gainNode);
gainNode.connect(analyser);
osc.start(now);
osc.stop(now+atk+dec+rel+1);
oscillators.push({osc:osc,gain:gainNode});
osc.onended=function(){oscillators=oscillators.filter(function(o){return o.osc!==osc})};
});
drawWaveform();
generateCode();
showToast('和弦播放中');
}
function stopAll(){
oscillators.forEach(function(o){try{o.osc.stop()}catch(e){}});
oscillators=[];
}
function drawWaveform(){
if(!analyser)return;
var canvas=document.getElementById('waveCanvas');
if(!canvas)return;
var ctx=canvas.getContext('2d');
var bufLen=analyser.frequencyBinCount;
var data=new Uint8Array(bufLen);
function draw(){
if(oscillators.length===0){ctx.clearRect(0,0,canvas.width,canvas.height);return}
analyser.getByteTimeDomainData(data);
ctx.fillStyle='#0f172a';
ctx.fillRect(0,0,canvas.width,canvas.height);
ctx.lineWidth=2;
ctx.strokeStyle='#06b6d4';
ctx.beginPath();
var sliceWidth=canvas.width/bufLen;
var x=0;
for(var i=0;i<bufLen;i++){
var v=data[i]/128.0;
var y=v*canvas.height/2;
if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
x+=sliceWidth;
}
ctx.lineTo(canvas.width,canvas.height/2);
ctx.stroke();
requestAnimationFrame(draw);
}
draw();
}
function generateCode(){
var wave=document.getElementById('waveform').value;
var freq=document.getElementById('frequency').value||'440';
var det=document.getElementById('detune').value||'0';
var vol=document.getElementById('gain').value||'0.5';
var fType=document.getElementById('filterType').value;
var fFreq=document.getElementById('filterFreq').value||'2000';
var fQ=document.getElementById('filterQ').value||'1';
var atk=document.getElementById('attack').value||'0.05';
var dec=document.getElementById('decay').value||'0.1';
var sus=document.getElementById('sustain').value||'0.7';
var rel=document.getElementById('release').value||'0.3';
var code='// Web Audio Synthesizer\n';
code+='const ctx = new AudioContext();\n\n';
code+='const osc = ctx.createOscillator();\n';
code+='osc.type = "'+wave+'";\n';
code+='osc.frequency.value = '+freq+';\n';
code+='osc.detune.value = '+det+';\n\n';
code+='const filter = ctx.createBiquadFilter();\n';
code+='filter.type = "'+fType+'";\n';
code+='filter.frequency.value = '+fFreq+';\n';
code+='filter.Q.value = '+fQ+';\n\n';
code+='const gain = ctx.createGain();\n';
code+='const now = ctx.currentTime;\n';
code+='gain.gain.setValueAtTime(0, now);\n';
code+='gain.gain.linearRampToValueAtTime('+vol+', now + '+atk+');\n';
code+='gain.gain.linearRampToValueAtTime('+(parseFloat(vol)*parseFloat(sus)).toFixed(2)+', now + '+(parseFloat(atk)+parseFloat(dec)).toFixed(2)+');\n';
code+='gain.gain.linearRampToValueAtTime(0, now + '+(parseFloat(atk)+parseFloat(dec)+parseFloat(rel)+0.5).toFixed(2)+');\n\n';
code+='osc.connect(filter);\n';
code+='filter.connect(gain);\n';
code+='gain.connect(ctx.destination);\n\n';
code+='osc.start(now);\n';
code+='osc.stop(now + '+(parseFloat(atk)+parseFloat(dec)+parseFloat(rel)+1).toFixed(2)+');\n';
document.getElementById('output').textContent=code;
}
function execute(){
playNote();
}
function downloadOutput(){
var text=document.getElementById('output').textContent;
if(!text||text==='等待生成...'){showToast('请先播放生成代码');return}
downloadText('synth.js',text);
}
