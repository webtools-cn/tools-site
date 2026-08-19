
    // BTU data for common firewood
    const btuData = [
      { name: '橡木 Oak', btu: 24.0, heat: 5, desc: '硬木，燃烧久，热值高' },
      { name: '山核桃 Hickory', btu: 27.7, heat: 5, desc: '最高热值，烟熏味佳' },
      { name: '枫木 Maple', btu: 24.0, heat: 5, desc: '硬木，燃烧均匀' },
      { name: '白蜡木 Ash', btu: 24.2, heat: 5, desc: '易劈裂，低含水率' },
      { name: '桦木 Birch', btu: 20.8, heat: 4, desc: '中硬木，易点燃' },
      { name: '山毛榉 Beech', btu: 24.0, heat: 5, desc: '硬木，燃烧稳定' },
      { name: '樱桃木 Cherry', btu: 20.0, heat: 4, desc: '果木，香味宜人' },
      { name: '松木 Pine', btu: 15.0, heat: 2, desc: '软木，易燃但快烧完' },
      { name: '云杉 Spruce', btu: 14.5, heat: 2, desc: '软木，适合引火' },
      { name: '铁杉 Hemlock', btu: 18.5, heat: 3, desc: '中软木，易劈裂' },
      { name: '杨木 Poplar', btu: 14.5, heat: 2, desc: '软木，热值较低' },
      { name: '胡桃木 Walnut', btu: 22.2, heat: 4, desc: '硬木，燃烧稳定' }
    ];

    function switchTab(tab) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
      event.target.classList.add('active');
      document.getElementById('tab-' + tab).style.display = 'block';
      if (tab === 'btu') renderBTUTable();
    }

    function updateShape() {
      const shape = document.getElementById('shape').value;
      if (shape === 'cylinder') {
        document.getElementById('depth-group').style.display = 'none';
        document.getElementById('diameter-group').style.display = 'block';
      } else {
        document.getElementById('depth-group').style.display = 'block';
        document.getElementById('diameter-group').style.display = 'none';
      }
    }

    function calcVolume() {
      const shape = document.getElementById('shape').value;
      const length = parseFloat(document.getElementById('length').value) || 0;
      const height = parseFloat(document.getElementById('height').value) || 0;
      const packing = parseFloat(document.getElementById('packing').value);
      const price = parseFloat(document.getElementById('price').value) || 0;

      let cubicFt;
      if (shape === 'cylinder') {
        const diameter = parseFloat(document.getElementById('diameter').value) || 0;
        const radius = diameter / 2;
        cubicFt = Math.PI * radius * radius * length;
      } else {
        const depth = parseFloat(document.getElementById('depth').value) || 0;
        cubicFt = length * height * depth;
      }

      if (cubicFt <= 0) {
        showToast('请输入有效尺寸');
        return;
      }

      // Adjust for packing efficiency
      const solidCubicFt = cubicFt * packing;
      const cords = solidCubicFt / 128;
      const faceCords = solidCubicFt / 42.7;
      const cubicMeters = solidCubicFt * 0.0283168;
      const totalCost = cords * price;

      document.getElementById('volume-grid').innerHTML = `
        <div class="result-item">
          <div class="label">Cord数</div>
          <div class="value">${cords.toFixed(3)}<span class="unit"> cord</span></div>
        </div>
        <div class="result-item">
          <div class="label">Face Cord</div>
          <div class="value">${faceCords.toFixed(2)}<span class="unit"> face cord</span></div>
        </div>
        <div class="result-item">
          <div class="label">立方英尺</div>
          <div class="value">${solidCubicFt.toFixed(1)}<span class="unit"> ft³</span></div>
        </div>
        <div class="result-item">
          <div class="label">立方米</div>
          <div class="value">${cubicMeters.toFixed(2)}<span class="unit"> m³</span></div>
        </div>
        <div class="result-item">
          <div class="label">估算成本</div>
          <div class="value">$${totalCost.toFixed(2)}</div>
        </div>
      `;

      let info = '';
      if (cords < 0.5) {
        info = '💡 这个量适合偶尔使用或试烧。建议先少量购买，确认木柴质量后再大批购入。';
      } else if (cords < 2) {
        info = '💡 这个量适合辅助取暖或一个温和地区的冬季。';
      } else if (cords < 4) {
        info = '💡 这个量可以满足寒冷地区一个冬季的主要取暖需求。';
      } else {
        info = '💡 这个量足够严寒地区整个冬季的主要取暖。确保有干燥通风的存储空间。';
      }
      document.getElementById('volume-info').textContent = info;
      document.getElementById('volume-result').classList.add('show');
    }

    function calcNeed() {
      const method = document.getElementById('heat-method').value;
      const climate = document.getElementById('climate').value;
      const insulation = document.getElementById('insulation').value;
      const houseSize = parseFloat(document.getElementById('house-size').value) || 1500;

      // Base cords per 1000 sqft per winter
      const baseCords = {
        'very-cold': { primary: 5.0, supplement: 2.0, occasional: 0.5 },
        'cold': { primary: 3.5, supplement: 1.5, occasional: 0.4 },
        'moderate': { primary: 2.0, supplement: 1.0, occasional: 0.3 },
        'mild': { primary: 1.0, supplement: 0.5, occasional: 0.2 }
      };

      const insulationFactor = { good: 0.8, average: 1.0, poor: 1.3 };
      const sizeFactor = houseSize / 1000;

      let cords = baseCords[climate][method] * insulationFactor[insulation] * sizeFactor;
      cords = Math.round(cords * 10) / 10;

      const faceCords = Math.round((cords * 3) * 10) / 10;
      const cubicFt = Math.round(cords * 128);
      const estCost = cords * 300;

      document.getElementById('need-grid').innerHTML = `
        <div class="result-item">
          <div class="label">建议购买</div>
          <div class="value">${cords}<span class="unit"> cord</span></div>
        </div>
        <div class="result-item">
          <div class="label">约等于</div>
          <div class="value">${faceCords}<span class="unit"> face cord</span></div>
        </div>
        <div class="result-item">
          <div class="label">体积</div>
          <div class="value">${cubicFt}<span class="unit"> ft³</span></div>
        </div>
        <div class="result-item">
          <div class="label">预估成本</div>
          <div class="value">$${estCost.toLocaleString()}</div>
        </div>
      `;

      let info = '';
      if (method === 'primary') {
        info = '⚠️ 作为主要热源，建议多备10-15%的余量以防寒潮。硬木（如橡木、山核桃）热值更高，适合主要取暖。';
      } else if (method === 'supplement') {
        info = '💡 辅助取暖可优先选择桦木或白蜡木，易点燃且燃烧稳定，适合配合壁炉使用。';
      } else {
        info = '🎉 偶尔使用可选择果木（如樱桃木），燃烧时散发怡人香味，适合营造氛围。';
      }
      document.getElementById('need-info').textContent = info;
      document.getElementById('need-result').classList.add('show');
    }

    function renderBTUTable() {
      const tbody = document.getElementById('btu-tbody');
      tbody.innerHTML = btuData.map(w => {
        const bars = Array.from({length: 5}, (_, i) =>
          `<span class="heat-bar ${i < w.heat ? 'on' : ''}"></span>`
        ).join('');
        return `
          <tr>
            <td>${w.name}</td>
            <td>${w.btu}M</td>
            <td><span class="heat-bars">${bars}</span></td>
            <td style="color:var(--text-dim);font-size:.82rem;">${w.desc}</td>
          </tr>
        `;
      }).join('');
    }

    function resetForm() {
      document.getElementById('length').value = '8';
      document.getElementById('height').value = '4';
      document.getElementById('depth').value = '4';
      document.getElementById('diameter').value = '4';
      document.getElementById('price').value = '300';
      document.getElementById('packing').value = '0.5';
      document.getElementById('shape').value = 'rect';
      updateShape();
      document.getElementById('volume-result').classList.remove('show');
    }

    function toggleFaq(el) {
      el.classList.toggle('open');
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2500);
    }

    // Init
    renderBTUTable();
  