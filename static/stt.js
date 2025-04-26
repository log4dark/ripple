
// static/stt.js

// 파일 업로드 처리
//
document.getElementById("upload-form").addEventListener("submit", async e => {
  e.preventDefault();
  const form = new FormData(e.target);
  const res = await fetch("/stt/upload", { method: "POST", body: form });
  const json = await res.json();

  const box = document.getElementById("stt-result");
  box.innerHTML = ""; // 기존 내용 초기화

  if (json.raw) {
    const rawDiv = document.createElement("div");
    rawDiv.innerHTML = "<b>🧾 원문 STT 결과:</b><br>🔸 " + json.raw.trim(); 
    //rawDiv.innerHTML = "<b>🧾 원문 STT 결과:</b><br>" + json.raw.split(/(?<=[.?!])\s+/).map(line => "🔸 " + line.trim()).join("<br>");
    box.appendChild(rawDiv);
  }

  if (json.text) {
    const finalDiv = document.createElement("div");
    finalDiv.innerHTML = "<br><b>🎯 후처리 결과:</b><br>📄 " + json.text.trim();
    //finalDiv.innerHTML = "<br><b>🎯 후처리 결과:</b><br>" + json.text.split(/(?<=[.?!])\s+/).map(line => "📄 " + line.trim()).join("<br>");
    box.appendChild(finalDiv);
  }

  box.scrollTop = box.scrollHeight;
});

// 실시간 스트림 처리
//
let ws, mediaStream, mediaRecorder, recorder;
let recordedChunks = [];

async function startMic() {
  const status = document.getElementById("status-text");
  if (status) status.textContent = "🎤 Whisper 듣는 중...";

  recordedChunks = [];

  mediaStream = await navigator.mediaDevices.getUserMedia({
    audio: {
      sampleRate: 44100, // 실제는 이걸 기준으로 리샘플링
      channelCount: 1,
      echoCancellation: true,
      noiseSuppression: true,
      autoGainControl: true
    }
  });

  ws = new WebSocket(`ws://${location.host}/ws/stt/stream`);
  ws.onopen = () => console.log("✅ WebSocket 연결됨");
  ws.onclose = () => console.log("❌ WebSocket 닫힘");

  ws.onmessage = (e) => {
    const box = document.getElementById("stt-result");
    const line = document.createElement("div");
    line.textContent = e.data;
    box.appendChild(line);
    box.scrollTop = box.scrollHeight;
  };

  const audioContext = new AudioContext();
  const source = audioContext.createMediaStreamSource(mediaStream);
  const processor = audioContext.createScriptProcessor(4096, 1, 1);
  const inputSampleRate = audioContext.sampleRate;

  processor.onaudioprocess = (e) => {
    const input = e.inputBuffer.getChannelData(0);
    const ratio = inputSampleRate / 16000;
    const downsampled = new Int16Array(Math.floor(input.length / ratio));

    for (let i = 0; i < downsampled.length; i++) {
      const idx = Math.floor(i * ratio);
      downsampled[i] = Math.max(-32768, Math.min(32767, input[idx] * 32767));
    }

    if (ws.readyState === WebSocket.OPEN) {
      ws.send(downsampled.buffer);
    }
  };

  source.connect(processor);
  processor.connect(audioContext.destination);

  // WebPlayer 녹음용 MediaRecorder
  recorder = new MediaRecorder(mediaStream, { mimeType: "audio/webm" });
  recorder.ondataavailable = event => {
    if (event.data.size > 0) recordedChunks.push(event.data);
  };
  recorder.start();

  mediaRecorder = { context: audioContext, processor, source };
}

function stopMic() {
  if (recorder && recorder.state !== "inactive") {
    recorder.stop(); // ✅ MediaRecorder에 stop 명확히 호출!
    console.log("🛑 녹음 종료됨");
  }

  if (mediaRecorder?._processor) mediaRecorder._processor.disconnect();
  if (mediaRecorder?._source) mediaRecorder._source.disconnect();
  if (mediaRecorder?._context && mediaRecorder._context.state !== "closed") {
    mediaRecorder._context.close();
  }

  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.close();
  }

  console.log("📴 마이크 및 WebSocket 종료");
}

function recordAndPlay() {
  if (recordedChunks.length === 0) {
    console.warn("❗ 녹음된 데이터가 없습니다.");
    return;
  }

  const blob = new Blob(recordedChunks, { type: "audio/webm" });
  const url = URL.createObjectURL(blob);
  const audio = document.getElementById("player");
  if (audio) {
    audio.src = url;
    audio.play();
  }
}

