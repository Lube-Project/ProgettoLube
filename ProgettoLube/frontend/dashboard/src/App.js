import React from 'react';
import './css/App.css';
import Home from './components/Home';
import Mappa from './components/Mappa';
import Contact from './components/Contact';
import Navbar from './components/Navbar';
import Post from './components/Post';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Switch>
          <Route exact path='/' component={Home} />
          <Route exact path='/mappa' component={Mappa} />
          <Route exact path='/contact' component={Contact} />
          <Route exact path='/:id' component={Post} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
