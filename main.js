const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const statusBar = document.getElementById('status-bar');

let chatHistory = [];

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message');
    div.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    div.textContent = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    
    // 履歴に追加
    chatHistory.push({ role: sender, text: text });
}

// タイピングインジケーター（生成中のバブル）を表示
function showTypingIndicator() {
    const div = document.createElement('div');
    div.classList.add('message', 'bot-message', 'typing');
    div.id = 'typing-indicator';
    div.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// タイピングインジケーターを削除
function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';
    userInput.disabled = true;
    sendBtn.disabled = true;
    
    statusBar.textContent = "先生が考えています...";
    showTypingIndicator(); // バブルを表示

    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, history: chatHistory.slice(0, -1) }), // 最新のメッセージはmessageとして送るので履歴からは除く
        });

        const data = await response.json();
        hideTypingIndicator(); // バブルを消去

        if (response.ok) {
            addMessage(data.response, 'bot');
            statusBar.textContent = "いつでも話してね。";
        } else {
            addMessage("ごめんなさい、ちょっと考えがまとまらなくて。もう一度話してくれる？", "bot");
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage("接続がうまくいかないみたい。先生に直接会いに来てくれるかな？", "bot");
        console.error(error);
    } finally {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// 初期状態
userInput.disabled = false;
sendBtn.disabled = false;
