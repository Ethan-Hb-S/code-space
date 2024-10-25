/**
 * Pop up modal which allows students to join a course on the dashboard
 */

import React, { ChangeEvent, useContext, useState } from 'react';
import { api } from '../api';
import { StoreContext } from '../store';

interface ChildProps {
  setOpenModal: (value: boolean) => void;
  toggleUpdate: () => void;
}

export const JoinClassModal: React.FC<ChildProps> = ({ setOpenModal, toggleUpdate }) => {
  const { token } = useContext(StoreContext);
  const [course, setCourse] = useState({'token': token});
  const handleJoin = () => {
    api.post('/course/join', course)
    setOpenModal(false);
    toggleUpdate();
  }
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    let {value, name} = event.target;
    setCourse({ ...course, [name]: value.toUpperCase() });
  }
  return (
    <div className='fixed inset-0 flex items-center justify-center z-50'>
      <div className='fixed inset-0 bg-gray-500 opacity-50'></div>
      <div className='flex flex-col bg-white p-4 rounded-lg shadow-lg relative h-56 w-1/4'>
        <div className='flex align-center justify-between'>
          <h2 className='text-gray-800 text-2xl font-bold'>Enter the course code:</h2>
          <button type='button' className='text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg p-1.5 dark:hover:bg-gray-800' onClick={() => setOpenModal(false)}>
            <span>&times;</span>
          </button>
        </div>
        <div className='flex flex-col justify-center h-screen'>
          <input
            type='text'
            placeholder='Enter code'
            name='course_code'
            onChange={handleChange}
            className='border border-black p-1 rounded'
          />
        </div>
        <div>
          <button className='bg-blue-500 text-white border border-black rounded px-2' onClick={handleJoin}>Join</button>
        </div>
      </div>
    </div>  
  );
}