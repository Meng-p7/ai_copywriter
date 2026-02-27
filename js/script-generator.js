(function () {
    const app = window.AIApp;
    const state = app.state;

    function scrollToForm() {
        const formSection = document.querySelector(".form-section");
        if (!formSection) return;
        formSection.scrollIntoView({ behavior: "smooth" });
    }

    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function initUser() {
        const savedUserName = localStorage.getItem("ai_copywriter_user_name");
        if (savedUserName) {
            state.userName = savedUserName;
            app.getEl("userNameDisplay").textContent = state.userName;
        }
    }

    function resetGenerateButton() {
        const generateBtn = app.getEl("generateBtn");
        if (generateBtn) {
            generateBtn.innerHTML = "🤖 生成文案";
        }
    }

    function initSceneSelector() {
        const sceneCards = document.querySelectorAll(".scene-card");
        sceneCards.forEach(function (card) {
            card.addEventListener("click", function () {
                sceneCards.forEach(function (item) {
                    item.classList.remove("active");
                });
                card.classList.add("active");
                resetGenerateButton();
            });
        });

        if (sceneCards.length > 0) {
            sceneCards[0].classList.add("active");
        }
    }

    function setupInputListeners() {
        app.getEl("style").addEventListener("change", resetGenerateButton);
        app.getEl("duration").addEventListener("change", resetGenerateButton);
        app.getEl("keyInfo").addEventListener("input", resetGenerateButton);
    }

    function setLoading(isLoading) {
        const loadingState = app.getEl("loadingState");
        const schemeContent = app.getEl("schemeContent");

        if (!loadingState || !schemeContent) return;

        loadingState.classList.toggle("is-hidden", !isLoading);
        schemeContent.classList.toggle("is-hidden", isLoading);
    }

    function renderEmptyScheme(message) {
        return '<div class="scheme-empty">' + app.escapeHtml(message) + "</div>";
    }

    async function generateScript() {
        const sceneCard = document.querySelector(".scene-card.active");
        if (!sceneCard) {
            app.showToast("请选择创作场景");
            return;
        }

        const scene = sceneCard.dataset.value;
        const style = app.getEl("style").value;
        const duration = app.getEl("duration").value;
        const keyInfo = app.getEl("keyInfo").value.trim();

        if (!keyInfo) {
            app.showToast("请填写核心信息");
            return;
        }

        state.currentGenerateParams = {
            user_id: state.USER_ID,
            scene: scene,
            style: style,
            duration: duration,
            key_info: keyInfo
        };

        setLoading(true);

        const generateBtn = app.getEl("generateBtn");
        generateBtn.innerHTML = "🤖 不满意？点击再次生成";

        try {
            const response = await fetch("/api/script/create", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(state.currentGenerateParams)
            });

            const data = await response.json();
            if (data.code === 200) {
                if (data.data.schemes && data.data.schemes.length > 0) {
                    state.currentScheme = data.data.schemes[0];
                } else if (data.data.content) {
                    state.currentScheme = data.data.content;
                } else {
                    state.currentScheme = "";
                }
                renderScheme();
            } else {
                app.showToast("生成失败: " + (data.msg || "服务器错误"));
            }
        } catch (error) {
            app.showToast("请求失败，请检查网络连接");
            console.error(error);
        } finally {
            setLoading(false);
        }
    }

    function renderScheme() {
        const contentDiv = app.getEl("schemeContent");
        if (!contentDiv) return;

        if (!state.currentScheme) {
            contentDiv.innerHTML = renderEmptyScheme("生成失败，请重试");
            return;
        }

        contentDiv.innerHTML =
            '<div class="scheme-header">' +
            '<div class="scheme-label">AI 生成方案</div>' +
            '<button class="favorite-btn" onclick="toggleFavorite()">❤️</button>' +
            "</div>" +
            '<div class="script-content">' + formatScriptContent(state.currentScheme) + "</div>";
    }

    function formatScriptContent(content) {
        if (!content) return "<p>暂无内容</p>";

        let formatted = content
            .replace(/标题:/g, '<h4 class="script-title">标题:')
            .replace(/配乐建议:/g, '<div class="music-suggestion">配乐建议:')
            .replace(/镜头\d+:/g, '<div class="shot-item"><div class="shot-header">$&</div>')
            .replace(/台词\d+:/g, '<div class="shot-dialogue">$&</div>');

        formatted = formatted.replace(/(<h4[^>]*>.*?)(?=<h4|<div|$)/gs, "$1</h4>");
        formatted = formatted.replace(/(<div class="music-suggestion">.*?)(?=<h4|<div|$)/gs, "$1</div>");
        formatted = formatted.replace(/(<div class="shot-item">.*?)(?=<h4|<div class="shot-item"|<div class="music-suggestion"|$)/gs, "$1</div>");

        return formatted;
    }

    function toggleFavorite() {
        if (!state.currentScheme) {
            app.showToast("请先生成文案再收藏");
            return;
        }

        const sceneCard = document.querySelector(".scene-card.active");
        const scene = sceneCard ? sceneCard.dataset.value : "未知场景";
        const style = app.getEl("style").value;
        const duration = app.getEl("duration").value;
        const keyInfo = app.getEl("keyInfo").value.trim();

        const favoriteItem = {
            scene: scene,
            style: style,
            duration: duration,
            keyInfo: keyInfo,
            content: state.currentScheme,
            timestamp: new Date().toISOString()
        };

        const favorites = JSON.parse(localStorage.getItem("ai_copywriter_favorites") || "[]");
        favorites.push(favoriteItem);
        localStorage.setItem("ai_copywriter_favorites", JSON.stringify(favorites));

        app.showToast("收藏成功");
    }

    function init() {
        initUser();
        initSceneSelector();
        setupInputListeners();
    }

    app.renderScheme = renderScheme;

    app.bindGlobal({
        generateScript: generateScript,
        toggleFavorite: toggleFavorite,
        scrollToTop: scrollToTop,
        scrollToForm: scrollToForm
    });

    window.addEventListener("load", init);
})();
