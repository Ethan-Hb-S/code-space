/**
 *  Allow users to select their avatars for their profile
 */

import { Avatar } from "../types"

type AvatarSelectProps = {
  avatar: Avatar,
  onClick: () => void
}

export const AvatarSelect = ({avatar, onClick}: AvatarSelectProps) => {

  const handleClick = () => {
    onClick();
  }

  return (
    <div className='w-full flex justify-center items-center'>
      <button onClick={handleClick}>
        <img
          className='h-20 w-20 hover:cursor-pointer'
          src={`../assets/${avatar}.svg`}
        />
      </button>
    </div> 
  )
}