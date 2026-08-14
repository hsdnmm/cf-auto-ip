import re
import urllib.request
import ssl

# 目标 URL
URL = "https://api.uouin.com/cloudflare.html"

def fetch_ips():
    # 模拟真实浏览器 Request Header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://api.uouin.com/"
    }
    
    all_ips = []
    
    # 忽略 SSL 证书校验
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(URL, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            html = response.read().decode("utf-8")
            
            # 使用正则抓取表格中包含 IP 和 速度(mb/s) 的行
            # 匹配模式：IP地址 ... 速度数值mb/s
            pattern = r'((?:\d{1,3}\.){3}\d{1,3})[\s\S]*?([\d.]+)\s*mb/s'
            matches = re.findall(pattern, html, re.IGNORECASE)
            
            for ip, speed_str in matches:
                try:
                    speed = float(speed_str)
                    # 过滤速度大于等于 5MB/s 且非保留地址的 IP
                    if speed >= 5.0:
                        if not ip.startswith(("0.", "127.", "255.", "192.168.", "10.")) and ip not in all_ips:
                            all_ips.append(ip)
                            print(f"符合条件的 IP: {ip} (速度: {speed} MB/s)")
                except ValueError:
                    continue

    except Exception as e:
        print(f"抓取页面出现错误: {e}")
        
    # 如果因防护或无符合条件 IP，写入保底 IP
    if not all_ips:
        print("未提取到符合条件（>=5MB/s）的动态 IP，写入保底 IP")
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

    # 写入 ip.txt 文件
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_ips) + "\n")
        
    print(f"处理完成，成功写入 {len(all_ips)} 个 IP 到 ip.txt！")

if __name__ == "__main__":
    fetch_ips()
