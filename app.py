from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# โหลดข้อมูลห้องและเส้นทางภายในอาคาร
with open("data/indoor_routes.json", "r", encoding="utf-8") as f:
    indoor_routes = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/navigate", methods=["GET", "POST"])
def navigate():
    room = request.args.get("room")  # รองรับ GET
    if not room:  # ถ้า GET ไม่เจอ ลองใช้ POST
        room = request.form.get("room")  

    print(f"กำลังค้นหาห้อง: {room}")  # Debug เช็คค่า

    # ตรวจสอบว่าห้องอยู่ในข้อมูลหรือไม่
    if room in indoor_routes:
        room_info = indoor_routes[room]
        return render_template("navigation.html", 
                               room=room, 
                               lat=room_info["lat"], 
                               lng=room_info["lng"], 
                               steps=room_info["steps"])
    else:
        return "ไม่พบห้องที่ต้องการ", 404

# API ค้นหาห้องแบบอัตโนมัติ
@app.route("/search_rooms", methods=["GET"])
def search_rooms():
    query = request.args.get("q", "").strip().lower()
    suggestions = [room for room in indoor_routes if query in room.lower()]
    return jsonify(suggestions[:5])  # ส่งกลับ 5 ตัวเลือกที่ใกล้เคียง

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
