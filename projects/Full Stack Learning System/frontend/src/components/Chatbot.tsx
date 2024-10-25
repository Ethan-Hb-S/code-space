/**
 * Chatbot pop up window allowing users to send queries to the bot
 */

import React, { useState } from "react";
import { api } from "../api";

export const Chatbot = () => {
  
  const [openChat, setOpenChat] = useState<boolean>(false);
  const [query, setQuery] = useState<string>("");
  const [messages, setMessages] = useState<string[]>([]);

  // Initiate chatbot
  const handleOpenChat = async () => {
    setOpenChat(!openChat);
    const response = await api.get('/chatbot/start').then((res) => res.data);
    localStorage.setItem('botId', response.id);
  }

  const handleQuery = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  }

  const handleSendQuery = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Once user enters their query send it to the bot
    if (e.key === 'Enter') {
      setMessages((prev) => [...prev, query]);
      const sId = localStorage.getItem('botId');
      const msgResp = await api.post('/chatbot/send', {'query': query, 'session_id':sId})
        .then((res) => res.data);
      setMessages((prev) => [...prev, msgResp]);
      setQuery("");
    }
  }

  const handleCloseChat = () => {
    setOpenChat(!openChat);
    setMessages([]);
  }

  return(
    <div className='flex justify-end'>
      <div className='flex flex-col'>
        {openChat &&
          <div className='absolute flex flex-col justify-between right-5 bottom-5 h-1/2 border border-black rounded p-2 w-1/4'>
            <div className='whitespace-normal overflow-auto'>
              {messages.map((msg, idx) => {
                return(
                  <div 
                    key={idx}
                    className={`${idx % 2 === 0 ? 'bg-gray-300': ''}`}
                  >
                    <p>{msg}</p>
                  </div>
                );
              })}
            </div>
            <div className='flex'>
              <input
                type='text'
                placeholder='Enter your message'
                className='border border-black p-2 w-full'
                value={query === "" ? "" : query}
                onChange={handleQuery}
                onKeyDown={handleSendQuery}
              />
              <button type='button' className='text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg p-1.5 dark:hover:bg-gray-800' onClick={handleCloseChat}>
                <span>&times;</span>
              </button>
            </div>
          </div>
        }
        {!openChat &&
          <div className='border border-black rounded-full w-min p-2'>
            <button onClick={handleOpenChat}>Chat</button>
          </div>
        }
      </div>
    </div>
  );
}