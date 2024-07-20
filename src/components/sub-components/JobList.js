import React, { useState, useEffect } from 'react';

const jobs = [
  { title: 'Frontend Developer', company: 'Tech Corp', salary: 60000 },
  { title: 'Backend Developer', company: 'Innovate Ltd', salary: 70000 },
  { title: 'Full Stack Developer', company: 'Web Solutions', salary: 80000 },
  // Add more jobs here
];

const JobList = ({ onJobSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [minPackage, setMinPackage] = useState(0);
  const [sortOrder, setSortOrder] = useState('asc');
  const [filteredJobs, setFilteredJobs] = useState(jobs);

  useEffect(() => {
    let result = jobs
      .filter(job => job.title.toLowerCase().includes(searchTerm.toLowerCase()) && job.salary >= minPackage)
      .sort((a, b) => sortOrder === 'asc' ? a.salary - b.salary : b.salary - a.salary);
    setFilteredJobs(result);
  }, [searchTerm, minPackage, sortOrder]);

  return (
    <div>
      <div className="flex space-x-4 mb-4">
        <input
          type="text"
          placeholder="Search"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-1/3 p-2 bg-slate-700 text-white rounded"
        />
        <input
          type="number"
          placeholder="Min Package"
          value={minPackage}
          onChange={(e) => setMinPackage(Number(e.target.value))}
          className="w-1/3 p-2 bg-slate-700 text-white rounded"
        />
        <button
          onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
          className="w-1/3 p-2 bg-slate-700 text-white rounded"
        >
          Sort by Salary ({sortOrder === 'asc' ? 'Ascending' : 'Descending'})
        </button>
      </div>
      {filteredJobs.map((job, index) => (
        <div
          key={index}
          className="p-4 mb-4 bg- border-b-2 border-slate-200  cursor-pointer transition-opacity duration-500 flex justify-between"
          // style={{
          //   opacity: 1 - (index / (filteredJobs.length - 1)) * 0.5,
          // }}
          onClick={() => onJobSelect(job)}
        > 
        <div>

          <h2 className="text-xl font-bold">{job.title}</h2>
          <p>{job.company} - {job.role}</p>
          <p>Expected Salary: ${job.salary}</p>
          </div>
          <button className="mt-2 p-2 bg-blue-500 rounded h-min self-center">Apply</button>
        </div>
      ))}
    </div>
  );
};

export default JobList;
