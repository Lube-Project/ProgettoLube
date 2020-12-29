import React, { useState } from 'react';
//import '../css/App.css';
import '../css/Navbar.css';

import { Link } from 'react-router-dom';
import logoLube from '../logoLube.png';
import { StepButton } from '@material-ui/core';
import {Button} from './Button';


function Navbar() {
  const [click,setClick]= useState(false);
  const [button,setButton]= useState(true);

  const handleClick=()=> setClick(!click);
  const closeMobileMenu=()=>setClick(false);

  const showButton=() =>{
    if(window.innerWidth<=960){
      setButton(false);
    }else{
      setButton(true);
    }
    }
  
  window.addEventListener("resize",showButton);

  const Logo = () => {
    return <div className={button ? 'NavbarLogo' : 'NavbarLogoHidden'} >
      <img src={logoLube} style={{ height: '100%', width: '10%' }} />
     
    </div>
  }
  
  const Title= ()=> {
  return <div className={button ? 'NavbarTitle' : 'NavbarTitleHidden'}> <Link style={{ color: '#fff', textDecoration: 'none' }} to="/" >
  <h1 style={{ fontSize: 65, fontFamily: 'Dancing Script'}}>Dashboard</h1>
  </Link>
  </div>
  }
  
  return (
    <div className="Navbar">
    
    
      <Logo />
      <Title/>
      <div className="menu-icon" onClick={handleClick}>
        <i className={click ? 'fas fa-times' : 'fas fa-bars'}/>
      </div>

      <ul className={click ? 'nav-menu active' : 'nav-menu'}>
        <Link style={{ color: '#fff', textDecoration: 'none' }} to="/" onClick={closeMobileMenu}>
          <li className="nav-item">
            Home</li>
        </Link>
        <Link style={{ color: '#fff', textDecoration: 'none' }} to="/mappa" onClick={closeMobileMenu}>
          <li className="nav-item">
            Mappa</li>
        </Link>
        <Link style={{ color: '#fff', textDecoration: 'none' }} to="/contact" onClick={closeMobileMenu}>
          <li className="nav-item">
            Contact</li>
        </Link></ul>
    </div>
  );
}

export default Navbar;
