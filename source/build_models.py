from markov_chains import german_text

CORPUS_PATH_YES = "/Users/filter/code/fds-util/data/suc_msg.json"
CORPUS_PATH = "/Users/filter/code/fds-util/data/failed_msg.json"
MODEL_BASE_PATH = "models/no"
MODEL_BASE_PATH_YES = "models/yes"

# build_model.build_model(CORPUS_PATH, MODEL_BASE_PATH)
german_text.build_model(CORPUS_PATH_YES, MODEL_BASE_PATH_YES)
