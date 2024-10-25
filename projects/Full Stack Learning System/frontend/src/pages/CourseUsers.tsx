/**
 * List all users that are currently enrolled in a specific course
 */

import { useContext, useEffect, useState } from 'react';
import { Layout } from '../components/Layout';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api';
import avatar from '../images/user.png';
import { StoreContext } from '../store';

export const CourseUsers = () => {
  const code = useParams().courseCode;
  const [users, setUsers] = useState<string[]>([]);
	const [searchField, setSearchField] = useState<string>('');
  const { token, isTeacher } = useContext(StoreContext);
	const navigate = useNavigate();

  // When a teacher clicks on a user direct them to the users grades
  const handleClick = (user: object) => {
    if (isTeacher) {
      navigate(`/course/${code}/${user.user_id}/grades`);
    }
  }

  useEffect(() => {
    // Get all users in a course
    const getUsers = async () => {
      const getUsers = await api.get('/course/list', {
        params: {
          'course_code': code,
          'token': token
        }
      })
      .then((res) => res.data);
      setUsers([...getUsers.students, ...getUsers.lecturers]);
    }
    getUsers();
  }, [])



  return (
    <Layout>
      <div className='text-2xl text-left'>
        <p>{code}</p>
      </div>
      <hr className='h-px bg-black'/>
      <div className='flex justify-between items-center'>
        <div className='text-xl text-left'>
          <p>Users</p>
        </div>
        <div>
          <input 
            type='search'
            placeholder='Search Users'
            className='bg-gray-50 border border-black rounded-lg p-2'
            onChange={e => setSearchField(e.target.value)}
          />
        </div>
      </div>
      <div>
        
      </div>
      <table className='text-left w-3/5'>
        <thead className='text-md bg-gray-50'>
          <tr>
            <th className='px-6 py-3'>Name</th>
            <th className='px-6 py-3'>ID</th>
          </tr>
        </thead>
        <tbody>
          {users
            .filter((user) => {
              return (user.user_id.includes(searchField) || user.user_name.toLowerCase().includes(searchField.toLowerCase()));
            })
            .map((user) => {
              return(
                <tr
                  key={user.user_id}
                  className='border hover:bg-slate-200'
                  onClick={() => handleClick(user)}
                >
                  <th className='flex items-center px-6 py-4'>
                    <img className='w-6 h-6 rounded-full' src={avatar} alt='user_avatar' />
                    <div className='pl-3'>
                      <div className='text-base font-semibold'>{user.user_name}</div>
                    </div>
                  </th>
                  <td className='px-6 py-2'>{user.user_id}</td>
                </tr>
              );
            })
          }
        </tbody>
      </table>
    </Layout>
  );
}