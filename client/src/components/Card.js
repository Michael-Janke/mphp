import React, { Component } from 'react';
import Paper from 'material-ui/Paper';
import request from '../request';

class Content extends Component {
  constructor(props) {
    super(props);
    this.state = { isLoading: true, data: null };
  }

  componentDidMount() {
    request(this.props.route).then((data) => {
      this.setState({ isLoading: false, data });
    });
  }

  render() {
    return (
      <Paper style={styles.card} zDepth={1}>
        {this.state.isLoading ? this.renderLoading() : this.renderData(this.state.data)}
      </Paper>
    );
  }

  renderLoading() {
    // TODO add some spinner
    return <p>Loading ...</p>;
  }

  renderData(data) {
    return <p>{JSON.stringify(data)}</p>;
  }
}

const styles = {
  card: {
    margin: 12,
    padding: 12,
    paddingVertical: 6,
  },
}

export default Content;
