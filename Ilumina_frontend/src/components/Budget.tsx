import React from "react";
import {type FormEvent,useRef} from 'react';

interface BudgetProps {
  title: string;
}

export const Budget: React.FC<BudgetProps> = ({ title }) => {
    // @ts-ignore
    const tabla = useRef<any>(null);
    const handleSubmit = async (e:FormEvent) => {
        e.preventDefault();
        let ipcInput = document.querySelector('#ipc') as HTMLInputElement;
        let ipc = ipcInput ? parseFloat(ipcInput.value) : NaN;
        if (!ipc){
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
            let table = new Tabulator('#table', {
                data: jsonData,
                nestedFieldSeparator: false,
                autoColumns: true,
                }
            )
            table.on('tableBuilt',()=>{
                const allCols = table.getColumns();
                    //@ts-expect-error
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
                        //@ts-expect-error
                        let fila = cell.getRow().getData();
                        console.log(fila);
                        }
                    });
                });
                // Variable para debug en consola
                //@ts-ignore
                window.table = table;
                tabla.current = table
                
            })
        }
    }
  return (
    <div className="flex-col pt-4 pb-4">
        <p>{title}</p>
        <p className="text-4xl text-ilumina text-center">Presupuestación</p>
        <div className="flex justify-center">
            <form onSubmit={handleSubmit} className='text-2xl pt-4 pb-4 flex justify-center w-full gap-4'>
                <input type="number" name="ipc" id="ipc" placeholder="Ingrese IPC" step='any'/>
                <button className="rounded-2xl bg-ilumina text-white font-semibold px-3 py-2" type="submit">Generar Presupuesto</button>
            <button onClick={() => tabla.current ? tabla.current.download('xlsx', 'Presupuesto.xlsx') : alert('No hay tabla para exportar')} className="rounded-2xl bg-ilumina px-3 py-2 text-white font-semibold p-2">Exportar</button>
            </form>

        </div>
        <div className="flex justify-center">
            <div className="w-8xl h-120 mx-4" id="table"/>
        </div>
    </div>

    )
};