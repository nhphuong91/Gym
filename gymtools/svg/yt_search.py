import urllib.request, urllib.parse, re, json, sys
qs = ["knee to wall test ankle dorsiflexion", "lateral step down test", "single leg heel raise test", "single leg stance test balance", "single leg squat test", "single leg sit to stand test", "single leg bridge test hamstring"]
hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9"}
for q in qs:
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q)
    try:
        html = urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=20).read().decode("utf-8", "replace")
    except Exception as e:
        print("##", q, "ERROR", e); continue
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    print("##", q)
    if not m:
        print("  no ytInitialData"); continue
    data = json.loads(m.group(1))
    out = []
    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                vid = v.get("videoId")
                title = "".join(r.get("text","") for r in v.get("title",{}).get("runs",[]))
                ch = "".join(r.get("text","") for r in v.get("ownerText",{}).get("runs",[]))
                ln = v.get("lengthText",{}).get("simpleText","")
                out.append((vid, title, ch, ln))
            for k in o.values(): walk(k)
        elif isinstance(o, list):
            for k in o: walk(k)
    walk(data)
    for vid, t, ch, ln in out[:8]:
        print("  ", vid, "|", t, "|", ch, "|", ln)
