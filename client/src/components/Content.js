import React, { Component } from "react";
import styled from "styled-components";

import ExperimentInformation from "./cards/ExperimentInformation";
import DataSelection from "./cards/DataSelectionContainer";
import FeatureAnalysis from "./cards/FeatureAnalysisContainer";
import Results from "./cards/ResultsContainer";

class Content extends Component {
  render() {
    return (
      <StyledRoot className="content">
        <StyledExperimentInformation data={{ dataset: "DATA SET 4" }} />
        <DataSelection />
        <FeatureAnalysis />
        <Results />
      </StyledRoot>
    );
  }
}

const StyledRoot = styled.div`
  overflow: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const StyledExperimentInformation = styled(ExperimentInformation)`
  margin-top: 150px;
`;

export default Content;
