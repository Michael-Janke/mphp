import React, { PureComponent } from "react";
import styled from "styled-components";
import RaisedButton from "material-ui/RaisedButton";
import { List } from "material-ui/List";
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
          <label>Not selected Tcga</label>
          {notSelectedTcgaTokens.map(tcgaToken => (
            <StyledButton
              primary={true}
              key={tcgaToken}
              onClick={() => this.transferTcgaToken(tcgaToken)}
              value={tcgaToken}
            >
              {tcgaToken}
            </StyledButton>
          ))}
        </StyledList>
        <StyledList>
          <label>Selected Tcga</label>
          {selectedTcgaTokens.map(tcgaToken => (
            <StyledButton
              secondary={true}
              key={tcgaToken}
              onClick={() => this.transferTcgaToken(tcgaToken)}
              value={tcgaToken}
              selected={true}
            >
              {tcgaToken}
            </StyledButton>
          ))}
        </StyledList>
        <StyledList>
          <label>Not selected Tissue</label>
          {notSelectedTissueTypes.map(tissueType => (
            <StyledButton
              primary={true}
              key={tissueType}
              onClick={() => this.transferTissueType(tissueType)}
              value={tissueType}
            >
              {tissueType}
            </StyledButton>
          ))}
        </StyledList>
        <StyledList>
          <label>Selected Tissue</label>
          {selectedTissueTypes.map(tissueType => (
            <StyledButton
              secondary={true}
              key={tissueType}
              onClick={() => this.transferTissueType(tissueType)}
              value={tissueType}
              selected={true}
            >
              {tissueType}
            </StyledButton>
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
        ? props.theme.leafGreen
        : props.theme.boringBlue} !important;
  }
`;

const StyledList = styled(List)`
  display: flex;
  flex-direction: column;
  margin: 0px 16px;
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
