export type Token = string | null;

export type UserId = string | null;

export type IsTeacher = boolean;

export enum LoginState {
  FORM,
  LOADING,
  SELECT_USER
}

export interface TokenContextType {
  token: Token;
  setToken: (token: Token) => void;
  userId: UserId;
  setUserId: (userId: UserId) => void;
  isTeacher: IsTeacher;
  setIsTeacher: (IsTeacher: IsTeacher) => void;
}

export enum Avatar {
  avatar1 = 'avatar1',
  avatar2 = 'avatar2',
  avatar3 = 'avatar3',
  avatar4 = 'avatar4',
  avatar5 = 'avatar5',
  avatar6 = 'avatar6',
  default = 'default',
}

export interface CourseItems {
  name: string,
  code: string,
  description: string,
}

export interface Messages {
  message_id: number,
  messages: MessageItems,
  created: Date,
  uid: number
}

export interface MessageItems {
  author_id: string,
  author_name: string,
  created: Date,
  message_id: number,
  files: FileItems
}

export interface FileItems {
  file_id: number,
  file_url: string,
  name: string
}

export interface ThreadItems {
  thread_id: number,
  thread_title: string,
  author_name: string,
  uid: number,
  created: Date
}

export interface PinnedThreads {
  author_name: string,
  thread_title:string,
  thread_id: number
}

export interface Assessments {
  asstName: string,
  course: string,
  due_date: string
}
export interface Quiz {
  quiz_id: number,
  name: string,
  description: string,
  due_date: string,
}

export interface Question {
  question_id: number,
  description: string
}

export interface Answer {
  answer_id: number,
  answer_string: string,
  is_correct: boolean,
}

export interface StudentAss {
  file: string,
  student: string
  fileName: string
}
