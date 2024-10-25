/**
 * Display course information on a card which contains the name, course code and earliest assessment due date
 */

import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { api } from '../api';
import { StoreContext } from '../store';
import { Assessments } from '../types';

export const CourseCard = ({ name, code }: CourseType) => {
  const navigate = useNavigate();
  
  const handleClick = (event: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => {
    navigate(`/course/${event.currentTarget.id}`);
  }

  const { token } = useContext(StoreContext);
  const [assessments, setAssessments] = useState<Assessments[]>([]);
  useEffect(() => {
    // Fetch a list of the earliest assessment due dates for each course that the student is in
    const fetchAssessments = async () => {
      const userAssessments = await api.get('/open/assessments', {
        params: {
          'token': token
        }
      })
        .then((res) => res.data);
      setAssessments(userAssessments);
    }
    fetchAssessments();
  },[])

  return (
    <a id={code} className='hover:cursor-pointer w-min text-black hover:text-black hover:shadow-lg' onClick={handleClick}>
      <div className='flex flex-col bg-yellow-100 rounded-md w-56 h-56'>
          <div className='flex-2 mt-3'>
            <p>{code} - {name}</p>
          </div>
          <hr className='h-px bg-black'/>
          <div className='flex-1 p-2'>
            {assessments && 
              assessments.map((ass, idx) => {
                if (ass.course === code) {
                  return (
                    <p key={idx}>{ass.asstName} - {ass.due_date.slice(0,12)}</p>
                  );
                }
              })
            }
          </div>
      </div>
    </a>
  );
}

type CourseType = {
  name: string,
  code: string,
}