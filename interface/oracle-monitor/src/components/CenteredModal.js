import useFetch from "../utils/useFetch"
import Modal from 'react-bootstrap/Modal';
import ListGroup from 'react-bootstrap/ListGroup';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';

export default function ModalCentered(props){
    const {data, isPending, error}= useFetch("http://localhost:7050/users_privileges/"+ props.user_id)

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
              {isPending && <Spinner animation="border" />}
              {error &&  <Alert variant="danger">{error}</Alert>}
            <ListGroup>
                
                {props.user_id !== null && data && data.map(el =>{
                    return (<ListGroup.Item>{el.NAME}</ListGroup.Item>)
                })}
            </ListGroup>
          </Modal.Body>
          <Modal.Footer>
            <Button onClick={props.onHide}>Close</Button>
          </Modal.Footer>
        </Modal>
      );
}