// static/app.js
document.addEventListener('DOMContentLoaded', () => {
  console.log('[app] DOM ready');

  const img       = document.getElementById('stream');
  const statusEl  = document.getElementById('status');
  const conf      = document.getElementById('conf');
  const iou       = document.getElementById('iou');
  const confv     = document.getElementById('confv');
  const iouv      = document.getElementById('iouv');
  const source    = document.getElementById('source');
  const startBtn  = document.getElementById('startBtn');
  const stopBtn   = document.getElementById('stopBtn');

  const showLabels = document.getElementById('showLabels');
  const saveFrames = document.getElementById('saveFrames');
  const modelSelect= document.getElementById('modelSelect');

  // Sanity checks
  const ids = {img, statusEl, conf, iou, confv, iouv, source, startBtn, stopBtn};
  for (const [k,v] of Object.entries(ids)) {
    if (!v) console.error(`[app] Missing element: ${k}`);
  }

  let running = false;
  let refreshTimer = null;

  function updateLabelsUI() {
    if (confv && conf) confv.textContent = Number(conf.value).toFixed(2);
    if (iouv && iou)  iouv.textContent  = Number(iou.value).toFixed(2);
  }
  updateLabelsUI();

  function buildStreamURL() {
    const params = new URLSearchParams({
      conf: conf ? conf.value : '0.25',
      iou:  iou  ? iou.value  : '0.45',
      source: source ? source.value : '0',
      labels: showLabels ? String(showLabels.checked) : 'true',
      save:   saveFrames ? String(saveFrames.checked) : 'false',
      model:  modelSelect ? modelSelect.value : 'yolov8n.pt',
      t: Date.now().toString() // cache-buster
    });
    return `/video_feed?${params.toString()}`;
  }

  function setStatus(on) {
    running = on;
    if (!statusEl) return;
    statusEl.textContent = on ? 'ON' : 'OFF';
    statusEl.classList.toggle('text-emerald-300', on);
    statusEl.classList.toggle('text-rose-300', !on);
  }

  function start() {
    if (!img) return console.error('[app] <img id="stream"> missing');
    const url = buildStreamURL();
    console.log('[app] start →', url);
    img.src = url;
    setStatus(true);
  }

  function stop() {
    if (img) img.src = '';
    console.log('[app] stop');
    setStatus(false);
  }

  function softRefresh() {
    if (!running || !img) return;
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(() => {
      const url = buildStreamURL();
      console.log('[app] refresh →', url);
      img.src = url;
    }, 200);
  }

  // Bind handlers (with logs)
  if (startBtn) startBtn.addEventListener('click', start);
  if (stopBtn)  stopBtn.addEventListener('click', stop);

  if (conf) conf.addEventListener('input', () => { updateLabelsUI(); softRefresh(); });
  if (iou)  iou.addEventListener('input',  () => { updateLabelsUI(); softRefresh(); });
  if (showLabels) showLabels.addEventListener('change', softRefresh);
  if (saveFrames) saveFrames.addEventListener('change', softRefresh);
  if (modelSelect) modelSelect.addEventListener('change', () => {
    if (running) { stop(); setTimeout(start, 80); }
  });

  // If the image errors (e.g., camera busy), mark as OFF.
  if (img) img.addEventListener('error', () => { if (running) stop(); });

  console.log('[app] handlers bound');
});
