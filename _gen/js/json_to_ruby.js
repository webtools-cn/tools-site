function loadExample(){
document.getElementById('input').value='{\n  "name": "张三",\n  "age": 25,\n  "email": "zhang@example.com",\n  "is_vip": true,\n  "address": {\n    "city": "上海",\n    "zip_code": "200000"\n  },\n  "tags": ["ruby", "dev"]\n}';
execute();
}
function clearInput(){document.getElementById('input').value='';document.getElementById('output').textContent='等待生成...'}
function capitalize(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function toSnakeCase(s){return s.replace(/([A-Z])/g,'_$1').toLowerCase().replace(/^_/,'')}
function toCamelCase(s){return s.replace(/_([a-z])/g,function(m,c){return c.toUpperCase()})}
function rubyClass(val){
if(val===null)return 'nil';
if(typeof val==='string')return 'String';
if(typeof val==='boolean')return 'Boolean';
if(typeof val==='number'){if(Number.isInteger(val))return 'Integer';return 'Float'}
if(Array.isArray(val)){if(val.length>0)return 'Array<'+rubyClass(val[0])+'>';return 'Array'}
return 'Object';
}
function generateClass(obj,name,useStruct,useAttr,indent){
indent=indent||'';var lines=[];
if(useStruct){
lines.push(indent+'# frozen_string_literal: true');
lines.push(indent+'');
lines.push(indent+'require \'ostruct\'');
lines.push(indent+'');
lines.push(indent+name+' = Struct.new(');
var keys=Object.keys(obj);
lines.push(indent+'  '+keys.map(function(k){return ':'+toSnakeCase(k)}).join(', '));
lines.push(indent+', keyword_init: true)');
lines.push(indent+'');
lines.push(indent+'# Example usage:');
lines.push(indent+'# data = '+name+'.new(');
for(var i=0;i<keys.length;i++){
var k=keys[i];var v=obj[k];var field=toSnakeCase(k);
var example=typeof v==='string'?"'"+v+"'":(typeof v==='boolean'?(v?'true':'false'):JSON.stringify(v));
var comma=i<keys.length-1?',':'';
lines.push(indent+'#   '+field+': '+example+comma);
}
lines.push(indent+'# )');
}else{
lines.push(indent+'# frozen_string_literal: true');
lines.push(indent+'');
lines.push(indent+'require \'json\'');
lines.push(indent+'');
lines.push(indent+'class '+name);
if(useAttr){
lines.push(indent+'  attr_accessor '+Object.keys(obj).map(function(k){return ':'+toSnakeCase(k)}).join(', '));
lines.push(indent+'');
}
lines.push(indent+'  def initialize('+Object.keys(obj).map(function(k){return toSnakeCase(k)+': nil'}).join(', ')+')');
for(var key in obj){
if(!obj.hasOwnProperty(key))continue;
var field=toSnakeCase(key);
lines.push(indent+'    @'+field+' = '+field);
}
lines.push(indent+'  end');
lines.push(indent+'');
lines.push(indent+'  def to_h');
lines.push(indent+'    {');
for(var key in obj){
if(!obj.hasOwnProperty(key))continue;
var field=toSnakeCase(key);
lines.push(indent+'      '+field+': @'+field+',');
}
lines.push(indent+'    }');
lines.push(indent+'  end');
lines.push(indent+'');
lines.push(indent+'  def to_json(*args)');
lines.push(indent+'    to_h.to_json(*args)');
lines.push(indent+'  end');
lines.push(indent+'');
lines.push(indent+'  def self.from_json(json_str)');
lines.push(indent+'    data = JSON.parse(json_str, symbolize_names: true)');
lines.push(indent+'    new(');
for(var key in obj){
if(!obj.hasOwnProperty(key))continue;
var field=toSnakeCase(key);
lines.push(indent+'      '+field+': data[:'+field+'],');
}
lines.push(indent+'    )');
lines.push(indent+'  end');
lines.push(indent+'end');
}
return lines.join('\n');
}
function execute(){
var raw=document.getElementById('input').value.trim();
if(!raw){showToast('请输入JSON');return}
try{var obj=JSON.parse(raw)}catch(e){showToast('JSON解析失败: '+e.message);return}
var className=document.getElementById('className').value||'MyData';
var useStruct=document.getElementById('classType').value==='struct';
var useAttr=document.getElementById('useAttr').checked;
var code=generateClass(obj,className,useStruct,useAttr,'');
document.getElementById('output').textContent=code;
saveHistory('jsonToRubyHistory',raw.substring(0,100));
showToast('Ruby类生成完成');
}
function downloadOutput(){
var text=document.getElementById('output').textContent;
if(!text||text==='等待生成...'){showToast('请先生成代码');return}
var name=document.getElementById('className').value||'my_data';
downloadText(name+'.rb',text);
}
window.addEventListener('load',function(){loadExample()});
