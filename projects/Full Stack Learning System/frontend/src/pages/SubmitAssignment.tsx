/**
 * STUDENT VIEW: Submission box to allow students to submit their assessments
 * TEACHER VIEW: Lists all the students who have submitted their assessment and allows them to download the file to mark
 */

import { ChangeEvent, useContext, useEffect, useState } from "react";
import { Layout } from "../components/Layout";
import { StoreContext } from "../store";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api";
import { StudentAss } from "../types";

export const SubmitAssignment = () => {
  
  const [fileName, setFileName] = useState<string>("");
  const [file, setFile] = useState<File>();
  const { token, isTeacher } = useContext(StoreContext);
  const { courseCode, asstName, asstId } = useParams();
  const navigate = useNavigate();
  const [submittedAss, setSubmittedAss] = useState<StudentAss[]>([]);

  useEffect(() => {
    const fetchInfo = async () => {
      // Get the submitted files from the students
      const response = await api.get('/submitted/files', {
        params: {
          'token': token,
          'assessment_id': asstId,
        }
      })
        .then((res) => res.data.files);

      // Fetch from GCS
      const fetchFiles = response.map((file: object) => {
        return api.get('/retrieve/files/cloud', {
          params: {
            'fileName': file.file
          }
        })
          .then((res) => res.data);
      })
      const fetchResult = await Promise.all(fetchFiles);
      const combine = response.map((student: object, idx: number) => ({
        ...student,
        file: Object.values(fetchResult[idx])[0],
        fileName: Object.keys(fetchResult[idx])[0]
      }));
      setSubmittedAss(combine);
    }
    if (isTeacher) {
      fetchInfo();
    }
  }, [])

  const handleUploadFile = (event: ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files[0];
    setFileName(uploadedFile.name);
    setFile(uploadedFile);
  }

  const handleSubmit = () => {
    // submit assignment
    api.post('/submit/assessment', {
      'token': token,
      'assessment': asstId,
      'file_name': fileName
    })

    // Upload to GCS
    if (file) {
      const formData = new FormData();
      formData.append(fileName, file);
      api.post('/upload/cloud', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    }
    navigate(`/course/${courseCode}`);
  }

  return(
    <Layout>
      <div>
        <div className='text-2xl text-left'>
          <p>Asessment</p>
        </div>
        <hr className='h-px bg-black'/>
        <div className='flex flex-col gap-5'>
          {!isTeacher &&
            <div>
              <div className='text-xl text-left mt-5'>
                <p>Submit your {asstName} assignment below</p>
              </div>
              <p className='text-sm text-left'>Name your file as "assessmentName_Id"</p>
              <div className='flex w-1/2 items-center p-4 border border-black rounded'>
                <label className='mr-2 flex-1 text-left'>Upload Assignment: </label>
                <input
                  type='file'
                  onChange={handleUploadFile}
                />
              </div>
              <div>
                <button
                  className='border border-black rounded w-1/12 mt-5'
                  onClick={handleSubmit}
                >
                  Submit
                </button>
              </div>
            </div>
          }
          {isTeacher &&
            <div>
              <div className='text-xl text-left mt-5'>
                <p>Submitted assignments for {asstName}:</p>
              </div>
              <div className='text-left mt-3'>
                {submittedAss && 
                  submittedAss.map((ass, idx) => {
                    return (
                      <div key={idx} className='flex gap-3'>
                        <p>{ass.student}</p> - 
                        <a
                          href={ass.file}
                          target="_blank"
                          rel="noreferrer"
                        >
                          {ass.fileName}
                        </a>
                      </div>
                    );
                  })
                }
              </div>
            </div>
          }
        </div>
      </div>
    </Layout>
  );
}