

def runAgent(args):
    args.parse()
    agent_name = args['agent']
    agent_password = args['password']
    try:
        agent_data = agents.get(agent_name)
        agent = agent_data['agentClass'](agent_data['jid'],  agent_password)
    except KeyError e:
        print(f"Unknown agent {agent_name}: {e}")
    finally:
        agent.start()

