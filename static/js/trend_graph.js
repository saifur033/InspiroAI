// trend_graph.js
// Renders a Chart.js line using provided labels/values/colors/points
function renderTrendChart(canvasId, labels, values, colors, points) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext('2d');
    const wrapper = canvas.parentElement || canvas.closest('.trend-chart-card');
    canvas.width = Math.max(320, wrapper.clientWidth || 600);
    canvas.height = canvas.clientHeight || 280;

    const gradient = ctx.createLinearGradient(0, 0, canvas.width, 0);
    gradient.addColorStop(0, 'rgba(140,112,255,0.95)');
    gradient.addColorStop(1, 'rgba(0,178,255,0.95)');

    const glowDataset = {
        label: 'Glow',
        data: values,
        borderColor: 'rgba(140,112,255,0.14)',
        borderWidth: 12,
        tension: 0.35,
        pointRadius: 0,
        fill: false,
        order: 1,
    };

    const mainDataset = {
        label: 'Viral Score',
        data: values,
        borderColor: gradient,
        backgroundColor: gradient,
        borderWidth: 4,
        tension: 0.4,
        pointRadius: 6,
        pointHoverRadius: 9,
        pointBackgroundColor: colors,
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        fill: false,
        order: 2,
    };

    if (window._trendChartInstance) {
        try { window._trendChartInstance.destroy(); } catch(e){}
    }

    window._trendChartInstance = new Chart(ctx, {
        type: 'line',
        data: { labels: labels, datasets: [glowDataset, mainDataset] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 900, easing: 'easeOutQuart' },
            plugins: {
                legend: { display: false },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        title: (items) => {
                            const i = items[0].dataIndex;
                            return labels[i];
                        },
                        label: (item) => {
                            const i = item.dataIndex;
                            const p = points[i] || {};
                            return [`Viral: ${p.viral_score}`, `Speed: ${p.speed}`, `Category: ${p.category}`];
                        }
                    }
                }
            },
            scales: {
                x: { display: false },
                y: {
                    beginAtZero: true,
                    max: 110,
                    ticks: { color: '#ddd' },
                    grid: { color: 'rgba(255,255,255,0.03)' }
                }
            },
            elements: { point: { hoverRadius: 9 } },
            onHover: (evt, elements) => {
                if (elements && elements.length) {
                    const idx = elements[0].index;
                    if (window.showTrendIntelCard) window.showTrendIntelCard(idx, points[idx]);
                }
            }
        }
    });

    return window._trendChartInstance;
}
