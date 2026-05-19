import re

file_path = 'c:/Users/User/database-teamproject/frontend/app.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace loadMessages and chat-send-btn
new_chat_logic = """// ===============================
// 對話系統邏輯 (Chat)
// ===============================
let currentChatProductId = null;
let currentChatSellerId = null;
let currentChatMessages = [];

function openChatModal(productId, sellerId) {
    currentChatProductId = productId;
    currentChatSellerId = sellerId;
    
    // 動態修改標題
    const titleEl = document.querySelector('#chat-modal h2');
    if (CURRENT_USER_ID === sellerId) {
        titleEl.innerHTML = '<i class="fa-regular fa-comments"></i> 回覆買家';
    } else {
        titleEl.innerHTML = '<i class="fa-regular fa-comments"></i> 聯絡賣家';
    }
    
    document.getElementById('chat-modal').classList.add('show');
    loadMessages();
}

async function loadMessages() {
    if(!currentChatProductId) return;
    const msgContainer = document.getElementById('chat-messages');
    try {
        const res = await fetch(`${API_BASE}/products/${currentChatProductId}/messages`);
        const msgs = await res.json();
        currentChatMessages = msgs;
        
        msgContainer.innerHTML = msgs.length ? msgs.map(m => `
            <div style="align-self: ${m.SenderID === CURRENT_USER_ID ? 'flex-end' : 'flex-start'}; background: ${m.SenderID === CURRENT_USER_ID ? 'var(--primary)' : 'rgba(255,255,255,0.8)'}; color: ${m.SenderID === CURRENT_USER_ID ? 'white' : 'var(--text)'}; padding: 10px 15px; border-radius: 12px; max-width: 80%; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <p style="font-size: 0.75rem; margin-bottom: 5px; opacity: 0.8; font-weight: bold;">
                    ${m.SenderID === currentChatSellerId ? '賣家' : '買家'} (User ${m.SenderID})
                </p>
                <p style="word-break: break-all;">${m.Content}</p>
            </div>
        `).join('') : '<p style="text-align: center; color: var(--text-muted); margin-top: 50px;">還沒有留言，來打個招呼吧！</p>';
        msgContainer.scrollTop = msgContainer.scrollHeight;
    } catch(err) { console.error('Failed to load messages', err); }
}

document.getElementById('chat-send-btn').addEventListener('click', async () => {
    const input = document.getElementById('chat-input');
    const content = input.value.trim();
    if(!content || !currentChatProductId) return;
    
    const senderId = CURRENT_USER_ID;
    let receiverId = currentChatSellerId; 

    if (senderId === currentChatSellerId) {
        const lastBuyerMsg = currentChatMessages.slice().reverse().find(m => m.SenderID !== currentChatSellerId);
        if (lastBuyerMsg) {
            receiverId = lastBuyerMsg.SenderID;
        } else {
            alert('目前沒有買家詢問，無法回覆喔！');
            return;
        }
    }

    try {
        const res = await fetch(`${API_BASE}/messages/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ProductID: currentChatProductId,
                SenderID: senderId,
                ReceiverID: receiverId,
                Content: content
            })
        });
        if(res.ok) {
            input.value = '';
            loadMessages();
        }
    } catch(err) { console.error('Send message failed', err); }
});"""

content = re.sub(r'// ===============================\n// 對話系統邏輯 \(Chat\)\n// ===============================.*', new_chat_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Chat logic updated successfully")
