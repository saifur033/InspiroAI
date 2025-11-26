/* ============================================================
   🔵 PRO MODE – UNIFIED DASHBOARD CONTROLLER v6.0
   Combines: API calls, UI interactions, event listeners
   ============================================================ */

// Utility: Safe DOM selector
const $ = (id) => document.getElementById(id);

// Loader helpers (fallback if loader.js not loaded)
function showLoader() {
  try { loaderShow(); } catch (e) { console.warn('[Loader] Show failed:', e); }
}
function hideLoader() {
  try { loaderHide(); } catch (e) { console.warn('[Loader] Hide failed:', e); }
}

// Toast helper (fallback if toast.js not loaded)
function toast(type, msg) {
  try { window.toast(type, msg); } catch (e) {
    console.warn(`[Toast] ${type}: ${msg}`);
    alert(msg);
  }
}

/* ============================================================
   🔐 TOKEN MANAGEMENT
============================================================ */
$("verifyTokenBtn")?.addEventListener("click", () => {
  const token = $("#fbToken")?.value.trim() || "";
  const pageId = $("#fbPageId")?.value.trim() || "";
  const status = $("#tokenStatus");

  if (!status) return;

  if (token.length > 20 && pageId.length > 3) {
    status.innerText = "Connected";
    status.className = "status-pill connected";
    status.style.background = "linear-gradient(90deg, #3be07a, #1fb46a)";
    status.style.color = "#fff";
    toast("success", "Token verified!");
  } else {
    status.innerText = "Not connected";
    status.className = "status-pill";
    status.style.background = "transparent";
    status.style.color = "#999";
    toast("error", "Invalid token or page ID");
  }
});

/* ============================================================
   📝 CAPTION MANAGEMENT
============================================================ */
$("#clearCaptionPro")?.addEventListener("click", () => {
  const box = $("#userCaptionPro");
  if (box) {
    box.value = "";
    box.focus();
    toast("info", "Caption cleared");
  }
});

/* ============================================================
   🎤 VOICE TO TEXT
============================================================ */
let recorder = null;
let audioChunks = [];

$("#startVoicePro")?.addEventListener("click", async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    audioChunks = [];

    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunks.push(e.data);
    };

    recorder.onstop = async () => {
      const blob = new Blob(audioChunks, { type: "audio/wav" });
      const form = new FormData();
      form.append("audio", blob, "voice.wav");

      showLoader();
      try {
        const res = await fetch("/api/voice_to_text", {
          method: "POST",
          body: form,
        });
        const data = await res.json();
        hideLoader();

        if (data.caption_text) {
          const box = $("#userCaptionPro");
          if (box) {
            box.value += (box.value ? " " : "") + data.caption_text;
            toast("success", "Voice converted to text");
          }
        } else {
          toast("error", "Failed to convert voice");
        }
      } catch (err) {
        hideLoader();
        toast("error", "Voice API error: " + err.message);
      }
    };

    recorder.start();
    const loader = $("#voiceLoaderPro");
    if (loader) loader.innerText = "Listening…";
    toast("info", "Recording started…");
  } catch (err) {
    toast("error", "Microphone access denied: " + err.message);
  }
});

$("#stopVoicePro")?.addEventListener("click", () => {
  if (recorder) {
    recorder.stop();
    const loader = $("#voiceLoaderPro");
    if (loader) loader.innerText = "Stopped";
  }
});

/* ============================================================
   🖼️ IMAGE → CAPTION
============================================================ */
$("#imageUploadPro")?.addEventListener("change", async (e) => {
  const file = e.target.files?.[0];
  if (!file) return toast("error", "Select an image");

  const form = new FormData();
  form.append("image", file);

  showLoader();
  try {
    const res = await fetch("/api/image_caption", {
      method: "POST",
      body: form,
    });
    const data = await res.json();
    hideLoader();

    if (data.caption) {
      const box = $("#userCaptionPro");
      if (box) {
        box.value = data.caption;
        toast("success", "Caption generated from image");
      }
    } else {
      toast("error", "Failed to generate caption from image");
    }
  } catch (err) {
    hideLoader();
    toast("error", "Image API error: " + err.message);
  }
});

