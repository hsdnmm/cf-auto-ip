import re
import urllib.request
from bs4 import BeautifulSoup

URL = "https://vps789.com/cfip/?remarks=ip"

def fetch_ips():
    req = urllib.request.Request(
        URL, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        html = urllib.request.urlopen(req).read().decode("utf-8")
    except Exception as e:
        print(f"请求失败: {e}")
        return

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        print("未找到表格数据")
        return

    all_ips = []

    for row in table.find_all("tr"):
        cols = [ele.text.strip() for ele in row.find_all(["td", "th"])]
        if cols:
            ip = cols[0]
            # 校验是否为合法 IPv4 地址且防止重复添加
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip) and ip not in all_ips:
                all_ips.append(ip)

    if not all_ips:
        print("未提取到任何有效 IP")
        return

    # 提取第一个 IP 作为最优 IP
    best_ip = all_ips[0]

    # 保存单个最快/最优 IP
    with open("ct_fastest.txt", "w", encoding="utf-8") as f:
        f.write(best_ip)

    with open("cu_fastest.txt", "w", encoding="utf-8") as f:
        f.write(best_ip)

    # 保存所有抓取到的 IP 列表
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_ips) + "\n")

    print(f"抓取完成！共提取到 {len(all_ips)} 个 IP，最优 IP: {best_ip}")

if __name__ == "__main__":
    fetch_ips()
