const API_BASE = "http://127.0.0.1:8000";

let CURRENT_USER_ID = 1;
let currentSelectedProductId = null;
let currentReviewOrderId = null;
let currentSearchProducts = [];
let currentChatId = null;
let unreadPollingInterval = null;
let chatPollingInterval = null;
let memberMap = {};
let groupMap = {};
let currentLanguage = localStorage.getItem("uiLanguage") || "en";

const TRANSLATIONS = {
    en: {
        "login.title": "Login",
        "login.email": "Email",
        "login.password": "Password",
        "login.submit": "Login",
        "login.noAccount": "No account?",
        "login.registerLink": "Register",
        "login.demo": "Demo: winnie@example.com / hashed_pw_1",
        "register.title": "Register",
        "register.username": "Username",
        "register.confirmPassword": "Confirm password",
        "register.submit": "Register",
        "register.already": "Already registered?",
        "register.backLogin": "Back to login",
        "nav.home": "Home",
        "nav.wishlist": "Wishlist",
        "nav.orders": "Orders",
        "nav.sell": "Sell",
        "nav.analytics": "Analytics",
        "nav.messages": "Messages",
        "nav.profile": "Profile",
        "nav.logout": "Logout",
        "home.titlePrefix": "Find your",
        "home.titleAccent": "idol goods",
        "home.subtitle": "Search by group or member, then buy, chat, and review in one place.",
        "home.search": "Search",
        "home.results": "Results",
        "common.groupName": "Group name",
        "common.memberName": "Member name",
        "common.add": "Add",
        "common.group": "Group",
        "common.members": "Members",
        "common.loading": "Loading...",
        "common.confirm": "Confirm",
        "common.chat": "Chat",
        "common.buy": "Buy",
        "wishlist.title": "Wishlist",
        "wishlist.subtitle": "Add a member and budget so sellers can see what buyers want.",
        "wishlist.maxPrice": "Max price",
        "wishlist.myWishlist": "My Wishlist",
        "orders.title": "Orders",
        "sell.title": "Sell an item",
        "sell.subtitle": "List an item with member tags so buyers can find it quickly.",
        "sell.groupExample": "Example: NewJeans",
        "sell.membersExample": "Example: Minji, Hanni",
        "sell.productName": "Product name",
        "sell.price": "Price",
        "sell.description": "Description",
        "sell.image": "Image",
        "sell.publish": "Publish",
        "analytics.title": "Database Insights",
        "analytics.marketTag": "GROUP BY / AVG",
        "analytics.marketTitle": "Market historical average",
        "analytics.demandTag": "Wishlist matching",
        "analytics.demandTitle": "Member demand heat",
        "analytics.reputationTag": "Review aggregation",
        "analytics.reputationTitle": "Seller reputation ranking",
        "messages.title": "Messages",
        "messages.input": "Type a message...",
        "profile.title": "Profile",
        "buy.title": "Confirm purchase",
        "buy.questionPrefix": "Buy this item for",
        "review.title": "Review seller",
        "review.packing": "Packing score (1-5)",
        "review.video": "Video proof score (1-5)",
        "review.speed": "Speed score (1-5)",
        "review.comment": "Comment",
        "review.submit": "Submit review",
        "detail.title": "Product details",
        "detail.name": "Name:",
        "detail.description": "Description:",
        "detail.condition": "Condition:",
        "detail.trade": "Trade:",
        "detail.seller": "Seller",
        "detail.sellerId": "Seller ID:",
        "detail.reputation": "Reputation:",
        "value.New": "New",
        "value.Like New": "Like New",
        "value.Used - Good": "Used - Good",
        "value.Used - Fair": "Used - Fair",
        "value.Meetup": "Meetup",
        "value.Shipping": "Shipping",
        "value.Mailing": "Mailing",
    },
    zh: {
        "login.title": "登入",
        "login.email": "電子郵件",
        "login.password": "密碼",
        "login.submit": "登入",
        "login.noAccount": "還沒有帳號？",
        "login.registerLink": "註冊",
        "login.demo": "測試帳號：winnie@example.com / hashed_pw_1",
        "register.title": "註冊",
        "register.username": "使用者名稱",
        "register.confirmPassword": "確認密碼",
        "register.submit": "註冊",
        "register.already": "已經有帳號？",
        "register.backLogin": "回到登入",
        "nav.home": "首頁",
        "nav.wishlist": "願望清單",
        "nav.orders": "訂單",
        "nav.sell": "上架",
        "nav.analytics": "分析",
        "nav.messages": "訊息",
        "nav.profile": "個人資料",
        "nav.logout": "登出",
        "home.titlePrefix": "尋找你的",
        "home.titleAccent": "偶像周邊",
        "home.subtitle": "依團體或成員搜尋，並在同一個系統完成購買、聊天與評價。",
        "home.search": "搜尋",
        "home.results": "搜尋結果",
        "common.groupName": "團體名稱",
        "common.memberName": "成員名稱",
        "common.add": "新增",
        "common.group": "團體",
        "common.members": "成員",
        "common.loading": "載入中...",
        "common.confirm": "確認",
        "common.chat": "聊天",
        "common.buy": "購買",
        "wishlist.title": "願望清單",
        "wishlist.subtitle": "設定想找的成員與預算，讓系統自動比對符合條件的商品。",
        "wishlist.maxPrice": "最高價格",
        "wishlist.myWishlist": "我的願望清單",
        "orders.title": "訂單",
        "sell.title": "上架商品",
        "sell.subtitle": "用成員標籤上架商品，讓買家更快搜尋到。",
        "sell.groupExample": "例如：NewJeans",
        "sell.membersExample": "例如：Minji, Hanni",
        "sell.productName": "商品名稱",
        "sell.price": "價格",
        "sell.description": "商品描述",
        "sell.image": "圖片",
        "sell.publish": "發布",
        "analytics.title": "資料庫分析亮點",
        "analytics.marketTag": "GROUP BY / AVG",
        "analytics.marketTitle": "市場歷史均價",
        "analytics.demandTag": "Wishlist 撮合",
        "analytics.demandTitle": "成員需求熱度",
        "analytics.reputationTag": "評價聚合",
        "analytics.reputationTitle": "賣家信譽排行",
        "messages.title": "訊息",
        "messages.input": "輸入訊息...",
        "profile.title": "個人資料",
        "buy.title": "確認購買",
        "buy.questionPrefix": "是否購買此商品，價格為",
        "review.title": "評價賣家",
        "review.packing": "包裝分數（1-5）",
        "review.video": "對光/影片確認分數（1-5）",
        "review.speed": "出貨速度分數（1-5）",
        "review.comment": "評論",
        "review.submit": "送出評價",
        "detail.title": "商品詳情",
        "detail.name": "名稱：",
        "detail.description": "描述：",
        "detail.condition": "狀況：",
        "detail.trade": "交易方式：",
        "detail.seller": "賣家",
        "detail.sellerId": "賣家編號：",
        "detail.reputation": "信譽分數：",
        "value.New": "全新",
        "value.Like New": "近全新",
        "value.Used - Good": "二手良好",
        "value.Used - Fair": "二手普通",
        "value.Meetup": "面交",
        "value.Shipping": "宅配",
        "value.Mailing": "郵寄",
    },
};

