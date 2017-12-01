import React, { Component } from "react";
import logo from "../assets/images/logo.png";
import styled from "styled-components";

class Header extends Component {
  render() {
    return (
      <StyledHeaderContainer>
        <StyledHeader>
          <StyledLogo src={logo} />
          <StyledTitle>Clustered Gene Analysis</StyledTitle>
        </StyledHeader>
        <StyledExperimentHeader>
          <StyledExperimentName>Experiment Name</StyledExperimentName>
        </StyledExperimentHeader>
      </StyledHeaderContainer>
    );
  }
}

const StyledHeaderContainer = styled.div`
  display: flex;
  flex-direction: column;
  position: fixed;
  width: 100%;
  z-index: 9001; /* The z-index is over 9000! */
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

const StyledExperimentName = styled.div`
  color: ${props => props.theme.almostWhite};
  font-size: ${props => props.theme.h2};
`;

const StyledLogo = styled.img`
  height: 45px;
`;

export default Header;
