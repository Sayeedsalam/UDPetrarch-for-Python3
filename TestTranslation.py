from babelpy.babelfy import BabelfyClient

API_KEY = "e82d2ed5-62cb-44da-8ea6-98471171cecd"
# Instantiate BabelFy client.
params = dict()
params['lang'] = "en"
babel_client = BabelfyClient(API_KEY, params)

# Babelfy sentence.
babel_client.babelfy("ELN")

# Get entity data.
print(babel_client.entities)

# Get entity and non-entity data.
print(babel_client.all_entities)

# Get merged entities only.
print(babel_client.merged_entities)

# Get all merged entities.
babel_client.all_merged_entities
