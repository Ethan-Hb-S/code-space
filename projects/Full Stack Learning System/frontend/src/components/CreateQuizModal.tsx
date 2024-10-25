/**
 * A form which allows teachers to create quizzes for students
 */
import { useContext, useState } from "react";
import { api } from "../api";
import { TokenContextType } from "../types";
import { StoreContext } from "../store";

interface CreateQuizModalProps {
  setOpenModal: (isOpen: boolean) => void;
  courseCode: string;
  incrementQuizCount: () => void;
}

interface QuizFormData {
  name: string;
  description: string;
  dueDate: string;
}

export const CreateQuizModal = ({ setOpenModal, courseCode, incrementQuizCount }: CreateQuizModalProps) => {
  const tokenContext: TokenContextType = useContext(StoreContext);

  const [quizFormData, setQuizFormData] = useState<QuizFormData>({
    name: '',
    description: '',
    dueDate: '',
  })

  const [nameError, setNameError] = useState<string>('');
  const [descriptionError, setDescriptionError] = useState<string>('');
  const [datesError, setDatesError] = useState<string>('');

  // Ensure that all required fields are filled in
  const validateForm = () => {
    if (quizFormData.name === '') {
      setNameError('Quiz name is required');
      return false;
    }

    if (quizFormData.description === '') {
      setDescriptionError('Description is required');
      return false;
    }

    const currentDate = new Date().toISOString().slice(0, 10);
    if (quizFormData.dueDate < currentDate) {
      setDatesError('Quiz due date cannot be before the current date');
      return false;
    }

    return true;
  }

  const clearErrors = () => {
    setNameError('');
    setDescriptionError('');
    setDatesError('');
  }

  // Record form details
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setQuizFormData((prevData) => ({ ...prevData, [name]: value }));
    clearErrors();
  }

  // Submit form with the details filled in
  const handleSubmit = async () => {
    if (validateForm()) {
      try {
        const quizId = await api.post('/quiz/create', {
          token: tokenContext.token,
          name: quizFormData.name,
          description: quizFormData.description,
          'due_date': quizFormData.dueDate,
          'result_hidden': false,
          'max_duration': 0,
          'course_code': courseCode,
        })
          .then(res => res.data)
      } catch (err) {
        if (err instanceof Error) {
          console.log(err.message);
        }
      }
      incrementQuizCount();
      setOpenModal(false);
    }
  }

  return (
    <div className='fixed inset-0 flex items-center justify-center'>
      <div className='fixed inset-0 bg-gray-500 opacity-50'></div>
      <div className='flex flex-col bg-white p-4 rounded-lg shadow-lg relative w-1/4'>
        <div className='flex align-center justify-between'>
          <h2 className='text-gray-800 text-2xl font-bold'>New quiz</h2>
          <button type='button' className='text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg p-1.5 dark:hover:bg-gray-800' onClick={() => setOpenModal(false)}>
            <span>&times;</span>
          </button>
        </div>
        <div className='flex flex-col justify-center'>
          <label>
            Quiz name
          </label>
          <input
            type='text'
            name='name'
            value={quizFormData.name}
            onChange={handleChange}
            className='border border-black p-1 rounded'
          />
          {nameError !== '' && <div className='text-red-500'>{nameError}</div>}
        </div>
        <div className='flex flex-col justify-center'>
          <label>
            Description
          </label>
          <input
            type='text'
            name='description'
            value={quizFormData.description}
            onChange={handleChange}
            className='border border-black p-1 rounded'
          />
          {descriptionError !== '' && <div className='text-red-500'>{descriptionError}</div>}
        </div>
        <div className='flex flex-col justify-center'>
          <label>
            Due date
          </label>
          <input
            type='date'
            name='dueDate'
            className='border border-black p-1 rounded'
            value={quizFormData.dueDate}
            onChange={handleChange}
          />
          {datesError !== '' && <div className='text-red-500'>{datesError}</div>}
        </div>
        <button className='bg-blue-500 hover:bg-blue-600 text-white border mt-2 rounded-md' onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
}