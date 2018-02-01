import React, { Component } from "react";
import { connect } from "react-redux";
import styled from "styled-components";
import FlatButton from "material-ui/FlatButton";
import Dialog from "material-ui/Dialog";
import { loadContext } from "../actions/contextActions";
import { startRun, updateRun, deleteRun } from "../actions/runActions";
import Spinner from "./Spinner";

import Run from "./Run";

class Content extends Component {
  constructor(props) {
    super(props);
    const context = this.props.context;
    if (!context.datasets) {
      this.props.loadContext();
    }
    this.state = { maxRunsPerRow: 0 };
    this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
  }

  render() {
    const { runs, context, startRun, updateRun, deleteRun } = this.props;
    return (
      <ContentContainer>
        {context.datasets ? (
          [
            ...Object.keys(runs)
              .reverse()
              .map(runId => {
                const run = runs[runId];
                return (
                  <Run
                    key={runId}
                    runId={runId}
                    {...run}
                    startRun={startRun}
                    updateRun={updateRun}
                    deleteRun={deleteRun}
                    {...context}
                  />
                );
              }),
            ...this.addMissingRuns()
          ]
        ) : (
          <Dialog
            actions={[
              <FlatButton
                label="Retry"
                primary={true}
                disabled={!context.isError}
                onClick={this.props.loadContext}
              />
            ]}
            modal={false}
            open={!context.datasets}
          >
            {context.isError ? (
              <LoadingText>
                Couldn't load context data. Retry? ({context.error.message})
              </LoadingText>
            ) : (
              <StyledSpinnerContainer>
                <Spinner size={20} />
                <LoadingText>loading context data</LoadingText>
              </StyledSpinnerContainer>
            )}
          </Dialog>
        )}
      </ContentContainer>
    );
  }

  addMissingRuns() {
    const currentRuns = Object.keys(this.props.runs).length;
    const missingRuns =
      this.state.maxRunsPerRow - currentRuns % this.state.maxRunsPerRow;
    var result = [];
    for (let i = 0; i < missingRuns; i++) {
      result.push(<EmptyRun />);
    }
    return result;
  }

  componentDidMount() {
    this.updateWindowDimensions();
    window.addEventListener("resize", this.updateWindowDimensions);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.updateWindowDimensions);
  }

  updateWindowDimensions() {
    const maxRunsPerRow = Math.floor(window.innerWidth / 950);
    this.setState({ maxRunsPerRow });
  }
}

const ContentContainer = styled.div`
  display: flex;
  flex-flow: row wrap;
`;

const StyledSpinnerContainer = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  height: 100px;
`;

const LoadingText = styled.div`
  font-size: ${props => props.theme.h1};
  margin-left: 10px;
`;

const EmptyRun = styled.div`
  margin: ${props => props.theme.mediumSpace};
  padding: ${props => props.theme.mediumSpace};
  min-width: 800px;
  max-width: 1000px;
  flex: 1;
`;

const mapStateToProps = state => {
  return {
    runs: state.runs,
    context: state.context
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadContext: () => {
      dispatch(loadContext());
    },
    startRun: (runId, params) => {
      dispatch(startRun(runId, params));
    },
    deleteRun: runId => {
      dispatch(deleteRun(runId));
    },
    updateRun: (runId, params) => {
      dispatch(updateRun(runId, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Content);
