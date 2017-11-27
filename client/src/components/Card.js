import React, { Component } from 'react';
import { Card, CardTitle, CardText } from 'material-ui/Card';
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
      <Card style={styles.card} zDepth={1}>
        <CardTitle>{this.props.title}</CardTitle>
        <CardText>
          {this.state.isLoading ? this.renderLoading() : this.renderData(this.state.data)}
        </CardText>
      </Card>
    );
  }

  renderLoading() {
    // TODO add some spinner
    return <p>Loading ...</p>;
  }

  renderData(data) {
    // TODO do whatever we want to do here
    return <p>{JSON.stringify(data)}</p>;
  }
}

// TODO put magic numbers into constants
const styles = {
  card: {
    margin: 12,
    padding: 12,
    paddingVertical: 6,
  },
}

export default Content;
