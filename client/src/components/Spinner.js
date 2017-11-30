import React, { Component } from "react";
import styled from "styled-components";

class Spinner extends Component {
  render() {
    return <StyledRoot className="spinner" size={this.props.size} />;
  }
}

const StyledRoot = styled.div`
  height: ${props => props.size || 20}px;
  width: ${props => props.size || 20}px;
  border-style: solid;
  border-width: ${props => (props.size ? props.size / 2 : 10)}px;
  border-color: ${props => props.theme.lightGray};
  border-top-color: ${props => props.theme.boringBlue};
  border-radius: 50%;
  animation: spin 2s linear infinite;

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
`;

export default Spinner;