function $(id) {
    return document.getElementById(id);
}

function translate(key) {
    return TRANSLATIONS[currentLanguage]?.[key] || TRANSLATIONS.en[key] || key;
}

function applyTranslations() {
    document.documentElement.lang = currentLanguage === "zh" ? "zh-Hant" : "en";
    document.querySelectorAll("[data-i18n]").forEach((element) => {
        element.textContent = translate(element.dataset.i18n);
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
        element.placeholder = translate(element.dataset.i18nPlaceholder);
    });

    const toggleLabel = $("language-toggle-label");
    if (toggleLabel) toggleLabel.innerText = currentLanguage === "en" ? "中文" : "EN";
}

function setupLanguageToggle() {
    const button = $("language-toggle");
    if (!button) return;
    button.addEventListener("click", () => {
        currentLanguage = currentLanguage === "en" ? "zh" : "en";
        localStorage.setItem("uiLanguage", currentLanguage);
        applyTranslations();
    });
    applyTranslations();
}

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }[char]));
}

async function readJson(response) {
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.detail || `Request failed: ${response.status}`);
    }
    return data;
}

function setError(id, message) {
    const box = $(id);
    box.innerText = message;
    box.style.display = message ? "block" : "none";
}

function showLoginPage() {
    $("login-box").style.display = "block";
    $("register-box").style.display = "none";
}

function showRegisterPage() {
    $("login-box").style.display = "none";
    $("register-box").style.display = "block";
}

function checkLoginStatus() {
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
    $("auth-container").style.display = isLoggedIn ? "none" : "flex";
    $("main-app").style.display = isLoggedIn ? "block" : "none";

    if (!isLoggedIn) {
        showLoginPage();
        return;
    }

    CURRENT_USER_ID = Number(localStorage.getItem("currentUserId")) || 1;
    const username = localStorage.getItem("currentUser") || "User";
    $("current-username-display").innerText = username;
    $("user-avatar").src = `https://ui-avatars.com/api/?name=${encodeURIComponent(username)}&background=f472b6&color=fff`;

    loadUserReputation(CURRENT_USER_ID);
    loadPopularMembers();
    searchProducts();
    startUnreadPolling();
}

function startUnreadPolling() {
    if (unreadPollingInterval) clearInterval(unreadPollingInterval);
    loadUserChats();
    unreadPollingInterval = setInterval(() => {
        if (localStorage.getItem("isLoggedIn") === "true") {
            loadUserChats();
        }
    }, 5000);
}

