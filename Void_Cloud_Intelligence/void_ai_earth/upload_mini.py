from huggingface_hub import HfApi


hf_token = 'stub'

#import token from .env

api = HfApi(token=hf_token)
api.upload_folder(
    folder_path="./exported_model",
    repo_id="a13a/UI_Classifer",
    repo_type="model",
)
