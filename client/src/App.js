import React, { Component } from "react";
import styled from "styled-components";
import Header from "./components/Header";
import Content from "./components/Content";

const THRESHOLD = 100;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      minimize: false
    };
  }

  render() {
    return (
      <StyledRoot className="app">
        <Header minimized={this.state.minimize} />
        <ScrollableArea
          innerRef={comp => (this.scrollableArea = comp)}
          onScroll={this.handleScroll}
        >
          <Content />
        </ScrollableArea>
      </StyledRoot>
    );
  }
  handleScroll = event => {
    if (event.target.scrollTop > THRESHOLD) {
      this.setState({ minimize: true });
    } else {
      this.setState({ minimize: false });
    }
  };
}

const StyledRoot = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`;

const ScrollableArea = styled.div`
  overflow: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
`;

export default App;

// scrollTop - Content has been scrolled? give prop to header to become smaller
