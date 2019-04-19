import React from 'react';

class Host extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      players: [],
      stage: 0,
      answeredPlayers: [],
      votedPlayers: [],
      winners: [],
    };

    this.handleStartButton = this.handleStartButton.bind(this);
    this.handleResetPlayers = this.handleResetPlayers.bind(this);
    this.handleDoneButton = this.handleDoneButton.bind(this);

  }

  componentDidMount() {
    this.interval = setInterval(() => this.getPlayers(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  handleResetPlayers() {
    fetch('/api/v1/resetplayers', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/resetquestions', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/resetvotes', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })
  }

  getPlayers() {

    fetch('/api/v1/players', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })
    .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }).then((data) => {
        this.setState(prevState => ({
          players: data.players,
        }));
      })
      .catch();

      // Update answered players
      var ansPlayers = [];
      this.state.players.forEach(function(player) {
        if(player.ans1 !== "" && player.ans2 !== "") {
          ansPlayers.push(player)
        }
      });

      this.setState(prevState => ({
          answeredPlayers: ansPlayers,
        }));

      // Check if all players have answered
      if(this.state.answeredPlayers.length === this.state.players.length && this.state.answeredPlayers.length > 0) {
        // All players have answered, next stage
        this.setState(prevState => ({
          stage: 2,
        }));
      }

      // Update voted players
      fetch('/api/v1/votedPlayers', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }).then((data) => {
        this.setState(prevState => ({
          votedPlayers: data.voters,
        }));
      })
      .catch();

      // Check if all players have voted
      if(this.state.votedPlayers.length === this.state.players.length && this.state.votedPlayers.length > 0) {
        // All players have voted, next stage
        this.setState(prevState => ({
          stage: 3,
        }));
      }

      // Update winners
      fetch('/api/v1/winners', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }).then((data) => {
        this.setState(prevState => ({
          winners: data.winners,
        }));
      })
      .catch();

  }

  handleStartButton() {
    fetch('/api/v1/resetanswer', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/assignquestions', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    this.setState(prevState => ({
          stage: 1,
          answeredPlayers: [],
        }));

  }

  handleDoneButton() {
    fetch('/api/v1/resetanswer', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/resetquestions', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/resetvotes', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    this.setState(prevState => ({
          stage: 0,
          answeredPlayers: [],
        }));

    // Increment scores
    fetch('/api/v1/incrementScores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({"winners": this.state.winners}),
    })

  }


  render() {
    let output = ""
    switch(this.state.stage) {
      case 0:
        // Waiting for players
        output = (<div><p>Waiting for all players...</p>
          <ul>
            {
            this.state.players.map((player, index) =>
              <li key={index}><p>{player.name}: {player.points}</p></li>)
              }
          </ul>

        { this.state.players.length > 2 && 
          <button onClick={this.handleStartButton}>Start</button>
        }
        <button onClick={this.handleResetPlayers}>Reset</button>
        </div>);
        break;

      case 1:
        // Answering questions
        output = (<div><p>Waiting for players to answer questions...</p>

        <ul>
            {
            this.state.answeredPlayers.map((player, index) =>
              <li key={index}><p>{player.name}</p></li>)
              }
          </ul>
          </div>);

        break;

      case 2:
        // Display answers and wait for all votes
        output = (<div><p>Waiting for players to vote on questions...</p>

        <ul>
            {
            this.state.votedPlayers.map((player, index) =>
              <li key={index}><p>{player}</p></li>)
              }
          </ul>
          </div>);

        break;

      case 3:
        // Display winners of votes
        output = (<div><p>Winners:</p>

        <ul>
            {
            this.state.winners.map((question, index) =>
              <li key={index}>
                <p>{question.question}</p>
                <p>{question.ansA + ": \t" + question.votesA}</p>
                <p>{question.ansB + ": \t" + question.votesB}</p>
              </li>)
              }
          </ul>
          <button onClick={this.handleDoneButton}>Done</button>
          </div>);

        break;

    }
    return (
      <div className="host">
        {output}
      </div>
    );
  }
}

Host.propTypes = {
};

export default Host;
