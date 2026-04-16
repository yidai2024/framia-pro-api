#!/usr/bin/env python3
"""
Framia.pro API抓取脚本
使用Playwright抓取framia.pro的API接口
"""
import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def capture_framia():
    print("抓取framia.pro...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        page = await context.new_page()
        
        # 收集请求
        api_requests = []
        
        async def handle_request(request):
            url = request.url
            if any(x in url for x in ['/api/', '/auth/', '/graphql']):
                api_requests.append({
                    "method": request.method,
                    "url": url,
                    "headers": dict(request.headers),
                    "post_data": request.post_data
                })
                print(f"[API] {request.method} {url}")
        
        page.on("request", handle_request)
        
        await page.goto("https://framia.pro/create", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(5000)
        
        await browser.close()
        
        # 保存结果
        with open("api_requests.json", "w") as f:
            json.dump(api_requests, f, indent=2)
        
        print(f"发现 {len(api_requests)} 个API请求")

if __name__ == "__main__":
    asyncio.run(capture_framia())
