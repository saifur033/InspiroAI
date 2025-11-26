// caption_core.js
// Shared caption analysis & optimization logic for Free and Pro pages
(function(){
  const $id = (prefix, id) => document.getElementById(id + prefix) || document.getElementById(id + '_' + prefix) || document.getElementById(id + prefix + '');
  const $ = id => document.getElementById(id);

  function showLoaderSafe(){ try{ if(window.showLoader) showLoader(); }catch(e){} }
  function hideLoaderSafe(){ try{ if(window.hideLoader) hideLoader(); }catch(e){} }
  function toastSafe(msg, type='success'){ if(type==='success' && window.toastSuccess) return toastSuccess(msg); if(type==='error' && window.toastError) return toastError(msg); if(window.toast) return window.toast(type,msg); console.log(type,msg); }

  async function postProcessCaption(caption, tone){
    const payload = { caption: caption || '' };
    if(tone) payload.tone = tone;
    const res = await fetch('/api/process_caption', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    if(!res.ok){ const t = await res.text(); throw new Error('Server: '+res.status+' '+t.slice(0,200)); }
    return res.json();
  }

  function populateAnalyzeByIds(prefix, data){
    // SEO
    const seoScoreEl = document.getElementById('seoScore'+prefix);
    if(seoScoreEl) seoScoreEl.innerText = (data.seo_original && data.seo_original.score != null) ? data.seo_original.score : '-';
    const seoGradeEl = document.getElementById('seoGrade'+prefix);
    if(seoGradeEl) seoGradeEl.innerText = (data.seo_original && data.seo_original.grade) ? data.seo_original.grade : '-';
    const sugEl = document.getElementById('seoSuggestions'+prefix);
    if(sugEl) sugEl.innerHTML = (data.seo_original && data.seo_original.suggestions ? data.seo_original.suggestions : []).map(s=>`<li>${s}</li>`).join('');

    // Emotion
    const emoMain = document.getElementById('emotionMain'+prefix);
    if(emoMain) emoMain.innerText = (data.emotion && data.emotion.original && data.emotion.original.top_emotion) ? data.emotion.original.top_emotion : '-';
    const emoDist = document.getElementById('emotionDist'+prefix);
    if(emoDist) emoDist.innerText = JSON.stringify((data.emotion && data.emotion.original && data.emotion.original.distribution) || {});
    const emoReason = document.getElementById('emotionReason'+prefix);
    if(emoReason) emoReason.innerText = (data.emotion && data.emotion.original && data.emotion.original.reason) ? data.emotion.original.reason : '';

    // Fake/Real
    const fakeEl = document.getElementById('fakePercent'+prefix);
    const realEl = document.getElementById('realPercent'+prefix);
    if(fakeEl) fakeEl.innerText = ((data.fake_real && data.fake_real.original && data.fake_real.original.fake) ? data.fake_real.original.fake : 0) + '%';
    if(realEl) realEl.innerText = ((data.fake_real && data.fake_real.original && data.fake_real.original.real) ? data.fake_real.original.real : 0) + '%';
    const fakeReasonEl = document.getElementById('fakeReason'+prefix);
    if(fakeReasonEl) fakeReasonEl.innerText = (data.fake_real && data.fake_real.original && data.fake_real.original.reason) ? data.fake_real.original.reason : '';

    const resultsContainer = document.getElementById('analyzeResults'+prefix);
    if(resultsContainer) resultsContainer.classList.remove('hidden');
  }

  function populateOptimizeByIds(prefix, data){
    const rew = document.getElementById('rewrittenCaption'+prefix);
    if(rew) rew.innerText = data.optimized_caption || '';

    const hashtagsEl = document.getElementById('hashtagList'+prefix);
    if(hashtagsEl){ if(Array.isArray(data.hashtags)) hashtagsEl.innerText = data.hashtags.join(' '); else hashtagsEl.innerText = data.hashtags || ''; }

    const oldSeo = document.getElementById('oldSeo'+prefix);
    const newSeo = document.getElementById('newSeo'+prefix);
    const diffSeo = document.getElementById('diffSeo'+prefix);
    if(oldSeo) oldSeo.innerText = (data.seo_original && data.seo_original.score!=null) ? data.seo_original.score : '-';
    if(newSeo) newSeo.innerText = (data.seo && data.seo.optimized_score!=null) ? data.seo.optimized_score : (data.seo && data.seo.optimized_score==0?0:'-');
    if(diffSeo) diffSeo.innerText = (data.seo && data.seo.difference!=null) ? data.seo.difference : ((data.seo && data.seo.optimized_score!=null && data.seo_original && data.seo_original.score!=null) ? (data.seo.optimized_score - data.seo_original.score) : '-');

    const optEmo = document.getElementById('optEmotion'+prefix);
    if(optEmo) optEmo.innerText = (data.emotion && data.emotion.optimized && data.emotion.optimized.top_emotion) ? data.emotion.optimized.top_emotion : '-';

    const optFake = document.getElementById('optFake'+prefix);
    const optReal = document.getElementById('optReal'+prefix);
    if(optFake) optFake.innerText = ((data.fake_real && data.fake_real.optimized && data.fake_real.optimized.fake_new) ? data.fake_real.optimized.fake_new : 0) + '%';
    if(optReal) optReal.innerText = ((data.fake_real && data.fake_real.optimized && data.fake_real.optimized.real_new) ? data.fake_real.optimized.real_new : 0) + '%';

    const optPanel = document.getElementById('optimizeBox'+prefix);
    if(optPanel) optPanel.classList.remove('hidden');
  }

  // voice recorder factory returns start/stop handlers bound to textarea id
  function createVoiceHandlers(textareaId, statusId){
    let recorder=null; let chunks=[]; let recognition=null; let lastAppended='';
    async function start(){
      // Prefer Web Speech API for continuous live transcription
      try{
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        const statusEl = document.getElementById(statusId);
        if(SpeechRec){
          recognition = new SpeechRec();
          recognition.lang = 'en-US';
          recognition.interimResults = true;
          recognition.continuous = true;
          recognition.onstart = ()=>{ if(statusEl) statusEl.innerText='Listening...'; };
          recognition.onerror = (e)=>{ console.error('speech error',e); if(statusEl) statusEl.innerText='Error'; };
          recognition.onresult = (evt)=>{
            let interim = '';
            let final = '';
            for(let i=evt.resultIndex;i<evt.results.length;i++){
              const res = evt.results[i];
              if(res.isFinal) final += res[0].transcript + ' ';
              else interim += res[0].transcript + ' ';
            }
            const ta = document.getElementById(textareaId);
            if(ta){
              // append only new final text to avoid duplicates
              if(final.trim()){ if(!ta.value.endsWith(final.trim())) ta.value = (ta.value + ' ' + final).trim(); }
            }
          };
          recognition.start();
          return;
        }
        // Fallback: record audio and send on stop
        const stream = await navigator.mediaDevices.getUserMedia({audio:true});
        recorder = new MediaRecorder(stream);
        chunks = [];
        recorder.ondataavailable = e=>{ if(e.data.size>0) chunks.push(e.data); };
        recorder.onstop = async ()=>{
          const blob = new Blob(chunks, {type:'audio/wav'});
          const fd = new FormData(); fd.append('audio', blob, 'voice.wav');
          showLoaderSafe();
          try{
            const r = await fetch('/api/voice_to_text', { method:'POST', body: fd });
            const j = await r.json();
            if(j.caption_text){ const ta = document.getElementById(textareaId); if(ta){
              // prevent duplicates
              const toAdd = j.caption_text.trim();
              if(!ta.value.includes(toAdd)) ta.value = (ta.value + ' ' + toAdd).trim();
            } toastSafe('Voice converted'); }
          }catch(err){ console.error(err); toastSafe('Voice API error','error'); }
          hideLoaderSafe();
          const st = document.getElementById(statusId); if(st) st.innerText = 'Idle';
        };
        recorder.start();
        const st = document.getElementById(statusId); if(st) st.innerText = 'Listening...';
      }catch(err){ console.error(err); toastSafe('Microphone access denied','error'); const st = document.getElementById(statusId); if(st) st.innerText='Idle'; }
    }
    function stop(){ if(recognition){ try{ recognition.stop(); }catch(e){} recognition=null; } if(recorder) { recorder.stop(); recorder=null; } }
    return { start, stop };
  }

  function initCaptionModule(prefix){
    // prefix is 'Free' or 'Pro' matching element IDs in templates
    const textarea = document.getElementById('userCaption'+prefix);
    const analyzeBtn = document.getElementById('analyzeCaption'+prefix);
    const optimizeBtn = document.getElementById('optimizeCaption'+prefix);
    const toneSelect = document.getElementById('toneSelect'+prefix);

    // enable/disable
    function updateBtns(){ const has = textarea && textarea.value.trim().length>0; if(analyzeBtn) analyzeBtn.disabled = !has; if(optimizeBtn) optimizeBtn.disabled = !has; }

    if(textarea){
      textarea.addEventListener('input', ()=>{ updateBtns(); const ar = document.getElementById('analyzeResults'+prefix); const op = document.getElementById('optimizeBox'+prefix); if(ar && !textarea.value.trim()) ar.classList.add('hidden'); if(op && !textarea.value.trim()) op.classList.add('hidden'); });
      updateBtns();
    }

    // voice
    const startVoice = document.getElementById('startVoice'+prefix);
    const endVoice = document.getElementById('endVoice'+prefix);
    if(startVoice && endVoice && textarea){
      const v = createVoiceHandlers('userCaption'+prefix, 'voiceStatus'+prefix);
      startVoice.addEventListener('click', v.start);
      endVoice.addEventListener('click', v.stop);
    }

    // analyze
    if(analyzeBtn){
      analyzeBtn.addEventListener('click', async ()=>{
        if(!textarea || !textarea.value.trim()) return toastSafe('Caption empty','error');
        showLoaderSafe();
        try{
          const data = await postProcessCaption(textarea.value.trim(), toneSelect? toneSelect.value : undefined);
          populateAnalyzeByIds(prefix, data);
          toastSafe('Analysis complete');
        }catch(err){ console.error(err); toastSafe('Analysis failed','error'); }
        finally{ hideLoaderSafe(); }
      });
    }

    // optimize
    if(optimizeBtn){
      optimizeBtn.addEventListener('click', async ()=>{
        if(!textarea || !textarea.value.trim()) return toastSafe('Caption empty','error');
        showLoaderSafe();
        try{
          const data = await postProcessCaption(textarea.value.trim(), toneSelect? toneSelect.value : undefined);
          populateOptimizeByIds(prefix, data);
          toastSafe('Optimization complete');
        }catch(err){ console.error(err); toastSafe('Optimization failed','error'); }
        finally{ hideLoaderSafe(); }
      });
    }
  }

  // expose
  window.initCaptionModule = initCaptionModule;
})();
