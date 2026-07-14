function loadExample(){
document.getElementById('input').value='{\n  "name": "Alice",\n  "age": 30,\n  "score": 95.5,\n  "is_active": true,\n  "address": {\n    "street": "123 Main St",\n    "city": "Beijing"\n  },\n  "tags": ["cpp", "dev"]\n}';
execute();
}
function clearInput(){document.getElementById('input').value='';document.getElementById('output').textContent='等待生成...'}
function capitalize(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function toCamelCase(s){return s.replace(/_([a-z])/g,function(m,c){return c.toUpperCase()})}
function cppType(val,useStdString){
if(val===null)return 'std::variant<int,double,bool,std::string>';
if(typeof val==='string')return useStdString?'std::string':'std::string';
if(typeof val==='boolean')return 'bool';
if(typeof val==='number'){if(Number.isInteger(val))return 'int';return 'double'}
if(Array.isArray(val)){if(val.length>0)return 'std::vector<'+cppType(val[0],useStdString)+'>';return 'std::vector<std::variant<int,double,bool,std::string>>'}
return 'std::any';
}
function generateStruct(obj,name,useStdString,useNlohmann,indent){
indent=indent||'';var lines=[];
if(useNlohmann)lines.push(indent+'// Requires: #include <nlohmann/json.hpp>');
lines.push(indent+'struct '+name+' {');
var innerStructs=[];
for(var key in obj){
if(!obj.hasOwnProperty(key))continue;
var val=obj[key];var field=toCamelCase(key);var type=cppType(val,useStdString);
if(typeof val==='object'&&val!==null&&!Array.isArray(val)){
var innerName=capitalize(field);type=innerName;
innerStructs.push(generateStruct(val,innerName,useStdString,useNlohmann,indent+'  '));
lines.push(indent+'  '+type+' '+field+';');
}else if(Array.isArray(val)&&val.length>0&&typeof val[0]==='object'&&val[0]!==null){
var innerName=capitalize(field.replace(/s$/,''));
innerStructs.push(generateStruct(val[0],innerName,useStdString,useNlohmann,indent+'  '));
lines.push(indent+'  std::vector<'+innerName+'> '+field+';');
}else{
lines.push(indent+'  '+type+' '+field+';');
}}
if(useNlohmann){
lines.push('');lines.push(indent+'  // NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE or manual to_json/from_json');
lines.push(indent+'  NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE('+name+', '+Object.keys(obj).map(function(k){return toCamelCase(k)}).join(', ')+')');
}
lines.push(indent+'};');
var result=lines.join('\n');
for(var i=0;i<innerStructs.length;i++){result+='\n\n'+innerStructs[i]}
return result;
}
function execute(){
var raw=document.getElementById('input').value.trim();
if(!raw){showToast('请输入JSON');return}
try{var obj=JSON.parse(raw)}catch(e){showToast('JSON解析失败: '+e.message);return}
var structName=document.getElementById('structName').value||'MyData';
var useNlohmann=document.getElementById('useNlohmann').checked;
var useStdString=true;
var code='#include <string>\n#include <vector>\n';
if(useNlohmann)code+='#include <nlohmann/json.hpp>\n';
code+='using json = nlohmann::json;\n\n';
code+=generateStruct(obj,structName,useStdString,useNlohmann,'');
document.getElementById('output').textContent=code;
saveHistory('jsonToCppHistory',raw.substring(0,100));
showToast('C++结构体生成完成');
}
function downloadOutput(){
var text=document.getElementById('output').textContent;
if(!text||text==='等待生成...'){showToast('请先生成代码');return}
var name=document.getElementById('structName').value||'MyData';
downloadText(name+'.hpp',text);
}
window.addEventListener('load',function(){loadExample()});
