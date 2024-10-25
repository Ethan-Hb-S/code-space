/**
 * Allow teachers to add/delete/update quiz details or quiz questions
 */

import { useContext, useEffect, useState } from "react";
import { StoreContext } from "../store";
import { Question, Quiz, TokenContextType } from "../types";
import { useNavigate, useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { api } from "../api";

export const EditQuizPage = () => {
  const tokenContext: TokenContextType = useContext(StoreContext);
  const quizId = useParams().quizId;
  const courseCode = useParams().courseCode;

  const [nameError, setNameError] = useState<string>('');
  const [descriptionError, setDescriptionError] = useState<string>('');
  const [datesError, setDatesError] = useState<string>('');

  const [questions, setQuestions] = useState<Question[]>([]);

  const [quiz, setQuiz] = useState<Quiz>({
    'quiz_id': -1,
    name: '',
    description: '',
    due_date: '',
  });

  const navigate = useNavigate();

  const handleClickQuestion = (questionId: number) => {
    navigate(`/course/${courseCode}/quiz/edit/${quiz.quiz_id}/${questionId}`);
  }
  
  // Add a new question in the quiz
  const handleAddQuestion = async () => {
    try {
      const questionId = await api.post('/question/create', {
        token: tokenContext.token,
        description: 'New question',
        quiz_id: quizId,
      })
        .then(res => res.data)
        .then(data => data.question_id)
      navigate(`/course/${courseCode}/quiz/edit/${quizId}/${questionId}`);
    } catch (err) {
      if (err instanceof Error) {
        console.log(err);
      }
    }
  }

  // Delete a question from the quiz
  const handleDelete = async (questionId: number) => {
    try {
      await api.delete('/question/delete', {
        data: {
          token: tokenContext.token,
          question_id: questionId,
        }
      });
      setQuestions([]);
    } catch (err) {
      if (err instanceof Error) {
        console.log(err);
      }
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setQuiz((prevData) => ({ ...prevData, [name]: value }));
    clearErrors();
  }

  const clearErrors = () => {
    setNameError('');
    setDescriptionError('');
    setDatesError('');
  }

  // Ensure that all required details of the quiz are filled out
  const validateChanges = () => {
    if (quiz.name === '') {
      setNameError('Quiz name is required');
      return false;
    }

    if (quiz.description === '') {
      setDescriptionError('Description is required');
      return false;
    }

    const currentDate = new Date().toISOString().slice(0, 10);
    if (quiz.due_date < currentDate) {
      setDatesError('Quiz due date cannot be before the current date');
      return false;
    }
    return true;
  }

  const handleSave = async () => {
    if (validateChanges()) {
      try {
        await api.put('/quiz/update', {
          token: tokenContext.token,
          ...quiz
        })
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message)
        }
      }
    }
  }


  
  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const data = await api
          .get('/quiz', {
            params: {
              token: tokenContext.token,
              'quiz_id': quizId
            }
          })
          .then(res => res.data)
        const formattedDate = new Date(data.due_date).toLocaleDateString('en-CA')
        const newQuiz: Quiz = {
          quiz_id: data.quiz_id,
          name: data.name,
          description: data.description,
          due_date: formattedDate,
        }
        setQuiz(newQuiz);
        const newQuestions: Question[] = data.questions.map((obj: { description: any; question_id: any; }) => {
          const { description, question_id } = obj;
          return { description, question_id };
        });
        setQuestions(newQuestions);
      } catch (e) {
        if (e instanceof Error) {
          console.log(e);
        }
      }
    }
    fetchQuiz();
  }, [questions.length])

  return (
    <Layout>
      <div className="flex gap-10">
        <div>
          <div className='text-start'>
            <label className='text-black font-medium'>
              Quiz name
            </label>
            <div>
              <input
                type='text'
                name='name'
                value={quiz.name}
                onChange={handleChange}
                className='w-full rounded border px-2 h-10 border-slate-400' />
            </div>
            {nameError !== '' && <div className='text-red-500'>{nameError}</div>}
          </div>
          <div className='text-start'>
            <label className='text-black font-medium'>
              Quiz description
            </label>
            <div>
              <input
                type='text'
                name='description'
                value={quiz.description}
                onChange={handleChange}
                className='w-full rounded border px-2 h-10 border-slate-400' />
            </div>
            {descriptionError !== '' && <div className='text-red-500'>{descriptionError}</div>}
          </div>
          <div className='text-start'>
            <label className='text-black font-medium'>
              Due date
            </label>
            <div>
              <input
                type='date'
                name='due_date'
                value={quiz.due_date}
                onChange={handleChange}
                className='w-full rounded border px-2 h-10 border-slate-400' />
            </div>
            {datesError !== '' && <div className='text-red-500'>{datesError}</div>}
          </div>
          <button onClick={handleSave} className="bg-blue-500 hover:bg-blue-600 text-white border mt-2 rounded-md px-2">
            Save changes
          </button>
        </div>
        <div className='w-full'>
          <h1 className='text-left'>
            Questions
          </h1>
          <div className='flex flex-col mt-4 gap-4'>
            {questions.map(question => (
              <div key={question.question_id} className='flex gap-2'>
                <button className='w-full' onClick={() => handleClickQuestion(question.question_id)} key={question.question_id}>
                  <div className='rounded-lg hover:bg-slate-100 border border-slate-600 p-4 flex text-left'>
                    <h3 className='font-lg'>
                      {question.description}
                    </h3>
                  </div>
                </button>
                <button>
                  <div className="rounded-lg hover:bg-red-600 bg-red-500 text-white p-2" onClick={() => handleDelete(question.question_id)}>
                    Delete
                  </div>
                </button>
              </div>
            ))}
          </div>
          <button onClick={handleAddQuestion} className='text-slate-500 mt-5'>
            Add question
          </button>
        </div>
      </div>
    </Layout>
  )
}