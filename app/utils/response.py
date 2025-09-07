from fastapi.responses import JSONResponse

def response(success: bool, data = None, status_code: int = 200) -> JSONResponse:
    if data is None:
        data = {}
    return JSONResponse(content={"success": success, "data": data}, status_code=status_code)