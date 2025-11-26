/* =========================================================
   InspiroAI — API Error Handler
   Global error popup for failed API calls
========================================================= */

window.apiError = function(message = "Something went wrong!") {
    const box = document.createElement("div");
    box.className = "api-error-toast";
    box.innerHTML = `
        <div class="api-error-inner">
            <span class="api-error-icon">⚠️</span>
            <p>${message}</p>
        </div>
    `;

    document.body.appendChild(box);

    setTimeout(() => {
        box.classList.add("hide");
        setTimeout(() => box.remove(), 400);
    }, 3000);
};

// Auto wrap fetch to capture failures
window.safeFetch = async function(url, options = {}) {
    try {
        const res = await fetch(url, options);
        if (!res.ok) {
            apiError(`Server Error: ${res.status}`);
        }
        return res;
    } catch (err) {
        apiError("Network Error! Check your internet.");
        throw err;
    }
};
