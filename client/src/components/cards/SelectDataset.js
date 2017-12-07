import React, { Component } from "react";
import styled from "styled-components";
import Card from "../Card";

const StyledContent = styled.p`
  margin-left: 16px;
`;

class SelectDataset extends Component {
  render() {
    return (
      <Card
        title={this.props.title}
        data={this.props.data}
        DataViewer={DataViewer}
        width="100%"
      />
    );
  }
}

class DataViewer extends Component {
  render() {
    return <StyledContent>{this.props.data}</StyledContent>;
  }
}

export default SelectDataset;
