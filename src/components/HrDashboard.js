// src/components/MainContent.js
import React from 'react';
import Navbar from './sub-components/Navbar';
import Sidebar from './sub-components/Sidebar';
import WelcomeDash from './sub-components/WelcomeDash';
import Apply from './Apply';
import AddPosition from './UploadPage';
const HrDashboard = () => {
  return (
    <>
    <div className="min-h-screen flex flex-col overflow-y-hidden">
      <Navbar />
      <div className="flex w-full">
        <Sidebar />
        <AddPosition/>
        {/* <WelcomeDash/> */}
              </div>
    </div>
    
    </>
  );
};

export default HrDashboard;
