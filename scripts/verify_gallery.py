import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

groups = re.findall(r'gallery-group-title', html)
items = re.findall(r'class="group-item"', html)
print("Gallery groups:", len(groups))
print("Gallery items:", len(items))

dups = ["elite-brands-mural-wide2", "trinity-place-exterior-sign2", "novara-reception.jpg"]
for d in dups:
    count = html.count(d)
    status = "CLEAN" if count == 0 else "WARNING: still present"
    print("  " + d + ": " + str(count) + " - " + status)

required = [
    "cybertruck-side.jpg", "957-party-vehicle-wrap.jpg",
    "peak-elevator-lobby-sign.jpg", "novara-frosted-glass.jpg",
    "kpa-lobby-sign.jpg", "glover-masonry-lobby.jpg",
    "omeara-room-wrap.jpg", "elite-brands-wall-mural.jpg", "gque-bbq-mural.jpg",
    "iheart-elevator-wrap.jpg",
    "buffalo-restaurant-exterior.jpg", "trinity-place-exterior-sign.jpg", "westbound-building-sign.jpg"
]
print("Image check:")
for img in required:
    found = ("images/" + img) in html
    print("  " + img + ": " + ("OK" if found else "MISSING"))
