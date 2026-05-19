import re

file_path = 'c:/Users/User/database-teamproject/frontend/app.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded 1s and 2s
content = content.replace("loadUserReputation(1); // 假設目前登入的買家/賣家是 User 1", "CURRENT_USER_ID = 1;\n    loadUserReputation(CURRENT_USER_ID);")
content = content.replace("const res = await fetch(`${API_BASE}/users/1`);", "const res = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}`);")
content = content.replace("UserID: 1,", "UserID: CURRENT_USER_ID,")
content = content.replace("fetch(`${API_BASE}/users/1/wishlists`)", "fetch(`${API_BASE}/users/${CURRENT_USER_ID}/wishlists`)")
content = content.replace("fetch(`${API_BASE}/users/2/orders`);", "fetch(`${API_BASE}/users/${CURRENT_USER_ID}/orders`);")
content = content.replace("BuyerID: 2,", "BuyerID: CURRENT_USER_ID,")
content = content.replace("loadUserReputation(1); // 重新載入信譽", "loadUserReputation(CURRENT_USER_ID); // 重新載入信譽")
content = content.replace("SellerID: 1,", "SellerID: CURRENT_USER_ID,")
content = content.replace("const senderId = 2;", "const senderId = CURRENT_USER_ID;")

# Add switchUser function at the top
switch_code = """let CURRENT_USER_ID = 1;

function switchUser() {
    CURRENT_USER_ID = parseInt(document.getElementById('user-selector').value);
    loadUserReputation(CURRENT_USER_ID);
    if(document.getElementById('tab-profile').style.display === 'block') loadProfile();
    if(document.getElementById('tab-orders').style.display === 'block') loadOrders();
    if(document.getElementById('tab-wishlist').style.display === 'block') loadWishlists();
}
"""
content = content.replace("const API_BASE = 'http://127.0.0.1:8000';", f"const API_BASE = 'http://127.0.0.1:8000';\n{switch_code}")

# Improve loadProfile to include bought and sold
profile_replacement = """        const res = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}`); // 假設登入的是 User 1
        const user = await res.json();
        
        const soldRes = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/sold_products`);
        const soldProducts = await soldRes.json();
        
        const boughtRes = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/bought_orders`);
        const boughtOrders = await boughtRes.json();
        
        let soldHTML = soldProducts.map(p => `<li>精選周邊 #${p.ProductID} (NT$ ${p.Price}) - 狀態: ${p.Status}</li>`).join('');
        let boughtHTML = boughtOrders.map(o => `<li>訂單 #${o.OrderID} (商品 #${o.ProductID}, NT$ ${o.OrderPrice}) - 狀態: ${o.Status}</li>`).join('');
        
        document.getElementById('profile-container').innerHTML = `
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-id-card"></i> 使用者 ID：</strong> ${user.UserID}</p>
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-at"></i> 帳號名稱：</strong> ${user.Account}</p>
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-envelope"></i> 電子信箱：</strong> ${user.Email}</p>
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-star"></i> 賣家信譽：</strong> ⭐ ${user.SellerReputation}</p>
            <p style="margin-bottom:10px;"><strong><i class="fa-solid fa-star-half-stroke"></i> 買家信譽：</strong> ⭐ ${user.BuyerReputation}</p>
            <hr style="margin: 20px 0; border: 0; border-top: 1px solid var(--border);">
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

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("app.js updated successfully")
