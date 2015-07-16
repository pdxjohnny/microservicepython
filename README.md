mircopython
---

This is an example of using python and the stratus module to create a fault
tolerant micro service orientated application.

Start the main server
```bash
python -m app start
```

From other computers you can start other swarm nodes
```bash
python -m app connect --host <hostname or ip>
```

Services will be launched on all computers with swarms connected
