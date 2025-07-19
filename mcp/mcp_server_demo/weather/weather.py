import os
from dotenv import load_dotenv, find_dotenv

import json
import asyncio

from watchfiles import run_process

from typing import Any
import httpx

_ = load_dotenv(find_dotenv())
# weather_api_key = os.getenv("weather_service")

weather_api_key = "09daff2e044a5eb0e7b4f1d52c311cf6"
weather_base_url = "https://restapi.amap.com/v3/weather/weatherInfo"


from mcp.server.fastmcp import FastMCP


# 初始化 FastMCP server
mcp = FastMCP("gd_weather")


async def get_weather_base(city, extensions="base"):
    params = {"key": weather_api_key, "city": city, "extensions": extensions}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://restapi.amap.com/v3/weather/weatherInfo", params=params
            )
            response.raise_for_status()
            return response
        except httpx.RequestError as exc:
            print(f"发起请求错误 {exc.request.url!r}.")
        except httpx.HTTPStatusError as exc:
            print(
                f"响应错误 {exc.response.status_code} 在请求发起 {exc.request.url!r}."
            )


res = asyncio.run(get_weather_base("北京", "all"))
print(type(res))
if __name__ == "__main__":
    run_process("./", target={}, args=(), kwargs={})
