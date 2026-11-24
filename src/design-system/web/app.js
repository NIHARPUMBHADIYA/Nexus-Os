// NEXUS OS — Design System Studio Interactive Controller

const THEMES = [
  { id: "midnight", name: "Midnight" },
  { id: "nord", name: "Nord" },
  { id: "dracula", name: "Dracula" },
  { id: "catppuccin", name: "Catppuccin" },
  { id: "tokyo-night", name: "Tokyo Night" },
  { id: "terminal-green", name: "Terminal Green" },
  { id: "paper-light", name: "Paper Light" },
  { id: "amoled", name: "AMOLED" },
  { id: "deep-space", name: "Deep Space" }
];

const ACCENTS = [
  { name: "Indigo", color: "#6366F1" },
  { name: "Emerald", color: "#10B981" },
  { name: "Amber", color: "#F59E0B" },
  { name: "Crimson", color: "#EF4444" },
  { name: "Cyan", color: "#06B6D4" },
  { name: "Violet", color: "#8B5CF6" },
  { name: "Rose", color: "#F43F5E" }
];

document.addEventListener("DOMContentLoaded", () => {
  const themePillsContainer = document.getElementById("theme-pills");
  const accentContainer = document.getElementById("accent-palette");
  const navList = document.getElementById("nav-list");
  const reducedMotionToggle = document.getElementById("reduced-motion-toggle");
  const tokenGrid = document.getElementById("token-grid");
  const sampleModal = document.getElementById("sample-modal");

  // 1. Render Theme Switcher Pills
  THEMES.forEach((theme, index) => {
    const pill = document.createElement("button");
    pill.className = `theme-pill ${index === 0 ? "active" : ""}`;
    pill.textContent = theme.name;
    pill.addEventListener("click", () => {
      document.body.setAttribute("data-theme", theme.id);
      document.querySelectorAll(".theme-pill").forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      updateTokenCards();
    });
    themePillsContainer.appendChild(pill);
  });

  // 2. Render Accent Palette
  ACCENTS.forEach(accent => {
    const dot = document.createElement("div");
    dot.className = "accent-dot";
    dot.style.background = accent.color;
    dot.title = accent.name;
    dot.addEventListener("click", () => {
      document.documentElement.style.setProperty("--color-accent", accent.color);
      document.querySelectorAll(".accent-dot").forEach(d => d.classList.remove("active"));
      dot.classList.add("active");
      updateTokenCards();
    });
    accentContainer.appendChild(dot);
  });

  // 3. Render Navigation Switching
  navList.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
      const targetSection = item.getAttribute("data-section");
      navList.querySelectorAll(".nav-item").forEach(i => i.classList.remove("active"));
      item.classList.add("active");

      document.querySelectorAll(".section-pane").forEach(pane => {
        pane.classList.remove("active");
      });
      const activePane = document.getElementById(`section-${targetSection}`);
      if (activePane) activePane.classList.add("active");
    });
  });

  // 4. Reduced Motion
  reducedMotionToggle.addEventListener("change", (e) => {
    if (e.target.checked) {
      document.body.classList.add("reduced-motion");
    } else {
      document.body.classList.remove("reduced-motion");
    }
  });

  // 5. Render Semantic Token Cards
  const tokens = [
    { label: "Background", token: "--color-bg" },
    { label: "Secondary Bg", token: "--color-sec-bg" },
    { label: "Surface", token: "--color-surface" },
    { label: "Elevated Surface", token: "--color-elevated" },
    { label: "Accent", token: "--color-accent" },
    { label: "Success", token: "--color-success" },
    { label: "Warning", token: "--color-warning" },
    { label: "Error", token: "--color-error" }
  ];

  function updateTokenCards() {
    tokenGrid.innerHTML = "";
    const computed = getComputedStyle(document.body);
    tokens.forEach(t => {
      const card = document.createElement("div");
      card.className = "token-card";
      const val = computed.getPropertyValue(t.token).trim();
      card.style.background = val;

      const label = document.createElement("span");
      label.className = "token-card-label";
      label.textContent = t.label;

      const hex = document.createElement("span");
      hex.className = "token-card-hex";
      hex.textContent = val;

      // Ensure legible text contrast
      label.style.color = (t.label === "Background" || t.label === "Secondary Bg" || t.label === "Surface" || t.label === "Elevated Surface") 
        ? computed.getPropertyValue("--color-text-primary").trim()
        : "#FFFFFF";
      hex.style.color = label.style.color;

      card.appendChild(label);
      card.appendChild(hex);
      tokenGrid.appendChild(card);
    });
  }

  updateTokenCards();

  // 6. Modal Dialog triggers
  document.getElementById("open-dialog-btn").addEventListener("click", () => {
    sampleModal.classList.add("open");
  });
  document.getElementById("close-dialog-btn").addEventListener("click", () => {
    sampleModal.classList.remove("open");
  });
  document.getElementById("confirm-dialog-btn").addEventListener("click", () => {
    sampleModal.classList.remove("open");
  });
});
