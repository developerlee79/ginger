from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.calculate.usage_calculator import UsageCalculator
from app.image.detection.azure_open_ai_vision import AzureOpenAIVisionDetector
from app.image.detection.image_detector import ImageDetector
from app.image.storage.azure_blob import AzureBlobStorage
from app.image.storage.image_storage import ImageStorage
from app.search.azure_database_finder import AzureDatabaseFinder
from app.search.azure_openai_parser import AzureOpenAIParser
from app.search.device_info_finder import DeviceInfoFinder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="/"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/result", response_class=HTMLResponse)
async def post_result(request: Request, content: str = Form(...)):
    ai_parser = AzureOpenAIParser()
    search_query = ai_parser.convert_text_to_query(content)
    device_info_finder: DeviceInfoFinder = AzureDatabaseFinder()
    products = device_info_finder.get_recommend_devices(search_query)

    if not products:
        print("no matched data")
        products = []

    return templates.TemplateResponse("result.html",
                                      {
                                          "request": request,
                                          "content": content,
                                          "explain": "test",
                                          "products": products
                                      })


@app.get("/detail/{device_id}", response_class=HTMLResponse)
async def get_product_detail(request: Request, device_id: int):
    device_info_finder: DeviceInfoFinder = AzureDatabaseFinder()
    device_info = device_info_finder.get_device_info(device_id)
    power_consumption = device_info["power_consumption"]
    electricity_bill = UsageCalculator.calculate_electricity_bill(power_consumption)
    carbon_footprint = UsageCalculator.calculate_carbon_footprint(power_consumption)
    device_info["electricity_bill"] = electricity_bill
    device_info["carbon_footprint"] = carbon_footprint

    if not device_info:
        return templates.TemplateResponse("error.html", {"request": request, "message": "상품을 찾을 수 없습니다."})

    return templates.TemplateResponse("detail.html", {"request": request, "product": device_info})

@app.get("/detail-scan", response_class=HTMLResponse)
async def get_detail_scan(request: Request):
    return templates.TemplateResponse("detail-scan.html", {"request": request})

@app.post("/device/info")
async def get_device_info_from_image(image: UploadFile = File(...)):
    contents = await image.read()
    filename = image.filename

    image_storage: ImageStorage = AzureBlobStorage()
    image_url = image_storage.upload_file(contents, filename)

    image_detector: ImageDetector = AzureOpenAIVisionDetector()
    device_info = image_detector.extract_info_from_image(image_url)

    manufacturer = device_info["manufacturer"]
    model_code = device_info["model_code"]

    device_info_finder: DeviceInfoFinder = AzureDatabaseFinder()
    device_name, power_consumption = device_info_finder.find_device_info(manufacturer, model_code)

    electricity_bill = UsageCalculator.calculate_electricity_bill(watt=power_consumption)
    carbon_footprint = UsageCalculator.calculate_carbon_footprint(watt=power_consumption)

    return {
        "device_name": device_name,
        "power_consumption": power_consumption,
        "electricity_bill": electricity_bill,
        "carbon_footprint": carbon_footprint
    }

@app.get("/device/recommend")
async def search_device_recommends(query: str):
    ai_parser = AzureOpenAIParser()
    search_query = ai_parser.convert_text_to_query(query)
    device_info_finder: DeviceInfoFinder = AzureDatabaseFinder()
    device_list = device_info_finder.get_recommend_devices(search_query)
    return device_list

@app.get("/device")
async def get_device_info_list(category: int = 0, page: int = 0, size: int = 10):
    device_info_finder: DeviceInfoFinder = AzureDatabaseFinder()
    device_list = device_info_finder.get_device_list(category, page, size)
    return device_list

@app.get("/device/{device_id}")
async def get_device_info(device_id: int):
    device_info_finder: DeviceInfoFinder = AzureDatabaseFinder()
    device_info = device_info_finder.get_device_info(device_id)
    power_consumption = device_info["power_consumption"]
    electricity_bill = UsageCalculator.calculate_electricity_bill(power_consumption)
    carbon_footprint = UsageCalculator.calculate_carbon_footprint(power_consumption)
    device_info["electricity_bill"] = electricity_bill
    device_info["carbon_footprint"] = carbon_footprint
    return device_info
