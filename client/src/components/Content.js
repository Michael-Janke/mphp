import React, { Component } from "react";
import { connect } from "react-redux";
import { load as loadStatistics } from "../actions/statisticsActions";
import {
  loadAlgorithms,
  runAlgorithm,
  updateAlgorithm
} from "../actions/runActions";

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
    const { runs, context, runAlgorithm, updateAlgorithm } = this.props;
    const { algorithms, statistics } = context;
    return (
      <div className="content">
        {Object.keys(runs).map(runId => {
          const { algorithm, result, isLoading } = runs[runId];
          return (
            <Run
              key={runId}
              isLoading={!algorithms || !statistics || isLoading}
              isError={
                (statistics && statistics.isError) ||
                (algorithms && algorithms.isError)
              }
              runId={runId}
              algorithm={algorithm}
              result={result}
              runAlgorithm={runAlgorithm}
              updateAlgorithm={updateAlgorithm}
              {...context}
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
    updateAlgorithm: (runId, params) => {
      dispatch(updateAlgorithm(runId, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Content);
