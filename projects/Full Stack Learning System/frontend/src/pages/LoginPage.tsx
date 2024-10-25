/**
 * Login page to allow users to log into the system
 */

import { useContext, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { StoreContext } from '../store';
import { LoginState, TokenContextType } from '../types';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { GoogleButton } from '../components/GoogleButton';
import { api } from '../api';
import { SelectUserType } from '../components/SelectUserType';

export const LoginPage = () => {
  const [email, setEmail] = useState<string>('');
  const [emailError, setEmailError] = useState<boolean>(false);
  const [password, setPassword] = useState<string>('');
  const [passwordError, setPasswordError] = useState<boolean>(false);
  const [loginState, setLoginState] = useState<LoginState>(LoginState.FORM);
  const [tempToken, setTempToken] = useState<string>('');

  const tokenContext: TokenContextType = useContext(StoreContext);
  const navigate = useNavigate();

  const googleLogin = useGoogleLogin({
    onSuccess: async tokenResponse => {
      const userInfo = await axios
        .get('https://www.googleapis.com/oauth2/v3/userinfo', {
          headers: {
            Authorization: `Bearer ${tokenResponse.access_token}`
          },
        })
        .then(res => res.data);
        const userId = userInfo.sub.substring(userInfo.sub.length - 8);
      // check if user is registered
      try {
        const isRegistered = await api
          .get('/user/exists', {
            params: { user_id: userId }
          })
          .then(res => res.data);

        //handle login if already registered
        if (isRegistered.exists) {
          const authToken = await api
            .post('/user/login', {
              'user_id': userId,
              email: userInfo.email,
            })
            .then(res => res.data)
            .then(data => data.token);
          tokenContext.setToken(authToken);
          tokenContext.setUserId(userId);
          const isTeacher = await api.get('/user/is_lecturer', {
            params: {
              'token': authToken
            }
          })
            .then((res) => res.data.is_lecturer);
          tokenContext.setIsTeacher(isTeacher);
          navigate('/dashboard');
        } else {
          // handle registration of new user
          const authToken = await api
            .post('/user/add', {
              'user_id': userId,
              name: userInfo.name,
              email: userInfo.email,
            })
            .then(res => res.data)
            .then(data => data.token);
          setTempToken(authToken);
          tokenContext.setUserId(userId);
          setLoginState(LoginState.SELECT_USER);
        }
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message);
        }
      } 
    },
    onError: () => {
      setLoginState(LoginState.FORM);
    },
    onNonOAuthError: () => {
      setLoginState(LoginState.FORM);
    }
  })

  const handleGoogleLogin = () => {
    setLoginState(LoginState.LOADING);
    googleLogin();
  }
  
  useEffect(() => {
    if (tokenContext.token !== null) {
      console.log(tokenContext.token);
    }
  })

  return (
    <div className='flex pt-48 justify-center'>
      {loginState === LoginState.LOADING && <svg
        className="animate-spin inline-block w-6 h-6 border-[3px] border-current border-t-transparent text-blue-600 rounded-full"
        viewBox="0 0 24 24"
      ></svg>}
      {loginState === LoginState.FORM && <div className="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-sm p-5">
        <div className='flex justify-center p-4'>
          <img className='w-24 h-24' src='../assets/logo.svg'/>
        </div>
        <h2 className="text-center text-3xl font-bold leading-9 tracking-tight text-gray-900">
         Sign in
        </h2>
        <div className='my-6'>
          <p className='text-slate-600 text-left text-lg'>
            Welcome to Yellow Frogs LMS. Please log in or sign up below using Google.
          </p>
        </div>
        <GoogleButton
          onClick={handleGoogleLogin}
        />
      </div>}
      {loginState === LoginState.SELECT_USER && <SelectUserType token={tempToken} />}
    </div>
  )
}