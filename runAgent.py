#!/usr/bin/python3
from agents import agents
import argparse
from getpass import getpass
from spade import quit_spade
from aiosasl import AuthenticationFailure
import time



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('agent', choices=agents.keys())
    parser.add_argument('--password', '-p')
    parser.add_argument('--web', action='store')
    parser.add_argument('--all', action='store')
    parser.parse_args()
    args = parser.parse_args()
    agent_name = args.agent

    agent = None
    try:
        agent_data = agents.get(agent_name)
        agent_jid = agent_data['jid']

        if args.password:
            agent_password = args.password
        else:
            agent_password = getpass(f'Enter {agent_name} agent {agent_jid} password:')

        agent = agent_data['agentClass'](agent_jid,  agent_password)
        for key, val in agent_data['params'].items():
            agent.set(key, val)

        agent.start()
        if args.web:
            agent.web.start(hostname="127.0.0.1", port="10000")
        while agent.is_alive():
            try:
                time.sleep(3)
            except KeyboardInterrupt:
                print("Attempting to stop agent...")
                if agent.is_alive():
                    agent.stop()
                quit_spade()
    except KeyError as e:
        print(f"Unknown agent {agent_name}: {e}")
    except AuthenticationFailure as e:
        # FIXME: nie dziala, jakis duzy stack wyjatkow - ogolem syf.
        print(f"Wrong agent {agent_name} password: {e}")

