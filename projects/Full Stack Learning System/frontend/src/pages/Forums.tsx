/**
 * List all the threads in a forum
 */

import { MouseEvent, useContext, useEffect, useState } from 'react';
import { Layout } from '../components/Layout';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../api';
import avatar from '../images/user.png';
import { StoreContext } from '../store';
import { ThreadItems, PinnedThreads } from '../types';
import { Chatbot } from '../components/Chatbot';

export const Forums = () => {
  const [pinnedThreads, setPinnedThreads] = useState<PinnedThreads[]>([]);
  const [threads, setThreads] = useState<ThreadItems[]>([]);
  const [update, setUpdate] = useState<boolean>(false);
  const code = useParams().courseCode;
  const navigate = useNavigate();

  const { token } = useContext(StoreContext);

  const handleCreateForum = () => {
    navigate(`/course/${code}/forums/create`);
  }
  
  useEffect(() => {
    const getInfo = async () => {
      // Get list of threads to display to user
      const threadList = await api.get('/threads/list', {
        params: {
          'token': token,
          'course_code': code
        }
      })
      .then((res) => res.data);

      setThreads(threadList.threads);
      setPinnedThreads(threadList.pinned_threads);
    }
    getInfo();
  }, [update])

  // Pin thread
  const handlePinForum = async (event: MouseEvent<HTMLButtonElement>, threadId: number) => {
    event.stopPropagation();
    api.post('/thread/pin', {'thread_id': threadId, 'token': token});
    setUpdate(!update);
  }

  // Unpin thread
  const handleUnpinForum = async (event: MouseEvent<HTMLButtonElement>, threadId: number) => {
    event.stopPropagation();
    try {
      api.delete('/thread/unpin', {
        data: {
          'thread_id': threadId,
          'token': token
        },
      })
      setUpdate(!update);
    } catch (e) {
      if (e instanceof Error) {
        console.log(e);
      }
    }
  }

  return (
    <Layout>
      <div className='text-2xl text-left'>
        <p>{code} - Forums</p>
        <hr className='h-px bg-black'/>
      </div>
      <div className='flex flex-col h-full justify-between'>
        <div>
          <div className='flex items-center justify-between'>
            <h2 className='text-xl'>Forums</h2>
            <button onClick={handleCreateForum}>Create forum</button>
          </div>
          <table className='table-auto text-left w-3/5'>
            <thead className='text-md bg-gray-50'>
              <tr>
                <th className='px-6 py-3'>Forums</th>
                <th className='px-6 py-3'>Created by</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {pinnedThreads.map((pinnedThread) => {
                return(
                  <tr
                    key={pinnedThread.thread_id}
                    className='border hover:bg-slate-200'
                    onClick={() => navigate(`/course/${code}/forums/${pinnedThread.thread_id}`)}
                  >
                    <td className='px-6 py-3'>{pinnedThread.thread_title}</td>
                    <td>
                      <div className='flex items-center gap-5 px-6 py-3'>
                        <img className='w-6 h-6 rounded-full' src={avatar}/>
                        <p>{pinnedThread.author_name}</p>
                      </div>
                    </td>
                    <td>
                      <button onClick={(event) => handleUnpinForum(event, pinnedThread.thread_id)}>Unpin</button>
                    </td>
                  </tr>
                );
              })}
              {threads.map((thread) => {
                return(
                  <tr
                    key={thread.thread_id}
                    className='border hover:bg-slate-200'
                    onClick={() => navigate(`/course/${code}/forums/${thread.thread_id}`)}
                  >
                    <td className='px-6 py-3'>{thread.thread_title}</td>
                    <td>
                      <div className='flex items-center gap-5 px-6 py-3'>
                        <img className='w-6 h-6 rounded-full' src={avatar}/>
                        <p>{thread.author_name}</p>
                      </div>
                    </td>
                    <td>
                      <button onClick={(event) => handlePinForum(event, thread.thread_id)}>Pin</button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <Chatbot />
      </div>
    </Layout>
  );
}