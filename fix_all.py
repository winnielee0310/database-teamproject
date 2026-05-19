import re

# 1. Fix main.py (bought_orders)
main_path = 'c:/Users/User/database-teamproject/backend/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('"ProductCondition": p.Condition,', '"ProductName": p.ProductName,\n            "Description": p.Description,')
with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Fix schemas.py (ProductResponse)
schemas_path = 'c:/Users/User/database-teamproject/backend/schemas.py'
with open(schemas_path, 'r', encoding='utf-8') as f:
    content = f.read()

schemas_fix = """class ProductResponse(BaseModel):
    ProductID: int
    SellerID: int
    Price: float
    ProductName: str
    Description: Optional[str] = None
    TradeMethod: str
    Status: str
    ImageUrl: Optional[str] = None
    MemberNames: Optional[List[str]] = []
    GroupNames: Optional[List[str]] = []
    class Config:"""

content = re.sub(r'class ProductResponse\(BaseModel\):\n.*?class Config:', schemas_fix, content, flags=re.DOTALL)
with open(schemas_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Fix app.js (searchProducts)
app_path = 'c:/Users/User/database-teamproject/frontend/app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the whole products.forEach loop
search_replace = """        products.forEach(p => {
            const card = document.createElement('div');
            card.className = 'product-card';
            
            const imgHTML = p.ImageUrl 
                ? `<div style="width:100%; height:200px; border-radius:8px; overflow:hidden; margin-bottom:15px;"><img src="${p.ImageUrl}" style="width:100%; height:100%; object-fit:cover;"></div>`
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
                <button class="btn-primary" style="width: 100%; padding: 10px; margin-bottom: 8px;" onclick="openProductModal(${p.ProductID}, ${p.Price}, '${p.ProductName}', '${p.Description || ''}', '${p.TradeMethod}', ${p.SellerID}, '${p.ImageUrl || ''}', '${groupsText}', '${membersText}')">
                    查看詳細與賣家資訊
                </button>
                <button class="btn-primary" style="width: 100%; padding: 10px; background: transparent; border: 1px solid var(--secondary); color: var(--secondary);" onclick="openBuyModal(${p.ProductID}, ${p.Price})">
                    直接購買
                </button>
            `;
            grid.appendChild(card);
        });"""

content = re.sub(r'        products\.forEach\(p => \{.*?grid\.appendChild\(card\);\n        \}\);', search_replace, content, flags=re.DOTALL)
with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed main.py, schemas.py, and app.js")
