import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import SelectField from "material-ui/SelectField";
import MenuItem from "material-ui/MenuItem";
import TextField from "material-ui/TextField";
import styled from "styled-components";

import { boringBlue } from "../../config/colors";
import Card from "../Card";
import Plot from "./Plot";

export default class FeatureAnalysis extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedAlgorithm: null,
      params: {}
    };
    if (this.props.algorithms === null) {
      this.props.loadAlgorithms();
    }
  }

  render() {
    const runnable = this.state.selectedAlgorithm !== null;

    return (
      <div className="feature-analysis">
        <Card
          title={"Feature Analysis"}
          isLoading={!this.props.algorithms}
          isError={this.props.algorithms && this.props.algorithms.isError}
        >
          {this.props.algorithms &&
            !this.props.algorithms.isError && (
              <StyledMenu>
                <StyledOptions>
                  <StyledSelectField
                    floatingLabelText="Algorithm"
                    floatingLabelFixed={true}
                    hintText="Select algorithm..."
                    value={runnable ? this.state.selectedAlgorithm.key : null}
                    onChange={this.selectAlgorithm.bind(this)}
                    autoWidth={true}
                    selectedMenuItemStyle={{ color: boringBlue }}
                  >
                    {this.props.algorithms.map(this.renderMenuItem)}
                  </StyledSelectField>
                  {runnable
                    ? this.state.selectedAlgorithm.parameters.map(
                        this.renderParameter.bind(this)
                      )
                    : null}
                </StyledOptions>
                <CardActions>
                  <StyledButton
                    title={
                      runnable
                        ? `Run ${this.state.selectedAlgorithm.name}`
                        : `Please select an algorithm`
                    }
                    label="Run"
                    primary={true}
                    onClick={() => {
                      this.executeAlgorithm();
                    }}
                    disabled={!runnable}
                  />
                </CardActions>
              </StyledMenu>
            )}
        </Card>
        <StyledCards>
          {Object.keys(this.props.runs).map(this.renderRun.bind(this))}
        </StyledCards>
      </div>
    );
  }

  renderRun(runId) {
    const run = this.props.runs[runId];
    return (
      <Card
        title={run.params.name}
        isLoading={!run.result}
        isError={run.result && run.result.isError}
        key={`run-${runId}`}
      >
        <Plot {...run.result} />
      </Card>
    );
  }

  renderMenuItem(algorithm, index) {
    return (
      <MenuItem
        key={`algorithm-option-${index}`}
        value={algorithm.key}
        primaryText={algorithm.name}
      />
    );
  }

  renderParameter(parameter, index) {
    return (
      <StyledTextField
        key={parameter.key}
        id={parameter.key}
        defaultValue={parameter.default}
        hintText={parameter.default}
        floatingLabelText={parameter.name}
        floatingLabelFixed={true}
        type="number"
        onChange={this.changeParameter.bind(this)}
      />
    );
  }

  changeParameter(event, index, key) {
    const params = this.state.params;
    params[event.target.id] = event.target.value;
    this.setState({
      params
    });
  }

  selectAlgorithm(event, index, key) {
    const selectedAlgorithm = this.props.algorithms.find(
      algorithm => algorithm.key === key
    );
    const params = {};
    selectedAlgorithm.parameters.forEach(param => {
      params[param.key] = param.default;
    });
    this.setState({
      selectedAlgorithm,
      params
    });
  }

  executeAlgorithm() {
    const { selectedAlgorithm } = this.state;
    const cancerTypes = this.props.dataSelection.tcgaTokens
      .filter(token => token.selected)
      .map(token => token.name);
    const sickTissueTypes = this.props.dataSelection.tissueTypes
      .filter(tissueType => !tissueType.isHealthy && tissueType.selected)
      .map(tissueType => tissueType.name);
    const healthyTissueTypes = this.props.dataSelection.tissueTypes
      .filter(tissueType => tissueType.isHealthy && tissueType.selected)
      .map(tissueType => tissueType.name);
    const params = {
      name: selectedAlgorithm.name,
      key: selectedAlgorithm.key,
      cancerTypes,
      sickTissueTypes,
      healthyTissueTypes,
      parameters: {
        ...this.state.params
      }
    };
    this.props.runAlgorithm(params);
  }
}

const CardActions = styled.div`
  display: flex;
  flex-direction: row-reverse;
`;

const StyledButton = styled(RaisedButton)`
  && {
    margin: 12px;
  }
  button {
    background: ${props => props.theme.boringBlue} !important;
  }
  button:disabled {
    background: ${props => props.theme.lightGray} !important;
  }
`;

const StyledCards = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

const StyledMenu = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 16px;
`;

const StyledOptions = styled.div`
  display: flex;
  align-items: center;
`;

const StyledSelectField = styled(SelectField)`
  button {
    fill: ${props => props.theme.textColor} !important;
  }
`;

const StyledTextField = styled(TextField)`
  margin-left: ${props => props.theme.mediumSpace};
`;
