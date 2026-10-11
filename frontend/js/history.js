const historyList = document.getElementById("historyList");

function formatDate(isoString) {
  const d = new Date(isoString);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" }) +
    " · " + d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}

function renderAnalysisDetail(item) {
  return item.detail;
}

function renderInterviewDetail(item) {
  try {
    const history = JSON.parse(item.detail);
    return history.map((h, i) => {
      let block = `Q${i + 1}: ${h.question}\n`;
      if (h.answer) block += `\nYour answer: ${h.answer}\n`;
      if (h.feedback) block += `\n${h.feedback}\n`;
      return block;
    }).join("\n" + "-".repeat(30) + "\n");
  } catch {
    return "Could not load interview detail.";
  }
}

async function loadHistory() {
  try {
    const response = await fetch("/api/history");
    const data = await response.json();

    if (!data.items || data.items.length === 0) {
      historyList.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">📂</div>
          <p>Nothing here yet. Analyze a resume or run a mock interview to start building your history.</p>
        </div>`;
      return;
    }

    historyList.innerHTML = "";

    data.items.forEach((item) => {
      const el = document.createElement("div");
      el.className = "history-item";

      const scoreLabel = item.score !== null && item.score !== undefined
        ? `${item.score}${item.type === "interview" ? " avg" : ""} / 10`
        : "—";

      el.innerHTML = `
        <div class="history-item-top">
          <div>
            <span class="history-type-tag">${item.type === "analysis" ? "Resume analysis" : "Mock interview"}</span>
            <div class="history-item-title">${item.title}</div>
            <div class="history-item-meta">${formatDate(item.created_at)}</div>
          </div>
          <span class="history-badge">${scoreLabel}</span>
        </div>
        <div class="history-detail"></div>
      `;

      el.addEventListener("click", () => {
        const wasExpanded = el.classList.contains("expanded");
        document.querySelectorAll(".history-item.expanded").forEach((e) => e.classList.remove("expanded"));

        if (!wasExpanded) {
          const detailEl = el.querySelector(".history-detail");
          if (!detailEl.textContent) {
            detailEl.textContent = item.type === "analysis"
              ? renderAnalysisDetail(item)
              : renderInterviewDetail(item);
          }
          el.classList.add("expanded");
        }
      });

      historyList.appendChild(el);
    });
  } catch (err) {
    historyList.innerHTML = `<p class="card-sub">Could not load history: ${err.message}</p>`;
  }
}

loadHistory();
