import { useState } from 'react';
import logo from '../assets/1.svg';
import { ArrowLeftEndOnRectangleIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/solid';

export function NavBar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-ilumina bg-opacity-95 backdrop-blur-2xl py-3 font-poppins shadow-md z-10 relative">
      <div className="max-w-full mx-auto flex items-center px-12 justify-between">
        
        <div className='flex'>
          <a href="/" className="w-45">
            <img src={logo} alt="Logo" />
          </a>
        </div>

        <div className="hidden md:flex space-x-10 text-white">
          <a href="/" className="font-semibold hover:text-iluminac">Inicio</a>
          <a href="/load" className="font-semibold hover:text-iluminac">Cargar</a>
          <a href="/budget" className="font-semibold hover:text-iluminac">Presupuesto</a>
          <a href="/login">
            <i className='hover:text-iluminac'>
              <ArrowLeftEndOnRectangleIcon className="size-6 hover:text-iluminac" />
            </i>
          </a>  
        </div>

        {isOpen && (
          <div className="md:hidden flex text-white space-x-3">
            <a href="/" className="font-semibold hover:text-iluminac">Inicio</a>
            <a href="/load" className="font-semibold hover:text-iluminac">Cargar</a>
            <a href="/budget" className="font-semibold hover:text-iluminac">Presupuesto</a>
            <a href="/login" className="">
              <i className='hover:text-iluminac'>
                <ArrowLeftEndOnRectangleIcon className="size-6 hover:text-iluminac" />
              </i>
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

