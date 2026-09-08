let tg = window.Telegram.WebApp;
tg.expand();

const pizzas = [
    { id: 1, name: "Маргарита", price: 150, desc: "Сир, томати, базилік" },
    { id: 2, name: "Пепероні", price: 200, desc: "Сир, ковбаса пепероні" },
    { id: 3, name: "Гавайська", price: 180, desc: "Курка, ананаси, сир" },
    { id: 4, name: "4 Сири", price: 220, desc: "Моцарела, дорблю, пармезан, чеддер" }
];

let cart = [];

function renderPizzas() {
    const list = document.getElementById('pizza-list');
    pizzas.forEach(pizza => {
        const item = document.createElement('div');
        item.className = 'pizza-item';
        item.innerHTML = `
            <div class="pizza-info">
                <h3>${pizza.name}</h3>
                <p>${pizza.desc}</p>
                <b>${pizza.price} грн</b>
            </div>
            <button class="add-btn" id="btn-${pizza.id}" onclick="togglePizza(${pizza.id})">Додати</button>
        `;
        list.appendChild(item);
    });
}

function togglePizza(id) {
    const btn = document.getElementById(`btn-${id}`);
    const index = cart.indexOf(id);
    if (index > -1) {
        cart.splice(index, 1);
        btn.innerText = "Додати";
        btn.classList.remove('added');
    } else {
        cart.push(id);
        btn.innerText = "У кошику";
        btn.classList.add('added');
    }
    updateMainButton();
}

function updateMainButton() {
    if (cart.length > 0) {
        let total = 0;
        cart.forEach(id => {
            const pizza = pizzas.find(p => p.id === id);
            total += pizza.price;
        });
        tg.MainButton.text = `Замовити (${total} грн)`;
        tg.MainButton.show();
    } else {
        tg.MainButton.hide();
    }
}

Telegram.WebApp.onEvent("mainButtonClicked", function() {
    let orderDetails = [];
    let totalPrice = 0;
    cart.forEach(id => {
        const pizza = pizzas.find(p => p.id === id);
        orderDetails.push(pizza.name);
        totalPrice += pizza.price;
    });
    
    const data = {
        items: orderDetails.join(', '),
        total: totalPrice
    };
    
    tg.sendData(JSON.stringify(data));
});

renderPizzas();
