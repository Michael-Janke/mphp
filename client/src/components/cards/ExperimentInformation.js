import React, { Component } from "react";
import styled from "styled-components";

import Card from "../Card";

export default class SelectDataset extends Component {
  render() {
    return (
      <Card className={this.props.className} title="Experiment Information">
        <StyledContent>Data Set: {this.props.data.dataset}</StyledContent>
      </Card>
    );
  }
}

const StyledContent = styled.div`
  display: inline-flex;
  flex-direction: row;
  margin: 16px;
`;
