let inventory = JSON.parse(localStorage.getItem('boutique_inventory')) || [];

const sampleData = [
    // Ko'ylaklar (Dresses)
    { id: 1, brand: "Zara", name: "Fransuzcha ko'ylak (Uzun, ipak)", price: 850000, size: "M", color: "Zangori", date: "2024-05-01", total: 12, sold: 10, discount: 10 },
    { id: 2, brand: "Gucci", name: "Fransuzcha ko'ylak (Kalta, shifon)", price: 560000, size: "S", color: "Oq", date: "2024-05-02", total: 15, sold: 14, discount: 0 },
    { id: 3, brand: "Armani", name: "Klassik kostyum shim", price: 2500000, size: "XL", color: "To'q ko'k", date: "2024-05-03", total: 10, sold: 1, discount: 5 },
    { id: 4, brand: "H&M", name: "Kundalik ko'ylak (Paxta)", price: 350000, size: "M", color: "Yashil", date: "2024-05-04", total: 20, sold: 18, discount: 0 },
    
    // Yubkalar (Skirts)
    { id: 5, brand: "Chanel", name: "Klassik yubka (Uzun, plissey)", price: 420000, size: "S", color: "Jigarrang", date: "2024-05-05", total: 18, sold: 16, discount: 20 },
    { id: 6, brand: "Prada", name: "Kalta yubka (Jinsi)", price: 280000, size: "M", color: "Moviy", date: "2024-05-06", total: 25, sold: 24, discount: 0 },
    { id: 7, brand: "Versace", name: "Yubka-qalam (Ofis uchun)", price: 380000, size: "L", color: "To'q ko'k", date: "2024-05-07", total: 14, sold: 3, discount: 5 },
    { id: 8, brand: "Mango", name: "Mini yubka (Charm)", price: 450000, size: "XS", color: "Qizil", date: "2024-05-08", total: 10, sold: 2, discount: 0 },
    
    // Futbolkalar (T-shirts)
    { id: 9, brand: "Nike", name: "Futbolka (100% Paxta)", price: 120000, size: "M", color: "Sariq", date: "2024-05-09", total: 40, sold: 38, discount: 0 },
    { id: 10, brand: "Adidas", name: "Futbolka (Lakra)", price: 150000, size: "L", color: "Pushti", date: "2024-05-10", total: 35, sold: 12, discount: 10 },
    { id: 11, brand: "Puma", name: "Futbolka (Saten)", price: 180000, size: "S", color: "Kulrang", date: "2024-05-11", total: 25, sold: 5, discount: 0 },
    
    // Koftalar va Kostyumlar (Cardigans & Sets)
    { id: 12, brand: "Fendi", name: "Kofta (Junli, trikotaj)", price: 520000, size: "M", color: "Bej", date: "2024-05-12", total: 15, sold: 4, discount: 0 },
    { id: 13, brand: "Burberry", name: "Yubka va kofta to'plami", price: 950000, size: "L", color: "Siyohrang", date: "2024-05-13", total: 10, sold: 8, discount: 30 },
    { id: 14, brand: "Zara", name: "Kardigan (Yengil)", price: 330000, size: "XL", color: "Oq", date: "2024-05-14", total: 20, sold: 6, discount: 0 },
    { id: 15, brand: "Mango", name: "Ayollar jeketi", price: 720000, size: "M", color: "Pista rang", date: "2024-05-15", total: 12, sold: 3, discount: 10 }
];

// Elementlar
const form = document.getElementById('clothing-form');
const tableBody = document.getElementById('inventory-body');
const searchInput = document.getElementById('search');
const totalItemsEl = document.getElementById('total-items');
const totalSalesEl = document.getElementById('total-sales');
const lowStockAlert = document.getElementById('low-stock-alert');
const addSampleBtn = document.getElementById('add-sample-data');

// Dasturni boshlash
function init() {
    // Agar baza bo'sh bo'lsa yoki eski formatda bo'lsa (brend yo'q bo'lsa), yangilaymiz
    const isOldData = inventory.length > 0 && !inventory[0].hasOwnProperty('brand');
    
    if (inventory.length === 0 || isOldData) {
        inventory = [...sampleData];
        saveInventory();
    }
    renderTable();
    updateStats();
}

