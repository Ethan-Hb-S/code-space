/**
 * Basic layout of the LMS
 */

import React, { useContext, useEffect, useState } from 'react';
import defaultAvatar from '../images/user.png';
import { useNavigate } from 'react-router-dom';
import { Avatar, TokenContextType } from '../types';
import { StoreContext } from '../store';
import { api } from '../api';

export const Layout = (props: ContainerProps) => {
  const tokenContext: TokenContextType = useContext(StoreContext);

  const navigate = useNavigate();

  const [avatar, setAvatar] = useState<Avatar>(Avatar.default);

  const handleClickUserAvatar = () => {
    navigate(`/user/${tokenContext.userId}`);
  }

  const handleLogout = () => {
    const logout = async () => {
      try {
        await api
          .post('/user/logout', {
            token: tokenContext.token
          })
        tokenContext.setToken(null);
        tokenContext.setUserId(null);
        navigate('/login');
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message);
        }
      }
    }
    logout();
  }

  useEffect(() => {
    const getUserInfo = async () => {
      try {
        const userInfo = await api.get('/user', { params: { 'token': tokenContext.token } })
          .then(res => res.data);
        if (userInfo.avatar) {
          setAvatar(userInfo.avatar);
        }
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message);
        }
      }
    }
    getUserInfo();
  }, [tokenContext.userId]);

  return (
    <div className='flex flex-col h-screen w-screen'>
      <div className='flex justify-between items-center p-3 gap-2 bg-blue-500'>
        <button title='Go to dashboard' onClick={() => navigate('/dashboard')}>
          <img className='w-10 h-10' src='/assets/logo.svg' />
        </button>
        <div className='flex gap-3'>
          <div className='avatar flex items-center'>
            <button onClick={handleClickUserAvatar}>
              <img src={avatar === Avatar.default ? defaultAvatar : `/assets/${avatar}.svg`} height={30} width={30} />
            </button>
          </div>
          <button onClick={handleLogout}>
            Log out
          </button>
        </div>
      </div>
      <div className='flex-1 p-5 flex flex-col w-full gap-2'>
        {props.children}
      </div>
    </div>
  );
};

type ContainerProps = {
  children: React.ReactNode,
};