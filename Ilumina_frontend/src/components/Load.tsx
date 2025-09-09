import React, { useState, type FormEvent } from 'react';

interface LoadProps {
  title: string;
}

export const Load: React.FC<LoadProps> = ({ title }) => {
  const [message, setMessage] = useState<string>('');
  const [loading, setLoading] = useState(false);

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
    <div className='flex justify-center'>
      <form onSubmit={handleSubmit} className="space-y-3 space-x-4 text-2xl">
        <input className='border rounded-xl text-center' type="file" accept=".xlsx,.xls" name="data" id="data" />
        <button
          type="submit"
          value="Enviar"
          className="px-4 py-2 border rounded cursor-pointer"
        >
          {loading ? 'Cargando archivo a la base de datos...' : 'Enviar'}
        </button>
      </form>
      {message && (
        <div className="mt-4 p-2 rounded bg-gray-100 text-green-700">
          {message}
        </div>
      )}
    </div>
    </>
  );
};
