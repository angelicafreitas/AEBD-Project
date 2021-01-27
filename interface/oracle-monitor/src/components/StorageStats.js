import useFetch from "../utils/useFetch"

import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import Tab from 'react-bootstrap/Tab';
import Nav from 'react-bootstrap/Nav';
import Card from "react-bootstrap/Card";

export default function Storage(props) {
    const {data, isPending, error} = useFetch("http://localhost:7050/tablespaces/" + props.db)

    return (
      <>
        <div>
              <Tab.Container id="left-tabs-example" defaultActiveKey="first">
                <div className="storage-content">
                  <div className="tablespaces-list">
                    <Card bg="light" border="dark">
                      <Card.Header>
                        Tablespaces:
                      </Card.Header>
                      <Card.Body>
                      {isPending && <Spinner animation="border" />}
                      {error &&  <Alert variant="danger">{error}</Alert>}
                      <Nav variant="pills" className="flex-column">
                        {data && data.map(el => {
                          return(
                            <Nav.Item>
                              <Nav.Link eventKey={el.TABLESPACE_NAME}>{el.TABLESPACE_NAME}</Nav.Link>
                            </Nav.Item>
                          )
                        })}
                      </Nav>
                      </Card.Body>
                    </Card>

                  </div>
                  <div className="datafiles-stats">
                    <Tab.Content>
                      {data && data.map(el => {
                        return(<Tab.Pane eventKey={el.TABLESPACE_NAME}>
                          <h1>{el.TABLESPACE_NAME}</h1>
                        </Tab.Pane>)
                      })}
                    </Tab.Content>
                  </div>
                </div>
              </Tab.Container>

      </ div>
    </>
    )
  }