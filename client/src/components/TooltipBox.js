import React, { Component } from "react";
import styled from "styled-components";
import Paper from "material-ui/Paper";
import Color from "tinycolor2";

class TooltipBox extends Component {
  render() {
    const position = this.props.position || "below";
    const width = this.props.width || 300;
    let tooltipstyles;
    switch (position) {
      case "right":
        tooltipstyles = "top: -5px; left: 105%;";
        break;
      case "right width":
        tooltipstyles = `width: ${width}px;
        top: -5px; left: 105%;`;
        break;
      case "left":
        tooltipstyles = "top: -5px; right: 105%;";
        break;
      case "top":
        tooltipstyles = `width: ${width}px;
        bottom: 100%;
        left: 50%;
        margin-left: -${width / 2}px;`;
        break;
      case "top right":
        tooltipstyles = `width: ${width}px;
        top: -40px;
        left: 105%;
        `;
        break;
      default:
        tooltipstyles = `  width: ${width}px;
        top: 100%;
        left: 50%;
        margin-left: -${width / 2}px`;
    }
    return (
      <StyledTooltipBox className={this.props.className}>
        {this.props.children}
        <StyledTooltip tooltipstyles={tooltipstyles}>
          {this.props.text}
        </StyledTooltip>
      </StyledTooltipBox>
    );
  }
}

const StyledTooltipBox = styled.div`
  position: relative;
  //display: inline-block;
  padding: 0 4px;
  cursor: ${props => props.cursor || "pointer"} !important;
`;

export const StyledTooltip = styled(Paper)`
  visibility: hidden;
  transition: visibility 0s linear 0ms, opacity 0ms !important;
  position: absolute;
  background-color: ${props =>
    Color(props.theme.leafGreen)
      .brighten()
      .lighten()
      .toString()} !important;
  color: black !important;
  text-align: center;
  padding: 8px 4px;
  /* Position the tooltip text - see examples below! */
  ${props => props.tooltipstyles};
  z-index: 20001;
  font-size: 14px;
  ${StyledTooltipBox}:hover & {
    visibility: visible !important;
  }
`;

export default TooltipBox;
