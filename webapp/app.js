let tg = window.Telegram.WebApp;
tg.expand(); // Розгорнути на весь екран
tg.MainButton.color = "#ff8a00"; // Змінити колір головної кнопки під дизайн
tg.MainButton.textColor = "#ffffff";

const pizzas = [
    { id: 1, name: "Маргарита", price: 150, desc: "Сир, томати, базилік", image: "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=300&q=80" },
    { id: 2, name: "Пепероні", price: 200, desc: "Сир, ковбаса пепероні", image: "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300&q=80" },
    { id: 3, name: "Гавайська", price: 180, desc: "Курка, ананаси, сир", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=300&q=80" },
    { id: 4, name: "4 Сири", price: 220, desc: "Дорблю, пармезан, чеддер, моцарела", image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300&q=80" },
    { id: 5, name: "М'ясна", price: 250, desc: "Бекон, салямі, шинка, сир", image: "https://images.unsplash.com/photo-1590947132387-155cc02f3212?w=300&q=80" },
    { id: 6, name: "Веганська", price: 160, desc: "Томати, гриби, перець, оливки", image: "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=300&q=80" }
];

let cart = {}; // Об'єкт для зберігання кількості товарів {id: count}

function renderPizzas() {
    const list = document.getElementById('pizza-list');
    list.innerHTML = '';
    
    pizzas.forEach(pizza => {
        const count = cart[pizza.id] || 0;
        
        const card = document.createElement('div');
        card.className = 'pizza-card';
        
        let controlsHtml = '';
        if (count === 0) {
            controlsHtml = `<button class="btn" onclick="add(${pizza.id})">Додати</button>`;
        } else {
            // Кнопки плюс та мінус, якщо товар вже в кошику
            controlsHtml = `
                <div class="controls">
                    <button class="btn-icon" onclick="remove(${pizza.id})">-</button>
                    <span class="count">${count}</span>
                    <button class="btn-icon" onclick="add(${pizza.id})">+</button>
                </div>
            `;
        }
        
        card.innerHTML = `
            <img src="${pizza.image}" alt="${pizza.name}" class="pizza-image">
            <div class="pizza-info">
                <h3>${pizza.name}</h3>
                <p class="desc">${pizza.desc}</p>
                <p class="price">${pizza.price} грн</p>
            </div>
            <div class="card-controls" id="controls-${pizza.id}">
                ${controlsHtml}
            </div>
        `;
        list.appendChild(card);
    });
}

function add(id) {
    if (!cart[id]) {
        cart[id] = 0;
    }
    cart[id]++;
    renderPizzas();
    updateMainButton();
    // Легка вібрація для кращого UX
    tg.HapticFeedback.selectionChanged();
}

function remove(id) {
    if (cart[id] > 0) {
        cart[id]--;
        if (cart[id] === 0) {
            delete cart[id];
        }
    }
    renderPizzas();
    updateMainButton();
    tg.HapticFeedback.selectionChanged();
}

function updateMainButton() {
    let total = 0;
    let count = 0;
    
    for (let id in cart) {
        const pizza = pizzas.find(p => p.id == id);
        total += pizza.price * cart[id];
        count += cart[id];
    }
    
    // Якщо ми в Telegram (ініціалізаційні дані не порожні)
    if (tg.initData !== "") {
        let fallbackBtn = document.getElementById('fallback-cart');
        fallbackBtn.style.display = 'none'; // Ховаємо нашу запасну кнопку
        
        if (total > 0) {
            tg.MainButton.text = `Оформити замовлення (${total} грн)`;
            tg.MainButton.show();
        } else {
            tg.MainButton.hide();
        }
    } else {
        // Якщо ми в звичайному браузері (для тестів)
        let fallbackBtn = document.getElementById('fallback-cart');
        if (total > 0) {
            fallbackBtn.style.display = 'block';
            fallbackBtn.innerText = `🛒 Оформити замовлення (${total} грн)`;
        } else {
            fallbackBtn.style.display = 'none';
        }
    }
}

Telegram.WebApp.onEvent("mainButtonClicked", function() {
    submitOrder();
});

function submitOrder() {
    let orderDetails = [];
    let totalPrice = 0;
    
    for (let id in cart) {
        const pizza = pizzas.find(p => p.id == id);
        const qty = cart[id];
        orderDetails.push(`${pizza.name} (x${qty})`);
        totalPrice += pizza.price * qty;
    }
    
    const data = {
        items: orderDetails.join(', '),
        total: totalPrice
    };
    
    if (tg.initData !== "") {
        tg.sendData(JSON.stringify(data));
    } else {
        alert("Успішно! Дані кошика: " + JSON.stringify(data) + "\n\n(Ви в браузері, тому замовлення не пішло в Telegram)");
    }
}

// Первинне відмальовування меню
renderPizzas();
