# Speech to Text Recorder

Aplikasi untuk merekam suara dari microphone dan mengkonversinya menjadi text menggunakan Together AI (Whisper model).

## Setup

### Prerequisites
#### 1 Clean up previous attempts (if any):
```bash
brew uninstall portaudio
pip uninstall pyaudio
```
#### 2. Update your system tools:
```bash
brew update
python3 -m pip install --upgrade pip setuptools wheel
```

#### 3. Install portaudio:
```bash
brew install portaudio
```

#### 4. Install PyAudio:
```bash
pip install pyaudio
```

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note untuk macOS**: Jika ada error saat install PyAudio, install portaudio terlebih dahulu:
```bash
brew install portaudio
pip install pyaudio
```

2. Setup API Key:
   - Copy `.env.example` menjadi `.env`
   - Isi `TOGETHER_API_KEY` dengan API key dari [Together AI](https://api.together.xyz/)

```bash
cp .env.example .env
# Edit .env dan isi TOGETHER_API_KEY
```


## Cara Menggunakan

Jalankan program:
```bash
python main.py
```

Program akan:
1. 🎤 Merekam suara dari microphone (default 5 detik)
2. 💾 Menyimpan audio ke folder `recordings/`
3. 🔄 Mengkonversi audio ke text menggunakan Together AI
4. 💾 Menyimpan hasil transcription ke `transcriptions/transcriptions.csv`

## Fitur

- ✅ Recording audio dari microphone
- ✅ Auto-detect bahasa
- ✅ Menyimpan audio dalam format WAV
- ✅ Export hasil ke CSV dengan informasi lengkap (timestamp, file, text, bahasa, durasi)
- ✅ Support custom durasi recording

## Output

- **Audio files**: `recordings/recording_YYYYMMDD_HHMMSS.wav`
- **Transcriptions**: `transcriptions/transcriptions.csv`

Format CSV:
- timestamp: Waktu transcription
- audio_file: Path ke file audio
- text: Hasil transcription
- language: Bahasa yang terdeteksi
- duration: Durasi audio (detik)
