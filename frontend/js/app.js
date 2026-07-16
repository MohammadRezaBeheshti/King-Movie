import "../css/app.css";
import EmblaCarousel from "embla-carousel";

const STORAGE_KEY = "king-movie-theme";
const DARK_CLASS = "dark";
const LIGHT_CLASS = "light";

const getSystemTheme = () => {
  if (!window.matchMedia) {
    return "dark";
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
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
  document.documentElement.classList.toggle(
    DARK_CLASS,
    normalizedTheme === "dark",
  );
  document.documentElement.classList.toggle(
    LIGHT_CLASS,
    normalizedTheme === "light",
  );
  document.documentElement.dataset.theme = normalizedTheme;

  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.setAttribute("aria-pressed", String(normalizedTheme === "dark"));
    button
      .querySelector('[data-theme-icon="dark"]')
      ?.classList.toggle("hidden", normalizedTheme === "dark");
    button
      .querySelector('[data-theme-icon="light"]')
      ?.classList.toggle("hidden", normalizedTheme !== "dark");
  });
};

const initializeTheme = () => {
  applyTheme(getStoredTheme() || getSystemTheme());

  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const nextTheme = document.documentElement.classList.contains(DARK_CLASS)
        ? "light"
        : "dark";
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

const createDotButtons = (emblaApi, dotsNode) => {
  if (!dotsNode) {
    return;
  }

  const scrollSnaps = emblaApi.scrollSnapList();
  dotsNode.innerHTML = scrollSnaps
    .map(
      (_, index) =>
        `<button class="embla__dot" type="button" aria-label="رفتن به اسلاید ${index + 1}"></button>`,
    )
    .join("");

  const dotNodes = Array.from(dotsNode.querySelectorAll(".embla__dot"));

  dotNodes.forEach((dotNode, index) => {
    dotNode.addEventListener("click", () => emblaApi.scrollTo(index));
  });

  const toggleActiveDot = () => {
    const selectedIndex = emblaApi.selectedScrollSnap();
    dotNodes.forEach((dotNode, index) => {
      dotNode.classList.toggle("embla__dot--selected", index === selectedIndex);
    });
  };

  toggleActiveDot();
  emblaApi.on("select", toggleActiveDot);
  emblaApi.on("reInit", toggleActiveDot);
};

const bindArrowButtons = (emblaApi, rootNode) => {
  const prevButton = rootNode.querySelector(".embla__button--prev");
  const nextButton = rootNode.querySelector(".embla__button--next");

  if (!prevButton || !nextButton) {
    return;
  }

  prevButton.addEventListener("click", () => emblaApi.scrollPrev());
  nextButton.addEventListener("click", () => emblaApi.scrollNext());

  const toggleButtons = () => {
    prevButton.disabled = !emblaApi.canScrollPrev();
    nextButton.disabled = !emblaApi.canScrollNext();
  };

  toggleButtons();
  emblaApi.on("select", toggleButtons);
  emblaApi.on("reInit", toggleButtons);
};

const initializeHeroSlider = () => {
  document.querySelectorAll("[data-hero-slider]").forEach((sliderNode) => {
    const viewportNode = sliderNode.querySelector(
      "[data-hero-slider-viewport]",
    );
    if (!viewportNode) {
      return;
    }

    const slideNodes = sliderNode.querySelectorAll(".embla__slide");
    if (!slideNodes.length) {
      return;
    }

    const emblaApi = EmblaCarousel(viewportNode, {
      loop: slideNodes.length > 1,
      align: "start",
      direction: "rtl",
    });

    bindArrowButtons(emblaApi, sliderNode);
    createDotButtons(emblaApi, sliderNode.querySelector(".embla__dots"));
  });
};

const initializeMediaRowSliders = () => {
  document.querySelectorAll("[data-media-row-slider]").forEach((sliderNode) => {
    const viewportNode = sliderNode.querySelector("[data-media-row-viewport]");
    if (!viewportNode) return;

    const slideNodes = sliderNode.querySelectorAll(".embla__slide");
    if (!slideNodes.length) return;

    const emblaApi = EmblaCarousel(viewportNode, {
      loop: false,
      align: "start",
      direction: "rtl",
      slidesPerView: 2,
      breakpoints: {
        "(min-width: 768px)": { slidesPerView: 2.5 },
        "(min-width: 1024px)": { slidesPerView: 6 },
      },
    });

    const sectionNode = sliderNode.closest("section");
    if (sectionNode) {
      bindArrowButtons(emblaApi, sectionNode);
    }
  });
};

const initializeSearchFormAccordion = () => {
  document.querySelectorAll("[data-search-form]").forEach((formNode) => {
    const extraNode = formNode.querySelector("[data-search-form-extra]");
    const toggleButton = formNode.querySelector("[data-search-form-toggle]");
    const labelNode = formNode.querySelector("[data-search-form-toggle-label]");
    const iconNode = formNode.querySelector("[data-search-form-toggle-icon]");

    if (!extraNode || !toggleButton) {
      return;
    }

    const setExpanded = (expanded) => {
      extraNode.classList.toggle("hidden", !expanded);
      toggleButton.setAttribute("aria-expanded", String(expanded));

      if (labelNode) {
        labelNode.textContent = expanded ? "نمایش کمتر" : "نمایش بیشتر";
      }

      if (iconNode) {
        iconNode.textContent = expanded ? "−" : "+";
      }
    };

    setExpanded(false);

    toggleButton.addEventListener("click", () => {
      const isExpanded = toggleButton.getAttribute("aria-expanded") === "true";
      setExpanded(!isExpanded);
    });
  });
};

initializeTheme();
initializeHeroSlider();
initializeMediaRowSliders();
initializeSearchFormAccordion();
