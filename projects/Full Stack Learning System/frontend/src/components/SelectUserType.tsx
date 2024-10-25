import { useContext, useState } from 'react';
import { api } from '../api';
import { TokenContextType } from '../types';
import { StoreContext } from '../store';

type SelectUserTypeProps = {
  token: string
}

export const SelectUserType = ({ token }: SelectUserTypeProps) => {
  const [userType, setUserType] = useState<String>('');
  const tokenContext: TokenContextType = useContext(StoreContext);
  const [nextDisabled, setNextDisabled] = useState<boolean>(true);

  const handleSelectUserType = (userType: string) => {
    setUserType(userType);
    setNextDisabled(false);
  }

  const handleClickNext = () => {
    if (userType === 'teacher') {
      api.post('/user/add_lecturer', {'token': token});
      tokenContext.setIsTeacher(true);
    } else {
      api.post('/user/add_student', {'token': token});
      tokenContext.setIsTeacher(false);
    }
    tokenContext.setToken(token);
  }

  return (
    <div className='flex flex-col gap-10 m-10'>
      <div className='text-2xl'>
        <p>Are you a</p>
      </div>
      <div className='flex text-2xl gap-5'>
        <button onClick={() => handleSelectUserType('teacher')}>
          <div className={`rounded-lg p-5 ${userType === 'teacher' ? 'grow border border-slate-400 bg-blue-500' : 'grow border border-slate-400'}`}>
            Teacher
          </div>
        </button>
        <button onClick={() => handleSelectUserType('student')}>
          <div className={`rounded-lg p-5 ${userType === 'student' ? 'grow border border-slate-400 bg-blue-500' : 'grow border border-slate-400'}`}>
            Student
          </div>
        </button>
      </div>
      <div>
        <button
          className={`border rounded-md border-slate-400 w-1/2 ${ nextDisabled ? 'bg-slate-300' : 'hover:bg-slate-100' }`}
          disabled={nextDisabled}
          onClick={handleClickNext}
        >
          next
        </button>
      </div>
    </div>
  );
}