import logo from '../assets/3.svg'

export function NavBar() {

  return (
  <nav className="bg-ilumina border-b border-gray-200 px-4 py-4">
    <div className="max-w-7xl mx-auto flex items-center justify-between">
      
      {/* Logo */}
      <div className="text-xl font-bold text-ilumina">
        <a href="/">
          <img className="w-10"src={logo} alt="" />
        </a>
      </div>

      {/* Navegación - Escritorio */}
      <div className="hidden md:flex space-x-6 text-white">
        <a href="/" className="font-semibold hover:underline">Inicio</a>
        <a href="/load" className="font-semibold hover:underline">Cargar</a>
        <a href="/budget" className="font-semibold hover:underline">Generar Presupuesto</a>
      </div>

      {/* Botón */}
      <div className="hidden md:block">
        <a href="/register" className="bg-white text-ilumina font-semibold px-4 py-2 rounded hover:opacity-90">
          Login
        </a>
      </div>

      {/* Menú mobile */}
      <div className="md:hidden">
        <button className="text-gray-600 hover:text-ilumina focus:outline-none">
          {/* Ícono hamburguesa (usa Heroicons o SVG) */}
          <svg className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="2"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round"
                  d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
      </div>
    </div>

    {/* Menú desplegable mobile (puedes controlarlo con estado React si quieres funcionalidad) */}
      <div className="md:hidden space-x-6 text-white">
        <a href="/" className="font-semibold hover:underline">Inicio</a>
        <a href="/load" className="font-semibold hover:underline">Cargar</a>
        <a href="/budget" className="font-semibold hover:underline">Generar Presupuesto</a>
        <a href="/register" className="bg-white text-ilumina font-semibold px-4 py-2 rounded hover:opacity-90">
          Login
        </a>
      </div>
  </nav>

  )
};