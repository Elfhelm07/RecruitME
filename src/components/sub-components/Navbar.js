// src/components/Navbar.js
import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-white border-b border-gray-200 px-4 py-2 flex justify-between items-center">
      <div className="flex items-center">
        <img src="/path-to-logo.png" alt="Logo" className="h-10" />
        <div className="ml-6 space-x-4">
          <button className="text-slate-800">Home</button>
          <button className="text-slate-800">About</button>
          <button className="text-slate-800">Services</button>
        </div>
      </div>
      <button className="text-slate-800">Logout</button>
    </nav>
  );
};

export default Navbar;
