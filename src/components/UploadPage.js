
import CriteriaForm from './sub-components/CriteriaForm';
import PDFUpload from './sub-components/PDFUpload';
import HRDetails from './sub-components/HRDetails';
import React, { useState } from 'react';

const AddPosition = () => {
  const [step, setStep] = useState(1);
  const [criteriaList, setCriteriaList] = useState([]); // Initialize as an array
  const [file, setFile] = useState(null);
  const [details, setDetails] = useState({
    companyName: '',
    jobPosition: '',
    expectedCTC: '',
    email: '',
    lastDate: ''
  });

  const nextStep = () => setStep(step + 1);
  const previousStep = () => setStep(step - 1);

  const handleCriteriaChange = (newCriteriaList) => {
    setCriteriaList(newCriteriaList);
  };

  const handleFileChange = (file) => {
    setFile(file);
  };

  const handleDetailsChange = (updatedDetails) => {
    setDetails(updatedDetails);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = {
      criteriaList,
      file,
      details
    };
    console.log(formData);
    // send formData to the backend
  };

  return (
    <div className="bg-slate-800 min-h-screen flex items-center justify-center w-full">
      <div className="bg-slate-900 p-8 rounded shadow-lg w-3/4">
        <h1 className="text-4xl text-center font-bold text-white mb-8">Create Candidate Form</h1>
        {step === 1 && (
          <CriteriaForm
            criteriaList={criteriaList}
            onCriteriaChange={handleCriteriaChange}
            nextStep={nextStep}
          />
        )}
        {step === 2 && (
          <PDFUpload
            file={file}
            onFileChange={handleFileChange}
            nextStep={nextStep}
            previousStep={previousStep}
          />
        )}
        {step === 3 && (
          <HRDetails
            details={details}
            onDetailsChange={handleDetailsChange}
            previousStep={previousStep}
            onSubmit={handleSubmit}
          />
        )}
      </div>
    </div>
  );
};

export default AddPosition;
