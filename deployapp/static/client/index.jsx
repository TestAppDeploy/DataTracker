import React from "react";
import { render, ReactDOM } from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import MainLayout from "../imports/layouts/MainLayout.jsx";
import 'bootstrap/dist/css/bootstrap.min.css';

render(<Router>
  <Switch>
  <Route path="/" component={MainLayout} />
  </Switch>
</Router>, document.getElementById("content"));
