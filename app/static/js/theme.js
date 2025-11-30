document.addEventListener("DOMContentLoaded", () => {
  const html = document.documentElement;
  const btn = document.getElementById("theme-toggle");
  const icon = document.getElementById("theme-toggle-icon");
  const text = document.getElementById("theme-toggle-text");
  const STORAGE_KEY = "theme";

  function applyTheme(theme) {
    const isDark = theme === "dark";

    if (isDark) {
      html.classList.add("dark");
    } else {
      html.classList.remove("dark");
    }

    if (icon && text) {
      if (isDark) {
        icon.textContent = "🌙";
        text.textContent = "Mode Gelap";
      } else {
        icon.textContent = "☀";
        text.textContent = "Mode Terang";
      }
    }
  }

  const stored = localStorage.getItem(STORAGE_KEY);
  const prefersDark =
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;

  const initialTheme = stored || (prefersDark ? "dark" : "light");
  applyTheme(initialTheme);

  if (btn) {
    btn.addEventListener("click", () => {
      const isDark = html.classList.contains("dark");
      const nextTheme = isDark ? "light" : "dark";
      localStorage.setItem(STORAGE_KEY, nextTheme);
      applyTheme(nextTheme);
    });
  }
});

    // ====== NAV ACTIVE STATE ======
  const navLinks = document.querySelectorAll(".nav-link");

  function setActiveNavBySection(section) {
    navLinks.forEach((link) => {
      const sec = link.getAttribute("data-section");
      if (sec === section) {
        link.classList.add(
          "text-sky-600",
          "dark:text-sky-300",
          "border-b-2",
          "border-sky-500",
          "pb-1"
        );
      } else {
        link.classList.remove(
          "text-sky-600",
          "dark:text-sky-300",
          "border-b-2",
          "border-sky-500",
          "pb-1"
        );
      }
    });
  }

  // Saat pertama load halaman index: paksa posisi ke atas (beranda) dan tandai menu Beranda
  if (window.location.pathname === "/" || window.location.pathname === "{{ url_for('main.index') }}") {
    window.scrollTo({ top: 0, behavior: "instant" });
    setActiveNavBySection("beranda");
  }

  // Klik menu lain: beri tanda aktif
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      const sec = link.getAttribute("data-section");
      setActiveNavBySection(sec);
    });
  });

    // ====== BERSIHKAN FRAGMENT #... DARI URL SAAT LOAD ======
  if (window.location.hash) {
    // Hapus #fitur / #testimoni / #kontak dari URL tanpa reload
    history.replaceState(
      null,
      "",
      window.location.pathname + window.location.search
    );
  }