/* ============================================================
   📊 ANALYZE CAPTION
============================================================ */
$("#analyzeCaptionPro")?.addEventListener("click", async () => {
  const caption = $("#userCaptionPro")?.value.trim();
  if (!caption) return toast("error", "Caption is empty");

  showLoader();
  try {
    const res = await fetch("/api/process_caption", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ caption }),
    });
    const data = await res.json();
    hideLoader();

    if (data.error) {
      toast("error", data.error);
      return;
    }

    // Display SEO analysis
    if (data.seo_original) {
      $("#seoScorePro").innerText = data.seo_original.score ?? "–";
      $("#seoGradePro").innerText = data.seo_original.grade ?? "–";
      const suggestions = data.seo_original.suggestions || [];
      $("#seoSuggestionsPro").innerHTML = suggestions
        .map((s) => `<li>${s}</li>`)
        .join("");
    }

    // Display emotion analysis
    if (data.emotion?.original) {
      $("#emotionMainPro").innerText = data.emotion.original.top_emotion ?? "–";
      $("#emotionReasonPro").innerText = data.emotion.original.reason ?? "–";
    }

    // Display fake/real analysis
    if (data.fake_real?.old) {
      $("#fakePercentPro").innerText = data.fake_real.old.fake ?? "–";
      $("#realPercentPro").innerText = data.fake_real.old.real ?? "–";
      $("#fakeReasonPro").innerText = data.fake_real.old.reason ?? "–";
    }

    // Show results
    const resultsDiv = $("#analyzeResultsPro");
    if (resultsDiv) resultsDiv.classList.remove("hidden");

    toast("success", "Analysis complete!");
  } catch (err) {
    hideLoader();
    toast("error", "Analysis error: " + err.message);
  }
});

/* ============================================================
   ✨ OPTIMIZE CAPTION
============================================================ */
$("#optimizeCaptionPro")?.addEventListener("click", async () => {
  const caption = $("#userCaptionPro")?.value.trim();
  const tone = $("#toneSelectPro")?.value || "friendly";

  if (!caption) return toast("error", "Caption is empty");

  showLoader();
  try {
    const res = await fetch("/api/process_caption", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ caption, tone }),
    });
    const data = await res.json();
    hideLoader();

    if (data.error) {
      toast("error", data.error);
      return;
    }

    // Display optimized content
    if (data.optimized_caption) {
      $("#rewrittenCaptionPro").innerText = data.optimized_caption;
    }

    // Display hashtags
    if (data.hashtags) {
      if (Array.isArray(data.hashtags)) {
        $("#hashtagListPro").innerText = data.hashtags.join(" ");
      } else {
        $("#hashtagListPro").innerText = data.hashtags;
      }
    }

    // Display SEO improvement
    if (data.seo_original && data.seo) {
      const oldScore = data.seo_original.score ?? 0;
      const newScore = data.seo.optimized_score ?? 0;
      $("#oldSeoPro").innerText = oldScore;
      $("#newSeoPro").innerText = newScore;
      $("#diffSeoPro").innerText = newScore - oldScore;
    }

    // Display emotion
    if (data.emotion?.optimized) {
      $("#optEmotionPro").innerText = data.emotion.optimized.top_emotion ?? "–";
    }

    // Display fake/real
    if (data.fake_real?.new) {
      $("#optFakePro").innerText = data.fake_real.new.fake ?? "–";
      $("#optRealPro").innerText = data.fake_real.new.real ?? "–";
    }

    // Show optimization results
    const optBox = $("#optimizeBoxPro");
    if (optBox) optBox.classList.remove("hidden");

    toast("success", "Caption optimized successfully!");
  } catch (err) {
    hideLoader();
    toast("error", "Optimization error: " + err.message);
  }
});

