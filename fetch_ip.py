import json
import urllib.request
import ssl

# 目标 API URL (包含电信 CT、联通 CU、移动 CM 分线路优选 IP)
URL = "https://vps789.com/openApi/cfIpApi"

def fetch_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://vps789.com/"
    }

    all_ips = []

    # 忽略 SSL 证书校验
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(URL, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            res_data = json.loads(response.read().decode("utf-8"))

            if res_data.get("code") == 0 and "data" in res_data:
                ip_data = res_data["data"]
                
                # 遍历 CT (电信), CU (联通), CM (移动) 列表中的 IP
                for line in ["CT", "CU", "CM"]:
                    for item in ip_data.get(line, []):
                        ip = item.get("ip")
                        # 重新加回限制：必须以 172. 开头且不重复
                        if ip and ip.startswith("172.") and ip not in all_ips:
                            all_ips.append(ip)
                            print(f"符合条件的 IP [{line}]: {ip}")
            else:
                print(f"API 返回错误或数据异常: {res_data.get('message')}")

    except Exception as e:
        print(f"抓取 API 数据出现错误: {e}")

    # 如果未抓取到符合条件的 IP，写入 172 开头的保底 IP
    if not all_ips:
        print("未提取到符合条件（172.开头）的 IP，写入保底 IP")
        all_ips = [
            "172.64.229.52",
            "172.64.79.228",
            "172.64.48.55",
            "172.64.229.86",
            "172.64.89.156"
        ]

    # 写入 ip.txt 文件
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_ips) + "\n")
    
    print(f"处理完成，成功写入 {len(all_ips)} 个 IP 到 ip.txt！")

if __name__ == "__main__":
    fetch_ips()
