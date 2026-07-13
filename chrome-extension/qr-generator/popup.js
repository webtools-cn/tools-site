/* ===================================================================
 * 二维码生成器 - Chrome 扩展 popup 逻辑
 * 复用工具站 free-toolbase.com/qr-generator/ 核心算法
 * 纯前端，零依赖，数据完全本地处理
 * =================================================================== */
(function() {
'use strict';

/* ========== QR Code Generator Core (Pure JavaScript, Zero Dependencies) ========== */
const QRMode = { NUMERIC: 1, ALPHANUMERIC: 2, BYTE: 4, ECI: 7, KANJI: 8, STRUCTURED_APPEND: 3, FNC1_1: 5, FNC1_2: 9 };
const QRErrorCorrectionLevel = { L: 1, M: 0, Q: 3, H: 2 };
const QRMaskPattern = { PATTERN000: 0, PATTERN001: 1, PATTERN010: 2, PATTERN011: 3, PATTERN100: 4, PATTERN101: 5, PATTERN110: 6, PATTERN111: 7 };

const QRRSBlockTable = [
  [1,26,19],[1,26,16],[1,26,13],[1,26,9],[1,44,34],[1,44,28],[1,44,22],[1,44,16],[1,70,55],[1,70,44],
  [2,35,17],[2,35,13],[1,100,80],[2,50,32],[2,50,24],[4,25,9],[1,134,108],[2,67,43],[2,33,15,2,34,16],
  [2,33,11,2,34,12],[2,86,68],[4,43,27],[4,43,19],[4,43,15],[2,98,78],[4,49,31],[2,32,14,4,33,15],
  [4,39,13,1,40,14],[2,121,97],[2,60,38,2,61,39],[4,40,18,2,41,19],[4,40,14,2,41,15],[2,146,116],
  [3,58,36,2,59,37],[4,36,16,4,37,17],[4,36,12,4,37,13],[2,86,68,2,87,69],[4,69,43,1,70,44],
  [6,43,19,2,44,20],[6,43,15,2,44,16],[4,101,81],[1,80,50,4,81,51],[4,50,22,4,51,23],[3,36,12,8,37,13],
  [2,116,92,2,117,93],[6,58,36,2,59,37],[4,46,20,6,47,21],[7,42,14,4,43,15],[4,133,107],[8,59,37,1,60,38],
  [8,44,20,4,45,21],[12,33,11,4,34,12],[3,145,115,1,146,116],[4,64,40,5,65,41],[11,36,16,5,37,17],
  [11,36,12,5,37,13],[5,109,87,1,110,88],[5,65,41,5,66,42],[5,54,24,7,55,25],[11,36,12,7,37,13],
  [5,122,98,1,123,99],[7,73,45,3,74,46],[15,43,19,2,44,20],[3,45,15,13,46,16],[1,135,107,5,136,108],
  [10,74,46,1,75,47],[1,50,22,15,51,23],[2,42,14,17,43,15],[5,150,120,1,151,121],[9,69,43,4,70,44],
  [17,50,24,1,51,25],[2,42,14,19,43,15],[3,141,113,4,142,114],[3,70,44,11,71,45],[17,47,21,4,48,22],
  [9,39,13,16,40,14],[3,135,107,5,136,108],[3,67,41,13,68,42],[15,54,24,5,55,25],[15,43,15,10,44,16],
  [4,144,116,4,145,117],[17,68,42],[17,50,24,6,51,25],[19,46,16,6,47,17],[2,139,111,7,140,112],
  [17,74,46],[7,54,24,16,55,25],[34,37,13],[4,151,121,5,152,122],[4,75,47,14,76,48],[11,54,24,14,55,25],
  [16,45,15,14,46,16],[6,147,117,4,148,118],[6,73,45,14,74,46],[11,54,24,16,55,25],[30,46,16,2,47,17],
  [8,132,106,4,133,107],[8,75,47,13,76,48],[7,54,24,22,55,25],[22,45,15,13,46,16],[10,142,114,2,143,115],
  [19,74,46,4,75,47],[28,50,24,6,51,25],[33,46,16,4,47,17],[8,152,122,4,153,123],[22,73,45,3,74,46],
  [8,53,23,26,54,24],[12,45,15,28,46,16],[3,147,117,10,148,118],[3,73,45,23,74,46],[4,54,24,31,55,25],
  [11,45,15,31,46,16],[7,146,116,7,147,117],[21,73,45,7,74,46],[1,53,23,37,54,24],[19,45,15,26,46,16],
  [5,145,115,10,146,116],[19,75,47,10,76,48],[15,54,24,25,55,25],[23,45,15,25,46,16],[13,145,115,3,146,116],
  [2,74,46,29,75,47],[42,54,24,1,55,25],[23,45,15,28,46,16],[17,145,115],[10,74,46,23,75,47],
  [10,54,24,35,55,25],[19,45,15,35,46,16],[17,145,115,1,146,116],[14,74,46,21,75,47],[29,54,24,19,55,25],
  [11,45,15,46,46,16],[13,145,115,6,146,116],[14,74,46,23,75,47],[44,54,24,7,55,25],[59,46,16,1,47,17],
  [12,151,121,7,152,122],[12,75,47,26,76,48],[39,54,24,14,55,25],[22,45,15,41,46,16],[6,151,121,14,152,122],
  [6,75,47,34,76,48],[46,54,24,10,55,25],[2,45,15,64,46,16],[17,152,122,4,153,123],[29,74,46,14,75,47],
  [49,54,24,10,55,25],[24,45,15,46,46,16],[4,152,122,18,153,123],[13,74,46,32,75,47],[48,54,24,14,55,25],
  [42,45,15,32,46,16],[20,147,117,4,148,118],[40,75,47,7,76,48],[43,54,24,22,55,25],[10,45,15,67,46,16],
  [19,148,118,6,149,119],[18,75,47,31,76,48],[34,54,24,34,55,25],[20,45,15,61,46,16]
];

function getRSBlocks(typeNumber, errorCorrectionLevel) {
  const rsBlock = Array.isArray(QRRSBlockTable[(typeNumber - 1) * 4 + errorCorrectionLevel])
    ? QRRSBlockTable[(typeNumber - 1) * 4 + errorCorrectionLevel]
    : [QRRSBlockTable[(typeNumber - 1) * 4 + errorCorrectionLevel]];
  const length = rsBlock.length / 3;
  const list = [];
  for (let i = 0; i < length; i++) {
    const count = rsBlock[i * 3 + 0];
    const totalCount = rsBlock[i * 3 + 1];
    const dataCount = rsBlock[i * 3 + 2];
    for (let j = 0; j < count; j++) list.push({ totalCount, dataCount });
  }
  return list;
}

const QRCodeCapacityTable = [
  { ver: 1, L: 152, M: 128, Q: 104, H: 72 },
  { ver: 2, L: 272, M: 224, Q: 176, H: 128 },
  { ver: 3, L: 440, M: 352, Q: 272, H: 208 },
  { ver: 4, L: 640, M: 512, Q: 384, H: 288 },
  { ver: 5, L: 864, M: 688, Q: 496, H: 368 },
  { ver: 6, L: 1088, M: 864, Q: 608, H: 480 },
  { ver: 7, L: 1248, M: 992, Q: 704, H: 528 },
  { ver: 8, L: 1552, M: 1232, Q: 880, H: 688 },
  { ver: 9, L: 1856, M: 1456, Q: 1056, H: 800 },
  { ver: 10, L: 2192, M: 1728, Q: 1232, H: 976 },
  { ver: 11, L: 2592, M: 2032, Q: 1440, H: 1120 },
  { ver: 12, L: 2960, M: 2320, Q: 1648, H: 1264 },
  { ver: 13, L: 3424, M: 2672, Q: 1952, H: 1440 },
  { ver: 14, L: 3688, M: 2920, Q: 2088, H: 1576 },
  { ver: 15, L: 4184, M: 3320, Q: 2360, H: 1784 },
  { ver: 16, L: 4712, M: 3624, Q: 2600, H: 2024 },
  { ver: 17, L: 5176, M: 4056, Q: 2936, H: 2264 },
  { ver: 18, L: 5768, M: 4504, Q: 3176, H: 2504 },
  { ver: 19, L: 6360, M: 5016, Q: 3560, H: 2728 },
  { ver: 20, L: 6888, M: 5352, Q: 3880, H: 3080 },
  { ver: 21, L: 7456, M: 5712, Q: 4096, H: 3248 },
  { ver: 22, L: 8048, M: 6256, Q: 4544, H: 3536 },
  { ver: 23, L: 8752, M: 6880, Q: 4912, H: 3712 },
  { ver: 24, L: 9392, M: 7312, Q: 5312, H: 4112 },
  { ver: 25, L: 10208, M: 7936, Q: 5744, H: 4304 },
  { ver: 26, L: 10960, M: 8464, Q: 6032, H: 4768 },
  { ver: 27, L: 11744, M: 8992, Q: 6464, H: 5024 },
  { ver: 28, L: 12248, M: 9544, Q: 6968, H: 5288 },
  { ver: 29, L: 13048, M: 10136, Q: 7288, H: 5608 },
  { ver: 30, L: 13880, M: 10984, Q: 7880, H: 5960 },
  { ver: 31, L: 14744, M: 11640, Q: 8264, H: 6344 },
  { ver: 32, L: 15640, M: 12328, Q: 8920, H: 6760 },
  { ver: 33, L: 16568, M: 13048, Q: 9368, H: 7208 },
  { ver: 34, L: 17528, M: 13800, Q: 9848, H: 7688 },
  { ver: 35, L: 18448, M: 14496, Q: 10288, H: 7888 },
  { ver: 36, L: 19472, M: 15312, Q: 10832, H: 8432 },
  { ver: 37, L: 20528, M: 15936, Q: 11408, H: 8768 },
  { ver: 38, L: 21616, M: 16816, Q: 12016, H: 9136 },
  { ver: 39, L: 22496, M: 17728, Q: 12656, H: 9776 },
  { ver: 40, L: 23648, M: 18672, Q: 13328, H: 10208 }
];

function getMinVersion(byteLength, errorCorrectionLevel) {
  const names = ['M', 'L', 'H', 'Q'];
  const name = names[errorCorrectionLevel] || 'M';
  for (const c of QRCodeCapacityTable) {
    if (c[name] >= byteLength + 3) return c.ver;
  }
  return 40;
}

const QRAlignmentPatternTable = [
  [], [6,18], [6,22], [6,26], [6,30], [6,34], [6,22,38], [6,24,42], [6,26,46], [6,28,50],
  [6,30,54], [6,32,58], [6,34,62], [6,26,46,66], [6,26,48,70], [6,26,50,74], [6,30,54,78],
  [6,30,56,82], [6,30,58,86], [6,34,62,90], [6,28,50,72,94], [6,26,50,74,98],
  [6,30,54,78,102], [6,28,54,80,106], [6,32,58,84,110], [6,30,58,86,114],
  [6,34,62,90,118], [6,26,50,74,98,122], [6,30,54,78,102,126],
  [6,26,52,78,104,130], [6,30,56,82,108,134], [6,34,60,86,112,138],
  [6,30,58,86,114,142], [6,34,62,90,118,146], [6,30,54,78,102,126,150],
  [6,24,50,76,102,128,154], [6,28,54,80,106,132,158], [6,32,58,84,110,136,162],
  [6,26,54,82,110,138,166], [6,30,58,86,114,142,170]
];

/* Galois Field GF(256) */
const GF = {};
(function() {
  const exp = [], log = [];
  let x = 1;
  for (let i = 0; i < 255; i++) { exp[i] = x; log[x] = i; x <<= 1; if (x & 0x100) x ^= 0x11d; }
  for (let i = 255; i < 512; i++) exp[i] = exp[i - 255];
  GF.exp = exp; GF.log = log;
})();

function gfMul(a, b) { if (a === 0 || b === 0) return 0; return GF.exp[(GF.log[a] + GF.log[b]) % 255]; }
function gfDiv(a, b) { if (b === 0) throw new Error('div by zero'); if (a === 0) return 0; return GF.exp[(GF.log[a] - GF.log[b] + 255) % 255]; }

function polyMul(a, b) {
  const result = new Array(a.length + b.length - 1).fill(0);
  for (let i = 0; i < a.length; i++) for (let j = 0; j < b.length; j++) result[i + j] ^= gfMul(a[i], b[j]);
  return result;
}

function polyRemainder(data, gen) {
  let rem = data.slice();
  for (let i = 0; i < data.length - gen.length + 1; i++) {
    const coef = rem[i];
    if (coef !== 0) for (let j = 1; j < gen.length; j++) rem[i + j] ^= gfMul(gen[j], coef);
  }
  return rem.slice(data.length - gen.length + 1);
}

function rsGeneratorPoly(degree) {
  let g = [1];
  for (let i = 0; i < degree; i++) g = polyMul(g, [1, GF.exp[i]]);
  return g;
}

function rsEncode(data, ecCount) {
  const gen = rsGeneratorPoly(ecCount);
  const rem = polyRemainder(data.concat(new Array(ecCount).fill(0)), gen);
  return data.concat(rem);
}

function encodeQR(text, errorCorrectionLevel) {
  const data = new TextEncoder().encode(text);
  const byteModeIndicator = [0, 1, 0, 0];
  const levelName = ['M', 'L', 'H', 'Q'][errorCorrectionLevel];
  const version = getMinVersion(data.length, errorCorrectionLevel);
  const size = version * 4 + 17;
  const modeBitLength = version < 10 ? 8 : 16;
  const capacity = QRCodeCapacityTable[version - 1][levelName];
  const totalBits = capacity * 8;

  let bits = [];
  bits = bits.concat(byteModeIndicator);
  for (let i = modeBitLength - 1; i >= 0; i--) bits.push((data.length >> i) & 1);
  for (const b of data) for (let i = 7; i >= 0; i--) bits.push((b >> i) & 1);

  // terminator
  const terminatorLen = Math.min(4, totalBits - bits.length);
  for (let i = 0; i < terminatorLen; i++) bits.push(0);
  // pad to byte boundary
  while (bits.length % 8 !== 0) bits.push(0);
  // pad bytes
  const padBytes = [0b11101100, 0b00010001];
  let padIdx = 0;
  while (bits.length < totalBits) { for (let i = 7; i >= 0; i--) bits.push((padBytes[padIdx % 2] >> i) & 1); padIdx++; }

  // to bytes
  const bytes = [];
  for (let i = 0; i < bits.length; i += 8) { let b = 0; for (let j = 0; j < 8; j++) b = (b << 1) | bits[i + j]; bytes.push(b); }

  const rsBlocks = getRSBlocks(version, errorCorrectionLevel);
  let totalDataCount = 0;
  for (const b of rsBlocks) totalDataCount += b.dataCount;
  if (bytes.length < totalDataCount) while (bytes.length < totalDataCount) { bytes.push(0b11101100); bytes.push(0b00010001); }

  // distribute to blocks
  const dataBlocks = [], ecBlocks = [];
  let byteIdx = 0;
  for (const block of rsBlocks) {
    const db = bytes.slice(byteIdx, byteIdx + block.dataCount);
    dataBlocks.push(db);
    ecBlocks.push(rsEncode(db, block.totalCount - block.dataCount));
    byteIdx += block.dataCount;
  }

  // interleave
  const finalData = [], finalEC = [];
  let maxDc = 0; for (const b of dataBlocks) maxDc = Math.max(maxDc, b.length);
  for (let i = 0; i < maxDc; i++) for (const b of dataBlocks) if (i < b.length) finalData.push(b[i]);
  let maxEc = 0; for (const b of ecBlocks) maxEc = Math.max(maxEc, b.length);
  for (let i = 0; i < maxEc; i++) for (const b of ecBlocks) if (i < b.length) finalEC.push(b[i]);

  const finalMessage = finalData.concat(finalEC);

  // create matrix
  const moduleCount = size;
  const modules = [];
  for (let r = 0; r < moduleCount; r++) { modules[r] = []; for (let c = 0; c < moduleCount; c++) modules[r][c] = null; }

  function setModule(row, col, isDark) { modules[row][col] = isDark; }

  // finder patterns
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      if ((r < 7 && c < 7) || (r < 7 && c >= moduleCount - 7) || (r >= moduleCount - 7 && c < 7)) {
        const dark = (r === 0 || r === 6 || c === 0 || c === 6) || ((r >= 2 && r <= 4 && c >= 2 && c <= 4));
        if (r < 7 && c < 7) setModule(r, c, dark);
        else if (r < 7 && c >= moduleCount - 7) setModule(r, c, dark);
        else if (r >= moduleCount - 7 && c < 7) setModule(r, c, dark);
      }
    }
  }
  // separators
  for (let i = 0; i < 8; i++) {
    if (i < 7) { setModule(7, i, false); setModule(i, 7, false); }
    if (moduleCount - 8 + i < moduleCount) { setModule(7, moduleCount - 8 + i, false); setModule(moduleCount - 8 + i, 7, false); }
    if (moduleCount - 8 + i < moduleCount) { setModule(moduleCount - 8 + i, 7, false); }
    if (i < 7) { setModule(moduleCount - 8, 7, false); setModule(7, moduleCount - 8, false); }
    setModule(7, 7, false);
  }
  // timing patterns
  for (let i = 8; i < moduleCount - 8; i++) { setModule(6, i, i % 2 === 0); setModule(i, 6, i % 2 === 0); }
  // dark module
  setModule(4 * version + 9, 8, true);
  // alignment patterns
  const alignPos = QRAlignmentPatternTable[version - 1] || [];
  for (let i = 0; i < alignPos.length; i++) {
    for (let j = 0; j < alignPos.length; j++) {
      if ((i === 0 && j === 0) || (i === 0 && j === alignPos.length - 1) || (i === alignPos.length - 1 && j === 0)) continue;
      const r = alignPos[i], c = alignPos[j];
      for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) {
        const dark = (Math.abs(dy) === 2 || Math.abs(dx) === 2 || (dy === 0 && dx === 0));
        setModule(r + dy, c + dx, dark);
      }
    }
  }
  // reserve format info
  for (let i = 0; i < 9; i++) { if (modules[8][i] === null) setModule(8, i, 0); if (modules[i][8] === null) setModule(i, 8, 0); }
  for (let i = moduleCount - 8; i < moduleCount; i++) { if (modules[8][i] === null) setModule(8, i, 0); if (modules[i][8] === null) setModule(i, 8, 0); }
  // reserve version info
  if (version >= 7) {
    for (let i = 0; i < 6; i++) for (let j = 0; j < 3; j++) { setModule(i, moduleCount - 11 + j, 0); setModule(moduleCount - 11 + j, i, 0); }
  }

  // place data
  let bitIdx = 0;
  let direction = -1;
  let col = moduleCount - 1;
  let row = moduleCount - 1;
  while (col > 0) {
    if (col === 6) col--;
    while (true) {
      for (let c = 0; c < 2; c++) {
        const cc = col - c;
        if (modules[row][cc] === null) {
          let dark = false;
          if (bitIdx < finalMessage.length * 8) {
            dark = ((finalMessage[Math.floor(bitIdx / 8)] >> (7 - bitIdx % 8)) & 1) === 1;
          }
          setModule(row, cc, dark);
          bitIdx++;
        }
      }
      row += direction;
      if (row < 0 || row >= moduleCount) { direction = -direction; row += direction; col -= 2; break; }
    }
  }

  // format info BCH
  const formatBits = [
    [0b01, 0b0100110111001110], [0b00, 0b0001111010110000], [0b11, 0b0010110100010011], [0b10, 0b0111111001101101]
  ];
  const fmt = formatBits[errorCorrectionLevel][0] << 10 | formatBits[errorCorrectionLevel][1];
  const fmtMasked = fmt ^ 0b101010000010010;
  for (let i = 0; i < 15; i++) {
    const bit = (fmtMasked >> i) & 1;
    if (i < 6) setModule(8, i, !!bit);
    else if (i < 8) setModule(8, i + 1, !!bit);
    else if (i === 8) setModule(7, 8, !!bit);
    else setModule(14 - i, 8, !!bit);
    const bit2 = (fmtMasked >> (14 - i)) & 1;
    if (i < 8) setModule(moduleCount - 1 - i, 8, !!bit2);
    else if (i < 9) setModule(8, moduleCount - 15 + i, !!bit2);
    else setModule(8, 15 - i, !!bit2);
  }

  // version info
  if (version >= 7) {
    const versionInfoBits = [
      0b000111110010010100, 0b001000010110111100, 0b001001101011011000, 0b001010010011010100,
      0b001011101111110000, 0b001100011101100000, 0b001101100001000100, 0b001110011001001000, 0b001111100101101100,
      0b010000101101111000, 0b010001010001011100, 0b010010101001010000, 0b010011010101110100, 0b010100100111100100,
      0b010101011011000000, 0b010110100011001100, 0b010111011111101000, 0b011000000010001100, 0b011001111110101000,
      0b011010000110100100, 0b011011111010000000, 0b011100001000010000, 0b011101110100110100, 0b011110001100111000,
      0b011111110000011100, 0b100000011000111100, 0b100001100100011000, 0b100010011100010100, 0b100011100000110000,
      0b100100010010100000, 0b100101101110000100, 0b100110010110001000, 0b100111101010101100, 0b101000110101111000,
      0b101001001001011100, 0b101010110001010000, 0b101011001101110100, 0b101100111111100100, 0b101101000011000000,
      0b101110111011001100, 0b101111000111101000
    ][version - 7];
    for (let i = 0; i < 18; i++) {
      const bit = (versionInfoBits >> i) & 1;
      const r = Math.floor(i / 3), c = i % 3;
      setModule(r, moduleCount - 11 + c, !!bit);
      setModule(moduleCount - 11 + c, r, !!bit);
    }
  }

  // mask evaluation and apply
  const maskFns = [
    (r, c) => (r + c) % 2 === 0, (r, c) => r % 2 === 0, (r, c) => c % 3 === 0, (r, c) => (r + c) % 3 === 0,
    (r, c) => (Math.floor(r / 2) + Math.floor(c / 3)) % 2 === 0, (r, c) => ((r * c) % 2) + ((r * c) % 3) === 0,
    (r, c) => (((r * c) % 2) + ((r * c) % 3)) % 2 === 0, (r, c) => (((r + c) % 2) + ((r * c) % 3)) % 2 === 0
  ];

  function getPenaltyScore(mods) {
    const n = mods.length; let score = 0;
    // rule 1: same color rows
    for (let r = 0; r < n; r++) {
      let count = 1;
      for (let c = 1; c < n; c++) {
        if (mods[r][c] === mods[r][c - 1]) count++; else { count = 1; }
        if (count >= 5) score += count - 5 + 3;
      }
    }
    for (let c = 0; c < n; c++) {
      let count = 1;
      for (let r = 1; r < n; r++) {
        if (mods[r][c] === mods[r - 1][c]) count++; else { count = 1; }
        if (count >= 5) score += count - 5 + 3;
      }
    }
    // rule 2: 2x2 blocks
    for (let r = 0; r < n - 1; r++) for (let c = 0; c < n - 1; c++) {
      const dark = mods[r][c];
      if (dark === mods[r][c + 1] && dark === mods[r + 1][c] && dark === mods[r + 1][c + 1]) score += 3;
    }
    // rule 3: patterns
    const patterns = [[1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0], [0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]];
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n - 10; c++) {
        let match = true;
        for (let i = 0; i < 11; i++) if (!!mods[r][c + i] !== !!patterns[0][i]) { match = false; break; }
        if (match) score += 40;
        match = true;
        for (let i = 0; i < 11; i++) if (!!mods[r][c + i] !== !!patterns[1][i]) { match = false; break; }
        if (match) score += 40;
      }
    }
    for (let c = 0; c < n; c++) {
      for (let r = 0; r < n - 10; r++) {
        let match = true;
        for (let i = 0; i < 11; i++) if (!!mods[r + i][c] !== !!patterns[0][i]) { match = false; break; }
        if (match) score += 40;
        match = true;
        for (let i = 0; i < 11; i++) if (!!mods[r + i][c] !== !!patterns[1][i]) { match = false; break; }
        if (match) score += 40;
      }
    }
    // rule 4: balance
    let darkCount = 0;
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (mods[r][c]) darkCount++;
    const pct = Math.abs(darkCount * 100 / (n * n) - 50) / 5;
    score += Math.floor(pct) * 10;
    return score;
  }

  let bestScore = Infinity, bestPattern = 0;
  for (let p = 0; p < 8; p++) {
    const test = modules.map(row => row.slice());
    for (let r = 0; r < moduleCount; r++) for (let c = 0; c < moduleCount; c++) {
      if (test[r][c] !== null && test[r][c] !== undefined) continue;
      if ((r < 9 && c < 9) || (r < 9 && c >= moduleCount - 8) || (r >= moduleCount - 8 && c < 9) || (r === 6) || (c === 6)) continue;
      if (r >= moduleCount - 11 && c < 6 && version >= 7) continue;
      if (c >= moduleCount - 11 && r < 6 && version >= 7) continue;
    }
    const score = getPenaltyScore(test);
    if (score < bestScore) { bestScore = score; bestPattern = p; }
  }

  // apply best mask
  for (let r = 0; r < moduleCount; r++) for (let c = 0; c < moduleCount; c++) {
    if (modules[r][c] === null || modules[r][c] === undefined) continue;
    if ((r < 9 && c < 9) || (r < 9 && c >= moduleCount - 8) || (r >= moduleCount - 8 && c < 9) || (r === 6) || (c === 6)) continue;
    if (version >= 7 && ((r < 6 && c >= moduleCount - 11) || (c < 6 && r >= moduleCount - 11))) continue;
    modules[r][c] = modules[r][c] !== maskFns[bestPattern](r, c);
  }

  // update format info with best mask
  const fmt2 = formatBits[errorCorrectionLevel][0] << 10 | formatBits[errorCorrectionLevel][1];
  const fmtMask2 = (fmt2 ^ 0b101010000010010) | (bestPattern << 13);
  for (let i = 0; i < 15; i++) {
    const bit = (fmtMask2 >> i) & 1;
    if (i < 6) setModule(8, i, !!bit);
    else if (i < 8) setModule(8, i + 1, !!bit);
    else if (i === 8) setModule(7, 8, !!bit);
    else setModule(14 - i, 8, !!bit);
    const bit2 = (fmtMask2 >> (14 - i)) & 1;
    if (i < 8) setModule(moduleCount - 1 - i, 8, !!bit2);
    else if (i < 9) setModule(8, moduleCount - 15 + i, !!bit2);
    else setModule(8, 15 - i, !!bit2);
  }

  return { modules, size, version };
}

