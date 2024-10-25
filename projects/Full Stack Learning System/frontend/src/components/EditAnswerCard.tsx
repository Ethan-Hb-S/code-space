/**
 * When teachers add questions for a quiz, the solution and answers will be recorded
 */

import { useState } from "react";

interface EditAnswerCardProps {
  answerString: string;
  answerIndex: number;
  updateAnswer: (answerIndex: number, updatedAnswer: string, isCorrect: boolean) => void;
  isCorrect: boolean;
}

export const EditAnswerCard = ({ answerString, answerIndex, updateAnswer, isCorrect }: EditAnswerCardProps) => {
  const [ currAnswerString, setCurrAnswerString ] = useState<string>(answerString);
  const [ correct, setCorrect ] = useState<boolean>(isCorrect);

  // Record the answers for each question
  const handleChangeAnswerString = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrAnswerString(e.target.value);
    updateAnswer(answerIndex, e.target.value, correct);
  }

  const handleChangeCorrect = () => {
    setCorrect(!correct);
    updateAnswer(answerIndex, currAnswerString, !correct);
  }

  return (
    <div className={`flex justify-center w-1/3 ${correct ? 'bg-green-500' : ''} rounded-lg border border-slate-600 p-4 flex text-left`}>
      <input
        type='text'
        value={currAnswerString}
        onChange={handleChangeAnswerString}
        className='w-3/4 rounded border px-2 h-10 border-slate-400'
      />
      <button onClick={handleChangeCorrect}>
        Mark correct
      </button>
    </div>
  )
}