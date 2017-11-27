import React, { Component } from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Statistics from './cards/Statistics';
import Data from './cards/Data';

class Content extends Component {
  constructor(props) {
    super(props);
    this.state = { cards: [] };
  }

  render() {
    return (
      <div className="content">
        <div className="menu">
           <RaisedButton
             label="Show statistics"
             primary={true}
             style={styles.button}
             onClick={() => { this.addCard(Statistics); }}
          />
           <RaisedButton
             label="Show some data"
             primary={true}
             style={styles.button}
             onClick={() => { this.addCard(Data); }}
          />
        </div>
        <div className="cards">
          {this.state.cards.map(this.renderCard)}
        </div>
      </div>
    );
  }

  renderCard(Card, index) {
    return <Card key={`card-${index}`} />
  }

  addCard(Card) {
    this.setState({ cards: [ ...this.state.cards, Card ]});
  }
}

const styles = {
  button: {
    margin: 12,
  },
};

export default Content;
