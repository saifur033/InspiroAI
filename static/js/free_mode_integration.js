/*
  free_mode_integration.js
  Wires Free Mode UI controls to backend endpoints (/api/process_caption, /api/voice_to_text)
  - Supports both ID variants used across templates and the custom free.html
  - Robust: checks element existence, shows loader/toast if available
*/

(function () {
  // small helpers
  const $ = id => document.getElementById(id);
  const exists = id => !!$(id);

  function getCaptionEl() { return $('userCaptionFree') || $('captionBox') || $('userCaption'); }
  function getAnalyzeBtn() { return $('analyzeCaptionFree') || $('analyzeBtn'); }
  function getOptimizeBtn() { return $('optimizeCaptionFree') || $('optimizeBtn'); }
  function getToneSelect() { return $('toneSelectFree') || $('toneSelect'); }

  function safeToast(msg, type='success'){
    if (window.toastSuccess && type==='success') return toastSuccess(msg);
    if (window.toastError && type==='error') return toastError(msg);
    if (window.toast && type) return window.toast(type, msg);
    console.log(type.toUpperCase()+':', msg);
  }

  async function postProcessCaption(caption, tone){
    // prefer shared fetch implementation if available
    if (window.fetchProcessCaption && typeof window.fetchProcessCaption === 'function'){
      return window.fetchProcessCaption(caption, tone);
    }

    const payload = { caption: caption || '' };
    if (tone) payload.tone = tone;

    const res = await fetch('/api/process_caption', {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Server error: '+res.status);
    return res.json();
  }

  // populate fields for analyze results (supports both sets)
  function populateAnalyze(data){
    // Handle both analyze response format
    const isAnalyzeMode = data.action === 'analyze';
    
    // SEO
    const seoScore = $('seoScoreFree') || $('seoScore'); 
    if (seoScore) seoScore.innerText = data.seo ?? data.seo_score ?? '-';
    
    const seoGrade = $('seoGradeFree') || $('seoGrade'); 
    if (seoGrade) seoGrade.innerText = data.seo_grade ?? '-';
    
    const sug = $('seoSuggestionsFree') || $('seoSuggestions'); 
    if (sug){
      const arr = data.seo_tips || data.seo_suggestions || [];
      sug.innerHTML = arr.map(s=>`<li>${s}</li>`).join('');
    }

    // Emotion - IMPORTANT: Show reason why it's that emotion
    const emoMain = $('emotionMainFree') || $('emotionMain'); 
    if (emoMain) emoMain.innerText = data.emotion ?? '-';
    
    const emoConf = $('emotionConfidenceFree'); 
    if (emoConf) {
      const dist = data.emotions || {};
      const topEmo = data.emotion;
      const confidence = topEmo && dist[topEmo] ? Math.round((dist[topEmo]) * 100) + '%' : '-';
      emoConf.innerText = confidence;
    }
    
    // Emotion Reason/Details - কেন এই emotion detected হলো
    const emoReason = $('emotionReasonFree') || $('emotionReason'); 
    if (emoReason) {
      const reason = data.reason ?? '-';
      emoReason.innerText = reason;
    }

    // Fake/Real - IMPORTANT: Show reason why it's fake/real
    const fakePct = $('fakePercentFree') || $('fakePct') || $('fakePctFree'); 
    if (fakePct) fakePct.innerText = (data.fake_percent ?? 0) + '%';
    
    const realPct = $('realPercentFree') || $('realPct') || $('realPctFree'); 
    if (realPct) realPct.innerText = (data.real_percent ?? 0) + '%';
    
    // Fake/Real Reason/Details - কেন এই % এবং কেন এত fake/real
    const fakeReason = $('fakeReasonFree') || $('fakeReason'); 
    if (fakeReason) {
      const reason = data.reasoning ?? '-';
      fakeReason.innerText = reason;
    }

    // show analyze container if exists
    const analyzeResults = $('analyzeResultsFree') || $('analyzeResults'); 
    if (analyzeResults) analyzeResults.classList.remove('hidden');

    // hide per-card spinners if present
    const hideSpinner = id => { const s = document.getElementById(id); if(s) s.classList.add('hidden'); };
    hideSpinner('rewrittenSpinner'); hideSpinner('hashtagSpinner'); hideSpinner('seoSpinner');
  }

  // populate optimization results
  function populateOptimize(data){
    // AI Rewritten Caption
    const rew = $('rewrittenCaptionFree') || $('rewrittenCaption'); 
    if (rew) rew.innerText = data.optimized_caption ?? '';
    
    // Hashtags: ensure minimum 10 from API response or generate more
    const hashtagsEl = $('hashtagListFree') || $('hashtagsList') || $('hashtagList');
    if (hashtagsEl){
      let hashtags = [];
      if (Array.isArray(data.hashtags)) {
        hashtags = data.hashtags;
      } else if (typeof data.hashtags === 'string') {
        hashtags = data.hashtags.split(' ').filter(h => h.startsWith('#'));
      }
      
      // If less than 10, generate more from caption
      if (hashtags.length < 10 && data.optimized_caption) {
        const caption = data.optimized_caption.toLowerCase();
        const keywords = caption.match(/\b\w{4,}\b/g) || [];
        const uniqueKeywords = [...new Set(keywords)];
        const generated = uniqueKeywords.slice(0, 10 - hashtags.length).map(kw => '#' + kw);
        hashtags = [...hashtags, ...generated];
      }
      
      hashtagsEl.innerText = hashtags.slice(0, 15).join(' ');
    }
    
    // === SEO SCORES ===
    const oldSeo = $('oldSeoFree') || $('oldSeo'); 
    if (oldSeo) oldSeo.innerText = data.old_seo ?? '-';
    
    const newSeo = $('newSeoFree') || $('newSeo'); 
    if (newSeo) newSeo.innerText = data.new_seo ?? '-';
    
    const diff = $('diffSeoFree') || $('diffSeo'); 
    if (diff) {
      const oldv = parseFloat(data.old_seo ?? 0) || 0;
      const newv = parseFloat(data.new_seo ?? 0) || 0;
      const d = Math.round(newv - oldv);
      diff.innerText = (d>0?'+':'') + d;
      diff.classList.remove('seo-diff--up','seo-diff--down');
      if(d>0) diff.classList.add('seo-diff--up'); 
      else if(d<0) diff.classList.add('seo-diff--down');
    }
    
    // === OPTIMIZED EMOTION ===
    const optEmo = $('optEmotionFree') || $('optEmotion'); 
    if (optEmo) optEmo.innerText = data.new_emotion ?? '-';
    
    const optEmoReason = $('optEmotionReasonFree'); 
    if (optEmoReason) optEmoReason.innerText = 'Updated emotion detected';
    
    // === OPTIMIZED FAKE/REAL ===
    const optFake = $('optFakeFree') || $('optFake'); 
    if (optFake) optFake.innerText = (data.new_fake_percent ?? 0) + '%';
    
    const optReal = $('optRealFree') || $('optReal'); 
    if (optReal) optReal.innerText = (data.new_real_percent ?? 0) + '%';
    
    const optFakeReason = $('optFakeReasonFree'); 
    if (optFakeReason) optFakeReason.innerText = 'Updated authenticity score';

    // show optimize panel
    const optPanel = $('optimizeBoxFree') || $('optimizePanel'); 
    if (optPanel) optPanel.classList.remove('hidden');

    // hide any spinners
    const hideSpinner = id => { const s = document.getElementById(id); if(s) s.classList.add('hidden'); };
    hideSpinner('rewrittenSpinner'); hideSpinner('hashtagSpinner'); hideSpinner('seoSpinner');
  }

  // Expose helpers so other modules (free_api.js) can call them directly
  window.populateAnalyze = populateAnalyze;
  window.populateOptimize = populateOptimize;

  // enable/disable analyze & optimize
  function bindEnableLogic(){
    const captionEl = getCaptionEl();
    const analyze = getAnalyzeBtn();
    const optimize = getOptimizeBtn();
    if (!captionEl) return;
    function update(){
      const has = captionEl.value.trim().length>0;
      if (analyze) analyze.disabled = !has;
      if (optimize) optimize.disabled = !has;
    }
    captionEl.addEventListener('input', ()=>{
      update();
      // hide results when cleared
      if (!captionEl.value.trim()){
        const ar = $('analyzeResultsFree') || $('analyzeResults'); if (ar) ar.classList.add('hidden');
        const op = $('optimizeBoxFree') || $('optimizePanel'); if (op) op.classList.add('hidden');
      }
    });
    update();
  }

  // Voice recording (supports both ids) — improved continuous update + language detection
  function bindVoice(){
    const start = $('startVoiceFree') || $('startVoice');
    const end = $('endVoiceFree') || $('endVoice');
    const captionEl = getCaptionEl();
    const voiceLoading = $('voiceLoading') || $('voiceLoadingFree');
    const voiceStatus = $('voiceStatusFree') || $('voiceStatus');

    if (!start || !end || !captionEl) return;
    // Prefer Web Speech API for live transcription when available
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition || null;

    if (SpeechRec) {
      let recognition = null;
      start.addEventListener('click', ()=>{
        try{
          recognition = new SpeechRec();
          recognition.continuous = true;
          recognition.interimResults = true;
          // Detect language from captionLang select: en or bn
          const langSelect = document.getElementById('captionLang');
          recognition.lang = (langSelect?.value === 'bn') ? 'bn-BD' : 'en-US';
          if (voiceLoading) { voiceLoading.classList.remove('hidden'); }
          if (voiceStatus) voiceStatus.innerText = 'Listening...';

          let interim = '';
          recognition.onresult = (ev)=>{
            let finalTranscript = '';
            interim = '';
            for (let i = ev.resultIndex; i < ev.results.length; ++i) {
              const res = ev.results[i];
              if (res.isFinal) finalTranscript += (res[0].transcript + ' ');
              else interim += res[0].transcript;
            }
            // continuously update with final results, avoiding duplicates
            if (finalTranscript.trim()) {
              const newText = finalTranscript.trim();
              if (!captionEl.value.endsWith(newText)) {
                captionEl.value = (captionEl.value.trim() + ' ' + newText).trim();
              }
            }
            if (voiceStatus) voiceStatus.innerText = interim ? 'Listening (interim)...' : 'Listening...';
          };

          recognition.onerror = (e)=>{
            console.error('SpeechRec error', e);
            safeToast('Speech recognition failed','error');
            if (voiceLoading) voiceLoading.classList.add('hidden');
            if (voiceStatus) voiceStatus.innerText = 'Idle';
            recognition && recognition.stop();
          };

          recognition.onend = ()=>{
            if (voiceLoading) voiceLoading.classList.add('hidden');
            if (voiceStatus) voiceStatus.innerText = 'Idle';
          };

          recognition.start();
        }catch(err){ console.error(err); safeToast('Microphone access denied or unavailable','error'); }
      });

      end.addEventListener('click', ()=>{
        try{ recognition && recognition.stop(); }
        catch(e){ console.warn('stop error', e); }
      });

    } else {
      // Fallback: record audio blob and send to backend for transcription
      let recorder = null; let chunks = [];

      start.addEventListener('click', async ()=>{
        try{
          if (voiceLoading) { voiceLoading.classList.remove('hidden'); }
          if (voiceStatus) voiceStatus.innerText = 'Listening...';
          const stream = await navigator.mediaDevices.getUserMedia({ audio:true });
          recorder = new MediaRecorder(stream);
          chunks = [];
          recorder.ondataavailable = e => { if (e.data.size>0) chunks.push(e.data); };
          recorder.onstop = async ()=>{
            if (voiceLoading) voiceLoading.classList.add('hidden');
            if (voiceStatus) voiceStatus.innerText = 'Processing...';
            const blob = new Blob(chunks, {type:'audio/wav'});
            const fd = new FormData(); fd.append('audio', blob, 'voice.wav');
            try{
              const r = await fetch('/api/voice_to_text', { method:'POST', body: fd });
              const data = await r.json();
              if (data.caption_text) {
                captionEl.value = (captionEl.value+' '+data.caption_text).trim();
                safeToast('Voice converted');
              } else {
                safeToast('No transcription', 'warning');
              }
            }catch(err){ console.error(err); safeToast('Voice API error','error'); }
            if (voiceStatus) voiceStatus.innerText = 'Idle';
          };
          recorder.start();
        }catch(err){
          console.error(err); safeToast('Microphone access denied','error');
          if (voiceLoading) voiceLoading.classList.add('hidden');
          if (voiceStatus) voiceStatus.innerText = 'Idle';
        }
      });

      end.addEventListener('click', ()=>{ if (recorder) recorder.stop(); });
    }
  }

  // bind analyze & optimize click
  function bindActions(){
    // Analysis & optimization are handled centrally in free_api.js to avoid duplicate handlers.
    // This module keeps enable/voice bindings only.
  }

  // init
  document.addEventListener('DOMContentLoaded', ()=>{
    bindEnableLogic();
    bindVoice();
    bindActions();
  });

})();
