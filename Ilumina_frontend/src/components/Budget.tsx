import React from "react";
import {type FormEvent} from 'react';

interface BudgetProps {
  title: string;
}

export const Budget: React.FC<BudgetProps> = ({ title }) => {

    const handleSubmit = async (e:FormEvent) => {
        e.preventDefault();
        const response = await 
        fetch("http://localhost:8000/api/show_file", {
            method: "GET",
            }
        );
        if(response.ok){
            const jsonData = await response.json();
            //@ts-expect-error no table
            const table = new Tabulator('#table', {
                data: jsonData,
                nestedFieldSeparator: false,
                autoColumns: true
                }
            )
            console.log(table)
        }
    }
  return (
    <div className="flex-col pt-4 pb-4">
        <p>{title}</p>
        <p className="text-4xl text-ilumina text-center">Presupuestación</p>
        <div className="flex justify-center">
            <form onSubmit={handleSubmit} className='text-2xl pt-4 pb-4'>
                <button className="rounded-2xl bg-ilumina text-white font-semibold px-3 py-2" type="submit">Generar Presupuesto</button>
            </form>
        </div>
        <div className="flex justify-center">
            <div className="w-8xl h-120 mx-4" id="table"/>
        </div>
    </div>

    )
};