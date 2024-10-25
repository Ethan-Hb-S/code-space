/**
 * Allow teachers to create new courses for students to join
 */

import { ChangeEvent, useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout } from '../components/Layout';
import { api } from '../api.tsx';
import { StoreContext } from '../store.tsx';
export const CreateCourse = () => {
  const navigate = useNavigate();

  const { token } = useContext(StoreContext);

  const [courseData, setCourseData] = useState({ 'token': token });

  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { value, name } = event.target;
    setCourseData({ ...courseData, [name]: value });
  }

  // Create the course and store it in the database
  const handleSubmit = () => {
    console.log(courseData);
    try {
      api.post('/create/course', courseData);
    } catch (err) {
      if (err instanceof Error) {
        console.log(err.message);
      }
    }
    navigate('/');
  }

  return (
    <Layout>
      <div className='flex flex-col'>
        <div>
          <h1 className='text-left'>Course details</h1>
          <hr className='h-px bg-black'/>
          {/* Form */}
          <form className='flex mt-5'>
            <div className='flex flex-col gap-4 w-full'>

              {/* Course name */}
              <div className='flex w-1/2 items-center'>
                <label className='mr-2 flex-1 text-left'>Course Name:</label>
                <input
                  type='text'
                  className='flex-4 bg-gray-50 border border-black rounded-lg p-1'
                  name='name'
                  id='courseName'
                  onChange={handleChange}
                />
              </div>

              {/* Course Code */}
              <div className='flex w-1/2 items-center'>
                <label className='mr-2 flex-1 text-left'>Course Code:</label>
                <input
                  type='text'
                  className='flex-4 bg-gray-50 border border-black rounded-lg p-1'
                  name='code'
                  id='courseCode'
                  onChange={handleChange}
                />
              </div>

              {/* Course Description */}
              <div className='flex w-1/2'>
                <label className='mr-2 flex-1 text-left'>Description:</label>
                <textarea
                  id='description'
                  name='description'
                  className='flex-4 bg-gray-50 border border-black rounded-lg p-1'
                  onChange={handleChange}
                />
              </div>

              {/* Submit button */}
              <div className='flex justify-center gap-5'>
                <button
                  className='border border-black bg-blue-500 text-white rounded p-2'
                  onClick={handleSubmit}
                  name='publish'
                >
                  Publish
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
};