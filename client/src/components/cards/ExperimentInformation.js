import React, { Component } from "react";
import styled from "styled-components";
import Card from "../Card";

class SelectDataset extends Component {
  render() {
    return (
      <Card
        title="Experiment Information"
        data={this.props.data}
        DataViewer={DataViewer}
      />
    );
  }
}

class DataViewer extends Component {
  render() {
    return <StyledContent>Data Set: {this.props.data.dataset}</StyledContent>;
  }
}

const StyledContent = styled.p`
  margin-left: 16px;
`;

export default SelectDataset;
