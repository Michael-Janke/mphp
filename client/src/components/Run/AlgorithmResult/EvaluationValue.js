import React, { Component } from "react";
import styled from "styled-components";
import { ListItem } from "material-ui/List";

export default class EvaluationValue extends Component {
  render() {
    const primaryText = this.props.primaryText.toFixed(2);
    const props = { ...this.props, primaryText };
    return <ColoredValue {...props} />;
  }
}

const ColoredValue = styled(ListItem)`
  div:first-child {
    color: ${props => getColor(props)};
  }
`;

function getColor({ theme, primaryText }) {
  return primaryText < 0.5
    ? theme.cherryRed
    : primaryText < 0.67
      ? theme.lightOrange
      : primaryText < 0.8 ? theme.sunYellow : theme.leafGreen;
}
