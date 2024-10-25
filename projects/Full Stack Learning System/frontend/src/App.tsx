import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { CreateCourse } from './pages/CreateCourse';
import { CoursePage } from './pages/CoursePage';
import { CourseUsers } from './pages/CourseUsers';
import { UserGrades } from './pages/UserGrades';
import './App.css'
import { LoginPage } from './pages/LoginPage'
import { Search } from './pages/Search';
import { UserPage } from './pages/UserPage';
import { Forums } from './pages/Forums';
import { CreateForums } from './pages/CreateForums';
import { ForumPage } from './pages/ForumPage';
import { ClassPage } from './pages/ClassPage';
import { TokenContextType } from './types';
import { useContext } from 'react';
import { StoreContext } from './store';
import { QuizzesPage } from './pages/QuizzesPage';
import { SubmitAssignment } from './pages/SubmitAssignment';
import { AssessmentsPage } from './pages/AssessmentsPage';
import { EditQuizPage } from './pages/EditQuizPage';
import { EditQuestionPage } from './pages/EditQuestionPage';
import { QuizQuestions } from './pages/QuizQuestions';
import { QuizCompletion } from './pages/QuizCompletion';

function App() {
  const tokenContext: TokenContextType = useContext(StoreContext);

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={ tokenContext.token ? <Navigate to={'/dashboard'} /> : <Navigate to={'/login'} /> } />
        <Route path='/dashboard' element={ tokenContext.token ? <Dashboard /> : <Navigate to={'/login'} /> } />
        <Route path='/create-course' element={ tokenContext.token ? <CreateCourse /> : <Navigate to={'/login'} /> } />
        <Route path='/login' element={ tokenContext.token ? <Navigate to={'/dashboard'} /> : <LoginPage />} />s
        <Route path='/user/:userId' element={ tokenContext.token ? <UserPage/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode' element={ tokenContext.token ? <CoursePage/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/class' element={ tokenContext.token ? <ClassPage/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/users' element={ tokenContext.token ? <CourseUsers/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/:userId/grades' element={ tokenContext.token ? <UserGrades/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/search/:search' element={ tokenContext.token ? <Search/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/forums' element={ tokenContext.token ? <Forums/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/forums/create' element={ tokenContext.token ? <CreateForums/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/forums/:threadId' element={ tokenContext.token ? <ForumPage/> : <Navigate to={'/login'} /> } />

        <Route path='/course/:courseCode/quizzes' element={ <QuizzesPage /> } />
        <Route path='/course/:courseCode/quiz/edit/:quizId' element={ <EditQuizPage /> } />
        <Route path='/course/:courseCode/quiz/edit/:quizId/:questionId' element={ <EditQuestionPage /> } />

        <Route path='/course/:courseCode/quiz/:quizId' element={ tokenContext.token ? <QuizQuestions/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/quiz/:quizId/complete' element={ tokenContext.token ? <QuizCompletion/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/:asstName/:asstId/submit-assignment' element={ tokenContext.token ? <SubmitAssignment/> : <Navigate to={'/login'} /> } />
        <Route path='/course/:courseCode/assessments' element={ tokenContext.token ? <AssessmentsPage/> : <Navigate to={'/login'} /> } />
      </Routes>
    </BrowserRouter>
  )
}

export default App
