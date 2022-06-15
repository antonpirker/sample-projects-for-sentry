from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from my_routes.routes import boom

from sentry_sdk.integrations.starlette import StarletteIntegration
import my_routes

import sentry_sdk
sentry_sdk.init(
    "https://125f495809d8406da340cedf11250a04@o447951.ingest.sentry.io/6492973",
    integrations=[
        StarletteIntegration(
           # transaction_style="url",
        ),
    ],
    debug=True,
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


async def homepage(request):
    return JSONResponse({'hello': 'world'})


async def debug_sentry(request):
    bla = 1/0
    return JSONResponse({'hello': 'world'})

async def upload_somethign(request):
    bla = 1/0
    return JSONResponse({'upload': 'hello'})



app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/debug-sentry', debug_sentry), 
    Route('/float/{number:float}', boom),
    Route('/upload/{rest_of_path:path}', upload_somethign, methods=["POST"]),
])
