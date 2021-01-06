import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import '../css/App.css';
import TextField from "@material-ui/core/TextField";
import DatePicker from 'react-date-picker';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import {
    DataGrid,
    ColDef,
    ValueGetterParams,
    CellParams,
    GridApi
} from "@material-ui/data-grid";

import {Card, Carousel } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
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

    const classes = useStyles();

    

    useEffect(() => {
        // fetchData();
        //fetchPino();
        fetchLastReports();
        
      }, []);


     /* chiamata VERA per richiedere i dati al server */
  
    function feedRow() {
        return reports; 
        //reports;
      }
    
    
    
      function getLastReports() {
        fetchLastReports();
        return null;
      }

  
    const data = props.match.params.name;

    /* Hooks */
    const [posts, setPosts] = useState([]);
    const [storeName, setStoreName] = useState([]);
    const [index, setIndex] = useState(0);
    const [drop, setDrop] = useState([]);
    const [value, setValue] = React.useState();
    const [siti, setSiti] = useState([]);
    const [datatable, setDatatable] = useState({});
    const reports=[];

    var report=[];
    var comune;
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
    const [viewmonth, setViewmonth] = useState(0);

    const fetchLastReports = async () => {
      axios.get(` http://127.0.0.1:5000/resellers/retrieveResellerDetails?name=${props.match.params.name}`)
      // axios.get(`http://localhost:5000/reports/retrieveLastReports`)
      .then(res => {
        report = res.data;
        comune=report.COMUNE["70"];
        console.log(comune);
        
        //report.map()(rep=>reports.push(rep));
      //  setReports(report);
     //   console.log("reports ",reports);
  
        //  const pino = [
          
        //     // { field: 'id', headerName: 'id', width: 200, hide: true },
        //     // { field: 'date', headerName: 'Data', width: 200 },
        //     // { field: 'name', headerName: 'Nome', width: 200 },
        //     // { field: 'valutazione', headerName: 'Valutazione', width: '100%' },
  
        //     { field: 'id', headerName: 'Ragione Sociale'  },
        //     { field: 'INDIRIZZO', headerName: 'Indirizzo'  },
        //     { field: 'valutazione', headerName: 'Valutazione'  },
        //     { field: 'COMUNE', headerName: 'Comune'  },
        //     { field: 'provincia', headerName: 'Provincia'  },
        //     { field: 'tipologia', headerName: 'Tipologia'  },
        //     { field: 'mail', headerName: 'Mail'  },
        //     { field: 'sito', headerName: 'Sito'  },
        //     { field: 'fb', headerName: 'Facebook'  },
        //     { field: 'ig', headerName: 'Instagram'  },
        //   ];
        //   setColumns(pino);
  
        })
  
    }
    /* Variabili */
    const history = useHistory();

    const handleChange = (event) => {
        setChoice(event.target.value);
    };

    // function FormAnnuale() {
    //     return (
    //         <div className="RicercaAnnuale">

                

    //             <div className="InputGroup">

    //                 <Row>
    //                     <Col md={10}>
    //                         <RangeSlider

    //                             step={0.1}
    //                             max={3}
    //                             min={1}
    //                             progress
    //                             style={{ marginTop: 16, marginBottom: 16 }}
    //                             value={range}
    //                             onChange={value => {
    //                                 if (value[0] <= value[1]) {
    //                                     setRange(value);
    //                                     // console.log(range)
    //                                 }
    //                             }}
    //                         />
    //                     </Col>
    //                     <Col md={8}>
    //                         <InputGroup
    //                             style={{ width: 200 }}
    //                         >
    //                             <InputNumber
    //                                 min={1}
    //                                 max={3}
    //                                 value={range[0]}
    //                                 onChange={nextValue => {
    //                                     const [start, end] = range;
    //                                     if (nextValue > end) {
    //                                         return;
    //                                     }
    //                                     setRange([nextValue, end]);
    //                                 }}
    //                             />
    //                             <InputGroup.Addon>to</InputGroup.Addon>
    //                             <InputNumber
    //                                 min={1}
    //                                 max={3}
    //                                 value={range[1]}
    //                                 onChange={nextValue => {
    //                                     const [start, end] = range;
    //                                     if (start > nextValue) {
    //                                         return;
    //                                     }
    //                                     setRange([start, nextValue]);
    //                                 }}
    //                             />
    //                         </InputGroup>
    //                     </Col>
    //                 </Row>
    //             </div>
    //             <YearPicker
    //                 defaultValue={'Seleziona anno'}
    //                 start={2020}
    //                 end={2050}
    //                 required={true}
    //                 value={year}
    //                 onChange={(year) => {
    //                     if (year != NaN) year = parseInt(year);
    //                     setYear(year);
    //                     console.log(year);
    //                 }}
    //                 id={'year'}
    //                 name={'year'}
    //                 classes={'classes'}
    //                 optionClasses={'option classes'}
    //             />

    //             <Button
    //                 // onClick={fetchReportAnnuali()}
    //                 onClick={() => { fetchReportAnnuali() }}
    //                 variant="contained"
    //                 color="primary"
    //                 className={classes.button}
    //                 endIcon={<SearchIcon />}
    //             >
    //                 Send
    //       </Button>

    //         </div>
    //     )

    // }

    // function FormMensile() {
    //     return (
    //         <div className="RicercaAnnuale">

                
    //             <div className="InputGroup">
    //                 <Row>
    //                     <Col md={10}>
    //                         <RangeSlider

    //                             step={0.1}
    //                             max={3}
    //                             min={1}
    //                             progress
    //                             style={{ marginTop: 16, marginBottom: 16 }}
    //                             value={range}
    //                             onChange={value => {
    //                                 if (value[0] <= value[1]) {
    //                                     setRange(value);
    //                                     // console.log(range)
    //                                 }
    //                             }}
    //                         />
    //                     </Col>
    //                     <Col md={8}>
    //                         <InputGroup
    //                             style={{ width: 200 }}
    //                         >
    //                             <InputNumber
    //                                 min={1}
    //                                 max={3}
    //                                 value={range[0]}
    //                                 onChange={nextValue => {
    //                                     const [start, end] = range;
    //                                     if (nextValue > end) {
    //                                         return;
    //                                     }
    //                                     setRange([nextValue, end]);
    //                                 }}
    //                             />
    //                             <InputGroup.Addon>to</InputGroup.Addon>
    //                             <InputNumber
    //                                 min={1}
    //                                 max={3}
    //                                 value={range[1]}
    //                                 onChange={nextValue => {
    //                                     const [start, end] = range;
    //                                     if (start > nextValue) {
    //                                         return;
    //                                     }
    //                                     setRange([start, nextValue]);
    //                                 }}
    //                             />
    //                         </InputGroup>
    //                     </Col>
    //                 </Row>
    //             </div>
    //             <YearPicker
    //                 defaultValue={'Seleziona anno'}
    //                 start={2020}
    //                 end={2050}
    //                 required={true}
    //                 value={year}
    //                 onChange={(year) => {
    //                     if (year != NaN) year = parseInt(year);
    //                     setYear(year);
    //                     console.log(year);
    //                 }}
    //                 id={'year'}
    //                 name={'year'}
    //                 classes={'classes'}
    //                 optionClasses={'option classes'}
    //             />
    //             <MonthPicker
    //                 defaultValue={'Seleziona mese'}
    //                 numeric                   // to get months as numbers
    //                 short                     // default is full name
    //                 caps                      // default is Titlecase
    //                 endYearGiven              // mandatory if end={} is given in YearPicker
    //                 year={year}    // mandatory
    //                 required={true}           // default is false
    //                 // disabled={true}           // default is false
    //                 value={viewmonth}  // mandatory
    //                 onChange={(month) => {    // mandatory
    //                     if (month != NaN) var supp = parseInt(month);
    //                     supp = supp + 1;
    //                     setMonth(supp);
    //                     setViewmonth(month);
    //                     console.log('mese: ', supp);
    //                 }}
    //                 id={'month'}
    //                 name={'month'}
    //                 classes={'classes'}
    //                 optionClasses={'option classes'}
    //             />
    //             <Button
    //                 variant="contained"
    //                 color="primary"
    //                 className={classes.button}
    //                 endIcon={<SearchIcon />}
    //             >
    //                 Send
    //       </Button>

    //         </div>

    //     )

    // }

    // function FormGiornaliero() {
    //     return (
    //         <div className="RicercaAnnuale">

                
    //             <div className="InputGroup">

    //                 <Row>
    //                     <Col md={10}>
    //                         <RangeSlider

    //                             step={0.1}
    //                             max={3}
    //                             min={1}
    //                             progress
    //                             style={{ marginTop: 16, marginBottom: 16 }}
    //                             value={range}
    //                             onChange={value => {
    //                                 if (value[0] <= value[1]) {
    //                                     setRange(value);
    //                                     // console.log(range)
    //                                 }
    //                             }}
    //                         />
    //                     </Col>
    //                     <Col md={8}>
    //                         <InputGroup
    //                             style={{ width: 200 }}
    //                         >
    //                             <InputNumber
    //                                 min={1}
    //                                 max={3}
    //                                 value={range[0]}
    //                                 onChange={nextValue => {
    //                                     const [start, end] = range;
    //                                     if (nextValue > end) {
    //                                         return;
    //                                     }
    //                                     setRange([nextValue, end]);
    //                                 }}
    //                             />
    //                             <InputGroup.Addon>to</InputGroup.Addon>
    //                             <InputNumber
    //                                 min={1}
    //                                 max={3}
    //                                 value={range[1]}
    //                                 onChange={nextValue => {
    //                                     const [start, end] = range;
    //                                     if (start > nextValue) {
    //                                         return;
    //                                     }
    //                                     setRange([start, nextValue]);
    //                                 }}
    //                             />
    //                         </InputGroup>
    //                     </Col>
    //                 </Row>
    //             </div>
    //             <DatePicker
    //                 onChange={setDate}
    //                 value={date}
    //             />
    //             <Button
    //                 variant="contained"
    //                 color="primary"
    //                 className={classes.button}
    //                 endIcon={<SearchIcon />}
    //             >
    //                 Send
    //       </Button>

    //         </div>)
    // }
    const prova = [
        { field: 'id', headerName: 'Ragione Sociale', width: 200, },
        { field: 'address', headerName: 'Indirizzo', width: 200 },
        { field: 'valutazione', headerName: 'Valutazione', width: '100%' },
 
        
      ];

    return (
        <div className="App">
            <h1>DETTAGLI {data}</h1>

            {/* <div className="Titolo">
        <h3>HOME</h3>
      </div> */}

            {/* VECCHIO
      posts.map(post => (
        <Link key={post.id} to={`/${post.id}`}>
          <h4 key={post.id} >{post.title}</h4>
        </Link>
      )) */}

            {/*  , giorno , anno, mese , range valutazione(tra 1 e 3) */}

            <div className="Container">

                {/* <Carousel activeIndex={index} onSelect={handleSelect} interval={null}>

  <Carousel.Item> */}

                {/* <div className={button ? 'Ricerca' : 'RicercaHidden'} > */}
                    {/* <h4 style={{ letterSpacing: 5 }}>SITI WEB</h4> */}

                    {/* {choice == 'Report annuali' ?
                        <FormAnnuale /> : choice == 'Report mensili' ?
                            <FormMensile /> : choice == 'Report giornalieri' ?
                                <FormGiornaliero /> : getLastReports()}

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
                            <MenuItem value={'Last reports'}>Ultimi Report</MenuItem>
                        </Select>
                    </FormControl>
                </div> */}

                <br />
                {/*<div className="ContainerTabella">
                    <div className="Tabella"> */}
                        {/*console.log('datatable', datatable)*/}
                        {/*  <MDBDataTableV5 hover entriesOptions={[5, 20, 25]}
          entries={5} pagesAmount={4} data={datatable} />*/}
                        {/* <DataGrid rows={feedRow()} columns={columns} /> */}
                        <div className="cardsContainer">
                          
  <Card style={{ width: '20vh', height:"30vh", marginTop:5, marginBottom:5, marginLeft:5, marginRight:5, }}>
  <Card.Body>
    <Card.Title>{comune}</Card.Title>
    <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
    <Card.Text>
      Some quick example text to build on the card title and make up the bulk of
      the card's content.
    </Card.Text>
    <Card.Link href="#">Card Link</Card.Link>
    <Card.Link href="#">Another Link</Card.Link>
  </Card.Body>
</Card>

<Card style={{  width: '20vh', height:"30vh", marginTop:5, marginBottom:5, marginLeft:5, marginRight:5, }}>
 <Card.Body>
    <Card.Title>Card Title</Card.Title>
    <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
    <Card.Text>
      Some quick example text to build on the card title and make up the bulk of
      the card's content.
    </Card.Text>
    <Card.Link href="#">Card Link</Card.Link>
    <Card.Link href="#">Another Link</Card.Link>
  </Card.Body>
</Card>

<Card style={{  width: '20vh', height:"30vh", marginTop:5, marginBottom:5, marginLeft:5, marginRight:5,  }}>
  <Card.Body>
    <Card.Title>Card Title</Card.Title>
    <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
    <Card.Text>
      Some quick example text to build on the card title and make up the bulk of
      the card's content.
    </Card.Text>
    <Card.Link href="#">Card Link</Card.Link>
    <Card.Link href="#">Another Link</Card.Link>
  </Card.Body>
</Card>

<Card style={{  width: '20vh', height:"30vh", marginTop:5, marginBottom:5, marginLeft:5, marginRight:5, }}>
 <Card.Body>
    <Card.Title>Card Title</Card.Title>
    <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
    <Card.Text>
      Some quick example text to build on the card title and make up the bulk of
      the card's content.
    </Card.Text>
    <Card.Link href="#">Card Link</Card.Link>
    <Card.Link href="#">Another Link</Card.Link>
  </Card.Body>
</Card>
</div>
                    {/* </div>
                </div> */}
                {/* </Carousel.Item> */}

                {/* <Carousel.Item>*/}
                {/* <h4 style={{ letterSpacing: 5 }}>PROFILI SOCIAL</h4> */}
                {/* <br />
    <div className="ContainerTabella">
      <div className="Tabella"> */}
                {/* <DataGrid rows={siti} columns={columns} /> */}
                {/* </div>
    </div> */}

                {/* </Carousel.Item>
</Carousel>   */}
            </div>
        </div>
    );
}

export default Store;