/* ============================================================
   📤 SHARE TO FACEBOOK
============================================================ */
$("#shareNowBtn")?.addEventListener("click", async () => {
  const message = $("#rewrittenCaptionPro")?.innerText.trim();
  const token = $("#fbToken")?.value.trim() || $("#fbApiToken")?.value.trim();
  const pageId = $("#fbPageId")?.value.trim();

  if (!token || !pageId) {
    return toast("error", "Token and Page ID are required");
  }

  if (!message) {
    return toast("error", "No caption to share. Optimize first!");
  }

  showLoader();
  try {
    const res = await fetch("/api/facebook_post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, page_id: pageId, message }),
    });
    const data = await res.json();
    hideLoader();

    if (data.success) {
      toast("success", data.reason || "Post shared to Facebook!");
    } else {
      toast("error", data.reason || "Failed to share post");
    }
  } catch (err) {
    hideLoader();
    toast("error", "Share error: " + err.message);
  }
});

/* ============================================================
   ⏰ SCHEDULE POST
============================================================ */
$("#scheduleBtn")?.addEventListener("click", async () => {
  const token = $("#fbToken")?.value.trim() || $("#fbApiToken")?.value.trim();
  const pageId = $("#fbPageId")?.value.trim();
  const message = $("#rewrittenCaptionPro")?.innerText.trim();

  const date = $("#scheduleDate")?.value || $("#schedDate")?.value;
  const time = $("#scheduleTime")?.value || $("#schedTime")?.value;

  if (!token || !pageId) {
    return toast("error", "Token and Page ID are required");
  }

  if (!date || !time) {
    return toast("error", "Select a date and time");
  }

  if (!message) {
    return toast("error", "No caption to schedule");
  }

  try {
    const timestamp = Math.floor(new Date(`${date}T${time}`).getTime() / 1000);

    showLoader();
    const res = await fetch("/api/facebook_schedule", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        token,
        page_id: pageId,
        message,
        timestamp,
      }),
    });
    const data = await res.json();
    hideLoader();

    if (data.success) {
      toast("success", data.reason || "Post scheduled!");
    } else {
      toast("error", data.reason || "Failed to schedule post");
    }
  } catch (err) {
    hideLoader();
    toast("error", "Schedule error: " + err.message);
  }
});

/* ============================================================
   🎯 POST REACH PREDICTION
============================================================ */
$("#calcReachBtn")?.addEventListener("click", async () => {
  const day = $("#reachDay")?.value || "Monday";
  const type = $("#reachType")?.value || "Non-Paid";

  showLoader();
  try {
    const res = await fetch("/api/post_reach", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ day, type }),
    });
    const data = await res.json();
    hideLoader();

    if (data.reach) {
      $("#predictedReach").innerText = data.reach;
      $("#bestTime").innerText = data.best_time || "18:00";
      toast("success", "Reach prediction calculated");
    } else {
      toast("error", "Could not calculate reach");
    }
  } catch (err) {
    hideLoader();
    toast("error", "Reach prediction error: " + err.message);
  }
});

/* ============================================================
   🔄 AUTO SHARE BY REACH GOAL
============================================================ */
$("#saveAutoShareBtn")?.addEventListener("click", async () => {
  const goal = $("#reachGoal")?.value;
  const caption = $("#autoSharePreview")?.value;

  if (!goal || !caption) {
    return toast("error", "Enter reach goal and caption");
  }

  showLoader();
  try {
    const res = await fetch("/api/save_auto_share", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal: parseInt(goal), caption }),
    });
    const data = await res.json();
    hideLoader();

    if (data.success) {
      toast("success", data.reason || "Auto-share configured!");
    } else {
      toast("error", data.reason || "Failed to save auto-share");
    }
  } catch (err) {
    hideLoader();
    toast("error", "Auto-share error: " + err.message);
  }
});

/* ============================================================
   🎬 INITIALIZE ON DOM READY
============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  console.log("[Pro Dashboard] Initialized - All event listeners active");
});
