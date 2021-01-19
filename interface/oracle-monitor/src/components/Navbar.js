import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { VscPulse } from "react-icons/vsc";
import { MdStorage } from "react-icons/md";
import { FaUsers } from "react-icons/fa";

import {useState} from 'react'

function NavbarComp(props) {

  const [selected, setSelected] = useState(1)

  return (
    <div className="App">
      <Navbar bg="dark" variant="dark">
        <Navbar.Brand href="#home">
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
          <Nav className="mr-auto ml-3" activeKey={1}>
            <Nav.Link eventKey={1} onClick={() => setSelected(1)} className="ml-3" href="/system">System <VscPulse /></Nav.Link>
            <Nav.Link eventKey={2} onClick={() => setSelected(2)} className="ml-3" href="/storage">Storage <MdStorage /></Nav.Link>
            <Nav.Link eventKey={3} onClick={() => setSelected(3)} className="ml-3" href="/users">Users <FaUsers /></Nav.Link>
          </Nav>
        }
      </Navbar>
    </div>
  );
}

export default NavbarComp;
