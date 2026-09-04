import os
import requests
from datetime import datetime, timezone, timedelta

# Lấy webhook URL từ Secrets của GitHub
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Dữ liệu thời khóa biểu
LICH_HOC = {
    "07/09": {"sáng": {"nd": "BC", "vt": "Bãi Tập 24", "gv": "Trống"}, "chiều": {"nd": "QS1,2 (13g30-15g00)", "vt": "A2.202", "gv": "Nhiên"}},
    "08/09": {"sáng": {"nd": "ĐL1, ĐL2", "vt": "BT18", "gv": "Đ.Mạnh"}, "chiều": {"nd": "ĐL3", "vt": "BT13", "gv": "Đ.Mạnh"}},
    "09/09": {"sáng": {"nd": "ĐL4", "vt": "A3.204", "gv": "Bão"}, "chiều": {"nd": "ĐL5", "vt": "A3.204", "gv": "Bão"}},
    "10/09": {"sáng": {"nd": "QS4", "vt": "BT40", "gv": "T.Hùng"}, "chiều": {"nd": "QS3", "vt": "BT37", "gv": "T.Hùng"}},
    "11/09": {"sáng": {"nd": "ĐL6", "vt": "BT11", "gv": "N.Mạnh"}, "chiều": {"nd": "ĐL7", "vt": "BT11", "gv": "N.Mạnh"}},
    "12/09": {"sáng": {"nd": "QS6", "vt": "A3.205", "gv": "T.Hùng"}, "chiều": {"nd": "QS5", "vt": "BT22", "gv": "T.Hùng"}},
    "14/09": {"sáng": {"nd": "ĐL8", "vt": "A3.205", "gv": "Hải"}, "chiều": {"nd": "ĐL9", "vt": "A3.205", "gv": "Hải"}},
    "15/09": {"sáng": {"nd": "ĐL10,11", "vt": "BT11", "gv": "Vân"}, "chiều": {"nd": "ĐL+", "vt": "BT11", "gv": "Vân"}},
    "16/09": {"sáng": {"nd": "QS7", "vt": "A2.208", "gv": "Sơn"}, "chiều": {"nd": "QS+", "vt": "BT22", "gv": "Sơn"}},
    "17/09": {"sáng": {"nd": "Thi P1 LTP3", "vt": "A3.102", "gv": "Trống"}, "chiều": {"nd": "Thi THP3", "vt": "BT21", "gv": "Đức"}},
    "18/09": {"sáng": {"nd": "KC1", "vt": "BT31", "gv": "Ý"}, "chiều": {"nd": "KC1", "vt": "BT31", "gv": "Ý"}},
    "19/09": {"sáng": {"nd": "KC2", "vt": "BT3", "gv": "Hoàn"}, "chiều": {"nd": "KC3", "vt": "BT3", "gv": "Hoàn"}},
    "21/09": {"sáng": {"nd": "CT1", "vt": "A3.201", "gv": "Tâm"}, "chiều": {"nd": "CT2", "vt": "A3.201", "gv": "Tâm"}},
    "22/09": {"sáng": {"nd": "KC4", "vt": "BT39", "gv": "Chung"}, "chiều": {"nd": "KC4", "vt": "BT39", "gv": "Chung"}},
    "23/09": {"sáng": {"nd": "CT3", "vt": "BT12", "gv": "Hinh"}, "chiều": {"nd": "CT4,5", "vt": "BT12", "gv": "Hinh"}},
    "24/09": {"sáng": {"nd": "LT KC5,6", "vt": "BT28", "gv": "Chung"}, "chiều": {"nd": "KC7,KC+", "vt": "BT28", "gv": "Chung"}},
    "25/09": {"sáng": {"nd": "CT6,7", "vt": "A3.201", "gv": "Đ.Thắng"}, "chiều": {"nd": "CT+", "vt": "A3.201", "gv": "Đ.Thắng"}},
    "26/09": {"sáng": {"nd": "Thi THP4", "vt": "BT1", "gv": "Chung"}, "chiều": {"nd": "Thi P2 LTP4", "vt": "A2.109", "gv": "Trống"}}
}

def gui_thong_bao():
    if not WEBHOOK_URL:
        print("Lỗi: Chưa cấu hình WEBHOOK_URL")
        return

    # Lấy thời gian thực (UTC+7)
    tz_vn = timezone(timedelta(hours=7))
    now = datetime.now(tz_vn)
    
    hom_nay = "27/09"#now.strftime("%d/%m")
    ngay = 27#now.day
    thang = now.month

    # Logic thời gian chạy tự động
    if thang == 9:
        if ngay < 7:
            print(f"Hôm nay ({hom_nay}): Chưa đến ngày nhập học quân sự.")
            
        elif 7 <= ngay <= 26:
            if hom_nay in LICH_HOC:
                lich = LICH_HOC[hom_nay]
                data = {
                    "content": "Goooood Morning!🪖⏰",
                    "embeds": [{
                        "title": f"📅 LỊCH HỌC GDQP&AN - HÔM NAY ({hom_nay})",
                        "color": 3066993,
                        "fields": [
                            {
                                "name": "🌅 Sáng (7h30 - 11h00)",
                                "value": f"**Nội dung:** {lich['sáng']['nd']}\n**Vị trí:** {lich['sáng']['vt']}\n**Giảng viên:** {lich['sáng']['gv']}",
                                "inline": False
                            },
                            {
                                "name": "🌇 Chiều (13h30 - 16h30)",
                                "value": f"**Nội dung:** {lich['chiều']['nd']}\n**Vị trí:** {lich['chiều']['vt']}\n**Giảng viên:** {lich['chiều']['gv']}",
                                "inline": False
                            }
                        ],
                        "footer": {
                            "text": "📌 Nhắc nhở: Ăn sáng/tối tại Tầng trệt nhà ăn 1 (ca 1)."
                        }
                    }]
                }
                requests.post(WEBHOOK_URL, json=data)
                print(f"Đã gửi lịch học ngày {hom_nay}")
            else:
                print(f"Hôm nay ({hom_nay}): Không có lịch học")
                
        elif ngay == 27:
            # Sáng 27/9 (sau ngày thi cuối cùng) sẽ tự động gửi tin này
            data = {
                "content": "🎉 **BÁO CÁO HOÀN THÀNH NHIỆM VỤ!** 🎉\nChúc mừng chồng iu đã hoàn thành xuất xắc nhiệm vụ 🥳"
            }
            requests.post(WEBHOOK_URL, json=data)
            print("Đã gửi tin nhắn chúc mừng xuất ngũ.")
            
        else:
            print(f"Hôm nay ({hom_nay}): Đã học xong, bot chuyển về trạng thái nghỉ.")
    else:
        print("Không nằm trong tháng diễn ra môn học.")

if __name__ == "__main__":
    gui_thong_bao()
