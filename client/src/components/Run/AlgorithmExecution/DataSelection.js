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
        {this.props.disabled ? null : (
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
        )}
      </StyledContent>
    );
  }

  parseData() {
    const { counts, cancerTypes }  = this.props.statistics[this.props.dataset];

    return cancerTypes.map(cancerType => ({
      name: cancerType,
      ...counts[cancerType] 
    }));
  }

  renderBars() {
    const { sampleTypes }  = this.props.statistics[this.props.dataset];
    const dataKeys = sampleTypes.map((name, index) => (
      { name, 
        color: statisticsColors[index] 
      }));
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
