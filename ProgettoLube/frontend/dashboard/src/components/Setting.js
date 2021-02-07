import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/App.css';


function Setting() {

  useEffect(() => {
    getCrawlerKeywords();
    getSocialCrawlerDays();

  }, []);

  function getCrawlerKeywords() {
    axios.get(`http://127.0.0.1:5000/settings/getKeywords`)
      .then(res => {
        const data = res.data;
        console.log(data.lista);
        setKeywords(data.lista)
      })
  }

  async function addCrawlerKeywords(keyword) {
    await axios.get(`http://127.0.0.1:5000/settings/addKeyword?keyword=${keyword}`)
  }

  async function deleteCrawlerKeywords(keyword) {
    await axios.get(`http://127.0.0.1:5000/settings/deleteKeyword?keyword=${keyword}`)
  }

  function getSocialCrawlerDays() {
    axios.get(`http://127.0.0.1:5000/settings/getSocialActivityTimeCrawler`)
      .then(res => {
        const data = res.data;
        console.log(data);
        setDays(data)
      })
  }

  async function changeSocialCrawlerDays(days) {
    await axios.get(`http://127.0.0.1:5000/settings/modifySocialActivityTimeCrawler?days=${days}`)
  }


  const [keywords, setKeywords] = useState([]);
  const [days, setDays] = useState(0);


  return (
    <div className="App">
      <h1>Settings</h1>
      <div>GIORNI : {days}</div>
        {keywords.map(keyword =>
         ( <p key={keyword}>PAROLA CHIAVE : {keyword}</p>)
        )}
      
    </div>
  );
}

export default Setting;
