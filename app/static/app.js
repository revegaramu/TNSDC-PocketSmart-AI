"use strict";

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => {
        const entities = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        };

        return entities[character];
    });
}

function formatCurrency(value) {
    const amount = Number(value);

    if (!Number.isFinite(amount)) {
        return "₹0.00";
    }

    return "₹" + amount.toLocaleString("en-IN", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function renderRecommendation(result) {
    const items = Array.isArray(result.items) ? result.items : [];
    const tips = Array.isArray(result.tips) ? result.tips : [];

    const itemHTML = items.map((item) => `
        <article class="recommendation-item">
            <div class="item-heading">
                <h3>${escapeHTML(item.name)}</h3>
                <strong>${formatCurrency(item.estimated_cost)}</strong>
            </div>
            <p>${escapeHTML(item.description)}</p>
        </article>
    `).join("");

    const tipsHTML = tips.length ? `
        <div class="tips-box">
            <h3>Smart tips</h3>
            <ul>
                ${tips.map((tip) => `<li>${escapeHTML(tip)}</li>`).join("")}
            </ul>
        </div>
    ` : "";

    const provider = result.ai_provider === "gemini"
        ? "AI-generated"
        : "Smart recommendations";

    return `
        <div class="result-card">
            <div class="result-topline">
                <span class="result-badge">✦ Your plan</span>
                <span class="provider-badge">${provider}</span>
            </div>

            <h2>${escapeHTML(result.title)}</h2>
            <p class="result-summary">${escapeHTML(result.summary)}</p>

            <div class="result-total">
                <span>Estimated total</span>
                <strong>${formatCurrency(result.estimated_total)}</strong>
            </div>

            <div class="recommendation-items">${itemHTML}</div>

            ${tipsHTML}

            <p class="disclaimer">
                Estimates are for planning purposes only. Verify actual
                prices, availability, and terms before purchasing.
            </p>

            <div class="result-actions">
                <a class="button button-secondary"
                   href="/result/${encodeURIComponent(result.id)}">
                    Open saved result
                </a>
                <button class="button" type="button"
                        onclick="window.print()">
                    Print plan
                </button>
            </div>
        </div>
    `;
}

async function parseResponse(response) {
    const contentType = response.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
        return response.json();
    }

    return {
        detail: await response.text()
    };
}

function getErrorMessage(data, response) {
    if (Array.isArray(data.detail)) {
        return data.detail
            .map((item) => item.msg || "Invalid input")
            .join(", ");
    }

    if (typeof data.detail === "string") {
        return data.detail;
    }

    return `Request failed (${response.status}). Please try again.`;
}

document.addEventListener("DOMContentLoaded", () => {
    const apiForms = document.querySelectorAll("[data-api-form]");

    apiForms.forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = form.querySelector('button[type="submit"]');
            const message = form.querySelector(".form-message");
            const originalText = button.textContent.trim();

            button.disabled = true;
            button.textContent = "Please wait...";
            message.textContent = "";

            try {
                const payload = Object.fromEntries(new FormData(form));

                const response = await fetch(form.action, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload),
                    credentials: "same-origin"
                });

                const data = await parseResponse(response);

                if (!response.ok) {
                    throw new Error(getErrorMessage(data, response));
                }

                window.location.href = data.redirect || "/dashboard";
            } catch (error) {
                message.textContent =
                    error.message || "Something went wrong.";
            } finally {
                button.disabled = false;
                button.textContent = originalText;
            }
        });
    });

    const recommendationForms = document.querySelectorAll(
        "[data-recommendation-form]"
    );

    recommendationForms.forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = form.querySelector('button[type="submit"]');
            const message = form.querySelector(".form-message");
            const resultContainer = document.getElementById(
                "recommendation-result"
            );

            const originalText = button.textContent.trim();

            button.disabled = true;
            button.textContent = "Creating your plan...";
            message.textContent = "";
            resultContainer.innerHTML = "";

            try {
                let response;

                if (form.hasAttribute("data-image-form")) {
                    response = await fetch(form.action, {
                        method: "POST",
                        body: new FormData(form),
                        credentials: "same-origin"
                    });
                } else {
                    const payload = Object.fromEntries(
                        new FormData(form)
                    );

                    if (payload.budget !== undefined) {
                        payload.budget = Number(payload.budget);
                    }

                    if (payload.guests !== undefined) {
                        payload.guests = Number(payload.guests);
                    }

                    response = await fetch(form.action, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(payload),
                        credentials: "same-origin"
                    });
                }

                const data = await parseResponse(response);

                if (!response.ok) {
                    throw new Error(getErrorMessage(data, response));
                }

                resultContainer.innerHTML = renderRecommendation(data);
                resultContainer.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            } catch (error) {
                message.textContent =
                    error.message || "Unable to create a recommendation.";
            } finally {
                button.disabled = false;
                button.textContent = originalText;
            }
        });
    });
});