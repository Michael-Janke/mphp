import React, { Component } from "react";
import styled from "styled-components";

class Footer extends Component {
  render() {
    return (
      <Container>
        <Link href="https://hpi.de/en/impressum.html">Legal Notice</Link>
        <Link href="https://hpi.de/en/data-privacy.html">Data Privacy</Link>
        <Link href="https://hpi.de/en/kontakt.html">Contact</Link>
      </Container>
    );
  }
}

const Container = styled.div`
  width: 100%;
  heigth: ${props => props.theme.footerHeight};
  background-color: ${props => props.theme.slightlyBoringBlue};
  padding-top: ${props => props.theme.mediumSpace};
  padding-bottom: ${props => props.theme.smallSpace};
  display: flex;
  justify-content: center;
`;

const Link = styled.a`
  font-size: ${props => props.theme.smallText};
  color: ${props => props.theme.almostWhite};
  margin-left: ${props => props.theme.largeSpace};
  margin-right: ${props => props.theme.largeSpace};
  text-decoration: none;
`;

export default Footer;
