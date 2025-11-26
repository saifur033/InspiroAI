/* free_api.js — Free Mode client helpers (Safe Edition)
   Exposes: fetchProcessCaption(caption, tone), resetFreeUI()
   Safe wrapper for all handlers + timeout protection
*/

const safe = (fn) => (...args) => {
  try { return fn(...args); }
  catch(err){ console.error("Free API JS Error:", err); }
};

function $id(id){ 
  try { return document.getElementById(id); } 
  catch(err) { return null; }
}

// Reset UI: clear textarea, hide results, clear cards
function resetFreeUI(){
  safe(() => {
    const ta = $id('userCaptionFree') || $id('userCaption') || $id('captionBox');
    if(ta) ta.value = '';

    const clearToDash = (sel) => {
      const el = $id(sel);
      if(!el) return;
      if (el.tagName === 'UL') el.innerHTML = '';
      else el.textContent = '–';
    };

    clearToDash('seoScoreFree');
    clearToDash('seoGradeFree');
    const sug = $id('seoSuggestionsFree');
    if(sug) sug.innerHTML='';

    clearToDash('emotionMainFree');
    clearToDash('emotionConfidenceFree');
    clearToDash('emotionReasonFree');

    clearToDash('fakePercentFree');
    clearToDash('realPercentFree');
    clearToDash('fakeReasonFree');

    const opt = $id('optimizeBoxFree');
    if(opt) opt.classList.add('hidden');
    const ar = $id('analyzeResultsFree');
    if(ar) ar.classList.add('hidden');
  })();
}

// Fetch fresh analysis from the server — sends exact caption text with timeout
async function fetchProcessCaption(caption, tone, action){
  console.log(`[fetchProcessCaption] Starting: action=${action}, tone=${tone}, captionLen=${(caption||'').length}`);
  
  window._processCaptionInFlight = window._processCaptionInFlight || false;
  let retries = 0;
  while(window._processCaptionInFlight && retries < 10){
    console.debug(`[fetchProcessCaption] Waiting for in-flight request (retry ${retries})`);
    await new Promise(r=>setTimeout(r, 150));
    retries++;
  }
  
  window._processCaptionInFlight = true;

  if(typeof showLoader === 'function') {
    showLoader();
    console.log('[fetchProcessCaption] Loader shown');
  }
  
  const payload = { 
    caption: (caption||'').toString(), 
    tone: tone||'professional', 
    action: action||'optimize' 
  };
  
  console.log('[fetchProcessCaption] Sending payload:', payload);
  
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);
  
  try {
    const res = await fetch('/api/process_caption', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload),
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if(!res.ok){
      const txt = await res.text().catch(()=>'No error details');
      console.error(`[fetchProcessCaption] HTTP ${res.status}:`, txt);
      throw new Error(`Server error ${res.status}: ${txt}`);
    }
    
    const j = await res.json();
    console.log(`[fetchProcessCaption] Success:`, j);
    return j;
    
  } catch(err) {
    console.error('[fetchProcessCaption] Error:', err);
    if(typeof hideLoader === 'function') hideLoader();
    window._processCaptionInFlight = false;
    throw err;
  } finally {
    clearTimeout(timeoutId);
    window._processCaptionInFlight = false;
    if(typeof hideLoader === 'function') {
      hideLoader();
      console.log('[fetchProcessCaption] Loader hidden');
    }
  }
}

