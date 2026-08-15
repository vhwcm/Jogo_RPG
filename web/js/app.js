document.addEventListener('DOMContentLoaded', () => {
    let currentCampaignId = null;
    let currentTurnNum = 1;
    let currentRace = "Humano";

    const modalNewGame = document.getElementById('modal-new-game');
    const modalMemories = document.getElementById('modal-memories');
    const modalCampaigns = document.getElementById('modal-campaigns');
    const actionForm = document.getElementById('action-form');
    const actionInput = document.getElementById('action-input');
    const btnSubmit = document.getElementById('btn-submit');
    const inputImport = document.getElementById('input-import-campaign');

    // Fetch existing campaigns & health status
    checkHealth();
    checkExistingCampaigns();

    async function checkHealth() {
        try {
            const resp = await fetch('/api/health');
            const data = await resp.json();
            const warningBar = document.getElementById('api-key-warning-bar');
            if (data.has_api_key === false && warningBar) {
                warningBar.classList.remove('hidden');
            }
        } catch (e) {
            console.warn('Health check failed:', e);
        }
    }

    async function checkExistingCampaigns() {
        try {
            const resp = await fetch('/api/campaigns');
            const campaigns = await resp.json();
            if (campaigns && campaigns.length > 0) {
                currentCampaignId = campaigns[0].id;
                loadCampaignInfo(currentCampaignId);
            } else {
                modalNewGame.classList.remove('hidden');
            }
        } catch (e) {
            console.warn('API error, using new game fallback:', e);
            modalNewGame.classList.remove('hidden');
        }
    }

    async function loadCampaignInfo(id) {
        try {
            currentCampaignId = id;
            const infoResp = await fetch(`/api/campaigns/${id}`);
            const info = await infoResp.json();
            if (info.race) {
                currentRace = info.race;
            }
            if (info.status) {
                UI.updateStatusHUD(info.status, info.turn_number, currentRace);
                currentTurnNum = info.turn_number;
            }

            UI.clearNarrativeFeed();

            const histResp = await fetch(`/api/campaigns/${id}/history`);
            const histData = await histResp.json();
            const history = histData.history || [];

            if (history.length > 0) {
                history.forEach((h, index) => {
                    const raw = h.raw_state || {};
                    if (raw.user_action) {
                        UI.appendNarrativeBlock(raw.user_action, "ORDEM DO IMPERADOR");
                    }
                    if (raw.aventura) {
                        UI.appendNarrativeBlock(raw.aventura, "CONSELHO REAL");
                    }
                    if (raw.clima && window.rpgAudio) {
                        window.rpgAudio.updateThemeFromModel(raw.clima);
                    }
                    // For the last turn, render quick options
                    if (index === history.length - 1 && raw.opcoes) {
                        UI.renderQuickOptions(raw.opcoes, raw.aventura, (selected) => {
                            actionInput.value = selected;
                            actionForm.dispatchEvent(new Event('submit'));
                        });
                    }
                });
            } else {
                UI.appendNarrativeBlock("Iniciando crônica do reino...", "CONSELHO REAL");
            }
        } catch (e) {
            console.error('Failed to load campaign:', e);
        }
    }

    async function refreshCampaignsModal() {
        try {
            const resp = await fetch('/api/campaigns');
            const campaigns = await resp.json();
            UI.renderCampaignsList(campaigns, currentCampaignId, {
                onSelect: (id) => {
                    modalCampaigns.classList.add('hidden');
                    loadCampaignInfo(id);
                },
                onExport: async (id) => {
                    try {
                        const resp = await fetch(`/api/campaigns/${id}/export`);
                        const data = await resp.json();
                        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `aventura_${id}.json`;
                        a.click();
                        URL.revokeObjectURL(url);
                    } catch (err) {
                        alert('Erro ao exportar aventura.');
                    }
                },
                onDelete: async (id) => {
                    if (confirm('Tem certeza que deseja excluir esta aventura permanentemente?')) {
                        try {
                            await fetch(`/api/campaigns/${id}`, { method: 'DELETE' });
                            if (id === currentCampaignId) {
                                const checkResp = await fetch('/api/campaigns');
                                const checkCamps = await checkResp.json();
                                if (checkCamps && checkCamps.length > 0) {
                                    loadCampaignInfo(checkCamps[0].id);
                                } else {
                                    UI.clearNarrativeFeed();
                                    modalCampaigns.classList.add('hidden');
                                    modalNewGame.classList.remove('hidden');
                                }
                            }
                            refreshCampaignsModal();
                        } catch (err) {
                            alert('Erro ao excluir aventura.');
                        }
                    }
                }
            });
        } catch (err) {
            console.error('Error fetching campaigns list:', err);
        }
    }

    // Modal Navigation Listeners
    document.getElementById('btn-new-game').onclick = () => modalNewGame.classList.remove('hidden');
    document.getElementById('btn-close-modal').onclick = () => modalNewGame.classList.add('hidden');

    const btnCampaignsDrawer = document.getElementById('btn-campaigns-drawer');
    if (btnCampaignsDrawer) {
        btnCampaignsDrawer.onclick = () => {
            modalCampaigns.classList.remove('hidden');
            refreshCampaignsModal();
        };
    }
    const btnCloseCampaigns = document.getElementById('btn-close-campaigns');
    if (btnCloseCampaigns) {
        btnCloseCampaigns.onclick = () => modalCampaigns.classList.add('hidden');
    }
    const btnModalNewCampaign = document.getElementById('btn-modal-new-campaign');
    if (btnModalNewCampaign) {
        btnModalNewCampaign.onclick = () => {
            modalCampaigns.classList.add('hidden');
            modalNewGame.classList.remove('hidden');
        };
    }

    if (inputImport) {
        inputImport.onchange = async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            try {
                const text = await file.text();
                const json = JSON.parse(text);
                const resp = await fetch('/api/campaigns/import', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_data: json })
                });
                const resData = await resp.json();
                if (resData.campaign_id) {
                    modalCampaigns.classList.add('hidden');
                    loadCampaignInfo(resData.campaign_id);
                }
            } catch (err) {
                alert('Erro ao importar arquivo de aventura inválido.');
            }
            inputImport.value = '';
        };
    }

    document.getElementById('form-new-game').onsubmit = async (e) => {
        e.preventDefault();
        currentRace = document.getElementById('input-race').value;
        const payload = {
            campaign_name: document.getElementById('input-campaign-name').value,
            ruler_name: document.getElementById('input-ruler-name').value,
            kingdom_name: document.getElementById('input-kingdom-name').value,
            race: currentRace,
            provider: document.getElementById('input-provider').value
        };

        modalNewGame.classList.add('hidden');
        UI.clearNarrativeFeed();
        UI.appendNarrativeBlock("Fundando um novo reino e consultando os conselheiros...", "SISTEMA");

        try {
            const resp = await fetch('/api/campaigns', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();
            
            // Get newly created campaign ID
            const listResp = await fetch('/api/campaigns');
            const camps = await listResp.json();
            currentCampaignId = camps[0].id;
            currentTurnNum = 1;

            UI.updateStatusHUD(data.status_reino, 1, currentRace);
            if (data.clima) {
                window.rpgAudio.updateThemeFromModel(data.clima);
            }
            UI.appendNarrativeBlock(data.aventura, "CONSELHO REAL");
            UI.renderQuickOptions(data.opcoes, data.aventura, (selected) => {
                actionInput.value = selected;
                actionForm.dispatchEvent(new Event('submit'));
            });
        } catch (err) {
            console.error(err);
            UI.appendNarrativeBlock("Erro ao iniciar novo reino. Verifique se o servidor está rodando.", "ERRO");
        }
    };

    // Pre-flight action impact estimation listener
    let estimateDebounceTimer = null;
    if (actionInput) {
        actionInput.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            if (estimateDebounceTimer) clearTimeout(estimateDebounceTimer);
            if (!val || val.length < 5 || !currentCampaignId) {
                UI.showPreflightEstimate(null);
                return;
            }
            estimateDebounceTimer = setTimeout(async () => {
                try {
                    const resp = await fetch(`/api/campaigns/${currentCampaignId}/estimate_action`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ action_text: val })
                    });
                    const est = await resp.json();
                    if (actionInput.value.trim() === val) {
                        UI.showPreflightEstimate(est);
                    }
                } catch (err) {
                    console.warn('Preflight estimation error:', err);
                }
            }, 600);
        });
    }

    // Execute Turn Form Submission
    actionForm.onsubmit = async (e) => {
        e.preventDefault();
        const text = actionInput.value.trim();
        if (!text || !currentCampaignId) return;

        UI.showPreflightEstimate(null);
        actionInput.value = '';
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<span>Consultando...</span>';

        UI.appendNarrativeBlock(text, "ORDEM DO IMPERADOR");

        await executePlayerAction(text);

        btnSubmit.disabled = false;
        btnSubmit.innerHTML = '<span>Enviar Ordem</span>';
    };

    async function executePlayerAction(actionText) {
        if (!currentCampaignId) return;
        try {
            const resp = await fetch('/api/turn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    campaign_id: currentCampaignId,
                    player_action: actionText
                })
            });
            const data = await resp.json();
            currentTurnNum += 1;
            
            UI.updateStatusHUD(data.status_reino, currentTurnNum, currentRace);
            if (data.clima) {
                window.rpgAudio.updateThemeFromModel(data.clima);
            }
            UI.appendNarrativeBlock(data.aventura, "CONSELHO REAL");
            UI.renderQuickOptions(data.opcoes, data.aventura, (selected) => {
                actionInput.value = selected;
                actionForm.dispatchEvent(new Event('submit'));
            });
        } catch (err) {
            console.error(err);
            UI.appendNarrativeBlock("Falha ao comunicar com os conselheiros do reino.", "ERRO");
        }
    }

    // Memory Drawer Listeners
    document.getElementById('btn-memory-drawer').onclick = async () => {
        modalMemories.classList.remove('hidden');
        if (currentCampaignId) {
            try {
                const resp = await fetch(`/api/memories/${currentCampaignId}`);
                const memories = await resp.json();
                UI.renderMemories(memories);
            } catch (e) {
                console.error(e);
            }
        }
    };
    document.getElementById('btn-close-memories').onclick = () => modalMemories.classList.add('hidden');

    // Audio Controls Listeners
    const btnAudioToggle = document.getElementById('btn-audio-toggle');
    if (btnAudioToggle) {
        btnAudioToggle.onclick = () => window.rpgAudio.togglePlay();
    }
});
