try {
  const addon = require('./build/Release/addon');
  console.log('Module loaded successfully');
  console.log('2 + 3 =', addon.add(2, 3));
  console.log('5! =', addon.factorial(5));
} catch (error) {
  console.error('Failed to load module:', error.message);
  console.error('Full error:', error);
}