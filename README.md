# ResuMatch | Screening & Matching

## Problem Statement

Develop an agent that can intelligently screen and match resumes with job descriptions. The agent should use natural language processing (NLP) and machine learning techniques to understand the requirements listed in a job description and evaluate resumes based on these criteria.

## Overview

This document describes the communication protocol and functionality between two agents, Agent1 and Agent2, developed using the Fetch.AI UAgent framework. The agents interact with each other through a decentralized network using asynchronous communication.

## Setup
- Install dependencies
```
pip install -r requirments.txt
```
- Run the agents with
Agent1 with

```
python agent1.py
```
Agent2 with 

```
python agent2.py
```
## Agent1: Resume Score Calculator

### Functionality

Agent1's responsibilities include:

- Calculating a score based on a job applicant's resume and a job description.
- Sending the calculated score to Agent2 for further processing.

### Communication Details

- **Agent Name:** Agent1
- **Address:** agent1qv2l7qzcd2g2rcv2p93tqflrcaq5dk7c2xc7fcnfq3s37zgkhxjmq5mfyvz
- **Port:** 8001
- **Seed:** "agent1 secret phrase"

### Message Models

- **Model Used:** Message(Model)
  - Fields:
    - `message`: str

### Interactions

- On interval (every 3 seconds), Agent1 logs a greeting message containing its address.

- Receives messages from Agent2:
  - Expects a message containing the applicant's resume and job description.
  - Calculates the similarity score between the resume and job description.
  - Sends the score to Agent2 for further action.

## Agent2: Alert Dispatcher

### Functionality

Agent2's responsibilities include:

- Sending periodic messages to Agent1.
- Receiving and processing scores from Agent1.
- Determining whether to send an alert based on the received score.

### Communication Details

- **Agent Name:** Agent2
- **Address:** agent2qp5d4qr7tdcfk46wnxgsr7m5s62c6xsyylf9z6q5q2kqf3g6v8q75nrejz
- **Port:** 8000
- **Seed:** "alice secret phrase"

### Message Models

- **Model Used:** Message(Model)
  - Fields:
    - `message`: str

### Interactions

- On interval (every 2 seconds), Agent2 sends a greeting message to Agent1.

- Receives messages from Agent1:
  - Checks for a message indicating the similarity score.
  - Parses the score and decides whether to send an alert based on a threshold (50).

## Conclusion

This document outlines the functionalities and communication protocols of Agent1 and Agent2 within the Fetch.AI UAgent framework. Agents communicate asynchronously, exchanging messages to calculate and process a resume similarity score and send the alert of the Resume score.

## Future Goals

Develop a comprehensive user interface similar to platforms such as Indeed or LinkedIn Jobs where companies can input Job Descriptions (JDs). If a candidate's resume score exceeds the threshold set by the company, Agent2 will automatically dispatch an email to the candidate to advance to the next stage of the recruitment process. Conversely, if the score falls below the company's requirements, a rejection email will be sent to the candidate automatically.
