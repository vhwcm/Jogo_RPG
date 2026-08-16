const RACE_ASSETS = {
    "Anão": { leader: "anão.jpeg", reino: "reino anão.png" },
    "Centauro": { leader: "centauro.jpg", reino: "reino centauro.png" },
    "Demônio": { leader: "demonio.jpeg", reino: "reino demonio.png" },
    "Djinn": { leader: "djinn.jpeg", reino: "reino djinn.png" },
    "Dragão": { leader: "dragão.jpeg", reino: "reino dragão.png" },
    "Elemental": { leader: "elemental.jpeg", reino: "reino elemental.png" },
    "Elfo": { leader: "elfo.jpeg", reino: "reino elfo.png" },
    "Fauno": { leader: "fauno.jpeg", reino: "reino fauno.png" },
    "Gnomo": { leader: "gnomo.jpeg", reino: "reino gnomo.png" },
    "Goblin": { leader: "goblin.jpeg", reino: "reino goblin.png" },
    "Humano": { leader: "humano.jpeg", reino: "reino humano.png" },
    "Leprechaun": { leader: "Leprechaun.jpeg", reino: "reino leprechaun.png" },
    "Mago": { leader: "mago.jpeg", reino: "reino mago.png" },
    "Morto Vivo": { leader: "morto vivo.jpeg", reino: "reino morto vivo.png" },
    "Orc": { leader: "orc.jpeg", reino: "reino orc.png" },
    "Rinoceronte": { leader: "rinoceronte.jpeg", reino: "reino rinoceronte.png" },
    "Sereia": { leader: "sereia.jpeg", reino: "reino sereia.png" },
    "Trol": { leader: "trol.jpeg", reino: "reino trol.png" },
    "Vampiro": { leader: "vampiro.jpeg", reino: "reino vampiro.png" }
};

