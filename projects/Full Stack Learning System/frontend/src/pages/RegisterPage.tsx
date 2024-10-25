/**
 * Registration page
 */

import { useContext, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { GoogleButton } from '../components/GoogleButton';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { api } from '../api';
import { TokenContextType } from '../types';
import { StoreContext } from '../store';

export const RegisterPage = () => {
  const [email, setEmail] = useState<string>('');
  const [emailError, setEmailError] = useState<boolean>(false);
  const [password, setPassword] = useState<string>('');
  const [passwordError, setPasswordError] = useState<boolean>(false);
  const [userType, setUserType] = useState<string>('');
  const [userTypeError, setUserTypeError] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const tokenContext: TokenContextType = useContext(StoreContext);

  const navigate = useNavigate();

  const handleSignUp = (e: React.FormEvent<HTMLButtonElement>) => {
    e.preventDefault();
    
    // validate email and password and userType selection
    if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
      setEmailError(true);
    } else if (password.length < 6) {
      setPasswordError(true);
    } else if (userType === '') {
      setUserTypeError(true);
    }

    if (emailError || passwordError) {
      return;
    } 
    //TODO: Handle backend registration
  }

  const googleRegistration = useGoogleLogin({
    onSuccess: async tokenResponse => {
      const userInfo = await axios
        .get('https://www.googleapis.com/oauth2/v3/userinfo', {
          headers: {
            Authorization: `Bearer ${tokenResponse.access_token}`
          },
        })
        .then(res => res.data);
      setIsLoading(false);

      // check if user is registered
      try {
        const isRegistered = await api
          .get('/user/exists', {
            params: { user_id: userInfo.sub }
          })
          .then(res => res.data);

        // handle login if already registered
        if (isRegistered.exists) {
          const authToken = await api
            .post('/user/login', {
              'user_id': userInfo.sub,
              email: userInfo.email,
            })
            .then(res => res.data)
            .then(data => data.token);
          tokenContext.setToken(authToken);
          tokenContext.setUserId(userInfo.sub);
          navigate('/dashboard');
        } else {
          // handle registration of new user
          const authToken = await api
            .post('/user/add', {
              'user_id': userInfo.sub,
              name: userInfo.name,
              email: userInfo.email,
            })
            .then(res => res.data)
            .then(data => data.token);
          tokenContext.setToken(authToken);
          tokenContext.setUserId(userInfo.sub);
          navigate('/userType');
        }
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message);
        }
      } 
    },
    onError: () => {
      setIsLoading(false);
    },
    onNonOAuthError: () => {
      setIsLoading(false);
    }
  })
  
  const handleGoogleRegistration = () => {
    setIsLoading(true);
    googleRegistration();
  }

  const handleSelectTeacher = (e: React.FormEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setUserTypeError(false);
    setUserType('teacher');
  }

  const handleSelectStudent = (e: React.FormEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setUserTypeError(false);
    setUserType('student');
  }

  return (
    <div className='flex justify-center'>
      {
        isLoading ? (
          <svg
            className="animate-spin inline-block w-6 h-6 border-[3px] border-current border-t-transparent text-blue-600 rounded-full"
            viewBox="0 0 24 24"
          ></svg>
        ) : (
          <div className='w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-sm p-5'>
            <h2 className='text-center text-3xl font-bold leading-9 tracking-tight text-gray-900'>
              Register
            </h2>
            <form className='space-y-6 mt-10'>
              <div className='text-start'>
                <label className='text-black font-medium'>
                  Email
                </label>
                <div>
                  <input
                    type='email'
                    required
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    onBlur={() => setEmailError(false)}
                    className='w-full rounded border px-2 h-10 border-slate-400' />
                </div>
                {emailError ? <p className='text-red-500'>Please enter a valid email address</p> : null}
              </div>
              <div className='text-start'>
                <label className='text-black font-medium'>
                  Password
                </label>
                <div>
                  <input
                    type='password'
                    required
                    value={password}
                    onBlur={() => setPasswordError(false)}
                    onChange={e => setPassword(e.target.value)}
                    className='w-full rounded border px-2 h-10 border-slate-400' />
                  {passwordError ? <p className='text-red-500'>Password must be at least 6 characters</p> : null}
                </div>
              </div>
              <div className='text-start'>
              </div>
              <div className='flex'>
                <button
                  className={userType === 'teacher' ? 'grow border border-slate-400 bg-blue-500' : 'grow border border-slate-400'}
                  onClick={handleSelectTeacher}
                >
                  Teacher
                </button>
                <button
                  className={userType === 'student' ? 'grow border border-slate-400 bg-blue-500' : 'grow border border-slate-400'}
                  onClick={handleSelectStudent}
                >
                  Student
                </button>
              </div>
              {userTypeError ? <p className='text-red-500'>Please select a user type</p> : null}
              <button
                type='submit'
                onClick={handleSignUp}
                className='bg-blue-500 text-white w-full rounded-lg h-10 hover:bg-blue-600'>
                Sign up
              </button>
            </form>
            <div className='flex items-center my-4'>
              <hr className='flex-grow border-t border-slate-400' />
              <span className='mx-4 text-gray-500'>or</span>
              <hr className='flex-grow border-t border-slate-400' />
            </div>
            <GoogleButton onClick={handleGoogleRegistration} />
            <p className='mt-4'>
              Already have an account? <Link className='text-blue-500 underline' to={'/login'}>Log in</Link>
            </p>
          </div>
        )
      }
    </div>
  )
}