// Real-time SEO calculation as user types
function calculateSEOLive(caption){
  safe(() => {
    if(!caption || !caption.trim()){
      const scoreEl = $id('seoScoreFree');
      const gradeEl = $id('seoGradeFree');
      if(scoreEl) scoreEl.textContent = '–';
      if(gradeEl) gradeEl.textContent = '–';
      return;
    }
    
    let score = 0;
    
    const length = caption.length;
    const words = caption.match(/[\w\u0980-\u09FF]+/g) || [];
    if(length >= 120 && length <= 250) score += 25;
    else if(length >= 90 && length < 120) score += 18;
    else if(length > 250) score += 10;
    else if(length >= 30) score += 6;
    
    const emojis = caption.match(/[\U0001F300-\U0001FAFF\u2764\uFE0F✨🌟💫🌸🔥☺️❤️😍🤩😇🌿🎉]/g) || [];
    if(emojis.length >= 3) score += 15;
    else if(emojis.length >= 1) score += 10;
    
    const tags = caption.match(/#\w+/g) || [];
    if(tags.length >= 3 && tags.length <= 6) score += 18;
    else if(tags.length > 6) score += 10;
    else if(tags.length >= 1) score += 6;
    
    const cta = /follow|share|comment|learn|watch|check|join|explore|subscribe|click|ফলো|শেয়ার|কমেন্ট|দেখুন/i;
    if(cta.test(caption)) score += 12;
    
    const powerWords = /amazing|new|offer|sale|update|exclusive|today|viral|trending|launch|limited|best|premium|gift|bonus|breaking|latest/i;
    let powerCount = (caption.match(/amazing|new|offer|sale|update|exclusive|today|viral|trending|launch|limited|best|premium|gift|bonus|breaking|latest/gi) || []).length;
    score += Math.min(12, powerCount * 6);
    
    const sentences = caption.split(/[.!?]+/).filter(s=>s.trim());
    if(sentences.length > 0){
      const avgWords = words.length / sentences.length;
      if(avgWords <= 20) score += 8;
    }
    
    score = Math.min(100, Math.max(5, score));
    
    const grade = score >= 95 ? 'A+' : score >= 85 ? 'A' : score >= 75 ? 'B' : score >= 60 ? 'C' : score >= 40 ? 'D' : 'F';
    
    const seoEl = $id('seoScoreFree');
    const gradeEl = $id('seoGradeFree');
    if(seoEl) seoEl.textContent = score;
    if(gradeEl) gradeEl.textContent = grade;
  })();
}

// Bind handlers with safe wrapper
function initFreeAPIBindings(){
  safe(() => {
    const ta = $id('userCaptionFree') || $id('userCaption') || $id('captionBox');
    if(ta){
      ta.addEventListener('input', safe(() => {
        calculateSEOLive(ta.value);
      }));
    }
  })();
  
  safe(() => {
    const clearBtn = $id('clearCaptionFree') || $id('clearCaption');
    if(clearBtn){
      clearBtn.addEventListener('click', safe((e) => {
        e.preventDefault();
        resetFreeUI();
      }));
    }
  })();

  safe(() => {
    const analyzeBtn = $id('analyzeCaptionFree') || $id('analyzeBtn');
    if(analyzeBtn){
      analyzeBtn.addEventListener('click', safe(async () => {
        const ta = $id('userCaptionFree') || $id('userCaption') || $id('captionBox');
        if(!ta || !ta.value.trim()) {
          alert('Please enter a caption to analyze.');
          return;
        }
        const tone = ($id('toneSelectFree') || $id('toneSelect'))?.value || 'professional';

        const originalText = analyzeBtn.textContent;
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing…';
        
        try{
          const data = await fetchProcessCaption(ta.value, tone, 'analyze');
          console.log('[analyze] Response:', data);
          if(window.populateAnalyze) await window.populateAnalyze(data);
        }catch(err){
          console.error('[analyze] Error:', err);
          alert('Analysis failed: '+err.message);
        }
        finally{
          analyzeBtn.disabled = false;
          analyzeBtn.textContent = originalText;
        }
      }));
    }
  })();

  safe(() => {
    const optimizeBtn = $id('optimizeCaptionFree') || $id('optimizeBtn');
    if(optimizeBtn){
      optimizeBtn.addEventListener('click', safe(async () => {
        const ta = $id('userCaptionFree') || $id('userCaption') || $id('captionBox');
        if(!ta || !ta.value.trim()) {
          alert('Please enter a caption to optimize.');
          return;
        }
        
        const toneSelect = $id('toneSelectFree') || $id('toneSelect');
        const tone = toneSelect ? toneSelect.value : 'professional';
        const orig = optimizeBtn.textContent;
        optimizeBtn.disabled = true;
        optimizeBtn.textContent = 'Optimizing…';
        
        try{
          const data = await fetchProcessCaption(ta.value, tone, 'optimize');
          console.log('[optimize] Response:', data);
          if(window.populateOptimize) await window.populateOptimize(data);
        }catch(err){
          console.error('[optimize] Error:', err);
          alert('Optimize failed: '+err.message);
        }
        finally{
          optimizeBtn.disabled = false;
          optimizeBtn.textContent = orig;
        }
      }));
    }
  })();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', safe(initFreeAPIBindings));
} else {
  safe(initFreeAPIBindings)();
}

// Copy button handlers
function setupCopyButtons(){
  const copyBtn = safe((id) => {
    const btn = $id(id);
    if(!btn) return;
    btn.addEventListener('click', safe(async (e) => {
      e.preventDefault();
      let sourceId = 'rewrittenCaptionFree';
      if(id.includes('Hashtags')) sourceId = 'hashtagListFree';
      
      const sourceEl = $id(sourceId);
      if(!sourceEl) {
        alert('No content to copy');
        return;
      }
      
      const text = sourceEl.textContent || sourceEl.innerText;
      if(!text || text === '–') {
        alert('No content to copy');
        return;
      }
      
      try {
        if(navigator.clipboard && navigator.clipboard.writeText){
          await navigator.clipboard.writeText(text);
        } else {
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.left = '-9999px';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
        }
        const origText = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = origText; }, 1500);
      } catch(err){
        console.error('Copy failed:', err);
        alert('Copy failed - try manual selection');
      }
    }));
  });
  
  copyBtn('copyRewrittenFree');
  copyBtn('copyHashtagsFree');
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', safe(setupCopyButtons));
} else {
  safe(setupCopyButtons)();
}

