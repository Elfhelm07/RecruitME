import React, { useState, useRef } from 'react';

const CriteriaForm = ({ criteriaList = [], onCriteriaChange, nextStep }) => {
  const [criteria, setCriteria] = useState('');

  const addCriteria = () => {
    if (criteria.trim()) {
      onCriteriaChange([...criteriaList, criteria]);
      setCriteria('');
    }
  };

  const removeCriteria = (index) => {
    onCriteriaChange(criteriaList.filter((_, i) => i !== index));
  };

 
  return (
    <div className="text-white p-8 flex flex-col">
      <h2 className="text-3xl font-semibold mb-1">Add Criteria</h2>
      <h2 className="text-lg font-light mb-4">give the criteria a candidate should pass to apply this job</h2>
      <div className="mb-4 flex gap-0 rounded-full bg-slate-600 border-2 border-slate-200 justify-center align-middle items-center">
        <input
          type="text"
          value={criteria}
          onChange={(e) => setCriteria(e.target.value)}
          className="p-2 rounded bg-transparent w-full focus:outline-none placeholder:text-lg text-lg"
          placeholder="Enter criteria"
        />
        <button
        id='criteriaAddBtn'
          onClick={addCriteria}
          className=" w-10 h-10 bg-white text-black text-3xl mr-1 rounded-full hover:bg-black hover:text-white"
        >
          +
        </button>
      </div>
      <div>
        {criteriaList.map((item, index) => (
          <div key={index} className="flex justify-between items-center bg-slate-700 p-2 rounded mb-2">
            <span className="truncate">{item}</span>
            <button
              onClick={() => removeCriteria(index)}
              className="text-red-500 hover:text-red-700"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
      <button
        onClick={nextStep}
        className="mt-4 p-2 py-1 rounded text-lg bg-green-700  hover:bg-green-600 ml-auto"
      >
        Next
      </button>
    </div>
  );
};

export default CriteriaForm;
