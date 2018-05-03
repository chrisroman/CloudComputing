The files here are meant to start up an edge server. Each edge server creates
its own queue and subscribes it to the area topic based on the `SERVER_ID`
environment variable. It then pulls messages from its queue and prints it
