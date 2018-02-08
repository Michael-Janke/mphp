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
  Legend,
  Label
} from "recharts";

import { statisticsColors } from "../../../config/colors";

export default class DataSelection extends Component {
  render() {
    const chartOptions = {
      data: this.parseData(),
      margin: { top: 5, right: 30, left: 20, bottom: 25 },
      layout: "vertical"
    };

    return (
      <StyledContent>
        {this.props.disabled ? null : (
          <DiagramContainer>
            <ResponsiveContainer width={300}>
              <BarChart {...chartOptions}>
                <XAxis type="number">
                  <Label
                    position="bottom"
                    offset={-3}
                    value={"Number of Samples"}
                  />
                </XAxis>
                <YAxis dataKey="name" type="category" />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Legend verticalAlign="top" height={36} />
                {this.renderBars()}
              </BarChart>
            </ResponsiveContainer>
          </DiagramContainer>
        )}
      </StyledContent>
    );
  }

  parseData() {
    const { counts, cancerTypes } = this.props.statistics[this.props.dataset];
    const { algorithm } = this.props;

    // necessary to get the same ordering in diagram
    const selectedCancerTypes = cancerTypes.filter(cancerType =>
      algorithm.cancerTypes.includes(cancerType)
    );

    return selectedCancerTypes.map(cancerType => ({
      name: cancerType,
      ...counts[cancerType]
    }));
  }

  renderBars() {
    const tissueTypes = [
      ...this.props.algorithm.healthyTissueTypes,
      ...this.props.algorithm.sickTissueTypes
    ];

    const dataKeys = tissueTypes.map((name, index) => ({
      name,
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

const XAxisLabel = styled.span`
  color: blue;
`;

const StyledContent = styled.div`
  display: flex;
`;

const DiagramContainer = styled.div`
  width: 100%;
`;
