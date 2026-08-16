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
                iconSpan.textContent = '🔊';
                labelSpan.textContent = 'Ligada';
            } else if (!this.isMuted && !this.isPlaying) {
                btn.classList.remove('playing');
                iconSpan.textContent = '🎵';
                labelSpan.textContent = 'Ativando...';
            } else {
                btn.classList.remove('playing');
                iconSpan.textContent = '🔇';
                labelSpan.textContent = 'Desligada';
            }
        }
        this.updateBadgeUI();
    }
}

window.rpgAudio = new AudioManager();
