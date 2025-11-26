/* =========================================================
   LIVE CLOCK
========================================================= */
function updateClock() {
    const now = new Date();
    document.getElementById("liveDate").innerText = now.toLocaleDateString();
    document.getElementById("liveDay").innerText = now.toLocaleString("en-US", { weekday: "long" });
    document.getElementById("liveTime").innerText = now.toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();


/* =========================================================
   CATEGORY COLORS (Safe fallback)
========================================================= */
const categoryColors = {
    Politics: "#ff5252",
    Cricket: "#00d27f",
    Tech: "#00b2ff",
    Crime: "#ff8c00",
    Campus: "#9b59b6",
    Accident: "#e74c3c",
    Entertainment: "#f1c40f",
    General: "#bdc3c7",
};


/* =========================================================
   LOAD TRENDS (BD Trend Engine PRO)
========================================================= */
async function loadLiveTrends() {
    try {
        const res = await fetch("/api/trends");
        const data = await res.json();

        const list = document.getElementById("trendList");
        const graph = document.getElementById("trendGraph");

        list.innerHTML = "";
        graph.innerHTML = "";

        if (!data.trends || data.trends.length === 0) {
            list.innerHTML = "<li>No trends found</li>";
            return;
        }

        data.trends.forEach((item, index) => {

            /* ================================
               SAFE CATEGORY COLOR
            ================================= */
            const catColor = categoryColors[item.category] || "#7c8ffc";


            /* ================================
               🔥 LIST SECTION
            ================================= */
            const li = document.createElement("li");
            li.style.lineHeight = "1.35";

            li.innerHTML = `
                <strong>${index + 1}. ${item.raw || item.topic}</strong>
                <span style="
                    background:${catColor}25;
                    color:${catColor};
                    padding:3px 8px;
                    border-radius:6px;
                    font-size:11px;
                    margin-left:6px;">
                    ${item.category}
                </span>
                <br>
                <small style="opacity:0.8">${item.momentum} • ${item.score}%</small>
            `;

            list.appendChild(li);


            /* ================================
               🔥 GRAPH SECTION (3D Glow Bars)
            ================================= */
            const wrap = document.createElement("div");
            wrap.className = "trend-item";

            const bar = document.createElement("div");
            bar.className = "trend-bar trend-bar-glow";
            bar.style.height = "0%";
            bar.style.background = `linear-gradient(180deg, ${catColor}, ${catColor}99)`;

            // Fix: Prevent over-animation crash
            requestAnimationFrame(() => {
                setTimeout(() => {
                    bar.style.height = Math.min(item.score, 100) + "%";
                }, 150);
            });

            const label = document.createElement("span");
            label.className = "trend-label";
            label.innerText = item.score + "%";

            wrap.appendChild(bar);
            wrap.appendChild(label);
            graph.appendChild(wrap);
        });

        graph.classList.add("graph-refresh");
        setTimeout(() => graph.classList.remove("graph-refresh"), 500);

    } catch (err) {
        console.log("Trend Error:", err);
    }
}


/* =========================================================
   REFRESH BUTTON
========================================================= */
document.getElementById("refreshTrendsBtn").onclick = () => {
    const g = document.getElementById("trendGraph");
    g.style.opacity = "0.4";
    setTimeout(() => (g.style.opacity = "1"), 250);

    loadLiveTrends();
};


/* =========================================================
   INITIAL + AUTO REFRESH
========================================================= */
loadLiveTrends();
setInterval(loadLiveTrends, 600000); // 10 minutes