function stopUnreadPolling() {
    if (unreadPollingInterval) clearInterval(unreadPollingInterval);
    unreadPollingInterval = null;
    updateMessagesUnreadBadge(0);
}

async function handleLogin() {
    const email = $("login-email").value.trim();
    const password = $("login-password").value.trim();
    setError("login-error", "");

    if (!email || !password) {
        setError("login-error", "Please enter email and password.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });
        const data = await readJson(response);
        localStorage.setItem("isLoggedIn", "true");
        localStorage.setItem("currentUser", data.username);
        localStorage.setItem("currentUserId", data.id);
        $("login-email").value = "";
        $("login-password").value = "";
        checkLoginStatus();
    } catch (error) {
        setError("login-error", error.message);
    }
}

async function handleRegister() {
    const username = $("reg-username").value.trim();
    const email = $("reg-email").value.trim();
    const password = $("reg-password").value.trim();
    const confirmPassword = $("reg-password-confirm").value.trim();
    setError("register-error", "");

    if (!username || !email || !password || !confirmPassword) {
        setError("register-error", "Please fill in every field.");
        return;
    }
    if (!/^\S+@\S+\.\S+$/.test(email)) {
        setError("register-error", "Please enter a valid email.");
        return;
    }
    if (password !== confirmPassword) {
        setError("register-error", "Passwords do not match.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password }),
        });
        await readJson(response);
        alert("Registration complete. Please log in.");
        $("reg-username").value = "";
        $("reg-email").value = "";
        $("reg-password").value = "";
        $("reg-password-confirm").value = "";
        showLoginPage();
    } catch (error) {
        setError("register-error", error.message);
    }
}

function handleLogout() {
    stopUnreadPolling();
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("currentUser");
    localStorage.removeItem("currentUserId");
    checkLoginStatus();
}

async function loadPopularMembers() {
    try {
        const [membersResponse, groupsResponse] = await Promise.all([
            fetch(`${API_BASE}/members/`),
            fetch(`${API_BASE}/groups/`),
        ]);
        const members = await readJson(membersResponse);
        const groups = await readJson(groupsResponse);

        memberMap = {};
        groupMap = {};
        $("popular-members").innerHTML = members.map((member) => {
            memberMap[member.MemberID] = member.MemberName;
            return `<option value="${escapeHTML(member.MemberName)}"></option>`;
        }).join("");
        $("popular-groups").innerHTML = groups.map((group) => {
            groupMap[group.GroupID] = group.GroupName;
            return `<option value="${escapeHTML(group.GroupName)}"></option>`;
        }).join("");
    } catch (error) {
        console.error("Failed to load groups and members", error);
    }
}

async function loadUserReputation(userId) {
    try {
        const response = await fetch(`${API_BASE}/users/${userId}/reputation`);
        const data = await readJson(response);
        $("reputation-badge").innerHTML = `<i class="fa-solid fa-star"></i> ${data.Total_Reputation || "5.0"} / 5.0`;
    } catch (error) {
        console.error("Failed to load reputation", error);
    }
}

async function searchProducts() {
    const memberName = $("member-search-input").value.trim();
    const groupName = $("group-search-input").value.trim();
    const grid = $("product-grid");

    grid.innerHTML = '<p style="text-align:center; color:#94a3b8; grid-column:1/-1;">Loading...</p>';

    try {
        const params = new URLSearchParams();
        if (memberName) params.set("member_name", memberName);
        if (groupName) params.set("group_name", groupName);

        const response = await fetch(`${API_BASE}/products/search?${params.toString()}`);
        const products = await readJson(response);
        currentSearchProducts = products;
        $("result-count").innerText = `(${products.length})`;

        if (!products.length) {
            grid.innerHTML = '<p style="text-align:center; color:#94a3b8; grid-column:1/-1;">No available products found.</p>';
            return;
        }

        grid.innerHTML = products.map(renderProductCard).join("");
    } catch (error) {
        console.error(error);
        grid.innerHTML = `<p style="color:#ec4899; text-align:center; grid-column:1/-1;">${escapeHTML(error.message)}</p>`;
    }
}

