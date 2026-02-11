// ============================================
// CONFIGURATION
// ============================================

const API_BASE_URL = 'http://localhost:5001/api';
const REFRESH_INTERVAL = 30000; // 30 seconds

// ============================================
// STATE MANAGEMENT
// ============================================

let allLeads = [];
let filteredLeads = [];
let currentView = 'dashboard';
let refreshTimer = null;

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    console.log('🚀 Initializing LeadFlow Dashboard...');

    // Setup event listeners
    setupNavigation();
    setupRefreshButton();
    setupFilters();
    setupModal();

    // Load initial data
    loadDashboardData();

    // Start auto-refresh
    startAutoRefresh();

    console.log('✅ Dashboard initialized successfully');
}

// ============================================
// NAVIGATION
// ============================================

function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const view = item.getAttribute('data-view');
            switchView(view);
        });
    });

    // Handle "View All" link
    const viewAllLinks = document.querySelectorAll('[data-view="leads"]');
    viewAllLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchView('leads');
        });
    });
}

function switchView(view) {
    currentView = view;

    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-view') === view) {
            item.classList.add('active');
        }
    });

    // Update views
    document.querySelectorAll('.view').forEach(v => {
        v.classList.remove('active');
    });
    document.getElementById(`${view}-view`).classList.add('active');

    // Update header
    const titles = {
        dashboard: { title: 'Dashboard Overview', subtitle: 'Real-time lead management system' },
        leads: { title: 'All Leads', subtitle: 'Complete list of all leads from Telegram' },
        analytics: { title: 'Analytics', subtitle: 'Performance metrics and insights' }
    };

    document.getElementById('page-title').textContent = titles[view].title;
    document.getElementById('page-subtitle').textContent = titles[view].subtitle;

    // Load view-specific data
    if (view === 'leads') {
        renderAllLeads();
    }
}

// ============================================
// DATA LOADING
// ============================================

