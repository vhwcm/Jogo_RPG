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

    updateStatusHUD(status, turnNum, race) {
        const prev = this.previousStatus;

        document.getElementById('val-reino').textContent = status.nome_reino || 'Valdrin';
        document.getElementById('val-imperador').textContent = status.imperador || 'Arthur';
        document.getElementById('val-dinheiro').textContent = (status.dinheiro || 0).toLocaleString();
        const popEl = document.getElementById('val-populacao');
        if (popEl) {
            popEl.textContent = (status.populacao || status.população || 10000).toLocaleString();
        }
        document.getElementById('val-militar').textContent = (status.poder_militar || 0).toLocaleString();
        document.getElementById('val-felicidade').textContent = status.felicidade || '70%';
        document.getElementById('val-religiao').textContent = status.religião || 'Nenhuma';
        document.getElementById('val-turno').textContent = turnNum || 1;

        if (race) {
            this.updateRaceVisuals(race);
        }

        // Trigger Notifications & HUD Highlights on Status Changes
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
        void el.offsetWidth; // Trigger reflow
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
        
        // Update race badge text
        const badgeEl = document.getElementById('val-raca');
        if (badgeEl) badgeEl.textContent = normRace.toUpperCase();

        // Update leader portrait image
        const portraitImg = document.getElementById('ruler-portrait');
        if (portraitImg) {
            portraitImg.src = `assets/lideres/${encodeURIComponent(assetInfo.leader)}`;
        }

        // Update background kingdom landscape image
        const bgOverlay = document.getElementById('bg-overlay');
        if (bgOverlay) {
            const bgPath = `assets/reinos/${encodeURIComponent(assetInfo.reino)}`;
            bgOverlay.style.backgroundImage = `linear-gradient(rgba(5, 5, 8, 0.82), rgba(5, 5, 8, 0.98)), url('${bgPath}')`;
            bgOverlay.style.backgroundSize = 'cover';
            bgOverlay.style.backgroundPosition = 'center';
        }
    },

    appendNarrativeBlock(text, speaker = "CONSELHO REAL") {
        const feed = document.getElementById('narrative-feed');
        const block = document.createElement('div');
        block.className = 'narrative-block';
        
        const speakerTag = document.createElement('div');
        speakerTag.className = 'speaker-tag';
        speakerTag.textContent = speaker;
        
        const storyText = document.createElement('div');
        storyText.className = 'story-text';
        storyText.textContent = text;
        
        block.appendChild(speakerTag);
        block.appendChild(storyText);
        feed.appendChild(block);
        
        feed.scrollTop = feed.scrollHeight;
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
            const optionLines = lines.filter(l => /^\s*(\d+[\.\)]|\*\*?\d+[\.\)]\*\*?)\s+/.test(l));
            if (optionLines.length > 0) {
                parsedOptions = optionLines.map(l => l.trim());
            } else {
                const inlineMatches = text.match(/(?:^|\s)(\d+[\.\)]\s+[^1-9\n]+?)(?=\s+\d+[\.\)]|$)/g);
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

                // Render Impact Badges if present
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

            const createdDate = c.created_at ? new Date(c.created_at).toLocaleDateString('pt-BR') : '';

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
                        ${createdDate ? `<span>Criado em: <strong>${createdDate}</strong></span>` : ''}
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

        // Bind button actions
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
    }
};