function renderProductCard(product) {
    const imageUrl = product.ImageUrl
        ? (product.ImageUrl.startsWith("http") ? product.ImageUrl : `${API_BASE}/uploads/${product.ImageUrl}`)
        : null;
    const imageHtml = imageUrl
        ? `<div style="width:100%; height:200px; border-radius:8px; overflow:hidden; margin-bottom:15px;"><img src="${escapeHTML(imageUrl)}" alt="" style="width:100%; height:100%; object-fit:cover;"></div>`
        : `<div style="width:100%; height:200px; border-radius:8px; background:rgba(255,255,255,0.5); display:flex; align-items:center; justify-content:center; color:var(--text-muted); font-size:3rem; margin-bottom:15px;"><i class="fa-regular fa-image"></i></div>`;
    const groupsText = product.GroupNames?.length ? product.GroupNames.join(", ") : "Unknown group";
    const membersText = product.MemberNames?.length ? product.MemberNames.join(", ") : "No member tag";

    return `
        <div class="product-card">
            ${imageHtml}
            <div class="tags">
                <span class="tag condition">${escapeHTML(product.Condition)}</span>
                <span class="tag method">${escapeHTML(product.TradeMethod)}</span>
            </div>
            <h3 style="margin-bottom:5px;">${escapeHTML(product.ProductName)}</h3>
            <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:8px;">${escapeHTML(groupsText)} - ${escapeHTML(membersText)}</p>
            <p style="color:#94a3b8; font-size:0.9rem;">Seller ID: ${product.SellerID}</p>
            <div class="price">NT$ ${Number(product.Price).toFixed(0)}</div>
            <button class="btn-primary" style="width:100%; padding:10px; margin-bottom:8px;" onclick="openProductModal(${product.ProductID})">
                Details
            </button>
            <button class="btn-primary" style="width:100%; padding:10px; background:transparent; border:1px solid var(--secondary); color:var(--secondary);" onclick="openBuyModal(${product.ProductID}, ${Number(product.Price)})">
                Buy
            </button>
        </div>
    `;
}

function matchToProduct(match) {
    return {
        ProductID: match.ProductID,
        SellerID: match.SellerID,
        Price: match.Price,
        ProductName: match.ProductName,
        Description: "",
        Condition: match.Condition,
        TradeMethod: match.TradeMethod,
        Status: "Available",
        ImageUrl: match.ImageUrl,
        MemberNames: match.MemberNames || [],
        GroupNames: match.GroupNames || [],
    };
}

function switchTab(event, tabId) {
    if (event) event.preventDefault();
    document.querySelectorAll(".tab-content").forEach((element) => {
        element.style.display = "none";
    });
    $(`tab-${tabId}`).style.display = "block";

    if (event) {
        document.querySelectorAll("nav a").forEach((element) => element.classList.remove("active"));
        event.currentTarget.classList.add("active");
    }

    if (tabId === "wishlist") loadWishlists();
    if (tabId === "orders") loadOrders();
    if (tabId === "analytics") loadAnalytics();
    if (tabId === "messages") showMessagesPage();
    if (tabId === "profile") loadProfile();
}

function openBuyModal(productId, price) {
    currentSelectedProductId = productId;
    $("modal-price").innerText = `NT$ ${Number(price).toFixed(0)}`;
    $("buy-modal").classList.add("show");
}

async function confirmBuy() {
    if (!currentSelectedProductId) return;
    const button = $("confirm-buy-btn");
    button.innerText = "Processing...";
    button.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/orders/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                BuyerID: CURRENT_USER_ID,
                ProductID: currentSelectedProductId,
            }),
        });
        await readJson(response);
        alert("Order created. Status: Pending.");
        $("buy-modal").classList.remove("show");
        searchProducts();
        loadOrders();
    } catch (error) {
        alert(error.message);
    } finally {
        button.innerText = "Confirm";
        button.disabled = false;
    }
}

function openProductModal(id) {
    const product = currentSearchProducts.find((item) => item.ProductID === id);
    if (!product) return;

    const groupsText = product.GroupNames?.length ? product.GroupNames.join(", ") : "Unknown group";
    const membersText = product.MemberNames?.length ? product.MemberNames.join(", ") : "No member tag";

    $("detail-title").innerText = `${groupsText} - ${membersText}`;
    $("detail-price").innerText = `NT$ ${Number(product.Price).toFixed(0)}`;
    $("detail-name").innerText = product.ProductName;
    $("detail-desc").innerText = product.Description || "No description";
    $("detail-condition").innerText = product.Condition;
    $("detail-method").innerText = product.TradeMethod;
    $("detail-seller-id").innerText = product.SellerID;
    $("detail-seller-rep").innerText = "Loading...";

    const image = $("detail-image");
    const icon = $("detail-image-icon");
    if (product.ImageUrl) {
        image.src = product.ImageUrl.startsWith("http") ? product.ImageUrl : `${API_BASE}/uploads/${product.ImageUrl}`;
        image.style.display = "block";
        icon.style.display = "none";
    } else {
        image.style.display = "none";
        icon.style.display = "block";
    }

    currentSelectedProductId = id;
    $("detail-buy-btn").onclick = () => {
        $("product-modal").classList.remove("show");
        openBuyModal(id, product.Price);
    };
    $("detail-chat-btn").onclick = () => {
        $("product-modal").classList.remove("show");
        openChatModal(id, product.SellerID, product.ProductName);
    };

    $("product-modal").classList.add("show");
    fetch(`${API_BASE}/users/${product.SellerID}/reputation`)
        .then(readJson)
        .then((data) => {
            $("detail-seller-rep").innerText = `${data.Total_Reputation} / 5.0`;
        })
        .catch(() => {
            $("detail-seller-rep").innerText = "Unavailable";
        });
}

