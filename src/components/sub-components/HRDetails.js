import React from 'react';

const HRDetails = ({ details, onDetailsChange, previousStep, onSubmit }) => {
  const handleChange = (e) => {
    onDetailsChange({
      ...details,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="text-white p-8">
      <h2 className="text-3xl font-semibold mb-4">Company and HR Details</h2>
      <form onSubmit={onSubmit} className="space-y-4">
        <input
          type="text"
          name="companyName"
          value={details.companyName}
          onChange={handleChange}
          className="p-2 rounded bg-slate-700 border border-gray-600 w-full"
          placeholder="Company Name"
          required
        />
        <input
          type="text"
          name="jobPosition"
          value={details.jobPosition}
          onChange={handleChange}
          className="p-2 rounded bg-slate-700 border border-gray-600 w-full"
          placeholder="Job Position"
          required
        />
        <input
          type="text"
          name="expectedCTC"
          value={details.expectedCTC}
          onChange={handleChange}
          className="p-2 rounded bg-slate-700 border border-gray-600 w-full"
          placeholder="Expected CTC"
          required
        />
        <input
          type="email"
          name="email"
          value={details.email}
          onChange={handleChange}
          className="p-2 rounded bg-slate-700 border border-gray-600 w-full"
          placeholder="Email"
          required
        />
        <input
          type="date"
          name="lastDate"
          value={details.lastDate}
          onChange={handleChange}
          className="p-2 rounded bg-slate-700 border border-gray-600 w-full"
          required
        />
        <div className="flex justify-between">
          <button
            type="button"
            onClick={previousStep}
            className="p-2 bg-gray-500 rounded hover:bg-gray-600"
          >
            Previous
          </button>
          <button
            type="submit"
            className="p-2 bg-green-500 rounded hover:bg-green-600"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

export default HRDetails;
