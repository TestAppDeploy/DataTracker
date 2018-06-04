import React from "react";
import Hello from "./Hello";
import { PageHeader } from "react-bootstrap";

require('../css/fullstack.css');
var $ = require('jquery');

import HeaderBackgroundImage from '../images/header.jpg';

export default class App extends React.Component {
  render () {
    return (
      <Hello />
    )
  }
}