window.fetchProcessCaption = fetchProcessCaption;
window.resetFreeUI = resetFreeUI;

// Real-time SEO calculation as user types
function calculateSEOLive(caption){
  if(!caption || !caption.trim()){
    $id('seoScoreFree').innerText = '–';
    $id('seoGradeFree').innerText = '–';
    return;
  }
  
  let score = 0;
  
  // Length (0-25)
  const length = caption.length;
  const words = caption.match(/[\w\u0980-\u09FF]+/g) || [];
  if(length >= 120 && length <= 250) score += 25;
  else if(length >= 90 && length < 120) score += 18;
  else if(length > 250) score += 10;
  else if(length >= 30) score += 6;
  
  // Emojis (0-15)
  const emojis = caption.match(/[\U0001F300-\U0001FAFF\u2764\uFE0F✨🌟💫🌸🔥☺️❤️😍🤩😇🌿🎉]/g) || [];
  if(emojis.length >= 3) score += 15;
  else if(emojis.length >= 1) score += 10;
  
  // Hashtags (0-18)
  const tags = caption.match(/#\w+/g) || [];
  if(tags.length >= 3 && tags.length <= 6) score += 18;
  else if(tags.length > 6) score += 10;
  else if(tags.length >= 1) score += 6;
  
  // CTA (0-12)
  const cta = /follow|share|comment|learn|watch|check|join|explore|subscribe|click|ফলো|শেয়ার|কমেন্ট|দেখুন/i;
  if(cta.test(caption)) score += 12;
  
  // Power words (0-12)
  const powerWords = /amazing|new|offer|sale|update|exclusive|today|viral|trending|launch|limited|best|premium|gift|bonus|breaking|latest/i;
  let powerCount = (caption.match(/amazing|new|offer|sale|update|exclusive|today|viral|trending|launch|limited|best|premium|gift|bonus|breaking|latest/gi) || []).length;
  score += Math.min(12, powerCount * 6);
  
  // Readability bonus (0-10)
  const sentences = caption.split(/[.!?]+/).filter(s=>s.trim());
  if(sentences.length > 0){
    const avgWords = words.length / sentences.length;
    if(avgWords <= 20) score += 8;
  }
  
  score = Math.min(100, Math.max(5, score));
  
  const grade = score >= 95 ? 'A+' : score >= 85 ? 'A' : score >= 75 ? 'B' : score >= 60 ? 'C' : score >= 40 ? 'D' : 'F';
  
  const seoEl = $id('seoScoreFree');
  const gradeEl = $id('seoGradeFree');
  if(seoEl) seoEl.innerText = score;
  if(gradeEl) gradeEl.innerText = grade;
}

// Bind clear/analyze/optimize handlers with safe immediate init (in case DOMContentLoaded already fired)
function initFreeAPIBindings(){
  // Caption textarea - add real-time SEO calculation
  const ta = $id('userCaptionFree') || $id('userCaption') || $id('captionBox');
  if(ta){
    ta.addEventListener('input', ()=>{
      calculateSEOLive(ta.value);
    });
  }
  
  // Clear
  const clearBtn = $id('clearCaptionFree') || $id('clearCaption');
  if(clearBtn){
    clearBtn.addEventListener('click', (e)=>{ e.preventDefault(); resetFreeUI(); });
  }

  // Analyze
  const analyzeBtn = $id('analyzeCaptionFree') || $id('analyzeBtn');
  if(analyzeBtn){
    analyzeBtn.addEventListener('click', async ()=>{
      const ta = $id('userCaptionFree') || $id('userCaption') || $id('captionBox');
      if(!ta || !ta.value.trim()) return alert('Please enter a caption to analyze.');
      const tone = ($id('toneSelectFree') || $id('toneSelect'))?.value || 'professional';

      // loading state
      const originalText = analyzeBtn.innerText;
      analyzeBtn.disabled = true; analyzeBtn.innerText = 'Analyzing…';
      try{
        const showSpinner = id => { const s = $id(id); if(s) s.classList.remove('hidden'); };
        showSpinner('seoSpinner'); showSpinner('rewrittenSpinner'); showSpinner('hashtagSpinner');
        const data = await fetchProcessCaption(ta.value, tone, 'analyze');
        const hideSpinner = id => { const s = $id(id); if(s) s.classList.add('hidden'); };
        hideSpinner('rewrittenSpinner'); hideSpinner('hashtagSpinner'); hideSpinner('seoSpinner');
        // populateAnalyze (reuse existing helper)
        try{ populateAnalyze(data); } catch(e){ console.error('populateAnalyze failed', e); }
      }catch(err){ console.error(err); alert('Analysis failed: '+err.message); }
      finally{ analyzeBtn.disabled = false; analyzeBtn.innerText = originalText; }
    });
  }

  // Optimize: always fetch fresh, read tone from tone selector in optimize panel
  const optimizeBtn = $id('optimizeCaptionFree') || $id('optimizeBtn');
  if(optimizeBtn){
    optimizeBtn.addEventListener('click', async ()=>{
      const ta = $id('userCaptionFree') || $id('userCaption') || $id('captionBox');
      if(!ta || !ta.value.trim()) return alert('Please enter a caption to optimize.');
      // Read tone from the optimize panel selector if present
      const toneSelect = $id('toneSelectFree') || $id('toneSelect');
      const tone = toneSelect ? toneSelect.value : 'professional';
      const orig = optimizeBtn.innerText; optimizeBtn.disabled = true; optimizeBtn.innerText = 'Optimizing…';
      const showSpinner = id => { const s = $id(id); if(s) s.classList.remove('hidden'); };
      showSpinner('rewrittenSpinner'); showSpinner('hashtagSpinner'); showSpinner('seoSpinner');
      try{
        const data = await fetchProcessCaption(ta.value, tone, 'optimize');
        const hideSpinner = id => { const s = $id(id); if(s) s.classList.add('hidden'); };
        hideSpinner('rewrittenSpinner'); hideSpinner('hashtagSpinner'); hideSpinner('seoSpinner');
        try{ if (typeof populateOptimize === 'function') populateOptimize(data); else if(window.populateOptimize) window.populateOptimize(data); } catch(e){ console.error('populateOptimize failed:', e); }
      }catch(err){ console.error('Optimize error:', err); alert('Optimize failed: '+err.message); }
      finally{ optimizeBtn.disabled = false; optimizeBtn.innerText = orig; }
    });
  }
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initFreeAPIBindings); else initFreeAPIBindings();

// Copy button handlers
function setupCopyButtons(){
  const copyBtn = id => {
    const btn = $id(id);
    if(!btn) return;
    btn.addEventListener('click', async (e)=>{
      e.preventDefault();
      // determine source element based on button id
      let sourceId = 'rewrittenCaptionFree';
      if(id.includes('Hashtags')) sourceId = 'hashtagListFree';
      
      const sourceEl = $id(sourceId);
      if(!sourceEl) return alert('No content to copy');
      
      const text = sourceEl.innerText || sourceEl.textContent;
      if(!text || text === '–') return alert('No content to copy');
      
      try {
        // try modern API first
        if(navigator.clipboard && navigator.clipboard.writeText){
          await navigator.clipboard.writeText(text);
        } else {
          // fallback: use textarea trick
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.left = '-9999px';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
        }
        // Show feedback
        const origText = btn.innerText;
        btn.innerText = 'Copied!';
        setTimeout(()=>{ btn.innerText = origText; }, 1500);
      } catch(err){
        console.error('Copy failed:', err);
        alert('Copy failed - try manual selection');
      }
    });
  };
  
  copyBtn('copyRewrittenFree');
  copyBtn('copyHashtagsFree');
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setupCopyButtons); else setupCopyButtons();

// expose for other modules
window.fetchProcessCaption = fetchProcessCaption;
window.resetFreeUI = resetFreeUI;
