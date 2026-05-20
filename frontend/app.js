const API_BASE = "http://127.0.0.1:8001";
let CURRENT_USER_ID = 1;

function switchUser() {
    CURRENT_USER_ID = parseInt(document.getElementById('user-selector').value);
    loadUserReputation(CURRENT_USER_ID);
    if (document.getElementById('tab-profile').style.display === 'block') loadProfile();
    if (document.getElementById('tab-orders').style.display === 'block') loadOrders();
    if (document.getElementById('tab-wishlist').style.display === 'block') loadWishlists();
}

let currentSelectedProductId = null;

// 初始化載入
document.addEventListener('DOMContentLoaded', () => {
    CURRENT_USER_ID = 1;
    loadUserReputation(CURRENT_USER_ID);
    loadPopularMembers();
    searchProducts(); // 預設搜尋
});

let memberMap = {}; // { id: name }
let groupMap = {}; // { id: name }

async function loadPopularMembers() {
    try {
        const resMem = await fetch(`${API_BASE}/members/`);
        const members = await resMem.json();
        const datalistMem = members.map(m => {
            memberMap[m.MemberID] = m.MemberName;
            return `<option value="${m.MemberName}">`;
        }).join('');

        if (!document.getElementById('popular-members')) {
            const datalist = document.createElement('datalist');
            datalist.id = 'popular-members';
            document.body.appendChild(datalist);
        }
        document.getElementById('popular-members').innerHTML = datalistMem;

        const resGroup = await fetch(`${API_BASE}/groups/`);
        const groups = await resGroup.json();
        const datalistGroup = groups.map(g => {
            groupMap[g.GroupID] = g.GroupName;
            return `<option value="${g.GroupName}">`;
        }).join('');

        if (!document.getElementById('popular-groups')) {
            const datalist = document.createElement('datalist');
            datalist.id = 'popular-groups';
            document.body.appendChild(datalist);
        }
        document.getElementById('popular-groups').innerHTML = datalistGroup;
    } catch (err) { console.error('Failed to load popular members', err); }
}

// 讀取賣家信譽 (展示聚合查詢功能)
async function loadUserReputation(userId) {
    try {
        const res = await fetch(`${API_BASE}/users/${userId}/reputation`);
        const data = await res.json();
        const badge = document.getElementById('reputation-badge');
        badge.innerHTML = `<i class="fa-solid fa-star"></i> 信譽 ${data.Total_Reputation || '5.0'} / 5.0`;
    } catch (err) {
        console.error('Failed to load reputation', err);
    }
}

// 搜尋按鈕綁定
document.getElementById('search-btn').addEventListener('click', searchProducts);

// 搜尋商品 (展示 JOIN 多成員查詢功能)
async function searchProducts() {
    const searchInput = document.getElementById('member-search-input');
    const groupInput = document.getElementById('group-search-input');
    const memberName = searchInput ? searchInput.value.trim() : '';
    const groupName = groupInput ? groupInput.value.trim() : '';
    const grid = document.getElementById('product-grid');
    const countSpan = document.getElementById('result-count');

    grid.innerHTML = '<p style="text-align:center; color:#94a3b8; grid-column: 1/-1;">搜尋中...</p>';

    try {
        let url = `${API_BASE}/products/search?`;
        if (memberName) url += `member_name=${encodeURIComponent(memberName)}&`;
        if (groupName) url += `group_name=${encodeURIComponent(groupName)}`;

        const res = await fetch(url);
        const products = await res.json();
        currentSearchProducts = products;

        countSpan.innerText = `(${products.length})`;
        grid.innerHTML = '';

        if (products.length === 0) {
            grid.innerHTML = '<p style="text-align:center; color:#94a3b8; grid-column: 1/-1;">目前沒有這位成員的可售商品喔！</p>';
            return;
        }

        products.forEach(p => {
            const card = document.createElement('div');
            card.className = 'product-card';

            const imgUrl = p.ImageUrl ? (p.ImageUrl.startsWith('http') ? p.ImageUrl : `${API_BASE}/uploads/${p.ImageUrl.split('/').pop()}`) : null;
            const imgHTML = imgUrl
                ? `<div style="width:100%; height:200px; border-radius:8px; overflow:hidden; margin-bottom:15px;"><img src="${imgUrl}" style="width:100%; height:100%; object-fit:cover;"></div>`
                : `<div style="width:100%; height:200px; border-radius:8px; background:rgba(255,255,255,0.5); display:flex; align-items:center; justify-content:center; color:var(--text-muted); font-size:3rem; margin-bottom:15px;"><i class="fa-regular fa-image"></i></div>`;

            const groupsText = (p.GroupNames && p.GroupNames.length > 0) ? p.GroupNames.join(', ') : '群星周邊';
            const membersText = (p.MemberNames && p.MemberNames.length > 0) ? p.MemberNames.join(', ') : '成員不詳';

            card.innerHTML = `
                ${imgHTML}
                <div class="tags">
                    <span class="tag condition">${p.ProductName}</span>
                    <span class="tag method">${p.TradeMethod}</span>
                </div>
                <h3 style="margin-bottom: 5px;">${groupsText} - ${membersText}</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 10px;">精選周邊 #${p.ProductID}</p>
                <p style="color: #94a3b8; font-size: 0.9rem;">賣家 ID: ${p.SellerID}</p>
                <div class="price">NT$ ${p.Price}</div>
                <button class="btn-primary" style="width: 100%; padding: 10px; margin-bottom: 8px;" onclick="openProductModal(${p.ProductID})">
                    查看詳細與賣家資訊
                </button>
                <button class="btn-primary" style="width: 100%; padding: 10px; background: transparent; border: 1px solid var(--secondary); color: var(--secondary);" onclick="openBuyModal(${p.ProductID}, ${p.Price})">
                    直接購買
                </button>
            `;
            grid.appendChild(card);
        });
    } catch (err) {
        console.error(err);
        grid.innerHTML = '<p style="color: #ec4899; text-align:center; grid-column: 1/-1;">伺服器連線失敗，請確認後端已啟動。</p>';
    }
}

