import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home';
import PassesPerStation from './pages/PassesPerStation';
import ChargesBy from './pages/ChargesBy';
import PassesAnalysis from './pages/Passes Analysis';
import PassesCost from './pages/PassesCost';



function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Switch>
          <Route path='/' exact component={Home} />
          <Route path='/PassesPerStation' component={PassesPerStation} />
          <Route path='/ChargesBy' component={ChargesBy} />
          <Route path='/PassesAnalysis' component={PassesAnalysis} />
          <Route path='/PassesCost' component={PassesCost} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
