# api/__init__.py
from ninja import NinjaAPI
from provas.routers import include_routers as include_provas

api = NinjaAPI()

include_provas(api)
