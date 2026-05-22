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

function $(id) {
    return document.getElementById(id);
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
        alert("Purchase completed.");
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
        const response = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/wishlists`);
        const wishlists = await readJson(response);
        const grid = $("wishlist-grid");
        grid.innerHTML = wishlists.length ? wishlists.map((wish) => `
            <div class="product-card">
                <div class="tags"><span class="tag method">Watching</span></div>
                <h3>${escapeHTML(memberMap[wish.MemberID] || `Member #${wish.MemberID}`)}</h3>
                <div class="price">Max NT$ ${Number(wish.MaxPrice).toFixed(0)}</div>
                <p style="color:var(--text-muted);">${escapeHTML(wish.ConditionReq || "Any condition")}</p>
            </div>
        `).join("") : '<p style="color:var(--text-muted);">No wishlist items yet.</p>';
    } catch (error) {
        console.error(error);
    }
}

async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE}/users/${CURRENT_USER_ID}/orders`);
        const orders = await readJson(response);
        const grid = $("orders-grid");
        grid.innerHTML = orders.length ? orders.map((order) => `
            <div class="product-card">
                <div class="tags"><span class="tag condition">${escapeHTML(order.Status)}</span></div>
                <h3>Order #${order.OrderID}</h3>
                <p style="color:var(--text-muted); margin-bottom:10px;">Product ID: ${order.ProductID}</p>
                <div class="price">NT$ ${Number(order.OrderPrice).toFixed(0)}</div>
                <p style="font-size:0.8rem; color:var(--text-muted); margin-top:15px;">${new Date(order.OrderDate).toLocaleString()}</p>
                ${order.Status === "Completed" ? `<button onclick="openReviewModal(${order.OrderID})" class="btn-primary" style="width:100%; margin-top:15px; padding:10px; font-size:0.9rem;">Review seller</button>` : ""}
            </div>
        `).join("") : '<p style="color:var(--text-muted);">No orders yet.</p>';
    } catch (error) {
        console.error(error);
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
