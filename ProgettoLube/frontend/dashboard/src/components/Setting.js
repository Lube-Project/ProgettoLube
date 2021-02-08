import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/App.css';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import { makeStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';


import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';
import FolderIcon from '@material-ui/icons/Folder';
import DeleteIcon from '@material-ui/icons/Delete';

import { FixedSizeList } from 'react-window';


const useStyles = makeStyles((theme) => ({
  button: {
    margin: theme.spacing(1),
    width: 100,
  },
  demo: {
    backgroundColor: theme.palette.background.paper,
  },
}));


function Setting() {

  const classes = useStyles();

  useEffect(() => {
    getCrawlerKeywords();
    getSocialCrawlerDays();

  }, []);

  function getCrawlerKeywords() {
    axios.get(`http://377d9b605ad4.ngrok.io/settings/getKeywords`)
      .then(res => {
        const data = res.data;
        console.log(data.lista);
        setKeywords(data.lista)
      })
  }

  async function addCrawlerKeywords(keyword) {
    await axios.get(`http://377d9b605ad4.ngrok.io/settings/addKeyword?keyword=${keyword}`)
  }

  async function deleteCrawlerKeywords(keyword) {
    await axios.get(`http://377d9b605ad4.ngrok.io/settings/deleteKeyword?keyword=${keyword}`)
  }

  function getSocialCrawlerDays() {
    axios.get(`http://377d9b605ad4.ngrok.io/settings/getSocialActivityTimeCrawler`)
      .then(res => {
        const data = res.data;
        console.log(data);
        setDays(data)
      })
  }

  async function changeSocialCrawlerDays(days) {
    await axios.get(`http://377d9b605ad4.ngrok.io/settings/modifySocialActivityTimeCrawler?days=${days}`)
  }


  const [keywords, setKeywords] = useState([]);
  const [days, setDays] = useState(0);
  const [parola, setParola] = useState("");
  const handleChange = (event) => {
    setDays(event.target.value);
  };
  const handleChange2 = (event) => {
    setParola(event.target.value);
  };

  const [dense, setDense] = React.useState(false);
  const [secondary, setSecondary] = React.useState(false);


  return (
    <div className="App">

      <div className="Container">

        <div className="Sezione">
          <div className="TitoloImpo">
            <h3 className="Scritta">Impostazioni Web</h3>
          </div>

          <Divider light />
          <br />
          <div className="Impostazione2">
            <p>Descrizione ....</p>

            <div className="Scroll">
              <List>
                {keywords.map(value => {
                  return <ListItem key={value}>
                    <ListItemText
                      primary={value}
                    />

                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="delete">
                        <DeleteIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                })}
              </List>
            </div>

            <TextField
              id="outlined-helperText"
              label="Inserisci parola"
              defaultValue=""
              variant="outlined"
              value={parola}
              onChange={handleChange2}
            />

            <Button
              variant="contained"
              color="primary"
              className={classes.button}
              endIcon={<Icon>send</Icon>}
            >
              INVIA
            </Button>

          </div>
          <br />
          <Divider light />

        </div>

        <div className="Sezione">
          <div className="TitoloImpo">
            <h3 className="Scritta">Impostazioni Social</h3>
          </div>
          <Divider light />
          <br />
          <div className="Impostazione">
            <p>Descrizione ....</p>
            <TextField
              id="outlined-number"
              label="A quanti giorni vuoi risalire"
              type="number"
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
              className="Number"
              defaultValue="30"
              value={days}
              onChange={handleChange}
            />

            <Button
              variant="contained"
              color="primary"
              className={classes.button}
              endIcon={<Icon>send</Icon>}
            >
              INVIA
            </Button>
          </div>
          <br />
          <Divider light />
          <br />

          <div className="Impostazione2">
            <p>Descrizione ....</p>

            <div className="Scroll">
              <List>
                {keywords.map(value => {
                  return <ListItem key={value}>
                    <ListItemText
                      primary={value}
                    />

                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="delete">
                        <DeleteIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                })}
              </List>
            </div>

            <TextField
              id="outlined-helperText"
              label="Inserisci parola"
              defaultValue=""
              variant="outlined"
              value={parola}
              onChange={handleChange2}
            />

            <Button
              variant="contained"
              color="primary"
              className={classes.button}
              endIcon={<Icon>send</Icon>}
            >
              INVIA
            </Button>

          </div>

        </div>

      </div>

      {/* 


      <div>GIORNI : {days}</div>
      {keywords.map(keyword =>
        (<p key={keyword}>PAROLA CHIAVE : {keyword}</p>)
      )}*/}

    </div>
  );
}

export default Setting;
