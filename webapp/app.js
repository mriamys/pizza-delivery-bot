let tg = window.Telegram.WebApp;
tg.expand(); // Розгорнути на весь екран
tg.MainButton.color = "#ff8a00"; // Змінити колір головної кнопки під дизайн
tg.MainButton.textColor = "#ffffff";

const pizzas = [
    { id: 1, name: "Маргарита", price: 150, desc: "Сир, томати, базилік", image: "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=300&q=80" },
    { id: 2, name: "Пепероні", price: 200, desc: "Сир, ковбаса пепероні", image: "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300&q=80" },
    { id: 3, name: "Гавайська", price: 180, desc: "Курка, ананаси, сир", image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=300&q=80" },
    { id: 4, name: "4 Сири", price: 220, desc: "Дорблю, пармезан, чеддер, моцарела", image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300&q=80" },
    { id: 5, name: "М'ясна", price: 250, desc: "Бекон, салямі, шинка, сир", image: "https://images.unsplash.com/photo-1534308983496-4fbf1a0d0bf2?w=300&q=80" },
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
    
    if (total > 0) {
        tg.MainButton.text = `Оформити замовлення (${total} грн)`;
        tg.MainButton.show();
    } else {
        tg.MainButton.hide();
    }
}

Telegram.WebApp.onEvent("mainButtonClicked", function() {
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
    
    // Надсилаємо дані боту для запису в БД
    tg.sendData(JSON.stringify(data));
});

// Первинне відмальовування меню
renderPizzas();
