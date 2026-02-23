// ============================================
// GhostTrack v3.0 - Renderer Process
// ============================================

document.addEventListener('DOMContentLoaded', () => {
  // --- Window Controls ---
  document.getElementById('btn-minimize').addEventListener('click', () => window.ghostAPI.minimize());
  document.getElementById('btn-maximize').addEventListener('click', () => window.ghostAPI.maximize());
  document.getElementById('btn-close').addEventListener('click', () => window.ghostAPI.close());

  // --- Navigation ---
  const navBtns = document.querySelectorAll('.nav-btn');
  const pages = document.querySelectorAll('.page');

  navBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetPage = btn.dataset.page;

      navBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');

      pages.forEach((p) => p.classList.remove('active'));
      document.getElementById(`page-${targetPage}`).classList.add('active');
    });
  });

  // --- Utility Functions ---

  function setLoading(button, loading) {
    const text = button.querySelector('.btn-text');
    const loader = button.querySelector('.btn-loader');
    if (loading) {
      text.classList.add('hidden');
      loader.classList.remove('hidden');
      button.disabled = true;
    } else {
      text.classList.remove('hidden');
      loader.classList.add('hidden');
      button.disabled = false;
    }
  }

  function createResultCard(label, value, isLink = false) {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.innerHTML = `
      <div class="result-label">${escapeHtml(label)}</div>
      <div class="result-value${isLink ? '' : ''}">${
      isLink
        ? `<a href="#" onclick="return false;" data-url="${escapeHtml(value)}">${escapeHtml(value)}</a>`
        : escapeHtml(String(value))
    }</div>`;
    return card;
  }

  function createBoolCard(label, value) {
    const card = document.createElement('div');
    card.className = 'result-card';
    const boolClass = value ? 'badge-true' : 'badge-false';
    const boolText = value ? 'Yes' : 'No';
    card.innerHTML = `
      <div class="result-label">${escapeHtml(label)}</div>
      <div class="result-value"><span class="${boolClass}">${boolText}</span></div>`;
    return card;
  }

  function createSection(title) {
    const section = document.createElement('div');
    section.className = 'result-section';
    section.textContent = title;
    return section;
  }

  function showError(container, message) {
    container.innerHTML = `<div class="error-msg">${escapeHtml(message)}</div>`;
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // Make links open in external browser
  document.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.dataset.url) {
      e.preventDefault();
      require('electron')?.shell?.openExternal?.(e.target.dataset.url);
    }
  });

  // --- IP Tracker ---

  const ipInput = document.getElementById('ip-input');
  const ipTrackBtn = document.getElementById('ip-track-btn');
  const ipResults = document.getElementById('ip-results');

  ipTrackBtn.addEventListener('click', trackIP);
  ipInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') trackIP();
  });

  async function trackIP() {
    const ip = ipInput.value.trim();
    if (!ip) {
      showError(ipResults, 'Please enter an IP address');
      return;
    }

    setLoading(ipTrackBtn, true);
    ipResults.innerHTML = '<div class="loading-text">Tracking IP address...</div>';

    try {
      const result = await window.ghostAPI.trackIP(ip);

      if (!result.success) {
        showError(ipResults, result.error);
        return;
      }

      const d = result.data;
      ipResults.innerHTML = '';

      // Location section
      ipResults.appendChild(createSection('Location'));
      const locGrid = document.createElement('div');
      locGrid.className = 'result-grid';
      locGrid.appendChild(createResultCard('IP Address', d.ip));
      locGrid.appendChild(createResultCard('Country', `${d.country} (${d.countryCode})`));
      locGrid.appendChild(createResultCard('Region', `${d.region} (${d.regionCode})`));
      locGrid.appendChild(createResultCard('City', d.city));
      locGrid.appendChild(createResultCard('Continent', `${d.continent} (${d.continentCode})`));
      locGrid.appendChild(createResultCard('Zip / Postal', d.zip || 'N/A'));
      locGrid.appendChild(createResultCard('Latitude', String(d.latitude)));
      locGrid.appendChild(createResultCard('Longitude', String(d.longitude)));
      locGrid.appendChild(createResultCard('Google Maps', d.mapsUrl, true));
      ipResults.appendChild(locGrid);

      // Network section
      ipResults.appendChild(createSection('Network'));
      const netGrid = document.createElement('div');
      netGrid.className = 'result-grid';
      netGrid.appendChild(createResultCard('ISP', d.isp));
      netGrid.appendChild(createResultCard('Organization', d.org));
      netGrid.appendChild(createResultCard('AS Number', d.as || 'N/A'));
      netGrid.appendChild(createResultCard('AS Name', d.asName || 'N/A'));
      netGrid.appendChild(createResultCard('Reverse DNS', d.reverse || 'N/A'));
      ipResults.appendChild(netGrid);

      // Timezone section
      ipResults.appendChild(createSection('Timezone & Other'));
      const tzGrid = document.createElement('div');
      tzGrid.className = 'result-grid';
      tzGrid.appendChild(createResultCard('Timezone', d.timezone));
      tzGrid.appendChild(createResultCard('UTC Offset', d.utcOffset));
      tzGrid.appendChild(createResultCard('Currency', d.currency || 'N/A'));

      // Boolean flags
      if (d.isMobile !== undefined) {
        tzGrid.appendChild(createBoolCard('Mobile Connection', d.isMobile));
        tzGrid.appendChild(createBoolCard('Proxy / VPN', d.isProxy));
        tzGrid.appendChild(createBoolCard('Hosting / Datacenter', d.isHosting));
      }

      // Extras from fallback API
      if (d.callingCode) tzGrid.appendChild(createResultCard('Calling Code', d.callingCode));
      if (d.capital) tzGrid.appendChild(createResultCard('Capital', d.capital));
      if (d.flag) tzGrid.appendChild(createResultCard('Flag', d.flag));
      if (d.borders) tzGrid.appendChild(createResultCard('Borders', d.borders));

      ipResults.appendChild(tzGrid);
    } catch (err) {
      showError(ipResults, err.message || 'An unexpected error occurred');
    } finally {
      setLoading(ipTrackBtn, false);
    }
  }

  // --- My IP ---

  const myIpBtn = document.getElementById('myip-btn');
  const myIpResults = document.getElementById('myip-results');

  myIpBtn.addEventListener('click', showMyIP);

  async function showMyIP() {
    setLoading(myIpBtn, true);
    myIpResults.innerHTML = '<div class="loading-text">Discovering your IP address...</div>';

    try {
      const result = await window.ghostAPI.showMyIP();

      if (!result.success) {
        showError(myIpResults, result.error);
        return;
      }

      myIpResults.innerHTML = `
        <div class="my-ip-display">
          <div class="my-ip-value">${escapeHtml(result.ip)}</div>
          <div class="my-ip-label">Your Public IP Address</div>
        </div>`;

      // Auto-track the IP for full details
      const trackResult = await window.ghostAPI.trackIP(result.ip);
      if (trackResult.success) {
        const d = trackResult.data;
        const grid = document.createElement('div');
        grid.className = 'result-grid';
        grid.appendChild(createResultCard('Country', `${d.country} (${d.countryCode})`));
        grid.appendChild(createResultCard('City', d.city));
        grid.appendChild(createResultCard('ISP', d.isp));
        grid.appendChild(createResultCard('Timezone', d.timezone));
        grid.appendChild(createResultCard('Google Maps', d.mapsUrl, true));
        if (d.isMobile !== undefined) {
          grid.appendChild(createBoolCard('VPN / Proxy', d.isProxy));
        }
        myIpResults.appendChild(grid);
      }
    } catch (err) {
      showError(myIpResults, err.message || 'An unexpected error occurred');
    } finally {
      setLoading(myIpBtn, false);
    }
  }

  // --- Phone Tracker ---

  const phoneInput = document.getElementById('phone-input');
  const phoneRegion = document.getElementById('phone-region');
  const phoneTrackBtn = document.getElementById('phone-track-btn');
  const phoneResults = document.getElementById('phone-results');

  phoneTrackBtn.addEventListener('click', trackPhone);
  phoneInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') trackPhone();
  });

  async function trackPhone() {
    const phone = phoneInput.value.trim();
    if (!phone) {
      showError(phoneResults, 'Please enter a phone number');
      return;
    }

    const region = phoneRegion.value;
    setLoading(phoneTrackBtn, true);
    phoneResults.innerHTML = '<div class="loading-text">Analyzing phone number...</div>';

    try {
      const result = await window.ghostAPI.trackPhone(phone, region);

      if (!result.success) {
        showError(phoneResults, result.error);
        return;
      }

      const d = result.data;
      phoneResults.innerHTML = '';

      phoneResults.appendChild(createSection('Phone Number Information'));
      const grid = document.createElement('div');
      grid.className = 'result-grid';
      grid.appendChild(createResultCard('Country', d.country));
      grid.appendChild(createResultCard('Country Code', d.countryCode));
      grid.appendChild(createResultCard('Calling Code', d.callingCode));
      grid.appendChild(createResultCard('National Number', d.nationalNumber));
      grid.appendChild(createResultCard('Type', d.type));
      phoneResults.appendChild(grid);

      phoneResults.appendChild(createSection('Formatted Numbers'));
      const fmtGrid = document.createElement('div');
      fmtGrid.className = 'result-grid';
      fmtGrid.appendChild(createResultCard('International', d.internationalFormat));
      fmtGrid.appendChild(createResultCard('National', d.nationalFormat));
      fmtGrid.appendChild(createResultCard('E.164 Format', d.e164Format));
      fmtGrid.appendChild(createResultCard('URI', d.uri));
      phoneResults.appendChild(fmtGrid);

      phoneResults.appendChild(createSection('Validation'));
      const valGrid = document.createElement('div');
      valGrid.className = 'result-grid';
      valGrid.appendChild(createBoolCard('Valid Number', d.isValid));
      valGrid.appendChild(createBoolCard('Possible Number', d.isPossible));
      phoneResults.appendChild(valGrid);
    } catch (err) {
      showError(phoneResults, err.message || 'An unexpected error occurred');
    } finally {
      setLoading(phoneTrackBtn, false);
    }
  }

  // --- Username Tracker ---

  const usernameInput = document.getElementById('username-input');
  const usernameTrackBtn = document.getElementById('username-track-btn');
  const usernameResults = document.getElementById('username-results');

  usernameTrackBtn.addEventListener('click', trackUsername);
  usernameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') trackUsername();
  });

  async function trackUsername() {
    const username = usernameInput.value.trim();
    if (!username) {
      showError(usernameResults, 'Please enter a username');
      return;
    }

    setLoading(usernameTrackBtn, true);
    usernameResults.innerHTML = `
      <div class="loading-text">Searching for "${escapeHtml(username)}" across platforms...</div>
      <div class="progress-bar"><div class="progress-fill" style="width: 10%"></div></div>`;

    // Animate progress bar
    const progressFill = usernameResults.querySelector('.progress-fill');
    let progress = 10;
    const progressInterval = setInterval(() => {
      if (progress < 90) {
        progress += Math.random() * 15;
        progressFill.style.width = Math.min(progress, 90) + '%';
      }
    }, 500);

    try {
      const result = await window.ghostAPI.trackUsername(username);

      clearInterval(progressInterval);

      if (!result.success) {
        showError(usernameResults, result.error);
        return;
      }

      usernameResults.innerHTML = '';

      // Stats
      const stats = document.createElement('div');
      stats.className = 'username-stats';
      stats.innerHTML = `
        <div class="stat-box">
          <div class="stat-number green">${result.totalFound}</div>
          <div class="stat-label">Found</div>
        </div>
        <div class="stat-box">
          <div class="stat-number red">${result.totalChecked - result.totalFound}</div>
          <div class="stat-label">Not Found</div>
        </div>
        <div class="stat-box">
          <div class="stat-number blue">${result.totalChecked}</div>
          <div class="stat-label">Checked</div>
        </div>`;
      usernameResults.appendChild(stats);

      // Filter tabs
      const filterDiv = document.createElement('div');
      filterDiv.className = 'filter-tabs';
      filterDiv.innerHTML = `
        <button class="filter-tab active" data-filter="all">All (${result.totalChecked})</button>
        <button class="filter-tab" data-filter="found">Found (${result.totalFound})</button>
        <button class="filter-tab" data-filter="not-found">Not Found (${result.totalChecked - result.totalFound})</button>`;
      usernameResults.appendChild(filterDiv);

      // Results list
      const listContainer = document.createElement('div');
      listContainer.className = 'username-list';
      listContainer.id = 'username-list';

      // Found items first
      const allItems = [...result.found, ...result.notFound];

      allItems.forEach((item) => {
        const el = document.createElement('div');
        el.className = `username-item ${item.found ? 'found' : 'not-found'}`;
        el.dataset.filter = item.found ? 'found' : 'not-found';
        el.innerHTML = `
          <span class="platform-name">${escapeHtml(item.name)}</span>
          ${
            item.found
              ? `<a href="#" onclick="return false;" data-url="${escapeHtml(item.url)}">Open</a>`
              : ''
          }
          <span class="platform-status">${item.found ? 'FOUND' : 'N/A'}</span>`;
        listContainer.appendChild(el);
      });

      usernameResults.appendChild(listContainer);

      // Filter functionality
      filterDiv.querySelectorAll('.filter-tab').forEach((tab) => {
        tab.addEventListener('click', () => {
          filterDiv.querySelectorAll('.filter-tab').forEach((t) => t.classList.remove('active'));
          tab.classList.add('active');

          const filter = tab.dataset.filter;
          listContainer.querySelectorAll('.username-item').forEach((item) => {
            if (filter === 'all') {
              item.style.display = '';
            } else {
              item.style.display = item.dataset.filter === filter ? '' : 'none';
            }
          });
        });
      });
    } catch (err) {
      clearInterval(progressInterval);
      showError(usernameResults, err.message || 'An unexpected error occurred');
    } finally {
      setLoading(usernameTrackBtn, false);
    }
  }
});
