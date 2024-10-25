/**
 * Lists all current quizzes that have been created
 */

import { useContext, useEffect, useState } from "react"
import { Quiz, TokenContextType } from "../types"
import { StoreContext } from "../store"
import { api } from "../api";
import { CreateQuizModal } from "./CreateQuizModal";
import { useNavigate } from "react-router-dom";

interface QuizListProps {
  isTeacher: boolean,
  courseCode: string,
}

export const QuizList = ({ isTeacher, courseCode }: QuizListProps) => {
  const tokenContext: TokenContextType = useContext(StoreContext);
  const navigate = useNavigate();

  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [quizCount, setQuizCount] = useState<number>(0);
  const [modalOpen, setModalOpen] = useState<boolean>(false);

  const handleClick = (quizId: number) => {
    if (isTeacher) {
      navigate(`/course/${courseCode}/quiz/edit/${quizId}`);
    } else {
      navigate(`/course/${courseCode}/quiz/${quizId}`)
    }
  }

  useEffect(() => {
    // Get all current quizzes that are available
    const getQuizzes = async () => {
      try {
        const data = await api.get('/quizzes', {
          params: {
            'token': tokenContext.token,
            'course_code': courseCode
          }
        })
          .then(res => res.data);
        setQuizzes(data.quizzes);
        setQuizCount(data.quizzes.length);
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message);
        }
      }
    }
    getQuizzes();
  }, [isTeacher, courseCode, quizCount])

  return (
    <div>
      <div className='flex flex-col gap-5'>
        {Array.from(quizzes).map(quiz => (
          <button key={quiz.quiz_id} onClick={() => handleClick(quiz.quiz_id)}>
            <div className='rounded-lg hover:bg-slate-100 border border-slate-600 p-4 flex  text-left'>
              <div className='flex-col'>
                <h3 className='font-lg'>
                  {quiz.name}
                </h3>
                <p className='text-sm'>
                  {quiz.description}
                </p>
                <p className='text-sm'>
                  Due: {quiz.due_date}
                </p>
              </div>
            </div>
          </button>
        ))}
      </div>
      {isTeacher && <button onClick={() => setModalOpen(true)} className='mt-10 bg-blue-500 text-white w-full rounded-lg h-10 hover:bg-blue-600'>
        Add new quiz
      </button>}
      {modalOpen && <CreateQuizModal incrementQuizCount={() => setQuizCount(quizCount + 1)} courseCode={courseCode ? courseCode : ''} setOpenModal={setModalOpen} />}
    </div>
  )
}