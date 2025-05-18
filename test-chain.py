from chain import graph

# Specify an ID for the thread
config = {"configurable": {"thread_id": "abc123"}}
input_message = "Qué materias comunes hay entre la Lic. en Cs de Datos y la Ingeniería en IA?"

for step in graph.stream(
    {"messages": [{"role": "user", "content": input_message}]},
    stream_mode="values",
    config=config,
):
    step["messages"][-1].pretty_print()