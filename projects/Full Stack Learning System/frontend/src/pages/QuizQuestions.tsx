/**
 * STUDENTS VIEW: This will display each question of the quiz which the teacher has created for the students to attempt
 * When the student clicks next it will take them to the next question
 */

import { useContext, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api";
import { StoreContext } from "../store";
import { Question, Answer } from "../types";

export const QuizQuestions = () => {
  const { courseCode, quizId } = useParams();
  const { token } = useContext(StoreContext)
  const [info, setInfo] = useState<string[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [idx, setIdx] = useState<number>(0);
  const [studentResponses, setStudentResponses] = useState<object>({});
  const [response, setResponse] = useState<number[]>([]);
  const navigate = useNavigate();
  useEffect(() => {
    const fetchQuiz = async () => {
      // Get the specific quiz which the student wants to attempt
      const data = await api.get('/quiz', {
        params: {
          'token': token,
          'quiz_id': quizId
        }
      })
        .then((res) => res.data);
      setInfo([data.description, data.name]);
      const qs: Question[] = data.questions.map((obj: any) => {
        const { description, question_id } = obj;
        return { description, question_id };
      })
      setQuestions(qs);

      const solns: Answer[] = data.questions.map((q: any) => {
        return (q.answers);
      })
      setAnswers(solns);

      // Once the student has attempted all the questions direct them to the completed quiz page
      if (idx === qs.length) {
        navigate(`/course/${courseCode}/quiz/${quizId}/complete`);
        api.post('/quiz/mark', {
          'token': token,
          'quiz_id': quizId,
          'answerList': studentResponses
        });
      }
    }
    fetchQuiz();
  }, [idx])

  const currQuestion = questions[idx]

  const handleRecordResponse = (id: number) => {
    if (response.indexOf(id) !== -1) {
      const temp = response;
      temp.splice(response.indexOf(id), 1);
      setResponse(temp);
    } else {
      setResponse((prev) => [...prev, id]);
    }
  }

  const handleNextQuestion = () => {
    let id = questions[idx].question_id;
    setStudentResponses({...studentResponses, [id]: response});
    setResponse([]);
    setIdx(idx + 1);
  }

  return (
    <div className='flex flex-col h-full text-left p-10'>
      <p>{info[0]} - {info[1]}</p>
      <hr className='h-px bg-black'/>
      <div className='flex gap-5 mt-10 border border-black rounded p-5'>
        <div>{idx+1}.</div>
        <div>{currQuestion && currQuestion.description}</div>
      </div>
      <div className='flex flex-col gap-2'>
        {answers[idx] && answers[idx].map((ans: { answer_id: number, answer_string: string }) => {
          return(
            <div key={ans.answer_id} className='w-1/4'>
              <input
                type='checkbox'
                className='border border-black w-1/2 mt-10 p-5 rounded w-min mr-2'
                onClick={() => handleRecordResponse(ans.answer_id)}
              />
              <label>{ans.answer_string}</label>
            </div>
          );
        })}
      </div>
      <div className='flex justify-end'>
        <button
          className='border border-black p-2 rounded hover:bg-slate-400'
          onClick={handleNextQuestion}
        >
          Next
        </button>
      </div>
    </div>
  );
}