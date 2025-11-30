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
