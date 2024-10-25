/**
 * Display all assessments that are currently open
 */

import { useEffect, useState } from "react";
import { Layout } from "../components/Layout";
import { api } from "../api";
import { useNavigate, useParams } from "react-router-dom";

interface Courses {
  title: string,
  due_date: Date,
  id: number
}

export const AssessmentsPage = () => {
  
  const [assessments, setAssessments] = useState<Courses[]>([]);
  const code = useParams().courseCode;
  const navigate = useNavigate();

  // Get all open assessments for specific course
  useEffect(() => {
    const getAssessments = async () => {
      const ass = await api.get('/course/assessments', {
        params: {
          'course': code
        }
      })
        .then((res) => res.data);
      setAssessments(ass);
    }
    getAssessments();
  }, [])

  return (
    <Layout>
      <div className='text-2xl text-left'>
        <p>{code} - Assessments</p>
      </div>
      <hr className='h-px bg-black'/>
      <div>
        <table className='text-left w-3/5'>
          <thead className='text-md bg-gray-50'>
            <tr>
              <th className='px-6 py-3'>Assessment</th>
              <th className='px-6 py-3'>Due Date</th>
            </tr>
          </thead>
          <tbody>
            {assessments.map((ass, idx) => {
              return(
                <tr
                  key={idx}
                  className='border hover:bg-slate-200'
                  onClick={() => navigate(`/course/${code}/${ass.title}/${ass.id}/submit-assignment`)}
                >
                  <td className='px-6 py-2'>{ass.title}</td>
                  <td className='px-6 py-2'>{ass.due_date}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}