import React, { Component } from "react";
import styled from "styled-components";

import Plot from "./Plot";
import Evaluation from "./Evaluation";
import GeneExploration from "./GeneExploration";

export default class Results extends Component {
  render() {
    const { result } = this.props;
    return (
      <div>
        {!result.isError ? (
          <StyledContent>
            <Columns>
              <Plot {...result} />
              <Evaluation {...result.evaluation} />
            </Columns>
            <GeneExploration {...result} />
          </StyledContent>
        ) : (
          <div>Server error</div>
        )}
      </div>
    );
  }
}

const StyledContent = styled.div`
  margin: 16px;
`;

const Columns = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-around;
`;
