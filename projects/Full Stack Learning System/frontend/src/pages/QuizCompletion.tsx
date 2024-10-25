import { useNavigate, useParams } from "react-router-dom";

export const QuizCompletion = () => {
  const navigate = useNavigate();
  const { courseCode } = useParams();
  return (
    <div>
      <p>You have reached the end of the quiz. Click below to return to course page</p>
      <button onClick={() => navigate(`/course/${courseCode}`)}>Exit</button>
    </div>
  );
}