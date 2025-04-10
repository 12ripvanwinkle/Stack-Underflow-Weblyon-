


require('electron-reload')(__dirname, {
    electron: require(`${__dirname}/node_modules/electron`)
  });
  
const { app, BrowserWindow, ipcMain } = require('electron');

app.whenReady().then(() => {

    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    mainWindow.loadFile('index.html');

    ipcMain.on('redirect', (event, targetPage) => {
        mainWindow.loadFile(targetPage);
      });

      win.webContents.openDevTools();


});
