import re

# 1. Update schemas.py
schemas_path = 'c:/Users/User/database-teamproject/backend/schemas.py'
with open(schemas_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "MemberNames:" not in content:
    content = content.replace(
        "ImageUrl: Optional[str] = None\n    class Config:",
        "ImageUrl: Optional[str] = None\n    MemberNames: Optional[List[str]] = []\n    GroupNames: Optional[List[str]] = []\n    class Config:"
    )
    with open(schemas_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Update main.py
main_path = 'c:/Users/User/database-teamproject/backend/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

search_logic = """    products = query.filter(models.Product.Status == "Available").all()
    res = []
    for p in products:
        m_names = [m.MemberName for m in p.members]
        g_names = list(set([m.group.GroupName for m in p.members if m.group]))
        res.append({
            "ProductID": p.ProductID,
            "SellerID": p.SellerID,
            "Price": p.Price,
            "Condition": p.Condition,
            "TradeMethod": p.TradeMethod,
            "Status": p.Status,
            "ImageUrl": p.ImageUrl,
            "MemberNames": m_names,
            "GroupNames": g_names
        })
    return res"""

content = re.sub(r'    return query\.filter\(models\.Product\.Status == "Available"\)\.all\(\)', search_logic, content)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Update app.js
app_path = 'c:/Users/User/database-teamproject/frontend/app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

app_search_replace = """        grid.innerHTML = products.map(p => {
            const groupsText = (p.GroupNames && p.GroupNames.length > 0) ? p.GroupNames.join(', ') : '群星周邊';
            const membersText = (p.MemberNames && p.MemberNames.length > 0) ? p.MemberNames.join(', ') : '成員不詳';
            return `
            <div class="product-card" style="background: var(--card-bg); border-radius: 12px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: left;">
                ${p.ImageUrl 
                    ? `<div style="width:100%; height:200px; border-radius:8px; overflow:hidden; margin-bottom:15px;"><img src="${p.ImageUrl}" style="width:100%; height:100%; object-fit:cover;"></div>`
                    : `<div style="width:100%; height:200px; border-radius:8px; background:rgba(255,255,255,0.5); display:flex; align-items:center; justify-content:center; color:var(--text-muted); font-size:3rem; margin-bottom:15px;"><i class="fa-regular fa-image"></i></div>`
                }
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="badge" style="background: var(--bg); color: var(--text-muted); padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; margin-bottom: 10px; display: inline-block;">${p.TradeMethod}</span>
                    <span class="badge" style="background: rgba(244, 114, 182, 0.1); color: var(--primary); padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; margin-bottom: 10px; display: inline-block;">${p.Condition}</span>
                </div>
                <h3 style="margin-bottom: 5px;">${groupsText} - ${membersText}</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 10px;">精選周邊 #${p.ProductID}</p>
                <p style="font-size: 1.2rem; font-weight: 800; color: var(--primary); margin-bottom: 15px;">NT$ ${p.Price}</p>
                <button class="btn-primary" style="width: 100%; padding: 10px; margin-bottom: 8px;" onclick="openProductModal(${p.ProductID}, ${p.Price}, '${p.Condition}', '${p.TradeMethod}', ${p.SellerID}, '${p.ImageUrl || ''}', '${groupsText}', '${membersText}')">
                    查看詳情
                </button>
            </div>
            `;
        }).join('');"""

content = re.sub(r'        grid\.innerHTML = products\.map\(p => \{\n.*?return `.*?`;\n        \}\)\.join\(\'\'\);', app_search_replace, content, flags=re.DOTALL)

modal_func_replace = """function openProductModal(id, price, condition, method, sellerId, imageUrl, groupName, memberName) {
    document.getElementById('detail-title').innerText = `${groupName} - ${memberName} (周邊 #${id})`;"""
content = re.sub(r"function openProductModal\(id, price, condition, method, sellerId, imageUrl\) \{\n    document\.getElementById\('detail-title'\)\.innerText = `精選周邊 #\$\{id\}`;", modal_func_replace, content)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated card logic successfully")