// 彈窗處理
const modal = document.getElementById('buy-modal');
const closeBtn = document.querySelector('.close-btn');

function openBuyModal(productId, price) {
    currentSelectedProductId = productId;
    document.getElementById('modal-price').innerText = `NT$ ${price}`;
    modal.classList.add('show');
}

closeBtn.onclick = () => modal.classList.remove('show');
window.onclick = (e) => {
    if (e.target === modal) modal.classList.remove('show');
}

// 確認結帳 (展示悲觀鎖機制)
document.getElementById('confirm-buy-btn').addEventListener('click', async () => {
    if (!currentSelectedProductId) return;

    const btn = document.getElementById('confirm-buy-btn');
    btn.innerText = '處理中...';
    btn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/orders/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                BuyerID: CURRENT_USER_ID, // 假設買家是 User 2
                ProductID: currentSelectedProductId
            })
        });

        if (res.ok) {
            alert('🎉 購買成功！訂單已成立！');
            modal.classList.remove('show');
            searchProducts(); // 重新整理商品列表
        } else {
            const errorData = await res.json();
            alert(`❌ 購買失敗: ${errorData.detail}`);
        }
    } catch (err) {
        alert('發生錯誤，請稍後再試！');
    } finally {
        btn.innerText = '確認結帳 (防超賣保護中)';
        btn.disabled = false;
    }
});

// ===============================
// 新增分頁切換與其他功能邏輯
// ===============================

// 分頁切換邏輯
function switchTab(event, tabId) {
    if (event) event.preventDefault();
    document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
    document.getElementById(`tab-${tabId}`).style.display = 'block';

    if (event) {
        document.querySelectorAll('nav a').forEach(el => el.classList.remove('active'));
        event.currentTarget.classList.add('active');
    }

    if (tabId === 'wishlist') loadWishlists();
    if (tabId === 'orders') loadOrders();
    if (tabId === 'profile') loadProfile();
}

// 個人資訊載入
async function loadProfile() {
    try {
        const res = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}`); // 假設登入的是 User 1
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
        `;
    } catch (err) { console.error('Failed to load profile', err); }
}

let currentSearchProducts = [];

