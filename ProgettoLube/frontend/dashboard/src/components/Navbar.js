import React from 'react';
import '../css/App.css';
import { Link } from 'react-router-dom';
import logoLube from '../logoLube.png';

const Logo = () => {
  return <div className="NavbarLogo" >
    <img src={logoLube} style={{ height: '100%', width: '10%' }} />
    <Link style={{ color: '#fff', textDecoration: 'none' }} to="/" >
      <h1 style={{ letterSpacing: 10, fontSize: 50 }}>DASHBOARD</h1>
    </Link>
  </div>
}

function Navbar() {
  return (
    <div className="Navbar">

      <Logo />

      <ul className="Links">
        <Link style={{ color: '#fff', textDecoration: 'none' }} to="/" >
          <li>Home</li>
        </Link>
        <Link style={{ color: '#fff', textDecoration: 'none' }} to="/mappa" >
          <li>Mappa</li>
        </Link>
        <Link style={{ color: '#fff', textDecoration: 'none' }} to="/contact" >
          <li>Contact</li>
        </Link>
      </ul>
    </div>
  );
}

export default Navbar;
