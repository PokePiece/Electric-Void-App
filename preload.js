const { contextBridge } = require('electron');
const path = require('path');

let nativeAddon = null;

try {
  // Get the correct path to the native module
  // Matches the build.files entry in package.json
  const addonPath = path.join(__dirname, 'build', 'Release', 'math.node');

  // Try to require the native addon
  nativeAddon = require(addonPath);
  
  console.log("Successfully loaded the native module.");

} catch (error) {
  // If loading fails, log the error and set nativeAddon to null
  console.error("Error loading native module:", error);
  nativeAddon = null;
}

// Expose a new object to the renderer process with added safety checks.
// The name "nativeAddon" now matches the React code.
contextBridge.exposeInMainWorld('nativeAddon', {
  add: (a, b) => {
    if (nativeAddon && typeof nativeAddon.add === 'function') {
      return nativeAddon.add(a, b);
    }
    throw new Error('C++ module function "add" not available.');
  },
  
  factorial: (n) => {
    if (nativeAddon && typeof nativeAddon.factorial === 'function') {
      return nativeAddon.factorial(n);
    }
    throw new Error('C++ module function "factorial" not available.');
  }
});