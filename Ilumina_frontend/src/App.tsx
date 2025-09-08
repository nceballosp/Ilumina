import './App.css'
import {type FormEvent} from 'react';


function App() {

    const handleSubmit = async (e:FormEvent) => {
        e.preventDefault();
        let file = document.querySelector('#data') as HTMLInputElement;
        if (!file.files || file.files.length === 0) {
            alert("Please select a file before submitting.");
            return;
        }

        const formData = new FormData();
        formData.append('data',file.files[0])
        const response = await 
        fetch("http://localhost:8000/api/read_file", {
            method: "POST",
            
            body: formData,

            }
        );
        if(response.ok){
            const jsonData = await response.json();
            //@ts-ignore
            const table = new Tabulator('#table',{
                data: jsonData,
                nestedFieldSeparator: false,
                autoColumns: true
            }
            )
        }
    }
    return (
    <>
    <form onSubmit={handleSubmit}>
        <input type="file"  accept='xlsx' name='data' id='data'/>
        <input type="submit" value="Enviar" />
    </form>
    <div id="table" style={{width:'80vw', height: '80vh'}}></div>
    


    </>
  )
}

export default App
