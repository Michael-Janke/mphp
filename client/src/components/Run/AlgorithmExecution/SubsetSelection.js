import React, { PureComponent } from "react";
import styled from "styled-components";
import RaisedButton from "material-ui/RaisedButton";
import { List } from "material-ui/List";
import Subheader from "material-ui/Subheader";
import { connect } from "react-redux";
import { FormattedMessage } from "react-intl";

import { toggleTcgaToken, toggleTissueType } from "../../../actions/runActions";
import { isHealthy } from "../../../utils";
import TooltipBox from "../../TooltipBox";

class SubsetSelection extends PureComponent {
  render() {
    const { algorithm, disabled } = this.props;
    const { cancerTypes, sampleTypes } = this.props.statistics[
      this.props.dataset
    ];
    const healthyTissueTypes = sampleTypes.filter(tissueType =>
      isHealthy(tissueType)
    );
    const sickTissueTypes = sampleTypes.filter(
      tissueType => !isHealthy(tissueType)
    );
    const selectedHealthyTissueTypes = algorithm.healthyTissueTypes;
    const selectedSickTissueTypes = algorithm.sickTissueTypes;

    return (
      <StyledRoot>
        <StyledList>
          <Subheader>Cancer Types</Subheader>
          {cancerTypes.map(
            tcgaToken =>
              disabled && !algorithm.cancerTypes.includes(tcgaToken) ? null : (
                <TooltipBox
                  key={tcgaToken}
                  text={<FormattedMessage id={`CancerTypes.${tcgaToken}`} />}
                  position={"right"}
                >
                  <StyledButton
                    label={tcgaToken}
                    value={tcgaToken}
                    onClick={() => this.transferTcgaToken(tcgaToken)}
                    selected={algorithm.cancerTypes.includes(tcgaToken)}
                    primary={algorithm.cancerTypes.includes(tcgaToken)}
                    disabled={disabled}
                  />
                </TooltipBox>
              )
          )}
        </StyledList>
        <StyledList>
          <Subheader>Healthy Tissue</Subheader>
          {healthyTissueTypes.map(
            tissueType =>
              disabled &&
              !selectedHealthyTissueTypes.includes(tissueType) ? null : (
                <TooltipBox
                  key={tissueType}
                  text={<FormattedMessage id={`HealthyTissue.${tissueType}`} />}
                  position={"right"}
                >
                  <StyledButton
                    label={tissueType}
                    value={tissueType}
                    onClick={() => this.transferTissueType(tissueType)}
                    selected={selectedHealthyTissueTypes.includes(tissueType)}
                    primary={selectedHealthyTissueTypes.includes(tissueType)}
                    disabled={disabled}
                  />
                </TooltipBox>
              )
          )}
          <Subheader>Sick Tissue</Subheader>
          {sickTissueTypes.map(
            tissueType =>
              disabled &&
              !selectedSickTissueTypes.includes(tissueType) ? null : (
                <TooltipBox
                  key={tissueType}
                  text={<FormattedMessage id={`SickTissue.${tissueType}`} />}
                  position={"right"}
                >
                  <StyledButton
                    label={tissueType}
                    value={tissueType}
                    onClick={() => this.transferTissueType(tissueType)}
                    selected={selectedSickTissueTypes.includes(tissueType)}
                    primary={selectedSickTissueTypes.includes(tissueType)}
                    disabled={disabled}
                  />
                </TooltipBox>
              )
          )}
        </StyledList>
      </StyledRoot>
    );
  }

  transferTcgaToken(tcgaToken) {
    this.props.toggleToken(this.props.runId, this.props.algorithm, tcgaToken);
  }

  transferTissueType(tissueType) {
    this.props.toggleTissue(this.props.runId, this.props.algorithm, tissueType);
  }

  handleClose = () => {
    this.setState({ tissueTypeError: false });
  };
}

const StyledRoot = styled.div`
  display: inline-flex;
`;

const StyledButton = styled(RaisedButton)`
  margin: 1px;
  width: 100%;
  button {
    background-color: ${props =>
      props.selected
        ? props.theme.boringBlue
        : props.theme.lightGray} !important;
  }
  button:disabled {
    background: ${props => props.theme.lightGray} !important;
  }
`;

const StyledList = styled(List)`
  display: flex;
  flex-direction: column;
  margin: 0px 16px;
  width: 120px;
`;

const mapStateToProps = state => ({});

const mapDispatchToProps = dispatch => {
  return {
    toggleToken: (runId, algorithm, tcgaToken) => {
      dispatch(toggleTcgaToken(runId, algorithm, tcgaToken));
    },
    toggleTissue: (runId, algorithm, tissueType) => {
      dispatch(toggleTissueType(runId, algorithm, tissueType));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(SubsetSelection);
