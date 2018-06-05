import React, {Component} from 'react';
import { render, ReactDOM } from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import App from './App.jsx';
import MyNavbar from '../components/MyNavbar/MyNavbar.jsx';

const MainLayout = () => {
  return (
    <div className="main-layout">
      <header>
        <MyNavbar />
      </header>

      <main>
        <Router>
          <Switch>
          <Route exact path="/" component={App} />
          </Switch>
        </Router>
      </main>

    </div>
  );
 }

 export default MainLayout;
