// Ad-hoc verification: IPv6 subnet calculator core logic

function ipv6ToFull(addr) {
  addr = addr.trim();
  if (addr.includes('::')) {
    var parts = addr.split('::');
    var left = parts[0] ? parts[0].split(':').filter(function(p){return p!==''}) : [];
    var right = parts[1] ? parts[1].split(':').filter(function(p){return p!==''}) : [];
    var missing = 8 - left.length - right.length;
    var middle = [];
    for (var i = 0; i < missing; i++) { middle.push('0'); }
    var allParts = left.concat(middle).concat(right);
  } else {
    var allParts = addr.split(':');
  }
  if (allParts.length !== 8) { return null; }
  for (var i = 0; i < 8; i++) {
    allParts[i] = allParts[i].padStart(4, '0');
  }
  return allParts.join(':').toLowerCase();
}

function ipv6ToBigInt(addr) {
  var full = ipv6ToFull(addr);
  if (!full) return null;
  return BigInt('0x' + full.replace(/:/g, ''));
}

function bigIntToIPv6Full(num) {
  var hex = num.toString(16).padStart(32, '0');
  var parts = [];
  for (var i = 0; i < 8; i++) {
    parts.push(hex.substring(i*4, i*4+4));
  }
  return parts.join(':');
}

function ipv6ToCompressed(addr) {
  var full = ipv6ToFull(addr);
  if (!full) return null;
  var parts = full.split(':').map(function(p){ return p.replace(/^0+/, '') || '0'; });
  var bestStart = -1, bestLen = 0;
  var curStart = -1, curLen = 0;
  for (var i = 0; i < 8; i++) {
    if (parts[i] === '0') {
      if (curStart === -1) { curStart = i; curLen = 1; }
      else { curLen++; }
    } else {
      if (curLen > bestLen) { bestStart = curStart; bestLen = curLen; }
      curStart = -1; curLen = 0;
    }
  }
  if (curLen > bestLen) { bestStart = curStart; bestLen = curLen; }
  if (bestLen < 2) { return parts.join(':'); }
  var result = [];
  for (var i = 0; i < 8; i++) {
    if (i === bestStart) {
      if (bestStart === 0) { result.push(''); }
      result.push('');
      i += bestLen - 1;
    } else {
      result.push(parts[i]);
    }
  }
  if (bestStart + bestLen === 8 && result[result.length-1] !== '') { result.push(''); }
  return result.join(':').replace(/:{3,}/g, '::');
}

var pass = 0, fail = 0;
function check(name, cond) {
  if (cond) { pass++; }
  else { console.log('FAIL: ' + name); fail++; }
}

// 1. Address parsing
check('parse 2001:db8::1', ipv6ToFull('2001:db8::1') === '2001:0db8:0000:0000:0000:0000:0000:0001');
check('parse ::1', ipv6ToFull('::1') === '0000:0000:0000:0000:0000:0000:0000:0001');
check('parse fe80::1', ipv6ToFull('fe80::1') === 'fe80:0000:0000:0000:0000:0000:0000:0001');
check('parse already full', ipv6ToFull('2001:0db8:0000:0000:0000:0000:0000:0001') === '2001:0db8:0000:0000:0000:0000:0000:0001');
check('invalid returns null', ipv6ToFull('not::an::address') === null);

// 2. Compression
check('compress 2001:db8::1', ipv6ToCompressed('2001:0db8:0000:0000:0000:0000:0000:0001') === '2001:db8::1');
check('compress ::1', ipv6ToCompressed('0000:0000:0000:0000:0000:0000:0000:0001') === '::1');
check('compress fe80::1', ipv6ToCompressed('fe80:0000:0000:0000:0000:0000:0000:0001') === 'fe80::1');
check('compress all zeros', ipv6ToCompressed('0000:0000:0000:0000:0000:0000:0000:0000') === '::');

// 3. Subnet calc: 2001:db8::/32
var ipBig = ipv6ToBigInt('2001:db8::');
var prefix = 32;
var mask = (BigInt(1) << BigInt(128 - prefix)) - BigInt(1);
var netBig = ipBig & (~mask);
check('network /32 compress', ipv6ToCompressed(bigIntToIPv6Full(netBig)) === '2001:db8::');
var firstBig = netBig + BigInt(1);
check('first addr /32', ipv6ToCompressed(bigIntToIPv6Full(firstBig)) === '2001:db8::1');

// 4. Subnet calc: 2001:db8::/64
prefix = 64;
mask = (BigInt(1) << BigInt(128 - prefix)) - BigInt(1);
netBig = ipBig & (~mask);
check('network /64 compress', ipv6ToCompressed(bigIntToIPv6Full(netBig)) === '2001:db8::');
var broadcastBig = netBig | mask;
check('broadcast /64', ipv6ToCompressed(bigIntToIPv6Full(broadcastBig)) === '2001:db8::ffff:ffff:ffff:ffff');
var lastBig = broadcastBig - BigInt(1);
check('last addr /64', ipv6ToCompressed(bigIntToIPv6Full(lastBig)) === '2001:db8::ffff:ffff:ffff:fffe');

// 5. Total usable
var totalBig = (BigInt(2) << BigInt(127 - prefix)) - BigInt(2);
check('total /64 = 2^64-2', totalBig === (BigInt(1) << BigInt(64)) - BigInt(2));

// 6. /64 subnet count
var num64 = (BigInt(1) << BigInt(64 - prefix));
check('num64 for /64 = 1', num64 === BigInt(1));
num64 = (BigInt(1) << BigInt(64 - 48));
check('num64 for /48 = 65536', num64 === BigInt(65536));

// 7. Edge cases
var m128 = (BigInt(1) << BigInt(128 - 128)) - BigInt(1);
check('/128 mask is zero', m128 === BigInt(0));
var m0 = (BigInt(1) << BigInt(128 - 0)) - BigInt(1);
check('/0 mask is huge', m0 > BigInt(0));
check('/127 usable=2', (BigInt(2) << BigInt(127 - 127)) - BigInt(2) === BigInt(2));

console.log('=== Results: ' + pass + ' passed, ' + fail + ' failed ===');
if (fail > 0) process.exit(1);