async function addWishlist() {
    const memberName = $("wish-member-input").value.trim();
    const groupName = $("wish-group-input").value.trim();
    const price = Number($("wish-price").value);

    if (!memberName || !price) {
        alert("Please enter a member and max price.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/wishlists/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                UserID: CURRENT_USER_ID,
                MaxPrice: price,
                CustomGroupName: groupName || "Unknown Group",
                CustomMemberName: memberName,
            }),
        });
        await readJson(response);
        $("wish-member-input").value = "";
        $("wish-group-input").value = "";
        $("wish-price").value = "";
        await loadPopularMembers();
        await loadWishlists();
    } catch (error) {
        alert(error.message);
    }
}

async function loadWishlists() {
    try {
        const [wishlistResponse, matchResponse] = await Promise.all([
            fetch(`${API_BASE}/users/${CURRENT_USER_ID}/wishlists`),
            fetch(`${API_BASE}/users/${CURRENT_USER_ID}/wishlist_matches`),
        ]);
        const wishlists = await readJson(wishlistResponse);
        const matches = await readJson(matchResponse);
        const grid = $("wishlist-grid");

        const matchedProducts = matches.map(matchToProduct);
        matchedProducts.forEach((product) => {
            if (!currentSearchProducts.some((item) => item.ProductID === product.ProductID)) {
                currentSearchProducts.push(product);
            }
        });

        const matchesHtml = matches.length ? `
            <div style="grid-column:1/-1; margin-bottom:5px;">
                <h3 style="color:var(--primary); margin-bottom:10px;">Matched products</h3>
            </div>
            ${matches.map((match) => `
                <div class="product-card">
                    <div class="tags">
                        <span class="tag condition">Wishlist match</span>
                        <span class="tag method">${escapeHTML(match.MemberName)}</span>
                    </div>
                    <h3>${escapeHTML(match.ProductName)}</h3>
                    <p style="color:var(--text-muted); font-size:0.9rem; margin-top:8px;">${escapeHTML((match.GroupNames || []).join(", ") || "Unknown group")} - ${escapeHTML((match.MemberNames || []).join(", ") || "No member tag")}</p>
                    <p style="color:var(--text-muted); font-size:0.9rem; margin-top:8px;">${escapeHTML(match.Condition)} / ${escapeHTML(match.TradeMethod)}</p>
                    <div class="price">NT$ ${Number(match.Price).toFixed(0)}</div>
                    <button class="btn-primary" style="width:100%; padding:10px; margin-bottom:8px;" onclick="openProductModal(${match.ProductID})">Details</button>
                    <button class="btn-primary" style="width:100%; padding:10px; background:transparent; border:1px solid var(--secondary); color:var(--secondary);" onclick="openBuyModal(${match.ProductID}, ${Number(match.Price)})">Buy</button>
                </div>
            `).join("")}
        ` : "";

        const wishesHtml = wishlists.length ? wishlists.map((wish) => `
            <div class="product-card">
                <div class="tags"><span class="tag method">Watching</span></div>
                <h3>${escapeHTML(memberMap[wish.MemberID] || `Member #${wish.MemberID}`)}</h3>
                <div class="price">Max NT$ ${Number(wish.MaxPrice).toFixed(0)}</div>
                <p style="color:var(--text-muted);">${escapeHTML(wish.ConditionReq || "Any condition")}</p>
            </div>
        `).join("") : '<p style="color:var(--text-muted);">No wishlist items yet.</p>';

        grid.innerHTML = matchesHtml + wishesHtml;
    } catch (error) {
        console.error(error);
    }
}

async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/orders`);
        const orders = await readJson(response);
        const grid = $("orders-grid");
        grid.innerHTML = orders.length ? orders.map((order) => {
            const nextAction = order.Status === "Pending"
                ? `<button onclick="updateOrderStatus(${order.OrderID}, 'Shipped')" class="btn-primary" style="width:100%; margin-top:15px; padding:10px; font-size:0.9rem;">Mark as shipped</button>`
                : order.Status === "Shipped"
                    ? `<button onclick="updateOrderStatus(${order.OrderID}, 'Completed')" class="btn-primary" style="width:100%; margin-top:15px; padding:10px; font-size:0.9rem;">Mark as completed</button>`
                    : `<button onclick="openReviewModal(${order.OrderID})" class="btn-primary" style="width:100%; margin-top:15px; padding:10px; font-size:0.9rem;">Review seller</button>`;
            return `
                <div class="product-card">
                    <div class="tags"><span class="tag condition">${escapeHTML(order.Status)}</span></div>
                    <h3>Order #${order.OrderID}</h3>
                    <p style="color:var(--text-muted); margin-bottom:10px;">Product ID: ${order.ProductID}</p>
                    <div class="price">NT$ ${Number(order.OrderPrice).toFixed(0)}</div>
                    <p style="font-size:0.8rem; color:var(--text-muted); margin-top:15px;">${new Date(order.OrderDate).toLocaleString()}</p>
                    ${nextAction}
                </div>
            `;
        }).join("") : '<p style="color:var(--text-muted);">No orders yet.</p>';
    } catch (error) {
        console.error(error);
    }
}

