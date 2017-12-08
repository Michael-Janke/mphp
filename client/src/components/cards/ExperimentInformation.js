import React, { Component } from "react";
import styled from "styled-components";
import Card from "../Card";

class SelectDataset extends Component {
  render() {
    return (
      <Card
        title="Experiment Information"
        DataViewer={DataViewer}
        viewerProps={{ ...this.props.data }}
      />
    );
  }
}

class DataViewer extends Component {
  render() {
    return <StyledContent>Data Set: {this.props.dataset}</StyledContent>;
  }
}

const StyledContent = styled.p`
  margin-left: 16px;
`;

export default SelectDataset;
