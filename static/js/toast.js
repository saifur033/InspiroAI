
/* =========================================================
   InspiroAI — Toast Notifications (Stable v3.5)
   Smooth, Fast & Fully Compatible with Free/Pro Mode
========================================================= */

window.toast = function(type = "info", message = "Message") {

    // CREATE CONTAINER IF MISSING
    let container = document.getElementById("toastContainer");
    if (!container) {
        container = document.createElement("div");
        container.id = "toastContainer";
        container.className = "toast-container";
        document.body.appendChild(container);
    }

    // CREATE TOAST ITEM
    const toast = document.createElement("div");
    toast.className = `toast-item ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">
            ${
                type === "success" ? "✅" :
                type === "error"   ? "❌" :
                type === "warning" ? "⚠️" : "ℹ️"
            }
        </div>
        <div class="toast-text">${message}</div>
    `;

    container.appendChild(toast);

    // Slight delay to trigger CSS animation
    requestAnimationFrame(() => {
        toast.classList.add("show");
    });

    // AUTO HIDE
    setTimeout(() => {
        toast.classList.remove("show");
        toast.classList.add("hide");

        setTimeout(() => {
            toast.remove();
        }, 350); // must match hide animation time
    }, 2600);
};

/* =========================================================
   SHORTCUT FUNCTIONS
========================================================= */
window.toastSuccess = msg => window.toast("success", msg);
window.toastError   = msg => window.toast("error", msg);
window.toastWarning = msg => window.toast("warning", msg);
window.toastInfo    = msg => window.toast("info", msg);
