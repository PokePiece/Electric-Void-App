// This code is a complete, self-contained React application
// designed to work within an Electron renderer process using Vite.
// It uses Tailwind CSS for styling.

import React, { useState } from 'react';

// Type definition for the native addon
declare global {
  interface Window {
    nativeAddon: {
      add: (a: number, b: number) => number;
      factorial: (n: number) => number;
    };
  }
}

export default function App() {
  const [num1, setNum1] = useState(5);
  const [num2, setNum2] = useState(3);
  const [addResult, setAddResult] = useState('');

  const [factNum, setFactNum] = useState(5);
  const [factResult, setFactResult] = useState('');

  const handleAdd = () => {
    // Check if the native module is available on the window object.
    if (window.nativeAddon) {
      try {
        const result = window.nativeAddon.add(num1, num2);
        setAddResult(`Result: ${result}`);
      } catch (error) {
        //setAddResult(`Error: ${error.message}`);
      }
    } else {
      setAddResult('Error: C++ module not available.');
    }
  };

  const handleFactorial = () => {
    if (window.nativeAddon) {
      try {
        const result = window.nativeAddon.factorial(factNum);
        setFactResult(`${factNum}! = ${result}`);
      } catch (error) {
        //setFactResult(`Error: ${error.message}`);
      }
    } else {
      setFactResult('Error: C++ module not available.');
    }
  };

  return (
    <div className="font-sans m-12">
      <h1 className="text-3xl font-bold mb-4">Math</h1>

      <hr className="my-6" />

      <h2 className="text-2xl font-semibold mb-2">Addition</h2>
      <div className="flex items-center mb-4">
        <input
          type="number"
          value={num1}
          onChange={(e) => setNum1(parseFloat(e.target.value))}
          className="border border-gray-300 p-2 rounded-md w-24"
        />
        <span className="mx-2 text-xl font-bold">+</span>
        <input
          type="number"
          value={num2}
          onChange={(e) => setNum2(parseFloat(e.target.value))}
          className="border border-gray-300 p-2 rounded-md w-24"
        />
        <button onClick={handleAdd} className="ml-4 bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors">
          Calculate
        </button>
      </div>
      <div className="bg-gray-100 p-4 my-2 rounded-md text-gray-800">
        {addResult}
      </div>

      <hr className="my-6" />

      <h2 className="text-2xl font-semibold mb-2">Factorial</h2>
      <div className="flex items-center mb-4">
        <input
          type="number"
          value={factNum}
          onChange={(e) => setFactNum(parseInt(e.target.value))}
          className="border border-gray-300 p-2 rounded-md w-24"
        />
        <button onClick={handleFactorial} className="ml-4 bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors">
          Calculate Factorial
        </button>
      </div>
      <div className="bg-gray-100 p-4 my-2 rounded-md text-gray-800">
        {factResult}
      </div>
    </div>
  );
}
