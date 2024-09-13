import math
 
# in order to calculate
# distance between two cities,
# I used the Euclidean distance formula
distance = lambda p, s_p: math.sqrt(
    (p._mapping['latitude'] - s_p._mapping['latitude'])**2 + \
    (p._mapping['longitude'] - s_p._mapping['longitude'])**2
    ) if p and s_p else 0


def sort_dists(dists: list[tuple]):
        """
        Quick sorting of the distances.
        """
        if len(dists) < 2:
            return dists
        else:
            pivot = dists[0]
            smaller_dists = [dists[i] for i in range(len(dists)) if dists[i][1] < pivot[1]]
            greater_dists = [dists[i] for i in range(len(dists)) if dists[i][1] > pivot[1]]

            return sort_dists(smaller_dists) + [pivot] + sort_dists(greater_dists)


def get_env_vars() -> dict[str, str | dict[str, str]]:
    """
    Load environmental vars at
    a runtime.
    """
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()

    db_configs: dict
    if getenv('PROD') == 'active':
         db_configs = {
              'DB_NAME': getenv('DB_NAME'),
              'USERNAME': getenv('USERNAME'),
              'PASSWORD': getenv('PASSWORD'),
              'PORT': getenv('PORT')
              }
    else:
        db_configs = {'url': getenv('SQLITE_PATH')}

    return {'api': getenv('API_KEY'), 'db_configs': db_configs}