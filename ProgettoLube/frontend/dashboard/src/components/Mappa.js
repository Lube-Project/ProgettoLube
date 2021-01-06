// import Autocomplete from '@material-ui/lab/Autocomplete';
import React from 'react';
import '../css/App.css';
// import AutoComplete from "./Autocomplete";
// import Map from "./MapComponent";
import { useState, useEffect } from 'react';
import ReactMapGL, { Marker } from 'react-map-gl';
import axios from 'axios';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from "@material-ui/core/TextField";
import logoLube from '../logoLube.png';
import 'mapbox-gl/dist/mapbox-gl.css';
import { Link } from 'react-router-dom';


function Mappa() {

  useEffect(() => {
    //getResellersName();
    getResellersPosition();
  }, []);


  function getResellersName() {
    axios.get(`http://localhost:5000/resellers/retrieveResellersNames`)
      .then(res => {
        const data = res.data;
        // console.log(data.lista);
        setStoreName(data.lista)
      })

  }
  function getResellersPosition() {
    axios.get(`http://localhost:5000/resellers/retrieveResellersPositions`)
      .then(res => {
        const data = res.data.lista;
        var lista = [];
        data.map(city => {
          lista.push(city.nome);
        });
        setStorePositions(data);
        setStoreName(lista);
      })

  }

  function selectStore(newValue) {

    if (newValue != null) {
      setValue(newValue);
      let pino = storePositions.find(x => x.nome === newValue);
      viewport.latitude = pino.latitudine;
      viewport.longitude = pino.longitudine;
      viewport.zoom = 11;

    }

  }

  const [storePositions, setStorePositions] = useState();
  const [storeName, setStoreName] = useState([]);
  const [value, setValue] = React.useState();
  const [name, setName] = React.useState();
  const [latitude, setLatitude] = React.useState();
  const [longitude, setLongitude] = React.useState();
  const [viewport, setViewport] = useState({
    width: "1000",
    height: "500px",

    latitude: 43.041040634170734,
    longitude: 12.65069401829706,
    zoom: 6,


  });

  return (
    <div className="App">
      <h1>MAPPA</h1>
      <div className="Container">
        <Autocomplete
          placeholder='Seleziona Sito'
          value={value}
          onChange={(event, newValue) => {
            selectStore(newValue);
          }}
          id="controllable-states-demo"
          options={storeName}
          style={{ width: '100%' }}
          renderInput={(params) => <TextField {...params} label="Seleziona sito" variant="outlined" />}
        />

        <ReactMapGL

          mapStyle='mapbox://styles/stagemtmv/ckjh2rchph5tm19mqudag4i6e'
          {...viewport}
          onViewportChange={nextViewport => setViewport(nextViewport)}
          mapboxApiAccessToken="pk.eyJ1Ijoic3RhZ2VtdG12IiwiYSI6ImNramgxZ25jcjk0a3UycWxiYmU1OWZ1ZnIifQ.uy5k7k9bzMeox5fzR3Iz3A"

        >

          {
            storePositions && storePositions.map(store => (
             
              <Link to={`/store/${store.nome}`}>
                <Marker key={store.nome} latitude={store.latitudine} longitude={store.longitudine}><img style={{ width: 50, height: 50 }} src={logoLube}></img></Marker>
              </Link>

            ))
          }
        </ReactMapGL>
      </div>
    </div>
  );
}

export default Mappa;
