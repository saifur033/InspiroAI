/* =========================================================
   InspiroAI — Neon 3D Animation Pack
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    // 3D Hover Depth
    document.querySelectorAll(".hover-3d").forEach(card => {
        card.addEventListener("mousemove", e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            card.style.transform = `rotateY(${x / 40}deg) rotateX(${-y / 40}deg)`;
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "rotateY(0deg) rotateX(0deg)";
        });
    });

    // Smooth fade-in animation
    document.querySelectorAll(".fade-in").forEach(el => {
        el.style.opacity = 0;
        setTimeout(() => {
            el.style.transition = "0.8s ease";
            el.style.opacity = 1;
        }, 50);
    });
});
