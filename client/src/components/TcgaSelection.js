import React, { PureComponent } from "react";
import styled from "styled-components";
import RaisedButton from "material-ui/RaisedButton";
import { List } from "material-ui/List";
import Subheader from "material-ui/Subheader";
import { connect } from "react-redux";

import {
  toggleTcgaToken,
  toggleTissueType
} from "../actions/datasetSelectionActions";

class TcgaSelection extends PureComponent {
  transferTcgaToken(tcgaToken) {
    this.props.toggleToken(tcgaToken);
  }

  transferTissueType(tissueType) {
    this.props.toggleTissue(tissueType);
  }

  render() {
    console.log("test");
    const tcgaTokens = this.props.tcgaTokens;
    const tissueTypes = this.props.tissueTypes;

    return (
      <StyledRoot>
        <StyledList>
          <Subheader>Cancer Type</Subheader>
          {tcgaTokens.map(tcgaToken => (
            <StyledButton
              label={tcgaToken.name}
              key={tcgaToken.name}
              value={tcgaToken.name}
              onClick={() => this.transferTcgaToken(tcgaToken)}
              selected={tcgaToken.selected}
            />
          ))}
        </StyledList>
        <StyledList>
          <Subheader>Tissue Type</Subheader>
          {tissueTypes.map(tissueType => (
            <StyledButton
              label={tissueType.name}
              key={tissueType.name}
              value={tissueType.name}
              onClick={() => this.transferTissueType(tissueType)}
              selected={tissueType.selected}
            />
          ))}
        </StyledList>
      </StyledRoot>
    );
  }
}

const StyledRoot = styled.div`
  display: inline-flex;
`;

const StyledButton = styled(RaisedButton)`
  margin: 1px;
  button {
    background-color: ${props =>
      props.selected
        ? props.theme.slightlyBoringBlue
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