async function loadDashboardData() {
    console.log('📊 Synchronizing Lead Data...');

    try {
        const [leadsResponse, statsResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/leads`),
            fetch(`${API_BASE_URL}/stats`)
        ]);

        if (!leadsResponse.ok) throw new Error('Backend Offline');

        const leadsData = await leadsResponse.json();
        const statsData = await statsResponse.json();

        // Update System Status Labels
        updateSystemStatus(leadsData.config_status);

        // Store and Render
        allLeads = leadsData.leads || [];
        filteredLeads = [...allLeads];
        updateStats(statsData.stats);
        renderRecentLeads();

    } catch (error) {
        console.error('❌ Sync Error:', error);
        showErrorState(error.message);
    }
}

function updateSystemStatus(config) {
    const statusText = document.querySelector('.status-indicator span');
    const statusDot = document.querySelector('.status-dot');

    if (config && config.clickup_connected && config.list_id_set) {
        statusText.textContent = 'System Online (ClickUp LIVE)';
        statusText.style.color = '#10b981';
        statusDot.style.background = '#10b981';
    } else {
        statusText.textContent = 'System Online (Local Dashboard Only)';
        statusText.style.color = '#3b82f6';
        statusDot.style.background = '#3b82f6';
        console.warn("⚠️ ClickUp API keys in .env are likely invalid. Leads are showing from local cache only.");
    }
}

function updateStats(stats) {
    // Update stat cards
    document.getElementById('total-leads').textContent = stats.total_leads || 0;

    // Calculate active leads (TO DO + IN PROGRESS)
    const activeCount = (stats.by_status['TO DO'] || 0) + (stats.by_status['IN PROGRESS'] || 0);
    document.getElementById('active-leads').textContent = activeCount;

    // Pending leads (TO DO)
    document.getElementById('pending-leads').textContent = stats.by_status['TO DO'] || 0;

    // Conversion rate (mock calculation)
    const completedCount = stats.by_status['COMPLETE'] || 0;
    const conversionRate = stats.total_leads > 0
        ? Math.round((completedCount / stats.total_leads) * 100)
        : 0;
    document.getElementById('conversion-rate').textContent = `${conversionRate}%`;
}

function renderRecentLeads() {
    const tbody = document.getElementById('recent-leads-body');

    if (allLeads.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 2rem; color: var(--text-muted);">
                    <p>No leads found. Send a message to your Telegram bot to create a lead!</p>
                </td>
            </tr>
        `;
        return;
    }

    // Show only the 5 most recent leads
    const recentLeads = allLeads.slice(0, 5);

    tbody.innerHTML = recentLeads.map(lead => `
        <tr>
            <td>
                <strong>${escapeHtml(lead.name)}</strong>
            </td>
            <td>
                <span class="badge ${getStatusClass(lead.status)}">
                    ${escapeHtml(lead.status)}
                </span>
            </td>
            <td>
                <span class="badge ${getPriorityClass(lead.priority)}">
                    ${escapeHtml(lead.priority)}
                </span>
            </td>
            <td>
                <span style="color: var(--text-secondary);">
                    ${formatDate(lead.created_at)}
                </span>
            </td>
            <td>
                <button class="btn-view" onclick="viewLeadDetails('${lead.id}')">
                    View
                </button>
            </td>
        </tr>
    `).join('');
}

function renderAllLeads() {
    const tbody = document.getElementById('all-leads-body');

    if (filteredLeads.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 2rem; color: var(--text-muted);">
                    <p>No leads match your filters.</p>
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = filteredLeads.map(lead => `
        <tr>
            <td>
                <strong>${escapeHtml(lead.name)}</strong>
            </td>
            <td>
                <span style="color: var(--text-secondary); font-size: 0.875rem;">
                    ${truncateText(stripMarkdown(lead.description), 50)}
                </span>
            </td>
            <td>
                <span class="badge ${getStatusClass(lead.status)}">
                    ${escapeHtml(lead.status)}
                </span>
            </td>
            <td>
                <span class="badge ${getPriorityClass(lead.priority)}">
                    ${escapeHtml(lead.priority)}
                </span>
            </td>
            <td>
                <span style="color: var(--text-secondary);">
                    ${formatDate(lead.created_at)}
                </span>
            </td>
            <td>
                <button class="btn-view" onclick="viewLeadDetails('${lead.id}')">
                    View
                </button>
            </td>
        </tr>
    `).join('');
}

// ============================================
// FILTERS
// ============================================

function setupFilters() {
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');

    statusFilter.addEventListener('change', applyFilters);
    priorityFilter.addEventListener('change', applyFilters);
}

function applyFilters() {
    const statusFilter = document.getElementById('status-filter').value;
    const priorityFilter = document.getElementById('priority-filter').value;

    filteredLeads = allLeads.filter(lead => {
        const matchesStatus = !statusFilter || lead.status === statusFilter;
        const matchesPriority = !priorityFilter || lead.priority === priorityFilter;
        return matchesStatus && matchesPriority;
    });

    renderAllLeads();
}

// ============================================
// MODAL
// ============================================

function setupModal() {
    const modal = document.getElementById('lead-modal');
    const closeBtn = document.getElementById('close-modal');

    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
}

async function viewLeadDetails(leadId) {
    const modal = document.getElementById('lead-modal');
    const modalBody = document.getElementById('modal-body');

    // Show modal with loading state
    modal.classList.add('active');
    modalBody.innerHTML = `
        <div style="text-align: center; padding: 2rem;">
            <div class="loading-spinner"></div>
            <p>Loading lead details...</p>
        </div>
    `;

    try {
        const response = await fetch(`${API_BASE_URL}/leads/${leadId}`);
        if (!response.ok) throw new Error('Failed to fetch lead details');

        const data = await response.json();
        const lead = data.lead;

        modalBody.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div>
                    <h4 style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">LEAD NAME</h4>
                    <p style="font-size: 1.25rem; font-weight: 600;">${escapeHtml(lead.name)}</p>
                </div>
                
                <div>
                    <h4 style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">DESCRIPTION</h4>
                    <div style="background: var(--surface-light); padding: 1rem; border-radius: var(--radius-md); white-space: pre-wrap;">
                        ${escapeHtml(stripMarkdown(lead.description)) || 'No description provided'}
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                    <div>
                        <h4 style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">STATUS</h4>
                        <span class="badge ${getStatusClass(lead.status)}">${escapeHtml(lead.status)}</span>
                    </div>
                    <div>
                        <h4 style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">PRIORITY</h4>
                        <span class="badge ${getPriorityClass(lead.priority)}">${escapeHtml(lead.priority)}</span>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                    <div>
                        <h4 style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">CREATED</h4>
                        <p>${formatDate(lead.created_at)}</p>
                    </div>
                    <div>
                        <h4 style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">UPDATED</h4>
                        <p>${formatDate(lead.updated_at)}</p>
                    </div>
                </div>
                
                ${lead.url ? `
                    <div>
                        <a href="${lead.url}" target="_blank" class="btn-view" style="display: inline-block; text-decoration: none;">
                            Open in ClickUp →
                        </a>
                    </div>
                ` : ''}
            </div>
        `;

    } catch (error) {
        console.error('Error loading lead details:', error);
        modalBody.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: var(--danger);">
                <p>Failed to load lead details. Please try again.</p>
            </div>
        `;
    }
}

// ============================================
// REFRESH
// ============================================

function setupRefreshButton() {
    const refreshBtn = document.getElementById('refresh-btn');
    refreshBtn.addEventListener('click', async () => {
        refreshBtn.style.animation = 'spin 1s linear';
        await loadDashboardData();
        setTimeout(() => {
            refreshBtn.style.animation = '';
        }, 1000);
    });
}

function startAutoRefresh() {
    refreshTimer = setInterval(() => {
        console.log('🔄 Auto-refreshing data...');
        loadDashboardData();
    }, REFRESH_INTERVAL);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function getStatusClass(status) {
    const statusMap = {
        'TO DO': 'status-todo',
        'IN PROGRESS': 'status-in-progress',
        'COMPLETE': 'status-complete'
    };
    return statusMap[status] || 'status-todo';
}

function getPriorityClass(priority) {
    const priorityMap = {
        'Urgent': 'priority-urgent',
        'High': 'priority-high',
        'Normal': 'priority-normal',
        'Low': 'priority-low'
    };
    return priorityMap[priority] || 'priority-normal';
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';

    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function stripMarkdown(text) {
    if (!text) return '';
    // Remove markdown formatting
    return text
        .replace(/\*\*/g, '')
        .replace(/\*/g, '')
        .replace(/\n/g, ' ')
        .replace(/#{1,6}\s/g, '');
}

function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

function showLoadingState() {
    const tbody = document.getElementById('recent-leads-body');
    tbody.innerHTML = `
        <tr class="loading-row">
            <td colspan="5">
                <div class="loading-spinner"></div>
                <p>Loading leads...</p>
            </td>
        </tr>
    `;
}

function showErrorState(message) {
    const tbody = document.getElementById('recent-leads-body');
    tbody.innerHTML = `
        <tr>
            <td colspan="5" style="text-align: center; padding: 2rem; color: var(--danger);">
                <p>⚠️ Error: ${escapeHtml(message)}</p>
                <p style="color: var(--text-muted); margin-top: 0.5rem;">Make sure the backend server is running on port 5000</p>
            </td>
        </tr>
    `;
}

// ============================================
// EXPORT FOR INLINE ONCLICK HANDLERS
// ============================================

window.viewLeadDetails = viewLeadDetails;
