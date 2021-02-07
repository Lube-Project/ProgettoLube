import React, { useState } from 'react';
//import '../css/App.css';
import '../css/Navbar.css';

import { Link } from 'react-router-dom';
import logoLube from '../logoLube.png';
import { StepButton } from '@material-ui/core';
import {Button} from './Button';
import Settings from '@material-ui/icons/Settings';


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
      <img src={logoLube} style={{ height: '100%', width: '20%' }} />
     
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
        <Link style={{ color: '#fff', textDecoration: 'none' }} to="/setting" onClick={closeMobileMenu}>
          <li className="nav-item">
            <Settings style={{ fontSize: 23 }}>Impostazioni</Settings></li>
        </Link></ul>
    </div>
  );
}

export default Navbar;

//  .nav-menu {
//    display: flex;
//    flex-direction: column;
//    width: 100%;
//    height: 100.6%;
//    position: absolute;
//    top: 63px;
//    left: 0;
//    opacity: 1;
//    transition: all 0.8s ease;
//    z-index: 1;
//  }
//  .nav-menu.active {
//    background: indianred;
//    left: 90px;
//    height: auto;
//    padding-bottom: 5%;
//    opacity: 1;
//    transition: all 0.3s ease;
//    z-index: 1;
// }