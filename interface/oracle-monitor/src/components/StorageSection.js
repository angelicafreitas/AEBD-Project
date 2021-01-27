import { useState } from "react";
import { Doughnut, Line } from 'react-chartjs-2';

import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import useFetch from "../utils/useFetch";
import Card from "react-bootstrap/esm/Card";
import ListGroup from "react-bootstrap/esm/ListGroup";
import Table from "react-bootstrap/esm/Table";

const dataChart = (l, v1,v2,v3) => {return {
    labels: l,
    datasets: [
      {
        label: 'Total Size (MB)',
        fill: false,
        lineTension: 0.1,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: '#FF8800',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: '#FF8800',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#FF8800',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        data: v1
      },
      {
        label: 'Free Space (MB)',
        fill: false,
        lineTension: 0.1,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: '#3799bf',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: '#3799bf',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#3799bf',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        data: v2
      },
      {
        label: 'Used Space (MB)',
        fill: false,
        lineTension: 0.1,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: '#c73a5f',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: '#c73a5f',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#c73a5f',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        data: v3
      }
    ]
  }};

const StorageSection = (props) => {
    const {data : recent, isPending: waitRecent, error : errorRecent} = useFetch('http://localhost:7050/tablespaces/' + props.db + '?tablespace=' + props.tablespace + '&recent=true')
    const {data : tablespaceData, isPending, error} = useFetch('http://localhost:7050/tablespaces/' + props.db + '?tablespace=' + props.tablespace)
    const {data : datafiles, isPending : waitDatafiles, error: errorDatafile} = useFetch('http://localhost:7050/datafiles/'+ props.tablespace)
    
    const prepareData = dataI => {
        let labels = []
        let values1 = []
        let values2 = []
        let values3 = []
        console.log(props.db)
        dataI.map(el => {
            console.log(el)
            labels.push(el.QUERY_DATE)
            values1.push(el.SIZEMB)
            values2.push(el.FREE)
            values3.push(el.USED)
        })

        return <Line data={dataChart(labels, values1, values2, values3)} width={500} />
    }

    return (
    <>
        <div className="storageSection mt-3 mr-2">
            <div>
            {isPending && waitRecent && waitDatafiles && <Spinner animation="border" />}
            {error || errorRecent || errorDatafile &&  <Alert variant="danger">{error}{errorRecent}{errorDatafile}</Alert>}
            {tablespaceData && prepareData(tablespaceData)}
            </div>
            
            <div className="mt-3 mb-3">
            {recent && <Doughnut className="mt-3" data={{
                	labels: [
                        'Total (MB)',
                        'Used (MB)',
                        'Free (MB)'
                    ],
                    datasets: [{
                        data: [recent[0].SIZEMB, recent[0].USED, recent[0].FREE],
                        backgroundColor: [
                            '#36A2EB',
                            '#FF6384',
                            '#FFCE56'
                        ],
                        hoverBackgroundColor: [
                            '#36A2EB',
                            '#FF6384',
                            '#FFCE56'
                        ]
                    }]
            }} />}
                <div className="mt-2 mb-3">
                    <h5>Datafiles:</h5>
                {datafiles && <Table className="datafileTable" style={{width: "85%", "margin-top": "2vh"}} striped bordered hover>
                    <thead className="table-header">
                      <tr>
                        <th>Name</th>
                        <th>Size (MB)</th>
                        <th>Used (MB)</th>
                        <th>Free (MB)</th>
                      </tr>
                    </thead>
                    <tbody>
                        {datafiles.map(el => {
                            return(
                            <tr>
                                <td>{el.FILE_NAME}</td>
                                <td>{el.SIZEMB}</td>
                                <td>{el.USED}</td>
                                <td>{el.FREE}</td>
                            </tr>
                            )
                        })}
                    </tbody>
                </Table>}
                </div>
                    
            </div>
        

        </div>
    </>
    );
}
 
export default StorageSection;