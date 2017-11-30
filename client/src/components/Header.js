import React, { Component } from "react";
import AppBar from "material-ui/AppBar";
import styled from "styled-components";
import logo from "../assets/images/logo.png";
import constants from "../constants";

const StyledLogo = styled.img`
  height: 45px;
`;

const StyledSmallSpacer = styled.div`
  height: ${constants.appBarPadding}px;
  width: ${constants.appBarPadding}px;
`;

const StyledLargeSpacer = styled.div`
  height: ${constants.appBarHeight}px;
  width: ${constants.appBarHeight}px;
`;

const StyledTitle = styled.h1`
  margin: 0;
  margin-left: 20;
`;

const StyledHeaderTitle = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: ${props => props.theme.textColor};
`;

const StyledRoot = styled.div`
  text-align: "center";
`;

class Header extends Component {
  render() {
    return (
      <StyledRoot>
        <AppBar
          title={
            <StyledHeaderTitle>
              {/* spacers needed to center the title */}
              <StyledSmallSpacer />
              <StyledLogo src={logo} alt="logo" />
              <StyledTitle>Epic Project</StyledTitle>
              <StyledLargeSpacer />
            </StyledHeaderTitle>
          }
        />
      </StyledRoot>
    );
  }
}

export default Header;
