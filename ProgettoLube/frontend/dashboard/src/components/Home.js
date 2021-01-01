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

import { Carousel } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
//import { MDBDataTableV5 } from 'mdbreact';
//import DatePicker from 'react-datepicker';
//import "react-datepicker/dist/react-datepicker.css";
import { YearPicker, MonthPicker, DayPicker } from 'react-dropdown-date';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import SearchIcon from '@material-ui/icons/Search';


const useStyles = makeStyles((theme) => ({
  button: {
    margin: theme.spacing(1),
  },
}));

function Home() {

  const classes = useStyles();


  /* codice eseguito all'avvio della pagina */
  useEffect(() => {
    // fetchData();
    //fetchPino();
    fetchLastReports();
    fetchResellerNames();
  }, []);



  /* chiamata VERA per richiedere i dati al server */
  const fetchLastReports = async () => {
    axios.get(`http://localhost:5000/reports/retrieveLastReports`)
      .then(res => {
        const reports = res.data.lista;
        console.log(reports);
        
        setLastReports(reports);
      })
  }

  const fetchResellerNames = async () => {
    axios.get(`http://localhost:5000/resellers/retrieveResellersNames`)
      .then(res => {
        const data = res.data;
        console.log(data.lista);
        setStoreName(data.lista)
      })

  }

  function feedRow(){
    
    return lastReports;
  }

  function fetchReportAnnuali(){

    lastReports = []
    console.log(lastReports)
    return null
  }


  /* Hooks */
  const [posts, setPosts] = useState([]);
  const [storeName, setStoreName] = useState([]);
  const [index, setIndex] = useState(0);
  const [drop, setDrop] = useState([]);
  const [value, setValue] = React.useState();
  const [siti, setSiti] = useState([]);
  const [datatable, setDatatable] = useState({});
  const [lastReports, setLastReports] = useState([]);
  const [choice, setChoice] = React.useState('');
  const [date, setDate] = useState(new Date());




  const [year, setYear] = useState(0);
  const [month, setMonth] = useState(0);
  const [viewmonth, setViewmonth] = useState(0);

  /* Variabili */
  const history = useHistory();
  const list = [];
  var sito;
  function lista(key, value, text) { // costruttore
    this.key = value;
    this.value = value;
    this.text = text;
  };
  const handleChange = (event) => {
    setChoice(event.target.value);
  };


  /* Liste */
  const columns = [
    {
      field: "",
      headerName: "Button",
      sortable: false,
      width: 100,
      disableClickEventBubbling: true,
      renderCell: (params: CellParams) => {
        const onClick = () => {
          const api: GridApi = params.api;
          const fields = api
            .getAllColumns()
            .map((c) => c.field)
            .filter((c) => c !== "__check__" && !!c);
          const thisRow = {};

          fields.forEach((f) => {
            thisRow[f] = params.getValue(f);
          });

          let path = `/${thisRow.id}`;
          return history.push(path);
        };

        return <Button onClick={onClick}>Dettagli</Button>;
      }
    },
    { field: 'id', headerName: 'id', width: 200, hide: true },
    { field: 'date', headerName: 'Data', width: 200 },
    { field: 'name', headerName: 'Nome', width: 200 },
    { field: 'valutazione', headerName: 'Valutazione', width: '100%' },
  ];

  /* creo la lista per il search selection */
  posts.map(post => (
    sito = new lista(post.userId, post.id, post.title),
    list.push(sito)
  ));

  /* carosello */
  const handleSelect = (selectedIndex, e) => {
    setIndex(selectedIndex);
  };

  function FormAnnuale() {
    return (
      <div>
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
        <Autocomplete
          placeholder='Seleziona Sito'
          value={value}
          onChange={(event, newValue) => {
            setValue(newValue);
          }}
          id="controllable-states-demo"
          options={storeName}
          style={{ width: '150%' }}
          renderInput={(params) => <TextField {...params} label="Seleziona sito" variant="outlined" />}
        />
        <Button
          // onClick={fetchReportAnnuali()}
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
      <div>
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
        <Autocomplete
          placeholder='Seleziona Sito'
          value={value}
          onChange={(event, newValue) => {
            setValue(newValue);
          }}
          id="controllable-states-demo"
          options={storeName}
          style={{ width: '150%' }}
          renderInput={(params) => <TextField {...params} label="Seleziona sito" variant="outlined" />}
        />
          <Button
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
    return (<div>
      <DatePicker
        onChange={setDate}
        value={date}
      />
      <Autocomplete
        placeholder='Seleziona Sito'
        value={value}
        onChange={(event, newValue) => {
          setValue(newValue);
        }}
        id="controllable-states-demo"
        options={storeName}
        style={{ width: '150%' }}
        renderInput={(params) => <TextField {...params} label="Seleziona sito" variant="outlined" />}
      />
        <Button
          
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

        <div className="Ricerca">
          {/* <h4 style={{ letterSpacing: 5 }}>SITI WEB</h4> */}

          {choice == 'Report annuali' ?
            <FormAnnuale /> : choice == 'Report mensili' ?
              <FormMensile /> : choice == 'Report giornalieri' ?
                <FormGiornaliero /> : null}


          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={choice}
            onChange={handleChange}
          >
            <MenuItem value={'Report annuali'}>Report annuali</MenuItem>
            <MenuItem value={'Report mensili'}>Report mensili</MenuItem>
            <MenuItem value={'Report giornalieri'}>Report giornalieri</MenuItem>
          </Select>
        </div>

        <br />
        <div className="ContainerTabella">
          <div className="Tabella">
            {/*console.log('datatable', datatable)*/}
            {/*  <MDBDataTableV5 hover entriesOptions={[5, 20, 25]}
                  entries={5} pagesAmount={4} data={datatable} />*/}
            <DataGrid rows={feedRow()} columns={columns} />
          </div>
        </div>
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

export default Home;
