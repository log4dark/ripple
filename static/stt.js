
// static/stt.js

// 파일 업로드 처리
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
