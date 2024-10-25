/**
 * Display the users grades
 */

import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { api } from "../api";
import { ChangeEvent, useContext, useEffect, useState } from "react";
import { StoreContext } from "../store";

export const UserGrades = () => {
  const { courseCode, userId } = useParams();
  const [users, setUsers] = useState<object>({});
  const { token, isTeacher } = useContext(StoreContext);
  const [marks, setMarks] = useState<Record<string, any>[]>([]);
  const [editRow, setEditRow] = useState<number>();
  const [inputVal, setInputVal] = useState<number | string>('');
  
  useEffect(() => {
    const fetchInfo = async () => {
      // Get all users and their details in the course
      const getUsers = await api.get('/course/list', {
        params: {
          'token': token,
          'course_code': courseCode
        }
      });
      const lecturers = getUsers.data.lecturers;
      const students = getUsers.data.students;

      // Find the specific user for the grades which we want to display
      let idx = lecturers.findIndex((user: object) => user.user_id === userId);
      if (idx != -1) {
        setUsers(lecturers[idx]);
      } else {
        idx = students.findIndex((user: object) => user.user_id === userId);
        setUsers(students[idx]);
      }

      // Get the marks of the user to display
      const getMarks = await api.get('/student/results', {
        params: {
          'token': token,
          'studentId': userId,
          'course': courseCode
        }
      })
        .then((res) => res.data);

      // Get the students quiz marks
      const getQuizMarks = await api.get('/student/quiz/mark', {
        params: {
          'token': token,
          'studentId': userId
        }
      })
        .then((res) => res.data);
      const combine = [...getMarks, ...getQuizMarks];
      setMarks(combine);
    }
    fetchInfo();
  }, [])

  const handleUpdateMark = (event: ChangeEvent<HTMLInputElement>, assName: string) => {
    const { value } = event.target;
    setInputVal(value);
    const assIdx = marks.findIndex((ass) => ass.asstName === assName);
    setMarks((prev) => prev.map((ass) => ass.asstName === assName ? { ...ass, mark: value }: ass));
    api.post('/mark/assessment', {
      'token': token,
      'mark': value,
      'assessment': marks[assIdx].id,
      'student_id': userId
    })
  }

  const handleEdit = (idx: number) => {
    setInputVal('');
    setEditRow(idx);
  }

  return (
    <Layout>
      <div className='text-2xl text-left'>
        <p>{courseCode}</p>
      </div>
      <hr className='h-px bg-black'/>
      <div>
        <div className='text-xl text-left'>
          <p>{users.user_name} - Grades</p>
        </div>
      </div>
      <table className='text-left w-1/2'>
        <thead className='text-md bg-gray-50'>
          <tr>
            <th className='px-6 py-3'>Assessments</th>
            <th className='px-6 py-3'>Grade</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {marks.map((ass, idx) => {
            return(
              <tr key={idx} className='border'>
                <th className='px-6 py-4 font-medium text-gray-900 whitespace-nowrap'>{ass.asstName}</th>
                <td className='px-6 py-2'>
                  <div className='flex'>
                    {editRow === idx ? (
                      <div className='flex'>
                        <input 
                          name='mark'
                          value={editRow === idx ? inputVal : ass.mark}
                          type='text'
                          className='w-5'
                          autoFocus
                          onFocus={(e) => (e.target.value === '')}
                          onChange={(e) => handleUpdateMark(e,ass.asstName)}
                        />
                        <p>{ass.outOf}</p>
                      </div>
                    ) : (
                      <p>{ass.mark}{ass.outOf}</p>
                    )}
                    
                  </div>
                </td>
                <td className='mr-10'>
                  {isTeacher && !ass.quiz ? (editRow === idx ? (
                      <button onClick={() => handleEdit(-1)}>
                        Confirm
                      </button>
                    ) : (
                      <button onClick={() => handleEdit(idx)}>
                        Edit
                      </button>
                    )) : null
                  }
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </Layout>
  );
}