import React from "react";
import { Link } from "react-router-dom";

interface ChildProps {
  code: string | undefined,
  userId: string | null
}

export const CourseTabs: React.FC<ChildProps> = ({ code, userId }) => {
  return (
    <div className='flex justify-between w-1/4'>
      <div className='hover:bg-slate-200 rounded p-2 w-full'>
        <Link className='text-black hover:text-black' to={`/course/${code}/users`}>Users</Link>
      </div>
      <div className='hover:bg-slate-200 rounded p-2 w-full'>
        <Link className='text-black hover:text-black' to={`/course/${code}/forums`}>Forum</Link>
      </div>
      <div className='hover:bg-slate-200 rounded p-2 w-full'>
        <Link className='text-black hover:text-black' to={`/course/${code}/quizzes`}>Quizzes</Link>
      </div>
      <div className='hover:bg-slate-200 rounded p-2 w-full'>
        <Link className='text-black hover:text-black' to={`/course/${code}/class`}>Class</Link>
      </div>
      <div className='hover:bg-slate-200 rounded p-2 w-full'>
        <Link className='text-black hover:text-black' to={`/course/${code}/${userId}/grades`}>Grades</Link>
      </div>
      <div className='hover:bg-slate-200 rounded p-2 w-full'>
        <Link className='text-black hover:text-black' to={`/course/${code}/assessments`}>Assessment</Link>
      </div>
    </div>
  );
}