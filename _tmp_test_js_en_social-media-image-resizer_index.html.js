
    let currentImage = null;
    let currentW = 1080, currentH = 1080;
    function selectPreset(el){
      document.querySelectorAll('.preset-btn').forEach(b=>b.classList.remove('active'));
      el.classList.add('active');
      currentW = parseInt(el.dataset.w);
      currentH = parseInt(el.dataset.h);
      document.getElementById('customW').value = currentW;
      document.getElementById('customH').value = currentH;
      resizeCanvas();
    }
    function handleFile(file){
      if(!file) return;
      const reader = new FileReader();
      reader.onload = e=>{
        const img = new Image();
        img.onload = ()=>{
          currentImage = img;
          resizeCanvas();
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
    function resizeCanvas(){
      if(!currentImage) return;
      currentW = parseInt(document.getElementById('customW').value)||1080;
      currentH = parseInt(document.getElementById('customH').value)||1080;
      const canvas = document.getElementById('canvas');
      canvas.width = currentW;
      canvas.height = currentH;
      const ctx = canvas.getContext('2d');
      const scale = Math.max(currentW/currentImage.width, currentH/currentImage.height);
      const sw = currentImage.width*scale, sh = currentImage.height*scale;
      const sx = (currentW-sw)/2, sy = (currentH-sh)/2;
      ctx.fillStyle = '#f1f5f9';
      ctx.fillRect(0,0,currentW,currentH);
      ctx.drawImage(currentImage, sx, sy, sw, sh);
      document.getElementById('dimInfo').textContent = `${currentW} × ${currentH}`;
    }
    function downloadImage(){
      const canvas = document.getElementById('canvas');
      const link = document.createElement('a');
      link.download = `resized-${currentW}x${currentH}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    }
    const uploadZone = document.getElementById('uploadZone');
    uploadZone.addEventListener('dragover',e=>{e.preventDefault();uploadZone.classList.add('dragover')});
    uploadZone.addEventListener('dragleave',()=>uploadZone.classList.remove('dragover'));
    uploadZone.addEventListener('drop',e=>{e.preventDefault();uploadZone.classList.remove('dragover');handleFile(e.dataTransfer.files[0])});
    document.getElementById('fileInput').addEventListener('change',e=>handleFile(e.target.files[0]));
    const demoCanvas = document.createElement('canvas');
    demoCanvas.width=1080;demoCanvas.height=1080;
    const dctx=demoCanvas.getContext('2d');
    dctx.fillStyle='#4F46E5';dctx.fillRect(0,0,1080,1080);
    dctx.fillStyle='#fff';dctx.font='bold 60px sans-serif';dctx.textAlign='center';
    dctx.fillText('Upload Image',540,500);
    dctx.fillText('📱',540,600);
    currentImage = demoCanvas;
    resizeCanvas();
  