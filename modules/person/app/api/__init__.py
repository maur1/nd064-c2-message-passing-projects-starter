
def register_routes(api, app, root="api"):
    from app.api.controller import uda_api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")