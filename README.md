# GhostTrack

OSINT & Information Gathering tool with a modern Electron desktop GUI.

<img src="https://github.com/HunxByts/GhostTrack/blob/main/asset/bn.png"/>

## Version 3.0 - Electron GUI Edition

### What's New

- **Modern Desktop GUI** - Dark-themed Electron interface with sidebar navigation
- **Better IP Tracking** - Dual API fallback (ip-api.com + ipwho.is), proxy/VPN detection, hosting detection
- **Improved Phone Analysis** - Google's libphonenumber (same library used by Android), more formats and validation
- **Expanded Username Search** - 35+ platforms searched concurrently (was 23), with filtering and status indicators
- **My IP Auto-Analysis** - Reveals your IP and automatically shows full geolocation details
- **Portable EXE** - One-click build script to create a standalone Windows executable
- **Custom Window** - Frameless dark window with custom controls

### Features

| Feature | Description |
|---------|-------------|
| IP Tracker | Geolocate any IP with country, city, ISP, proxy/VPN detection, and Google Maps link |
| My IP | Discover your public IP with auto-geolocation |
| Phone Tracker | Analyze phone numbers - carrier, type, country, multiple format outputs |
| Username Tracker | Search 35+ social platforms concurrently with found/not-found filtering |

## Installation & Usage

### Electron GUI (Recommended)

**Prerequisites:** [Node.js 18+](https://nodejs.org)

```bash
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack/electron-app
npm install
npm start
```

### Build Portable EXE (Windows)

Double-click `build-exe.bat` in the project root, or run:

```bash
cd electron-app
npm install
npm run build
```

The portable `.exe` will be in the `dist/` folder.

### Legacy CLI (Python)

The original Python CLI is still available:

```bash
pip3 install -r requirements.txt
python3 GhostTR.py
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Desktop Framework | Electron 33 |
| IP Geolocation | ip-api.com (primary) + ipwho.is (fallback) |
| Phone Parsing | libphonenumber-js (Google's library) |
| HTTP Client | Axios |
| Build Tool | electron-builder |
| UI | Custom HTML/CSS dark theme |

### Installation on Linux (deb)
```
sudo apt-get install git nodejs npm
```

### Installation on Termux
```
pkg install git nodejs
```

## Project Structure

```
GhostTrack/
├── electron-app/          # Electron desktop application
│   ├── main.js            # Main process (window, IPC handlers)
│   ├── preload.js         # Secure bridge between main & renderer
│   ├── package.json       # Dependencies & build config
│   ├── src/               # Backend modules
│   │   ├── ip-tracker.js      # IP geolocation (dual API)
│   │   ├── phone-tracker.js   # Phone number analysis
│   │   └── username-tracker.js # Username OSINT (35+ platforms)
│   └── renderer/          # Frontend
│       ├── index.html     # GUI layout
│       ├── styles.css     # Dark theme styles
│       └── renderer.js    # UI logic & event handling
├── GhostTR.py             # Legacy Python CLI
├── build-exe.bat          # Windows EXE build script
├── requirements.txt       # Python dependencies (legacy)
└── asset/                 # Images & branding
```

<details>
<summary>:zap: Author :</summary>
- <strong><a href="https://github.com/HunxByts">HunxByts</a></strong>
</details>
