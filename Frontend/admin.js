const API_URL = "https://robo-enhance.onrender.com/admin/activities";
let cachedLogs = [];

// MODAL CONTROLS
function openModal(id) {
    document.getElementById(id).classList.add('active');
    if (id === 'userModal') renderUserList();
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
}

// Close modals on background click
window.onclick = (e) => {
    if (e.target.classList.contains('modal-overlay')) e.target.classList.remove('active');
}

// MAIN LOGIC
async function loadActivities() {
    const tableBody = document.getElementById("logBody");
    const userSelector = document.getElementById("userSelector");
    
    tableBody.innerHTML = `<tr><td colspan="4" class="loading-state"><i class="ri-loader-4-line spin"></i><p>Establishing Secure Link...</p></td></tr>`;

    try {
        const res = await fetch(API_URL, { method: "GET", credentials: 'include' });
        const result = await res.json();
        if (!res.ok) throw new Error(result.error);

        cachedLogs = result.data;
        renderTabs();
        
        tableBody.innerHTML = `<tr><td colspan="4" class="loading-state"><i class="ri-fingerprint-line"></i><p>Access Granted. Select Identity Entity.</p></td></tr>`;
        document.getElementById("logCount").innerText = cachedLogs.length;

    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="4" class="loading-state" style="color:#ff5f5f"><i class="ri-error-warning-line"></i><p>AUTH_ERROR: ${err.message}</p></td></tr>`;
    }
}

function renderTabs() {
    const container = document.getElementById("userSelector");
    container.innerHTML = "";
    const users = [...new Set(cachedLogs.map(l => l.user))];

    users.forEach(user => {
        const btn = document.createElement("button");
        btn.className = "tab-btn";
        btn.innerHTML = `<i class="ri-user-line"></i> ${user}`;
        btn.onclick = () => filterLogs(user, btn);
        container.appendChild(btn);
    });
}

function filterLogs(username, btn) {
    const tableBody = document.getElementById("logBody");
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const filtered = cachedLogs.filter(l => l.user === username);
    tableBody.innerHTML = "";
    
    filtered.forEach((log, i) => {
        const time = new Date(log.time).toLocaleString();
        const row = document.createElement("tr");
        row.style.animation = `rowIn 0.4s ease forwards ${i * 0.05}s`;
        row.style.opacity = "0";

        row.innerHTML = `
            <td><strong style="color:var(--accent)">@${log.user}</strong></td>
            <td><span class="proto-tag">${log.action}</span></td>
            <td>${log.message}</td>
            <td style="color:var(--text-dim); font-size:12px;">${time}</td>
        `;
        tableBody.appendChild(row);
    });
}

function renderUserList() {
    const list = document.getElementById("modalUserList");
    const users = [...new Set(cachedLogs.map(l => l.user))];
    list.innerHTML = users.length ? "" : "<p>No users cached.</p>";
    users.forEach(u => {
        list.innerHTML += `<div class="user-row"><span>${u}</span><span class="admin-tag">TRACKED</span></div>`;
    });
}

// Permissions Toggle logic
document.querySelectorAll('.toggle').forEach(t => {
    t.onclick = () => t.classList.toggle('active');
});

// Row Animation Styles
const style = document.createElement('style');
style.innerHTML = `@keyframes rowIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }`;
document.head.appendChild(style);

document.addEventListener("DOMContentLoaded", loadActivities);