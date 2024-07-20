import React from 'react';
import axios from 'axios';
import FormData from 'form-data';
// import fs from 'fs'; 

const ResumeUpload = ({ resume, onResumeUpload, onNext }) => {
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    onResumeUpload(file);

    const data = new FormData();
    data.append('file', file);
    data.append(
      'queries',
      'tagged,image_only,title,subject,author,producer,creator,creation_date,modified_date,keywords,doc_language,page_count,contains_annotations,contains_signature,pdf_version,file_size,filename,restrict_permissions_set,contains_xfa,contains_acroforms,contains_javascript,contains_transparency,contains_embedded_file,uses_embedded_fonts,uses_nonembedded_fonts,pdfa,requires_password_to_open'
    );

    // Define configuration options for axios request
    const config = {
      method: 'post',
      maxBodyLength: Infinity, // Set maximum length of the request body
      url: 'https://api.pdfrest.com/pdf-info',
      headers: {
        'Api-Key': '49f3ce3f-8f67-405d-bbfa-0bd64084517a', // Replace with your API key
        'Content-Type': 'multipart/form-data',
      },
      data: data, // Set the data to be sent with the request
    };
    try {
      const response = await axios(config);
      console.log(JSON.stringify(response.data));
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  }
  return (
    <div className="p-4 bg-slate-700 rounded">
      <h2 className="text-xl font-bold mb-4">Upload Resume</h2>
      <input type="file" accept=".pdf" onChange={handleFileChange} className="block mb-4" />
      {resume && (
        <div className="mb-4">
          <p>Selected File: {resume.name}</p>
          <button onClick={() => onResumeUpload(null)} className="p-2 bg-red-500 rounded">Remove</button>
        </div>
      )}
      <button onClick={onNext} className="p-2 bg-green-500 rounded">Next</button>
    </div>
  );
};

export default ResumeUpload;

