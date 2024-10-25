/**
 * Display a list of avatars which users can select for their profile picture
 */

import { useContext, useEffect, useState } from "react";
import { AvatarSelect } from "../components/AvatarSelect";
import { Layout } from "../components/Layout"
import defaultAvatar from '../images/user.png';
import { Avatar } from "../types";
import { api } from "../api";
import { StoreContext } from "../store";

export const UserPage = () => {
  const { token } = useContext(StoreContext);

  const [avatar, setAvatar] = useState<Avatar>(Avatar.default);
  const [name, setName] = useState<string>('Name');
  const [email, setEmail] = useState<string>('name@email.com');

  const handleSelectAvatar = (selectedAvatar: Avatar) => {
    setAvatar(selectedAvatar);
  }
  
  const handleSaveAvatar = async () => {
    // Save the selected avatar in the database
    try {
      await api
      .put('/user/avatar', {
        'token': token,
        avatar: avatar,
      })
      .then()
    } catch (err) {
      if (err instanceof Error) {
        console.log(err.message);
      }
    }
  }

  useEffect(() => {
    const getUserInfo = async () => {
      try {
        // Get user information 
        const userInfo = await api.get('/user', { params: { 'token': token } })
          .then(res => res.data);
          setName(userInfo.name);
        setEmail(userInfo.email);
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
  }, [])

  return (
    <Layout>
      <div className='flex flex-col flex-1'>
        <div className='flex justify-between item-center border-b border-slate pb-4'>
          <h1>Profile</h1>
        </div>
        <div className='flex justify-center mt-5'>
          <div className='text-left'>
            <p><b>Name: </b>{name}</p>
            <p><b>Email: </b>{email}</p>
          </div>
        </div>
        <div className='w-full py-10 flex justify-center'>
          <img className='h-32 w-32' src={avatar === Avatar.default ? defaultAvatar : `../assets/${avatar}.svg`}></img>
        </div>
        <div className='grid grid-cols-3 grid-rows-2'>
          <AvatarSelect avatar={Avatar.avatar1} onClick={() => handleSelectAvatar(Avatar.avatar1)} />
          <AvatarSelect avatar={Avatar.avatar2} onClick={() => handleSelectAvatar(Avatar.avatar2)} />
          <AvatarSelect avatar={Avatar.avatar3} onClick={() => handleSelectAvatar(Avatar.avatar3)} />
          <AvatarSelect avatar={Avatar.avatar4} onClick={() => handleSelectAvatar(Avatar.avatar4)} />
          <AvatarSelect avatar={Avatar.avatar5} onClick={() => handleSelectAvatar(Avatar.avatar5)} />
          <AvatarSelect avatar={Avatar.avatar6} onClick={() => handleSelectAvatar(Avatar.avatar6)} />
        </div>
        <div className='mt-10 flex justify-center gap-16'>
          <button className='bg-red-500 text-white w-1/3 rounded-lg h-10 hover:bg-red-600' onClick={ () => setAvatar(Avatar.default) }>
            Remove avatar
          </button>
          <button className='bg-blue-500 text-white w-1/3 rounded-lg h-10 hover:bg-blue-600' onClick={handleSaveAvatar}>
            Save avatar
          </button>
        </div>
      </div>
    </Layout>
  )
}