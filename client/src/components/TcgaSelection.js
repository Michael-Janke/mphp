import React, { PureComponent } from "react";
import styled from "styled-components";
import RaisedButton from "material-ui/RaisedButton";
import { List } from "material-ui/List";
import Subheader from "material-ui/Subheader";
import Dialog from "material-ui/Dialog";
import { connect } from "react-redux";

import {
  toggleTcgaToken,
  toggleTissueType
} from "../actions/datasetSelectionActions";

class TcgaSelection extends PureComponent {
  constructor(props) {
    super(props);
    this.state = { tissueTypeError: false };
  }

  render() {
    const tcgaTokens = this.props.tcgaTokens;
    const tissueTypes = this.props.tissueTypes;
    const healthyTissueTypes = tissueTypes.filter(
      tissueType => tissueType.isHealthy
    );
    const sickTissueTypes = tissueTypes.filter(
      tissueType => !tissueType.isHealthy
    );

    // dialog
    const actions = [
      <StyledButton
        label="Close"
        selected={true}
        primary={true}
        onClick={this.handleClose}
      />
    ];

    return (
      <StyledRoot>
        <Dialog
          title="Warning"
          actions={actions}
          open={this.state.tissueTypeError}
          onRequestClose={this.handleClose}
        >
          You have to select at least one healthy tissue type and one sick
          tissue type.
        </Dialog>
        <StyledList>
          <Subheader>Cancer Types</Subheader>
          {tcgaTokens.map(tcgaToken => (
            <StyledButton
              label={tcgaToken.name}
              key={tcgaToken.name}
              value={tcgaToken.name}
              onClick={() => this.transferTcgaToken(tcgaToken)}
              selected={tcgaToken.selected}
              primary={tcgaToken.selected}
            />
          ))}
        </StyledList>
        <StyledList>
          <Subheader>Healthy Tissue</Subheader>
          {healthyTissueTypes.map(tissueType => (
            <StyledButton
              label={tissueType.name}
              key={tissueType.name}
              value={tissueType.name}
              onClick={() => this.transferTissueType(tissueType)}
              selected={tissueType.selected}
              primary={tissueType.selected}
            />
          ))}
        </StyledList>
        <StyledList>
          <Subheader>Sick Tissue</Subheader>
          {sickTissueTypes.map(tissueType => (
            <StyledButton
              label={tissueType.name}
              key={tissueType.name}
              value={tissueType.name}
              onClick={() => this.transferTissueType(tissueType)}
              selected={tissueType.selected}
              primary={tissueType.selected}
            />
          ))}
        </StyledList>
      </StyledRoot>
    );
  }

  transferTcgaToken(tcgaToken) {
    this.props.toggleToken(tcgaToken);
  }

  transferTissueType(tissueType) {
    // only toggle if at least one healthy type and one sick type remain selected
    if (tissueType.selected) {
      const currentlySelected = this.props.tissueTypes.filter(
        tissue => tissue.selected && tissue.name[0] === tissueType.name[0]
      );
      if (currentlySelected.length <= 1) {
        this.setState({ tissueTypeError: true });
        return;
      }
    }
    this.props.toggleTissue(tissueType);
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
  button {
    background-color: ${props =>
      props.selected
        ? props.theme.boringBlue
        : props.theme.lightGray} !important;
  }
`;

const StyledList = styled(List)`
  display: flex;
  flex-direction: column;
  margin: 0px 16px;
  width: 120px;
`;

const mapStateToProps = state => {
  return {
    tcgaTokens: state.dataSelection.tcgaTokens,
    tissueTypes: state.dataSelection.tissueTypes
  };
};

const mapDispatchToProps = dispatch => {
  return {
    toggleToken: tcgaToken => {
      dispatch(toggleTcgaToken(tcgaToken));
    },
    toggleTissue: tissueType => {
      dispatch(toggleTissueType(tissueType));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(TcgaSelection);
