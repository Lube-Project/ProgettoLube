import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../css/App.css';

function Dettagli(props) {

    // viene eseguito appena viene caricata la pagina
    useEffect(() => {
        fetchData();
    }, []);

    const [report, setReport] = useState({});

    // chiamata fake per richiedere i dati 
    const fetchData = async () => {
        const id = props.match.params.id;
        axios.get(`http://localhost:5000/reports/findOne?id=${id}`)
    .then(res => {
      const report = res.data.lista;
      console.log(report);
      setReport(report[0]);
    })  
    }

    return (
        <div className="App">

            <h1>{report.name}</h1>
            <h3>{report.id}</h3>
            <h3>{report.date}</h3>
            <h2>report :</h2>
            <h3>{report.valutazione}</h3>

        </div>
    );
}

export default Dettagli;
