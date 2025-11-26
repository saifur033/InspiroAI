// trend_loader.js
// Orchestrates fetching trend data, populating list, and rendering chart + intel

function updateClock() {
    const now = new Date();
    const elDate = document.getElementById("liveDate");
    const elDay = document.getElementById("liveDay");
    const elTime = document.getElementById("liveTime");
    if (elDate) elDate.innerText = now.toLocaleDateString();
    if (elDay) elDay.innerText = now.toLocaleString("en-US", { weekday: "long" });
    if (elTime) elTime.innerText = now.toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

const categoryColors = {
    Politics: "#ff4d4d",
    Cricket: "#07d27d",
    Tech: "#00b2ff",
    Crime: "#ff8c00",
    Campus: "#ae7bff",
    Accident: "#ff5733",
    Entertainment: "#ffd447",
    General: "#bdc3c7"
};

async function loadTrendsGraph() {
    try {
        const res = await fetch('/api/trends_graph');
        const data = await res.json();
        const labels = data.labels || [];
        const values = data.values || [];
        const colors = data.colors || [];
        const points = data.points || [];

        // populate left list
        const listEl = document.getElementById('trendList');
        if (listEl) {
            listEl.innerHTML = '';
            points.forEach((p, i) => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${i+1}. ${p.topic}</strong> <span style="background:${(categoryColors[p.category]||'#8a7cff')}22;color:${categoryColors[p.category]||'#8a7cff'};padding:3px 8px;border-radius:6px;font-size:11px;margin-left:6px;">${p.category}</span><br><small>${p.momentum||''} • ${p.viral_score}%</small>`;
                listEl.appendChild(li);
            });
        }

        // render chart
        if (typeof renderTrendChart === 'function') {
            renderTrendChart('trendChart', labels, values, colors, points);
        }

        // render intel box
        if (typeof renderTrendIntel === 'function') {
            renderTrendIntel(points);
        }

    } catch (err) {
        console.error('loadTrendsGraph error', err);
    }
}

// wire refresh button
const refreshBtn = document.getElementById('refreshTrendsBtn');
if (refreshBtn) refreshBtn.addEventListener('click', loadTrendsGraph);
// initial load
loadTrendsGraph();
// periodic refresh
setInterval(loadTrendsGraph, 600000);
