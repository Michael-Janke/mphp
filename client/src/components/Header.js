import React, { Component } from "react";
import { connect } from "react-redux";
import { updateName } from "../actions/experimentActions";
import logo from "../assets/images/logo.png";
import styled, { withTheme } from "styled-components";
import EditableText from "./EditableText";
import IconButton from "./IconButton";

class Header extends Component {
  render() {
    return (
      <StyledHeaderContainer>
        <StyledHeader>
          <StyledLogo src={logo} />
          <StyledTitle>Clustered Gene Analysis</StyledTitle>
        </StyledHeader>
        <StyledExperimentHeader>
          <EditableText
            text={this.props.experimentName}
            onChange={this.props.updateExperimentName}
          />
          <StyledButtonContainer>
            <IconButton
              tooltip="Open existing experiment"
              icon="open"
              color={this.props.theme.almostWhite}
            />
            <IconButton
              tooltip="Save experiment"
              icon="save"
              color={this.props.theme.almostWhite}
            />
          </StyledButtonContainer>
        </StyledExperimentHeader>
      </StyledHeaderContainer>
    );
  }
}

const StyledHeaderContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  z-index: 9001; /* The z-index is over 9000! */
  overflow: hidden;
`;

const StyledHeader = styled.div`
  background-color: ${props => props.theme.boringBlue};
  height: ${props => props.theme.headerHeight};
  padding-left: ${props => props.theme.largeSpace};
  padding-right: ${props => props.theme.largeSpace};
  display: flex;
  align-items: center;
`;

const StyledExperimentHeader = styled.div`
  background-color: ${props => props.theme.slightlyBoringBlue};
  height: ${props => props.theme.experimentHeaderHeight};
  padding-left: ${props => props.theme.largeSpace};
  padding-right: ${props => props.theme.largeSpace};
  display: flex;
  align-items: center;
`;

const StyledTitle = styled.h1`
  margin: 0;
  margin-left: 20px;
  color: ${props => props.theme.almostWhite};
  font-size: ${props => props.theme.h1};
`;

const StyledLogo = styled.img`
  height: 45px;
`;

const StyledButtonContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  width: 20%;
`;

const mapStateToProps = state => {
  return {
    experimentName: state.experiment.name
  };
};

const mapDispatchToProps = dispatch => {
  return {
    updateExperimentName: newName => {
      dispatch(updateName(newName));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(withTheme(Header));
