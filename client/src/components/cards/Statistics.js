import React, { Component } from "react";
import { connect } from "react-redux";
import { load } from "../../actions/statisticsActions";
import { withTheme } from "styled-components";
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

class Statistics extends Component {
  constructor(props) {
    super(props);
    if (this.props.statistics === null) {
      this.props.loadStatistics();
    }
  }

  render() {
    return (
      <Card
        title={"Statistics"}
        data={this.props.statistics}
        DataViewer={withTheme(DataViewer)}
      />
    );
  }
}

class DataViewer extends Component {
  render() {
    const chartOptions = {
      width: 600,
      height: 300,
      data: this.parseData(),
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

  parseData() {
    const { data } = this.props;
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

const mapStateToProps = state => {
  return {
    statistics: state.statistics
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadStatistics: () => {
      dispatch(load());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Statistics);
