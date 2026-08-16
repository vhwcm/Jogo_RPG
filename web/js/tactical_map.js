const TacticalMap = {
    canvas: null,
    ctx: null,
    wrapper: null,
    tooltip: null,
    nodes: [],
    edges: [],
    animId: null,
    isDestroyed: false,
    activeLayerFilter: 'all',

    camera: {
        x: 0,
        y: 0,
        zoom: 1.0,
        targetX: 0,
        targetY: 0,
        targetZoom: 1.0,
        isDragging: false,
        dragStartX: 0,
        dragStartY: 0,
        lastMouseX: 0,
        lastMouseY: 0
    },

    hoveredNode: null,
    selectedNode: null,
    particles: [],
    dashOffset: 0,
    warPulsePhase: 0,

    nodeSizes: {
        'mega': 32,
        'grande': 24,
        'medio': 18,
        'pequeno': 13,
        'micro': 10
    },

    nodeColors: {
        'capital': { border: '#d4af37', fill: 'rgba(212, 175, 55, 0.22)', glow: '#d4af37' },
        'bioma': { border: '#2a9d8f', fill: 'rgba(42, 157, 143, 0.2)', glow: '#2a9d8f' },
        'tropa': { border: '#3a86ff', fill: 'rgba(58, 134, 255, 0.2)', glow: '#3a86ff' },
        'exercito': { border: '#4a9eff', fill: 'rgba(74, 158, 255, 0.18)', glow: '#4a9eff' },
        'reino_vizinho': { border: '#8b5cf6', fill: 'rgba(139, 92, 246, 0.2)', glow: '#8b5cf6' },
        'estrutura': { border: '#e76f51', fill: 'rgba(231, 111, 81, 0.2)', glow: '#e76f51' },
        'fortificacao': { border: '#e63946', fill: 'rgba(230, 57, 70, 0.2)', glow: '#e63946' },
        'santuario': { border: '#f4a261', fill: 'rgba(244, 162, 97, 0.2)', glow: '#f4a261' },
        'monumento': { border: '#e0a96d', fill: 'rgba(224, 169, 109, 0.2)', glow: '#e0a96d' },
        'estatua': { border: '#ffd166', fill: 'rgba(255, 209, 102, 0.2)', glow: '#ffd166' },
        'obra': { border: '#f77f00', fill: 'rgba(247, 127, 0, 0.2)', glow: '#f77f00' },
        'ruina': { border: '#a8dadc', fill: 'rgba(168, 218, 220, 0.2)', glow: '#a8dadc' },
        'npc': { border: '#c084fc', fill: 'rgba(192, 132, 252, 0.18)', glow: '#c084fc' },
        'quest': { border: '#34d399', fill: 'rgba(52, 211, 153, 0.18)', glow: '#34d399' },
        'rumor': { border: '#94a3b8', fill: 'rgba(148, 163, 184, 0.12)', glow: '#94a3b8' },
        'mina': { border: '#fbbf24', fill: 'rgba(251, 191, 36, 0.18)', glow: '#fbbf24' },
        'vila': { border: '#a78bfa', fill: 'rgba(167, 139, 250, 0.18)', glow: '#a78bfa' },
        'porto': { border: '#38bdf8', fill: 'rgba(56, 189, 248, 0.18)', glow: '#38bdf8' },
        'posto_avancado': { border: '#34d399', fill: 'rgba(52, 211, 153, 0.15)', glow: '#34d399' },
        'floresta': { border: '#22c55e', fill: 'rgba(34, 197, 94, 0.15)', glow: '#22c55e' },
        'montanha': { border: '#78716c', fill: 'rgba(120, 113, 108, 0.18)', glow: '#78716c' }
    },

    typeLabels: {
        'capital': 'Capital Imperial',
        'bioma': 'Bioma / Região',
        'floresta': 'Floresta Selvagem',
        'montanha': 'Cordilheira Montanhosa',
        'mina': 'Mina de Extração',
        'vila': 'Vila Camponesa',
        'tropa': 'Divisão Militar',
        'exercito': 'Força Militar',
        'reino_vizinho': 'Reino Vizinho',
        'estrutura': 'Construção do Reino',
        'fortificacao': 'Fortaleza de Defesa',
        'posto_avancado': 'Posto Avançado',
        'santuario': 'Santuário Sagrado',
        'monumento': 'Monumento do Reino',
        'estatua': 'Estátua Sagrada',
        'obra': 'Grande Obra / Edificação',
        'ruina': 'Ruína Antiga',
        'porto': 'Porto Marítimo',
        'npc': 'Personagem / Conselheiro',
        'quest': 'Missão / Quest',
        'rumor': 'Rumor / Investigação'
    },

    edgeDiplomacyColors: {
        'alianca': { color: '#2ecc71', width: 2.2, dash: [] },
        'neutro': { color: '#3a86ff', width: 1.5, dash: [6, 4] },
        'tensao': { color: '#f1c40f', width: 2.0, dash: [4, 3] },
        'guerra': { color: '#e74c3c', width: 3.0, dash: [] }
    },

    init(canvasId, wrapperId, tooltipId) {
        this.canvas = document.getElementById(canvasId);
        this.wrapper = document.getElementById(wrapperId);
        this.tooltip = document.getElementById(tooltipId);
        if (!this.canvas || !this.wrapper) return;

        this.ctx = this.canvas.getContext('2d');
        this.isDestroyed = false;

        this.initParticles();
        this.resize();
        this.bindEvents();

        this.animate = this.animate.bind(this);
        this.animId = requestAnimationFrame(this.animate);
    },

    initParticles() {
        this.particles = [];
        for (let i = 0; i < 40; i++) {
            this.particles.push({
                x: (Math.random() - 0.5) * 1400,
                y: (Math.random() - 0.5) * 1400,
                radius: Math.random() * 1.6 + 0.5,
                alpha: Math.random() * 0.35 + 0.08,
                speedX: (Math.random() - 0.5) * 0.2,
                speedY: (Math.random() - 0.5) * 0.2
            });
        }
    },

    bindEvents() {
        window.addEventListener('resize', () => this.resize());

        const ro = new ResizeObserver(() => this.resize());
        ro.observe(this.wrapper);

        this.canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
        window.addEventListener('mousemove', (e) => this.onMouseMove(e));
        window.addEventListener('mouseup', (e) => this.onMouseUp(e));
        this.canvas.addEventListener('wheel', (e) => this.onWheel(e), { passive: false });

        this.canvas.addEventListener('touchstart', (e) => this.onTouchStart(e), { passive: false });
        this.canvas.addEventListener('touchmove', (e) => this.onTouchMove(e), { passive: false });
        this.canvas.addEventListener('touchend', (e) => this.onTouchEnd(e));
        this.canvas.addEventListener('mouseleave', () => this.onMouseLeave());
    },

    resize() {
        if (!this.canvas || !this.wrapper) return;
        const rect = this.wrapper.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;

        const w = Math.max(rect.width, 100);
        const h = Math.max(rect.height, 100);

        this.canvas.width = w * dpr;
        this.canvas.height = h * dpr;
        this.canvas.style.width = `${w}px`;
        this.canvas.style.height = `${h}px`;

        if (this.ctx) {
            this.ctx.setTransform(1, 0, 0, 1, 0, 0);
            this.ctx.scale(dpr, dpr);
        }
    },

    setData(nodes, edges) {
        const nodesMap = new Map();
        (nodes || []).forEach(n => {
            const existing = this.nodes.find(old => old.id === n.id);
            const nt = (n.node_type || 'estrutura').toLowerCase();
            const rawSize = (n.size || (n.metadata && n.metadata.size) || '').toLowerCase();
            let baseRadius = this.nodeSizes[rawSize];
            if (!baseRadius) {
                if (nt === 'capital' || nt === 'reino_vizinho') {
                    baseRadius = 32;
                } else if (nt === 'exercito' || nt === 'fortificacao' || nt === 'bioma' || nt === 'floresta' || nt === 'montanha') {
                    baseRadius = 24;
                } else if (nt === 'santuario' || nt === 'estatua' || nt === 'obra' || nt === 'monumento' || nt === 'totem' || nt === 'altar' || nt === 'ruina') {
                    baseRadius = 13;
                } else {
                    baseRadius = 18;
                }
            }
            nodesMap.set(n.id, {
                id: n.id,
                label: n.label || n.nome || 'Ponto',
                node_type: nt,
                emoji: n.emoji || '📍',
                x: typeof n.x === 'number' ? n.x : 0,
                y: typeof n.y === 'number' ? n.y : 0,
                status: n.status || 'ativo',
                size: rawSize || (baseRadius >= 30 ? 'mega' : (baseRadius >= 22 ? 'grande' : (baseRadius <= 14 ? 'pequeno' : 'medio'))),
                metadata: n.metadata || {},
                radius: baseRadius,
                currentRadius: existing ? existing.currentRadius : baseRadius
            });
        });

        this.nodes = Array.from(nodesMap.values());
        this.edges = (edges || []).map(e => ({
            id: e.id,
            source_node_id: e.source_node_id,
            target_node_id: e.target_node_id,
            edge_type: e.edge_type || 'estrada',
            descricao: e.descricao || ''
        }));

        const countEl = document.getElementById('map-nodes-count');
        if (countEl) {
            countEl.textContent = this.nodes.length;
        }
    },

    setLayerFilter(filter) {
        this.activeLayerFilter = filter || 'all';
    },

    isNodeVisible(node) {
        if (this.activeLayerFilter === 'all') return true;
        return node.node_type === this.activeLayerFilter;
    },

    zoomIn() {
        this.camera.targetZoom = Math.min(this.camera.targetZoom * 1.25, 3.2);
    },

    zoomOut() {
        this.camera.targetZoom = Math.max(this.camera.targetZoom / 1.25, 0.35);
    },

    recenter() {
        const capital = this.nodes.find(n => n.node_type === 'capital' || n.id === 'node_capital');
        if (capital) {
            this.camera.targetX = -capital.x;
            this.camera.targetY = -capital.y;
        } else {
            this.camera.targetX = 0;
            this.camera.targetY = 0;
        }
        this.camera.targetZoom = 1.0;
    },

    focusNode(nodeId) {
        const target = this.nodes.find(n => n.id === nodeId || (n.metadata && n.metadata.asset_id === nodeId));
        if (target) {
            this.selectedNode = target;
            this.camera.targetX = -target.x;
            this.camera.targetY = -target.y;
            this.camera.targetZoom = 1.35;
            window.dispatchEvent(new CustomEvent('node-inspect', { detail: target }));
        }
    },

    resetCamera() {
        this.camera.targetX = 0;
        this.camera.targetY = 0;
        this.camera.targetZoom = 1.0;
    },

    screenToWorld(screenX, screenY) {
        const rect = this.canvas.getBoundingClientRect();
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const wx = (screenX - rect.left - centerX - this.camera.x) / this.camera.zoom;
        const wy = (screenY - rect.top - centerY - this.camera.y) / this.camera.zoom;
        return { x: wx, y: wy };
    },

    findNodeAt(screenX, screenY) {
        const { x, y } = this.screenToWorld(screenX, screenY);
        for (let i = this.nodes.length - 1; i >= 0; i--) {
            const node = this.nodes[i];
            if (!this.isNodeVisible(node)) continue;
            const dx = node.x - x;
            const dy = node.y - y;
            const hitDist = (node.radius + 6);
            if (dx * dx + dy * dy <= hitDist * hitDist) {
                return node;
            }
        }
        return null;
    },

    onMouseDown(e) {
        if (e.button !== 0) return;
        this.camera.isDragging = true;
        this.camera.dragStartX = e.clientX - this.camera.x;
        this.camera.dragStartY = e.clientY - this.camera.y;
        this.camera.lastMouseX = e.clientX;
        this.camera.lastMouseY = e.clientY;
    },

    onMouseUp(e) {
        const dx = Math.abs(e.clientX - this.camera.lastMouseX);
        const dy = Math.abs(e.clientY - this.camera.lastMouseY);
        const wasClick = dx < 5 && dy < 5;

        if (wasClick) {
            const node = this.findNodeAt(e.clientX, e.clientY);
            if (node) {
                this.selectedNode = node;
                this.camera.targetX = -node.x;
                this.camera.targetY = -node.y;
                window.dispatchEvent(new CustomEvent('node-inspect', { detail: node }));
            } else {
                this.selectedNode = null;
                window.dispatchEvent(new CustomEvent('node-inspect-close'));
            }
        }

        this.camera.isDragging = false;
    },

    onMouseMove(e) {
        if (this.camera.isDragging) {
            this.camera.x = e.clientX - this.camera.dragStartX;
            this.camera.y = e.clientY - this.camera.dragStartY;
            this.camera.targetX = this.camera.x;
            this.camera.targetY = this.camera.y;
            this.hideTooltip();
            return;
        }

        const rect = this.canvas.getBoundingClientRect();
        if (
            e.clientX >= rect.left &&
            e.clientX <= rect.right &&
            e.clientY >= rect.top &&
            e.clientY <= rect.bottom
        ) {
            const node = this.findNodeAt(e.clientX, e.clientY);
            if (node !== this.hoveredNode) {
                this.hoveredNode = node;
                if (node) {
                    this.showTooltip(node, e.clientX, e.clientY);
                    this.canvas.style.cursor = 'pointer';
                } else {
                    this.hideTooltip();
                    this.canvas.style.cursor = 'grab';
                }
            } else if (node) {
                this.updateTooltipPosition(e.clientX, e.clientY);
            }
        }
    },

    onMouseLeave() {
        this.hoveredNode = null;
        this.hideTooltip();
    },

    onWheel(e) {
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.15 : 0.87;
        const newZoom = Math.min(Math.max(this.camera.targetZoom * factor, 0.35), 3.2);

        const rect = this.canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left - rect.width / 2;
        const mouseY = e.clientY - rect.top - rect.height / 2;

        const worldX = (mouseX - this.camera.x) / this.camera.zoom;
        const worldY = (mouseY - this.camera.y) / this.camera.zoom;

        this.camera.targetZoom = newZoom;
        this.camera.zoom = newZoom;
        this.camera.x = mouseX - worldX * newZoom;
        this.camera.y = mouseY - worldY * newZoom;
        this.camera.targetX = this.camera.x;
        this.camera.targetY = this.camera.y;

        const node = this.findNodeAt(e.clientX, e.clientY);
        if (node) {
            this.showTooltip(node, e.clientX, e.clientY);
        } else {
            this.hideTooltip();
        }
    },

    onTouchStart(e) {
        if (e.touches.length === 1) {
            const t = e.touches[0];
            this.camera.isDragging = true;
            this.camera.dragStartX = t.clientX - this.camera.x;
            this.camera.dragStartY = t.clientY - this.camera.y;
            this.camera.lastMouseX = t.clientX;
            this.camera.lastMouseY = t.clientY;

            const node = this.findNodeAt(t.clientX, t.clientY);
            if (node) {
                this.hoveredNode = node;
                this.showTooltip(node, t.clientX, t.clientY);
            }
        }
    },

    onTouchMove(e) {
        if (this.camera.isDragging && e.touches.length === 1) {
            e.preventDefault();
            const t = e.touches[0];
            this.camera.x = t.clientX - this.camera.dragStartX;
            this.camera.y = t.clientY - this.camera.dragStartY;
            this.camera.targetX = this.camera.x;
            this.camera.targetY = this.camera.y;
            this.hideTooltip();
        }
    },

    onTouchEnd(e) {
        if (this.camera.isDragging) {
            const dx = Math.abs((e.changedTouches[0]?.clientX || 0) - this.camera.lastMouseX);
            const dy = Math.abs((e.changedTouches[0]?.clientY || 0) - this.camera.lastMouseY);
            if (dx < 10 && dy < 10 && e.changedTouches[0]) {
                const node = this.findNodeAt(e.changedTouches[0].clientX, e.changedTouches[0].clientY);
                if (node) {
                    window.dispatchEvent(new CustomEvent('node-inspect', { detail: node }));
                }
            }
        }
        this.camera.isDragging = false;
    },

    showTooltip(node, clientX, clientY) {
        if (!this.tooltip || !this.wrapper) return;
        const meta = node.metadata || {};

        let metaRows = '';
        if (meta.tropas) {
            metaRows += `<div class="tooltip-meta-item"><span>Tropas:</span> <strong>⚔️ ${meta.tropas}</strong></div>`;
        }
        if (meta.comandante) {
            metaRows += `<div class="tooltip-meta-item"><span>Comandante:</span> <strong>🎖️ ${meta.comandante}</strong></div>`;
        }
        if (meta.moral) {
            metaRows += `<div class="tooltip-meta-item"><span>Moral:</span> <strong>💪 ${meta.moral}</strong></div>`;
        }
        if (meta.dono) {
            metaRows += `<div class="tooltip-meta-item"><span>Controle:</span> <strong>👑 ${meta.dono}</strong></div>`;
        }
        if (meta.perigo) {
            const dangerClass = meta.perigo.toLowerCase().includes('alto') ? 'text-danger' : (meta.perigo.toLowerCase().includes('médio') ? 'text-warning' : 'text-success');
            metaRows += `<div class="tooltip-meta-item"><span>Ameaça:</span> <strong class="${dangerClass}">⚠️ ${meta.perigo}</strong></div>`;
        }
        if (meta.recursos) {
            metaRows += `<div class="tooltip-meta-item"><span>Recursos:</span> <strong>💎 ${meta.recursos}</strong></div>`;
        }
        if (meta.lealdade) {
            metaRows += `<div class="tooltip-meta-item"><span>Lealdade:</span> <strong>🤝 ${meta.lealdade}</strong></div>`;
        }
        if (meta.papel) {
            metaRows += `<div class="tooltip-meta-item"><span>Papel:</span> <strong>📋 ${meta.papel}</strong></div>`;
        }
        if (meta.progresso !== undefined) {
            metaRows += `<div class="tooltip-meta-item"><span>Progresso:</span> <strong>📊 ${meta.progresso}%</strong></div>`;
        }
        if (meta.detalhes) {
            metaRows += `<div class="tooltip-meta-item"><span>Nota:</span> <em>${meta.detalhes}</em></div>`;
        }
        if (meta.rei) {
            metaRows += `<div class="tooltip-meta-item"><span>Soberano:</span> <strong>👑 ${meta.rei}</strong></div>`;
        }
        if (meta.raca) {
            metaRows += `<div class="tooltip-meta-item"><span>Raça:</span> <strong>🧬 ${meta.raca}</strong></div>`;
        }
        if (meta.poder_militar && node.node_type === 'reino_vizinho') {
            metaRows += `<div class="tooltip-meta-item"><span>Força Militar:</span> <strong>⚔️ ${meta.poder_militar}</strong></div>`;
        }
        if (meta.relacionamento !== undefined || meta.status_diplomatico) {
            const rel = meta.relacionamento !== undefined ? Math.max(-100, Math.min(100, Number(meta.relacionamento))) : 0;
            const barColor = rel >= 60 ? '#2ecc71' : (rel >= 0 ? '#f1c40f' : '#e74c3c');
            const statusLabel = (meta.status_diplomatico || (rel >= 60 ? 'Aliado' : (rel >= 0 ? 'Neutro' : 'Hostil'))).toUpperCase();
            metaRows += `
                <div class="tooltip-meta-item" style="margin-top: 6px; flex-direction: column; gap: 3px;">
                    <div style="display: flex; justify-content: space-between; width: 100%; font-size: 0.76rem;">
                        <span>Diplomacia: <strong style="color: ${barColor}">${statusLabel}</strong></span>
                        <strong style="color: ${barColor}">${rel > 0 ? '+' : ''}${rel} / 100</strong>
                    </div>
                    <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden;">
                        <div style="width: ${((rel + 100) / 200) * 100}%; height: 100%; background: ${barColor};"></div>
                    </div>
                </div>
            `;
        }

        const typeDisplay = this.typeLabels[node.node_type.toLowerCase()] || node.node_type;

        this.tooltip.innerHTML = `
            <div class="tooltip-header">
                <span class="tooltip-emoji">${node.emoji}</span>
                <div class="tooltip-title-group">
                    <div class="tooltip-name">${node.label}</div>
                    <div class="tooltip-type">${typeDisplay}</div>
                </div>
            </div>
            <div class="tooltip-body">
                <div class="tooltip-status-pill status-${node.status}">Status: ${node.status.toUpperCase()}</div>
                ${metaRows}
            </div>
        `;

        this.tooltip.classList.remove('hidden');
        this.updateTooltipPosition(clientX, clientY);
    },

    updateTooltipPosition(clientX, clientY) {
        if (!this.tooltip || !this.wrapper) return;
        const wrapRect = this.wrapper.getBoundingClientRect();
        const tipRect = this.tooltip.getBoundingClientRect();

        let posX = clientX - wrapRect.left + 14;
        let posY = clientY - wrapRect.top + 14;

        if (posX + tipRect.width > wrapRect.width - 8) {
            posX = clientX - wrapRect.left - tipRect.width - 14;
        }
        if (posY + tipRect.height > wrapRect.height - 8) {
            posY = clientY - wrapRect.top - tipRect.height - 14;
        }

        this.tooltip.style.left = `${Math.max(8, posX)}px`;
        this.tooltip.style.top = `${Math.max(8, posY)}px`;
    },

    hideTooltip() {
        if (this.tooltip) {
            this.tooltip.classList.add('hidden');
        }
    },

    animate() {
        if (this.isDestroyed) return;

        this.camera.x += (this.camera.targetX - this.camera.x) * 0.12;
        this.camera.y += (this.camera.targetY - this.camera.y) * 0.12;
        this.camera.zoom += (this.camera.targetZoom - this.camera.zoom) * 0.12;

        this.dashOffset = (this.dashOffset + 0.4) % 1000;
        this.warPulsePhase = (this.warPulsePhase + 0.03) % (Math.PI * 2);

        this.render();
        this.animId = requestAnimationFrame(this.animate);
    },

    render() {
        if (!this.ctx || !this.canvas) return;

        const rect = this.canvas.getBoundingClientRect();
        const width = rect.width;
        const height = rect.height;

        const grad = this.ctx.createRadialGradient(width / 2, height / 2, 40, width / 2, height / 2, Math.max(width, height) * 0.9);
        grad.addColorStop(0, '#10101c');
        grad.addColorStop(1, '#050509');
        this.ctx.fillStyle = grad;
        this.ctx.fillRect(0, 0, width, height);

        this.ctx.save();
        this.ctx.translate(width / 2 + this.camera.x, height / 2 + this.camera.y);
        this.ctx.scale(this.camera.zoom, this.camera.zoom);

        this.renderBackgroundGrid();
        this.renderParticles();
        this.renderEdges();
        this.renderNodes();

        this.ctx.restore();
    },

    renderBackgroundGrid() {
        const ctx = this.ctx;
        const gridSize = 60;
        const extent = 1400;

        ctx.strokeStyle = 'rgba(212, 175, 55, 0.035)';
        ctx.lineWidth = 1;

        ctx.beginPath();
        for (let x = -extent; x <= extent; x += gridSize) {
            ctx.moveTo(x, -extent);
            ctx.lineTo(x, extent);
        }
        for (let y = -extent; y <= extent; y += gridSize) {
            ctx.moveTo(-extent, y);
            ctx.lineTo(extent, y);
        }
        ctx.stroke();

        ctx.strokeStyle = 'rgba(212, 175, 55, 0.07)';
        ctx.beginPath();
        ctx.arc(0, 0, 180, 0, Math.PI * 2);
        ctx.arc(0, 0, 320, 0, Math.PI * 2);
        ctx.arc(0, 0, 480, 0, Math.PI * 2);
        ctx.stroke();
    },

    renderParticles() {
        const ctx = this.ctx;
        for (let p of this.particles) {
            p.x += p.speedX;
            p.y += p.speedY;
            if (p.x > 700) p.x = -700;
            if (p.x < -700) p.x = 700;
            if (p.y > 700) p.y = -700;
            if (p.y < -700) p.y = 700;

            ctx.fillStyle = `rgba(243, 229, 171, ${p.alpha * 0.3})`;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
        }
    },

    renderEdges() {
        const ctx = this.ctx;
        const nodeMap = new Map();
        this.nodes.forEach(n => nodeMap.set(n.id, n));

        for (let edge of this.edges) {
            const src = nodeMap.get(edge.source_node_id);
            const tgt = nodeMap.get(edge.target_node_id);
            if (!src || !tgt) continue;
            if (!this.isNodeVisible(src) && !this.isNodeVisible(tgt)) continue;

            const isHighlighted = this.hoveredNode && (this.hoveredNode.id === src.id || this.hoveredNode.id === tgt.id);
            const isDimmed = this.hoveredNode && !isHighlighted;

            ctx.save();
            ctx.beginPath();
            ctx.moveTo(src.x, src.y);
            ctx.lineTo(tgt.x, tgt.y);

            const diplomacy = this.edgeDiplomacyColors[edge.edge_type];
            if (diplomacy) {
                const alpha = isDimmed ? 0.12 : (isHighlighted ? 0.95 : 0.6);
                ctx.strokeStyle = diplomacy.color.replace(')', `, ${alpha})`).replace('rgb', 'rgba');
                if (diplomacy.color.startsWith('#')) {
                    const r = parseInt(diplomacy.color.slice(1, 3), 16);
                    const g = parseInt(diplomacy.color.slice(3, 5), 16);
                    const b = parseInt(diplomacy.color.slice(5, 7), 16);
                    ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, ${alpha})`;
                }
                ctx.lineWidth = isHighlighted ? diplomacy.width + 1 : diplomacy.width;
                ctx.setLineDash(diplomacy.dash);

                if (edge.edge_type === 'guerra') {
                    const warAlpha = 0.4 + 0.6 * Math.abs(Math.sin(this.warPulsePhase));
                    ctx.strokeStyle = `rgba(231, 76, 60, ${warAlpha})`;
                    ctx.shadowColor = '#e74c3c';
                    ctx.shadowBlur = 8;
                }
                if (edge.edge_type === 'tensao') {
                    ctx.lineDashOffset = -this.dashOffset;
                }
            } else if (edge.edge_type === 'fronteira') {
                ctx.strokeStyle = isHighlighted ? 'rgba(217, 64, 69, 0.95)' : (isDimmed ? 'rgba(217, 64, 69, 0.12)' : 'rgba(217, 64, 69, 0.55)');
                ctx.lineWidth = isHighlighted ? 2.5 : 1.6;
                ctx.setLineDash([6, 4]);
            } else if (edge.edge_type === 'rota') {
                ctx.strokeStyle = isHighlighted ? 'rgba(58, 134, 255, 0.95)' : (isDimmed ? 'rgba(58, 134, 255, 0.15)' : 'rgba(58, 134, 255, 0.6)');
                ctx.lineWidth = isHighlighted ? 2.8 : 1.8;
                ctx.setLineDash([8, 6]);
                ctx.lineDashOffset = -this.dashOffset * 0.8;
            } else {
                ctx.strokeStyle = isHighlighted ? 'rgba(212, 175, 55, 0.95)' : (isDimmed ? 'rgba(212, 175, 55, 0.15)' : 'rgba(212, 175, 55, 0.45)');
                ctx.lineWidth = isHighlighted ? 2.6 : 1.5;
                ctx.setLineDash([]);
            }

            if (isHighlighted && !diplomacy) {
                ctx.shadowColor = ctx.strokeStyle;
                ctx.shadowBlur = 10;
            }

            ctx.stroke();
            ctx.restore();
        }
    },

    renderNodes() {
        const ctx = this.ctx;

        for (let node of this.nodes) {
            if (!this.isNodeVisible(node)) continue;

            const isHovered = this.hoveredNode && this.hoveredNode.id === node.id;
            const isSelected = this.selectedNode && this.selectedNode.id === node.id;
            const isConnected = this.hoveredNode && this.edges.some(e =>
                (e.source_node_id === this.hoveredNode.id && e.target_node_id === node.id) ||
                (e.target_node_id === this.hoveredNode.id && e.source_node_id === node.id)
            );
            const isDimmed = this.hoveredNode && !isHovered && !isConnected;

            const baseRadius = node.radius;
            const targetRadius = isHovered ? baseRadius * 1.25 : (isConnected ? baseRadius * 1.1 : baseRadius);
            node.currentRadius += (targetRadius - node.currentRadius) * 0.2;

            ctx.save();
            ctx.translate(node.x, node.y);

            const colors = this.nodeColors[node.node_type.toLowerCase()] || this.nodeColors['estrutura'];

            const alpha = isDimmed ? 0.25 : 1.0;
            ctx.globalAlpha = alpha;

            if (node.node_type === 'capital' || node.size === 'mega') {
                ctx.shadowColor = colors.glow;
                ctx.shadowBlur = isHovered ? 24 : 15;
                ctx.beginPath();
                ctx.arc(0, 0, node.currentRadius + 5, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(212, 175, 55, ${isHovered ? 0.65 : 0.3})`;
                ctx.lineWidth = 1.2;
                ctx.setLineDash([3, 3]);
                ctx.stroke();
                ctx.setLineDash([]);
                ctx.shadowBlur = isHovered ? 24 : 15;
            } else if (isHovered || isSelected) {
                ctx.shadowColor = colors.glow;
                ctx.shadowBlur = node.radius <= 14 ? 10 : 18;
            }

            if (node.node_type === 'rumor') {
                ctx.setLineDash([4, 3]);
            }

            ctx.beginPath();
            ctx.arc(0, 0, node.currentRadius, 0, Math.PI * 2);
            ctx.fillStyle = colors.fill;
            ctx.fill();

            ctx.lineWidth = isHovered ? (node.radius <= 14 ? 1.8 : 2.5) : (node.radius <= 14 ? 1.2 : 1.8);
            ctx.strokeStyle = colors.border;
            ctx.stroke();

            ctx.setLineDash([]);
            ctx.shadowBlur = 0;

            if (node.node_type === 'quest' && node.status === 'em_andamento') {
                const pulseAlpha = 0.15 + 0.15 * Math.abs(Math.sin(this.warPulsePhase * 1.5));
                ctx.beginPath();
                ctx.arc(0, 0, node.currentRadius + 6, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(52, 211, 153, ${pulseAlpha})`;
                ctx.lineWidth = 2;
                ctx.stroke();
            }

            const badgeColor = node.status === 'hostil' ? '#d94045' : (node.status === 'em_marcha' ? '#3a86ff' : (node.status === 'em_andamento' ? '#34d399' : '#2a9d8f'));
            const badgeRadius = Math.max(2.5, Math.min(4, node.currentRadius * 0.22));
            ctx.beginPath();
            ctx.arc(node.currentRadius * 0.72, -node.currentRadius * 0.72, badgeRadius, 0, Math.PI * 2);
            ctx.fillStyle = badgeColor;
            ctx.fill();
            ctx.strokeStyle = '#050508';
            ctx.lineWidth = 1.0;
            ctx.stroke();

            const emojiSize = Math.max(9, Math.round(node.currentRadius * 1.05));
            ctx.font = `${emojiSize}px sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(node.emoji, 0, 1);

            const fontSize = node.radius <= 14 ? (isHovered ? '600 10px Inter, sans-serif' : '500 9px Inter, sans-serif') : (isHovered ? '600 11px Inter, sans-serif' : '500 10px Inter, sans-serif');
            ctx.font = fontSize;
            ctx.fillStyle = isHovered ? '#ffffff' : (isDimmed ? 'rgba(241, 241, 245, 0.3)' : 'rgba(241, 241, 245, 0.85)');
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';

            if (isHovered) {
                ctx.shadowColor = 'rgba(0, 0, 0, 0.9)';
                ctx.shadowBlur = 4;
            }
            ctx.fillText(node.label, 0, node.currentRadius + 4);

            if (node.node_type === 'reino_vizinho' || (node.metadata && (node.metadata.relacionamento !== undefined || node.metadata.status_diplomatico))) {
                const meta = node.metadata || {};
                const rel = meta.relacionamento !== undefined ? Number(meta.relacionamento) : 0;
                const status = (meta.status_diplomatico || '').toLowerCase();
                const diploColor = (status === 'aliado' || rel >= 60) ? '#2ecc71' : ((status === 'hostil' || status === 'guerra' || rel < 0) ? '#e74c3c' : '#f1c40f');
                
                ctx.beginPath();
                ctx.arc(0, 0, node.currentRadius + 3, 0, Math.PI * 2);
                ctx.strokeStyle = diploColor;
                ctx.lineWidth = isHovered ? 2.5 : 1.5;
                ctx.setLineDash([4, 2]);
                ctx.stroke();
                ctx.setLineDash([]);

                const sign = rel > 0 ? '+' : '';
                const icon = (status === 'aliado' || rel >= 60) ? '🤝' : ((status === 'hostil' || status === 'guerra' || rel < 0) ? '⚔️' : '⚖️');
                const badgeText = `${icon} ${sign}${rel}`;

                ctx.font = '700 9px Inter, sans-serif';
                const textMetrics = ctx.measureText(badgeText);
                const badgeW = textMetrics.width + 10;
                const badgeH = 14;
                const badgeY = node.currentRadius + 18;

                ctx.fillStyle = 'rgba(5, 5, 8, 0.85)';
                ctx.beginPath();
                ctx.roundRect(-badgeW / 2, badgeY, badgeW, badgeH, 4);
                ctx.fill();

                ctx.strokeStyle = diploColor;
                ctx.lineWidth = 1;
                ctx.stroke();

                ctx.fillStyle = diploColor;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(badgeText, 0, badgeY + badgeH / 2);
            }

            ctx.restore();
        }
    },

    destroy() {
        this.isDestroyed = true;
        if (this.animId) {
            cancelAnimationFrame(this.animId);
        }
    }
};

window.TacticalMap = TacticalMap;
