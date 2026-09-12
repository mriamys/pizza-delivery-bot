let tg = window.Telegram.WebApp;
tg.expand();
tg.MainButton.hide();

async function loadData() {
    try {
        // Додаємо timestamp щоб уникнути кешування
        const response = await fetch('data.json?t=' + new Date().getTime());
        const data = await response.json();
        
        document.getElementById('total-orders').innerText = data.total_orders;
        document.getElementById('total-revenue').innerText = data.total_revenue + ' грн';
        
        const list = document.getElementById('orders-list');
        list.innerHTML = '';
        
        if (data.recent_orders.length === 0) {
            list.innerHTML = '<p style="text-align:center;">Ще немає замовлень</p>';
            return;
        }
        
        data.recent_orders.forEach(order => {
            const card = document.createElement('div');
            card.className = 'order-card';
            
            const statuses = ['Нове', 'Готується', 'В дорозі', 'Виконано', 'Скасовано'];
            let optionsHtml = '';
            statuses.forEach(st => {
                const selected = st === order.status ? 'selected' : '';
                optionsHtml += `<option value="${st}" ${selected}>${st}</option>`;
            });
            
            card.innerHTML = `
                <div class="order-header">
                    <span class="order-id">#${order.id}</span>
                    <span class="order-date">${order.date}</span>
                </div>
                <div class="order-client">👤 @${order.username}</div>
                <div class="order-items">🍕 ${order.items}</div>
                <div class="order-footer">
                    <select class="status-select" onchange="updateStatus(${order.id}, this.value)">
                        ${optionsHtml}
                    </select>
                    <span style="color:var(--primary-color)">${order.total} грн</span>
                </div>
            `;
            list.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('orders-list').innerHTML = '<p style="color:red;text-align:center;">Помилка завантаження даних. Можливо, ще немає жодного замовлення.</p>';
    }
}

window.updateStatus = function(orderId, newStatus) {
    const data = {
        action: 'update_status',
        order_id: orderId,
        status: newStatus
    };
    tg.sendData(JSON.stringify(data));
};

// Завантажуємо дані при старті
loadData();

// Кнопка оновлення (нативна Telegram)
tg.SettingsButton.show();
Telegram.WebApp.onEvent('settingsButtonClicked', function() {
    loadData();
    tg.HapticFeedback.impactOccurred('light');
});
