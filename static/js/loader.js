/* =========================================================
   InspiroAI — Neon Loader (Stable v4.0 - Safe Edition)
   Smooth Fade + Safe DOM Handling + Error Protection
========================================================= */

const safe = (fn) => (...args) => {
  try { return fn(...args); }
  catch(err){ console.error("Loader JS Error:", err); }
};

window.showLoader = safe(function () {
    try {
        let ld = document.getElementById("globalLoader");
        if(ld) ld.remove();
        
        ld = document.createElement("div");
        ld.id = "globalLoader";
        ld.className = "loader-hidden";

        ld.innerHTML = `
            <div class="loader-overlay">
                <div class="loader-wrapper">
                    <div class="loader-dot"></div>
                    <div class="loader-dot"></div>
                    <div class="loader-dot"></div>
                </div>
            </div>
        `;

        document.body.appendChild(ld);

        requestAnimationFrame(() => {
            if(ld && ld.parentNode) {
                ld.classList.remove("loader-hidden");
                ld.classList.add("loader-visible");
            }
        });
    } catch(err) {
        console.error("showLoader error:", err);
    }
});

window.hideLoader = safe(function () {
    try {
        const ld = document.getElementById("globalLoader");
        if (!ld) return;

        ld.classList.remove("loader-visible");
        ld.classList.add("loader-hidden");

        setTimeout(() => {
            try {
                if(ld && ld.parentNode) ld.remove();
            } catch(e) { console.error("hideLoader cleanup error:", e); }
        }, 300);
    } catch(err) {
        console.error("hideLoader error:", err);
    }
});
