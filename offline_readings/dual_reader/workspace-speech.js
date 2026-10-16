/* One speech session follows the active pane. Text is requested only on Read aloud. */
(() => {
  'use strict';
  class OpenBooksSpeech {
    constructor(getActive) {
      this.getActive = getActive;
      this.synth = window.speechSynthesis;
      this.token = 0; this.state = 'idle'; this.chunks = []; this.index = 0;
      this.$ = id => document.getElementById(id);
      try { this.options = JSON.parse(localStorage.getItem('open-books-speech-v1')) || {}; }
      catch { this.options = {}; }
      this.$('speechRate').value = String(this.options.rate || 1);
      this.$('speechRead').onclick = () => this.start();
      this.$('speechPause').onclick = () => this.pause();
      this.$('speechStop').onclick = () => this.stop();
      for (const id of ['speechVoice', 'speechRate']) this.$(id).onchange = () => {
        this.stop();
        this.options = {voice: this.$('speechVoice').value, rate: Number(this.$('speechRate').value)};
        try { localStorage.setItem('open-books-speech-v1', JSON.stringify(this.options)); } catch {}
      };
      this.voicesChanged = () => this.voices();
      this.synth?.addEventListener('voiceschanged', this.voicesChanged);
      window.addEventListener('pagehide', () => this.stop());
      this.voices(); this.update();
    }
    voices() {
      const selected = this.$('speechVoice').value || this.options.voice;
      const voices = this.synth?.getVoices() || [];
      this.$('speechVoice').replaceChildren(new Option('System default', ''), ...voices.map(v => new Option(`${v.name} · ${v.lang}${v.localService ? ' · device' : ' · online'}`, v.voiceURI)));
      if (voices.some(v => v.voiceURI === selected)) this.$('speechVoice').value = selected;
    }
    context() {
      const pane = this.getActive();
      if (this.owner && (pane !== this.owner || pane.generation !== this.generation || (pane.record.view.page || 1) !== this.page)) this.stop();
      this.update();
    }
    update(message) {
      const pane = this.getActive(), format = pane?.document?.format;
      const supported = !!this.synth && typeof window.SpeechSynthesisUtterance === 'function';
      const nativePdf = format === 'pdf' && location.protocol === 'file:';
      const canRead = supported && pane?.ready && format !== 'image' && !nativePdf;
      this.$('speechRead').disabled = !canRead || this.state !== 'idle';
      this.$('speechPause').disabled = !['speaking', 'paused'].includes(this.state);
      this.$('speechStop').disabled = this.state === 'idle';
      this.$('speechPause').textContent = this.state === 'paused' ? 'Resume' : 'Pause';
      for (const id of ['speechVoice', 'speechRate']) this.$(id).disabled = !supported;
      this.$('speechStatus').textContent = message || (this.state === 'loading' ? 'Preparing text…' : this.state === 'speaking' ? `Reading ${this.index + 1} of ${this.chunks.length}` : this.state === 'paused' ? 'Paused' : !supported ? 'Read aloud is unavailable in this browser.' : nativePdf ? 'For PDF read aloud, open the hosted reader. Native local-file PDFs cannot expose text.' : format === 'image' ? 'Images have no readable text; OCR is not included.' : !pane?.ready ? 'Open a document to read aloud.' : format === 'pdf' ? 'Reads the current PDF page; scanned pages need OCR.' : format === 'epub' ? 'Reads the current EPUB section.' : 'Reads this text document.');
    }
    stop() {
      this.token++; this.synth?.cancel(); this.state = 'idle'; this.owner = null;
      this.utterance = null; this.chunks = []; this.index = 0; this.update();
    }
    async start() {
      const pane = this.getActive();
      if (!pane?.ready || this.$('speechRead').disabled) return;
      this.stop();
      this.owner = pane; this.generation = pane.generation; this.page = pane.record.view.page || 1;
      const token = this.token;
      this.state = 'loading'; this.update();
      try {
        const text = (await pane.readableText()).replace(/\s+/g, ' ').trim();
        if (token !== this.token) return;
        if (!text) { this.stop(); this.update('No readable text found. Scanned PDFs and images require OCR.'); return; }
        // Queue short utterances sequentially so long documents do not stall the engine.
        const words = text.split(' '); let chunk = '';
        for (const word of words) {
          if (chunk.length + word.length > 500 && chunk) { this.chunks.push(chunk); chunk = ''; }
          if (word.length > 500) { if (chunk) { this.chunks.push(chunk); chunk = ''; } for (let i = 0; i < word.length; i += 500) this.chunks.push(word.slice(i, i + 500)); }
          else chunk += (chunk ? ' ' : '') + word;
        }
        if (chunk) this.chunks.push(chunk);
        this.state = 'speaking'; this.speak(token);
      } catch (error) { if (token === this.token) { this.stop(); this.update(error.message || 'Could not prepare text for speech.'); } }
    }
    speak(token) {
      if (token !== this.token) return;
      if (this.index >= this.chunks.length) { this.stop(); this.update('Finished reading.'); return; }
      const utterance = new SpeechSynthesisUtterance(this.chunks[this.index]);
      this.utterance = utterance;
      utterance.voice = this.synth.getVoices().find(v => v.voiceURI === this.$('speechVoice').value) || null;
      if (utterance.voice) utterance.lang = utterance.voice.lang;
      utterance.rate = Number(this.$('speechRate').value) || 1;
      utterance.onend = () => { if (token === this.token) { this.index++; if (this.state !== 'paused') this.speak(token); } };
      utterance.onerror = event => { if (token === this.token) { this.stop(); this.update(`Speech could not continue (${event.error || 'voice unavailable'}).`); } };
      this.update(); this.synth.speak(utterance);
    }
    pause() {
      if (this.state === 'speaking') { this.state = 'paused'; this.synth.pause(); }
      else if (this.state === 'paused') {
        this.state = 'speaking'; this.synth.resume();
        if (!this.synth.speaking) this.speak(this.token);
      }
      this.update();
    }
  }
  window.OpenBooksSpeech = OpenBooksSpeech;
})();
