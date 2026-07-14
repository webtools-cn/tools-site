function loadExample(){
document.getElementById('input').value='{\n  "name": "张三",\n  "age": 25,\n  "email": "zhang@example.com",\n  "isVip": true,\n  "address": {\n    "city": "北京",\n    "zipCode": "100000"\n  },\n  "tags": ["开发", "Java"]\n}';
execute();
}
function clearInput(){document.getElementById('input').value='';document.getElementById('output').textContent='等待生成...'}
function capitalize(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function toCamelCase(s){return s.replace(/_([a-z])/g,function(m,c){return c.toUpperCase()})}
function javaType(val,useWrapper){
if(val===null)return useWrapper?'Object':'Object';
if(typeof val==='string')return 'String';
if(typeof val==='boolean')return useWrapper?'Boolean':'boolean';
if(typeof val==='number'){if(Number.isInteger(val))return useWrapper?'Integer':'int';return useWrapper?'Double':'double'}
if(Array.isArray(val)){if(val.length>0)return 'List<'+javaType(val[0],useWrapper)+'>';return 'List<Object>'}
return 'Object';
}
function generateClass(obj,name,useWrapper,annType,pkg,genGs,indent){
indent=indent||'';var lines=[];
if(pkg)lines.push('package '+pkg+';');
if(annType==='jackson')lines.push('import com.fasterxml.jackson.annotation.JsonProperty;');
else if(annType==='gson')lines.push('import com.google.gson.annotations.SerializedName;');
if(lines.length>0&&pkg)lines.push('');
var ann=annType==='lombok'?'@Data':'';
if(ann)lines.push(indent+ann);
lines.push(indent+'public class '+name+' {');
var innerClasses=[];
for(var key in obj){
if(!obj.hasOwnProperty(key))continue;
var val=obj[key];var field=toCamelCase(key);var type=javaType(val,useWrapper);
if(typeof val==='object'&&val!==null&&!Array.isArray(val)){
var innerName=capitalize(field);type=innerName;
innerClasses.push(generateClass(val,innerName,useWrapper,annType,null,genGs,indent+'  '));
if(annType==='jackson')lines.push(indent+'  @JsonProperty("'+key+'")');
else if(annType==='gson')lines.push(indent+'  @SerializedName("'+key+'")');
lines.push(indent+'  private '+type+' '+field+';');
}else if(Array.isArray(val)&&val.length>0&&typeof val[0]==='object'&&val[0]!==null){
var innerName=capitalize(field.replace(/s$/,''));
innerClasses.push(generateClass(val[0],innerName,useWrapper,annType,null,genGs,indent+'  '));
if(annType==='jackson')lines.push(indent+'  @JsonProperty("'+key+'")');
else if(annType==='gson')lines.push(indent+'  @SerializedName("'+key+'")');
lines.push(indent+'  private List<'+innerName+'> '+field+' = new ArrayList<>();');
}else{
if(annType==='jackson')lines.push(indent+'  @JsonProperty("'+key+'")');
else if(annType==='gson')lines.push(indent+'  @SerializedName("'+key+'")');
lines.push(indent+'  private '+type+' '+field+';');
}}
if(genGs&&annType!=='lombok'){
lines.push('');
for(var key in obj){
if(!obj.hasOwnProperty(key))continue;
var field=toCamelCase(key);var val=obj[key];var type=javaType(val,useWrapper);
if(typeof val==='object'&&val!==null&&!Array.isArray(val))type=capitalize(field);
lines.push(indent+'  public '+type+' get'+capitalize(field)+'() { return '+field+'; }');
lines.push(indent+'  public void set'+capitalize(field)+'('+type+' '+field+') { this.'+field+' = '+field+'; }');
}}lines.push(indent+'}');
var result=lines.join('\n');
for(var i=0;i<innerClasses.length;i++){result+='\n\n'+innerClasses[i]}
return result;
}
function execute(){
var raw=document.getElementById('input').value.trim();
if(!raw){showToast('请输入JSON');return}
try{var obj=JSON.parse(raw)}catch(e){showToast('JSON解析失败: '+e.message);return}
var className=document.getElementById('className').value||'MyData';
var annType=document.getElementById('annotation').value;
var pkg=document.getElementById('packageName').value;
var useWrapper=document.getElementById('useWrapper').checked;
var genGs=document.getElementById('genGetterSetter').checked;
var code=generateClass(obj,className,useWrapper,annType,pkg,genGs,'');
document.getElementById('output').textContent=code;
saveHistory('jsonToJavaHistory',raw.substring(0,100));
showToast('Java类生成完成');
}
function downloadOutput(){
var text=document.getElementById('output').textContent;
if(!text||text==='等待生成...'){showToast('请先生成代码');return}
var name=document.getElementById('className').value||'MyData';
downloadText(name+'.java',text);
}
window.addEventListener('load',function(){loadExample()});
