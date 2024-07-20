// src/components/Sidebar.js
import React from 'react';

const Sidebar = () => {
  return (
    <aside className="w-64 bg-white p-4 border-r border-gray-200">
      <div className="text-center">
        <img src="https://img.icons8.com/?size=100&id=7819&format=png&color=000000" alt="Profile" className="w-24 h-24 mx-auto rounded-full" />
        <h2 className="mt-4 text-xl font-semibold text-slate-800">HR Name</h2>
        <p className="text-slate-800">Company Name</p>
        <p className="text-slate-800">email@company.com</p>
      </div>
      <nav className="mt-6 flex flex-col gap-2">
        <a href="#" className="block py-2 px-4 text-slate-800 hover:bg-slate-100 rounded text-lg border-b-2">Profile</a>
        <a href="#" className="block py-2 px-4 text-slate-800 hover:bg-slate-100 rounded text-lg border-b-2">Dashboard</a>
        <a href="#" className="block py-2 px-4 text-slate-800 hover:bg-slate-100 rounded text-lg border-b-2">Add Position</a>
        <a href="#" className="block py-2 px-4 text-slate-800 hover:bg-slate-100 rounded text-lg border-b-2">Notification</a>
        <a href="#" className="block py-2 px-4 text-slate-800 hover:bg-slate-100 rounded text-lg border-b-2">Events</a>
      </nav>
    </aside>
  );
};

export default Sidebar;
