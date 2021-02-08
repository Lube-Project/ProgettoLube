import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../css/App.css';
import { Modal, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


function Dettagli(props) {

    const [modalShow, setModalShow] = React.useState(false);

    function MyVerticallyCenteredModal(props) {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
                animation={false}
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        TITOLO
              </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Sottotitolo</h4>
                    <p>
                        Cras mattis consectetur purus sit amet fermentum. Cras justo odio,
                        dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta ac
                        consectetur ac, vestibulum at eros.
              </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    // viene eseguito appena viene caricata la pagina
    useEffect(() => {
        fetchData();
    }, []);

    const [report, setReport] = useState({});

    // chiamata fake per richiedere i dati 
    const fetchData = async () => {
        const id = props.match.params.id;
        axios.get(`http://377d9b605ad4.ngrok.io/reports/findOne?id=${id}`)
            .then(res => {
                const report = res.data.lista;
                console.log('Report', report);
                setReport(report[0]);
            })
    }

    return (
        <div className="AppDettReport">

            <div className="Titolo">
                <h1>{report.name}</h1>
                <h3>REPORT del {report.date}</h3>
            </div>

            <div className="ContainerGriglia">

                <div className="CardDR" onClick={() => setModalShow(true)}>
                    <h3>script</h3>
                    <h4>si / no</h4>
                </div>
                <div className="CardDR" onClick={() => setModalShow(true)}>
                    <h3>parole chiave</h3>
                    <h4>si / no</h4>
                </div>
                <div className="CardDR" onClick={() => setModalShow(true)}>
                    <h3>valutazione</h3>
                    <h4>{report.valutazione}</h4>
                </div>
                <div className="CardDR" onClick={() => setModalShow(true)}>
                    <h3>correttezza logo</h3>
                    <h4>si / no</h4>
                </div>
                <div className="CardDR" onClick={() => setModalShow(true)}>
                    <h3>competitors</h3>
                    <h4>si / no</h4>
                </div>
                <div className="CardDR" onClick={() => setModalShow(true)}>
                    <h3>parole nelle foto</h3>
                    <h4>si / no</h4>
                </div>
            </div>

            <MyVerticallyCenteredModal
                show={modalShow}
                onHide={() => setModalShow(false)}
            />

        </div>
    );
}

export default Dettagli;