function renderAnalyticsRows(rows, formatter, emptyText) {
    if (!rows.length) {
        return `<p style="color:var(--text-muted); margin-top:12px;">${emptyText}</p>`;
    }
    return `
        <ul style="list-style:none; padding:0; margin-top:12px; color:var(--text-muted); line-height:1.7;">
            ${rows.map(formatter).join("")}
        </ul>
    `;
}

async function loadAnalytics() {
    const marketBox = $("analytics-market");
    const demandBox = $("analytics-demand");
    const reputationBox = $("analytics-reputation");
    if (!marketBox || !demandBox || !reputationBox) return;

    marketBox.innerHTML = '<p style="color:var(--text-muted); margin-top:12px;">Loading...</p>';
    demandBox.innerHTML = '<p style="color:var(--text-muted); margin-top:12px;">Loading...</p>';
    reputationBox.innerHTML = '<p style="color:var(--text-muted); margin-top:12px;">Loading...</p>';

    try {
        const [marketResponse, demandResponse, rankingResponse] = await Promise.all([
            fetch(`${API_BASE}/analytics/market_average`),
            fetch(`${API_BASE}/analytics/member_demand`),
            fetch(`${API_BASE}/analytics/seller_ranking`),
        ]);
        const market = await readJson(marketResponse);
        const demand = await readJson(demandResponse);
        const ranking = await readJson(rankingResponse);

        marketBox.innerHTML = renderAnalyticsRows(
            market,
            (item) => `<li><strong>${escapeHTML(item.GroupName)} ${escapeHTML(item.MemberName)}</strong><br>Trades: ${item.TradeCount} / Avg NT$ ${Number(item.AveragePrice).toFixed(0)} / Range NT$ ${Number(item.MinPrice).toFixed(0)}-${Number(item.MaxPrice).toFixed(0)}</li>`,
            "No completed order data yet."
        );
        demandBox.innerHTML = renderAnalyticsRows(
            demand,
            (item) => `<li><strong>${escapeHTML(item.GroupName)} ${escapeHTML(item.MemberName)}</strong><br>Wishlist: ${item.WishlistCount} / Avg budget NT$ ${Number(item.AverageBudget).toFixed(0)} / Available matches: ${item.MatchingAvailableProducts}</li>`,
            "No wishlist demand data yet."
        );
        reputationBox.innerHTML = renderAnalyticsRows(
            ranking,
            (item) => `<li><strong>${escapeHTML(item.Account)}</strong> (#${item.SellerID})<br>Reviews: ${item.ReviewCount} / Total ${Number(item.TotalReputation).toFixed(2)} / Packing ${Number(item.AveragePacking).toFixed(2)} / Video ${Number(item.AverageVideo).toFixed(2)} / Speed ${Number(item.AverageSpeed).toFixed(2)}</li>`,
            "No seller review data yet."
        );
    } catch (error) {
        const message = `<p style="color:#ec4899; margin-top:12px;">${escapeHTML(error.message)}</p>`;
        marketBox.innerHTML = message;
        demandBox.innerHTML = message;
        reputationBox.innerHTML = message;
    }
}

async function updateOrderStatus(orderId, status) {
    try {
        const response = await fetch(`${API_BASE}/orders/${orderId}/status`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ Status: status }),
        });
        await readJson(response);
        await loadOrders();
        loadProfile();
    } catch (error) {
        alert(error.message);
    }
}

function openReviewModal(orderId) {
    currentReviewOrderId = orderId;
    $("review-modal").classList.add("show");
}

