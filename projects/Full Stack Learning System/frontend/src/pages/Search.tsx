/** 
 * Allow users to search for course materials in a specific course
 */

import { useContext, useEffect, useState } from 'react';
import { Layout } from '../components/Layout';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../api';
import { StoreContext } from '../store';
import { Assessments } from '../types';

export const Search = () => {
  const { courseCode, search } = useParams();
  const { token } = useContext(StoreContext);
  const [files, setFiles] = useState<string[]>();
  const [assessments, setAssessments] = useState<Assessments[]>([])
  const navigate = useNavigate();
  useEffect(() => {
    const fetchMaterials = async () => {
      // Fetch all materials related to the students search
      const materials = await api.get('/search/material', {
        params: {
          'token': token,
          'course_code': courseCode,
          'search_word': search
        }
      })
        .then((res) => res.data);
      setAssessments(materials.assessments);

      // Fetch the file from GCS
      const fetchFiles = materials.files.map((file: string) => {
        return api.get('/retrieve/files/cloud', {
          params: {
            'fileName': file
          }
        })
          .then((res) => res.data);
      })
      const fetchResult = await Promise.all(fetchFiles);
      setFiles(fetchResult);
    }
    fetchMaterials();
  }, [])

	return (
		<Layout>
      <div className='text-2xl text-left'>
        <p>{courseCode}</p>
      </div>
      <hr className='h-px bg-black'/>
      <div className='text-xl text-left'>
        <p>Results for '{search}'</p>
      </div>
      <div>
        {files && 
          files.map((file, idx) => {
            const[name, url] = Object.entries(file)[0];
            return (
              <div key={idx}>
                <a
                  href={url}
                  target="_blank"
                  rel="noreferrer"
                >
                  {name}
                </a>
              </div>
            );
          })
        }
        {assessments &&
          assessments.map((ass, idx) => {
            const assId = Object.entries(ass)[0][1];
            const dueDate = Object.entries(ass)[1][1];
            const title = Object.entries(ass)[2][1];
            return (
              <div key={idx}>
                <button
                  onClick={() => navigate(`/course/${courseCode}/${title}/${assId}/submit-assignment`)}
                >
                  {title} - {dueDate}
                </button>
              </div>
            );
          })
        }
      </div>
    </Layout>
	);
}