// Jadvalni chizish
function renderTable(filter = '') {
    tableBody.innerHTML = '';
    lowStockAlert.innerHTML = '';
    
    const filtered = inventory.filter(item => 
        item.name.toLowerCase().includes(filter.toLowerCase()) ||
        item.brand?.toLowerCase().includes(filter.toLowerCase()) ||
        item.color.toLowerCase().includes(filter.toLowerCase())
    );

    filtered.forEach(item => {
        const remaining = item.total - item.sold;
        
        // Kam qolgan mahsulot ogohlantirishi
        if (remaining > 0 && remaining < 3) {
            const alert = document.createElement('div');
            alert.className = 'low-stock-warning';
            alert.innerHTML = `
                <span>⚠️ <strong>DIQQAT:</strong> "${item.name}" (Brend: ${item.brand || 'Noma\'lum'}) mahsulotidan atigi ${remaining} ta qoldi!</span>
                <button onclick="sellItem(${item.id})" class="btn-sm btn-sell">Sotish</button>
            `;
            lowStockAlert.appendChild(alert);
        }

        const discount = item.discount || 0;
        const currentPrice = discount > 0 ? item.price * (1 - discount/100) : item.price;
        const itemRevenue = item.sold * currentPrice;
        
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>#${item.id}</td>
            <td class="brand-name">${item.brand || '---'}</td>
            <td style="font-weight: 600">${item.name}</td>
            <td>
                ${discount > 0 ? `<span class="old-price">${item.price.toLocaleString()} so'm</span>` : ''}
                <span style="color: var(--primary-dark); font-weight: bold">
                    ${currentPrice.toLocaleString()} so'm 
                    ${discount > 0 ? `<span class="discount-badge">-${discount}%</span>` : ''}
                </span>
            </td>
            <td><span class="badge" style="background: #eee">${item.size}</span></td>
            <td>${item.color}</td>
            <td style="color: #95a5a6; font-size: 0.9rem">${item.date}</td>
            <td>${item.total}</td>
            <td><span class="badge badge-warning">${item.sold}</span></td>
            <td><span class="badge ${remaining > 5 ? 'badge-success' : remaining > 0 ? 'badge-warning' : 'badge-danger'}">${remaining}</span></td>
            <td style="font-weight: 700; color: #27ae60">${itemRevenue.toLocaleString()} so'm</td>
            <td class="actions">
                <button onclick="sellItem(${item.id})" class="btn-sm btn-sell">Sotish</button>
                <button onclick="deleteItem(${item.id})" class="btn-sm btn-delete">O'chirish</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Yangi mahsulot qo'shish (Dublikatlarni tekshirish bilan)
form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const brand = document.getElementById('brand').value.trim();
    const name = document.getElementById('name').value.trim();
    const price = parseInt(document.getElementById('price').value);
    const size = document.getElementById('size').value;
    const color = document.getElementById('color').value.trim();
    const quantity = parseInt(document.getElementById('quantity').value);
    
    // Mavjud mahsulotni qidirish (Brend, nomi, rangi va razmeri bir xil bo'lsa)
    const existingItem = inventory.find(item => 
        item.brand?.toLowerCase() === brand.toLowerCase() &&
        item.name.toLowerCase() === name.toLowerCase() && 
        item.color.toLowerCase() === color.toLowerCase() &&
        item.size === size
    );

    if (existingItem) {
        // Agar bor bo'lsa, sonini qo'shamiz
        existingItem.total += quantity;
        existingItem.price = price; 
        showToast(`"${brand} ${name}" mavjud ekan, uning soniga ${quantity} ta qo'shildi.`);
    } else {
        // Agar yo'q bo'lsa, yangi yaratamiz
        const newItem = {
            id: inventory.length > 0 ? Math.max(...inventory.map(i => i.id)) + 1 : 1,
            brand: brand,
            name: name,
            price: price,
            size: size,
            color: color,
            total: quantity,
            sold: 0,
            date: new Date().toISOString().split('T')[0],
            discount: 0
        };
        inventory.push(newItem);
        showToast("Yangi mahsulot muvaffaqiyatli qo'shildi!");
    }

    saveInventory();
    renderTable();
    updateStats();
    form.reset();
});

// Modal Elementlari
const sellModal = document.getElementById('sell-modal');
const modalItemName = document.getElementById('modal-item-name');
const modalItemPrice = document.getElementById('modal-item-price');
const sellQtyInput = document.getElementById('sell-qty');
const modalTotalPrice = document.getElementById('modal-total-price');
const confirmSellBtn = document.getElementById('confirm-sell');
const cancelSellBtn = document.getElementById('cancel-sell');

let currentItemToSell = null;

// Sotish (Maxsus Modal orqali)
window.sellItem = function(id) {
    const item = inventory.find(i => i.id === id);
    const remaining = item.total - item.sold;
    
    if (remaining <= 0) {
        showToast("Omborda qolmagan!", "danger");
        return;
    }

    currentItemToSell = item;
    modalItemName.innerText = item.name;
    modalItemPrice.innerText = `Donasi: ${item.price.toLocaleString()} so'm`;
    sellQtyInput.value = 1;
    sellQtyInput.max = remaining;
    updateModalTotal();
    
    sellModal.style.display = 'flex';
}

// Modalda jami summani hisoblash
function updateModalTotal() {
    if (!currentItemToSell) return;
    const qty = parseInt(sellQtyInput.value) || 0;
    const total = qty * currentItemToSell.price;
    modalTotalPrice.innerText = total.toLocaleString() + " so'm";
}

sellQtyInput.addEventListener('input', updateModalTotal);

// Tasdiqlash
confirmSellBtn.addEventListener('click', () => {
    const qty = parseInt(sellQtyInput.value);
    const remaining = currentItemToSell.total - currentItemToSell.sold;

    if (isNaN(qty) || qty <= 0) {
        showToast("Noto'g'ri miqdor kiritildi!", "danger");
        return;
    }

    if (qty > remaining) {
        showToast(`Xato: Omborda bor-yog'i ${remaining} ta mahsulot bor!`, "danger");
        return;
    }

    currentItemToSell.sold += qty;
    const discount = currentItemToSell.discount || 0;
    const currentPrice = discount > 0 ? currentItemToSell.price * (1 - discount/100) : currentItemToSell.price;
    const totalPrice = qty * currentPrice;
    
    saveInventory();
    renderTable(searchInput.value);
    updateStats();
    
    sellModal.style.display = 'none';
    showToast(`${qty} ta ${currentItemToSell.name} sotildi. Jami: ${totalPrice.toLocaleString()} so'm`);
});

// Bekor qilish
cancelSellBtn.addEventListener('click', () => {
    sellModal.style.display = 'none';
});

// O'chirish
window.deleteItem = function(id) {
    if (confirm("Haqiqatan ham o'chirmoqchimisiz?")) {
        inventory = inventory.filter(i => i.id !== id);
        saveInventory();
        renderTable(searchInput.value);
        updateStats();
        showToast("Mahsulot o'chirildi");
    }
}

// Qidiruv
searchInput.addEventListener('input', (e) => {
    renderTable(e.target.value);
});

// Statistikani yangilash
function updateStats() {
    totalItemsEl.innerText = inventory.length;
    
    const totalSoldQty = inventory.reduce((sum, item) => sum + item.sold, 0);
    totalSalesEl.innerText = totalSoldQty;
    
    const totalRevenue = inventory.reduce((sum, item) => {
        const discount = item.discount || 0;
        const currentPrice = discount > 0 ? item.price * (1 - discount/100) : item.price;
        return sum + (item.sold * currentPrice);
    }, 0);
    
    const revenueEl = document.getElementById('total-revenue');
    if (revenueEl) {
        revenueEl.innerText = totalRevenue.toLocaleString() + " so'm";
    }
}

// Saqlash
function saveInventory() {
    localStorage.setItem('boutique_inventory', JSON.stringify(inventory));
}

// Toast xabari
function showToast(msg, type = 'success') {
    const toast = document.getElementById('toast');
    toast.innerText = msg;
    toast.style.background = type === 'danger' ? '#e74c3c' : '#2c3e50';
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// Namuna ma'lumotlarni qayta yuklash
addSampleBtn.addEventListener('click', () => {
    if (confirm("Mavjud ma'lumotlarni o'chirib, namunaviy ma'lumotlarni qaytadan yuklamoqchimisiz?")) {
        inventory = [...sampleData];
        saveInventory();
        renderTable();
        updateStats();
        showToast("Namunaviy ma'lumotlar yuklandi!");
    }
});

init();
