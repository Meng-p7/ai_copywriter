(function () {
    const app = window.AIApp || {};

    app.state = app.state || {
        currentScheme: "",
        USER_ID: "local_user_fixed_id_2026",
        userName: "创作者",
        currentGenerateParams: null,
        historyData: [],
        videoQuota: null
    };

    app.getEl = function getEl(id) {
        return document.getElementById(id);
    };

    app.escapeHtml = function escapeHtml(value) {
        return String(value || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/\"/g, "&quot;")
            .replace(/'/g, "&#39;");
    };

    app.showToast = function showToast(message) {
        const toast = app.getEl("toast");
        if (!toast) return;

        toast.textContent = message;
        toast.classList.add("show");
        setTimeout(function () {
            toast.classList.remove("show");
        }, 3000);
    };

    app.openModal = function openModal(modalId, onBackdropClick) {
        const modal = app.getEl(modalId);
        if (!modal) return;

        modal.classList.add("show");
        modal.onclick = function (event) {
            if (event.target === modal && typeof onBackdropClick === "function") {
                onBackdropClick();
            }
        };
    };

    app.closeModal = function closeModal(modalId) {
        const modal = app.getEl(modalId);
        if (!modal) return;

        modal.classList.remove("show");
        modal.onclick = null;
    };

    app.bindGlobal = function bindGlobal(handlers) {
        Object.keys(handlers).forEach(function (key) {
            window[key] = handlers[key];
        });
    };

    window.AIApp = app;
})();
