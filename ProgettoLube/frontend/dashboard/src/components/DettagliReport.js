import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../css/App.css';
import { Modal, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Divider from '@material-ui/core/Divider';


function Dettagli(props) {



    // viene eseguito appena viene caricata la pagina
    useEffect(() => {
        fetchData();
    }, []);

    const [report, setReport] = useState({});
    const [dict_script, setDict_script] = useState({});
    const [dict_keywords_pagine, setDict_keywords_pagine] = useState({});
    const [dict_correttezzalogo, setDict_correttezzalogo] = useState({});
    const [dict_keywords_foto, setDict_keywords_foto] = useState({});
    const [dict_resoconto_logo, setDict_resoconto_logo] = useState({});
    // chiamata fake per richiedere i dati 
    const fetchData = async () => {
        const id = props.match.params.id;
        axios.get(`http://c1d480345a12.ngrok.io/reportsWeb/findOne?id=${id}`)
            .then(res => {
                const report = res.data.lista;
                console.log('Report', report);
                setDict_script(report[0].report_pagine.dictionary_script);
                setDict_keywords_pagine(report[0].report_pagine.dictionary_parolechiave.resoconto);
                setDict_correttezzalogo(report[0].report_foto.correttezza_logo);
                setDict_resoconto_logo(report[0].report_foto.correttezza_logo.logo_correctness);
                setDict_keywords_foto(report[0].report_foto.presenza_keywords_foto.resoconto);
                setReport(report[0]);
            })
    }

    return (
        <div className="AppDettReport">
            <br />
            <div className="Titolo">
                <h2 style={{ fontFamily: "Times New Roman" }} >{report.sito}</h2>
                <h5 style={{ fontFamily: "Times New Roman" }} >REPORT del {report.date}</h5>
            </div>

            <div className="ContainerGriglia">



                <div className="Sezione">
                    <div className="TitoloImpo">
                        <h3 className="Scritta" style={{ fontFamily: "Times New Roman" }}>Presenza Script {report.valutazione_script == 1 ? '🟢' : '🔴'}</h3>
                    </div>
                    <div className="Impostazione3">
                        {
                            Object.entries(dict_script).map(([key, value], i) => (
                                <div className="RigaDettagliScript">
                                    <p key={i}><b style={{ fontSize: 16 }}>{key}</b>  :  {value}
                                    </p>
                                </div>
                            ))

                        }

                    </div>
                </div>
                <div className="Sezione">
                    <div className="TitoloImpo">
                        <h3 className="Scritta" style={{ fontFamily: "Times New Roman" }}>Valutazione Parole Chiave {report.valutazione_keywords >= 2.75 && report.valutazione_keywords <= 3 ? '🔴'
                            : report.valutazione_keywords >= 2 && report.valutazione_keywords < 2.75 ? '🟡'
                                : report.valutazione_keywords >= 1 && report.valutazione_keywords < 2 ? '🟢'
                                    : ''}</h3>
                    </div>
                    <div className="Impostazione3">
                        {
                            Object.entries(dict_keywords_pagine).map(([key, value], i) => (
                                <div className="RigaDettagliScript">
                                    <p key={i}><b style={{ fontSize: 16 }}>{key}</b>  :  {value}
                                    </p>
                                </div>
                            ))

                        }

                    </div>
                </div>

                <div className="Sezione">
                    <div className="TitoloImpo">
                        <h3 className="Scritta" style={{ fontFamily: "Times New Roman" }}>Valutazione Foto {report.valutazione_foto >= 2.75 && report.valutazione_foto <= 3 ? '🔴'
                            : report.valutazione_foto >= 2 && report.valutazione_foto < 2.75 ? '🟡'
                                : report.valutazione_foto >= 1 && report.valutazione_foto < 2 ? '🟢'
                                    : ''}</h3>
                    </div>
                    <p style={{ fontSize: 18 }}><b>{dict_correttezzalogo.foto_trovate} foto totali</b></p>
                    <div className="Impostazione3">
                        {
                            Object.entries(dict_resoconto_logo).map(([key, value], i) => (
                                <div className="RigaDettagliScript">
                                    <p key={i}><b style={{ fontSize: 16 }}>{key}</b>  :  {value}
                                    </p>
                                </div>
                            ))

                        }

                    </div>
                </div>


                <div className="Sezione">
                    <div className="TitoloImpo">
                        <h3 className="Scritta" style={{ fontFamily: "Times New Roman" }}>Parole chiave nelle foto</h3>
                    </div>
                    <div className="Impostazione3">
                        {
                            Object.entries(dict_keywords_foto).map(([key, value], i) => (
                                <div className="RigaDettagliScript">
                                    <p key={i}><b style={{ fontSize: 16 }}>{key}</b>  :  {value}
                                    </p>
                                </div>
                            ))

                        }

                    </div>
                </div>
                
                
            </div>
            



        </div>
    );
}

export default Dettagli;
