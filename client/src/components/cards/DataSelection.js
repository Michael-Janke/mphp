import React, { Component } from "react";
import styled from "styled-components";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

import { statisticsColors } from "../../config/colors";
import Card from "../Card";
import TcgaSelection from "../TcgaSelection";

export default class DataSelection extends Component {
  constructor(props) {
    super(props);
    if (this.props.statistics === null) {
      this.props.loadStatistics();
    }
  }

  render() {
    const chartOptions = {
      width: 100 * this.props.tcgaTokens.filter(token => token.selected).length,
      height: 400,
      data: this.parseData(),
      margin: { top: 5, right: 30, left: 20, bottom: 5 }
    };

    return (
      <Card
        title={"Data Selection"}
        isLoading={!this.props.statistics}
        isError={this.props.statistics && this.props.statistics.isError}
      >
        {this.props.statistics &&
          !this.props.statistics.isError && (
            <StyledContent>
              <TcgaSelection data={this.props.statistics} />
              <BarChart {...chartOptions}>
                <XAxis dataKey="name" />
                <YAxis />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Legend />
                {this.renderBars()}
              </BarChart>
            </StyledContent>
          )}
      </Card>
    );
  }

  parseData() {
    const { statistics, tcgaTokens, tissueTypes } = this.props;
    const currentTcgaTokens = tcgaTokens.filter(token => token.selected);
    const currentTissueTypes = tissueTypes.filter(
      tissueType => tissueType.selected
    );
    return currentTcgaTokens.map(tcgaToken => {
      const result = { name: tcgaToken.name };
      currentTissueTypes.forEach(tissueType => {
        result[tissueType.name] = statistics[tcgaToken.name][tissueType.name];
      });
      return result;
    });
  }

  renderBars() {
    const tissueTypesWithColors = this.props.tissueTypes;
    tissueTypesWithColors.forEach((tissueType, index) => {
      tissueType.color = statisticsColors[index];
    });
    const dataKeys = tissueTypesWithColors.filter(
      tissueType => tissueType.selected
    );
    return dataKeys.map((dataKey, index) => {
      return (
        <Bar
          key={`bar-${dataKey.name}`}
          dataKey={dataKey.name}
          fill={dataKey.color}
        />
      );
    });
  }
}

const StyledContent = styled.div`
  display: inline-flex;
  flex-direction: row;
`;
