/* ===== Визитка Кирилла — интерактив ===== */
(function () {
    "use strict";

    /* ---------- 1. Эффект печатающегося текста ---------- */
    var phrases = [
        "Python Backend Developer",
        "14 лет — и уже пишу API",
        "Люблю чистый код и серверы",
        "Делаю Telegram-ботов"
    ];

    var typedEl = document.getElementById("typed");
    var phraseIndex = 0;
    var charIndex = 0;
    var deleting = false;

    function typeLoop() {
        if (!typedEl) return;

        var current = phrases[phraseIndex];
        typedEl.textContent = current.substring(0, charIndex);

        var delay = deleting ? 45 : 90;

        if (!deleting && charIndex === current.length) {
            deleting = true;
            delay = 1600;
        } else if (deleting && charIndex === 0) {
            deleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            delay = 400;
        } else {
            charIndex += deleting ? -1 : 1;
        }

        setTimeout(typeLoop, delay);
    }

    if (typedEl) {
        setTimeout(typeLoop, 500);
    }

    /* ---------- 2. Появление блоков при скролле ---------- */
    var revealEls = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry, i) {
                if (entry.isIntersecting) {
                    setTimeout(function () {
                        entry.target.classList.add("is-visible");
                    }, i * 60);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealEls.forEach(function (el) { observer.observe(el); });
    } else {
        revealEls.forEach(function (el) { el.classList.add("is-visible"); });
    }

    /* ---------- 3. Мобильное меню ---------- */
    var burger = document.getElementById("burger");
    var nav = document.getElementById("nav");

    function closeMenu() {
        if (!nav || !burger) return;
        nav.classList.remove("is-open");
        burger.classList.remove("is-open");
        burger.setAttribute("aria-label", "Открыть меню");
    }

    if (burger && nav) {
        burger.addEventListener("click", function () {
            var isOpen = nav.classList.toggle("is-open");
            burger.classList.toggle("is-open", isOpen);
            burger.setAttribute("aria-label", isOpen ? "Закрыть меню" : "Открыть меню");
        });

        nav.querySelectorAll(".nav__link").forEach(function (link) {
            link.addEventListener("click", closeMenu);
        });

        document.addEventListener("click", function (e) {
            if (!nav.contains(e.target) && !burger.contains(e.target)) {
                closeMenu();
            }
        });
    }

    /* ---------- 4. Тень у шапки при скролле ---------- */
    var header = document.querySelector(".header");

    function onScroll() {
        if (!header) return;
        header.classList.toggle("is-scrolled", window.scrollY > 12);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    /* ---------- 5. Активный пункт меню ---------- */
    var sections = Array.prototype.slice.call(document.querySelectorAll("main section[id]"));
    var navLinks = Array.prototype.slice.call(document.querySelectorAll(".nav__link"));

    if (sections.length && navLinks.length) {
        var navObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                navLinks.forEach(function (link) {
                    var target = link.getAttribute("href");
                    link.classList.toggle("is-active", target === "#" + entry.target.id);
                });
            });
        }, { rootMargin: "-45% 0px -50% 0px" });

        sections.forEach(function (section) { navObserver.observe(section); });
    }

    /* ---------- 6. Текущий год в подвале ---------- */
    var yearEl = document.getElementById("year");
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    /* ---------- 7. Фон с «частицами» на canvas ---------- */
    var canvas = document.getElementById("bg-canvas");

    if (canvas && canvas.getContext) {
        var ctx = canvas.getContext("2d");
        var particles = [];
        var W = 0, H = 0;
        var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        function resize() {
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
            var count = Math.min(90, Math.floor(W / 16));
            particles = [];
            for (var i = 0; i < count; i++) {
                particles.push({
                    x: Math.random() * W,
                    y: Math.random() * H,
                    vx: (Math.random() - 0.5) * 0.45,
                    vy: (Math.random() - 0.5) * 0.45,
                    r: Math.random() * 1.8 + 0.6
                });
            }
        }

        function draw() {
            ctx.clearRect(0, 0, W, H);

            for (var i = 0; i < particles.length; i++) {
                var p = particles[i];
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > W) p.vx *= -1;
                if (p.y < 0 || p.y > H) p.vy *= -1;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = "rgba(120, 165, 255, 0.7)";
                ctx.fill();

                for (var j = i + 1; j < particles.length; j++) {
                    var q = particles[j];
                    var dx = p.x - q.x;
                    var dy = p.y - q.y;
                    var dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 130) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(q.x, q.y);
                        ctx.strokeStyle = "rgba(79, 140, 255, " + (0.16 * (1 - dist / 130)) + ")";
                        ctx.lineWidth = 1;
                        ctx.stroke();
                    }
                }
            }

            if (!reducedMotion) requestAnimationFrame(draw);
        }

        resize();
        draw();
        window.addEventListener("resize", resize);
    }
})();

