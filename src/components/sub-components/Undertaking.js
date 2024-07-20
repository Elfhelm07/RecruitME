import React from 'react'

const Undertaking = ({job,onNext}) => {

  return (
    <div className='w-100vw h-100vh bg-slate-800'>
        <h1 className='text-2xl font-mono text-center'>Read Prerequisites / Criteria</h1>
        <ul className='mt-10 flex flex-col gap-1'>
            <li className=' list-disc text-xl font-light'>You Posses 75% or more in your 12th and 10th agregate</li>
            <li className=' list-disc text-xl font-light'>You are not having any backlogs in any semester</li>
            <li className=' list-disc text-xl font-light'>You have atleast 6 sgpa in each of the semesters</li>
            <li className=' list-disc text-xl font-light'>you have a total cgpa of minimum 7.5</li>
        </ul>
        <div class="flex items-center mb-4 mt-10">
    <input id="default-checkbox" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded  focus:ring-blue-600 ring-offset-gray-800 focus:ring-2 "/>
    <label for="default-checkbox" class="ms-2 text-lg font-medium text-gray-300">I have read and i am eligible for the job</label>
    <button onClick={onNext} className='self-end ml-auto bg-white rounded px-2 py-1 text-xl text-black hover:bg-black hover:text-white' >Continue</button>
</div>
    </div>
  )
}

export default Undertaking