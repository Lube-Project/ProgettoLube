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
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';



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
    getCrawlerKeywordsSocial();
    getSocialCrawlerDays();

  }, []);

  function getCrawlerKeywords() {
    axios.get(`http://localhost:5000/settings/getKeywordsCrawler`)
      .then(res => {
        const data = res.data;
        console.log("KEYWORDS WEB : ", data.lista);
        setKeywordsCrawler(data.lista)
      })
  }

  function addCrawlerKeywords(keyword) {
    if (typeof (keyword) == 'string') {
      axios.get(`http://localhost:5000/settings/addKeywordCrawler?keyword=${keyword}`);
      getCrawlerKeywords();
    }
  }

  function deleteCrawlerKeywords(keyword) {
    axios.get(`http://localhost:5000/settings/deleteKeywordCrawler?keyword=${keyword}`);
    getCrawlerKeywords();

  }


  function getCrawlerKeywordsSocial() {
    axios.get(`http://localhost:5000/settings/getKeywordsCrawlerSocial`)
      .then(res => {
        const data = res.data;
        console.log("KEYWORDS SOCIAL : ", data.lista);
        setKeywordsSocial(data.lista)
      })
  }

  function addCrawlerSocialKeywords(keyword) {
    if(typeof (keyword) == 'string'){
      axios.get(`http://localhost:5000/settings/addKeywordCrawlerSocial?keyword=${keyword}`);
      getCrawlerKeywordsSocial();
    }
    
  }

  function deleteCrawlerSocialKeywords(keyword) {
    axios.get(`http://localhost:5000/settings/deleteKeywordCrawlerSocial?keyword=${keyword}`);
    getCrawlerKeywordsSocial();
  }

  function getSocialCrawlerDays() {
    axios.get(`http://localhost:5000/settings/getSocialActivityTimeCrawler`)
      .then(res => {
        const data = res.data;
        console.log(data);
        setDays(data);
      })
  }

  function changeSocialCrawlerDays() {
    axios.get(`http://localhost:5000/settings/modifySocialActivityTimeCrawler?days=${daysInsert}`);
    getSocialCrawlerDays();
  }


  const [keywordsCrawler, setKeywordsCrawler] = useState([]);
  const [keywordsSocial, setKeywordsSocial] = useState([]);
  const [days, setDays] = useState();
  const [daysInsert, setDaysInsert] = useState();
  const [parolaWeb, setParolaWeb] = useState("");
  const [parolaSocial, setParolaSocial] = useState("");
  const handleChange = (event) => {
    setDaysInsert(event.target.value);
  };
  const handleChange2 = (event) => {
    setParolaWeb(event.target.value);
  };
  const handleChange3 = (event) => {
    setParolaSocial(event.target.value);
  };



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
          <div className="Descrizione">
            <p style={{fontSize:20}}><b>Lista parole chiave da cercare in un sito web :</b></p>
          </div>
            <div className="Scroll">
              <List>
                {keywordsCrawler.map(value => {
                  return <ListItem key={value}>
                    <ListItemText
                      primary={value}
                    />

                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="delete" onClick={() => {
                        deleteCrawlerKeywords(value);
                      }}>
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
              //defaultValue=""
              variant="outlined"
              value={parolaWeb}
              onChange={handleChange2}
            />

            <Button
              variant="contained"
              color="primary"
              className={classes.button}
              endIcon={<Icon>send</Icon>}
              onClick={() => {
                addCrawlerKeywords(parolaWeb);
                setParolaWeb('');
              }}
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
            <div className="Descrizione">
            <p style={{fontSize:20}}><b>Partendo dall'ultimo post, il numero di giorni precedenti che determinano il periodo di analisi</b></p>
            </div>
            <h4><b>Numero giorni : </b> {days} </h4>
            <TextField
              id="outlined-number"
              label="A quanti giorni vuoi risalire"
              type="number"
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
              className="Number"
              defaultValue={days}
              //value={days}
              onChange={handleChange}
            />

            <Button
              variant="contained"
              color="primary"
              className={classes.button}
              endIcon={<Icon>send</Icon>}
              onClick={() => {
                changeSocialCrawlerDays();
              }}
            >
              INVIA
            </Button>
          </div>
          <br />
          <Divider light />
          <br />

          <div className="Impostazione2">
          <div className="Descrizione">
            <p style={{fontSize:20}}><b>Lista parole chiave da cercare in un profilo social :</b></p>
          </div>

            <div className="Scroll">
              <List>
                {keywordsSocial.map(value => {
                  return <ListItem key={value}>
                    <ListItemText
                      primary={value}
                    />

                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="delete" onClick={() => {
                        deleteCrawlerSocialKeywords(value);
                      }}>
                        <DeleteIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                })}
              </List>
            </div>

            <TextField
              //id="outlined-helperText"
              label="Inserisci parola"
              //defaultValue=""
              variant="outlined"
              value={parolaSocial}
              onChange={handleChange3}
            />

            <Button
              variant="contained"
              color="primary"
              className={classes.button}
              endIcon={<Icon>send</Icon>}
              onClick={() => {
                addCrawlerSocialKeywords(parolaSocial);
                setParolaSocial('');
              }}
            >
              INVIA
            </Button>
          </div>
        </div>
        <br/>
      </div>
    </div>
  );
}

export default Setting;
