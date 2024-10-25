/**
 * Allow users to create a new forum post
 */

import { ChangeEvent, useState, useContext } from "react";
import { Layout } from "../components/Layout";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api";
import { StoreContext } from "../store";

export const CreateForums = () => {
  const code = useParams().courseCode;
  const navigate = useNavigate();
  const [forumTitle, setForumTitle] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [fileNames, setFileNames] = useState<string[]>([]);
  const [files, setFiles] = useState<File[]>([]);
  const { token } = useContext(StoreContext);

  const handleSubmit = async () => {
    try {
      // Add new forum to a course
      const threadId = await api.post('/thread/add', {'title': forumTitle, 'course': code, 'token': token})
      .then((res) => res.data);

      // Upload any files within the thread to cloud storage
      const formData = new FormData();
      files.forEach((file) => {
        formData.append(file.name, file);
      });
      api.post('/upload/cloud', formData, {
        headers: {
          'Content-type': 'multipart/form-data'
        }
      });

      // Upload file detail to DB
      api.post('/message/add', {
        'token': token,
        'message': message,
        'thread': threadId.thread_id,
        'file_name': fileNames
      })

      // Notify all users in the course about the thread
      api.post('/thread/notify', {'thread_id': threadId.thread_id, 'course_code': code, 'token': token});
    } catch (e) {
      if (e instanceof Error) {
        console.log(e.message);
      }
    }
    navigate(`/course/${code}/forums`);
  }

  const handleStoreFile = async (event: ChangeEvent<HTMLInputElement>) => {
    const uploadedFiles = event.target.files;
    if (uploadedFiles) {
      const filesArray = Array.from(uploadedFiles);
      filesArray.forEach((file) => {
        setFileNames((prev) => [...prev, file.name]);
        setFiles((prev) => [...prev, file]);
      })
    }
  }

  return(
    <Layout>
      <div className='flex flex-col'>
        <div>
          <div className='text-2xl text-left'>
            <p>{code}</p>
            <hr className='h-px bg-black'/>
            <div className='text-lg mt-3 font-bold'>
              <p>Create new forum</p>
            </div>
          </div>
          {/* Form */}
          <div className='flex flex-col gap-4 w-full mt-5'>
            {/* Course name */}
            <div className='flex w-1/2 items-center'>
              <label className='mr-2 flex-1 text-left'>Forum Title:</label>
              <input
                type='text'
                placeholder='Enter title of forum'
                className='flex-4 bg-gray-50 border border-black rounded-lg p-1'
                name='title'
                id='title'
                onChange={(e) => setForumTitle(e.target.value)}
              />
            </div>

            {/* Course Description */}
            <div className='flex w-1/2'>
              <label className='mr-2 flex-1 text-left'>Description:</label>
              <textarea
                id='message'
                placeholder='Type forum message'
                name='message'
                className='flex-4 bg-gray-50 border border-black rounded-lg p-1'
                onChange={(e) => setMessage(e.target.value)}
              />
            </div>

            {/* Files */}
            <div className='flex w-1/2'>
              <label className='mr-2 flex-1 text-left'>Upload files:</label>
              <input
                type='file'
                multiple
                onChange={handleStoreFile}
              />
            </div>

            <div>
              <button
                className='border border-black bg-blue-500 text-white'
                onClick={handleSubmit}
                name='publish'
              >
                Create Forum
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}