/* ========== UI Logic ========== */
const els = {
  qrInput: document.getElementById('qrInput'),
  qrCanvas: document.getElementById('qrCanvas'),
  sizeSlider: document.getElementById('sizeSlider'),
  sizeValue: document.getElementById('sizeValue'),
  fgColor: document.getElementById('fgColor'),
  bgColor: document.getElementById('bgColor'),
  btnDownload: document.getElementById('btnDownload'),
  btnCopy: document.getElementById('btnCopy'),
  levelBtns: document.querySelectorAll('.level-btn'),
  fmtPng: document.getElementById('fmtPng'),
  fmtSvg: document.getElementById('fmtSvg'),
  inputCount: document.getElementById('inputCount'),
  btnPaste: document.getElementById('btnPaste'),
  btnClear: document.getElementById('btnClear'),
};

let currentLevel = 0; // M
let currentFormat = 'png';

function drawQR(text, canvas, size, fg, bg, level) {
  try {
    const qr = encodeQR(text, level);
    const moduleCount = qr.size;
    const ctx = canvas.getContext('2d');
    canvas.width = size; canvas.height = size;
    const cellSize = Math.floor(size / moduleCount);
    const offset = Math.floor((size - cellSize * moduleCount) / 2);

    // background
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, size, size);

    // modules
    ctx.fillStyle = fg;
    for (let r = 0; r < moduleCount; r++) {
      for (let c = 0; c < moduleCount; c++) {
        if (qr.modules[r][c]) {
          ctx.fillRect(offset + c * cellSize, offset + r * cellSize, cellSize, cellSize);
        }
      }
    }

    // quiet zone border
    ctx.strokeStyle = bg;
    ctx.lineWidth = offset * 2 || 2;
    ctx.strokeRect(0, 0, size, size);

    return qr;
  } catch (e) {
    console.error(e);
    const ctx = canvas.getContext('2d');
    canvas.width = size; canvas.height = size;
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, size, size);
    ctx.fillStyle = '#ef4444';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('内容过长或生成失败', size / 2, size / 2);
    return null;
  }
}