async function submitReview() {
    if (!currentReviewOrderId) return;

    try {
        const response = await fetch(`${API_BASE}/reviews/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                OrderID: currentReviewOrderId,
                PackingScore: Number($("review-packing").value),
                VideoScore: Number($("review-video").value),
                SpeedScore: Number($("review-speed").value),
                Comment: $("review-comment").value.trim(),
            }),
        });
        await readJson(response);
        alert("Review submitted.");
        $("review-modal").classList.remove("show");
        $("review-comment").value = "";
        loadUserReputation(CURRENT_USER_ID);
        loadOrders();
        loadProfile();
    } catch (error) {
        alert(error.message);
    }
}

async function sellProduct() {
    const groupName = $("sell-group-name").value.trim();
    const memberNames = $("sell-member-names").value.split(",").map((name) => name.trim()).filter(Boolean);
    const productName = $("sell-name").value.trim();
    const price = Number($("sell-price").value);
    const description = $("sell-desc").value.trim();
    const condition = $("sell-condition").value;
    const method = $("sell-method").value;
    const imageInput = $("sell-image");

    if (!groupName || !memberNames.length || !productName || !price) {
        alert("Please fill in group, member, product name, and price.");
        return;
    }

    let imageUrl = null;
    if (imageInput.files.length > 0) {
        const formData = new FormData();
        formData.append("file", imageInput.files[0]);
        try {
            const uploadResponse = await fetch(`${API_BASE}/upload-image/`, {
                method: "POST",
                body: formData,
            });
            const uploadData = await readJson(uploadResponse);
            imageUrl = uploadData.ImageUrl;
        } catch (error) {
            alert(`Image upload failed: ${error.message}`);
            return;
        }
    }

    try {
        const response = await fetch(`${API_BASE}/products/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                SellerID: CURRENT_USER_ID,
                Price: price,
                ProductName: productName,
                Description: description,
                Condition: condition,
                TradeMethod: method,
                MemberIDs: [],
                CustomGroupName: groupName,
                CustomMemberNames: memberNames,
                ImageUrl: imageUrl,
            }),
        });
        await readJson(response);
        alert("Product published.");
        ["sell-group-name", "sell-member-names", "sell-name", "sell-price", "sell-desc"].forEach((id) => {
            $(id).value = "";
        });
        imageInput.value = "";
        await loadPopularMembers();
        switchTab(null, "home");
        searchProducts();
    } catch (error) {
        alert(error.message);
    }
}

async function showMessagesPage() {
    const html = await loadUserChats();
    $("messages-list").innerHTML = html || '<li style="text-align:center; color:var(--text-muted); margin-top:20px;">No chats yet.</li>';
}

async function loadProfile() {
    try {
        const [userResponse, soldResponse, boughtResponse] = await Promise.all([
            fetch(`${API_BASE}/users/${CURRENT_USER_ID}`),
            fetch(`${API_BASE}/users/${CURRENT_USER_ID}/sold_products`),
            fetch(`${API_BASE}/users/${CURRENT_USER_ID}/bought_orders`),
        ]);
        const user = await readJson(userResponse);
        const soldProducts = await readJson(soldResponse);
        const boughtOrders = await readJson(boughtResponse);

        const soldHtml = soldProducts.map((product) => `<li>${escapeHTML(product.ProductName)} - ${escapeHTML(product.Status)} - NT$ ${Number(product.Price).toFixed(0)}</li>`).join("");
        const boughtHtml = boughtOrders.map((order) => `<li>Order #${order.OrderID} - ${escapeHTML(order.ProductName)} - NT$ ${Number(order.OrderPrice).toFixed(0)}</li>`).join("");

        $("profile-container").innerHTML = `
            <p><strong>User ID:</strong> ${user.UserID}</p>
            <p><strong>Account:</strong> ${escapeHTML(user.Account)}</p>
            <p><strong>Email:</strong> ${escapeHTML(user.Email)}</p>
            <p><strong>Seller reputation:</strong> ${user.SellerReputation}</p>
            <p><strong>Buyer reputation:</strong> ${user.BuyerReputation}</p>
            <hr style="margin:20px 0; border:0; border-top:1px solid var(--border);">
            <h3 style="margin-bottom:10px; color:var(--primary);">Selling</h3>
            <ul style="padding-left:20px; margin-bottom:20px; color:var(--text-muted); line-height:1.8;">${soldHtml || "<li>No listed products.</li>"}</ul>
            <h3 style="margin-bottom:10px; color:var(--secondary);">Bought</h3>
            <ul style="padding-left:20px; color:var(--text-muted); line-height:1.8;">${boughtHtml || "<li>No purchases yet.</li>"}</ul>
        `;
    } catch (error) {
        console.error(error);
    }
}

function updateMessagesUnreadBadge(totalUnread) {
    const badge = $("nav-unread-badge");
    if (!badge) return;
    badge.innerText = totalUnread;
    badge.style.display = totalUnread > 0 ? "inline-block" : "none";
}

async function openChatModal(productId, sellerId, productName) {
    if (CURRENT_USER_ID === sellerId) {
        alert("You cannot chat with yourself as the seller.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/chats/create`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                product_id: productId,
                buyer_id: CURRENT_USER_ID,
                seller_id: sellerId,
            }),
        });
        const data = await readJson(response);
        currentChatId = data.chat_id;
        $("chat-title").innerHTML = `<i class="fa-regular fa-comments"></i> ${escapeHTML(productName || "Chat")}`;
        $("chat-modal").classList.add("show");
        await markChatAsRead(currentChatId);
        await loadMessages();
        if (chatPollingInterval) clearInterval(chatPollingInterval);
        chatPollingInterval = setInterval(loadMessages, 3000);
    } catch (error) {
        alert(error.message);
    }
}

function openExistingChat(chatId, productName) {
    currentChatId = chatId;
    $("chat-title").innerHTML = `<i class="fa-regular fa-comments"></i> ${escapeHTML(productName || "Chat")}`;
    $("chat-modal").classList.add("show");
    markChatAsRead(chatId);
    loadMessages();
    if (chatPollingInterval) clearInterval(chatPollingInterval);
    chatPollingInterval = setInterval(loadMessages, 3000);
}

