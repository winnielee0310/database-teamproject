const API_BASE = 'http://127.0.0.1:8001';
let currentSelectedProductId = null;

// 初始化載入
document.addEventListener('DOMContentLoaded', () => {
    loadUserReputation(1); // 假設目前登入的買家/賣家是 User 1
    searchProducts(); // 預設搜尋
});

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
    const memberId = document.getElementById('member-select').value;
    const grid = document.getElementById('product-grid');
    const countSpan = document.getElementById('result-count');
    
    grid.innerHTML = '<p style="text-align:center; color:#94a3b8; grid-column: 1/-1;">搜尋中...</p>';
    
    try {
        const res = await fetch(`${API_BASE}/products/search?member_id=${memberId}`);
        const products = await res.json();
        
        countSpan.innerText = `(${products.length})`;
        grid.innerHTML = '';
        
        if (products.length === 0) {
            grid.innerHTML = '<p style="text-align:center; color:#94a3b8; grid-column: 1/-1;">目前沒有這位成員的可售商品喔！</p>';
            return;
        }

        products.forEach(p => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `
                <div class="tags">
                    <span class="tag condition">${p.Condition}</span>
                    <span class="tag method">${p.TradeMethod}</span>
                </div>
                <h3 style="margin-bottom: 10px;">精選周邊 #${p.ProductID}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">賣家 ID: ${p.SellerID}</p>
                <div class="price">NT$ ${p.Price}</div>
                <button class="btn-primary" style="width: 100%; padding: 10px;" onclick="openBuyModal(${p.ProductID}, ${p.Price})">
                    立即購買
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
                BuyerID: 2, // 假設買家是 User 2
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
