(() => {
  const API_URL = ["127.0.0.1", "localhost"].includes(window.location.hostname)
    ? "http://127.0.0.1:8000"
    : "https://styl-style-trend-your-look-backend.onrender.com";
  const hasOccasionPage = !!document.getElementById("occasion-submit");
  const hasCompleteFitPage = !!document.getElementById("analyze-submit");

  if (!hasOccasionPage && !hasCompleteFitPage) return;

  const escapeHtml = (value) => String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");

  const currency = (value) => {
    const number = Number(value);
    return Number.isFinite(number) ? `INR ${number.toLocaleString("en-IN")}` : (value || "Price unavailable");
  };

  const setError = (node, message) => {
    if (!node) return;
    node.textContent = message || "";
    node.classList.toggle("hidden", !message);
  };

  const setLoading = (button, loading, idleText, loadingText) => {
    if (!button) return;
    button.disabled = loading;
    button.textContent = loading ? loadingText : idleText;
  };

  const getErrorMessage = async (response) => {
    try {
      const data = await response.json();
      return data?.detail || data?.message || `Request failed with status ${response.status}`;
    } catch (_) {
      return `Request failed with status ${response.status}`;
    }
  };

  const setSelected = (buttons, active, activeClasses, inactiveClasses) => {
    buttons.forEach((button) => {
      const on = button === active;
      activeClasses.forEach((name) => button.classList.toggle(name, on));
      inactiveClasses.forEach((name) => button.classList.toggle(name, !on));
    });
  };

  const productCard = (product) => {
    const image = product.thumbnail
      ? `<img alt="${escapeHtml(product.title || "Product")}" class="h-full w-full object-cover" src="${escapeHtml(product.thumbnail)}"/>`
      : `<div class="flex h-full w-full items-center justify-center bg-surface-container text-xs uppercase tracking-[0.2em] text-secondary">No Image</div>`;
    const cta = product.link
      ? `<a class="mt-4 inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-widest text-primary" href="${escapeHtml(product.link)}" rel="noreferrer" target="_blank">Shop Now <span class="material-symbols-outlined text-xs">arrow_forward</span></a>`
      : `<span class="mt-4 inline-flex text-[10px] font-bold uppercase tracking-widest text-secondary">Link unavailable</span>`;
    return `
      <article class="min-w-[220px] rounded-2xl border border-outline-variant/10 bg-white p-4 shadow-sm">
        <div class="mb-4 aspect-[4/5] overflow-hidden rounded-xl bg-surface-container">${image}</div>
        <div class="mb-2 flex items-start justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold">${escapeHtml(product.title || "Product")}</h4>
            <p class="text-[10px] uppercase tracking-widest text-secondary">${escapeHtml(product.source || "Store")}</p>
          </div>
          <span class="text-sm font-extrabold">${escapeHtml(product.price || "Price unavailable")}</span>
        </div>
        ${cta}
      </article>`;
  };

  const renderOccasionOutfit = (items) => {
    if (!items.length) {
      return `<div class="rounded-2xl bg-surface-container p-8 text-center text-secondary">No outfit items were returned from the backend.</div>`;
    }
    return items.map((item) => `
      <section class="rounded-2xl bg-surface-container p-6 md:p-8">
        <div class="mb-6 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <span class="mb-2 block text-[10px] font-bold uppercase tracking-widest text-primary">${escapeHtml(item.item_type || "Item")}</span>
            <h3 class="font-headline text-3xl italic">${escapeHtml(item.description || "Recommendation")}</h3>
          </div>
          <span class="text-sm font-bold uppercase tracking-widest text-secondary">Target ${currency(item.estimated_price)}</span>
        </div>
        <p class="mb-6 text-secondary">${escapeHtml(item.reason || "")}</p>
        <div class="flex gap-4 overflow-x-auto pb-2">
          ${Array.isArray(item.products) && item.products.length ? item.products.map(productCard).join("") : `<div class="rounded-2xl bg-white px-6 py-8 text-sm text-secondary">No products returned for this item.</div>`}
        </div>
      </section>
    `).join("");
  };

  const renderAnalysisDetails = (vision) => {
    const blocks = [];
    if (vision.shirt) {
      blocks.push(`
        <div class="rounded-2xl bg-surface-container p-4">
          <div class="mb-2 text-[10px] font-bold uppercase tracking-widest text-primary">Shirt</div>
          <p class="text-sm text-secondary">Color: <span class="font-bold text-on-background">${escapeHtml(vision.shirt.color || "unknown")}</span></p>
          <p class="text-sm text-secondary">Style: <span class="font-bold text-on-background">${escapeHtml(vision.shirt.style || "unknown")}</span></p>
          <p class="text-sm text-secondary">Fit: <span class="font-bold text-on-background">${escapeHtml(vision.shirt.fit || "unknown")}</span></p>
        </div>`);
    }
    if (vision.pants) {
      blocks.push(`
        <div class="rounded-2xl bg-surface-container p-4">
          <div class="mb-2 text-[10px] font-bold uppercase tracking-widest text-primary">Pants</div>
          <p class="text-sm text-secondary">Color: <span class="font-bold text-on-background">${escapeHtml(vision.pants.color || "unknown")}</span></p>
          <p class="text-sm text-secondary">Style: <span class="font-bold text-on-background">${escapeHtml(vision.pants.style || "unknown")}</span></p>
          <p class="text-sm text-secondary">Fit: <span class="font-bold text-on-background">${escapeHtml(vision.pants.fit || "unknown")}</span></p>
        </div>`);
    }
    blocks.push(`<p class="text-secondary">Overall vibe: <span class="font-bold text-primary">${escapeHtml(vision.overall_vibe || "unknown")}</span></p>`);
    return blocks.join("");
  };

  const renderAnalyzeGroups = (groups) => {
    const entries = Object.entries(groups).filter(([, items]) => Array.isArray(items) && items.length);
    if (!entries.length) {
      return `<div class="rounded-2xl bg-surface-container p-8 text-center text-secondary">No recommendations came back from the backend.</div>`;
    }
    return entries.map(([category, items]) => `
      <section class="rounded-2xl bg-surface-container p-6">
        <div class="mb-4 flex items-center justify-between">
          <h4 class="font-headline text-2xl italic">${escapeHtml(category)}</h4>
          <span class="text-[10px] font-bold uppercase tracking-widest text-secondary">${items.length} suggestions</span>
        </div>
        <div class="space-y-6">
          ${items.map((item) => `
            <div class="rounded-2xl bg-white p-5 shadow-sm">
              <h5 class="text-base font-bold">${escapeHtml(item.item || "Recommendation")}</h5>
              <p class="mb-4 mt-1 text-sm text-secondary">${escapeHtml(item.reason || "")}</p>
              <div class="flex gap-4 overflow-x-auto pb-2">
                ${Array.isArray(item.products) && item.products.length ? item.products.map(productCard).join("") : `<div class="rounded-2xl bg-surface-container px-6 py-8 text-sm text-secondary">No products returned for this suggestion.</div>`}
              </div>
            </div>
          `).join("")}
        </div>
      </section>
    `).join("");
  };

  const scoreMeta = (score) => {
    if (score >= 7) return { color: "#2d6a4f", label: "Great choice!" };
    if (score >= 4) return { color: "#9d6b2e", label: "Could work" };
    return { color: "#9d3d2e", label: "Not ideal" };
  };

  const initOccasionPage = () => {
    const occasionButtons = [...document.querySelectorAll(".occasion-pill")];
    const styleButtons = [...document.querySelectorAll(".style-pill")];
    const genderButtons = [...document.querySelectorAll(".gender-pill")];
    const slider = document.getElementById("budget-slider");
    const budgetValue = document.getElementById("budget-value");
    const submit = document.getElementById("occasion-submit");
    const error = document.getElementById("occasion-error");
    const meta = document.getElementById("occasion-meta");
    const results = document.getElementById("occasion-results");

    let occasion = occasionButtons.find((button) => button.classList.contains("bg-primary"))?.dataset.value || "Summer Soiree";
    let style = styleButtons.find((button) => button.classList.contains("border-primary"))?.dataset.value || "Minimalist";
    let gender = genderButtons.find((button) => button.classList.contains("bg-white"))?.dataset.value || "feminine";

    budgetValue.textContent = currency(slider.value);
    slider.addEventListener("input", () => {
      budgetValue.textContent = currency(slider.value);
    });

    occasionButtons.forEach((button) => button.addEventListener("click", () => {
      occasion = button.dataset.value;
      setSelected(occasionButtons, button, ["bg-primary", "text-on-primary", "shadow-lg", "shadow-primary/20"], ["border", "border-outline-variant", "text-secondary"]);
    }));

    styleButtons.forEach((button) => button.addEventListener("click", () => {
      style = button.dataset.value;
      setSelected(styleButtons, button, ["border-primary", "bg-white", "shadow-xl", "shadow-primary/5"], ["border-outline-variant"]);
      styleButtons.forEach((item) => item.querySelector("span")?.classList.toggle("text-primary", item === button));
    }));

    genderButtons.forEach((button) => button.addEventListener("click", () => {
      gender = button.dataset.value;
      setSelected(genderButtons, button, ["bg-white", "shadow-sm"], []);
    }));

    submit.addEventListener("click", async () => {
      setError(error, "");
      setLoading(submit, true, "Build My Outfit", "Building...");
      meta.textContent = "Fetching outfit plan";

      const form = new FormData();
      form.append("occasion", occasion);
      form.append("style", style);
      form.append("gender", gender);
      form.append("budget_min", String(Number(slider.min)));
      form.append("budget_max", String(Number(slider.value)));

      try {
        const response = await fetch(`${API_URL}/occasion`, {
          method: "POST",
          body: form
        });
        if (!response.ok) {
          const message = await getErrorMessage(response);
          console.error("Occasion request failed:", response.status, message);
          throw new Error(message);
        }
        const data = await response.json();
        if (Array.isArray(data.warnings) && data.warnings.length) {
          setError(error, data.warnings[0]);
        }
        meta.textContent = `${data.occasion} • ${data.style} • ${data.budget}`;
        results.innerHTML = renderOccasionOutfit(Array.isArray(data.outfit) ? data.outfit : []);
      } catch (err) {
        console.error("Occasion fetch error:", err);
        meta.textContent = "Request failed";
        results.innerHTML = `<div class="rounded-2xl bg-error-container p-8 text-center text-on-error-container">Unable to build outfit recommendations right now.</div>`;
        setError(error, err.message || "Request failed.");
      } finally {
        setLoading(submit, false, "Build My Outfit", "Building...");
      }
    });
  };

  const initDropzone = (input, preview, placeholder, zone) => {
    const updatePreview = (file) => {
      if (!file) return;
      preview.src = URL.createObjectURL(file);
      preview.classList.remove("hidden");
      placeholder.classList.add("hidden");
      zone.classList.add("border-primary");
    };
    input.addEventListener("change", () => updatePreview(input.files?.[0]));
    ["dragenter", "dragover"].forEach((name) => zone.addEventListener(name, (event) => {
      event.preventDefault();
      zone.classList.add("border-primary");
    }));
    ["dragleave", "drop"].forEach((name) => zone.addEventListener(name, (event) => {
      event.preventDefault();
    }));
    zone.addEventListener("drop", (event) => {
      const [file] = event.dataTransfer?.files || [];
      if (!file) return;
      const transfer = new DataTransfer();
      transfer.items.add(file);
      input.files = transfer.files;
      updatePreview(file);
    });
  };

  const initCompleteFitPage = () => {
    const occasionButtons = [...document.querySelectorAll(".analyze-occasion-pill")];
    const genderButtons = [...document.querySelectorAll(".analyze-gender-pill")];
    const submit = document.getElementById("analyze-submit");
    const error = document.getElementById("analyze-error");
    const meta = document.getElementById("analyze-meta");
    const analysisCard = document.getElementById("analysisCard");
    const analysisEmoji = document.getElementById("analysis-emoji");
    const analysisVibe = document.getElementById("analysis-vibe");
    const analysisScoreBadge = document.getElementById("analysis-score-badge");
    const analysisVerdict = document.getElementById("analysis-verdict");
    const analysisDetails = document.getElementById("analysis-details");
    const analysisWarningBanner = document.getElementById("analysis-warning-banner");
    const results = document.getElementById("analyze-results");
    const shirtInput = document.getElementById("shirt-input");
    const shirtPreview = document.getElementById("shirt-preview");
    const shirtPlaceholder = document.getElementById("shirt-placeholder");
    const shirtZone = document.getElementById("shirt-dropzone");
    const pantsInput = document.getElementById("pants-input");
    const pantsPreview = document.getElementById("pants-preview");
    const pantsPlaceholder = document.getElementById("pants-placeholder");
    const pantsZone = document.getElementById("pants-dropzone");

    initDropzone(shirtInput, shirtPreview, shirtPlaceholder, shirtZone);
    initDropzone(pantsInput, pantsPreview, pantsPlaceholder, pantsZone);

    let occasion = occasionButtons.find((button) => button.classList.contains("bg-primary"))?.dataset.value || "Date";
    let gender = genderButtons.find((button) => button.classList.contains("bg-white"))?.dataset.value || "feminine";
    occasionButtons.forEach((button) => button.addEventListener("click", () => {
      occasion = button.dataset.value;
      setSelected(occasionButtons, button, ["bg-primary", "text-on-primary", "shadow-lg", "shadow-primary/20"], ["bg-surface-container-high", "text-secondary"]);
    }));
    genderButtons.forEach((button) => button.addEventListener("click", () => {
      gender = button.dataset.value;
      setSelected(genderButtons, button, ["bg-white", "shadow-sm"], []);
    }));

    submit.addEventListener("click", async () => {
      setError(error, "");
      if (!shirtInput.files?.[0] && !pantsInput.files?.[0]) {
        setError(error, "Upload at least one image before analyzing.");
        return;
      }

      setLoading(submit, true, "Analyze My Fit", "Analyzing...");
      meta.textContent = "Running vision analysis";
      analysisEmoji.textContent = "⏳";
      analysisVibe.textContent = "Analyzing...";
      analysisScoreBadge.textContent = "Scoring...";
      analysisScoreBadge.style.backgroundColor = "#9d6b2e";
      analysisVerdict.textContent = "Reading the silhouette and checking if the outfit matches the occasion.";
      analysisDetails.innerHTML = `<p class="text-secondary">Uploading images and waiting for the backend response.</p>`;
      analysisWarningBanner.classList.add("hidden");

      const form = new FormData();
      form.append("occasion", occasion);
      form.append("gender", gender);
      if (shirtInput.files?.[0]) form.append("shirt", shirtInput.files[0]);
      if (pantsInput.files?.[0]) form.append("pants", pantsInput.files[0]);

      try {
        const response = await fetch(`${API_URL}/analyze`, {
          method: "POST",
          body: form
        });
        if (!response.ok) {
          const message = await getErrorMessage(response);
          console.error("Analyze request failed:", response.status, message);
          throw new Error(message);
        }
        const data = await response.json();
        const vision = data.vision || {};
        const recommendationGroups = data.recommendations?.recommendations || {};
        if (Array.isArray(data.warnings) && data.warnings.length) {
          setError(error, data.warnings[0]);
        }

        analysisEmoji.textContent = vision.vibe_emoji || "✨";
        analysisVibe.textContent = vision.overall_vibe || "unknown";
        const score = Number(vision.occasion_match_score ?? 0);
        const scoreInfo = scoreMeta(score);
        analysisScoreBadge.textContent = `${scoreInfo.label} • ${Number.isFinite(score) ? score.toFixed(1) : "0.0"}/10`;
        analysisScoreBadge.style.backgroundColor = scoreInfo.color;
        analysisVerdict.textContent = vision.stylist_verdict || "This is the honest stylist take on your outfit.";
        analysisDetails.innerHTML = renderAnalysisDetails(vision);
        if (score < 4) {
          analysisWarningBanner.textContent = `This outfit may not be the best choice for ${vision.occasion || occasion}. Here's what we recommend instead:`;
          analysisWarningBanner.classList.remove("hidden");
        } else {
          analysisWarningBanner.classList.add("hidden");
        }
        results.innerHTML = renderAnalyzeGroups(recommendationGroups);
        meta.textContent = `${Object.keys(recommendationGroups).length} recommendation groups`;
      } catch (err) {
        console.error("Analyze fetch error:", err);
        meta.textContent = "Request failed";
        analysisVibe.textContent = "Unavailable";
        analysisEmoji.textContent = "⚠️";
        analysisScoreBadge.textContent = "Unavailable";
        analysisScoreBadge.style.backgroundColor = "#9d3d2e";
        analysisVerdict.textContent = "We could not complete the stylist read this time.";
        analysisDetails.innerHTML = `<p class="text-on-error-container">The backend request failed before analysis could complete.</p>`;
        analysisWarningBanner.classList.add("hidden");
        results.innerHTML = `<div class="rounded-2xl bg-error-container p-8 text-center text-on-error-container">Unable to load product recommendations right now.</div>`;
        setError(error, err.message || "Request failed.");
      } finally {
        setLoading(submit, false, "Analyze My Fit", "Analyzing...");
      }
    });
  };

  if (hasOccasionPage) initOccasionPage();
  if (hasCompleteFitPage) initCompleteFitPage();
})();
