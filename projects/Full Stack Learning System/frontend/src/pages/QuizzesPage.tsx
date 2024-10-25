/**
 * List all the quizzes that are open
 */

import { useContext, useEffect, useState } from "react";
import { Layout } from "../components/Layout"
import { useParams } from "react-router-dom";
import { TokenContextType } from "../types";
import { StoreContext } from "../store";
import { api } from "../api";
import { QuizList } from "../components/QuizList";

export const QuizzesPage = () => {
  const { courseCode } = useParams();

  const tokenContext: TokenContextType = useContext(StoreContext);

  const [isTeacher, setIsTeacher] = useState<boolean>(false);

  useEffect(() => {
    const getIsTeacher = async () => {
      try {
        const teacher = await api.get('/user/is_lecturer', {
          params: {
            'token': tokenContext.token
          }
        })
        .then((res) => res.data);
        if (teacher.is_lecturer) {
          setIsTeacher(teacher.is_lecturer);
        } 
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message);
        }
      } 
    };
    getIsTeacher();
  }, [])

  return (
    <Layout>
      <div className='flex text-2xl justify-between item-center border-b border-slate pb-4'>
        <h1>Quizzes for {courseCode}</h1>
      </div>
      { courseCode && <QuizList isTeacher={isTeacher} courseCode={courseCode} /> }
    </Layout>
  )
}