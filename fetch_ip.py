import re
import requests
from bs4 import BeautifulSoup

URL = "https://v2rayssr.com/cfip/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_ips():
    response = requests.get(URL, headers=headers, timeout=15)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')
    
    ip_list = []
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            isp = cols[1].text.strip()
            # 提取表格中的纯 IP 地址
            raw_ip = cols[2].text.replace('已复制!', '').strip()
            
            # 正则校验是否为合法 IPv4 / IPv6
            if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', raw_ip) or ':' in raw_ip:
                # 拼接格式：IP#线路名称
                ip_list.append(f"{raw_ip}#{isp}优选")

    # 取前 15 个延迟最低/速度最快的 IP
    top_ips = ip_list[:15]
    
    if top_ips:
        with open("ip.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(top_ips))
        print("✅ 成功提取并保存了最新 IP！")
    else:
        print("⚠️ 未提取到合适数据，请检查网页格式。")

if __name__ == "__main__":
    fetch_ips()
