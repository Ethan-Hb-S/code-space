/**
 * Modal which allows teachers to upload course materials
 */

import React, { ChangeEvent, useContext, useState } from 'react';
import { api } from '../api';
import { StoreContext } from '../store';
import { useParams } from 'react-router-dom';

interface ChildProps {
  setOpenModal: (value: boolean) => void;
}

export const UploadFileModal: React.FC<ChildProps> = ({ setOpenModal }) => {
  const { token } = useContext(StoreContext);
  const code = useParams().courseCode;
  const [pdf, setPdf] = useState<File[]>([]);
  const [pdfName, setPdfName] = useState<string[]>([]);

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files;

    // Record the files uploaded by the teacher
    if (file) {
      for (const f of file) {
        setPdfName((prev) => [...prev, f.name]);
        setPdf((prev) => [...prev, f]);
      }
    }
  }
  const handleUpload = async () => {
    // Upload the metadata of each file into database
    for (const f of pdf) {
      api.post('/upload/file', {
        'token': token,
        'name': f.name,
        'course_code': code,
      })

      // Upload file into GCS
      const formData = new FormData();
      formData.append(f.name, f);
      api.post('/upload/cloud', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Notify all students that a new material has been posted
      api.post('/materials/notify', {
        'token': token,
        'filename': f.name,
        'course_code': code,
      })

    }
    setOpenModal(false);
  }
  return (
    <div className='fixed inset-0 flex items-center justify-center z-50'>
      <div className='fixed inset-0 bg-gray-500 opacity-50'></div>
      <div className='flex flex-col bg-white p-4 rounded-lg shadow-lg relative h-56 w-1/4'>
        <div className='flex align-center justify-between'>
          <h2 className='text-gray-800 text-2xl font-bold' onClick={() => console.log(pdf, pdfName)}>Upload Class Material:</h2>
          <button type='button' className='text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg p-1.5 dark:hover:bg-gray-800' onClick={() => setOpenModal(false)}>
            <span>&times;</span>
          </button>
        </div>
        <div className='flex flex-col justify-center h-screen'>
          <input
            className='border border-black rounded'
            type='file'
            multiple
            onChange={handleFileChange}
          />
        </div>
        <div>
          <button className='bg-blue-500 text-white border border-black rounded' onClick={handleUpload}>Upload</button>
        </div>
      </div>
    </div>
  );
}
