import React, { Component } from "react";
import SelectField from "material-ui/SelectField";
import MenuItem from "material-ui/MenuItem";
import TextField from "material-ui/TextField";
import styled from "styled-components";

import { boringBlue } from "../../../config/colors";

export default class AlgorithmSelection extends Component {
  render() {
    const { algorithms, algorithm, datasets, dataset } = this.props;
    return (
      <StyledMenu>
        <StyledOptions>
          <StyledSelectField
            floatingLabelText="Dataset"
            floatingLabelFixed={true}
            hintText="Select dataset..."
            value={dataset || null}
            onChange={this.changeDataset.bind(this)}
            autoWidth={true}
            selectedMenuItemStyle={{ color: boringBlue }}
            disabled={this.props.disabled}
            style={{ width: 220 }}
          >
            {Object.keys(datasets).map(dataset => (
              <MenuItem
                key={dataset}
                value={dataset}
                primaryText={datasets[dataset]}
              />
            ))}
          </StyledSelectField>
          <StyledSelectField
            floatingLabelText="Algorithm"
            floatingLabelFixed={true}
            hintText="Select algorithm..."
            value={algorithm.key || null}
            onChange={this.selectAlgorithm.bind(this)}
            autoWidth={true}
            selectedMenuItemStyle={{ color: boringBlue }}
            disabled={this.props.disabled}
            style={{ width: 220 }}
          >
            {Object.keys(algorithms).map(this.renderMenuItem.bind(this))}
          </StyledSelectField>
          {algorithm.key &&
            algorithms &&
            Object.keys(algorithms[algorithm.key].parameters).map(
              this.renderParameter.bind(this, this.props.disabled)
            )}
        </StyledOptions>
      </StyledMenu>
    );
  }

  renderMenuItem(algorithm, index) {
    // TODO only render if sufficient cancer and tissue types are selected (see #61)
    return (
      <MenuItem
        key={`algorithm-option-${index}`}
        value={algorithm}
        primaryText={this.props.algorithms[algorithm].name}
      />
    );
  }

  renderParameter(disabled, parameter, index) {
    var parameterObj = this.props.algorithms[this.props.algorithm.key]
      .parameters[parameter];
    return (
      <StyledTextField
        key={parameter}
        id={parameter}
        value={
          this.props.algorithm.parameters[parameter] || parameterObj.default
        }
        hintText={parameterObj.default}
        floatingLabelText={parameterObj.name}
        floatingLabelFixed={true}
        type="number"
        onChange={this.changeParameter.bind(this)}
        disabled={disabled}
        style={{ width: 210 }}
      />
    );
  }

  changeDataset(event, index, dataset) {
    const { runId, updateRun } = this.props;
    // necessary because not all cancer types are available in every data set
    const algorithm = {
      cancerTypes: ["THCA"],
      healthyTissueTypes: ["NT"],
      sickTissueTypes: ["TP"]
    };
    updateRun(runId, { dataset: dataset, algorithm: algorithm });
  }

  changeParameter(event, index, key) {
    const { algorithm, runId, updateRun } = this.props;
    const updatedParams = {
      ...algorithm.parameters,
      [event.target.id]: parseInt(event.target.value, 10)
    };
    updateRun(runId, {
      algorithm: { ...algorithm, parameters: updatedParams }
    });
  }

  selectAlgorithm(event, index, key) {
    const { algorithm, algorithms, runId, updateRun } = this.props;
    const parameters = algorithms[key].parameters;
    const updatedValues = {
      name: algorithms[key].name,
      key,
      parameters: Object.keys(parameters).reduce((reducedParams, param) => {
        return { ...reducedParams, [param]: parameters[param].default };
      }, {})
    };
    updateRun(runId, { algorithm: { ...algorithm, ...updatedValues } });
  }
}

const StyledMenu = styled.div``;

const StyledOptions = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 16px;
`;

const StyledSelectField = styled(SelectField)`
  button {
    fill: ${props => props.theme.textColor} !important;
  }
`;

const StyledTextField = styled(TextField)`
  margin-left: ${props => props.theme.mediumSpace};
`;
