import os, uvicorn
from fastapi import FastAPI
from rich.console import Console

# --- Constants --- #

app = FastAPI()
console = Console()
apps = []

# --- Import API Routes --- #
for route in [file[:-3] for file in os.listdir("./routes") if file.endswith(".py")]:
    exec("from routes.{} import app as route".format(route))
    exec("apps.append(route)")
    exec("del route")

for route in apps:
    app.include_router(route)
    console.log("[API] Loaded route: {}".format(route))

# --- Events --- #


@app.on_event("startup")
async def startup():
    console.log("[API] Starting...")


@app.on_event("shutdown")
async def shutdown():
    console.log("[API] Shutting down...")


# --- Home --- #

@app.get("/")
async def home():
    return 200

# --- Running --- #

if __name__ == "__main__":
    uvicorn.run(f"{os.path.basename(__file__).replace('.py', '')}:app", host="0.0.0.0", port=80, reload=True)
