import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { VscPulse } from "react-icons/vsc";
import { MdStorage } from "react-icons/md";
import { FaUsers } from "react-icons/fa";

function App(props) {
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
        <Nav className="mr-auto ml-3">
          <Nav.Link className="ml-3" href="/system" active={props.option == "system"}>System <VscPulse /></Nav.Link>
          <Nav.Link className="ml-3" href="/storage" active={props.option == "storage"}>Storage <MdStorage /></Nav.Link>
          <Nav.Link className="ml-3" href="/users" active={props.option == "users"}>Users <FaUsers /></Nav.Link>
        </Nav>

      </Navbar>
    </div>
  );
}

export default App;
