import React from 'react';
import './App.css';
import BackVideo from './Components/BackVideo.js'
import Element3 from './Components/Element3.js'
import { CSSTransition } from 'react-transition-group'
import Delayed from './Components/Delayed.jsx';
import DatePage from './Components/DatePage';
import Title from './Components/Title';
import Grid from './Media/zoom_grid.svg';
import TimeoutHelper from './Components/TimeoutHelper';

class App extends React.Component {

  constructor(props) {

    super(props);
  
    this.state = {
      el1: true,
      el2: false,
      el3: false,
      el4: false,
      el5: false,
      el6: false,
      el7: false,
      nuc: true
    };

    this.timer = new TimeoutHelper();
  }

  render(){

    return (

      <div>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <link rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Roboto+Mono"/>
        

      <CSSTransition
        in={this.state.el1}
        timeout={1000}
        unmountOnExit
        onEnter={() => this.setState({el7:false})}
        onExited={() => {this.timer.setTimeout(() => this.setState({el2:true}), 1000)}}
        classNames="fade"
      >
        <div>
          <div className="videoContainer">
            <BackVideo vidName={require("./Media/robot_full.mp4")} endFunc={() => {this.setState({el1:false})}}/>
          </div>
          <Delayed waitBeforeShow={1000} className="IntroText">
            <div className="IntroJumbotron">
              <p id="jumbotron-title">ALPHAGARDEN</p>
              <p id="jumbotron-subtitle">A LIVING PREVIEW</p>
            </div>
            <div className="IntroSubtitle">
              <p>UPDATED DAILY FROM BERKELEY, CALIFORNIA</p>
            </div>
          </Delayed>
        </div>

      </CSSTransition>

      <CSSTransition
        in={this.state.el2}
        timeout={500}
        unmountOnExit
        onEnter={() => this.setState({el1:false})}
        onExited={() => {this.timer.setTimeout(() => this.setState({el3:true}), 1000)}}
        classNames="fade"
      >

        <DatePage nuc={this.state.nuc} endFunc={() => {this.setState({el2:false})}}/>

      </CSSTransition>


      <CSSTransition
        in={this.state.el3}
        timeout={500}
        unmountOnExit
        onEnter={() => this.setState({el2:false})}
        onExited={() => {this.timer.setTimeout(() => this.setState({el4:true}), 1000)}}
        classNames="fade"
      >

        <Element3 endFunc={() => {this.setState({el3:false})}} nuc={this.state.nuc}/>

      </CSSTransition>

      <CSSTransition
        in={this.state.el4}
        timeout={1000}
        unmountOnExit
        onEnter={() => this.setState({el3:false})}
        onExited={() => {this.timer.setTimeout(() => this.setState({el5:true}), 500)}}
        classNames="fade"
            >

        <Title nuc={this.state.nuc} title={"SIMULATING POTENTIAL OUTCOMES"} endFunc={() => {this.setState({el4:false})}}/>

      </CSSTransition>

      <CSSTransition
        in={this.state.el5}
        timeout={500}
        unmountOnExit
        onEnter={() => this.setState({el4:false})}
        onExited={() => {this.timer.setTimeout(() => this.setState({el6:true}), 1000)}}
        classNames="fade"
      >
        <div>
          <img src={Grid} className="SimOverlay" alt="grid overlay"/>
          <BackVideo vidName={require("./Media/simulation.mp4")} endFunc={() => {this.setState({el5:false})}}/>
        </div>
      </CSSTransition>

      <CSSTransition
        in={this.state.el6}
        timeout={1000}
        unmountOnExit
        onEnter={() => this.setState({el5:false})}
        onExited={() => {this.timer.setTimeout(() => this.setState({el7:true}), 1000)}}
        classNames="fade"
            >

        <Title nuc={this.state.nuc} title={"OBSERVING REALITY"} endFunc={() => {this.setState({el6:false})}}/>

      </CSSTransition>

      <CSSTransition
        in={this.state.el7}
        timeout={1000}
        unmountOnExit
        onEnter={() => this.setState({el6:false})}
        onExited={() => {this.timer.setTimeout(() => this.setState({el1:true}), 2000)}}
        classNames="fadelonger"
      >

        <BackVideo vidName={require("./Media/closeup_side.mp4")} endFunc={() => {this.setState({el7:false})}}/>
      
      </CSSTransition>
        
      </div>
      )
  }

  componentWillUnmount() {
    this.timer.clearAllTimeouts();
  }
}

export default App;