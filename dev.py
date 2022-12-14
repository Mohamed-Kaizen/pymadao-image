"""Dev server for the app."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("madao_image.main:app", reload=True)


