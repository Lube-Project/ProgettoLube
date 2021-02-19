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
  GridApi,
  GridToolbar
} from "@material-ui/data-grid";

import Carousel from 'react-elastic-carousel';
import 'bootstrap/dist/css/bootstrap.min.css';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
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




function Home() {

  const classes = useStyles();


  /* codice eseguito all'avvio della pagina */
  useEffect(() => {
    fetchLastReportsWeb();
    fetchLastReportsFacebook();
    fetchLastReportsInstagram();
    fetchResellerNames();
  }, []);

  function mettiPallini(array) {
    array = array.map(oggetto => {
      oggetto.valutazione_foto = oggetto.valutazione_foto >= 2.75 && oggetto.valutazione_foto <= 3 ? '🔴'
        : oggetto.valutazione_foto >= 2 && oggetto.valutazione_foto < 2.75 ? '🟡'
          : oggetto.valutazione_foto >= 1 && oggetto.valutazione_foto < 2 ? '🟢'
            : '';
      oggetto.valutazione_keywords = oggetto.valutazione_keywords >= 2.75 && oggetto.valutazione_keywords <= 3 ? '🔴'
        : oggetto.valutazione_keywords >= 2 && oggetto.valutazione_keywords < 2.75 ? '🟡'
          : oggetto.valutazione_keywords >= 1 && oggetto.valutazione_keywords < 2 ? '🟢'
            : '';
      oggetto.valutazione_script = oggetto.valutazione_script == 1 ? '🟢' : '🔴';
    })
    return array;
  }
  function mettiPalliniSocial(array) {
    array = array.map(oggetto => {
      oggetto.valutazione_foto = oggetto.valutazione_foto >= 2.75 && oggetto.valutazione_foto <= 3 ? '🔴'
        : oggetto.valutazione_foto >= 2 && oggetto.valutazione_foto < 2.75 ? '🟡'
          : oggetto.valutazione_foto >= 1 && oggetto.valutazione_foto < 2 ? '🟢'
            : '';
      oggetto.valutazione_keywords = oggetto.valutazione_keywords >= 2.75 && oggetto.valutazione_keywords <= 3 ? '🔴'
        : oggetto.valutazione_keywords >= 2 && oggetto.valutazione_keywords < 2.75 ? '🟡'
          : oggetto.valutazione_keywords >= 1 && oggetto.valutazione_keywords < 2 ? '🟢'
            : '';
    })
    return array;
  }



  /* chiamata VERA per richiedere i dati al server */
  const fetchLastReportsWeb = async () => {
    axios.get(`http://c1d480345a12.ngrok.io/reportsWeb/retrieveLastReports`)
      .then(res => {
        const reports = res.data.lista;
        //console.log(reports);
        const pino = [
          {
            field: "",
            headerName: "Bottone",
            sortable: false,
            filterable: false,
            width: 200,
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

                let path = `/dettagliReport/${thisRow.id}`;
                return history.push(path);
              };

              return <Button onClick={onClick}>Dettagli</Button>;
            }
          },
          { field: 'id', headerName: 'id', width: 150, hide: true },
          { field: 'date', headerName: 'Data', width: 150 },
          { field: 'sito', headerName: 'Nome', width: 350, type: 'string' },
          { field: 'valutazione_foto', headerName: 'Foto', width: 150, filterable: false, },
          { field: 'valutazione_keywords', headerName: 'Parole chiave', width: 150, filterable: false, },
          { field: 'valutazione_script', headerName: 'Script', width: 150, filterable: false, },

        ];
        setColumns(pino);
        mettiPallini(reports);
        setReports(reports);
      })

  }

  const fetchLastReportsFacebook = async () => {
    axios.get(`http://c1d480345a12.ngrok.io/reportsFacebook/retrieveLastReportsFacebook`)
      .then(res => {
        const reports = res.data.lista;
        var social = 'facebook';
        //console.log(reports);
        const pino = [
          {
            field: "",
            headerName: "Bottone",
            sortable: false,
            filterable: false,
            width: 200,
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

                let path = `/dettagliReportSocial/${social}/${thisRow.id}`;
                return history.push(path);
              };

              return <Button onClick={onClick}>Dettagli</Button>;
            }
          },
          { field: 'id', headerName: 'id', width: 150, hide: true },
          { field: 'date', headerName: 'Data', width: 150 },
          { field: 'nome', headerName: 'Nome', width: 350, type: 'string' },
          { field: 'quantita_post_neltempo', headerName: 'N. Post', width: 150,type: 'number', },
          { field: 'valutazione_foto', headerName: 'Foto', width: 150, filterable: false, },
          { field: 'valutazione_keywords', headerName: 'Parole chiave', width: 150, filterable: false,},
        ];
        setColumnsF(pino);
        mettiPalliniSocial(reports);
        setReportsF(reports);
      })

  }

  const fetchLastReportsInstagram = async () => {
    axios.get(`http://c1d480345a12.ngrok.io/reportsInstagram/retrieveLastReportsInstagram`)
      .then(res => {
        const reports = res.data.lista;
        var social = 'instagram';
        const pino = [
          {
            field: "",
            headerName: "Bottone",
            sortable: false,
            filterable: false,
            width: 200,
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

                let path = `/dettagliReportSocial/${social}/${thisRow.id}`;
                return history.push(path);
              };

              return <Button onClick={onClick}>Dettagli</Button>;
            }
          },
          { field: 'id', headerName: 'id', width: 150, hide: true },
          { field: 'date', headerName: 'Data', width: 150 },
          { field: 'nome', headerName: 'Nome', width: 350, type: 'string' },
          { field: 'quantita_post_neltempo', headerName: 'N. Post', width: 150,type: 'number', },
          { field: 'valutazione_foto', headerName: 'Foto', width: 150, filterable: false, },
          { field: 'valutazione_keywords', headerName: 'Parole chiave', width: 150, filterable: false,},
        ];
        setColumnsI(pino);
        mettiPalliniSocial(reports);
        setReportsI(reports);
      })

  }

  const fetchResellerNames = async () => {
    axios.get(`http://c1d480345a12.ngrok.io/resellers/retrieveResellersNames`)
      .then(res => {
        const data = res.data;
        // console.log(data.lista);
        setStoreName(data.lista)
      })

  }
  /*
    function fetchReportAnnuali() {
  
      if (!value) {
        axios.get(`http://localhost:5000/reports/retrieveYearAverage?year=${year}&range1=${range[0]}&range2=${range[1]}`)
          .then(res => {
            const reports = res.data.lista;
            mettiPallini(reports);
            setReports(reports)
          });
      } else {
        axios.get(`http://localhost:5000/reports/retrieveYearAverageName?year=${year}&name=${value}&range1=${range[0]}&range2=${range[1]}`)
          .then(res => {
            const reports = res.data.lista;
            mettiPallini(reports);
            setReports(reports);
          });
      }
      const pino = [
        { field: 'id', headerName: 'Nome', width: 150, },
        { field: 'year', headerName: 'Anno', width: 150 },
        { field: 'valutazione', headerName: 'Valutazione', width: 150 },
        { field: 'script', headerName: 'Script', width: 150 },
        { field: 'keywords', headerName: 'Parole Chiave', width: 150 },
        { field: 'logo', headerName: 'Logo', width: 150 },
        { field: 'competitors', headerName: 'Competitors', width: 150 },
        { field: 'parolefoto', headerName: 'Parole Foto', width: 150 },
      ];
      setColumns(pino);
      return null;
    }
    function fetchReportMensili() {
      //non ha selezionato il nome dello store
  
      const pino = [
        { field: 'id', headerName: 'Nome', width: 150, },
        { field: 'year', headerName: 'Anno', width: 150 },
        { field: 'month', headerName: 'Mese', width: 150 },
        { field: 'valutazione', headerName: 'Valutazione', width: 150 },
        { field: 'script', headerName: 'Script', width: 150 },
        { field: 'keywords', headerName: 'Parole Chiave', width: 150 },
        { field: 'logo', headerName: 'Logo', width: 150 },
        { field: 'competitors', headerName: 'Competitors', width: 150 },
        { field: 'parolefoto', headerName: 'Parole Foto', width: 150 },
      ];
      if (!value) {
        axios.get(`http://localhost:5000/reports/retrieveMonthYearAverage?year=${year}&month=${month}&range1=${range[0]}&range2=${range[1]}`)
          .then(res => {
            const reports = res.data.lista;
            mettiPallini(reports);
            setReports(reports)
          });
        setColumns(pino);
        return null;
      } else {
        axios.get(`http://localhost:5000/reports/retrieveMonthYearAverageName?year=${year}&month=${month}&name=${value}&range1=${range[0]}&range2=${range[1]}`)
          .then(res => {
            const reports = res.data.lista;
            mettiPallini(reports);
            setReports(reports);
          });
        setColumns(pino);
        return null;
      }
    }
    function fetchReportDate() {
  
  
      const pino = [
        { field: 'id', headerName: 'Nome', width: 150, },
        { field: 'year', headerName: 'Anno', width: 150 },
        { field: 'month', headerName: 'Mese', width: 150 },
        { field: 'day', headerName: 'Giorno', width: 150 },
        { field: 'valutazione', headerName: 'Valutazione', width: 150 },
        { field: 'script', headerName: 'Script', width: 150 },
        { field: 'keywords', headerName: 'Parole Chiave', width: 150 },
        { field: 'logo', headerName: 'Logo', width: 150 },
        { field: 'competitors', headerName: 'Competitors', width: 150 },
        { field: 'parolefoto', headerName: 'Parole Foto', width: 150 },
      ];
      if (!value) {
        axios.get(`http://localhost:5000/reports/retrieveDayMonthYear?year=${date.getFullYear()}&month=${date.getMonth() + 1}&day=${date.getDate()}&range1=${range[0]}&range2=${range[1]}`)
          .then(res => {
            const reports = res.data.lista;
            mettiPallini(reports);
            setReports(reports)
          });
        setColumns(pino);
        return null;
      } else {
        axios.get(`localhost:5000/reports/retrieveDayMonthYearName?year=${date.getFullYear()}&month=${date.getMonth() + 1}&day=${date.getDate()}&name=${value}&range1=${range[0]}&range2=${range[1]}`)
          .then(res => {
            const reports = res.data.lista;
            mettiPallini(reports);
            setReports(reports);
          });
        setColumns(pino);
        return null;
      }
    }
  */

  /* Hooks */
  const [storeName, setStoreName] = useState([]);
  const [index, setIndex] = useState(0);
  const [value, setValue] = React.useState();
  const [reports, setReports] = useState([]);
  const [choice, setChoice] = React.useState('');
  const [date, setDate] = useState(new Date());
  const [range, setRange] = useState([1, 3]);
  const [columns, setColumns] = useState([]);
  const [click, setClick] = useState(false);
  const [button, setButton] = useState(true);
  const [year, setYear] = useState(0);
  const [month, setMonth] = useState(0);
  const [viewmonth, setViewmonth] = useState();
  const [reportsF, setReportsF] = useState([]);
  const [columnsF, setColumnsF] = useState([]);
  const [reportsI, setReportsI] = useState([]);
  const [columnsI, setColumnsI] = useState([]);
  /* Variabili */
  const history = useHistory();

  const handleChange = (event) => {
    setChoice(event.target.value);
  };


  const handleClick = () => setClick(!click);
  const closeMobileMenu = () => setClick(false);

  const showButton = () => {
    if (window.innerWidth <= 960) {
      setButton(false);
    } else {
      setButton(true);
    }
  }

  window.addEventListener("resize", showButton);


  /*function FormLastReports() {
    return (
      <div className="RicercaAnnuale">
        <Button
          // onClick={fetchReportAnnuali()}
          onClick={() => { fetchLastReports() }}
          variant="contained"
          color="primary"
          className={classes.button}
          endIcon={<SearchIcon />}
        >
          Cerca
      </Button>
      </div>
    );
  }

  function FormAnnuale() {
    return (
      <div className="RicercaAnnuale">

        <Autocomplete
          placeholder='Seleziona Sito'
          value={value}
          onChange={(event, newValue) => {
            setValue(newValue);
          }}
          id="controllable-states-demo"
          options={storeName}
          style={{ width: '20%' }}
          renderInput={(params) => <TextField {...params} label="Seleziona sito" variant="outlined" />}
        />

        <Row>
          <Col md={10}>
            <RangeSlider

              step={0.1}
              max={3}
              min={1}
              progress
              style={{ marginTop: 16, marginBottom: 16, width: "10vw" }}
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
              style={{ width: "15vw" }}
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
          onClick={() => { fetchReportAnnuali() }}
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
      <div className="RicercaMensile">

        <Autocomplete
          placeholder='Seleziona Sito'
          value={value}
          onChange={(event, newValue) => {
            setValue(newValue);
          }}
          id="controllable-states-demo"
          options={storeName}
          style={{ width: '20%' }}
          renderInput={(params) => <TextField {...params} label="Seleziona sito" variant="outlined" />}
        />

        <Row>
          <Col md={10}>
            <RangeSlider

              step={0.1}
              max={3}
              min={1}
              progress
              style={{ marginTop: 16, marginBottom: 16, width: "10vw" }}
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
              style={{ width: "15vw" }}
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
          onClick={() => { fetchReportMensili() }}
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
      <div className="RicercaMensile">

        <Autocomplete
          placeholder='Seleziona Sito'
          value={value}
          onChange={(event, newValue) => {
            setValue(newValue);
          }}
          id="controllable-states-demo"
          options={storeName}
          style={{ width: '20%' }}
          renderInput={(params) => <TextField {...params} label="Seleziona sito" variant="outlined" />}
        />

        <Row>
          <Col md={10}>
            <RangeSlider

              step={0.1}
              max={3}
              min={1}
              progress
              style={{ marginTop: 16, marginBottom: 16, width: "10vw" }}
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
              style={{ width: "15vw" }}
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
        <DatePicker
          onChange={(value) => {
            setDate(value);
          }}
          value={date}
        />
        <Button
          onClick={() => { fetchReportDate() }}
          variant="contained"
          color="primary"
          className={classes.button}
          endIcon={<SearchIcon />}
        >
          Send
      </Button>

      </div>)
  }
*/

  return (
    <div className="App Esempio">

      <Carousel itemsToShow={1}>

        <div className="CaroselloHome">
          <h2 style={{ fontFamily: "Times New Roman" }} >WEB</h2>

          {/*<div className={button ? 'Ricerca' : 'RicercaHidden'} >
            { <h4 style={{ letterSpacing: 5 }}>SITI WEB</h4> }

            {choice == 'Report annuali' ?
              <FormAnnuale /> : choice == 'Report mensili' ?
                <FormMensile /> : choice == 'Report giornalieri' ?
  <FormGiornaliero /> : choice == 'Last reports' ? <FormLastReports /> : null}

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
          </div>*/}

          <br />
          <div className="ContainerTabella">
            <div className="Tabella">
              <DataGrid rows={reports} columns={columns} showToolbar
                components={{
                  Toolbar: GridToolbar,
                }} />
            </div>
          </div>
        </div>

        <div className="CaroselloHome">
          <h2 style={{ fontFamily: "Times New Roman" }} >FACEBOOK</h2>
          <br />
          <div className="ContainerTabella">
            <div className="Tabella">
              <DataGrid rows={reportsF} columns={columnsF} showToolbar
                components={{
                  Toolbar: GridToolbar,
                }} />
            </div>
          </div>
        </div>
        <div className="CaroselloHome">
          <h2 style={{ fontFamily: "Times New Roman" }} >INSTAGRAM</h2>
          <br />
          <div className="ContainerTabella">
            <div className="Tabella">
              <DataGrid rows={reportsI} columns={columnsI} showToolbar
                components={{
                  Toolbar: GridToolbar,
                }} />
            </div>
          </div>
        </div>
      </Carousel>
      <br />
    </div>
  );
}

export default Home;
