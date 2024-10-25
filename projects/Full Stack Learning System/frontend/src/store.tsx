import { FC, ReactNode, createContext, useEffect, useState } from "react";
import { TokenContextType, Token, UserId, IsTeacher } from "./types";

export const StoreContext = createContext<TokenContextType>({
  token: null,
  setToken: () => {},
  userId: null,
  setUserId: () => {},
  isTeacher: false,
  setIsTeacher: () => {}
});

interface Props {
  children: ReactNode;
}

export const StoreProvider: FC<Props> = ({ children }) => {
  const [token, setToken] = useState<Token>(localStorage.getItem('token'));
  const [userId, setUserId] = useState<UserId>(localStorage.getItem('userId'));
  const [isTeacher, setIsTeacher] = useState<IsTeacher>(localStorage.getItem('isTeacher') === 'true');
  const store = {
    token: token,
    setToken: setToken,
    userId: userId,
    setUserId: setUserId,
    isTeacher: isTeacher,
    setIsTeacher: setIsTeacher
  }
  
  useEffect(() => {
    localStorage.setItem('token', token || '');
    localStorage.setItem('userId', userId || '');
    localStorage.setItem('isTeacher', isTeacher.toString());
    if (token === null || userId === null) {
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
      localStorage.removeItem('isTeacher')
    }
  }, [token, userId, isTeacher])
  
  return (
    <StoreContext.Provider value={store}>
      {children}
    </StoreContext.Provider>
  );
}