const UI = {
    previousStatus: null,
    inspectorOpen: false,

    updateStatusHUD(status, turnNum, race) {
        const prev = this.previousStatus;

        const reinoEl = document.getElementById('val-reino');
        if (reinoEl) reinoEl.textContent = status.nome_reino || 'Valdrin';

        const impEl = document.getElementById('val-imperador');
        if (impEl) impEl.textContent = status.imperador || 'Arthur';

        const dinheiroEl = document.getElementById('val-dinheiro');
        if (dinheiroEl) dinheiroEl.textContent = (status.dinheiro || 0).toLocaleString();

        const popEl = document.getElementById('val-populacao');
        if (popEl) popEl.textContent = (status.populacao || status.população || 10000).toLocaleString();

        const milEl = document.getElementById('val-militar');
        if (milEl) milEl.textContent = (status.poder_militar || 0).toLocaleString();

        const felEl = document.getElementById('val-felicidade');
        if (felEl) felEl.textContent = status.felicidade || '70%';

        const relEl = document.getElementById('val-religiao');
        if (relEl) relEl.textContent = status.religião || 'Nenhuma';

        const turnoEl = document.getElementById('val-turno-badge');
        if (turnoEl) turnoEl.textContent = `Turno ${turnNum || 1}`;

        if (race) {
            this.updateRaceVisuals(race);
        }

        if (prev) {
            const deltaGold = (status.dinheiro || 0) - (prev.dinheiro || 0);
            if (deltaGold < 0) {
                this.showToast(`🔴 Perdeu ${Math.abs(deltaGold).toLocaleString()} Ouro`, 'loss');
                this.flashHUDElement('card-dinheiro', 'pulse-loss');
            } else if (deltaGold > 0) {
                this.showToast(`🟢 Ganhou ${deltaGold.toLocaleString()} Ouro`, 'gain');
                this.flashHUDElement('card-dinheiro', 'pulse-gain');
            }

            const prevPop = prev.populacao || prev.população || 10000;
            const currPop = status.populacao || status.população || 10000;
            const deltaPop = currPop - prevPop;
            if (deltaPop < 0) {
                this.showToast(`👥 População reduziu em ${Math.abs(deltaPop).toLocaleString()} habitantes`, 'loss');
                this.flashHUDElement('card-populacao', 'pulse-loss');
            } else if (deltaPop > 0) {
                this.showToast(`👥 População cresceu em ${deltaPop.toLocaleString()} habitantes`, 'gain');
                this.flashHUDElement('card-populacao', 'pulse-gain');
            }

            if (status.religião && prev.religião && status.religião !== prev.religião) {
                this.showToast(`⛪ Religião alterada para: ${status.religião}`, 'religion');
                this.flashHUDElement('card-religiao', 'pulse-religion');
            }
        }

        this.previousStatus = { ...status };
    },

    flashHUDElement(elementId, cssClass) {
        const el = document.getElementById(elementId);
        if (!el) return;
        el.classList.remove('pulse-loss', 'pulse-gain', 'pulse-religion');
        void el.offsetWidth;
        el.classList.add(cssClass);
        setTimeout(() => el.classList.remove(cssClass), 2000);
    },

    showToast(message, type = 'loss') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `<span>${message}</span>`;

        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(50px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    },

    handleTurnActions(actions) {
        if (!Array.isArray(actions) || actions.length === 0) return;

        actions.forEach(act => {
            const type = act.action_type;
            const p = act.payload || {};
            const cat = (p.categoria || '').toLowerCase();

            if (type === 'add_item' || type === 'add_structure' || type === 'add_kingdom_asset') {
                const name = p.nome || 'Novo Ativo';
                if (cat === 'santuario') {
                    this.showToast(`⛪ Santuário edificado: <strong>${name}</strong>`, 'gain');
                } else if (cat === 'posto_avancado') {
                    this.showToast(`🛡️ Posto Avançado estabelecido: <strong>${name}</strong>`, 'gain');
                } else if (cat === 'estrutura' || cat === 'fortificacao' || cat === 'construcao') {
                    this.showToast(`🏛️ Estrutura concluída: <strong>${name}</strong>`, 'gain');
                } else {
                    const catLabel = p.categoria ? `[${p.categoria}] ` : '';
                    this.showToast(`🎒 Ativo obtido: ${catLabel}<strong>${name}</strong>`, 'action');
                }
            } else if (type === 'remove_item' || type === 'remove_structure' || type === 'remove_kingdom_asset') {
                const name = p.nome || p.id || 'Ativo';
                this.showToast(`🏛️ Ativo removido: <strong>${name}</strong>`, 'loss');
            } else if (type === 'create_task') {
                const title = p.titulo || 'Nova Tarefa';
                const prefix = p.is_incidente_dinamico ? '⚠️ Incidente Dinâmico' : '📜 Nova Quest';
                this.showToast(`${prefix}: <strong>${title}</strong>`, 'gain');
            } else if (type === 'update_task') {
                const title = p.titulo || p.id || 'Tarefa';
                const status = p.status || '';
                const prog = p.progresso !== undefined && p.progresso !== null ? ` (${p.progresso}%)` : '';
                if (status === 'concluida') {
                    this.showToast(`✅ Quest Concluída: <strong>${title}</strong>`, 'gain');
                } else if (status === 'falhou') {
                    this.showToast(`❌ Quest Falhou: <strong>${title}</strong>`, 'loss');
                } else {
                    this.showToast(`📜 Progresso da Quest: <strong>${title}</strong>${prog}`, 'action');
                }
            } else if (type === 'add_ally') {
                const name = p.nome || 'Novo Reino';
                this.showToast(`👑 Novo Reino Conhecido: <strong>${name}</strong>`, 'action');
            } else if (type === 'update_ally') {
                const name = p.nome || p.id || 'Reino';
                const rel = p.relacionamento !== undefined ? ` (Relação: ${p.relacionamento})` : '';
                this.showToast(`👑 Diplomacia Atualizada: <strong>${name}</strong>${rel}`, 'action');
            } else if (type === 'add_map_node') {
                const label = p.label || p.nome || 'Novo Local';
                const emoji = p.emoji || '📍';
                this.showToast(`🗺️ Local Mapeado: ${emoji} <strong>${label}</strong>`, 'gain');
            } else if (type === 'update_map_node') {
                const label = p.label || p.id || 'Local';
                this.showToast(`🗺️ Atualização Tática: <strong>${label}</strong>`, 'action');
            } else if (type === 'remove_map_node') {
                this.showToast(`🗺️ Ponto Removido do Mapa Tático`, 'loss');
            } else if (type === 'connect_map_nodes' || type === 'add_map_edge') {
                const desc = p.descricao || 'Nova Rota';
                this.showToast(`🗺️ Nova Rota Estabelecida: <strong>${desc}</strong>`, 'action');
            }
        });
    },

    renderInventory(items) {
        const modalList = document.getElementById('inventory-list');
        const countBadge = document.getElementById('badge-inventory-count');
        const summaryTag = document.getElementById('inventory-summary-tag');

        const count = items ? items.length : 0;
        if (countBadge) countBadge.textContent = count;
        if (summaryTag) summaryTag.textContent = `${count} ${count === 1 ? 'Ativo Registrado' : 'Ativos Registrados'}`;

        if (!modalList) return;
        modalList.innerHTML = '';

        if (!items || items.length === 0) {
            modalList.innerHTML = '<div class="modular-card"><p style="color: var(--text-muted); font-size: 0.85rem;">Nenhuma estrutura, santuário ou item registrado.</p></div>';
            return;
        }

        items.forEach(it => {
            const card = document.createElement('div');
            card.className = 'modular-card';

            const cat = (it.categoria || 'outro').toLowerCase();
            const badgeClass = `badge-${cat.replace(/\s+/g, '_')}`;

            let attrHtml = '';
            const attrs = it.atributos || {};
            const keys = Object.keys(attrs);
            if (keys.length > 0) {
                attrHtml = '<div class="attr-tag-group">';
                keys.forEach(k => {
                    attrHtml += `<span class="attr-tag">${k}: ${attrs[k]}</span>`;
                });
                attrHtml += '</div>';
            }

            let iconPrefix = '🏛️';
            if (cat === 'santuario') iconPrefix = '⛪';
            else if (cat === 'posto_avancado') iconPrefix = '🛡️';
            else if (cat === 'criatura') iconPrefix = '🐉';
            else if (cat === 'artefato') iconPrefix = '✨';
            else if (cat === 'equipamento') iconPrefix = '⚔️';
            else if (cat === 'recurso') iconPrefix = '📦';

            card.innerHTML = `
                <div class="modular-card-header">
                    <span class="modular-card-title">${iconPrefix} ${it.nome || 'Sem nome'}</span>
                    <span class="modular-badge ${badgeClass}">${(it.categoria || 'outro').replace('_', ' ')}</span>
                </div>
                <p class="modular-card-desc">${it.descricao || 'Sem descrição detalhada.'}</p>
                ${attrHtml}
            `;
            modalList.appendChild(card);
        });
    },

    renderTasks(tasks) {
        const liveList = document.getElementById('tasks-live-list');
        const countBadge = document.getElementById('badge-tasks-count');
        const summaryTag = document.getElementById('quests-summary-tag');

        const activeCount = tasks ? tasks.filter(t => t.status === 'em_andamento').length : 0;
        if (countBadge) countBadge.textContent = activeCount;
        if (summaryTag) summaryTag.textContent = `${activeCount} ${activeCount === 1 ? 'Quest Ativa' : 'Quests Ativas'}`;

        if (!liveList) return;
        liveList.innerHTML = '';

        if (!tasks || tasks.length === 0) {
            liveList.innerHTML = '<div class="modular-card"><p style="color: var(--text-muted); font-size: 0.85rem;">Nenhuma quest ativa no momento.</p></div>';
            return;
        }

        tasks.forEach(tk => {
            const card = document.createElement('div');
            card.className = 'modular-card';

            const statusClass = `badge-status-${tk.status || 'em_andamento'}`;
            const isIncident = tk.is_incidente_dinamico || tk.is_incidente;

            let progressHtml = '';
            if (tk.progresso !== null && tk.progresso !== undefined) {
                const progClamped = Math.max(0, Math.min(100, Number(tk.progresso)));
                progressHtml = `
                    <div class="task-progress-container">
                        <div class="task-meta-row">
                            <span>Progresso</span>
                            <strong>${progClamped}%</strong>
                        </div>
                        <div class="task-progress-bar">
                            <div class="task-progress-fill" style="width: ${progClamped}%;"></div>
                        </div>
                    </div>
                `;
            }

            let durationMeta = '';
            if (tk.duracao_estimada) {
                durationMeta = `
                    <div class="task-meta-row" style="margin-top: 4px;">
                        <span>⏳ ${tk.duracao_estimada}</span>
                    </div>
                `;
            }

            card.innerHTML = `
                <div class="modular-card-header">
                    <span class="modular-card-title">${tk.titulo || 'Sem título'}</span>
                    <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                        ${isIncident ? '<span class="modular-badge badge-incident">⚡ Incidente</span>' : ''}
                        <span class="modular-badge ${statusClass}">${(tk.status || 'em_andamento').replace('_', ' ')}</span>
                    </div>
                </div>
                <p class="modular-card-desc">${tk.descricao || 'Sem descrição.'}</p>
                ${tk.objetivo_esperado ? `<p style="font-size: 0.82rem; color: var(--gold-primary);">🎯 <strong>Objetivo:</strong> ${tk.objetivo_esperado}</p>` : ''}
                ${progressHtml}
                ${durationMeta}
            `;
            liveList.appendChild(card);
        });
    },

    renderAllies(allies) {
        const list = document.getElementById('allies-list');
        const countBadge = document.getElementById('badge-allies-count');
        const summaryTag = document.getElementById('allies-summary-tag');

        const count = allies ? allies.length : 0;
        if (countBadge) countBadge.textContent = count;
        if (summaryTag) summaryTag.textContent = `${count} ${count === 1 ? 'Reino Conhecido' : 'Reinos Conhecidos'}`;

        if (!list) return;
        list.innerHTML = '';

        if (!allies || allies.length === 0) {
            list.innerHTML = '<div class="modular-card"><p style="color: var(--text-muted);">Nenhum império estrangeiro ou aliado diplomático registrado.</p></div>';
            return;
        }

        allies.forEach(al => {
            const card = document.createElement('div');
            card.className = 'modular-card';

            const status = (al.status_diplomatico || 'neutro').toLowerCase();
            const badgeClass = `badge-diplomacy-${status}`;

            const rel = Math.max(-100, Math.min(100, Number(al.relacionamento || 50)));
            const relNormalizedPct = ((rel + 100) / 200) * 100;
            const barColor = rel >= 60 ? '#2ecc71' : (rel >= 0 ? '#f1c40f' : '#e74c3c');

            card.innerHTML = `
                <div class="modular-card-header">
                    <span class="modular-card-title">${al.nome || 'Reino'}</span>
                    <span class="modular-badge ${badgeClass}">${status}</span>
                </div>
                <div style="font-size: 0.86rem; color: #e2e8f0; display: flex; flex-direction: column; gap: 4px;">
                    <div>👑 <strong>Soberano:</strong> ${al.rei || 'Desconhecido'}</div>
                    <div style="display: flex; gap: 14px; color: var(--text-muted); font-size: 0.8rem;">
                        <span>⚔️ Militar: <strong style="color: #fff;">${al.poder_militar || 'N/A'}</strong></span>
                        <span>👥 População: <strong style="color: #fff;">${al.populacao || 'N/A'}</strong></span>
                    </div>
                </div>
                <div class="ally-thermometer">
                    <div class="task-meta-row">
                        <span>Relação Diplomática</span>
                        <strong style="color: ${barColor};">${rel > 0 ? '+' : ''}${rel} / 100</strong>
                    </div>
                    <div class="thermometer-bar">
                        <div class="thermometer-fill" style="width: ${relNormalizedPct}%; background: ${barColor};"></div>
                    </div>
                </div>
                ${al.historico_notas ? `<p style="font-size: 0.8rem; color: var(--text-muted); font-style: italic;">"${al.historico_notas}"</p>` : ''}
            `;
            list.appendChild(card);
        });
    },

    showPreflightEstimate(estimate) {
        const container = document.getElementById('preflight-estimate');
        if (!container) return;

        if (!estimate || (estimate.dinheiro === null && estimate.poder_militar === null)) {
            container.classList.add('hidden');
            container.innerHTML = '';
            return;
        }

        let badgesHtml = '';
        if (estimate.dinheiro !== null && estimate.dinheiro !== undefined && estimate.dinheiro !== 0) {
            const classType = estimate.dinheiro < 0 ? 'badge-cost' : 'badge-gain';
            const sign = estimate.dinheiro > 0 ? '+' : '';
            badgesHtml += `<span class="badge-impact ${classType}">💰 ${sign}${estimate.dinheiro.toLocaleString()} Ouro</span>`;
        }
        if (estimate.poder_militar !== null && estimate.poder_militar !== undefined && estimate.poder_militar !== 0) {
            const classType = estimate.poder_militar < 0 ? 'badge-military-loss' : 'badge-military-gain';
            const sign = estimate.poder_militar > 0 ? '+' : '';
            badgesHtml += `<span class="badge-impact ${classType}">⚔️ ${sign}${estimate.poder_militar.toLocaleString()} Militar</span>`;
        }

        if (!badgesHtml) {
            container.classList.add('hidden');
            return;
        }

        container.innerHTML = `
            <span><strong>Impacto Estimado:</strong> ${estimate.explicacao || ''}</span>
            <div class="preflight-estimate-badges">${badgesHtml}</div>
        `;
        container.classList.remove('hidden');
    },

    updateRaceVisuals(race) {
        const normRace = Object.keys(RACE_ASSETS).find(k => k.toLowerCase() === (race || '').toLowerCase()) || 'Humano';
        const assetInfo = RACE_ASSETS[normRace] || RACE_ASSETS['Humano'];

        const bgOverlay = document.getElementById('bg-overlay');
        if (bgOverlay) {
            const bgPath = `assets/reinos/${encodeURIComponent(assetInfo.reino)}`;
            bgOverlay.style.backgroundImage = `linear-gradient(rgba(5, 5, 8, 0.82), rgba(5, 5, 8, 0.98)), url('${bgPath}')`;
            bgOverlay.style.backgroundSize = 'cover';
            bgOverlay.style.backgroundPosition = 'center';
        }
    },

    showLoadingIndicator(message = "O Conselho Real delibera...") {
        this.hideLoadingIndicator();
        const feed = document.getElementById('narrative-feed');
        if (!feed) return;
        const block = document.createElement('div');
        block.id = 'narrative-loading-indicator';
        block.className = 'narrative-block loading-pulse';
        block.innerHTML = `
            <div class="speaker-tag">CONSELHO REAL</div>
            <div class="story-text" style="color: var(--text-muted); font-style: italic;">
                <span class="loading-spinner-inline">⏳</span> ${message}
            </div>
        `;
        feed.appendChild(block);
        feed.scrollTop = feed.scrollHeight;
    },

    hideLoadingIndicator() {
        const loader = document.getElementById('narrative-loading-indicator');
        if (loader) loader.remove();
    },

    appendNarrativeBlock(text, speaker = "CONSELHO REAL", animate = false) {
        this.hideLoadingIndicator();
        const feed = document.getElementById('narrative-feed');
        if (!feed) return;

        const block = document.createElement('div');
        block.className = 'narrative-block';

        const speakerTag = document.createElement('div');
        speakerTag.className = 'speaker-tag';
        speakerTag.textContent = speaker;

        const storyText = document.createElement('div');
        storyText.className = 'story-text';

        block.appendChild(speakerTag);
        block.appendChild(storyText);
        feed.appendChild(block);

        if (!animate || text.length < 10) {
            storyText.textContent = text;
            feed.scrollTop = feed.scrollHeight;
        } else {
            let index = 0;
            const step = Math.max(3, Math.floor(text.length / 40));
            const timer = setInterval(() => {
                index += step;
                if (index >= text.length) {
                    storyText.textContent = text;
                    clearInterval(timer);
                } else {
                    storyText.textContent = text.slice(0, index);
                }
                feed.scrollTop = feed.scrollHeight;
            }, 16);
        }
    },

    renderQuickOptions(opcoes, text, onOptionSelect) {
        const container = document.getElementById('quick-options');
        if (!container) return;
        container.innerHTML = '';

        if (typeof text === 'function') {
            onOptionSelect = text;
            text = typeof opcoes === 'string' ? opcoes : '';
            if (!Array.isArray(opcoes)) {
                opcoes = null;
            }
        }

        let parsedOptions = [];

        if (Array.isArray(opcoes) && opcoes.length > 0) {
            parsedOptions = opcoes;
        }

        if (parsedOptions.length === 0 && text && typeof text === 'string') {
            const lines = text.split('\n');
            const optionLines = lines.filter(l => /^\s*(\d+[\.)]|\*\*?\d+[\.)]?\*\*?)\s+/.test(l));
            if (optionLines.length > 0) {
                parsedOptions = optionLines.map(l => l.trim());
            } else {
                const inlineMatches = text.match(/(?:^|\s)(\d+[\.)]\s+[^1-9\n]+?)(?=\s+\d+[\.)]|$)/g);
                if (inlineMatches) {
                    parsedOptions = inlineMatches.map(m => m.trim());
                }
            }
        }

        if (parsedOptions.length > 0) {
            parsedOptions.forEach(optItem => {
                let optText = '';
                let impacto = null;

                if (typeof optItem === 'object' && optItem !== null) {
                    optText = optItem.texto || '';
                    impacto = optItem.impacto || null;
                } else {
                    optText = String(optItem).trim();
                }

                if (!optText) return;

                const btn = document.createElement('button');
                btn.className = 'choice-btn';

                const cleanLabel = optText.replace(/\*\*/g, '').trim();

                const textSpan = document.createElement('span');
                textSpan.className = 'choice-btn-text';
                textSpan.textContent = cleanLabel;
                btn.appendChild(textSpan);

                if (impacto) {
                    const badgesDiv = document.createElement('div');
                    badgesDiv.className = 'impact-badges';

                    if (impacto.dinheiro !== null && impacto.dinheiro !== undefined && impacto.dinheiro !== 0) {
                        const bClass = impacto.dinheiro < 0 ? 'badge-cost' : 'badge-gain';
                        const sign = impacto.dinheiro > 0 ? '+' : '';
                        badgesDiv.innerHTML += `<span class="badge-impact ${bClass}">💰 ${sign}${impacto.dinheiro.toLocaleString()}</span>`;
                    }

                    if (impacto.poder_militar !== null && impacto.poder_militar !== undefined && impacto.poder_militar !== 0) {
                        const bClass = impacto.poder_militar < 0 ? 'badge-military-loss' : 'badge-military-gain';
                        const sign = impacto.poder_militar > 0 ? '+' : '';
                        badgesDiv.innerHTML += `<span class="badge-impact ${bClass}">⚔️ ${sign}${impacto.poder_militar.toLocaleString()}</span>`;
                    }

                    if (badgesDiv.children.length > 0) {
                        btn.appendChild(badgesDiv);
                    }
                }

                btn.onclick = () => onOptionSelect(cleanLabel);
                container.appendChild(btn);
            });
        }
    },

    clearNarrativeFeed() {
        const feed = document.getElementById('narrative-feed');
        if (feed) feed.innerHTML = '';
        const quickOptions = document.getElementById('quick-options');
        if (quickOptions) quickOptions.innerHTML = '';
        this.showPreflightEstimate(null);
    },

    renderCampaignsList(campaigns, currentCampaignId, callbacks) {
        const container = document.getElementById('campaigns-list');
        if (!container) return;
        container.innerHTML = '';

        if (!campaigns || campaigns.length === 0) {
            container.innerHTML = '<div class="campaign-card"><p style="color: var(--text-muted);">Nenhuma aventura encontrada. Clique em "+ Novo Reino" para iniciar!</p></div>';
            return;
        }

        campaigns.forEach(c => {
            const card = document.createElement('div');
            const isActive = c.id === currentCampaignId;
            card.className = `campaign-card ${isActive ? 'active' : ''}`;

            const lastUpdated = c.updated_at ? new Date(c.updated_at).toLocaleString('pt-BR') : (c.created_at ? new Date(c.created_at).toLocaleString('pt-BR') : '');

            card.innerHTML = `
                <div class="campaign-info">
                    <div class="campaign-title-row">
                        <h3>${c.name || 'Sem nome'}</h3>
                        ${isActive ? '<span class="active-badge">EM JOGO</span>' : ''}
                    </div>
                    <div class="campaign-details-row">
                        <span>Reino: <strong>${c.kingdom_name || 'Desconhecido'}</strong></span>
                        <span>Imperador: <strong>${c.ruler_name || 'Desconhecido'}</strong></span>
                        <span>Raça: <strong>${c.race || 'Humano'}</strong></span>
                        <span>Turno: <strong>${c.turn_number || 1}</strong></span>
                        ${lastUpdated ? `<span>Último Acesso: <strong>${lastUpdated}</strong></span>` : ''}
                    </div>
                </div>
                <div class="campaign-card-actions">
                    ${!isActive ? `<button class="btn btn-primary btn-sm btn-load-camp" data-id="${c.id}">Carregar</button>` : ''}
                    <button class="btn btn-secondary btn-sm btn-export-camp" data-id="${c.id}">Exportar</button>
                    <button class="btn btn-danger btn-sm btn-delete-camp" data-id="${c.id}">Excluir</button>
                </div>
            `;

            container.appendChild(card);
        });

        container.querySelectorAll('.btn-load-camp').forEach(btn => {
            btn.onclick = () => callbacks.onSelect && callbacks.onSelect(btn.dataset.id);
        });
        container.querySelectorAll('.btn-export-camp').forEach(btn => {
            btn.onclick = () => callbacks.onExport && callbacks.onExport(btn.dataset.id);
        });
        container.querySelectorAll('.btn-delete-camp').forEach(btn => {
            btn.onclick = () => callbacks.onDelete && callbacks.onDelete(btn.dataset.id);
        });
    },

    renderMemories(memories) {
        const listContainer = document.getElementById('memory-list');
        if (!listContainer) return;
        listContainer.innerHTML = '';

        if (!memories || memories.length === 0) {
            listContainer.innerHTML = '<div class="memory-item">Nenhuma memória episódica registrada até o momento.</div>';
            return;
        }

        memories.forEach(m => {
            const item = document.createElement('div');
            item.className = 'memory-item';
            item.innerHTML = `<strong>Turno ${m.turn_number}</strong> (Importância: ${(m.importance || 0).toFixed(2)})<br>${m.content}`;
            listContainer.appendChild(item);
        });
    },

    openInspector(node) {
        const drawer = document.getElementById('inspector-drawer');
        if (!drawer || !node) return;

        this.inspectorOpen = true;

        document.getElementById('inspector-emoji').textContent = node.emoji || '📍';
        document.getElementById('inspector-name').textContent = node.label || 'Entidade';

        const typeLabels = window.TacticalMap ? window.TacticalMap.typeLabels : {};
        document.getElementById('inspector-type').textContent = typeLabels[node.node_type] || node.node_type;

        const statusPill = document.getElementById('inspector-status');
        statusPill.textContent = (node.status || 'ativo').toUpperCase();
        statusPill.className = 'inspector-status-pill';

        const statusColors = {
            'ativo': { bg: 'rgba(42, 157, 143, 0.25)', color: '#2a9d8f', border: 'rgba(42, 157, 143, 0.5)' },
            'hostil': { bg: 'rgba(217, 64, 69, 0.25)', color: '#ff6b6b', border: 'rgba(217, 64, 69, 0.5)' },
            'em_marcha': { bg: 'rgba(244, 162, 97, 0.25)', color: '#fca5a5', border: 'rgba(244, 162, 97, 0.5)' },
            'em_andamento': { bg: 'rgba(52, 152, 219, 0.2)', color: '#74b9ff', border: 'rgba(52, 152, 219, 0.4)' },
            'descoberto': { bg: 'rgba(58, 134, 255, 0.2)', color: '#93c5fd', border: 'rgba(58, 134, 255, 0.4)' },
            'concluida': { bg: 'rgba(46, 204, 113, 0.2)', color: '#55efc4', border: 'rgba(46, 204, 113, 0.4)' }
        };
        const sc = statusColors[node.status] || statusColors['ativo'];
        statusPill.style.background = sc.bg;
        statusPill.style.color = sc.color;
        statusPill.style.border = `1px solid ${sc.border}`;

        const body = document.getElementById('inspector-body');
        const actions = document.getElementById('inspector-actions');
        body.innerHTML = '';
        actions.innerHTML = '';

        const meta = node.metadata || {};
        const nt = node.node_type;

        this.buildInspectorAttributes(body, meta, nt);
        this.buildInspectorLore(body, meta);
        this.buildInspectorActions(actions, node);

        drawer.classList.remove('hidden');
    },

    buildInspectorAttributes(body, meta, nodeType) {
        const attrPairs = [];

        if (nodeType === 'capital' || nodeType === 'estrutura' || nodeType === 'fortificacao' || nodeType === 'santuario' || nodeType === 'posto_avancado') {
            if (meta.nivel) attrPairs.push(['Nível', meta.nivel]);
            if (meta.bonus) attrPairs.push(['Bônus', meta.bonus]);
            if (meta.producao) attrPairs.push(['Produção', meta.producao]);
            if (meta.capacidade) attrPairs.push(['Capacidade', meta.capacidade]);
            if (meta.dono) attrPairs.push(['Controle', meta.dono]);
        }

        if (nodeType === 'exercito' || nodeType === 'tropa') {
            if (meta.tropas) attrPairs.push(['Tropas', `⚔️ ${meta.tropas}`]);
            if (meta.comandante) attrPairs.push(['Comandante', `🎖️ ${meta.comandante}`]);
            if (meta.poder_combate) attrPairs.push(['Poder', `💪 ${meta.poder_combate}`]);
            if (meta.moral) attrPairs.push(['Moral', `🏳️ ${meta.moral}`]);
            if (meta.localizacao) attrPairs.push(['Localização', `📍 ${meta.localizacao}`]);
        }

        if (nodeType === 'reino_vizinho') {
            if (meta.rei) attrPairs.push(['Soberano', `👑 ${meta.rei}`]);
            if (meta.populacao) attrPairs.push(['População', `👥 ${meta.populacao}`]);
            if (meta.poder_militar) attrPairs.push(['Militar', `⚔️ ${meta.poder_militar}`]);
            if (meta.relacionamento !== undefined) attrPairs.push(['Relação', meta.relacionamento]);
            if (meta.status_diplomatico) attrPairs.push(['Diplomacia', meta.status_diplomatico]);
        }

        if (nodeType === 'npc') {
            if (meta.lealdade) attrPairs.push(['Lealdade', `🤝 ${meta.lealdade}`]);
            if (meta.papel) attrPairs.push(['Papel', `📋 ${meta.papel}`]);
            if (meta.localizacao) attrPairs.push(['Localização', `📍 ${meta.localizacao}`]);
        }

        if (nodeType === 'quest') {
            if (meta.objetivo) attrPairs.push(['Objetivo', `🎯 ${meta.objetivo}`]);
            if (meta.progresso !== undefined) attrPairs.push(['Progresso', `📊 ${meta.progresso}%`]);
            if (meta.prazo) attrPairs.push(['Prazo', `⏳ ${meta.prazo}`]);
            if (meta.recompensa) attrPairs.push(['Recompensa', `💰 ${meta.recompensa}`]);
        }

        if (meta.perigo) attrPairs.push(['Ameaça', `⚠️ ${meta.perigo}`]);
        if (meta.recursos) attrPairs.push(['Recursos', `💎 ${meta.recursos}`]);

        Object.keys(meta).forEach(k => {
            const skip = ['detalhes', 'lore', 'descricao', 'tropas', 'comandante', 'poder_combate', 'moral', 'localizacao', 'nivel', 'bonus', 'producao', 'capacidade', 'dono', 'rei', 'populacao', 'poder_militar', 'relacionamento', 'status_diplomatico', 'lealdade', 'papel', 'objetivo', 'progresso', 'prazo', 'recompensa', 'perigo', 'recursos'];
            if (!skip.includes(k)) {
                attrPairs.push([k, meta[k]]);
            }
        });

        if (attrPairs.length > 0) {
            const sectionTitle = document.createElement('div');
            sectionTitle.className = 'inspector-section-title';
            sectionTitle.textContent = 'ATRIBUTOS';
            body.appendChild(sectionTitle);

            const grid = document.createElement('div');
            grid.className = 'inspector-attr-grid';

            attrPairs.forEach(([label, value]) => {
                const attr = document.createElement('div');
                attr.className = 'inspector-attr';
                attr.innerHTML = `<span class="inspector-attr-label">${label}</span><span class="inspector-attr-value">${value}</span>`;
                grid.appendChild(attr);
            });

            body.appendChild(grid);
        }

        if (meta.relacionamento !== undefined && (nodeType === 'reino_vizinho')) {
            const rel = Math.max(-100, Math.min(100, Number(meta.relacionamento)));
            const pct = ((rel + 100) / 200) * 100;
            const barColor = rel >= 60 ? '#2ecc71' : (rel >= 0 ? '#f1c40f' : '#e74c3c');

            const sectionTitle = document.createElement('div');
            sectionTitle.className = 'inspector-section-title';
            sectionTitle.textContent = 'RELAÇÃO DIPLOMÁTICA';
            body.appendChild(sectionTitle);

            const bar = document.createElement('div');
            bar.className = 'inspector-diplomacy-bar';
            bar.innerHTML = `
                <div class="inspector-therm-row">
                    <span>Nível de Relação</span>
                    <strong style="color: ${barColor};">${rel > 0 ? '+' : ''}${rel} / 100</strong>
                </div>
                <div class="inspector-therm-bar">
                    <div class="inspector-therm-fill" style="width: ${pct}%; background: ${barColor};"></div>
                </div>
            `;
            body.appendChild(bar);
        }
    },

    buildInspectorLore(body, meta) {
        const loreText = meta.lore || meta.descricao || meta.detalhes;
        if (!loreText) return;

        const sectionTitle = document.createElement('div');
        sectionTitle.className = 'inspector-section-title';
        sectionTitle.textContent = 'CONTEXTO & LORE';
        body.appendChild(sectionTitle);

        const loreEl = document.createElement('div');
        loreEl.className = 'inspector-lore';
        loreEl.textContent = loreText;
        body.appendChild(loreEl);
    },

    buildInspectorActions(container, node) {
        const nt = node.node_type;
        const actionDefs = [];

        if (nt === 'exercito' || nt === 'tropa') {
            actionDefs.push({ icon: '🚶', text: `Marchar ${node.label} para fronteira norte`, cmd: `Ordenar ${node.label} a marchar para a fronteira norte` });
            actionDefs.push({ icon: '🏋️', text: `Treinar recrutas de ${node.label}`, cmd: `Treinar novos recrutas para ${node.label}` });
            actionDefs.push({ icon: '🎖️', text: `Designar comandante`, cmd: `Designar um novo comandante para ${node.label}` });
        } else if (nt === 'reino_vizinho') {
            actionDefs.push({ icon: '🕊️', text: `Enviar embaixador`, cmd: `Enviar um embaixador para ${node.label}` });
            actionDefs.push({ icon: '📜', text: `Propor aliança`, cmd: `Propor aliança comercial com ${node.label}` });
            actionDefs.push({ icon: '⚔️', text: `Declarar guerra`, cmd: `Declarar guerra contra ${node.label}` });
        } else if (nt === 'capital') {
            actionDefs.push({ icon: '🏗️', text: `Expandir fortificações`, cmd: `Expandir as fortificações da capital` });
            actionDefs.push({ icon: '📢', text: `Convocar conselho de guerra`, cmd: `Convocar conselho de guerra na capital` });
        } else if (nt === 'estrutura' || nt === 'fortificacao' || nt === 'santuario') {
            actionDefs.push({ icon: '🔨', text: `Melhorar ${node.label}`, cmd: `Investir na melhoria de ${node.label}` });
            actionDefs.push({ icon: '👁️', text: `Inspecionar ${node.label}`, cmd: `Inspecionar o estado de ${node.label}` });
        } else if (nt === 'npc') {
            actionDefs.push({ icon: '💬', text: `Conversar com ${node.label}`, cmd: `Iniciar conversa com ${node.label}` });
            actionDefs.push({ icon: '📋', text: `Dar missão`, cmd: `Dar uma missão para ${node.label}` });
        } else if (nt === 'quest') {
            actionDefs.push({ icon: '🔍', text: `Investigar mais`, cmd: `Investigar mais sobre a quest "${node.label}"` });
            actionDefs.push({ icon: '⚔️', text: `Focar recursos nesta quest`, cmd: `Priorizar e focar recursos na quest "${node.label}"` });
        } else if (nt === 'rumor') {
            actionDefs.push({ icon: '🕵️', text: `Investigar rumor`, cmd: `Enviar espiões para investigar "${node.label}"` });
        } else {
            actionDefs.push({ icon: '🔍', text: `Investigar ${node.label}`, cmd: `Investigar ${node.label}` });
            actionDefs.push({ icon: '🚶', text: `Enviar tropas`, cmd: `Enviar tropas para ${node.label}` });
        }

        if (actionDefs.length === 0) return;

        const sectionTitle = document.createElement('div');
        sectionTitle.className = 'inspector-section-title';
        sectionTitle.textContent = 'AÇÕES RÁPIDAS';
        container.appendChild(sectionTitle);

        actionDefs.forEach(def => {
            const btn = document.createElement('button');
            btn.className = 'inspector-action-btn';
            btn.innerHTML = `<span>${def.icon}</span> ${def.text}`;
            btn.onclick = () => {
                const input = document.getElementById('action-input');
                if (input) {
                    input.value = def.cmd;
                    input.focus();
                    const form = document.getElementById('action-form');
                    if (form) form.dispatchEvent(new Event('submit'));
                }
                this.closeInspector();
            };
            container.appendChild(btn);
        });
    },

    closeInspector() {
        const drawer = document.getElementById('inspector-drawer');
        if (drawer) {
            drawer.classList.add('hidden');
        }
        this.inspectorOpen = false;
    }
};
