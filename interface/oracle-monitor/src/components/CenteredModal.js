import useFetch from "../utils/useFetch"
import Modal from 'react-bootstrap/Modal';
import ListGroup from 'react-bootstrap/ListGroup';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import { useState } from "react";

export default function ModalCentered(props){
    const {data, isPending, error}= useFetch("http://localhost:7050/users_privileges/"+ props.user_id)
    const {data: sessions, isPending: waitSessions, error: sessionError} = useFetch("http://localhost:7050/sessions/"+ props.user_id)
    const [query, setQuery] = useState("")

    return (
        <Modal
          show={props.show}
          onHide = {props.onHide}
          size="lg"
          aria-labelledby="contained-modal-title-vcenter"
          centered
        >
          <Modal.Header closeButton>
            <Modal.Title id="contained-modal-title-vcenter">
              {props.header}
            </Modal.Title>
          </Modal.Header>
          <Modal.Body>
              <h5>Sessions:</h5>
              <ListGroup className="mb-3">
                
                {props.user_id !== null && sessions && sessions.map(el =>{
                    return (<ListGroup.Item>{"Session ID: " + el.SESSION_ID + " | " + el.SESSION_STATUS + " | " + el.LOGON_TIME}</ListGroup.Item>)
                })}
                {sessions && sessions.length == 0 && <Alert variant="warning">No sessions for this user</Alert>}
            </ListGroup>
            {(isPending || waitSessions) && <Spinner animation="border" />}
            {error || sessionError &&  <Alert variant="danger">{error}</Alert>}
            <h5>Privileges: <span><input onChange={(e) => setQuery(e.target.value)} type="text" /></span></h5>
            
            <ListGroup>
                
                {props.user_id !== null && data && data.map(el =>{
                  if(el.PRIV_NAME.trim().includes(query)){
                    return (<ListGroup.Item>{el.PRIV_NAME}</ListGroup.Item>)
                  }
                    
                })}
            </ListGroup>
            {(isPending || waitSessions) && <Spinner animation="border" />}
            {error || sessionError &&  <Alert variant="danger">{error}</Alert>}
          </Modal.Body>
          <Modal.Footer>
            <Button onClick={props.onHide}>Close</Button>
          </Modal.Footer>
        </Modal>
      );
}