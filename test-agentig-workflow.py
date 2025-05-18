from agentic_workflow import graph

'''
for step in graph.stream(
    {"question": "Qué materias hay en el primer año / primer semestre de la Licenciatura en Ciencias de Datos?"},
):
    print(f"{step}\n\n----------------\n")
'''

#result = graph.invoke({"question": "Qué materias hay en el primer año / primer semestre de la Licenciatura en Ciencias de Datos?"})
result = graph.invoke({"question": "Qué materias comunes hay entre la Lic. en Cs de Datos y la Ingeniería en IA?"})

print(f'Context: {result["context"]}\n\n')
print(f'Answer: {result["answer"]}')