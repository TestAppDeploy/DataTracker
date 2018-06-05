import React from "react";
import Hello from "../components/Hello/Hello.jsx";
import { PageHeader } from "react-bootstrap";


var $ = require('jquery');

export default class App extends React.Component {
  render () {
    return (
      <Hello />
    )
  }
}
