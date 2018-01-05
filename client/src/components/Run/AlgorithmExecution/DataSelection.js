import React, { Component } from "react";
import styled from "styled-components";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

import { statisticsColors } from "../../../config/colors";
import TcgaSelection from "./TcgaSelection";

export default class DataSelection extends Component {
  render() {
    const chartOptions = {
      data: this.parseData(),
      margin: { top: 5, right: 30, left: 20, bottom: 5 }
    };

    return (
      <StyledContent>
        <TcgaSelection {...this.props} />
        <DiagramContainer>
          <ResponsiveContainer height="100%" width="100%">
            <BarChart {...chartOptions}>
              <XAxis dataKey="name" />
              <YAxis />
              <CartesianGrid strokeDasharray="3 3" />
              <Tooltip />
              <Legend />
              {this.renderBars()}
            </BarChart>
          </ResponsiveContainer>
        </DiagramContainer>
      </StyledContent>
    );
  }

  parseData() {
    const { statistics, algorithm } = this.props;
    const tcgaTokens = algorithm.cancerTypes;
    const tissueTypes = [
      ...algorithm.healthyTissueTypes,
      ...algorithm.sickTissueTypes
    ];

    return tcgaTokens.map(tcgaToken => {
      const result = { name: tcgaToken.name };
      tissueTypes.forEach(tissueType => {
        result[tissueType] = statistics[tcgaToken][tissueType];
      });
      return result;
    });
  }

  renderBars() {
    const tissueTypes = [
      ...this.props.algorithm.healthyTissueTypes,
      ...this.props.algorithm.sickTissueTypes
    ];
    const dataKeys = tissueTypes.map((name, index) => {
      return { name, color: statisticsColors[index] };
    });
    return dataKeys.map((dataKey, index) => {
      return (
        <Bar
          key={`bar-${dataKey.name}`}
          dataKey={dataKey.name}
          fill={dataKey.color}
          maxBarSize={30}
        />
      );
    });
  }
}

const StyledContent = styled.div`
  display: flex;
`;

const DiagramContainer = styled.div`
  width: 100%;
`;
