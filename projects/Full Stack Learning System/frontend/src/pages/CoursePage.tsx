/**
 * Default home page when you click into a course on the dashboard
 */

import { useParams } from 'react-router';
import { Layout } from '../components/Layout';
import { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadFileModal } from '../components/UploadFileModal';
import { api } from '../api';
import { StoreContext } from '../store';
import { CourseTabs } from '../components/CourseTabs';
import { Chatbot } from '../components/Chatbot';

export const CoursePage = () => {
  const code = useParams().courseCode;
  const { token, isTeacher } = useContext(StoreContext);
  const navigate = useNavigate();
  const [searchField, setSearchField] = useState<string>('');
  const [openModal, setOpenModal] = useState<boolean>(false);
  const [pdf, setPdf] = useState<{ [key: string]: string }>();
  const [fileNames, setFileNames] = useState<string[]>([]);
  const [description, setDescription] = useState<string>("");
  const { userId } = useContext(StoreContext);

  useEffect(() => {
    // Get file names to display on course page
    const fetchMaterials = async () => {
      const getFileNames = await api.get('/files/list', {
        params: {
          'token': token,
          'code': code
        }
      })
        .then((res) => res.data);
      setFileNames([ ...fileNames, ...getFileNames]);

      const getCourseDescription = await api.get('/course/list', {
        params: {
          'token': token,
          'course_code': code
        }
      })
        .then((res) => res.data.description);
      setDescription(getCourseDescription);

      // Retrieve the files from cloud storage
      const file = await api.get('/retrieve/files/cloud')
        .then((res) => res.data);
      setPdf(file);
    }
    fetchMaterials();
  },[])

  const handleSearch = (event: any) => {
    if (event.key === 'Enter') {
      navigate(`/course/${code}/search/${searchField}`);
    }
  }

  const courseMaterials = fileNames.map((name: string, idx) => {
    if (pdf) {
      const pdfLink = pdf[name];
      return (
        <div key={idx}>
          <a
            href={pdfLink}
            target="_blank"
            rel="noreferrer"
          >
            {name}
          </a>
        </div>
      );
    }
  })

  return (
    <Layout>
      <div className='flex flex-col justify-between h-full'>
        <div>
          <div className='text-2xl text-left'>
            <p>{code}</p>
          </div>
          <hr className='h-px bg-black'/>
          <div className='flex justify-between items-center'>
            <CourseTabs code={code} userId={userId} />
            <div className='flex flex-col items-center'>
              <input 
                type='search'
                placeholder='Search course materials'
                className='bg-gray-50 border border-black rounded-lg p-2'
                onChange={e => setSearchField(e.target.value)}
                onKeyDown={handleSearch}
              />
              {isTeacher &&
                <button
                  className='border border-black rounded w-full mt-2'
                  onClick={() => setOpenModal(true)}
                >
                  Upload Files
                </button>
              }
            </div>
          </div>
          <div className='border text-left p-4 mt-2'>
            <div className='text-md font-bold'>
              <p>Course Overview</p>
            </div>
            <div>
              {description}
            </div>
          </div>
          <div className='text-left mt-5'>
            Course Materials:
            <div>
              {courseMaterials}
            </div>
          </div>
          {openModal &&
            <UploadFileModal setOpenModal={setOpenModal} />
          }
        </div>
        <Chatbot />
      </div>
    </Layout>
  );
}