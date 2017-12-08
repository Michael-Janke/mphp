import React, { Component } from "react";
import { connect } from "react-redux";
import styled, { withTheme } from "styled-components";
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
import TcgaSelection from "../TcgaSelection";
import { load } from "../../actions/statisticsActions";

class DataSelection extends Component {
  constructor(props) {
    super(props);
    if (this.props.statistics === null) {
      this.props.loadStatistics();
    }
  }

  render() {
    return (
      <Card
        title={"Data Selection"}
        DataViewer={withTheme(DataViewer)}
        isLoading={!this.props.statistics}
        viewerProps={{
          data: this.props.statistics,
          tcgaTokens: this.props.tcgaTokens,
          tissueTypes: this.props.tissueTypes
        }}
      />
    );
  }
}

class DataViewer extends Component {
  render() {
    const chartOptions = {
      width: 100 * this.props.tcgaTokens.filter(token => token.selected).length,
      height: 400,
      data: this.parseData(),
      margin: { top: 5, right: 30, left: 20, bottom: 5 }
    };
    return (
      <StyledRoot>
        <TcgaSelection data={this.props.data} />
        <BarChart {...chartOptions}>
          <XAxis dataKey="name" />
          <YAxis />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Legend />
          {this.renderBars()}
        </BarChart>
      </StyledRoot>
    );
  }

  parseData() {
    const { data, tcgaTokens, tissueTypes } = this.props;
    const currentTcgaTokens = tcgaTokens.filter(token => token.selected);
    return currentTcgaTokens.map(tcgaToken => {
      return {
        name: tcgaToken.name,
        NT: data[tcgaToken.name]["NT"],
        TR: data[tcgaToken.name]["TR"],
        TM: data[tcgaToken.name]["TM"],
        TB: data[tcgaToken.name]["TB"],
        TP: data[tcgaToken.name]["TP"]
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

const StyledRoot = styled.div`
  display: inline-flex;
  flex-direction: row;
`;

const mapStateToProps = state => {
  return {
    statistics: state.statistics,
    tcgaTokens: state.dataSelection.tcgaTokens,
    tissueTypes: state.dataSelection.tissueTypes
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadStatistics: () => {
      dispatch(load());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(DataSelection);
