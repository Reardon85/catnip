import React from 'react';
import './styles/app.css';
import {Link } from "react-router-dom";
import { Tab, Tabs, Row, Col} from 'react-bootstrap';
import QuickMatch from './QuickMatch.js';
import Matches from './Matches.js';
import Visitors from './Visitors';


const Match = () => {

  
  
  return (
    <Row className="justify-content-start ml-md-5">
        <Col>
            <Tabs defaultActiveKey="quick-match" id="uncontrolled-tab-example" className="px-1" justify >
                <Tab eventKey="quick-match" title="Quick Match" >
                    <QuickMatch />
                </Tab>
                <Tab eventKey="matches" title="Matches"  >
                    <Matches />
                </Tab>
                <Tab eventKey="visitors" title="Visitors" >
                    <Visitors />
                </Tab>
            </Tabs>
        </Col>
    </Row>

  );
};

export default Match;