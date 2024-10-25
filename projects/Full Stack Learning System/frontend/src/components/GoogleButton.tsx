type GoogleButtonProps = {
  onClick: () => void;
}

export const GoogleButton = ({onClick}: GoogleButtonProps) => (
    <button
      className="bg-white border px-2 h-10 border-slate-400 w-full rounded-lg hover:bg-slate-200"
      onClick={onClick}
    >
      <div className='flex items-center gap-5'>
        <img src='../assets/GoogleIcon.svg' className='w-5 h-5'/>
        <p>
          Continue with Google
        </p>
      </div>
   </button>
);