#!/usr/bin/env python3
"""Generate json-to-java pages (CN + EN)."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "json-to-java"

# ===== CN =====
cn_title = "JSON转Java类生成器 - 在线生成Java POJO·自动类型推断·纯前端"
cn_desc = "免费在线JSON转Java类代码生成器。一键将JSON数据转换为Java POJO类代码，支持嵌套对象、List泛型、Gson/Jackson注解。纯前端本地处理，数据不上传服务器。"
cn_kw = "JSON转Java,Java类生成,POJO生成,JSON转POJO,Gson注解,Jackson注解,在线Java工具"
cn_schema_name = "JSON转Java类生成器"
cn_schema_desc = cn_desc

cn_faqs = [
    ("JSON转Java类支持哪些类型映射？", "支持String、Integer/int、Long/long、Double/double、Boolean/boolean、BigDecimal、List<T>、Map<String,Object>等。日期格式自动识别为String或Date类型，空值字段使用Object或包装类型。"),
    ("支持Gson和Jackson注解吗？", "支持。可选择生成@SerializedName（Gson）或@JsonProperty（Jackson）注解，也可以选择不生成注解。字段名风格支持camelCase和保持原始JSON键名。"),
    ("嵌套JSON对象如何处理？", "嵌套对象自动生成独立的内部类（static inner class）或独立类文件。数组自动映射为List<T>泛型类型，元素类型根据数组内容自动推断。"),
    ("生成的Java代码可以直接编译吗？", "可以。生成的代码遵循标准Java语法，包含完整的类定义、字段声明和getter/setter方法（可选）。复制到项目中添加必要的import即可编译。"),
    ("数据安全如何保障？", "完全安全。所有JSON解析和代码生成均在浏览器本地执行，你的数据绝不会上传到任何服务器。关闭页面后数据自动清除。"),
    ("支持Lombok注解吗？", "支持。可选择添加@Data、@Getter、@Setter、@Builder等Lombok注解，减少样板代码。需要项目中引入Lombok依赖。"),
]

faq_json_cn = make_faq_json(cn_faqs)

cn_content = f"""{head_start(cn_title, cn_desc, cn_kw, f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc, f"https://free-toolbase.com/{SLUG}/", cn_schema_name, cn_schema_desc, faq_json_cn, "zh", SLUG)}

<div class="tool-section">
<h2>☕ JSON转Java类生成器 <span class="badge">零依赖·可离线</span></h2>
<p>{cn_desc}</p>
<div class="options-area">
<div class="option-row">
<label>类名: <input type="text" id="className" value="MyData" style="width:120px"></label>
<label>注解: <select id="annotation"><option value="none">无注解</option><option value="gson">Gson @SerializedName</option><option value="jackson" selected>Jackson @JsonProperty</option><option value="lombok">Lombok @Data</option></select></label>
<label>包名: <input type="text" id="packageName" value="com.example" style="width:150px"></label>
<label><input type="checkbox" id="useWrapper" checked> 包装类型</label>
<label><input type="checkbox" id="genGetterSetter" checked> Getter/Setter</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">JSON输入</label>
<textarea id="input" placeholder='{{"name":"张三","age":25,"email":"test@example.com","isVip":true}}'></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">生成的Java类</label>
<div class="result-output" id="output" style="min-height:200px">等待生成...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ 生成Java类</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制结果</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载Java</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 生成 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>JSON转Java类生成器能做什么？</h2>
<p>JSON转Java类生成器是一款免费的在线工具，帮助Java开发者快速将JSON数据转换为Java POJO类代码。无需手动编写实体类，粘贴JSON即可自动生成完整类定义，支持Gson/Jackson/Lombok注解，大幅提升开发效率。纯前端处理，数据绝不上传。</p>

<h2>核心功能</h2>
<ul>
<li><strong>智能类型推断</strong>：自动将JSON值类型映射为Java类型，字符串→String，整数→Integer，浮点数→Double，布尔→Boolean</li>
<li><strong>嵌套对象支持</strong>：嵌套JSON自动生成静态内部类，多层嵌套递归处理</li>
<li><strong>数组/List映射</strong>：JSON数组自动转换为List<T>泛型，元素类型自动推断</li>
<li><strong>注解生成</strong>：支持Gson @SerializedName、Jackson @JsonProperty、Lombok @Data注解</li>
<li><strong>Getter/Setter生成</strong>：可选生成完整的getter/setter方法，或使用Lombok简化</li>
</ul>

<h2>使用教程</h2>
<ol>
<li><strong>输入JSON数据</strong>：在左侧文本框粘贴JSON对象或数组</li>
<li><strong>配置选项</strong>：设置类名、包名、注解类型、是否使用包装类型</li>
<li><strong>点击生成</strong>：点击"生成Java类"按钮，右侧立即显示代码</li>
<li><strong>复制代码</strong>：复制生成的Java类到项目中的对应包下</li>
<li><strong>添加依赖</strong>：根据选择的注解类型，确保项目引入Gson/Jackson/Lombok依赖</li>
</ol>

<h2>应用场景</h2>
<h3>场景1：API接口对接</h3>
<p>对接第三方API时，根据返回的JSON数据快速生成Java实体类，省去手动编写的繁琐工作，配合Retrofit/OkHttp立即开始开发。</p>
<h3>场景2：JSON数据建模</h3>
<p>需要将JSON配置文件映射为Java对象时，一键生成类定义，确保字段名和类型完全匹配。</p>
<h3>场景3：数据迁移</h3>
<p>从NoSQL数据库导出JSON数据后，需要转为Java对象存入关系型数据库，本工具快速生成对应的实体类。</p>

