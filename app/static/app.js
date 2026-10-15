/**
 * SaferPassForge - Frontend Controller
 * Interacts with FastAPI REST endpoints for password generation and audit logging.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const lengthSlider = document.getElementById("lengthSlider");
  const lengthValue = document.getElementById("lengthValue");
  const chkUpper = document.getElementById("chkUpper");
  const chkLower = document.getElementById("chkLower");
  const chkDigits = document.getElementById("chkDigits");
  const chkSymbols = document.getElementById("chkSymbols");
  const chkExcludeAmbiguous = document.getElementById("chkExcludeAmbiguous");
  const contextInput = document.getElementById("contextInput");
  const generateBtn = document.getElementById("generateBtn");
  const passwordDisplay = document.getElementById("passwordDisplay");
  const copyBtn = document.getElementById("copyBtn");
  const copyIcon = document.getElementById("copyIcon");
  const copiedTooltip = document.getElementById("copiedTooltip");
  const entropyBits = document.getElementById("entropyBits");
  const entropyBar = document.getElementById("entropyBar");
  const strengthBadge = document.getElementById("strengthBadge");
  const historyTableBody = document.getElementById("historyTableBody");
  const historyCountBadge = document.getElementById("historyCountBadge");
  const clearHistoryBtn = document.getElementById("clearHistoryBtn");

  // Sync length slider
  lengthSlider.addEventListener("input", (e) => {
    lengthValue.textContent = e.target.value;
  });

  // Strength Styling Helper
  function applyStrengthStyle(category, bits) {
    strengthBadge.textContent = category;
    entropyBits.textContent = `${bits.toFixed(2)} bits`;

    // Maximum visual baseline: 100 bits
    const percent = Math.min(100, Math.round((bits / 100) * 100));
    entropyBar.style.width = `${percent}%`;

    // Reset badge and bar classes
    strengthBadge.className = "text-xs px-2.5 py-1 rounded-full font-semibold border";
    entropyBar.className = "h-2 rounded-full transition-all duration-500";

    switch (category) {
      case "Weak":
        strengthBadge.classList.add("bg-red-500/20", "text-red-400", "border-red-500/30");
        entropyBar.classList.add("bg-red-500");
        break;
      case "Fair":
        strengthBadge.classList.add("bg-amber-500/20", "text-amber-400", "border-amber-500/30");
        entropyBar.classList.add("bg-amber-500");
        break;
      case "Strong":
        strengthBadge.classList.add("bg-emerald-500/20", "text-emerald-400", "border-emerald-500/30");
        entropyBar.classList.add("bg-emerald-500");
        break;
      case "Very Strong":
        strengthBadge.classList.add("bg-teal-500/20", "text-teal-300", "border-teal-500/30");
        entropyBar.classList.add("bg-teal-400");
        break;
      default:
        strengthBadge.classList.add("bg-slate-700", "text-slate-300", "border-slate-600");
        entropyBar.classList.add("bg-slate-500");
    }
  }

  // Generate Password Request
  async function generatePassword() {
    const payload = {
      length: parseInt(lengthSlider.value, 10),
      use_uppercase: chkUpper.checked,
      use_lowercase: chkLower.checked,
      use_digits: chkDigits.checked,
      use_symbols: chkSymbols.checked,
      exclude_ambiguous: chkExcludeAmbiguous.checked,
      context_label: contextInput.value.trim() || null,
    };

    if (!payload.use_uppercase && !payload.use_lowercase && !payload.use_digits && !payload.use_symbols) {
      alert("Selecione ao menos um grupo de caracteres (Maiúsculas, Minúsculas, Números ou Símbolos).");
      return;
    }

    try {
      generateBtn.disabled = true;
      generateBtn.classList.add("opacity-70", "cursor-not-allowed");

      const response = await fetch("/api/v1/passwords/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Erro ao gerar senha");
      }

      const data = await response.json();

      passwordDisplay.value = data.password;
      applyStrengthStyle(data.strength_category, data.entropy_bits);

      // Refresh history table
      await loadHistory();
    } catch (err) {
      alert(`Falha na geração: ${err.message}`);
    } finally {
      generateBtn.disabled = false;
      generateBtn.classList.remove("opacity-70", "cursor-not-allowed");
    }
  }

  // Copy to Clipboard with Feedback
  async function copyPassword() {
    const pwd = passwordDisplay.value;
    if (!pwd || pwd === "Clique em Gerar") return;

    try {
      await navigator.clipboard.writeText(pwd);
      copyIcon.classList.add("hidden");
      copiedTooltip.classList.remove("hidden");

      setTimeout(() => {
        copyIcon.classList.remove("hidden");
        copiedTooltip.classList.add("hidden");
      }, 2000);
    } catch (err) {
      console.error("Erro ao copiar para clipboard:", err);
    }
  }

  // Load Audit History
  async function loadHistory() {
    try {
      const response = await fetch("/api/v1/passwords/history?limit=15");
      if (!response.ok) return;

      const items = await response.json();
      historyCountBadge.textContent = items.length;

      if (!items || items.length === 0) {
        historyTableBody.innerHTML = `
          <tr>
            <td colspan="6" class="text-center py-8 text-slate-500 font-sans text-xs">
              Nenhum registro de auditoria no histórico local.
            </td>
          </tr>
        `;
        return;
      }

      historyTableBody.innerHTML = items
        .map((item) => {
          const date = new Date(item.created_at);
          const formattedDate = date.toLocaleDateString("pt-BR", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          });

          let badgeColor = "bg-slate-800 text-slate-300 border-slate-700";
          if (item.strength_category === "Weak") badgeColor = "bg-red-500/10 text-red-400 border-red-500/20";
          if (item.strength_category === "Fair") badgeColor = "bg-amber-500/10 text-amber-400 border-amber-500/20";
          if (item.strength_category === "Strong") badgeColor = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
          if (item.strength_category === "Very Strong") badgeColor = "bg-teal-500/10 text-teal-300 border-teal-500/20";

          return `
            <tr class="hover:bg-slate-800/40 transition-colors">
              <td class="py-2.5 px-3 text-slate-400">${formattedDate}</td>
              <td class="py-2.5 px-3 text-slate-200">${item.context_label || '<span class="text-slate-600 font-sans italic">Geral</span>'}</td>
              <td class="py-2.5 px-3 text-slate-300">${item.length}</td>
              <td class="py-2.5 px-3 text-emerald-400 font-semibold">${item.entropy_bits.toFixed(1)}</td>
              <td class="py-2.5 px-3">
                <span class="px-2 py-0.5 rounded text-[10px] font-semibold border ${badgeColor}">
                  ${item.strength_category}
                </span>
              </td>
              <td class="py-2.5 px-3 text-slate-400 tracking-wider">${item.masked_preview}</td>
            </tr>
          `;
        })
        .join("");
    } catch (err) {
      console.error("Falha ao carregar histórico:", err);
    }
  }

  // Clear History
  async function clearHistory() {
    if (!confirm("Tem certeza que deseja apagar todo o histórico de auditoria local?")) {
      return;
    }

    try {
      const response = await fetch("/api/v1/passwords/history", { method: "DELETE" });
      if (response.ok || response.status === 204) {
        await loadHistory();
      }
    } catch (err) {
      alert("Falha ao limpar histórico.");
    }
  }

  // Event Listeners
  generateBtn.addEventListener("click", generatePassword);
  copyBtn.addEventListener("click", copyPassword);
  clearHistoryBtn.addEventListener("click", clearHistory);

  // Initial Load
  loadHistory();
  generatePassword();
});

