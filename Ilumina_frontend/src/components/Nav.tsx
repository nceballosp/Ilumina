import { useState } from 'react';
import logo from '../assets/3.svg';
import { ArrowLeftEndOnRectangleIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/solid';

export function NavBar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-ilumina border-b border-gray-200 py-3">
      <div className="max-w-full mx-auto flex items-center px-4 justify-between">
        
        <div className='flex w-1/2'>
          <a href="/" className="w-10">
            <img src={logo} alt="Logo" />
          </a>
        </div>

        <div className="hidden md:flex space-x-6 text-white">
          <a href="/" className="font-semibold hover:underline">Inicio</a>
          <a href="/load" className="font-semibold hover:underline">Cargar</a>
          <a href="/budget" className="font-semibold hover:underline">Presupuesto</a>
          <a href="/login">
            <ArrowLeftEndOnRectangleIcon className="size-6 text-white" />
          </a>  
        </div>

        {isOpen && (
          <div className="md:hidden flex text-white space-x-3">
            <a href="/" className="font-semibold hover:underline">Inicio</a>
            <a href="/load" className="font-semibold hover:underline">Cargar</a>
            <a href="/budget" className="font-semibold hover:underline">Presupuesto</a>
            <a href="/login" className="">
              <ArrowLeftEndOnRectangleIcon className="size-6 text-white" />
            </a>
          </div>
        )}
        
        <div className="md:hidden">
          <button onClick={() => setIsOpen(!isOpen)} className="text-white">
            {isOpen ? (
              <XMarkIcon className="size-6 hover:size-7" />
            ) : (
              <Bars3Icon className="size-6 hover:size-7" />
            )}
          </button>
        </div>
      </div>  

    </nav>
  );
}