function generateSVG(text, size, fg, bg, level) {
  try {
    const qr = encodeQR(text, level);
    const moduleCount = qr.size;
    const cellSize = Math.floor(size / moduleCount);
    const offset = Math.floor((size - cellSize * moduleCount) / 2);
    let rects = '';
    for (let r = 0; r < moduleCount; r++) {
      for (let c = 0; c < moduleCount; c++) {
        if (qr.modules[r][c]) {
          rects += `<rect x="${offset + c * cellSize}" y="${offset + r * cellSize}" width="${cellSize}" height="${cellSize}"/>`;
        }
      }
    }
    return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
<rect width="${size}" height="${size}" fill="${bg}"/>` + rects + `
</svg>`;
  } catch (e) { return null; }
}

function updatePreview() {
  const text = els.qrInput.value || ' ';
  const size = parseInt(els.sizeSlider.value, 10);
  drawQR(text, els.qrCanvas, size, els.fgColor.value, els.bgColor.value, currentLevel);
}

function updateInputCount() {
  const len = els.qrInput.value.length;
  els.inputCount.textContent = len + ' 字符';
}

// event listeners
els.sizeSlider.addEventListener('input', function() {
  els.sizeValue.textContent = els.sizeSlider.value;
  updatePreview();
});
els.fgColor.addEventListener('input', updatePreview);
els.bgColor.addEventListener('input', updatePreview);
els.qrInput.addEventListener('input', function() {
  updatePreview();
  updateInputCount();
});

els.levelBtns.forEach(function(btn) {
  btn.addEventListener('click', function() {
    els.levelBtns.forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    currentLevel = parseInt(btn.dataset.level, 10);
    updatePreview();
  });
});

els.fmtPng.addEventListener('click', function() {
  currentFormat = 'png';
  els.fmtPng.classList.add('active');
  els.fmtSvg.classList.remove('active');
});
els.fmtSvg.addEventListener('click', function() {
  currentFormat = 'svg';
  els.fmtSvg.classList.add('active');
  els.fmtPng.classList.remove('active');
});

els.btnDownload.addEventListener('click', function() {
  const text = els.qrInput.value || ' ';
  const size = parseInt(els.sizeSlider.value, 10);
  if (currentFormat === 'svg') {
    const svg = generateSVG(text, size, els.fgColor.value, els.bgColor.value, currentLevel);
    if (!svg) return;
    const blob = new Blob([svg], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'qrcode.svg'; a.click(); URL.revokeObjectURL(url);
  } else {
    const canvas = els.qrCanvas;
    const a = document.createElement('a'); a.href = canvas.toDataURL('image/png'); a.download = 'qrcode.png'; a.click();
  }
});

els.btnCopy.addEventListener('click', async function() {
  try {
    const canvas = els.qrCanvas;
    canvas.toBlob(async function(blob) {
      if (!blob) { flashMessage('复制失败'); return; }
      try {
        await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
        flashMessage('✅ 已复制到剪贴板');
      } catch (e) { flashMessage('复制失败，请直接下载'); }
    }, 'image/png');
  } catch (e) { flashMessage('复制失败'); }
});

els.btnClear.addEventListener('click', function() {
  els.qrInput.value = '';
  updatePreview();
  updateInputCount();
  els.qrInput.focus();
});

els.btnPaste.addEventListener('click', async function() {
  try {
    const text = await navigator.clipboard.readText();
    if (text) {
      els.qrInput.value = text;
      updatePreview();
      updateInputCount();
    }
  } catch (e) {
    flashMessage('请用 Ctrl+V 粘贴');
  }
});

function flashMessage(msg) {
  const existing = document.querySelector('.msg-toast');
  if (existing) existing.remove();
  const div = document.createElement('div');
  div.className = 'msg-toast';
  div.style.cssText = 'position:fixed;top:40px;left:50%;transform:translateX(-50%);padding:6px 14px;border-radius:6px;font-size:11px;z-index:1000;transition:opacity .3s;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.3);color:#10b981;';
  div.textContent = msg;
  document.body.appendChild(div);
  setTimeout(function() { div.style.opacity = '0'; setTimeout(function() { div.remove(); }, 300); }, 1800);
}

// 底部链接在新标签打开
document.getElementById('siteLink').addEventListener('click', function(e) {
  const url = this.href;
  if (chrome && chrome.tabs && chrome.tabs.create) {
    e.preventDefault();
    chrome.tabs.create({ url: url });
  }
});

// 初始化
updatePreview();
updateInputCount();

})();
