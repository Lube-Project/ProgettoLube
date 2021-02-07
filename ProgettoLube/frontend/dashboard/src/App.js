import React from 'react';
import './css/App.css';
import './css/Navbar.css';

import Home from './components/Home';
import Mappa from './components/Mappa';
import Setting from './components/Setting';
import Navbar from './components/Navbar';
import DettagliReport from './components/DettagliReport';
import DettagliStore from './components/DettagliStore';
import Footer from './components/Footer';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="AppOK">
        <Navbar />
        
          <Switch>
            <Route exact path='/' component={Home} />
            <Route exact path='/mappa' component={Mappa} />
            <Route exact path='/setting' component={Setting} />
            <Route exact path='/:id' component={DettagliReport} />
            <Route exact path='/store/:name' component={DettagliStore} />
          </Switch>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;
