import React from 'react';

const UserDetails = ({ userDetails, onUserDetailsChange, onSubmit }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    onUserDetailsChange({ ...userDetails, [name]: value });
  };

  return (
    <div className="p-4 bg-slate-700 rounded">
      <h2 className="text-xl font-bold mb-4">User Details</h2>
      <input
        type="text"
        name="name"
        placeholder="Name"
        value={userDetails.name}
        onChange={handleChange}
        className="block mb-4 p-2 bg-slate-600 rounded w-full"
      />
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={userDetails.email}
        onChange={handleChange}
        className="block mb-4 p-2 bg-slate-600 rounded w-full"
      />
      <input
        type="text"
        name="contact"
        placeholder="Contact Number"
        value={userDetails.contact}
        onChange={handleChange}
        className="block mb-4 p-2 bg-slate-600 rounded w-full"
      />
      <button id='submitbtn' onClick={onSubmit} className="p-2 bg-green-500 rounded">Submit</button>
    </div>
  );
};

export default UserDetails;
