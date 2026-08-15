const AUDIO_TRACKS = {
    "aventura": { name: "Aventura (Taverna)", file: "clima de aventura.mp3" },
    "calmo": { name: "Calmo", file: "clima de calmo.mp3" },
    "frenetico": { name: "Frenético", file: "clima frenetico.mp3" },
    "harmonia": { name: "Harmonia", file: "clima de harmonia.mp3" },
    "desenvolvimento": { name: "Desenvolvimento", file: "clima de desenvolvimento.mp3" },
    "desespero": { name: "Desespero", file: "clima de desespero.mp3" }
};

class AudioManager {
    constructor() {
        this.audio = new Audio();
        this.audio.loop = true;
        this.audio.volume = 0.35;
        this.isPlaying = false;
        
        // Restore mute preference (default: unmuted / music ON)
        const savedMute = localStorage.getItem('rpg_audio_muted');
        this.isMuted = savedMute === 'true';

        const savedTrack = localStorage.getItem('rpg_audio_track');
        this.currentTrackKey = (savedTrack && AUDIO_TRACKS[savedTrack]) ? savedTrack : 'aventura';

        // Unlock listeners for browser autoplay restriction
        this.unlockHandler = this.unlockAudio.bind(this);
        this.setupUnlockListeners();

        // Initial track setup
        this.setTrack(this.currentTrackKey, false);

        // Try playing immediately if user preference is unmuted
        if (!this.isMuted) {
            this.play();
        } else {
            this.updateUI();
        }
    }

    setupUnlockListeners() {
        const events = ['click', 'keydown', 'touchstart', 'pointerdown'];
        events.forEach(evt => {
            document.addEventListener(evt, this.unlockHandler, { capture: true, once: false });
        });
    }

    unlockAudio() {
        if (!this.isMuted && (!this.isPlaying || this.audio.paused)) {
            this.play();
        }
    }

    updateThemeFromModel(climaKey) {
        if (!climaKey) return;
        const normalized = String(climaKey).trim().toLowerCase();
        let targetKey = 'aventura';

        for (const key of Object.keys(AUDIO_TRACKS)) {
            if (normalized.includes(key)) {
                targetKey = key;
                break;
            }
        }

        this.setTrack(targetKey, true);
    }

    setTrack(trackKey, forcePlay = true) {
        if (!AUDIO_TRACKS[trackKey]) return;
        
        const isNewTrack = (this.currentTrackKey !== trackKey);
        this.currentTrackKey = trackKey;
        localStorage.setItem('rpg_audio_track', trackKey);

        const trackFile = AUDIO_TRACKS[trackKey].file;
        const targetSrc = `assets/musicas/${encodeURIComponent(trackFile)}`;

        if (isNewTrack || !this.audio.src || !this.audio.src.includes(encodeURIComponent(trackFile))) {
            this.audio.src = targetSrc;
        }

        if (!this.isMuted && (forcePlay || isNewTrack)) {
            this.play();
        } else {
            this.updateUI();
        }
    }

    togglePlay() {
        if (!this.isMuted && this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        this.isMuted = false;
        localStorage.setItem('rpg_audio_muted', 'false');
        
        if (!this.audio.src || this.audio.src === 'about:blank' || this.audio.src.endsWith('/')) {
            const trackFile = AUDIO_TRACKS[this.currentTrackKey].file;
            this.audio.src = `assets/musicas/${encodeURIComponent(trackFile)}`;
        }

        const playPromise = this.audio.play();
        if (playPromise !== undefined) {
            playPromise.then(() => {
                this.isPlaying = true;
                this.updateUI();
            }).catch(err => {
                console.warn('Audio play deferred (awaiting user gesture):', err);
                this.isPlaying = false;
                this.updateUI();
            });
        }
    }

    pause() {
        this.isMuted = true;
        localStorage.setItem('rpg_audio_muted', 'true');
        this.audio.pause();
        this.isPlaying = false;
        this.updateUI();
    }

    setVolume(val) {
        this.audio.volume = Math.max(0, Math.min(1, val));
    }

    updateBadgeUI() {
        const badgeEl = document.getElementById('audio-theme-badge');
        if (badgeEl) {
            const trackInfo = AUDIO_TRACKS[this.currentTrackKey] || AUDIO_TRACKS['aventura'];
            badgeEl.innerHTML = `<span>🎵 Clima: ${trackInfo.name} (IA)</span>`;
        }
    }

    updateUI() {
        const btn = document.getElementById('btn-audio-toggle');
        const iconSpan = document.getElementById('audio-status-icon');
        const labelSpan = document.getElementById('audio-status-label');
        
        if (btn && iconSpan && labelSpan) {
            if (!this.isMuted && this.isPlaying) {
                btn.classList.add('playing');
                iconSpan.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>`;
                labelSpan.textContent = 'Música: Ligada';
            } else if (!this.isMuted && !this.isPlaying) {
                btn.classList.remove('playing');
                iconSpan.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>`;
                labelSpan.textContent = 'Música: Ativando...';
            } else {
                btn.classList.remove('playing');
                iconSpan.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73 4.27 3zM12 4L9.91 6.09 12 8.18V4z"/></svg>`;
                labelSpan.textContent = 'Música: Desligada';
            }
        }
        this.updateBadgeUI();
    }
}

window.rpgAudio = new AudioManager();
