import re
import urllib.request
from bs4 import BeautifulSoup

URL = "https://www.wetest.vip/page/cloudflare/address_v4.html"

def fetch_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.wetest.vip/"
    }
    
    all_ips = []

    try:
        req = urllib.request.Request(URL, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        
        if table:
            for row in table.find_all("tr"):
                cols = [ele.text.strip() for ele in row.find_all(["td", "th"])]
                # 表格中第二列为“优选地址” (IP)
                if len(cols) >= 2:
                    ip = cols[1]
                    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip) and ip not in all_ips:
                        all_ips.append(ip)
                        
        # 备用正则提取（防止表格标签微调导致解析失效）
        if not all_ips:
            matched_ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", html)
            for ip in matched_ips:
                if not ip.startswith(("0.", "127.", "255.")) and ip not in all_ips:
                    all_ips.append(ip)

    except Exception as e:
        print(f"抓取微测网失败: {e}")

    if not all_ips:
        print("未提取到任何有效 IP")
        return

    # 写入 ip.txt
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_ips) + "\n")

    print(f"抓取完成！共从微测网提取到 {len(all_ips)} 个 IP，已保存至 ip.txt")

if __name__ == "__main__":
    fetch_ips()
