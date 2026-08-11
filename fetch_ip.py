import re
import urllib.request
import ssl

# 目标 URL
URL = "https://www.wetest.vip/page/cloudflare/address_v4.html"

def fetch_ips():
    # 模拟真实浏览器 Request Header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.wetest.vip/"
    }

    all_ips = []

    # 忽略 SSL 证书校验（防止部分 Runner 环境校验失败）
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(URL, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            html = response.read().decode("utf-8")

        # 使用正则快速匹配所有的 IPv4 地址
        raw_ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", html)
        for ip in raw_ips:
            # 排除非公网及保留 IP 地址
            if not ip.startswith(("0.", "127.", "255.", "192.168.", "10.")) and ip not in all_ips:
                all_ips.append(ip)

    except Exception as e:
        print(f"抓取页面出现错误: {e}")

    # 如果因 403/防护导致未拿到 IP，写入默认内置 Cloudflare 官方优选 Anycast IP 保底，防止 Actions 报错退出
    if not all_ips:
        print("未从页面提取到动态 IP，写入保底 IP")
        all_ips = [
            "104.16.242.6",
            "104.20.50.84",
            "104.24.33.100",
            "104.17.22.11",
            "172.64.48.55",
            "162.159.19.159",
            "162.159.60.190",
            "162.159.43.144"
        ]

    # 强制生成 ip.txt 文件
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_ips) + "\n")

    print(f"处理完成，成功写入 {len(all_ips)} 个 IP 到 ip.txt！")

if __name__ == "__main__":
    fetch_ips()
