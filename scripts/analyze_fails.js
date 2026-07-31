const fs = require('fs');
const report = JSON.parse(fs.readFileSync('quality-reports/puppeteer-L0.json', 'utf-8'));
const fails = report.failures || [];

const groups = {syntax: [], undefinedFn: [], domNull: [], other: []};
fails.forEach(f => {
  const err = f.reason || '';
  if (err.includes("missing )") || err.includes("Unexpected token") || 
      err.includes("Unexpected end") || err.includes("Illegal return") || 
      err.includes("Invalid regular")) {
    groups.syntax.push(f.tool);
  } else if (err.includes("is not defined") || err.includes("container is not defined")) {
    groups.undefinedFn.push(f.tool);
  } else if (err.includes("Cannot read properties of null") || err.includes("Cannot set property")) {
    groups.domNull.push(f.tool);
  } else {
    groups.other.push(f.tool);
  }
});

console.log("=== 语法错误 ===");
console.log(groups.syntax.length, "个:", groups.syntax.join(", "));
console.log("\n=== 函数未定义 ===");
console.log(groups.undefinedFn.length, "个:", groups.undefinedFn.join(", "));
console.log("\n=== DOM null ===");
console.log(groups.domNull.length, "个:", groups.domNull.join(", "));
console.log("\n=== 其他 ===");
console.log(groups.other.length, "个:", groups.other.join(", "));