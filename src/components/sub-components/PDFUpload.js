import React from 'react';

const PDFUpload = ({ file, onFileChange, nextStep, previousStep }) => {
  const handleFileChange = (e) => {
    if (e.target.files[0].type === 'application/pdf') {
      onFileChange(e.target.files[0]);
    } else {
      alert('Only PDF files are accepted');
    }
  };

  const removeFile = () => {
    onFileChange(null);
  };

  return (
    <div className="text-white p-8">
      <h2 className="text-3xl font-semibold mb-4">Upload Job Description (JD)</h2>
      <div className="mb-4">
        <input
          type="file"
          onChange={handleFileChange}
          className="p-2 rounded bg-slate-700 border border-gray-600 w-full"
        />
      </div>
      {file && (
        <div className="bg-slate-700 p-2 rounded mb-4 flex justify-between items-center">
          <span>{file.name}</span>
          <button
            onClick={removeFile}
            className="text-red-500 hover:text-red-700"
          >
            Remove
          </button>
        </div>
      )}
      <div className="flex justify-between">
        <button
          onClick={previousStep}
          className="p-2 bg-gray-500 rounded hover:bg-gray-600"
        >
          Previous
        </button>
        <button
          onClick={nextStep}
          className="p-2 bg-green-500 rounded hover:bg-green-600"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default PDFUpload;
