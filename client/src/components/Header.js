import React, { Component } from "react";
import logo from "../assets/images/logo.png";
import styled from "styled-components";

const HEADER_HEIGHT = 64;
const HEADER_PADDING = 24;

class Header extends Component {
  render() {
    return (
      <StyledHeader>
        <StyledLogo src={logo} />
        <StyledTitle>Clustered Gene Analysis</StyledTitle>
      </StyledHeader>
    );
  }
}

const StyledHeader = styled.div`
  background-color: ${props => props.theme.boringBlue};
  height: ${HEADER_HEIGHT}px;
  padding-left: ${HEADER_PADDING}px;
  padding-right: ${HEADER_PADDING}px;
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

export default Header;
