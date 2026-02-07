from .models import Post, Swap, BuySell, Donation
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = None 

def get_model():
    global model
    if model is None:
        print("Loading AI Model...")
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return model

def compute_similarity(source_text, candidates_list, threshold=0.35):
    """
    source_text: สิ่งที่ User อยากได้ (Text)
    candidates_list: รายการของที่มีคนอื่นมี [{'post': obj, 'text': '...'}, ...]
    """
    if not candidates_list:
        return []

    ai_model = get_model() # เรียกผ่านฟังก์ชันแทน
    source_emb = ai_model.encode([source_text])

    candidate_texts = [c['text'] for c in candidates_list]
    candidate_embs = ai_model.encode(candidate_texts)

    scores = cosine_similarity(source_emb, candidate_embs)[0]

    matched = []
    for i, score in enumerate(scores):
        if score >= threshold:
            matched.append({
                'my_post': None, 
                'matched_post': candidates_list[i]['post'],
                'score': round(score * 100, 2)
            })
    
    matched.sort(key=lambda x: x['score'], reverse=True)
    
    return matched[:5]

def find_matches_for_user(user):
    matches_found = []
    
    # --- STEP 1: หา "ของที่มีคนปล่อย" (Supply) ---
    # เราหาคนอื่นที่มีของ (ไม่เอาของตัวเอง)
    other_posts = Post.objects.filter(status='available').exclude(owner=user)
    
    supply_candidates = []
    for p in other_posts:
        real_post_obj = p # ค่าเริ่มต้น
        
        if p.post_type == 'buy_sell':
            # ถ้าเป็น BuySell ให้ลองดึง object ลูกมา
            if hasattr(p, 'buysell'):
                real_post_obj = p.buysell
                
                if real_post_obj.is_buying:
                    continue
            else:
                # กรณีข้อมูลผิดพลาด (มี Post แต่หาตารางลูกไม่เจอ) ให้ข้าม
                continue

        elif p.post_type == 'swap':
            if hasattr(p, 'swap'):
                real_post_obj = p.swap
            else:
                continue

        elif p.post_type == 'donate':
            if hasattr(p, 'donation'):
                real_post_obj = p.donation
            else:
                continue
        
        # -----------------------------------------------------------
        
        # สร้าง text สำหรับทำ embedding
        # ใช้ real_post_obj แทน p เพื่อความชัวร์ (แม้ title/description จะอยู่ที่แม่ก็ตาม)
        text_desc = f"{real_post_obj.title} {real_post_obj.description}"
        
        # เก็บลง list โดยใช้ object ที่แปลงร่างเป็นลูกแล้ว (real_post_obj)
        supply_candidates.append({
            'post': real_post_obj,  # <--- ส่งตัวลูกที่มี price ไปให้ Template
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

    #  กรณีเราลงรับซื้อ (is_buying=True) -> Demand คือ Title/Desc ของเรา
    my_buys = BuySell.objects.filter(owner=user, is_buying=True, status='available')
    for my_buy in my_buys:
        # สิ่งที่เราอยากซื้อ
        want_text = f"{my_buy.title} {my_buy.description}"
        
        # ส่งไปให้ AI หาคู่
        results = compute_similarity(want_text, supply_candidates)
        
        for res in results:
            res['my_post'] = my_buy
            matches_found.append(res)

    
    matches_found.sort(key=lambda x: x['score'], reverse=True)

    return matches_found, [] 