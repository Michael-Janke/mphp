import React, { Component } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";
import Card from "../Card";
import { withTheme } from "styled-components";

const ROUTE = "/statistics";
const TITLE = "Statistics";

class Statistics extends Component {
  render() {
    return <Card route={ROUTE} title={TITLE} DataView={withTheme(DataView)} />;
  }
}

class DataView extends Component {
  render() {
    const chartOptions = {
      width: 600,
      height: 300,
      data: parseData(this.props.data),
      margin: { top: 5, right: 30, left: 20, bottom: 5 }
    };
    return (
      <BarChart {...chartOptions}>
        <XAxis dataKey="name" />
        <YAxis />
        <CartesianGrid strokeDasharray="3 3" />
        <Tooltip />
        <Legend />
        {this.renderBars()}
      </BarChart>
    );
  }

  renderBars() {
    const dataKeys = ["NT", "TR", "TM", "TB", "TP"];
    return dataKeys.map((dataKey, index) => {
      return (
        <Bar
          key={`bar-${dataKey}`}
          dataKey={dataKey}
          fill={this.props.theme.statisticsColors[index]}
        />
      );
    });
  }
}

const parseData = data => {
  return Object.keys(data).map(tcgaToken => {
    return {
      name: tcgaToken,
      NT: data[tcgaToken]["NT"],
      TR: data[tcgaToken]["TR"],
      TM: data[tcgaToken]["TM"],
      TB: data[tcgaToken]["TB"],
      TP: data[tcgaToken]["TP"]
    };
  });
};

export default Statistics;
