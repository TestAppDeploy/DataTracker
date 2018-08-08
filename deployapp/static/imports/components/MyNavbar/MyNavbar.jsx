import React from "react";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem } from 'reactstrap';

  require('./MyNavbar.css');

export default class MyNavbar extends React.Component {
  constructor(props) {
  super(props);

  this.toggle = this.toggle.bind(this);
  this.state = {
    isOpen: false
  };
}
toggle() {
  this.setState({
    isOpen: !this.state.isOpen
  });
}

  render () {
    return (
      <Navbar color="light" light expand="md">
        <NavbarBrand href=""><img src="https://www.seeklogo.net/wp-content/uploads/2016/11/rbc-logo-preview-400x400.png"  id="RBC_logo"/>FRED Tracker</NavbarBrand>
        <NavbarToggler onClick={this.toggle} />
        <Collapse isOpen={this.state.isOpen} navbar>
          <Nav className="ml-auto" navbar>
            <NavItem>
              <NavLink href="/components/">Indexes</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="localhost:5000">Download Data</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="localhost:5000">Import CSV</NavLink>
            </NavItem>
          </Nav>
        </Collapse>
      </Navbar>
    )
  }
}
