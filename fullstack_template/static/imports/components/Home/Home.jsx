import React from "react";
import { Container, Row, Col } from 'reactstrap';
import {Line} from 'react-chartjs-2';
import {Bar} from 'react-chartjs-2';
import Fred from 'node-fred'


require('./Home.css');
var $ = require('jquery');

let apiKey = '9191e886eb8b7e932d92df410fbf0c9e'
const fred = new Fred(apiKey);

fred.categories.getCategory(125)
  .then((res) => {
    console.log('Category', res);
  })
  .catch((err) => {
    console.error('Error', err);
  })

const mixdata = {
  // labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [{
      label: 'Sales',
      type:'line',
      data: [51, 65, 40, 49, 60, 37, 40],
      fill: false,
      borderColor: '#EC932F',
      backgroundColor: '#EC932F',
      pointBorderColor: '#EC932F',
      pointBackgroundColor: '#EC932F',
      pointHoverBackgroundColor: '#EC932F',
      pointHoverBorderColor: '#EC932F',
      yAxisID: 'y-axis-2'
    },{
      type: 'bar',
      label: 'Visitor',
      data: [200, 185, 590, 621, 250, 400, 95],
      fill: false,
      backgroundColor: '#71B37C',
      borderColor: '#71B37C',
      hoverBackgroundColor: '#71B37C',
      hoverBorderColor: '#71B37C',
      yAxisID: 'y-axis-1'
    }]
};

const options = {
  responsive: true,
  tooltips: {
    mode: 'label'
  },
  elements: {
    line: {
      fill: false
    }
  },
  scales: {
    xAxes: [
      {
        display: true,
        gridLines: {
          display: false
        },
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      }
    ],
    yAxes: [
      {
        type: 'linear',
        display: true,
        position: 'left',
        id: 'y-axis-1',
        gridLines: {
          display: false
        },
        labels: {
          show: true
        }
      },
      {
        type: 'linear',
        display: true,
        position: 'right',
        id: 'y-axis-2',
        gridLines: {
          display: false
        },
        labels: {
          show: true
        }
      }
    ]
  }
};

const plugins = [{
    afterDraw: (chartInstance, easing) => {
        const ctx = chartInstance.chart.ctx;
        ctx.fillText("", 100, 100);
    }
}];


const bardata = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [
    {
      label: 'Data',
      backgroundColor: 'rgba(255,99,132,0.2)',
      borderColor: 'rgba(255,99,132,1)',
      borderWidth: 1,
      hoverBackgroundColor: 'rgba(255,99,132,0.4)',
      hoverBorderColor: 'rgba(255,99,132,1)',
      data: [65, 59, 80, 81, 56, 55, 40]
    }
  ]
};

const data = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [
    {
      label: 'Data',
      fill: false,
      lineTension: 0.1,
      backgroundColor: 'rgba(75,192,192,0.4)',
      borderColor: 'rgba(75,192,192,1)',
      borderCapStyle: 'butt',
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: 'miter',
      pointBorderColor: 'rgba(75,192,192,1)',
      pointBackgroundColor: '#fff',
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: 'rgba(75,192,192,1)',
      pointHoverBorderColor: 'rgba(220,220,220,1)',
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: [65, 59, 80, 81, 56, 55, 40]
    }
  ]
};

export default class Home extends React.Component {

  constructor(props) {
        super(props);
        this.state = {greeting: 'Hello ' + this.props.name};

        // This binding is necessary to make `this` work in the callback
        this.getPythonHello = this.getPythonHello.bind(this);
    }

    personaliseGreeting(greeting) {
        this.setState({greeting: greeting + ' ' + this.props.name + '!'});
    }

    getPythonHello() {
        $.get(window.location.href + 'data', (data) => {
            console.log(data);
            this.personaliseGreeting(data);
        });
    }


displayName: 'LineExample';
displayName: 'BarExample';
displayName: 'MixExample';

render() {
  return (
    <div>
      <Container>
        <Row>
          <Col>
            <h3>Graphing data from past days</h3>
          </Col>
        </Row>
      </Container>
      <Container>
        <Row>
          <Col className="Graph_block">
            <Line data={data} />
          </Col>
          <Col className="Graph_block">
            <Bar
          data={bardata}
          width={100}
          height={50}
          options={{
            maintainAspectRatio: false
          }}
        />
          </Col>
        </Row>
        <Row>
          <Col className="Graph_block">
            <Bar
          data={mixdata}
          options={options}
          plugins={plugins}
        />
          </Col>
          <Col className="Graph_block">
            <Line data={data} />
          </Col>
        </Row>
      </Container>

    </div>
  );
}
}
