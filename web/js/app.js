document.addEventListener('DOMContentLoaded', () => {
    let currentCampaignId = null;
    let currentTurnNum = 1;
    let currentDay = 1;
    let currentRace = "Humano";

    const modalNewGame = document.getElementById('modal-new-game');
    const modalCampaigns = document.getElementById('modal-campaigns');
    const modalInventory = document.getElementById('modal-inventory');
    const modalQuests = document.getElementById('modal-quests');
    const modalEvents = document.getElementById('modal-events');
    const modalAllies = document.getElementById('modal-allies');

    const actionForm = document.getElementById('action-form');
    const actionInput = document.getElementById('action-input');
    const btnSubmit = document.getElementById('btn-submit');
    const inputImport = document.getElementById('input-import-campaign');

    if (window.TacticalMap) {
        window.TacticalMap.init('tactical-map-canvas', 'map-canvas-wrapper', 'map-tooltip');

        const btnZoomIn = document.getElementById('btn-map-zoom-in');
        if (btnZoomIn) btnZoomIn.onclick = () => window.TacticalMap.zoomIn();

        const btnZoomOut = document.getElementById('btn-map-zoom-out');
        if (btnZoomOut) btnZoomOut.onclick = () => window.TacticalMap.zoomOut();

        const btnRecenter = document.getElementById('btn-map-recenter');
        if (btnRecenter) btnRecenter.onclick = () => window.TacticalMap.recenter();

        const btnResetCamera = document.getElementById('btn-map-reset-camera');
        if (btnResetCamera) btnResetCamera.onclick = () => window.TacticalMap.resetCamera();

        const layerFilter = document.getElementById('map-layer-filter');
        if (layerFilter) {
            layerFilter.onchange = () => window.TacticalMap.setLayerFilter(layerFilter.value);
        }
    }

    window.addEventListener('node-inspect', (e) => {
        UI.openInspector(e.detail);
    });

    window.addEventListener('node-inspect-close', () => {
        UI.closeInspector();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (UI.inspectorOpen) {
                UI.closeInspector();
                return;
            }
        }
    });

    const inspectorDrawer = document.getElementById('tactical-inspector') || document.getElementById('inspector-drawer');
    const panelTactical = document.getElementById('panel-tactical');
    if (panelTactical && inspectorDrawer) {
        panelTactical.addEventListener('click', (e) => {
            if (UI.inspectorOpen && !inspectorDrawer.contains(e.target)) {
                const node = window.TacticalMap ? window.TacticalMap.findNodeAt(e.clientX, e.clientY) : null;
                if (!node) {
                    UI.closeInspector();
                }
            }
        });
    }

    const btnCloseInspector = document.getElementById('btn-close-inspector');
    if (btnCloseInspector) {
        btnCloseInspector.onclick = () => UI.closeInspector();
    }

    const btnToggleTop = document.getElementById('btn-toggle-top-panel');
    const tacticalTopPanel = document.getElementById('tactical-top-panel');
    if (btnToggleTop && tacticalTopPanel) {
        btnToggleTop.addEventListener('click', (e) => {
            e.stopPropagation();
            tacticalTopPanel.classList.toggle('collapsed');
            const isCollapsed = tacticalTopPanel.classList.contains('collapsed');
            btnToggleTop.textContent = isCollapsed ? '▼' : '▲';
            btnToggleTop.title = isCollapsed ? 'Expandir Painel Superior' : 'Ocultar Painel Superior';
            if (window.TacticalMap && window.TacticalMap.resize) {
                setTimeout(() => window.TacticalMap.resize(), 50);
            }
        });
    }

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
            const savedCampaignId = localStorage.getItem('rpg_active_campaign_id');
            const resp = await fetch('/api/campaigns');
            const campaigns = await resp.json();
            if (campaigns && campaigns.length > 0) {
                const targetCampaign = savedCampaignId ? campaigns.find(c => c.id === savedCampaignId) : null;
                const selectedId = targetCampaign ? targetCampaign.id : campaigns[0].id;
                currentCampaignId = selectedId;
                localStorage.setItem('rpg_active_campaign_id', selectedId);
                loadCampaignInfo(currentCampaignId);
            } else {
                localStorage.removeItem('rpg_active_campaign_id');
                modalNewGame.classList.remove('hidden');
            }
        } catch (e) {
            console.warn('API error, using new game fallback:', e);
            modalNewGame.classList.remove('hidden');
        }
    }

    async function refreshStateDetails(campaignId) {
        if (!campaignId) return;
        try {
            const resp = await fetch(`/api/campaign/${campaignId}/state-details`);
            if (resp.ok) {
                const details = await resp.json();
                UI.renderInventory(details.items || []);
                UI.renderTasks(details.tasks || []);
                UI.renderEvents(details.periodic_events || [], currentDay);
                UI.renderAllies(details.allies || []);
                if (window.TacticalMap && details.map_nodes) {
                    window.TacticalMap.setData(details.map_nodes, details.map_edges || []);
                }
            }
        } catch (err) {
            console.warn('Error fetching state details:', err);
        }
    }

    async function loadCampaignInfo(id) {
        try {
            currentCampaignId = id;
            localStorage.setItem('rpg_active_campaign_id', id);
            const infoResp = await fetch(`/api/campaigns/${id}`);
            const info = await infoResp.json();
            if (info.race) {
                currentRace = info.race;
            }
            if (info.status) {
                currentDay = info.status.dia_atual || 1;
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

            refreshStateDetails(currentCampaignId);
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
                    localStorage.setItem('rpg_active_campaign_id', id);
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
                                    localStorage.setItem('rpg_active_campaign_id', checkCamps[0].id);
                                    loadCampaignInfo(checkCamps[0].id);
                                } else {
                                    localStorage.removeItem('rpg_active_campaign_id');
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

    document.getElementById('btn-new-game').onclick = () => modalNewGame.classList.remove('hidden');
    document.getElementById('btn-close-modal').onclick = () => modalNewGame.classList.add('hidden');

    const btnInventoryDrawer = document.getElementById('btn-inventory-drawer');
    if (btnInventoryDrawer) {
        btnInventoryDrawer.onclick = () => {
            modalInventory.classList.remove('hidden');
            refreshStateDetails(currentCampaignId);
        };
    }
    const btnCloseInventory = document.getElementById('btn-close-inventory');
    if (btnCloseInventory) {
        btnCloseInventory.onclick = () => modalInventory.classList.add('hidden');
    }

    const btnQuestsDrawer = document.getElementById('btn-quests-drawer');
    if (btnQuestsDrawer) {
        btnQuestsDrawer.onclick = () => {
            modalQuests.classList.remove('hidden');
            refreshStateDetails(currentCampaignId);
        };
    }
    const btnCloseQuests = document.getElementById('btn-close-quests');
    if (btnCloseQuests) {
        btnCloseQuests.onclick = () => modalQuests.classList.add('hidden');
    }

    const btnEventsDrawer = document.getElementById('btn-events-drawer');
    if (btnEventsDrawer) {
        btnEventsDrawer.onclick = () => {
            modalEvents.classList.remove('hidden');
            refreshStateDetails(currentCampaignId);
        };
    }
    const btnCloseEvents = document.getElementById('btn-close-events');
    if (btnCloseEvents) {
        btnCloseEvents.onclick = () => modalEvents.classList.add('hidden');
    }

    const btnAlliesDrawer = document.getElementById('btn-allies-drawer');
    if (btnAlliesDrawer) {
        btnAlliesDrawer.onclick = () => {
            modalAllies.classList.remove('hidden');
            refreshStateDetails(currentCampaignId);
        };
    }
    const btnCloseAllies = document.getElementById('btn-close-allies');
    if (btnCloseAllies) {
        btnCloseAllies.onclick = () => modalAllies.classList.add('hidden');
    }

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

            if (data.campaign_id) {
                currentCampaignId = data.campaign_id;
            } else {
                const listResp = await fetch('/api/campaigns');
                const camps = await listResp.json();
                const matched = camps.find(c => c.name === payload.campaign_name);
                currentCampaignId = matched ? matched.id : (camps[0] ? camps[0].id : null);
            }
            localStorage.setItem('rpg_active_campaign_id', currentCampaignId);
            currentTurnNum = 1;
            currentDay = (data.status_reino && data.status_reino.dia_atual) ? data.status_reino.dia_atual : 1;

            UI.updateStatusHUD(data.status_reino, 1, currentRace);
            if (data.clima) {
                window.rpgAudio.updateThemeFromModel(data.clima);
            }
            UI.appendNarrativeBlock(data.aventura, "CONSELHO REAL");
            UI.renderQuickOptions(data.opcoes, data.aventura, (selected) => {
                actionInput.value = selected;
                actionForm.dispatchEvent(new Event('submit'));
            });

            if (data.actions) {
                UI.handleTurnActions(data.actions);
            }
            refreshStateDetails(currentCampaignId);
        } catch (err) {
            console.error(err);
            UI.appendNarrativeBlock("Erro ao iniciar novo reino. Verifique se o servidor está rodando.", "ERRO");
        }
    };

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

    actionForm.onsubmit = async (e) => {
        e.preventDefault();
        const text = actionInput.value.trim();
        if (!text || !currentCampaignId) return;

        if (estimateDebounceTimer) clearTimeout(estimateDebounceTimer);
        UI.showPreflightEstimate(null);
        actionInput.value = '';
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<span>Consultando...</span>';

        UI.appendNarrativeBlock(text, "ORDEM DO IMPERADOR");
        UI.showLoadingIndicator();

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
            currentDay = (data.status_reino && data.status_reino.dia_atual) ? data.status_reino.dia_atual : currentDay;

            UI.updateStatusHUD(data.status_reino, currentTurnNum, currentRace);
            if (data.clima) {
                window.rpgAudio.updateThemeFromModel(data.clima);
            }
            UI.appendNarrativeBlock(data.aventura, "CONSELHO REAL", true);
            UI.renderQuickOptions(data.opcoes, data.aventura, (selected) => {
                if (estimateDebounceTimer) clearTimeout(estimateDebounceTimer);
                actionInput.value = selected;
                actionForm.dispatchEvent(new Event('submit'));
            });

            if (data.actions) {
                UI.handleTurnActions(data.actions);
            }
            refreshStateDetails(currentCampaignId);
        } catch (err) {
            console.error(err);
            UI.hideLoadingIndicator();
            UI.appendNarrativeBlock("Falha ao comunicar com os conselheiros do reino.", "ERRO");
        }
    }

    document.addEventListener('click', async (e) => {
        const placeBtn = e.target.closest('.place-asset-btn');
        if (placeBtn && currentCampaignId) {
            const assetId = placeBtn.getAttribute('data-asset-id');
            if (assetId) {
                placeBtn.disabled = true;
                placeBtn.textContent = 'Posicionando...';
                try {
                    const resp = await fetch(`/api/campaigns/${currentCampaignId}/assets/${assetId}/place_on_map`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ connect_to_capital: true })
                    });
                    if (resp.ok) {
                        await refreshStateDetails(currentCampaignId);
                        const tabBtn = document.querySelector('.tab-btn[data-tab="tab-map"]');
                        if (tabBtn) tabBtn.click();
                        setTimeout(() => {
                            if (window.TacticalMap) window.TacticalMap.focusNode(`node_${assetId}`);
                        }, 250);
                    }
                } catch (err) {
                    console.error('Error placing asset on map:', err);
                } finally {
                    placeBtn.disabled = false;
                }
            }
            return;
        }

        const unplaceBtn = e.target.closest('.unplace-asset-btn');
        if (unplaceBtn && currentCampaignId) {
            const assetId = unplaceBtn.getAttribute('data-asset-id');
            if (assetId) {
                unplaceBtn.disabled = true;
                unplaceBtn.textContent = 'Removendo...';
                try {
                    const resp = await fetch(`/api/campaigns/${currentCampaignId}/assets/${assetId}/unplace_from_map`, {
                        method: 'POST'
                    });
                    if (resp.ok) {
                        await refreshStateDetails(currentCampaignId);
                    }
                } catch (err) {
                    console.error('Error unplacing asset from map:', err);
                } finally {
                    unplaceBtn.disabled = false;
                }
            }
            return;
        }

        const focusBtn = e.target.closest('.focus-asset-btn');
        if (focusBtn) {
            const nodeId = focusBtn.getAttribute('data-node-id') || `node_${focusBtn.getAttribute('data-asset-id')}`;
            const tabBtn = document.querySelector('.tab-btn[data-tab="tab-map"]');
            if (tabBtn) tabBtn.click();
            const modal = document.getElementById('modal-inventory');
            if (modal) modal.classList.add('hidden');
            setTimeout(() => {
                if (window.TacticalMap) window.TacticalMap.focusNode(nodeId);
            }, 250);
            return;
        }
    });

    const btnAudioToggle = document.getElementById('btn-audio-toggle');
    if (btnAudioToggle) {
        btnAudioToggle.onclick = () => window.rpgAudio.togglePlay();
    }
});
