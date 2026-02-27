(function () {
    const app = window.AIApp;
    const state = app.state;

    function showNicknameModal() {
        app.openModal("nicknameModal", closeNicknameModal);
        app.getEl("nicknameInput").value = state.userName;
    }

    function closeNicknameModal() {
        app.closeModal("nicknameModal");
    }

    function saveNickname() {
        const newName = app.getEl("nicknameInput").value.trim();
        if (!newName) return;

        state.userName = newName;
        localStorage.setItem("ai_copywriter_user_name", newName);
        app.getEl("userNameDisplay").textContent = newName;
        closeNicknameModal();
        app.showToast("昵称已更新");
    }

    function renderRecordList(records, emptyText, onViewAction, timeLabel) {
        if (!records || records.length === 0) {
            return '<p class="empty-tip">' + app.escapeHtml(emptyText) + "</p>";
        }

        return records
            .map(function (item, index) {
                const scene = app.escapeHtml(item.scene || "");
                const summary = app.escapeHtml(item.key_info || item.keyInfo || "");
                const style = app.escapeHtml(item.style || "默认");
                const duration = app.escapeHtml(item.duration || "默认");
                const timestamp = item.create_time
                    ? app.escapeHtml(item.create_time)
                    : app.escapeHtml(new Date(item.timestamp).toLocaleString());

                return (
                    '<div class="record-item">' +
                    '<div class="record-title">' + scene + "</div>" +
                    '<div class="record-desc">' + summary + "</div>" +
                    '<div class="record-meta">风格: ' + style + " | 时长: " + duration + "</div>" +
                    '<div class="record-time">' + app.escapeHtml(timeLabel) + ": " + timestamp + "</div>" +
                    '<button class="record-btn" onclick="' + onViewAction + "(" + index + ')">查看详情</button>' +
                    "</div>"
                );
            })
            .join("");
    }

    async function showHistory() {
        app.openModal("historyModal", closeHistoryModal);

        try {
            const response = await fetch("/api/scripts/history?user_id=" + encodeURIComponent(state.USER_ID));
            const data = await response.json();

            if (data.code !== 200) return;

            const historyContent = app.getEl("historyContent");
            state.historyData = data.data || [];
            historyContent.innerHTML = renderRecordList(state.historyData, "暂无历史记录", "viewHistory", "生成时间");
        } catch (error) {
            console.error(error);
        }
    }

    function closeHistoryModal() {
        app.closeModal("historyModal");
    }

    function viewHistory(index) {
        if (!state.historyData || !state.historyData[index]) return;

        const item = state.historyData[index];
        state.currentScheme = item.content || (item.schemes && item.schemes[0]) || "";
        app.renderScheme();
        closeHistoryModal();
    }

    function showFavorites() {
        app.openModal("favoritesModal", closeFavoritesModal);

        const favorites = JSON.parse(localStorage.getItem("ai_copywriter_favorites") || "[]");
        const favoritesContent = app.getEl("favoritesContent");
        favoritesContent.innerHTML = renderRecordList(favorites, "暂无收藏内容", "viewFavorite", "收藏时间");
    }

    function closeFavoritesModal() {
        app.closeModal("favoritesModal");
    }

    function viewFavorite(index) {
        const favorites = JSON.parse(localStorage.getItem("ai_copywriter_favorites") || "[]");
        if (!favorites[index]) return;

        state.currentScheme = favorites[index].content;
        app.renderScheme();
        closeFavoritesModal();
    }

    function showFeatures() {
        app.openModal("featuresModal", closeFeaturesModal);
    }

    function closeFeaturesModal() {
        app.closeModal("featuresModal");
    }

    function showDocs() {
        app.openModal("docsModal", closeDocsModal);
    }

    function closeDocsModal() {
        app.closeModal("docsModal");
    }

    function showAbout() {
        app.openModal("aboutModal", closeAboutModal);
    }

    function closeAboutModal() {
        app.closeModal("aboutModal");
    }

    app.bindGlobal({
        showNicknameModal: showNicknameModal,
        closeNicknameModal: closeNicknameModal,
        saveNickname: saveNickname,
        showHistory: showHistory,
        closeHistoryModal: closeHistoryModal,
        viewHistory: viewHistory,
        showFavorites: showFavorites,
        closeFavoritesModal: closeFavoritesModal,
        viewFavorite: viewFavorite,
        showFeatures: showFeatures,
        closeFeaturesModal: closeFeaturesModal,
        showDocs: showDocs,
        closeDocsModal: closeDocsModal,
        showAbout: showAbout,
        closeAboutModal: closeAboutModal
    });
})();
