import React from 'react';
import './css/App.css';
import './css/Navbar.css';

import Home from './components/Home';
import Mappa from './components/Mappa';
import Contact from './components/Contact';
import Navbar from './components/Navbar';
import Dettagli from './components/Dettagli';
import Footer from './components/Footer';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <body>
          <Switch>
            <Route exact path='/' component={Home} />
            <Route exact path='/mappa' component={Mappa} />
            <Route exact path='/contact' component={Contact} />
            <Route exact path='/:id' component={Dettagli} />

          </Switch>
        </body>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