function openProductModal(id) {
    const p = currentSearchProducts.find(prod => prod.ProductID === id);
    if (!p) return;

    const groupsText = (p.GroupNames && p.GroupNames.length > 0) ? p.GroupNames.join(', ') : '群星周邊';
    const membersText = (p.MemberNames && p.MemberNames.length > 0) ? p.MemberNames.join(', ') : '成員不詳';

    document.getElementById('detail-title').innerText = `${groupsText} - ${membersText} (周邊 #${id})`;
    document.getElementById('detail-price').innerText = `NT$ ${p.Price}`;
    document.getElementById('detail-name').innerText = p.ProductName;
    document.getElementById('detail-desc').innerText = p.Description || '無詳細描述';
    document.getElementById('detail-method').innerText = p.TradeMethod;
    document.getElementById('detail-seller-id').innerText = p.SellerID;
    document.getElementById('detail-seller-rep').innerText = '載入中...';

    const imgEl = document.getElementById('detail-image');
    const iconEl = document.getElementById('detail-image-icon');

    if (p.ImageUrl) {
        imgEl.src = p.ImageUrl.startsWith('http') ? p.ImageUrl : `${API_BASE}/uploads/${p.ImageUrl.split('/').pop()}`;
        imgEl.style.display = 'block';
        iconEl.style.display = 'none';
    } else {
        imgEl.style.display = 'none';
        iconEl.style.display = 'block';
    }

    currentSelectedProductId = id;

    document.getElementById('detail-buy-btn').onclick = () => {
        document.getElementById('product-modal').classList.remove('show');
        openBuyModal(id, p.Price);
    };

    document.getElementById('detail-chat-btn').onclick = () => {
        document.getElementById('product-modal').classList.remove('show');
        openChatModal(id, p.SellerID);
    };

    document.getElementById('product-modal').classList.add('show');

    fetch(`${API_BASE}/users/${p.SellerID}/reputation`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('detail-seller-rep').innerText = `⭐ ${data.Total_Reputation} / 5.0\n(包裝: ${data.Average_Packing}, 錄影: ${data.Average_Video}, 速度: ${data.Average_Speed})`;
        })
        .catch(err => document.getElementById('detail-seller-rep').innerText = '無法載入');
}

// 願望清單
async function addWishlist() {
    const memberName = document.getElementById('wish-member-input').value.trim();
    const groupName = document.getElementById('wish-group-input').value.trim();
    const price = document.getElementById('wish-price').value;
    if (!price || !memberName) return alert('請輸入成員名稱與最高預算！');

    try {
        const res = await fetch(`${API_BASE}/wishlists/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                UserID: CURRENT_USER_ID,
                MaxPrice: parseFloat(price),
                CustomGroupName: groupName || "Unknown Group",
                CustomMemberName: memberName
            })
        });
        if (res.ok) {
            alert('願望新增成功！如果有賣家上架，系統會自動比對喔！');
            document.getElementById('wish-price').value = '';
            loadWishlists();
        } else {
            alert('新增失敗');
        }
    } catch (err) { alert('伺服器連線錯誤'); }
}

async function loadWishlists() {
    try {
        const res = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/wishlists`);
        const data = await res.json();
        const grid = document.getElementById('wishlist-grid');
        grid.innerHTML = data.length ? data.map(w => `
            <div class="product-card">
                <div class="tags"><span class="tag method">許願中</span></div>
                <h3>目標成員: ${memberMap[w.MemberID] || w.MemberID}</h3>
                <div class="price">預算: NT$ ${w.MaxPrice}</div>
            </div>
        `).join('') : '<p style="color: var(--text-muted);">目前沒有願望清單</p>';
    } catch (err) { console.error(err); }
}

// 我的訂單
async function loadOrders() {
    try {
        const res = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/orders`); // 模擬買家 2 登入
        const data = await res.json();
        const grid = document.getElementById('orders-grid');
        grid.innerHTML = data.length ? data.map(o => `
            <div class="product-card">
                <div class="tags"><span class="tag condition">${o.Status}</span></div>
                <h3>訂單 #${o.OrderID}</h3>
                <p style="color: var(--text-muted); margin-bottom: 10px;">購買商品 ID: ${o.ProductID}</p>
                <div class="price">結帳金額: NT$ ${o.OrderPrice}</div>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 15px;">訂單成立時間: ${new Date(o.OrderDate).toLocaleString()}</p>
                ${o.Status === 'Completed' ? `<button onclick="openReviewModal(${o.OrderID})" class="btn-primary" style="width:100%; margin-top:15px; padding: 10px; font-size: 0.9rem;">給予賣家評價</button>` : ''}
            </div>
        `).join('') : '<p style="color: var(--text-muted);">目前沒有訂單紀錄</p>';
    } catch (err) { console.error(err); }
}

let currentReviewOrderId = null;

function openReviewModal(orderId) {
    currentReviewOrderId = orderId;
    document.getElementById('review-modal').classList.add('show');
}

async function submitReview() {
    if (!currentReviewOrderId) return;

    const packing = parseInt(document.getElementById('review-packing').value);
    const video = parseInt(document.getElementById('review-video').value);
    const speed = parseInt(document.getElementById('review-speed').value);
    const comment = document.getElementById('review-comment').value;

    try {
        const res = await fetch(`${API_BASE}/reviews/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                OrderID: currentReviewOrderId,
                PackingScore: packing,
                VideoScore: video,
                SpeedScore: speed,
                Comment: comment
            })
        });

        if (res.ok) {
            alert('評價送出成功！已動態更新賣家信譽！');
            document.getElementById('review-modal').classList.remove('show');
            loadUserReputation(CURRENT_USER_ID); // 重新載入信譽
        } else {
            const err = await res.json();
            alert(`評價失敗: ${err.detail || '您可能已經評價過這筆訂單'}`);
        }
    } catch (err) { alert('伺服器連線錯誤'); }
}

