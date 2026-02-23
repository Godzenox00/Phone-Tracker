const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

// Modules
const ipTracker = require('./src/ip-tracker');
const phoneTracker = require('./src/phone-tracker');
const usernameTracker = require('./src/username-tracker');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 750,
    minWidth: 900,
    minHeight: 600,
    title: 'GhostTrack v3.0',
    icon: path.join(__dirname, 'assets', 'icon.png'),
    frame: false,
    transparent: false,
    backgroundColor: '#0a0a0f',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// --- IPC Handlers ---

// Window controls
ipcMain.on('window-minimize', () => {
  mainWindow?.minimize();
});

ipcMain.on('window-maximize', () => {
  if (mainWindow?.isMaximized()) {
    mainWindow.unmaximize();
  } else {
    mainWindow?.maximize();
  }
});

ipcMain.on('window-close', () => {
  mainWindow?.close();
});

// IP Tracker
ipcMain.handle('track-ip', async (_event, ip) => {
  return await ipTracker.trackIP(ip);
});

// Show My IP
ipcMain.handle('show-my-ip', async () => {
  return await ipTracker.getMyIP();
});

// Phone Number Tracker
ipcMain.handle('track-phone', async (_event, phoneNumber, regionCode) => {
  return phoneTracker.trackPhone(phoneNumber, regionCode);
});

// Username Tracker
ipcMain.handle('track-username', async (_event, username) => {
  return await usernameTracker.trackUsername(username);
});
