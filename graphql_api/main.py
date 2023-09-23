import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from query_bindables import query_bindables
from character_bindables import character_bindables

# Load the GraphQL schema from the .graphql file
SCHEMA_FILENAME = 'schema.graphql'
dirname = os.path.join(os.path.dirname(__file__), SCHEMA_FILENAME)
schema = load_schema_from_path(dirname)


bindables = [
    *query_bindables,
    *character_bindables,
]

# Create an executable schema with resolvers
executable_schema = make_executable_schema(schema, *bindables)

# Create an ASGI application
app = GraphQL(executable_schema)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
