import re
import urllib.request
from bs4 import BeautifulSoup

URL = "https://v2rayssr.com/cfip/"


def fetch_ips():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
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

    ct_ips = []  # 电信
    cu_ips = []  # 联通

    for row in table.find_all("tr"):
        cols = [
            ele.text.strip().replace("已复制!", "").strip()
            for ele in row.find_all(["td", "th"])
        ]
        if len(cols) >= 3:
            line_type = cols[1]
            ip = cols[2]

            # 校验是否为合法 IPv4 地址
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
                if "电信" in line_type:
                    ct_ips.append(ip)
                elif "联通" in line_type:
                    cu_ips.append(ip)

    # 取延迟最低/速度最快的第一个 IP（页面已按速度/排名排序）
    best_ct = ct_ips[0] if ct_ips else ""
    best_cu = cu_ips[0] if cu_ips else ""

    # 保存电信最快 IP
    with open("ct_fastest.txt", "w", encoding="utf-8") as f:
        f.write(best_ct)

    # 保存联通最快 IP
    with open("cu_fastest.txt", "w", encoding="utf-8") as f:
        f.write(best_cu)

    # 保存合并文本（多行或单行带标签均可，以下示例按换行保存）
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write(f"# 电信最快\n{best_ct}\n# 联通最快\n{best_cu}\n")

    print(f"抓取完成！电信最快: {best_ct}，联通最快: {best_cu}")


if __name__ == "__main__":
    fetch_ips()
