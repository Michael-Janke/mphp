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
    // switch item between the two lists
  }

  transferTissueType(tissueType) {
    this.props.toggleTissue(tissueType);
  }

  render() {
    const tcgaTokens = Object.keys(this.props.data);
    const selectedTcgaTokens = this.props.tcgaTokens;
    const notSelectedTcgaTokens = tcgaTokens.filter(
      x => selectedTcgaTokens.indexOf(x) === -1
    );

    const tissueTypes = Object.keys(this.props.data[tcgaTokens[0]]);
    tissueTypes.push("healthy");
    tissueTypes.push("sick");
    tissueTypes.push("all");
    const selectedTissueTypes = this.props.tissueTypes;
    const notSelectedTissueTypes = tissueTypes.filter(
      x => selectedTissueTypes.indexOf(x) === -1
    );

    return (
      <StyledRoot>
        <StyledList>
          <Subheader>Cancer Type</Subheader>
          {tcgaTokens.map(tcgaToken => (
            <StyledButton
              key={tcgaToken}
              label={tcgaToken}
              onClick={() => this.transferTcgaToken(tcgaToken)}
              value={tcgaToken}
              selected={selectedTcgaTokens.indexOf(tcgaToken) >= 0}
            />
          ))}
        </StyledList>
        <StyledList>
          <Subheader>Tissue Type</Subheader>
          {tissueTypes.map(tissueType => (
            <StyledButton
              key={tissueType}
              label={tissueType}
              onClick={() => this.transferTissueType(tissueType)}
              value={tissueType}
              selected={selectedTissueTypes.indexOf(tissueType) >= 0}
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
