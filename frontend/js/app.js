import "../css/app.css";

const STORAGE_KEY = "king-movie-theme";
const DARK_CLASS = "dark";
const LIGHT_CLASS = "light";

const getSystemTheme = () => {
  if (!window.matchMedia) {
    return "dark";
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
};

const getStoredTheme = () => {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch {
    return null;
  }
};

const storeTheme = (theme) => {
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    // Theme still works for this page view when storage is unavailable.
  }
};

const applyTheme = (theme) => {
  const normalizedTheme = theme === "dark" ? "dark" : "light";
  document.documentElement.classList.toggle(DARK_CLASS, normalizedTheme === "dark");
  document.documentElement.classList.toggle(LIGHT_CLASS, normalizedTheme === "light");
  document.documentElement.dataset.theme = normalizedTheme;

  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.setAttribute("aria-pressed", String(normalizedTheme === "dark"));
    button.querySelector('[data-theme-icon="dark"]')?.classList.toggle("hidden", normalizedTheme === "dark");
    button.querySelector('[data-theme-icon="light"]')?.classList.toggle("hidden", normalizedTheme !== "dark");
  });
};

const initializeTheme = () => {
  applyTheme(getStoredTheme() || getSystemTheme());

  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const nextTheme = document.documentElement.classList.contains(DARK_CLASS) ? "light" : "dark";
      applyTheme(nextTheme);
      storeTheme(nextTheme);
    });
  });

  const systemThemeQuery = window.matchMedia?.("(prefers-color-scheme: dark)");

  systemThemeQuery?.addEventListener?.("change", (event) => {
    if (!getStoredTheme()) {
      applyTheme(event.matches ? "dark" : "light");
    }
  });

  window.addEventListener("storage", (event) => {
    if (event.key === STORAGE_KEY) {
      applyTheme(event.newValue || getSystemTheme());
    }
  });
};

initializeTheme();
