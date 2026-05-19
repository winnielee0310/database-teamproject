import re

file_path = 'c:/Users/User/database-teamproject/frontend/app.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update loadProfile to include notifications
profile_replacement = """        const res = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}`); // 假設登入的是 User 1
        const user = await res.json();
        
        const soldRes = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/sold_products`);
        const soldProducts = await soldRes.json();
        
        const boughtRes = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/bought_orders`);
        const boughtOrders = await boughtRes.json();

        const notifRes = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/notifications`);
        const notifications = await notifRes.json();
        
        let soldHTML = soldProducts.map(p => `<li>精選周邊 #${p.ProductID} (NT$ ${p.Price}) - 狀態: ${p.Status}</li>`).join('');
        let boughtHTML = boughtOrders.map(o => `<li>訂單 #${o.OrderID} (商品 #${o.ProductID}, NT$ ${o.OrderPrice}) - 狀態: ${o.Status}</li>`).join('');
        let notifHTML = notifications.map(n => `<li style="margin-bottom:8px; border-bottom: 1px solid #eee; padding-bottom: 5px;"><strong>User ${n.SenderID}</strong> (商品 #${n.ProductID}): ${n.Content.substring(0, 30)}${n.MediaUrl ? ' [附帶多媒體檔案]' : ''}</li>`).join('');

        document.getElementById('profile-container').innerHTML = `
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-id-card"></i> 使用者 ID：</strong> ${user.UserID}</p>
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-at"></i> 帳號名稱：</strong> ${user.Account}</p>
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-envelope"></i> 電子信箱：</strong> ${user.Email}</p>
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-star"></i> 賣家信譽：</strong> ⭐ ${user.SellerReputation}</p>
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-star-half-stroke"></i> 買家信譽：</strong> ⭐ ${user.BuyerReputation}</p>
            <hr style="margin: 20px 0; border: 0; border-top: 1px solid var(--border);">
            
            <h3 style="margin-bottom: 10px; color: #f59e0b;"><i class="fa-solid fa-bell"></i> 最新對話通知</h3>
            <ul style="padding-left: 20px; margin-bottom: 20px; color: var(--text); line-height: 1.5; list-style-type: disc;">
                ${notifHTML || '<li>目前沒有任何新通知</li>'}
            </ul>

            <h3 style="margin-bottom: 10px; color: var(--primary);"><i class="fa-solid fa-box-open"></i> 賣出商品紀錄</h3>
            <ul style="padding-left: 20px; margin-bottom: 20px; color: var(--text-muted); line-height: 1.8;">
                ${soldHTML || '<li>目前沒有賣出紀錄</li>'}
            </ul>
            <h3 style="margin-bottom: 10px; color: var(--secondary);"><i class="fa-solid fa-bag-shopping"></i> 買入商品紀錄</h3>
            <ul style="padding-left: 20px; color: var(--text-muted); line-height: 1.8;">
                ${boughtHTML || '<li>目前沒有買入紀錄</li>'}
            </ul>
        `;"""
content = re.sub(r'const res = await fetch\(`\$\{API_BASE\}/users/\$\{CURRENT_USER_ID\}`\);.*?`;', profile_replacement, content, flags=re.DOTALL)

# 2. Update loadMessages to render media
load_messages_replacement = """        msgContainer.innerHTML = msgs.length ? msgs.map(m => {
            let mediaHTML = '';
            if(m.MediaUrl) {
                if(m.MediaUrl.match(/\\.(mp4|webm|ogg)$/i)) {
                    mediaHTML = `<video src="${m.MediaUrl}" controls style="max-width: 100%; border-radius: 8px; margin-top: 10px;"></video>`;
                } else {
                    mediaHTML = `<img src="${m.MediaUrl}" style="max-width: 100%; border-radius: 8px; margin-top: 10px;">`;
                }
            }
            return `
            <div style="align-self: ${m.SenderID === CURRENT_USER_ID ? 'flex-end' : 'flex-start'}; background: ${m.SenderID === CURRENT_USER_ID ? 'var(--primary)' : 'rgba(255,255,255,0.8)'}; color: ${m.SenderID === CURRENT_USER_ID ? 'white' : 'var(--text)'}; padding: 10px 15px; border-radius: 12px; max-width: 80%; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <p style="font-size: 0.75rem; margin-bottom: 5px; opacity: 0.8; font-weight: bold;">
                    ${m.SenderID === currentChatSellerId ? '賣家' : '買家'} (User ${m.SenderID})
                </p>
                <p style="word-break: break-all;">${m.Content}</p>
                ${mediaHTML}
            </div>
            `;
        }).join('') : '<p style="text-align: center; color: var(--text-muted); margin-top: 50px;">還沒有留言，來打個招呼吧！</p>';"""
content = re.sub(r'msgContainer\.innerHTML = msgs\.length \? msgs\.map\(m => `.*?`\)\.join\(\'\'\) : \'<p style="text-align: center; color: var\(--text-muted\); margin-top: 50px;">還沒有留言，來打個招呼吧！</p>\';', load_messages_replacement, content, flags=re.DOTALL)

# 3. Update chat-send-btn logic to upload file
chat_send_replacement = """document.getElementById('chat-send-btn').addEventListener('click', async () => {
    const input = document.getElementById('chat-input');
    const fileInput = document.getElementById('chat-file-input');
    const content = input.value.trim();
    
    // 如果沒有文字 也沒有檔案 就不要送出
    if(!content && fileInput.files.length === 0) return;
    if(!currentChatProductId) return;
    
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

    // 處理檔案上傳
    let mediaUrl = null;
    if(fileInput.files.length > 0) {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        try {
            const uploadRes = await fetch(`${API_BASE}/upload-image/`, {
                method: 'POST',
                body: formData
            });
            if(uploadRes.ok) {
                const uploadData = await uploadRes.json();
                mediaUrl = uploadData.filename;
            }
        } catch(err) { console.error("Upload failed", err); }
    }

    try {
        const res = await fetch(`${API_BASE}/messages/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ProductID: currentChatProductId,
                SenderID: senderId,
                ReceiverID: receiverId,
                Content: content || '(傳送了多媒體檔案)',
                MediaUrl: mediaUrl
            })
        });
        if(res.ok) {
            input.value = '';
            fileInput.value = ''; // 清除檔案
            loadMessages();
        }
    } catch(err) { console.error('Send message failed', err); }
});"""
content = re.sub(r"document\.getElementById\('chat-send-btn'\)\.addEventListener\('click', async \(\) => \{.*\}\);", chat_send_replacement, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("app.js media updated successfully")
