import React from 'react';
import '../css/App.css';
import '../css/Footer.css';
import unicam from '../unicam.png';


function Footer() {
  return (
    <div className="Footer">
        <h5 style={{ fontFamily: "Times New Roman" }}>Universita Degli Studi Di Camerino - Computer Science 2021</h5>
        <img src={unicam} style={{ height: '35px', width: '35px', marginLeft: 10 }} />
    </div>
  );
}

export default Footer;
