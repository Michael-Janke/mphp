import React, { Component } from "react";
import SelectField from "material-ui/SelectField";
import MenuItem from "material-ui/MenuItem";
import TextField from "material-ui/TextField";
import styled from "styled-components";

import { boringBlue } from "../../../config/colors";
import { isHealthy } from "../../../utils";

export default class AlgorithmSelection extends Component {
  render() {
    const { algorithms, selectedAlgorithm, isRunnable } = this.props;
    return (
      <StyledMenu>
        <StyledOptions>
          <StyledSelectField
            floatingLabelText="Algorithm"
            floatingLabelFixed={true}
            hintText="Select algorithm..."
            value={isRunnable ? selectedAlgorithm.key : null}
            onChange={this.selectAlgorithm.bind(this)}
            autoWidth={true}
            selectedMenuItemStyle={{ color: boringBlue }}
          >
            {algorithms.map(this.renderMenuItem)}
          </StyledSelectField>
          {isRunnable
            ? selectedAlgorithm.parameters.map(this.renderParameter.bind(this))
            : null}
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
    const updatedParams = {
      ...this.props.algorithm.parameters,
      [event.target.id]: parseInt(event.target.value, 10)
    };
    this.props.updateRun(
      this.props.runId,
      this.buildParams({ parameters: updatedParams })
    );
  }

  selectAlgorithm(event, index, key) {
    const updatedAlgorithm = this.props.algorithms.find(
      algorithm => algorithm.key === key
    );
    const updatedValues = {
      name: updatedAlgorithm.name,
      key: updatedAlgorithm.key,
      parameters: updatedAlgorithm.parameters.reduce((reducedParams, param) => {
        return { ...reducedParams, [param.key]: param.default };
      }, {})
    };
    this.props.updateRun(this.props.runId, this.buildParams(updatedValues));
  }

  buildParams(updatedValues = {}) {
    const { tcgaTokens, tissueTypes, selectedAlgorithm } = this.props;
    const cancerTypes = tcgaTokens
      .filter(token => token.selected)
      .map(token => token.name);
    const sickTissueTypes = tissueTypes
      .filter(tissueType => !isHealthy(tissueType) && tissueType.selected)
      .map(tissueType => tissueType.name);
    const healthyTissueTypes = tissueTypes
      .filter(tissueType => isHealthy(tissueType) && tissueType.selected)
      .map(tissueType => tissueType.name);

    return selectedAlgorithm === null
      ? { ...updatedValues, cancerTypes, sickTissueTypes, healthyTissueTypes }
      : {
          name: selectedAlgorithm.name,
          key: selectedAlgorithm.key,
          cancerTypes,
          sickTissueTypes,
          healthyTissueTypes,
          parameters: selectedAlgorithm.parameters,
          ...updatedValues
        };
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
