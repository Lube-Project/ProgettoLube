import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import '../css/App.css';
import axios from 'axios';
import { Card } from 'react-bootstrap';

import { makeStyles } from '@material-ui/core/styles';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import { SocialIcon } from 'react-social-icons';
import LanguageIcon from '@material-ui/icons/Language';



import TextField from "@material-ui/core/TextField";
import DatePicker from 'react-date-picker';
import {
    DataGrid,
    ColDef,
    ValueGetterParams,
    CellParams,
    GridApi
} from "@material-ui/data-grid";

import { Carousel } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import Autocomplete from '@material-ui/lab/Autocomplete';
//import { MDBDataTableV5 } from 'mdbreact';
//import DatePicker from 'react-datepicker';
//import "react-datepicker/dist/react-datepicker.css";
import { YearPicker, MonthPicker, DayPicker } from 'react-dropdown-date';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import SearchIcon from '@material-ui/icons/Search';
import { Slider, RangeSlider, InputNumber, InputGroup, Row, Col } from 'rsuite';
import 'rsuite/dist/styles/rsuite-default.css';


const useStyles = makeStyles((theme) => ({
    root: {
        minWidth: 275,
    },
    bullet: {
        display: 'inline-block',
        margin: '0 2px',
        transform: 'scale(0.8)',
    },
    title: {
        fontSize: 14,
    },
    pos: {
        marginBottom: 12,
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    root: {
        width: 300,
    },
    button: {
        margin: theme.spacing(1),
    },

}));

function Store(props) {

    const data = props.match.params.name;


    const classes = useStyles();
    const bull = <span className={classes.bullet}>•</span>;



    useEffect(() => {
        fetchResellerDetails();
    }, []);

    /* carosello */
    const handleSelect = (selectedIndex, e) => {
        setIndex(selectedIndex);
    };

    /*
    Hooks
    */
    const [storeDetails, setStoreDetails] = useState([]);
    const [reports, setReports] = useState([]);
    const [grid, setGrid] = useState(false);

    const [posts, setPosts] = useState([]);
    const [storeName, setStoreName] = useState([]);
    const [index, setIndex] = useState(0);
    const [drop, setDrop] = useState([]);
    const [value, setValue] = React.useState();
    const [siti, setSiti] = useState([]);
    const [datatable, setDatatable] = useState({});


    //const [reports, setReports] = useState([]);
    const [choice, setChoice] = React.useState('');
    const [date, setDate] = useState(new Date());
    const [range, setRange] = useState([1, 3]);
    const [columns, setColumns] = useState([]);

    const [click, setClick] = useState(false);
    const [button, setButton] = useState(true);



    const [name, setName] = useState(0);

    const [year, setYear] = useState(0);
    const [month, setMonth] = useState(0);
    const [viewmonth, setViewmonth] = useState();

    const showButton = () => {
        if (window.innerWidth <= 960) {
            setButton(false);
        } else {
            setButton(true);
        }
    }

    window.addEventListener("resize", showButton);


    const fetchResellerDetails = async () => {
        axios.get(` http://127.0.0.1:5000/resellers/retrieveResellerDetails?name=${data}`)
            .then(res => {
                const response = res.data;

                //comune = report.COMUNE["70"];
                setStoreDetails(response);


            })

    }

    const handleChange = (event) => {
        setChoice(event.target.value);
    };

    function getReportAnnuali() {
        var ciccio = "Pratola Peligna";
        const pino = [
            { field: 'id', headerName: 'Name', width: 400, },
            { field: 'year', headerName: 'Anno', width: 400 },
            { field: 'valutazione', headerName: 'Valutazione', width: '100%' },
        ];
        //waiting for backy
        axios.get(`http://localhost:5000/reports/retrieveYearAverageName?year=${year}&name=${data}&range1=${range[0]}&range2=${range[1]}`)
            .then(res => {
                const response = res.data.lista;
                console.log(response);
                setReports(response);
            });
        setColumns(pino);
        //setGrid(true);
        return null;

    }

    function getReportMensile() {
        //non ha selezionato il nome dello store
        console.log(month);
        const pino = [
            { field: 'id', headerName: 'Name', width: 400, },
            { field: 'year', headerName: 'Anno', width: 400 },
            { field: 'month', headerName: 'Mese', width: 400 },
            { field: 'valutazione', headerName: 'Valutazione', width: '100%' },
        ];

        axios.get(`http://localhost:5000/reports/retrieveMonthYearAverageName?year=${year}&month=${month}&name=${data}&range1=${range[0]}&range2=${range[1]}`)
            .then(res => {
                const reports = res.data.lista;
                setReports(reports);
            });
        setColumns(pino);
        return null;


    }

    function getReportDate() {
        
    const pino = [
        { field: 'id', headerName: 'Name', width: 350, },
        { field: 'year', headerName: 'Anno', width: 250 },
        { field: 'month', headerName: 'Mese', width: 250 },
        { field: 'day', headerName: 'Giorno', width: 250 },
        { field: 'valutazione', headerName: 'Valutazione', width: '100%' },
      ];
     
        axios.get(`http://localhost:5000/reports/retrieveDayMonthYearName?year=${date.getFullYear()}&month=${date.getMonth()+1}&day=${date.getDate()}&name=${data}&range1=${range[0]}&range2=${range[1]}`)
          .then(res => {
            const reports = res.data.lista;
            setReports(reports);
          });
        setColumns(pino);
        return null;
      

    }
    function FormAnnuale() {
        return (
            <div className="RicercaAnnuale">



                <div className="InputGroup">

                    <Row>
                        <Col md={10}>
                            <RangeSlider

                                step={0.1}
                                max={3}
                                min={1}
                                progress
                                style={{ marginTop: 16, marginBottom: 16 }}
                                value={range}
                                onChange={value => {
                                    if (value[0] <= value[1]) {
                                        setRange(value);
                                        // console.log(range)
                                    }
                                }}
                            />
                        </Col>
                        <Col md={8}>
                            <InputGroup
                                style={{ width: 200 }}
                            >
                                <InputNumber
                                    min={1}
                                    max={3}
                                    value={range[0]}
                                    onChange={nextValue => {
                                        const [start, end] = range;
                                        if (nextValue > end) {
                                            return;
                                        }
                                        setRange([nextValue, end]);
                                    }}
                                />
                                <InputGroup.Addon>to</InputGroup.Addon>
                                <InputNumber
                                    min={1}
                                    max={3}
                                    value={range[1]}
                                    onChange={nextValue => {
                                        const [start, end] = range;
                                        if (start > nextValue) {
                                            return;
                                        }
                                        setRange([start, nextValue]);
                                    }}
                                />
                            </InputGroup>
                        </Col>
                    </Row>
                </div>
                <YearPicker
                    defaultValue={'Seleziona anno'}
                    start={2020}
                    end={2050}
                    required={true}
                    value={year}
                    onChange={(year) => {
                        if (year != NaN) year = parseInt(year);
                        setYear(year);
                        console.log(year);
                    }}
                    id={'year'}
                    name={'year'}
                    classes={'classes'}
                    optionClasses={'option classes'}
                />

                <Button
                    // onClick={fetchReportAnnuali()}
                    onClick={() => { getReportAnnuali() }}
                    variant="contained"
                    color="primary"
                    className={classes.button}
                    endIcon={<SearchIcon />}
                >
                    Send
          </Button>

            </div>
        )

    }

    function FormMensile() {
        return (
            <div className="RicercaAnnuale">


                <div className="InputGroup">
                    <Row>
                        <Col md={10}>
                            <RangeSlider

                                step={0.1}
                                max={3}
                                min={1}
                                progress
                                style={{ marginTop: 16, marginBottom: 16 }}
                                value={range}
                                onChange={value => {
                                    if (value[0] <= value[1]) {
                                        setRange(value);
                                        // console.log(range)
                                    }
                                }}
                            />
                        </Col>
                        <Col md={8}>
                            <InputGroup
                                style={{ width: 200 }}
                            >
                                <InputNumber
                                    min={1}
                                    max={3}
                                    value={range[0]}
                                    onChange={nextValue => {
                                        const [start, end] = range;
                                        if (nextValue > end) {
                                            return;
                                        }
                                        setRange([nextValue, end]);
                                    }}
                                />
                                <InputGroup.Addon>to</InputGroup.Addon>
                                <InputNumber
                                    min={1}
                                    max={3}
                                    value={range[1]}
                                    onChange={nextValue => {
                                        const [start, end] = range;
                                        if (start > nextValue) {
                                            return;
                                        }
                                        setRange([start, nextValue]);
                                    }}
                                />
                            </InputGroup>
                        </Col>
                    </Row>
                </div>
                <YearPicker
                    defaultValue={'Seleziona anno'}
                    start={2020}
                    end={2050}
                    required={true}
                    value={year}
                    onChange={(year) => {
                        if (year != NaN) year = parseInt(year);
                        setYear(year);
                        console.log(year);
                    }}
                    id={'year'}
                    name={'year'}
                    classes={'classes'}
                    optionClasses={'option classes'}
                />
                <MonthPicker
                    defaultValue={'Seleziona mese'}
                    numeric                   // to get months as numbers
                    short                     // default is full name
                    caps                      // default is Titlecase
                    endYearGiven              // mandatory if end={} is given in YearPicker
                    year={year}    // mandatory
                    required={true}           // default is false
                    // disabled={true}           // default is false
                    value={viewmonth}  // mandatory
                    onChange={(month) => {    // mandatory
                        if (month != NaN) var supp = parseInt(month);
                        supp = supp + 1;
                        setMonth(supp);
                        setViewmonth(month);
                        console.log('mese: ', supp);
                    }}
                    id={'month'}
                    name={'month'}
                    classes={'classes'}
                    optionClasses={'option classes'}
                />
                <Button
                    onClick={() => { getReportMensile() }}
                    variant="contained"
                    color="primary"
                    className={classes.button}
                    endIcon={<SearchIcon />}
                >
                    Send
          </Button>

            </div>

        )

    }

    function FormGiornaliero() {
        return (
            <div className="RicercaAnnuale">


                <div className="InputGroup">

                    <Row>
                        <Col md={10}>
                            <RangeSlider

                                step={0.1}
                                max={3}
                                min={1}
                                progress
                                style={{ marginTop: 16, marginBottom: 16 }}
                                value={range}
                                onChange={value => {
                                    if (value[0] <= value[1]) {
                                        setRange(value);
                                        // console.log(range)
                                    }
                                }}
                            />
                        </Col>
                        <Col md={8}>
                            <InputGroup
                                style={{ width: 200 }}
                            >
                                <InputNumber
                                    min={1}
                                    max={3}
                                    value={range[0]}
                                    onChange={nextValue => {
                                        const [start, end] = range;
                                        if (nextValue > end) {
                                            return;
                                        }
                                        setRange([nextValue, end]);
                                    }}
                                />
                                <InputGroup.Addon>to</InputGroup.Addon>
                                <InputNumber
                                    min={1}
                                    max={3}
                                    value={range[1]}
                                    onChange={nextValue => {
                                        const [start, end] = range;
                                        if (start > nextValue) {
                                            return;
                                        }
                                        setRange([start, nextValue]);
                                    }}
                                />
                            </InputGroup>
                        </Col>
                    </Row>
                </div>
                <DatePicker
                    onChange={setDate}
                    value={date}
                />
                <Button
                    onClick={() => { getReportDate() }}
                    variant="contained"
                    color="primary"
                    className={classes.button}
                    endIcon={<SearchIcon />}
                >
                    Send
          </Button>

            </div>)
    }


    return (
        <div className="App">
            <div className="Titolo">
                <h2>DETTAGLI {data}</h2>
            </div>
            <div className={button ? 'Ricerca' : 'RicercaHidden'} >
                {choice == 'Report annuali' ?
                    <FormAnnuale /> : choice == 'Report mensili' ?
                        <FormMensile /> : choice == 'Report giornalieri' ?
                            <FormGiornaliero /> : null}

                <FormControl className={classes.formControl}   >

                    <InputLabel id="demo-simple-select-disabled-label">Ultimi Report</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={choice}
                        onChange={handleChange}
                        placeholder={choice}


                    >
                        <MenuItem value={'Report annuali'}>Report annuali</MenuItem>
                        <MenuItem value={'Report mensili'}>Report mensili</MenuItem>
                        <MenuItem value={'Report giornalieri'}>Report giornalieri</MenuItem>
                    </Select>
                </FormControl>
            </div>
            <div className="ContainerTabella">
                <div className="Tabella">
                    <DataGrid rows={reports} columns={columns} />
                </div>
            </div>

            {/* <div className="Container"> */}

            <div className="cardsContainer">

                <Card className={classes.root} variant="outlined" style={{ position: "relative", width: 'auto', height: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5 }}>
                    <CardContent >
                        <Typography variant="h5" component="h2">
                            TIPOLOGIA: <br /> {storeDetails.TIPOLOGIA}

                        </Typography>
                        <Typography className={classes.title} color="textSecondary" gutterBottom>
                            ID NEGOZIO: {storeDetails.IDNEGOZIO}
                        </Typography>
                        {/* <Typography className={classes.pos} color="textSecondary">
                                adjective
        </Typography> */}
                        <Typography variant="body2" component="p">
                            <br /> RAGIONE SOCIALE:   {storeDetails["RAGIONE SOCIALE"]}
                            <br /> DESAGE: {storeDetails.DESAGE}
                            <br />  BRAND LUBE: {storeDetails["BRAND LUBE"]}
                            <br />  BRAND CREO: {storeDetails["BRAND CREO"]}
                        </Typography>
                    </CardContent>

                </Card>
                <Card className={classes.root} variant="outlined" style={{ position: "relative", width: 'auto', height: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5, }}>
                    <CardContent>

                        <Typography variant="h5" component="h2">
                            LOCAZIONE: <br /> {storeDetails.COMUNE}
                        </Typography>
                        <Typography className={classes.pos} color="textSecondary">
                            {storeDetails.INDIRIZZO}
                        </Typography>
                        <Typography variant="body2" component="p">
                            PROVINCIA: ({storeDetails.PROV})
                            <br />
                            {storeDetails.CAP}


                        </Typography>
                    </CardContent>

                </Card>
                <Card className={classes.root} variant="outlined" style={{ position: "relative", width: 'auto', height: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5, }}>
                    <CardContent>
                        <Typography variant="h5" component="h2">
                            SOCIAL
        </Typography>

                        <Typography variant="body2" component="p">
                            <br />   {storeDetails.FB ? <SocialIcon url={storeDetails.FB} /> : null} <br />
                            <br />   {storeDetails.ISTAGRAM ? <SocialIcon url={storeDetails.ISTAGRAM} /> : null} <br />
                            <br /> {storeDetails.SITO ? <a href={storeDetails.SITO}><LanguageIcon style={{ fontSize: 53 }}></LanguageIcon></a> : null}

                        </Typography>
                    </CardContent>

                </Card>
                <Card className={classes.root} variant="outlined" style={{ position: "relative", width: 'auto', height: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5, }}>
                    <CardContent>

                        <Typography variant="h5" component="h2">
                            CONTATTI
        </Typography>
                        <Typography className={classes.pos} color="textSecondary">
                            <br />  <SocialIcon url="http://whatsapp.com" /> <br />{storeDetails.Whatsapp}
                        </Typography>
                        <Typography variant="body2" component="p">
                            <br />   <SocialIcon url="mailto:" /> <br />{storeDetails["Mail 1"]}
                            <br /><br />  <SocialIcon url="mailto:" /> <br />{storeDetails["MAIL 2"]}

                        </Typography>
                    </CardContent>

                </Card>


                {/* <Card style={{ width: '20vh', maxHeight: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5, }}>
                        <Card.Body>
                            <Card.Title>INDIRIZZO</Card.Title>
                            <Card.Text>
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                          
                            
                            </Card.Text>
                           
                        </Card.Body>
                    </Card>
                    <Card style={{ width: '20vh', maxHeight: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5, }}>
                        <Card.Body>
                            <Card.Title>INDIRIZZO</Card.Title>
                            <Card.Text>
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                          
                            
                            </Card.Text>
                           
                        </Card.Body>
                    </Card>
                    <Card style={{ width: '20vh', maxHeight: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5, }}>
                        <Card.Body>
                            <Card.Title>INDIRIZZO</Card.Title>
                            <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
                            <Card.Text>
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                          
                            
                            </Card.Text>
                           
                        </Card.Body>
                    </Card>
                    <Card style={{ width: '20vh', maxHeight: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5, }}>
                        <Card.Body>
                            <Card.Title>INDIRIZZO</Card.Title>
                            <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
                            <Card.Text>
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                          
                            
                            </Card.Text>
                           
                        </Card.Body>
                    </Card>
                    <Card style={{ width: '20vh', maxHeight: "auto", marginTop: 5, marginBottom: 5, marginLeft: 5, marginRight: 5, }}>
                        <Card.Body>
                            <Card.Title>INDIRIZZO</Card.Title>
                            <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
                            <Card.Text>
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                            FALCONARA MARITTIMA , VIA N. BIXIO, 112, "AN", 60015
                          
                            
                            </Card.Text>
                           
                        </Card.Body>
                    </Card> */}
            </div>


            {/* </div> */}
        </div>
    );
}
export default Store;