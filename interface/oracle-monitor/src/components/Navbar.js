import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { VscPulse } from "react-icons/vsc";
import { MdStorage } from "react-icons/md";
import { FaUsers } from "react-icons/fa";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import {useState} from 'react'

function NavbarComp(props) {



  return (
    <div className="App">
      <Navbar bg="dark" variant="dark">
        <Navbar.Brand href="/">
          <img
            alt=""
            src="/oracle.png"
            width="40"
            height="30"
            className="d-inline-block align-top"
          />{' '}
          Oracle Monitor
        </Navbar.Brand>
        {props.showLinks && 
          <Nav className="mr-auto ml-3" activeKey={props.selected}>
            <Nav.Link eventKey={1} className="ml-3" href={"http://localhost:3000" + props.path + "/system"}>System <VscPulse /></Nav.Link>
            <Nav.Link eventKey={2} className="ml-3" href={"http://localhost:3000" + props.path + "/storage"}>Storage <MdStorage /></Nav.Link>
            <Nav.Link eventKey={3} className="ml-3" href={"http://localhost:3000" + props.path + "/users"}>Users <FaUsers /></Nav.Link>
          </Nav>
        }
        <span style={{"fontWeight": "600", "color": "white"}}>{props.selectedDB}</span>
      </Navbar>
      
    </div>
  );
}

export default NavbarComp;
