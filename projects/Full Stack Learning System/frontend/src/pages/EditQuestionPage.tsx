/**
 * Allow teachers to edit a question in a quiz
 */

import { useContext, useEffect, useState } from "react"
import { Answer, TokenContextType } from "../types"
import { useNavigate, useParams } from "react-router-dom"
import { Layout } from "../components/Layout";
import { api } from "../api";
import { StoreContext } from "../store";
import { EditAnswerCard } from "../components/EditAnswerCard";

export const EditQuestionPage = () => {
  const questionId = useParams().questionId;
  const quizId = useParams().quizId;
  const courseCode = useParams().courseCode;

  const tokenContext: TokenContextType = useContext(StoreContext);

  const [description, setDescription] = useState<string>('');
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [descriptionError, setDescriptionError] = useState<string>('');
  const [answersError, setAnswersError] = useState<string>('');

  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDescription(e.target.value);
    setDescriptionError('');
  }

  // Update the answer of the question
  const updateAnswer = (answerIndex: number, updatedAnswer: string, isCorrect: boolean) => {
    const updatedAnswers = answers;
    updatedAnswers[answerIndex] = {
      answer_id: updatedAnswers[answerIndex].answer_id,
      answer_string: updatedAnswer,
      is_correct: isCorrect,
    }
    setAnswers(updatedAnswers);
    setAnswersError('');
  }

  const handleSaveChanges = async () => {
    if (!validateChanges()) {
      return;
    }
    
    try {
      await api.put('/question/update', {
        token: tokenContext.token,
        question_id: questionId,
        description: description,
        answers: answers,
      })
    } catch (err) {
      if (err instanceof Error) {
        console.log(err);
      }
    }
  }

  const validateChanges = () => {
    if (description === '') {
      setDescriptionError('Question cannot be empty')
      return false;
    }

    let correctAnswerExists = false;
    let emptyAnswerExists = false;
    answers.forEach(answer => {
      if (answer.is_correct) {
        correctAnswerExists = true;
      }
      if (answer.answer_string === '') {
        emptyAnswerExists = true;
      }
    })

    if (emptyAnswerExists) {
      setAnswersError('Answers cannot be empty');
      return false;
    }

    if (!correctAnswerExists) {
      setAnswersError('Question must have AT LEAST ONE correct answer');
      return false;
    }

    return true;
  }

  const handleClickBack = () => {
    navigate(`/course/${courseCode}/quiz/edit/${quizId}`);
  }

  useEffect(() => {
    const fetchQuestion = async () => {
      try {
        const question = await api.get('/question', {
          params: {
            token: tokenContext.token,
            question_id: questionId
          }
        })
          .then(res => res.data);
        setDescription(question.description);
        setAnswers(question.answers);
      } catch (err) {
        if (err instanceof Error) {
          console.log(err);
        }
      }
    }
    fetchQuestion();
  }, [])

  return (
    <Layout>
      <div className='flex justify-between item-center border-b border-slate pb-4'>
        <h1>Edit question</h1>
      </div>
      <input
        type='text'
        name='description'
        value={description}
        onChange={handleChange}
        className='w-full rounded border px-2 h-10 border-slate-400'
      />
      { descriptionError !== '' && <p className='text-red-500'>{descriptionError}</p> }
      <div className='mt-10 flex flex-col gap-5 items-center w-full'>
        { answers.map((answer, idx) => {
          return <EditAnswerCard key={idx} answerIndex={idx} isCorrect={answer.is_correct} answerString={answer.answer_string} updateAnswer={updateAnswer} />
        }) }
      </div>
      { answersError !== '' && <div className='text-red-500'>{answersError}</div> }
      <div className='flex justify-center mt-10 gap-5'>
        <button className="w-1/5">
          <div onClick={handleClickBack} className="rounded-lg hover:bg-slate-100 border border-slate-600 p-4 text-center">
            Back
          </div>
        </button>
        <button className="w-1/5 ">
          <div onClick={handleSaveChanges} className="rounded-lg hover:bg-blue-600 bg-blue-500 text-white p-4 text-center">
            Save Changes
          </div>
        </button>
      </div>
    </Layout>
  )
}