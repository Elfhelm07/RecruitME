import React, { useState } from 'react';
import JobList from './sub-components/JobList';
// import JobApply from './components/JobApply';
import ResumeUpload from './sub-components/ResumeUpload';
import UserDetails from './sub-components/UserDetails';
import Undertaking from './sub-components/Undertaking';
import axios from 'axios';

const Apply = () => {
  const [step, setStep] = useState(1);
  const [selectedJob, setSelectedJob] = useState(null);
  const [resume, setResume] = useState(null);
  const [userDetails, setUserDetails] = useState({ name: '', email: '', contact: '' });

  const handleYesClick = () => {
    window.open('http://localhost:3000/test', '_blank');
  };

  const handleJobSelect = (job) => {
    setSelectedJob(job);
    setStep(2);
  };

  const handleResumeUpload = (file) => {
    setResume(file);
  };

  const handleUserDetailsChange = (details) => {
    setUserDetails(details);
  };

  async function handlesubmit(e){
    e.preventDefault();
  const formData = new FormData();
  formData.append('name', userDetails.name);
  formData.append('phone', userDetails.contact);
  formData.append('email', userDetails.email);
  formData.append('resume', resume);
  document.getElementById("submitbtn").innerHTML="Wait..."
    try {
      const response = await fetch('http://localhost:5000/upload_resume', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      // console.log(result)
      const score = result.score;
      await axios.get(`https://urldb-backend.vercel.app/1/m1716299394158/add_data/recruiteme/userdata?name=${userDetails.name}&email=${userDetails.email}&contact=${userDetails.contact}&score=${score}&job=${selectedJob.title}`).then((res)=>{
        console.log(res);
      })
      document.getElementById("redirect-msg").style.display="flex";



    } catch (error) {
      console.error('Error:', error);
    }
  }

  return (
    <>
     <div id='redirect-msg' className="hidden fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center">
      <div className=" bg-white p-8 rounded-lg shadow-lg text-center">
        <h2 className="text-2xl font-semibold mb-4">Take a Personalized Test</h2>
        <p className="mb-6">
          This test can improve your chances of selection and shortlisting, so attempt it very seriously.
          All the responses are recorded.
        </p>
        <div className="flex justify-center space-x-4">
          <button
            onClick={handleYesClick}
            className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700"
          >
            Yes
          </button>
          <button
            onClick={() => alert('No clicked')}
            className="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-700"
          >
            No
          </button>
        </div>
      </div>
    </div>
    <div className="min-h-screen bg-slate-800 text-white font-roboto">
      <h1 className="text-4xl text-center py-6">Apply to job</h1>
      <div className="max-w-4xl mx-auto p-4">
        {step === 1 && <JobList onJobSelect={handleJobSelect} />}
        {step === 2 && (
          <Undertaking
            job={selectedJob}
            onNext={()=>setStep(3)}
          />
        )}
        {step === 3 && (
          <ResumeUpload
            resume={resume}
            onResumeUpload={handleResumeUpload}
            onNext={() => setStep(4)}
          />
        )}
        {step === 4 && (
          <UserDetails
            userDetails={userDetails}
            onUserDetailsChange={handleUserDetailsChange}
            onSubmit={(e)=>handlesubmit(e)}
          />
        )}
      </div>
    </div>
    </>
  );
};

export default Apply;
