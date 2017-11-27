import React, { Component } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import Card from '../Card';
import constants from '../../constants';

const ROUTE = "/statistics";
const TITLE = "Statistics";

class Statistics extends Component {
  render() {
    return <Card route={ROUTE} title={TITLE} DataView={DataView} />;
  }
}

class DataView extends Component {
  render() {
    const chartOptions = {
      width: 600,
      height: 300,
      data: parseData(this.props.data),
      margin: {top: 5, right: 30, left: 20, bottom: 5},
    };
    return (
      <BarChart {...chartOptions}>
        <XAxis dataKey="name"/>
        <YAxis/>
        <CartesianGrid strokeDasharray="3 3"/>
        <Tooltip/>
        <Legend />
        <Bar dataKey="NT" fill={constants.blue} />
        <Bar dataKey="TR" fill={constants.purple} />
        <Bar dataKey="TM" fill={constants.orange} />
        <Bar dataKey="TB" fill={constants.green} />
        <Bar dataKey="TP" fill={constants.red} />
      </BarChart>
    );
  }
}

const parseData = (data) => {
  return Object.keys(data).map((tcgaToken) => {
    return {
      name: tcgaToken,
      NT: data[tcgaToken]["NT"],
      TR: data[tcgaToken]["TR"],
      TM: data[tcgaToken]["TM"],
      TB: data[tcgaToken]["TB"],
      TP: data[tcgaToken]["TP"],
    };
  });
};

export default Statistics;
