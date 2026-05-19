import re

app_path = 'c:/Users/User/database-teamproject/frontend/app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update sellProduct parameters
content = content.replace("const condition = document.getElementById('sell-condition').value.trim();", 
                          "const productName = document.getElementById('sell-name').value.trim();\n    const description = document.getElementById('sell-desc').value.trim();")
content = content.replace("Condition: condition,", "ProductName: productName,\n                Description: description,")
content = content.replace("document.getElementById('sell-condition').value = '';",
                          "document.getElementById('sell-name').value = '';\n            document.getElementById('sell-desc').value = '';")
content = content.replace("if(!price || !condition) return alert('請填寫完整資訊！');",
                          "if(!price || !productName) return alert('請填寫完整資訊！');")

# 2. Update searchProducts card rendering
content = content.replace('<span class="badge" style="background: rgba(244, 114, 182, 0.1); color: var(--primary); padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; margin-bottom: 10px; display: inline-block;">${p.Condition}</span>',
                          '<span class="badge" style="background: rgba(244, 114, 182, 0.1); color: var(--primary); padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; margin-bottom: 10px; display: inline-block;">${p.ProductName}</span>')
content = content.replace("onclick=\"openProductModal(${p.ProductID}, ${p.Price}, '${p.Condition}',",
                          "onclick=\"openProductModal(${p.ProductID}, ${p.Price}, '${p.ProductName}', '${p.Description || ''}',")

# 3. Update openProductModal definition and logic
modal_func_old = """function openProductModal(id, price, condition, method, sellerId, imageUrl, groupName, memberName) {
    document.getElementById('detail-title').innerText = `${groupName} - ${memberName} (周邊 #${id})`;
    document.getElementById('detail-price').innerText = `NT$ ${price}`;
    document.getElementById('detail-condition').innerText = condition;"""
modal_func_new = """function openProductModal(id, price, productName, description, method, sellerId, imageUrl, groupName, memberName) {
    document.getElementById('detail-title').innerText = `${groupName} - ${memberName} (周邊 #${id})`;
    document.getElementById('detail-price').innerText = `NT$ ${price}`;
    document.getElementById('detail-name').innerText = productName;
    document.getElementById('detail-desc').innerText = description || '無詳細描述';"""

content = content.replace(modal_func_old, modal_func_new)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.js successfully")
