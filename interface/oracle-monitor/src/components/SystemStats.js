import { Line } from 'react-chartjs-2';
import useFetch from '../utils/useFetch';
import SystemSection from './SystemSection';


const dataChart = (l, v) => {return {
  labels: l,
  datasets: [
    {
      label: 'Data',
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
      data: v
    }
  ]
}};

const dataChart2 = (l, v1, v2) => {return {
  labels: l,
  datasets: [
    {
      label: 'Total (MB)',
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
      label: 'Used (MB)',
      fill: false,
      lineTension: 0.1,
      backgroundColor: 'rgba(75,192,192,0.4)',
      borderColor: '#4193bf',
      borderCapStyle: 'butt',
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: 'miter',
      pointBorderColor: '#4193bf',
      pointBackgroundColor: '#fff',
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: '#4193bf',
      pointHoverBorderColor: 'rgba(220,220,220,1)',
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: v2
    }
  ]
}};

export default function System(props) {

    return (<>

      <SystemSection title="Number of CPU Cores" url={"http://localhost:7050/cpu/" + props.db + "?stat=NUM_CPU_CORES"}

        transform={(data) => {
          let labels = []
          let values = []
          let aux = data.slice(Math.max(data.length - 10, 0))

          aux.map( (el) => {
            labels.push(el.QUERY_DATE.replace(/T|Z|\.\d{3}/g, ' ').trim())
            values.push(el.VALUE)
          })

          return <Line width={900} height={300} data={dataChart(labels, values)} />
        }}
      
      />

      <SystemSection title="Nice Time" url={"http://localhost:7050/cpu/" + props.db + "?stat=NICE_TIME"}


        subtitle="Time (centi-secs) spent in low-priority user code"
        transform={(data) => {
          let labels = []
          let values = []
          let aux = data.slice(Math.max(data.length - 10, 0))

          aux.map( (el) => {
            labels.push(el.QUERY_DATE.replace(/T|Z|\.\d{3}/g, ' ').trim())
            values.push(el.VALUE)
          })

          return <Line width={900} height={300} data={dataChart(labels, values)} />
        }}
      
      />

      <SystemSection title="System Time" url={"http://localhost:7050/cpu/" + props.db + "?stat=SYS_TIME"}


        subtitle="Time (centi-secs) spent in the kernel"
        transform={(data) => {
          let labels = []
          let values = []
          let aux = data.slice(Math.max(data.length - 10, 0))

          aux.map( (el) => {
            labels.push(el.QUERY_DATE.replace(/T|Z|\.\d{3}/g, ' ').trim())
            values.push(el.VALUE)
          })

          return <Line width={900} height={300} data={dataChart(labels, values)} />
        }}
      
      />

      <SystemSection title="Busy Time" url={"http://localhost:7050/cpu/" + props.db + "?stat=BUSY_TIME"}


        subtitle="Time (centi-secs) that CPUs have been in the busy state"
        transform={(data) => {
          let labels = []
          let values = []
          let aux = data.slice(Math.max(data.length - 10, 0))

          aux.map( (el) => {
            labels.push(el.QUERY_DATE.replace(/T|Z|\.\d{3}/g, ' ').trim())
            values.push(el.VALUE)
          })

          return <Line width={900} height={300} data={dataChart(labels, values)} />
        }}
      
      />

      <SystemSection title="IO Wait Time" url={"http://localhost:7050/cpu/" + props.db + "?stat=IOWAIT_TIME"}


        subtitle="Time (centi-secs) spent waiting for IO"
        transform={(data) => {
          let labels = []
          let values = []
          let aux = data.slice(Math.max(data.length - 10, 0))

          aux.map( (el) => {
            labels.push(el.QUERY_DATE.replace(/T|Z|\.\d{3}/g, ' ').trim())
            values.push(el.VALUE)
          })

          return <Line width={900} height={300} data={dataChart(labels, values)} />
        }}
      
      />

      <SystemSection title="Load" url={"http://localhost:7050/cpu/" + props.db + "?stat=LOAD"}


        subtitle="Number of processes running or waiting on the run queue"
        transform={(data) => {
          let labels = []
          let values = []
          let aux = data.slice(Math.max(data.length - 10, 0))

          aux.map( (el) => {
            labels.push(el.QUERY_DATE.replace(/T|Z|\.\d{3}/g, ' ').trim())
            values.push(el.VALUE)
          })

          return <Line width={900} height={300} data={dataChart(labels, values)} />
        }}
      
      />

      <SystemSection title="Idle Time" url={"http://localhost:7050/cpu/" + props.db + "?stat=IDLE_TIME"}


        subtitle="Time (centi-secs) that CPUs have been in the idle state"
        transform={(data) => {
          let labels = []
          let values = []
          let aux = data.slice(Math.max(data.length - 10, 0))

          aux.map( (el) => {
            labels.push(el.QUERY_DATE.replace(/T|Z|\.\d{3}/g, ' ').trim())
            values.push(el.VALUE)
          })

          return <Line width={900} height={300} data={dataChart(labels, values)} />
        }}
      
      />

      <SystemSection title="Memory Statistics" url={"http://localhost:7050/memory/" + props.db}


        subtitle="Total and used memory"
        transform={(data) => {
          let labels = []
          let values1 = []
          let values2 = []

          let aux = data.slice(Math.max(data.length - 10, 0))

          aux.map( (el) => {
            labels.push(el.QUERY_DATE.replace(/T|Z|\.\d{3}/g, ' ').trim())
            values1.push(el.TOTAL)
            values2.push(el.USED)
          })

          return <Line width={900} height={300} data={dataChart2(labels, values1, values2)} />
        }}
      
      />
    
    </>)
  }