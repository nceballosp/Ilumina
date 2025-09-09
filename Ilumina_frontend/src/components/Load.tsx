import React, { useState, type FormEvent } from 'react';
import { DocumentIcon } from '@heroicons/react/24/solid';

interface LoadProps {
  title: string;
}

export const Load: React.FC<LoadProps> = ({ title }) => {
  const [message, setMessage] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [name, setName] = useState<string | undefined>('Cargar Archivo')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    setName(file?.name);
  };


  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const fileInput = document.querySelector('#data') as HTMLInputElement;
    if (!fileInput.files || fileInput.files.length === 0) {
      alert('Por favor selecciona un archivo antes de enviar.');
      return;
    }

    const formData = new FormData();
    formData.append('data', fileInput.files[0]);

    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/api/read_file', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const json = await response.json();
        setMessage(json.detail ?? 'Archivo cargado correctamente ✅');
      } else {
        setMessage(`Error al cargar archivo (status ${response.status})`);
      }
    } catch (err) {
      console.log(err);
      setMessage('Error de red o servidor no disponible');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
    {title}
    <div className='flex justify-center bg-iluminab max-w-full min-h-screen'>
      <div>
        <form onSubmit={handleSubmit} className="flex space-x-4 text-2xl pt-10">
          <label className="flex justify-center items-center border rounded-2xl p-3 font-medium text-white cursor-pointer" htmlFor="data">
            <DocumentIcon className='text-white size-10'/>
            <p className="px-2">{name}</p>
            </label>
          <input className="hidden w-100 text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50" id="data" name='data' type="file" onChange={handleChange}/>
          <button
            type="submit"
            value="Enviar"
            className="px-4 py-2 text-white font-semibold bg-iluminac rounded-2xl cursor-pointer"
          >
            {loading ? 'Cargando archivo a la base de datos...' : 'Enviar'}
          </button>
        </form>
        <div>
          {message && (
            <div className="mt-4 p-2 rounded bg-white text-green-700">
              {message}
            </div>
          )}
        </div>
      </div>
    </div>
    </>
  );
};
