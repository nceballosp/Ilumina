import React from 'react';
import { type FormEvent, useRef } from 'react';

interface BudgetProps {
  title: string;
}

export const Budget: React.FC<BudgetProps> = ({ title }) => {
    const tabla = useRef<any>(null);
    const handleSubmit = async (e:FormEvent) => {
        e.preventDefault();
        const ipcInput = document.querySelector('#ipc') as HTMLInputElement;
        const ipc = ipcInput ? parseFloat(ipcInput.value) : NaN;
        if (!ipc && !tabla){
            alert('IPC no puede ser vacio');
            return;
        }
        const response = await 
        fetch(`http://localhost:8000/api/show_file?ipc=${ipc}`, {
            method: "GET",
            }
        );
        if(response.ok){
            const jsonData = await response.json();
            //@ts-expect-error no table
            const table = new Tabulator('#table', {
                data: jsonData,
                nestedFieldSeparator: false,
                autoColumns: true,
                }
            )
            table.on('tableBuilt',()=>{
                const allCols = table.getColumns();
                    //@ts-expect-error cols
                allCols.slice(4).forEach(col => {
                    col.updateDefinition({
                        editor:'number',
                        formatter: "money",
                            formatterParams: {
                            thousand: ".",
                            decimal: ",",
                            precision: 0,
                            },
                        cellEdited:(cell:object)=>{
                        //fila
                        //@ts-expect-error no fila
                        const fila = cell.getRow().getData();
                        console.log(fila);
                        }
                    });
                });
                // Variable para debug en consola
                //@ts-expect-error debug
                window.table = table;
                tabla.current = table
                
            })
        }
    }
    return (
      <div className="flex-col pt-4 pb-4 bg-iluminab max-w-full min-h-screen">    
        <p className='hidden md:hidden'>{title}</p>
        <p className="text-4xl font-semibold text-white text-center pt-10">PRESUPUESTACIÓN</p>
        <div className="flex justify-center">
          <form
            onSubmit={handleSubmit}
            className="flex text-2xl pt-4 pb-4 justify-center items-center gap-6 min-w-full"
          >
            <input
              className='rounded-2xl text-black font-semibold border-ilumina px-3 py-2 w-50'
              type="number"
              name="ipc"
              id="ipc"
              placeholder="Ingrese IPC"
              step="any"
            />
            <button
              className="rounded-2xl bg-iluminac text-white font-semibold px-3 py-2 w-50 cursor-pointer"
              type="submit"
            >
              Generar
            </button>
            <button
              onClick={() =>
                tabla.current
                  ? tabla.current.download('xlsx', 'Presupuesto.xlsx')
                  : alert('No hay tabla para exportar')
              }
              className="rounded-2xl bg-iluminac text-white font-semibold px-3 py-2 w-50 cursor-pointer"
            >
              Exportar
            </button>
          </form>
        </div>
        <div className="flex justify-center">
          <div className="w-8xl h-120 mx-4" id="table" />
        </div>
      </div>
    );
  };
