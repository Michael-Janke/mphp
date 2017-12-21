import React, { Component } from "react";
import ExperimentInformation from "./cards/ExperimentInformation";
import DataSelection from "./cards/DataSelectionContainer";
import FeatureAnalysis from "./cards/FeatureAnalysisContainer";
import Results from "./cards/ResultsContainer";

class Content extends Component {
  render() {
    return (
      <div className="content">
        <ExperimentInformation data={{ dataset: "DATA SET 4" }} />
        <DataSelection />
        <FeatureAnalysis />
        <Results />
      </div>
    );
  }
}

export default Content;
