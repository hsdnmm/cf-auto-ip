import json
import re
import urllib.request

# 使用 VPS789 官方开放接口
API_URL = "https://vps789.com/openApi/cfIpApi"

def fetch_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://vps789.com/vps/cfIp",
        "Accept": "application/json, text/plain, */*"
    }
    
    all_ips = []

    try:
        req = urllib.request.Request(API_URL, headers=headers)
        response = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        res_data = json.loads(response)
        
        # 提取 CT(电信)、CU(联通)、CM(移动) 下的所有 IP
        if res_data.get("code") == 0 and "data" in res_data:
            data = res_data["data"]
            for line_key in ["CT", "CU", "CM"]:
                ip_list = data.get(line_key, [])
                for item in ip_list:
                    ip = item.get("ip")
                    if ip and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip) and ip not in all_ips:
                        all_ips.append(ip)

    except Exception as e:
        print(f"调用 API 失败: {e}")

    if not all_ips:
        print("未获取到 IP 数据")
        return

    # 保存所有 IP 到 ip.txt
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_ips) + "\n")

    print(f"抓取成功！共提取到 {len(all_ips)} 个 IP，已保存至 ip.txt")

if __name__ == "__main__":
    fetch_ips()
