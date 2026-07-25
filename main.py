import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="3億円宝くじ",
    page_icon="🎰",
    layout="centered"
)

# Colabで動いていたUI・アニメーション・音声ロジック（HTML/CSS/JS）
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@700;900&display=swap');

  body {
    font-family: 'Noto Sans JP', sans-serif;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: #fff;
    text-align: center;
    padding: 15px;
    margin: 0;
  }
  .card {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid #f39c12;
    border-radius: 20px;
    padding: 25px 15px;
    box-shadow: 0 0 20px rgba(243, 156, 18, 0.3);
    max-width: 90%;
    width: 100%;
    margin: 0 auto;
    box-sizing: border-box;
  }
  h1 {
    font-size: 1.5rem;
    color: #f1c40f;
    text-shadow: 0 0 10px rgba(241, 196, 15, 0.5);
    margin-bottom: 20px;
  }
  .input-group {
    margin: 20px 0;
  }
  input[type="number"] {
    font-size: 2rem;
    width: 140px;
    text-align: center;
    padding: 10px;
    border-radius: 12px;
    border: 3px solid #f39c12;
    background: #0f3460;
    color: #fff;
    font-weight: bold;
    outline: none;
  }
  button {
    background: linear-gradient(45deg, #e67e22, #e74c3c);
    color: white;
    font-size: 1.3rem;
    font-weight: 900;
    padding: 15px 30px;
    border: none;
    border-radius: 50px;
    box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
    cursor: pointer;
    width: 80%;
    margin-top: 10px;
    transition: transform 0.1s;
  }
  button:active {
    transform: scale(0.95);
  }
  #status {
    font-size: 1.2rem;
    margin: 20px 0;
    min-height: 30px;
    color: #00d2d3;
    font-weight: bold;
  }
  .result-box {
    display: none;
    background: linear-gradient(45deg, #f1c40f, #f39c12);
    color: #000;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
    animation: bounce 0.6s ease;
  }
  .result-title {
    font-size: 1.8rem;
    font-weight: 900;
    margin: 0;
  }
  .prize {
    font-size: 1.1rem;
    font-weight: 900;
    color: #d35400;
    margin: 10px 0;
    text-shadow: 1px 1px 0 #fff;
    word-break: break-all;
  }
  @keyframes bounce {
    0% { transform: scale(0.3); opacity: 0; }
    50% { transform: scale(1.05); }
    70% { transform: scale(0.9); }
    100% { transform: scale(1); opacity: 1; }
  }
</style>
</head>
<body>

<div class="card">
  <h1>🎰 一獲千金！<br>運試し！3億円宝くじ</h1>
  <p style="font-size: 0.9rem; color: #ccc;">好きな3桁の数字を入れてね！</p>
  
  <div class="input-group">
    <input type="number" id="numInput" placeholder="777" min="0" max="999" oninput="if(value.length>3)value=value.slice(0,3)">
  </div>
  
  <button onclick="drawLottery()">運命の抽選ボタン🎯</button>
  
  <div id="status"></div>
  
  <div id="result" class="result-box">
    <div class="result-title">🎊 超大当り 🎊</div>
    <div>1等当選おめでとうございます！</div>
    <div class="prize">￥300,000,000</div>
    <div style="font-size: 0.8rem; font-weight: bold;">（3億円獲得確定！！）</div>
  </div>
</div>

<script>
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playDrumroll(durationMs) {
  const startTime = audioCtx.currentTime;
  const endTime = startTime + (durationMs / 1000);
  let time = startTime;
  
  let interval = 0.1;
  while (time < endTime) {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(120, time);
    osc.frequency.exponentialRampToValueAtTime(40, time + 0.05);
    
    gain.gain.setValueAtTime(0.3, time);
    gain.gain.exponentialRampToValueAtTime(0.01, time + 0.05);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    osc.start(time);
    osc.stop(time + 0.05);
    
    time += interval;
    interval = Math.max(0.03, interval * 0.92);
  }
}

function playCymbal() {
  const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  
  osc.type = 'sawtooth';
  osc.frequency.setValueAtTime(523.25, now);
  osc.frequency.setValueAtTime(659.25, now + 0.1);
  osc.frequency.setValueAtTime(783.99, now + 0.2);
  osc.frequency.setValueAtTime(1046.50, now + 0.3);
  
  gain.gain.setValueAtTime(0.5, now);
  gain.gain.exponentialRampToValueAtTime(0.01, now + 1.2);
  
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  
  osc.start(now);
  osc.stop(now + 1.2);
}

function drawLottery() {
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }

  const input = document.getElementById('numInput').value;
  const status = document.getElementById('status');
  const result = document.getElementById('result');
  
  if (input === '' || input.length < 1) {
    alert('3桁の数字を入れてね！');
    return;
  }
  
  result.style.display = 'none';
  status.innerHTML = 'ドゥルルルルル……🥁';
  
  playDrumroll(1500);
  
  setTimeout(() => {
    status.innerHTML = '✨ 奇跡の波形を検知！！ ✨';
  }, 800);
  
  setTimeout(() => {
    status.innerHTML = '';
    result.style.display = 'block';
    playCymbal();
  }, 1600);
}
</script>

</body>
</html>
"""

# Streamlitのコンポーネント機能でHTML/CSS/JSをレンダリング
components.html(html_code, height=600, scrolling=True)