// 上架商品
async function sellProduct() {
    const groupName = document.getElementById('sell-group-name').value;
    const memberNamesStr = document.getElementById('sell-member-names').value;
    const price = document.getElementById('sell-price').value;
    const productName = document.getElementById('sell-name').value.trim();
    const description = document.getElementById('sell-desc').value.trim();
    const method = document.getElementById('sell-method').value;
    const imageInput = document.getElementById('sell-image');

    if (!price || !productName || !groupName || !memberNamesStr) return alert('請填寫完整商品資訊！');

    let imageUrl = null;
    if (imageInput.files.length > 0) {
        const formData = new FormData();
        formData.append("file", imageInput.files[0]);
        try {
            const uploadRes = await fetch(`${API_BASE}/upload-image/`, {
                method: 'POST',
                body: formData
            });
            if (uploadRes.ok) {
                const uploadData = await uploadRes.json();
                imageUrl = uploadData.ImageUrl;
            } else {
                alert("圖片上傳失敗，商品將不含圖片");
            }
        } catch (e) {
            console.error("圖片上傳發生錯誤", e);
        }
    }

    const memberNames = memberNamesStr.split(',').map(s => s.trim()).filter(s => s);

    try {
        const res = await fetch(`${API_BASE}/products/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                SellerID: CURRENT_USER_ID, // 模擬賣家 1 登入
                Price: parseFloat(price),
                ProductName: productName,
                Description: description,
                TradeMethod: method,
                MemberIDs: [],
                CustomGroupName: groupName,
                CustomMemberNames: memberNames,
                ImageUrl: imageUrl
            })
        });
        if (res.ok) {
            alert('🎉 商品上架成功！系統已開始為您進行自動撮合！');
            document.getElementById('sell-price').value = '';
            document.getElementById('sell-name').value = '';
            document.getElementById('sell-desc').value = '';
            document.getElementById('sell-group-name').value = '';
            document.getElementById('sell-member-names').value = '';
            if (imageInput) imageInput.value = '';
            // 自動跳轉回首頁看結果
            document.querySelector('nav a:nth-child(1)').click();
            searchProducts();
        } else {
            alert('上架失敗');
        }
    } catch (err) { alert('伺服器連線錯誤'); }
}

// ===============================
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
    if (!currentChatProductId) return;
    const msgContainer = document.getElementById('chat-messages');
    try {
        const res = await fetch(`${API_BASE}/products/${currentChatProductId}/messages`);
        const msgs = await res.json();
        currentChatMessages = msgs;

        msgContainer.innerHTML = msgs.length ? msgs.map(m => {
            let mediaHTML = '';
            if (m.MediaUrl) {
                const fullMediaUrl = m.MediaUrl.startsWith('http') ? m.MediaUrl : `${API_BASE}/uploads/${m.MediaUrl.split('/').pop()}`;
                if (m.MediaUrl.match(/\.(mp4|webm|ogg)$/i)) {
                    mediaHTML = `<video src="${fullMediaUrl}" controls style="max-width: 100%; border-radius: 8px; margin-top: 10px;"></video>`;
                } else {
                    mediaHTML = `<img src="${fullMediaUrl}" style="max-width: 100%; border-radius: 8px; margin-top: 10px;">`;
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
        }).join('') : '<p style="text-align: center; color: var(--text-muted); margin-top: 50px;">還沒有留言，來打個招呼吧！</p>';
        msgContainer.scrollTop = msgContainer.scrollHeight;
    } catch (err) { console.error('Failed to load messages', err); }
}

document.getElementById('chat-send-btn').addEventListener('click', async () => {
    const input = document.getElementById('chat-input');
    const fileInput = document.getElementById('chat-file-input');
    const content = input.value.trim();

    // 如果沒有文字 也沒有檔案 就不要送出
    if (!content && fileInput.files.length === 0) return;
    if (!currentChatProductId) return;

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
    if (fileInput.files.length > 0) {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        try {
            const uploadRes = await fetch(`${API_BASE}/upload-image/`, {
                method: 'POST',
                body: formData
            });
            if (uploadRes.ok) {
                const uploadData = await uploadRes.json();
                mediaUrl = uploadData.filename;
            }
        } catch (err) { console.error("Upload failed", err); }
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
        if (res.ok) {
            input.value = '';
            fileInput.value = ''; // 清除檔案
            loadMessages();
        }
    } catch (err) { console.error('Send message failed', err); }
});