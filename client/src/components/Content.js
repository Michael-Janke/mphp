import React, { Component } from "react";
import { connect } from "react-redux";
import { load as loadStatistics } from "../actions/statisticsActions";
import { loadAlgorithms, runAlgorithm, updateRun } from "../actions/runActions";

import Run from "./Run";

class Content extends Component {
  constructor(props) {
    super(props);
    const { algorithms, statistics } = this.props.context;
    if (algorithms === null) {
      this.props.loadAlgorithms();
    }
    if (statistics === null) {
      this.props.loadStatistics();
    }
  }

  render() {
    const { runs, runAlgorithm, updateRun } = this.props;
    const {
      algorithms,
      statistics,
      tissueTypes,
      tcgaTokens
    } = this.props.context;
    return (
      <div className="content">
        {Object.keys(runs).map(runId => {
          const run = runs[runId];
          return (
            <Run
              key={runId}
              isLoading={!algorithms || !statistics || run.isLoading}
              isError={
                (statistics && statistics.isError) ||
                (algorithms && algorithms.isError)
              }
              runId={runId}
              algorithm={run.algorithm}
              result={run.result}
              algorithms={algorithms}
              statistics={statistics}
              tcgaTokens={tcgaTokens}
              tissueTypes={tissueTypes}
              runAlgorithm={runAlgorithm}
              updateRun={updateRun}
            />
          );
        })}
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    runs: state.runs,
    context: state.context
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadAlgorithms: () => {
      dispatch(loadAlgorithms());
    },
    loadStatistics: () => {
      dispatch(loadStatistics());
    },
    runAlgorithm: (runId, params) => {
      dispatch(runAlgorithm(runId, params));
    },
    updateRun: (runId, params) => {
      dispatch(updateRun(runId, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Content);
