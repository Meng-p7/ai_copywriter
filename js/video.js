(function () {
    const app = window.AIApp;
    const state = app.state;

    function formatModelUsage(quota, model) {
        const data = quota && quota.models ? quota.models[model] : null;
        if (!data) {
            return "Seedance " + model + "：0/0次";
        }
        return "Seedance " + model + "：" + data.used + "/" + data.limit + "次（剩余" + data.remaining + "次）";
    }

    function renderQuota(quota) {
        if (!quota) return;

        const usageText = app.getEl("videoUsageText");
        const memberText = app.getEl("videoMemberText");
        if (!usageText || !memberText) return;

        usageText.textContent = formatModelUsage(quota, "2.0") + " | " + formatModelUsage(quota, "1.8");

        if (quota.is_member) {
            const expireAt = quota.member_expire_at || "未设置";
            memberText.textContent = "会员状态：已开通（到期时间：" + expireAt + "）";
        } else {
            memberText.textContent = "会员状态：普通用户";
        }
    }

    function getModelRemaining(quota, model) {
        if (!quota || !quota.models || !quota.models[model]) {
            return 0;
        }
        return Number(quota.models[model].remaining || 0);
    }

    async function fetchVideoQuota(showToastOnError) {
        try {
            const response = await fetch("/api/video/quota?user_id=" + encodeURIComponent(state.USER_ID));
            const data = await response.json();

            if (data.code !== 200 || !data.data) {
                throw new Error(data.msg || "获取视频配额失败");
            }

            state.videoQuota = data.data;
            renderQuota(state.videoQuota);
            return state.videoQuota;
        } catch (error) {
            console.error(error);
            if (showToastOnError) {
                app.showToast("获取视频配额失败，请稍后重试");
            }
            return null;
        }
    }

    function showVideoModal() {
        if (!state.currentScheme) {
            app.showToast("请先生成文案再生成视频");
            return;
        }
        app.openModal("videoModal", closeVideoModal);
        fetchVideoQuota(false);
    }

    function closeVideoModal() {
        app.closeModal("videoModal");
    }

    function showRechargeModal() {
        app.openModal("rechargeModal", closeRechargeModal);
    }

    function closeRechargeModal() {
        app.closeModal("rechargeModal");
    }

    async function processRecharge() {
        try {
            const response = await fetch("/api/video/recharge", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: state.USER_ID,
                    months: 1
                })
            });
            const data = await response.json();

            if (data.code !== 200) {
                app.showToast("开通失败: " + (data.msg || "服务器错误"));
                return;
            }

            state.videoQuota = data.data;
            renderQuota(state.videoQuota);
            app.showToast("会员开通成功！");
            closeRechargeModal();
        } catch (error) {
            app.showToast("开通失败，请检查网络连接");
            console.error(error);
        }
    }

    async function generateVideo() {
        const model = app.getEl("videoModel").value;
        const digitalHuman = app.getEl("digitalHuman").value;
        const voiceStyle = app.getEl("voiceStyle").value;
        const script = state.currentScheme;

        if (!script) {
            app.showToast("请先生成文案再生成视频");
            return;
        }

        const latestQuota = await fetchVideoQuota(false);
        if (latestQuota && getModelRemaining(latestQuota, model) <= 0) {
            app.showToast("该模型今日次数已用完，请开通会员");
            showRechargeModal();
            return;
        }

        const generateBtn = app.getEl("generateVideoBtn");
        const originalText = generateBtn.innerHTML;
        generateBtn.innerHTML = "⏳ 生成中...";
        generateBtn.disabled = true;

        try {
            const response = await fetch("/api/video/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: state.USER_ID,
                    model: model,
                    digital_human: digitalHuman,
                    voice_style: voiceStyle,
                    script: script
                })
            });

            const data = await response.json();
            if (data.code === 200) {
                if (data.data && data.data.quota) {
                    state.videoQuota = data.data.quota;
                    renderQuota(state.videoQuota);
                } else {
                    await fetchVideoQuota(false);
                }

                app.showToast("视频生成成功！");
                closeVideoModal();
            } else {
                app.showToast("生成失败: " + (data.msg || "服务器错误"));
                if ((data.msg || "").includes("次数已用完")) {
                    showRechargeModal();
                }
            }
        } catch (error) {
            app.showToast("请求失败，请检查网络连接");
            console.error(error);
        } finally {
            generateBtn.innerHTML = originalText;
            generateBtn.disabled = false;
        }
    }

    app.bindGlobal({
        showVideoModal: showVideoModal,
        closeVideoModal: closeVideoModal,
        showRechargeModal: showRechargeModal,
        closeRechargeModal: closeRechargeModal,
        processRecharge: processRecharge,
        generateVideo: generateVideo
    });

    window.addEventListener("load", function () {
        fetchVideoQuota(false);
    });
})();