<h2>扩展知识</h2>
<p>Java POJO（Plain Old Java Object）是最常见的Java数据载体模式。Gson和Jackson是最流行的两个JSON序列化库：Gson轻量简洁，Jackson功能强大。Lombok通过编译期注解处理，自动生成getter/setter/constructor等样板代码，显著减少代码量。使用@SerializedName或@JsonProperty注解可以在JSON键名与Java字段名不一致时进行映射。</p>
</div>

{faq_html(cn_faqs, "zh")}
{footer("zh", SLUG, "JSON转Java类生成器")}
<script>
function loadExample(){{
document.getElementById('input').value='{{\\n  "name": "张三",\\n  "age": 25,\\n  "email": "zhang@example.com",\\n  "isVip": true,\\n  "address": {{\\n    "city": "北京",\\n    "zipCode": "100000"\\n  }},\\n  "tags": ["开发", "Java"]\\n}}';
execute();
}}
function clearInput(){{document.getElementById('input').value='';document.getElementById('output').textContent='等待生成...'}}
function capitalize(s){{return s.charAt(0).toUpperCase()+s.slice(1)}}
function toCamelCase(s){{return s.replace(/_([a-z])/g,function(m,c){{return c.toUpperCase()}})}}
function javaType(val,useWrapper){{if(val===null)return useWrapper?'Object':'Object';if(typeof val==='string')return 'String';if(typeof val==='boolean')return useWrapper?'Boolean':'boolean';if(typeof val==='number'){{if(Number.isInteger(val))return useWrapper?'Integer':'int';return useWrapper?'Double':'double'}}if(Array.isArray(val)){{if(val.length>0)return 'List<'+javaType(val[0],useWrapper)+'>';return 'List<Object>'}}return 'Object'}}
function generateClass(obj,name,useWrapper,annType,pkg,genGs,indent){{indent=indent||'';var lines=[];if(pkg)lines.push('package '+pkg+';');if(annType==='jackson')lines.push('import com.fasterxml.jackson.annotation.JsonProperty;');else if(annType==='gson')lines.push('import com.google.gson.annotations.SerializedName;');if(lines.length>0&&pkg)lines.push('');var ann=annType==='lombok'?'@Data':'';if(ann)lines.push(indent+ann);lines.push(indent+'public class '+name+' {{');var innerClasses=[];for(var key in obj){{if(!obj.hasOwnProperty(key))continue;var val=obj[key];var field=toCamelCase(key);var type=javaType(val,useWrapper);if(typeof val==='object'&&val!==null&&!Array.isArray(val)){{var innerName=capitalize(field);type=innerName;innerClasses.push(generateClass(val,innerName,useWrapper,annType,null,genGs,indent+'  '));if(annType==='jackson')lines.push(indent+'  @JsonProperty("'+key+'")');else if(annType==='gson')lines.push(indent+'  @SerializedName("'+key+'")');lines.push(indent+'  private '+type+' '+field+';')}else if(Array.isArray(val)&&val.length>0&&typeof val[0]==='object'&&val[0]!==null){{var innerName=capitalize(field.replace(/s$/,''));var innerType=generateClass(innerName,innerName,useWrapper,annType,null,genGs,indent+'  ');innerClasses.push(innerType);if(annType==='jackson')lines.push(indent+'  @JsonProperty("'+key+'")');else if(annType==='gson')lines.push(indent+'  @SerializedName("'+key+'")');lines.push(indent+'  private List<'+innerName+'> '+field+' = new ArrayList<>();');}}else{{if(annType==='jackson')lines.push(indent+'  @JsonProperty("'+key+'")');else if(annType==='gson')lines.push(indent+'  @SerializedName("'+key+'")');lines.push(indent+'  private '+type+' '+field+';')}}}}if(genGs&&annType!=='lombok'){{lines.push('');for(var key in obj){{if(!obj.hasOwnProperty(key))continue;var field=toCamelCase(key);var val=obj[key];var type=javaType(val,useWrapper);if(typeof val==='object'&&val!==null&&!Array.isArray(val))type=capitalize(field);lines.push(indent+'  public '+type+' get'+capitalize(field)+'() {{ return '+field+'; }}');lines.push(indent+'  public void set'+capitalize(field)+'('+type+' '+field+') {{ this.'+field+' = '+field+'; }}');}}}}lines.push(indent+'}}');var result=lines.join('\\n');for(var i=0;i<innerClasses.length;i++){{result+='\\n\\n'+innerClasses[i]}}return result}}
function execute(){{
var raw=document.getElementById('input').value.trim();if(!raw){{showToast('请输入JSON');return}}
try{{var obj=JSON.parse(raw)}}catch(e){{showToast('JSON解析失败: '+e.message);return}}
var className=document.getElementById('className').value||'MyData';
var annType=document.getElementById('annotation').value;
var pkg=document.getElementById('packageName').value;
var useWrapper=document.getElementById('useWrapper').checked;
var genGs=document.getElementById('genGetterSetter').checked;
var code=generateClass(obj,className,useWrapper,annType,pkg,genGs,'');
document.getElementById('output').textContent=code;saveHistory('jsonToJavaHistory',raw.substring(0,100));showToast('Java类生成完成');
}}
function downloadOutput(){{var text=document.getElementById('output').textContent;if(!text||text==='等待生成...'){{showToast('请先生成代码');return}}var name=document.getElementById('className').value||'MyData';downloadText(name+'.java',text)}}
window.addEventListener('load',function(){{loadExample()}});
</script>
</body></html>"""

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_content)
print(f"Written: {SLUG}/index.html ({len(cn_content)} bytes)")
