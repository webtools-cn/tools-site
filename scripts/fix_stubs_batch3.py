#!/usr/bin/env python3
"""Fix stub functions batch 3 - more tools"""
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def replace_stub_func(content, func_name, new_impl):
    """Replace a stub function that has 'coming soon'"""
    pattern = rf'function {re.escape(func_name)}\s*\([^)]*\)\s*\{{[^}}]*coming soon[^}}]*\}}'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return content[:match.start()] + new_impl + content[match.end():], True
    return content, False

def fix_yaml_diff(content):
    new_impl = """function compareYAML() {
  var a=document.getElementById('yamlA').value;
  var b=document.getElementById('yamlB').value;
  if(!a.trim()||!b.trim()){showToast('请输入两个YAML内容');return;}
  var linesA=a.split('\\n');
  var linesB=b.split('\\n');
  var maxLen=Math.max(linesA.length,linesB.length);
  var html='';
  var added=0,removed=0,modified=0;
  for(var i=0;i<maxLen;i++){
    var la=i<linesA.length?linesA[i]:null;
    var lb=i<linesB.length?linesB[i]:null;
    if(la===null&&lb!==null){html+='<div class="diff-added">+ '+escapeHtml(lb)+'</div>';added++}
    else if(la!==null&&lb===null){html+='<div class="diff-removed">- '+escapeHtml(la)+'</div>';removed++}
    else if(la!==lb){html+='<div class="diff-modified">~ '+escapeHtml(la)+' → '+escapeHtml(lb)+'</div>';modified++}
    else{html+='<div style="color:#64748b">  '+escapeHtml(la)+'</div>'}
  }
  function escapeHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
  document.getElementById('diffStats').style.display='block';
  document.getElementById('diffStats').innerHTML='新增:'+added+' 删除:'+removed+' 修改:'+modified;
  document.getElementById('diffResult').innerHTML=html;
  showToast('对比完成');
}"""
    content,_=replace_stub_func(content,'compareYAML',new_impl)
    return content

def fix_yaml_path_finder(content):
    new_list = """function listAllPaths() {
  var input=document.getElementById('yamlInput').value;
  if(!input.trim()){showToast('请输入YAML内容');return;}
  var lines=input.split('\\n');
  var paths=[];
  var stack=[];
  lines.forEach(function(line){
    if(!line.trim()||line.trim().startsWith('#'))return;
    var indent=line.length-line.replace(/^\\s+/,'').length;
    var match=line.match(/^(\\s*)([\\w-]+):\\s*(.*)$/);
    if(!match)return;
    var key=match[2];
    var val=match[3].trim();
    while(stack.length>0&&stack[stack.length-1].indent>=indent){stack.pop()}
    stack.push({indent:indent,key:key});
    var path=stack.map(function(s){return s.key}).join('.');
    if(val){paths.push(path+' = '+val)}else{paths.push(path)}
  });
  var html=paths.map(function(p){return '<div style="padding:2px 0;color:#94a3b8;font-family:monospace;font-size:.85rem">'+p+'</div>'}).join('');
  document.getElementById('pathList').innerHTML=html;
  document.getElementById('pathListArea').style.display='block';
  showToast('共'+paths.length+'条路径');
}"""
    content,_=replace_stub_func(content,'listAllPaths',new_list)
    
    new_query = """function queryPath() {
  var input=document.getElementById('yamlInput').value;
  var path=document.getElementById('pathInput').value.trim();
  if(!input.trim()){showToast('请输入YAML内容');return;}
  if(!path){showToast('请输入路径表达式');return;}
  var lines=input.split('\\n');
  var data={};
  var stack=[{indent:-1,obj:data}];
  lines.forEach(function(line){
    if(!line.trim()||line.trim().startsWith('#'))return;
    var indent=line.length-line.replace(/^\\s+/,'').length;
    var match=line.match(/^(\\s*)([\\w-]+):\\s*(.*)$/);
    if(!match)return;
    var key=match[2];
    var val=match[3].trim();
    while(stack.length>1&&stack[stack.length-1].indent>=indent){stack.pop()}
    var parent=stack[stack.length-1].obj;
    if(val){parent[key]=val}else{parent[key]={};stack.push({indent:indent,obj:parent[key]})}
  });
  var keys=path.split('.');
  var result=data;
  for(var i=0;i<keys.length;i++){
    if(result===undefined||result===null)break;
    result=result[keys[i]];
  }
  var html='';
  if(result===undefined){html='<span style="color:#f87171">未找到路径: '+path+'</span>'}
  else if(typeof result==='object'){html='<pre style="color:#e2e8f0;font-size:.85rem">'+JSON.stringify(result,null,2)+'</pre>'}
  else{html='<div style="color:#22d3ee;font-size:1.1rem;font-family:monospace">'+result+'</div>'}
  document.getElementById('resultArea').style.display='block';
  document.getElementById('resultArea').innerHTML='<h2>查询结果</h2>'+html;
  showToast('查询完成');
}"""
    content,_=replace_stub_func(content,'queryPath',new_query)
    return content

