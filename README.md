# Github-repo-info-API
Gets github repo's basic information
##### Gif Demo :point_down:

![Github repo info - Gif demo](github-repo-info-sample.gif)

check it out: https://github-repos-info.herokuapp.com/

#### Request (GET)
  https://github-repos-info.herokuapp.com/repo?url=github-repo-url
  
  **returns**:
  ```
    {
      "repo_title"       : str,
      "repo_path"        : str,
      "repo_author"      : str,
      "repo"             : str,
      "repo_url"         : str,
      "repo_description" : str,
      "repo_readme_"     : str,
      "repo_tags"        : Array[str],
    }
    ```