function closeChatModal() {
    $("chat-modal").classList.remove("show");
    if (chatPollingInterval) clearInterval(chatPollingInterval);
    chatPollingInterval = null;
    currentChatId = null;
}

async function markChatAsRead(chatId) {
    if (!chatId) return;
    try {
        await fetch(`${API_BASE}/chats/${chatId}/read?user_id=${CURRENT_USER_ID}`, {
            method: "POST",
        });
        loadUserChats();
    } catch (error) {
        console.error("Failed to mark chat as read", error);
    }
}

async function loadMessages() {
    if (!currentChatId) return;
    const container = $("chat-messages");
    const wasNearBottom = container.scrollHeight - container.clientHeight <= container.scrollTop + 20;

    try {
        const response = await fetch(`${API_BASE}/messages/${currentChatId}`);
        const messages = await readJson(response);
        container.innerHTML = messages.length ? messages.map((message) => {
            const isMe = message.sender_id === CURRENT_USER_ID;
            return `
                <div style="align-self:${isMe ? "flex-end" : "flex-start"}; background:${isMe ? "var(--primary)" : "rgba(255,255,255,0.8)"}; color:${isMe ? "white" : "var(--text-main)"}; padding:10px 15px; border-radius:8px; max-width:80%; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
                    <p style="font-size:0.75rem; margin-bottom:5px; opacity:0.8; font-weight:bold;">${isMe ? "Me" : `User ${message.sender_id}`}</p>
                    <p style="word-break:break-word; font-size:0.95rem;">${escapeHTML(message.message)}</p>
                    <p style="font-size:0.65rem; text-align:right; margin-top:5px; opacity:0.7;">${new Date(message.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</p>
                </div>
            `;
        }).join("") : '<p style="text-align:center; color:var(--text-muted); margin-top:50px;">No messages yet.</p>';

        if (wasNearBottom) container.scrollTop = container.scrollHeight;
    } catch (error) {
        console.error("Failed to load messages", error);
    }
}

async function sendChatMessage() {
    const input = $("chat-input");
    const content = input.value.trim();
    if (!content || !currentChatId) return;

    try {
        const response = await fetch(`${API_BASE}/messages/send`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                chat_id: currentChatId,
                sender_id: CURRENT_USER_ID,
                message: content,
            }),
        });
        await readJson(response);
        input.value = "";
        await loadMessages();
        $("chat-messages").scrollTop = $("chat-messages").scrollHeight;
        loadUserChats();
    } catch (error) {
        alert(error.message);
    }
}

async function loadUserChats() {
    if (!CURRENT_USER_ID) return "";
    try {
        const response = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/chats`);
        const chats = await readJson(response);
        let totalUnread = 0;
        const html = chats.map((chat) => {
            totalUnread += chat.unread_count || 0;
            const itemClass = chat.unread_count ? "unread-chat-item" : "";
            const titleClass = chat.unread_count ? "unread-chat-title" : "";
            const unreadLabel = chat.unread_count ? `<span class="unread-chat-label">${chat.unread_count} unread</span>` : "";
            return `
                <li class="${itemClass}" style="margin-bottom:12px; border-bottom:1px solid var(--glass-border); padding:10px; cursor:pointer;" onclick="openExistingChat(${chat.chat_id}, '${escapeHTML(chat.product_name).replace(/'/g, "\\'")}')">
                    <div class="${titleClass}" style="font-weight:600; color:var(--primary);">
                        <i class="fa-regular fa-comments"></i> ${escapeHTML(chat.product_name)} ${unreadLabel}
                    </div>
                    <div style="font-size:0.9rem; color:var(--text-muted); margin-top:5px;">
                        ${escapeHTML(chat.last_message || "No messages yet.")}
                    </div>
                </li>
            `;
        }).join("");

        updateMessagesUnreadBadge(totalUnread);
        const messagesTab = $("tab-messages");
        if (messagesTab && messagesTab.style.display !== "none") {
            $("messages-list").innerHTML = html || '<li style="text-align:center; color:var(--text-muted); margin-top:20px;">No chats yet.</li>';
        }
        return html;
    } catch (error) {
        console.error("Failed to load chats", error);
        return '<li style="color:#ec4899;">Failed to load chats.</li>';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    setupLanguageToggle();
    $("buy-modal-close").addEventListener("click", () => $("buy-modal").classList.remove("show"));
    $("confirm-buy-btn").addEventListener("click", confirmBuy);
    $("chat-send-btn").addEventListener("click", sendChatMessage);
    $("chat-input").addEventListener("keydown", (event) => {
        if (event.key === "Enter") sendChatMessage();
    });
    window.addEventListener("click", (event) => {
        if (event.target.classList?.contains("modal")) {
            event.target.classList.remove("show");
        }
    });
    checkLoginStatus();
});