def fix_vcf_generator(content):
    new_impl = """function previewVCF() {
  var ln=document.getElementById('lastName').value||'';
  var fn=document.getElementById('firstName').value||'';
  var cell=document.getElementById('cellPhone').value||'';
  var work=document.getElementById('workPhone').value||'';
  var pe=document.getElementById('personalEmail').value||'';
  var we=document.getElementById('workEmail').value||'';
  var org=document.getElementById('org').value||'';
  var title=document.getElementById('title').value||'';
  var url=document.getElementById('url').value||'';
  var bday=document.getElementById('bday').value||'';
  var street=document.getElementById('street').value||'';
  var city=document.getElementById('city').value||'';
  var region=document.getElementById('region').value||'';
  var postal=document.getElementById('postalCode').value||'';
  var country=document.getElementById('country').value||'';
  var note=document.getElementById('note').value||'';
  if(!ln&&!fn){showToast('请至少输入姓名');return;}
  var vcf='BEGIN:VCARD\\nVERSION:3.0\\n';
  vcf+='N:'+ln+';'+fn+';;;\\n';
  vcf+='FN:'+fn+' '+ln+'\\n';
  if(org||title)vcf+='ORG:'+org+';\\nTITLE:'+title+'\\n';
  if(cell)vcf+='TEL;TYPE=CELL:'+cell+'\\n';
  if(work)vcf+='TEL;TYPE=WORK:'+work+'\\n';
  if(pe)vcf+='EMAIL;TYPE=HOME:'+pe+'\\n';
  if(we)vcf+='EMAIL;TYPE=WORK:'+we+'\\n';
  if(url)vcf+='URL:'+url+'\\n';
  if(bday)vcf+='BDAY:'+bday+'\\n';
  if(street||city||region||postal||country)vcf+='ADR;TYPE=HOME:;;'+street+';'+city+';'+region+';'+postal+';'+country+'\\n';
  if(note)vcf+='NOTE:'+note+'\\n';
  vcf+='END:VCARD';
  var out=document.getElementById('vcfOutput')||document.getElementById('output');
  if(out){out.textContent=vcf;out.style.display='block'}
  else{
    var div=document.createElement('div');div.style.cssText='background:#0f172a;border-radius:8px;padding:16px;margin-top:12px';
    div.innerHTML='<pre style="white-space:pre-wrap;color:#e2e8f0;font-family:monospace;font-size:.85rem">'+vcf+'</pre>';
    var btn=document.createElement('button');btn.textContent='下载VCF';btn.className='btn btn-success';btn.style.marginTop='8px';
    btn.onclick=function(){var blob=new Blob([vcf],{type:'text/vcard'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=(fn||'contact')+'.vcf';a.click()};
    var container=document.querySelector('.tool-body')||document.querySelector('.section');
    var existing=document.getElementById('vcfResult');if(existing)existing.remove();
    div.id='vcfResult';div.appendChild(btn);container.appendChild(div);
  }
  showToast('VCF预览已生成');
}"""
    content,_=replace_stub_func(content,'previewVCF',new_impl)
    return content

