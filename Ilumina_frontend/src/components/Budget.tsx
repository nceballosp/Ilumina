import React from "react";
import {type FormEvent} from 'react';

interface BudgetProps {
  title: string;
}

export const Budget: React.FC<BudgetProps> = ({ title }) => {
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
            let tabla = new Tabulator('#table', {
                data: jsonData,
                nestedFieldSeparator: false,
                autoColumns: true,
                }
            )
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
            </form>
        </div>
        <div className="flex justify-center">
            <div className="w-8xl h-120 mx-4" id="table"/>
        </div>
    </div>

    )
};