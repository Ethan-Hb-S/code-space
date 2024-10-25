/**
 * List all the messages within a thread in a forum
 */

import { useEffect, useState, MouseEvent, ChangeEvent, useContext } from 'react';
import { Layout } from '../components/Layout';
import { useParams } from 'react-router-dom';
import { api } from '../api';
import { StoreContext } from '../store';
import { MessageItems, Messages, ThreadItems } from '../types';


export const ForumPage = () => {
  const code = useParams().courseCode;
  const threadId = useParams().threadId;
  const [messageList, setMessageList] = useState<MessageItems[]>([]);
  const [thread, setThread] = useState<ThreadItems>();
  const [pinned, setPinned] = useState<boolean>(false);
  const [liked, setLiked] = useState<boolean>(false);
  const [numLikes, setNumLikes] = useState<number>(0);
  const [showReply, setShowReply] = useState<boolean>(false);
  const [reply, setReply] = useState<string>("");
  const [files, setFiles] = useState<File[]>([]);
  const [fileNames, setFileNames] = useState<string[]>([]);
  const [update, setUpdate] = useState<boolean>(false);
  const { token } = useContext(StoreContext);
  const [cloudFiles, setCloudFiles] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    const getInfo = async () => {
      try {
        // Get list of threads
        const threadList = await api.get('/threads/list', {
          params: {
            'token': token,
            'course_code': code
          }
        })
          .then((res) => res.data);
        // Get the thread which the user is currently on
        threadList.threads.map(async (thread: ThreadItems) => {
          if (thread.thread_id === parseInt(threadId)) {
            setThread(thread);
          }
        })

        // Get pinned thread and check if current thread is pinned
        threadList.pinned_threads.map(async (thread: ThreadItems) => {
          if (thread.thread_id === parseInt(threadId)) {
            setThread(thread);
            setPinned(true);
          }
        })

        // Get list of messages in the thread
        const getMessages = await api.get('/message/list', {
          params: {
            'token': token,
            'thread_id': threadId
          }
        })
          .then((res) => res.data);
        const list: Messages[] = Object.values(getMessages.messages);
        setMessageList(list);

        // Check if message has been liked
        const messageLiked = await api.get('/message/liked', {
          params: {
            'token': token
          }
        })
          .then((res) => res.data);
        if (messageLiked.some((msg: number) => msg === list[0].message_id)) {
          setLiked(true);
        }

        // Get number of likes for message
        const messageLikes = await api.get('/message/likes_count', {
          params: {
            'token': token,
            'message_id': list[0].message_id
          }
        })
          .then((res) => res.data)
        setNumLikes(messageLikes.count);

        // Retrieve files from GCS
        const getCloudFiles = await api.get('/retrieve/files/cloud')
          .then((res) => res.data);
        setCloudFiles(getCloudFiles)
      } catch (e) {
        if (e instanceof Error) {
          console.log(e.message);
        }
      }
    }
    getInfo();
  },[showReply]);

  const handlePin = () => {
    if (pinned) {
      setPinned(!pinned);
      api.delete('/thread/unpin', {
        data: {
          'thread_id': threadId,
          'token': token
        }
      })
    } else {
      api.post('/thread/pin', {'thread_id': threadId, 'token': token});
      setPinned(!pinned);
    }
  }

  const handleLike = (event: MouseEvent<HTMLButtonElement>) => {
    if (liked) {
      api.delete('/message/unlike', {
        data: {
          'message': event.target.id,
          'token': token
        }
      });
      setLiked(!liked);
      setNumLikes(numLikes-1);
    } else {
      api.post('/message/like', {'message': event.target.id, 'token': token});
      setLiked(!liked);
      setNumLikes(numLikes+1);
    }
  }

  const handleStoreFile = (event: ChangeEvent<HTMLInputElement>) => {
    const uploadedFiles = event.target.files;
    if (uploadedFiles) {
      const filesArray = Array.from(uploadedFiles);
      filesArray.forEach((file) => {
        setFileNames((prev) => [...prev, file.name]);
        setFiles((prev) => [...prev, file]);
      })
    }
  }

  const handleReply = async () => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append(file.name, file);
    });
    api.post('/upload/cloud', formData, {
      headers: {
        'Content-type': 'multipart/form-data'
      }
    });
    api.post('/message/add', {
      'token': token,
      'message': reply,
      'thread': threadId,
      'file_name': fileNames,
    })

    setUpdate(!update);
    setShowReply(!reply);
  }
  const messageEntries = Object.entries(messageList).slice(1);
  return(
    <Layout>
      <div className='text-2xl text-left'>
        <p>{code} - Forums</p>
      </div>
      <hr className='h-px bg-black'/>
      {/* Initial thread box */}
      {messageList[0] &&
        <div className='flex flex-col'>
          <div className='text-xl text-left'>
            <p>{thread?.thread_title}</p>
          </div>
          <div className='flex flex-col border'>
            <div className='flex justify-between items-center p-2 mr-10 ml-10 mt-3'>
              <p>{thread?.author_name} - {thread?.created.toString()}</p>
              <div className='flex gap-2'>
                <button onClick={handlePin}>{pinned ? "Unpin" : "Pin"}</button>
                  <button
                    id={messageList[0].message_id}
                    className={`${liked ? 'bg-red-500' : 'bg-gray-300'}`}
                    onClick={handleLike}
                  >
                    {numLikes}-Like
                  </button>
              </div>
            </div>
            <div className='flex flex-col text-left p-2 mr-10 ml-10 mb-3'>
              <p>
                {messageList[0].message}
              </p>
              <div>
                <img src={cloudFiles[messageList[0].files[0].name]}/>
              </div>
            </div>
          </div>
        </div>
      }
      {/* Subsequent messages for the thread */}
      {messageEntries.map(([key, msg]) => {
        let fileList = msg.files;
        return(
          <div key={key} className='border flex flex-col text-left ml-12'>
            <div className=' mr-10 ml-10'>
              <div className='flex justify-between items-center p-2 mt-3'>
                {msg.author_name} - {msg.created.toString()}
              </div>
              <div className='flex text-left p-2 mb-3'>
                {msg.message}
              </div>
              <div>
                {cloudFiles &&
                  fileList.map((file: object, idx) => {
                    let name = file.name;
                    return (
                      <img key={idx} src={cloudFiles[name]} />
                    );
                  })
                }
              </div>
            </div>
          </div>
        );
      })}

      {/* Reply box */}
      {showReply &&
        <div className='flex border border-black rounded p-2'>
          <div className='flex gap-2 w-full'>
            <div className='flex flex-col gap-2 w-full'>
              <textarea
                className='w-full'
                placeholder='Write your reply'
                onChange={(e) => setReply(e.target.value)}
              />
              <input
                type='file'
                name='file_url'
                multiple
                onChange={handleStoreFile}
              />
            </div>
            <div className='flex'>
              <button onClick={handleReply}>Send</button>
            </div>
          </div>
        </div>
      }
      <div className='flex justify-end'>
        <button onClick={() => setShowReply(!showReply)}>Reply</button>
      </div>
    </Layout>
  );
}