def fix_yaml_formatter(content):
    new_jty = """function jsonToYaml() {
  var input=document.getElementById('jsonInput')?document.getElementById('jsonInput').value:document.querySelector('textarea').value;
  if(!input.trim()){showToast('请输入JSON内容');return;}
  try{var obj=JSON.parse(input)}catch(e){showToast('JSON解析失败: '+e.message);return;}
  function toYaml(obj,indent){
    var sp=''.repeat(indent);
    if(obj===null)return 'null';
    if(typeof obj!=='object')return String(obj);
    if(Array.isArray(obj)){
      var lines=obj.map(function(v){
        if(typeof v==='object'&&v!==null)return '\\n'+sp+'- '+toYaml(v,indent+2).replace(/^\\s+/,'');
        return '\\n'+sp+'- '+String(v);
      });
      return lines.join('');
    }
    var lines=Object.keys(obj).map(function(k){
      var v=obj[k];
      if(typeof v==='object'&&v!==null)return sp+k+':\\n'+toYaml(v,indent+2);
      return sp+k+': '+String(v);
    });
    return lines.join('\\n');
  }
  var yaml=toYaml(obj,0);
  var out=document.getElementById('yamlOutput')||document.getElementById('output');
  if(out){out.value=yaml;out.textContent=yaml}
  showToast('已转换为YAML');
}"""
    content,_=replace_stub_func(content,'jsonToYaml',new_jty)
    
    new_ytj = """function yamlToJson() {
  var input=document.getElementById('yamlInput')?document.getElementById('yamlInput').value:document.querySelector('textarea').value;
  if(!input.trim()){showToast('请输入YAML内容');return;}
  var lines=input.split('\\n');
  var result={};
  var stack=[{indent:-1,obj:result}];
  lines.forEach(function(line){
    if(!line.trim()||line.trim().startsWith('#'))return;
    var indent=line.length-line.replace(/^\\s+/,'').length;
    var match=line.match(/^(\\s*)([\\w-]+):\\s*(.*)$/);
    if(!match)return;
    var key=match[2];var val=match[3].trim();
    while(stack.length>1&&stack[stack.length-1].indent>=indent){stack.pop()}
    var parent=stack[stack.length-1].obj;
    if(val){
      if(val==='true')parent[key]=true;
      else if(val==='false')parent[key]=false;
      else if(val==='null')parent[key]=null;
      else if(!isNaN(val))parent[key]=Number(val);
      else parent[key]=val.replace(/^["']|["']$/g,'');
    }else{parent[key]={};stack.push({indent:indent,obj:parent[key]})}
  });
  var json=JSON.stringify(result,null,2);
  var out=document.getElementById('jsonOutput')||document.getElementById('output');
  if(out){out.value=json;out.textContent=json}
  showToast('已转换为JSON');
}"""
    content,_=replace_stub_func(content,'yamlToJson',new_ytj)
    return content

# Process
fixes = {
    'yaml-diff/index.html': fix_yaml_diff,
    'yaml-path-finder/index.html': fix_yaml_path_finder,
    'vcf-generator/index.html': fix_vcf_generator,
    'yaml-formatter/index.html': fix_yaml_formatter,
}

fixed = 0
for rel, fixer in fixes.items():
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f"SKIP: {rel}")
        continue
    content = read_file(path)
    new_content = fixer(content)
    if new_content != content:
        write_file(path, new_content)
        fixed += 1
        print(f"FIXED: {rel}")
    else:
        print(f"NO CHANGE: {rel}")

print(f"\nTotal: {fixed}")
