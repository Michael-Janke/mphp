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
          >
            {Object.keys(datasets).map((dataset) => <MenuItem
              key={dataset}
              value={dataset}
              primaryText={datasets[dataset]}/>)
            }
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
          >
            {algorithms.map(this.renderMenuItem)}
          </StyledSelectField>
          {algorithm.key &&
            this.algorithmDescription().parameters.map(
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
        value={algorithm.key}
        primaryText={algorithm.name}
      />
    );
  }

  renderParameter(disabled, parameter, index) {
    return (
      <StyledTextField
        key={parameter.key}
        id={parameter.key}
        value={
          this.props.algorithm.parameters[parameter.key] || parameter.default
        }
        hintText={parameter.default}
        floatingLabelText={parameter.name}
        floatingLabelFixed={true}
        type="number"
        onChange={this.changeParameter.bind(this)}
        disabled={disabled}
      />
    );
  }

  changeDataset(event, index, dataset) {
    const { runId, updateRun } = this.props;
    updateRun(runId, { dataset: dataset });
  }

  changeParameter(event, index, key) {
    const { algorithm, runId, updateRun } = this.props;
    const updatedParams = {
      ...algorithm.parameters,
      [event.target.id]: parseInt(event.target.value, 10)
    };
    updateRun(runId, { algorithm: {...algorithm, parameters: updatedParams} });
  }

  selectAlgorithm(event, index, key) {
    const { algorithm, runId, updateRun } = this.props;
    const updatedAlgorithm = this.algorithmDescription(key);
    const updatedValues = {
      name: updatedAlgorithm.name,
      key: updatedAlgorithm.key,
      parameters: updatedAlgorithm.parameters.reduce((reducedParams, param) => {
        return { ...reducedParams, [param.key]: param.default };
      }, {})
    };
    updateRun(runId, { algorithm: {...algorithm, ...updatedValues}});
  }

  algorithmDescription(algorithmKey) {
    algorithmKey = algorithmKey || this.props.algorithm.key;
    return this.props.algorithms.find(
      algorithm => algorithm.key === algorithmKey
    );
  }
}

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
