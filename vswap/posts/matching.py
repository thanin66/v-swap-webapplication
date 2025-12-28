# posts/matching.py
from .models import Post, Swap, BuySell, Donation
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. โหลด Model เตรียมไว้ (โหลดครั้งเดียวตอนรัน Server)
print("Loading AI Model... (Please wait)")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
print("AI Model Loaded!")

def compute_similarity(source_text, candidates_list, threshold=0.35):
    """
    source_text: สิ่งที่ User อยากได้ (Text)
    candidates_list: รายการของที่มีคนอื่นมี [{'post': obj, 'text': '...'}, ...]
    """
    if not candidates_list:
        return []

    # แปลง Source (ความต้องการ) เป็น Vector
    source_emb = model.encode([source_text])

    # แปลง Candidates (ของที่มีทั้งหมด) เป็น Vector
    # *ข้อควรระวัง: ตรงนี้จะช้าถ้าของเยอะ แต่ทำเพื่อ Test Logic ถือว่าโอเคครับ
    candidate_texts = [c['text'] for c in candidates_list]
    candidate_embs = model.encode(candidate_texts)

    # คำนวณความเหมือน
    scores = cosine_similarity(source_emb, candidate_embs)[0]

    matched = []
    for i, score in enumerate(scores):
        if score >= threshold:
            matched.append({
                'my_post': None, # เดี๋ยวไปใส่ค่าข้างนอก
                'matched_post': candidates_list[i]['post'],
                'score': round(score * 100, 2)
            })
    
    # เรียงคะแนนมากไปน้อย
    matched.sort(key=lambda x: x['score'], reverse=True)
    
    # ส่งคืนแค่ 5 อันดับแรกเพื่อความสวยงาม
    return matched[:5]

def find_matches_for_user(user):
    """
    หัวใจหลัก: หาของที่ User นี้อยากได้ (My Demand -> System Supply)
    """
    matches_found = []
    
    # --- STEP 1: เตรียม Supply (ของที่มีในระบบ) ---
    # ดึงโพสต์ของคนอื่นทั้งหมด ที่สถานะ available
    other_posts = Post.objects.filter(status='available').exclude(owner=user)
    
    supply_candidates = []
    for p in other_posts:
        # กรอง: ไม่เอา "ประกาศรับซื้อ" ของคนอื่นมาเป็น Supply (เพราะเขาไม่มีของให้เรา)
        if p.post_type == 'buy_sell':
            # เช็คว่าเป็น BuySell object จริงๆ
            try:
                bs = p.buysell 
                if bs.is_buying: # ถ้าคนอื่นประกาศรับซื้อ ข้ามไป
                    continue
            except:
                continue

        # จัดเตรียม Text สำหรับ Supply (เอา Title + Description)
        text_desc = f"{p.title} {p.description}"
        supply_candidates.append({
            'post': p,
            'text': text_desc
        })

    if not supply_candidates:
        return [], [] # ถ้าไม่มีของในระบบเลย ก็จบข่าว

    # --- STEP 2: วนลูปความต้องการของเรา (My Demand) ---
    
    # 2.1 กรณีเราลง Swap (เรามีของ A อยากแลกของ B) -> Demand คือ B
    my_swaps = Swap.objects.filter(owner=user, status='available')
    for my_post in my_swaps:
        # สิ่งที่เราอยากได้
        want_text = my_post.swap_item_description 
        
        # ส่งไปให้ AI หาคู่
        results = compute_similarity(want_text, supply_candidates)
        
        for res in results:
            res['my_post'] = my_post # ระบุว่าโพสต์ไหนของเราที่เจอคู่นี้
            matches_found.append(res)

    # 2.2 กรณีเราลงรับซื้อ (is_buying=True) -> Demand คือ Title/Desc ของเรา
    my_buys = BuySell.objects.filter(owner=user, is_buying=True, status='available')
    for my_buy in my_buys:
        # สิ่งที่เราอยากซื้อ
        want_text = f"{my_buy.title} {my_buy.description}"
        
        # ส่งไปให้ AI หาคู่
        results = compute_similarity(want_text, supply_candidates)
        
        for res in results:
            res['my_post'] = my_buy
            matches_found.append(res)

    # เรียงลำดับตามคะแนนความแมทช์รวมทั้งหมดอีกที
    matches_found.sort(key=lambda x: x['score'], reverse=True)

    return matches_found, [] # return matches_incoming, matches_outgoing (ว่างไว้ก่อน)