/**
 * Display all all the courses which the user is enrolled in or teachers
 */

import { useEffect, useState, useContext } from 'react';
import { StoreContext } from '../store';
import { Layout } from '../components/Layout';
import { CourseCard } from '../components/CourseCard';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import { JoinClassModal } from '../components/JoinClassModal';
import { CourseItems } from '../types';
import { Chatbot } from '../components/Chatbot';

export const Dashboard = () => {
  const [openModal, setOpenModal] = useState<boolean>(false);
  const navigate = useNavigate();
  const [userCourses, setUserCourses] = useState<CourseItems[]>([]);
  const [searchField, setSearchField] = useState<String>("");
  const [updateDashboard, setUpdateDashboard] = useState<Boolean>(false);

  const { token, isTeacher } = useContext(StoreContext);

  useEffect(() => {
    // Get all courses which user is enrolled in
    const getCourses = async () => {
      try {
        const courses = await api.get('/user/courses', {
          params: {
            'token': token
          }
        })
        .then((res) => res.data);

        if (isTeacher) {
          setUserCourses(courses.teaches);
        } else {
          setUserCourses(courses.student_of);
        }
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message);
        }
      }
    };
    getCourses();
  }, [updateDashboard]);

  const handleClick = () => {
    if (isTeacher) {
      navigate('/create-course');
    } else {
      setOpenModal(true);
    }
  };

  const toggleUpdate = () => {
    setUpdateDashboard(!updateDashboard);
  }

  return (
    <Layout>
      {/* Dashboard */}
      <div className='dashboard flex flex-col flex-1'>
        <div className='heading flex pb-1 justify-between item-center'>
          <h1 className='text-2xl'>Dashboard</h1>
          {/* Search bar */}
          <div className='flex items-center relative'>
            <input 
              type='text'
              placeholder='Search Courses'
              className='bg-gray-50 border border-black rounded-lg p-2'
              onChange={e => setSearchField(e.target.value)}
            />
          </div>
        </div>

        <hr className='h-px bg-black'/>

        {/* Create Course */}
        <div className='flex justify-end'>
          <button
            className='
              bg-transparent
              hover:bg-slate-100
              text-black-700
              border
              border-black
              hover:border-transparent
              rounded
              h-10
              mt-3
              text-center
              p-2'
            onClick={handleClick}
          >
            {isTeacher ? 'Create Course' : 'Join Course'}
          </button>
        </div>
        {openModal &&
          <JoinClassModal setOpenModal={setOpenModal} toggleUpdate={toggleUpdate}/>
        }
        <div className='flex flex-wrap gap-10'>
          {userCourses &&
            userCourses
            .filter((courses) => {
              return (courses.code.toLowerCase().includes(searchField.toLowerCase()));
            })
            .map((courses, id) => {
              return <CourseCard key={id} name={courses.name} code={courses.code}/>
            })
          }
        </div>
      </div>
      <Chatbot />
    </Layout>
  );
};