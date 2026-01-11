import os
import csv
import wave
import pyaudio
import threading
from datetime import datetime
from pathlib import Path
from together import Together
from dotenv import load_dotenv

load_dotenv()

class SpeechToTextRecorder:
    def __init__(self):
        self.together_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.recordings_dir = Path("recordings")
        self.transcriptions_dir = Path("transcriptions")
        
        self.recordings_dir.mkdir(exist_ok=True)
        self.transcriptions_dir.mkdir(exist_ok=True)

    def record_audio(self):
        """Record audio from microphone and save as WAV file (start/stop)"""
        print("\nTekan 1 untuk START record")
        while True:
            cmd = input("Input (1=start): ").strip()
            if cmd == "1":
                break
            print("Input tidak valid. Tekan 1 untuk mulai.")

        print("\n🎤 Recording... (tekan 2 lalu Enter untuk STOP)")
        print("Start speaking now!")

        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        frames: list[bytes] = []
        stop_event = threading.Event()

        def _record_loop():
            while not stop_event.is_set():
                try:
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    frames.append(data)
                except Exception:
                    stop_event.set()

        thread = threading.Thread(target=_record_loop, daemon=True)
        thread.start()

        while True:
            cmd = input("Input (2=stop): ").strip()
            if cmd == "2":
                break
            print("Input tidak valid. Tekan 2 untuk stop.")

        stop_event.set()
        thread.join(timeout=2)

        print("✅ Recording finished!")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = self.recordings_dir / f"recording_{timestamp}.wav"

        with wave.open(str(audio_filename), "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(frames))

        print(f"💾 Audio saved to: {audio_filename}")
        return audio_filename
    
    def transcribe_audio(self, audio_file):
        """Convert audio to text using Together AI"""
        print(f"\n🔄 Transcribing audio using Together AI...")
        
        try:
            response = self.together_client.audio.transcriptions.create(
                file=str(audio_file),
                model="openai/whisper-large-v3",
                language="auto",
                response_format="verbose_json"
            )
            
            print("✅ Transcription completed!")
            return {
                'text': response.text,
                'language': response.language if hasattr(response, 'language') else 'unknown',
                'duration': response.duration if hasattr(response, 'duration') else 0
            }
        except Exception as e:
            print(f"❌ Error during transcription: {e}")
            return None
    
    def save_to_csv(self, audio_file, transcription_data):
        """Save transcription results to CSV file"""
        csv_filename = self.transcriptions_dir / "transcriptions.csv"
        
        file_exists = csv_filename.exists()
        
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'audio_file', 'text', 'language', 'duration']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'audio_file': str(audio_file),
                'text': transcription_data['text'],
                'language': transcription_data['language'],
                'duration': transcription_data['duration']
            })
        
        print(f"💾 Transcription saved to: {csv_filename}")
        return csv_filename
    
    def run(self):
        """Main workflow: record -> transcribe -> save"""
        print("=" * 60)
        print("🎙️  SPEECH TO TEXT RECORDER")
        print("=" * 60)

        audio_file = self.record_audio()
        
        transcription_data = self.transcribe_audio(audio_file)
        
        if transcription_data:
            print(f"\n📝 Transcription:")
            print(f"   Text: {transcription_data['text']}")
            print(f"   Language: {transcription_data['language']}")
            print(f"   Duration: {transcription_data['duration']:.2f}s")
            
            csv_file = self.save_to_csv(audio_file, transcription_data)
            
            print("\n" + "=" * 60)
            print("✅ Process completed successfully!")
            print("=" * 60)
        else:
            print("\n❌ Transcription failed!")


if __name__ == "__main__":
    recorder = SpeechToTextRecorder()

    recorder.run()
