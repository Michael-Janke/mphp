import React, { Component } from 'react';
import AppBar from 'material-ui/AppBar';
import logo from '../assets/images/logo.png';
import constants from '../constants';

class Header extends Component {
  render() {
    return (
      <div style={{textAlign: 'center'}}>
        <AppBar
          title={
            <div class="header-title" style={styles.title}>
              {/* spacers needed to center the title */}
              <div style={styles.smallSpacer} />
              <img src={logo} className="logo" alt="logo" style={styles.logo} />
              <p style={styles.titleText}>Epic Project</p>
              <div style={styles.largeSpacer} />
            </div>
          }
        />
      </div>
    );
  }
}

const styles = {
  logo: {
    height: 45,
  },
  title: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  titleText: {
    margin: 0,
    marginLeft: 20,
  },
  smallSpacer: {
    height: constants.headerPadding,
    width: constants.headerPadding,
  },
  largeSpacer: {
    height: constants.headerSize,
    width: constants.headerSize,
  },
}

export default Header;
