const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('ghostAPI', {
  // Window controls
  minimize: () => ipcRenderer.send('window-minimize'),
  maximize: () => ipcRenderer.send('window-maximize'),
  close: () => ipcRenderer.send('window-close'),

  // IP Tracker
  trackIP: (ip) => ipcRenderer.invoke('track-ip', ip),
  showMyIP: () => ipcRenderer.invoke('show-my-ip'),

  // Phone Number Tracker
  trackPhone: (phone, region) => ipcRenderer.invoke('track-phone', phone, region),

  // Username Tracker
  trackUsername: (username) => ipcRenderer.invoke('track-username', username),
});
