import json
from datetime import date

with open('posts.json', 'r') as f:
    existing_posts = json.load(f)

existing_keys = set()
for p in existing_posts:
    key = p['body'][:80].lower().strip()
    existing_keys.add(key)

next_id = max(p['id'] for p in existing_posts) + 1
today = date.today().isoformat()

def detect_conditions(text):
    t = text.lower()
    cond_map = {
        'bunion': 'bunion', 'hammer toe': 'hammer toe', 'hammertoe': 'hammer toe',
        'hallux valgus': 'hallux valgus', 'hallux limitus': 'hallux limitus',
        'hallux rigidus': 'hallux rigidus', "tailor's bunion": "tailor's bunion",
        'bunionette': 'bunionette', 'plantar fasciitis': 'plantar fasciitis',
        'heel spur': 'heel spur', 'flat feet': 'flat feet', 'flat foot': 'flat feet',
        'toenail fungus': 'toenail fungus', 'fungal nail': 'toenail fungus',
        'ingrown toenail': 'ingrown toenail', 'ingrown': 'ingrown toenail',
        'metatarsalgia': 'metatarsalgia', 'neuroma': 'neuroma',
        "morton's neuroma": 'neuroma', 'morton neuroma': 'neuroma',
        'sesamoiditis': 'sesamoiditis', 'gout': 'gout', 'arthritis': 'arthritis',
        'bone spur': 'bone spur', 'neuropathy': 'neuropathy', 'edema': 'edema',
        'tendonitis': 'tendonitis', 'plantar plate': 'plantar plate tear',
    }
    found = set()
    results = []
    for keyword, condition in cond_map.items():
        if keyword in t and condition not in found:
            found.add(condition)
            results.append(condition)
    return ', '.join(results) if results else ''

def detect_surgery(text):
    t = text.lower()
    surg_map = {
        'minimally invasive': 'MIS', 'minimal invasive': 'MIS', 'mis ': 'MIS',
        'lapiplasty': 'Lapiplasty', 'scarf': 'scarf akin', 'akin': 'scarf akin',
        'osteotomy': 'osteotomy', 'chevron': 'chevron', 'austin': 'Austin',
        'arthroplasty': 'arthroplasty', 'arthrodesis': 'arthrodesis',
        'bunionectomy': 'bunionectomy', 'toe fusion': 'toe fusion',
        'fusion': 'toe fusion', 'mica': 'MICA', 'percutaneous': 'percutaneous',
        'cheilectomy': 'cheilectomy',
    }
    found = set()
    results = []
    for keyword, surgery in surg_map.items():
        if keyword in t and surgery not in found:
            found.add(surgery)
            results.append(surgery)
    return ', '.join(results) if results else ''

def detect_treatments(text):
    t = text.lower()
    treat_map = {
        'surgery': 'surgery', 'physical therapy': 'physical therapy', 'physio': 'physical therapy',
        'cortisone': 'cortisone', 'steroid injection': 'steroid injection',
        'orthotic': 'orthotics', 'taping': 'taping', 'icing': 'icing', 'ice ': 'icing',
        'elevation': 'elevation', 'elevat': 'elevation', 'stretching': 'stretching',
        'stretch': 'stretching', 'massage': 'massage', 'acupuncture': 'acupuncture',
        'shockwave': 'shockwave therapy', 'laser': 'laser therapy',
        'anti-inflammatory': 'anti-inflammatory', 'ibuprofen': 'ibuprofen',
        'night splint': 'night splint', 'rolling': 'rolling',
        'arch support': 'arch support', 'antibiot': 'antibiotics',
        'anti fungal': 'antifungal', 'antifungal': 'antifungal',
        'soaking': 'soaking',
    }
    found = set()
    results = []
    for keyword, treatment in treat_map.items():
        if keyword in t and treatment not in found:
            found.add(treatment)
            results.append(treatment)
    return ', '.join(results) if results else ''

def detect_products(text):
    t = text.lower()
    prod_map = {
        'hoka': 'Hoka', 'orthofeet': 'Orthofeet', 'new balance': 'New Balance',
        'skechers': 'Skechers', 'brooks': 'Brooks', 'nike': 'Nike',
        'birkenstock': 'Birkenstock', 'vionic': 'Vionic', 'oofos': 'Oofos',
        'crocs': 'Crocs', 'correct toes': 'Correct Toes',
        'kerasal': 'Kerasal', 'kuru': 'Kuru', 'knee scooter': 'knee scooter',
    }
    found = set()
    results = []
    for keyword, product in prod_map.items():
        if keyword in t and product not in found:
            found.add(product)
            results.append(product)
    return ', '.join(results) if results else ''

new_posts_raw = [
    {"body": "Good morning, new to the group. My x-rays showed my right bunion to be severe and arthritic, plus I have flat feet. The Dr. recommends bunion fusion surgery. I am a 66 yr old female. Has anyone had this surgery, and how was the recovery, the results afterward?", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Those of you with hypermobile feet, pretty severe bunions as well as flat feet - which procedure did you go with? I have seen two different doctors. Both with great reviews. One recommends Lapiplasty and the other recommends a traditional approach with scarf and Akin osteotomy. I'm torn on what to do.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Has anyone had a big bunion fixed and fusion for flat feet? I'm looking into options and want to hear from people who've had both addressed at the same time.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Has anyone had surgery to fix a bunion and flat feet? I just had my first consultation. I didn't get good vibes from my doctor. He was very eager to say surgery for this and surgery for that, like it was so simple. He suggested bunion correction, flat feet correction, and lengthening my calves. Anyone have this or have any advice?", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Positive story so far. Had lapiplasty in January of this year on the right foot. Not gonna lie it was living hell the first few days. But my bones fused in record time and its been pretty seamless since. Still some swelling and tenderness but every day is a little better. Had MIS surgery today on my left foot. So far its been painless! He numbed the foot but no nerve block. He doesn't like doing them, thinks it causes nerve damage. Will be partial weight bearing tomorrow as tolerated. So far I'm glad I did both feet and hope to be walking without bunion pain soon!", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Hey yall! I am having the lapiplasty operation on my left foot this June! I had the Austin procedure done to my right foot in 2022. It was a long hard recovery. But the pain was manageable. Just took a long time for my foot to look normal nevertheless, it changed my life for the better! And it's time to do the left! I am in pain all day everyday! I am wondering if anyone has had the two separate procedures on their feet?", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Recovery update after my June 2025 bunion repair - Lapiplasty with correction of the bunion with Calcaneal Bone Graft and lesser toe corrections. Non-weight bearing for 4 weeks to walking in boot for 4 weeks. Then transitioned to a tennis shoe for 12 weeks of physical therapy and returned to work in October on modified duty. After returning, I started having pain under the outside of my ankle toward pinkie toe.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Good Morning! I will be having Lapiplasty procedure done on April 8th. I know how some feel about this procedure, but my DR and I have agreed this is best for me. My question, what is something that you wish you did before your surgery or bought to help with recovery?", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Hi has anyone tried softwave for Morton neuroma? I've been dealing with this pain for months and looking for alternatives to surgery.", "source_group": "Forefoot forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"},
    {"body": "I'm trying to decide between surgical options or no surgery. I'm 57 years old and have lots of travel and other plans for being active. Problem: painful toes for 15+ years and metatarsal ball of foot pain since last fall. Cause of pain: toes stepping on the bottoms of their neighboring toes causing painful sores and prominent metatarsals taking too much impact, leading to stress fractures.", "source_group": "Forefoot forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"},
    {"body": "I'm hoping for some advice. I live in the UK and I hurt my foot at the beginning of June. The pain is around the ball of my foot, it feels like there is a lump there and it's painful to walk on. I have been to my GP, who thinks it may be a Morton's neuroma and has referred me to hand and foot surgery. I'm not convinced as it is now making my second toe stick up and there is generalised swelling in the area.", "source_group": "Forefoot forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"},
    {"body": "Is Plantar calcaneal spur the same thing as plantar fasciitis? That's what my X-ray said and I have my dr appointment in May. I'm confused about the difference and what treatment to expect.", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "Plantar fasciitis with multiple treatments for 15 years. Just got steroid injections. It cleared the pain up all except for where my heel spur is in my left foot. The insoles make me feel the best, but depending on what shoe I'm wearing, my feet either slide to the outside where I start getting pains. So I tried Kuru. With these shoes every step gives me pain in my heel spur.", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "I do feel a bit uneasy. Had TenJet surgery in December after injections and boot and all that jazz to try to heal my PF. Still had more pain weeks after procedure. Doctor ordered another MRI and PF got worse, is now tearing off the heel bone on the inside and lateral side plus tendinitis of the tibia tendon and heel spurs. Podiatrist recommended releasing the fascia as we have been at this for 2 years now with no progress.", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "Anyone else only have pain in their heel? Not even the bottom of my heel, it's the sides. Hurts when I squeeze them from the sides and when I walk. Anything you find that helps with this?", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "I had my first shockwave treatment on my left heel but it didn't hurt at all. I was under the impression that shockwave hurts. Has anyone else had it not hurt? Even my podiatrist was surprised. Has shockwave helped cure your PF?", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "Can you walk in these type of night splints? I have to get up to use the rest room, but most, you get up and walk on them they fall or lose the secureness of them. I know you can walk on a boot, so are these kind the same concept?", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "I have had heel spurs with plantar fasciitis under both feet for 20 months now. I have tried a night splint, 8 shockwave treatments, 5 osteopath visits, orthopedic insoles, stretching and strengthening exercises including with a ball, cooling, and massage devices. Nothing helps; I am at my wit's end. Do you have any tips? I am a young woman of 29.", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "Almost fully recovered thanks to my night splint. Next up: 10 day trip to Paris this summer. I have very flat feet, so a little lift in my shoes works wonders. Experienced flat footers weigh in! What sandal would you recommend for flat feet and somewhat stylish?", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "Is night splint a big help for you guys? Planning to buy those. I've been dealing with plantar fasciitis for several months and trying to find what actually works.", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "While a night splint does seem to help, it's bulky and uncomfortable. My sheets are loose, but my feet are pointed down while I sleep and that seems to aggravate BOTH calves. Are y'all using anything while you sleep that keeps your feet more towards 90 degrees?", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "Fungus is different for every person. Had another doctors appointment yesterday. Had a really good chat with him about this. He told me toenail fungus is different for all of us which is why there isn't a 100 percent cure or product out there to offer from any medical professional.", "source_group": "Toenail Fungus Support & Management"},
    {"body": "I have fought and learned to live with toenail fungus for 15 years. If it's easy enough to contract it at the gym or the pool, why haven't my husband or kids caught it? Is this the case with any of you?", "source_group": "Toenail Fungus Support & Management"},
    {"body": "Podiatrist appointment today. Not ingrown. He said it was curved though and cut it down. Not throbbing now, so we will see. When he cut it, most of the fungus is gone. The other toe still has some fungus though. I'm still using anti fungal and soaking. So hoping maybe I got it early enough.", "source_group": "Toenail Fungus Support & Management"},
    {"body": "I keep reading having an unhealthy diet gives you toenail fungus! As a former professional footballer for 22 years I have had the best dietician, personal trainers fitness programmes. I maintained very good fitness all my life and a healthy balanced diet. I have never had any toenail issues until 15 years ago after my career. I shared changing rooms with many other team mates including showers.", "source_group": "Toenail Fungus Support & Management"},
    {"body": "Does anyone here who has toenail fungus also have OCD contamination? I think I do and the two of these conditions together have been very rough on me. Anyone else? Any tips on how you mentally deal with possibly having these conditions together?", "source_group": "Toenail Fungus Support & Management"},
    {"body": "I have done 3 cortisone injections in each heel. We are now talking surgery vs shockwave therapy. The shockwave therapy they offer is 750 dollars upfront to go once a week for 5 weeks for one foot. Has anyone done the once a week for 5 weeks for the shockwave therapy? Any relief?", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "When cortisone finally stopped working I went with the next best thing. Had my first shockwave treatment today. He said I will probably need 4-5 treatments. If it doesn't work I can opt for plasma injections or surgery. He has much better success with immature plasma extracted from umbilical cords. One day at a time.", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "I received a cortisone shot this past Thursday and not seeing any results! My foot hurts so bad to walk and even burns on the back of my upper heel. Any thoughts to my next step? I've even been doing my stretches.", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "Been offered cortisone or shockwave? I've had plantar fasciitis for nearly 1 year and getting worse. What's best in your experience?", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "Just got first cortisone shot for PF. Anyone have luck with that? Hoping this gives me some relief after months of dealing with the pain.", "source_group": "Plantar Fasciitis Talk and Tips Support Group"},
    {"body": "I transitioned into shoes last Thursday and I went and bought 8.5 mens wide Hoka Bondi 9. The women's Hoka shoe at the store don't have a wide. I feel so good in the men's wide. This week marks 10 weeks post op. I'm now walking around 8-10k steps most days. I continue to elevate my foot and ice it anytime I'm sitting down.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Any ladies out there looking for sandals should check these two out, one high end price and one is low end. Hoka Infini Hike TC and Whitin Hiking Sandal. Both have been very comfortable since transitioning from having to wear a carbon fiber insole. They also are fully adjustable and allow for my swelling that I am still experiencing.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Shoes or slippers? I was fitted for Hoka Clifton at running shop. I wore these on Sunday, but shoes seem pretty snug on surgical foot. Foot was too swollen for any shoes by mid-morning on Monday so I bought extra large mens slippers. Should I buy a size up for my surgical foot?", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "7 days post washing my foot. I can see it healing. Thank you bunion family for encouraging to wash. Someone said washing will help with healing. I've been using antibacterial soap. Currently 8 weeks post op. Hopefully I can drive soon. What sneakers are better Hoka or Brooks?", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Sandal suggestions? I will be post op a year in June. Just got home from Spring Break and couldn't wear my pre surgery sandals. They hurt my foot. I hate socks and shoes in the summer. I need to find something comfortable to wear.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Anyone with a current bunion have pain and tenderness on the top center of the foot with the bunion? Swelling at end of day as well. Looking to hear if this is common.", "source_group": "Minimally invasive bunion surgery"},
    {"body": "Here is my journey with having both pinky toes fixed for hammertoes. 4 weeks post op and I am cleared for regular shoes. Still a little painful from the incision area while in shoes but still went to a wide width while I heal up. Dr says they can be swollen for months.", "source_group": "Minimally invasive bunion surgery"},
    {"body": "I'm 4 and a half months into my surgery, and my foot is still super sensitive even when I take a shower and the water hits my foot. Is this normal? Swelling still comes and goes especially with the heat. I try icing behind the knee and keeping myself cool, but it swells to an uncomfortable level.", "source_group": "Minimally invasive bunion surgery"},
    {"body": "I am 6 weeks post op from MIS on left foot. No pins or screws. Cleared to get into regular shoes and cleared for most types of exercise. First 4 weeks I was in a boot, then went to oversized shoes wearing a brace on the toe. Very little swelling, minimal pain. All recoveries are different but that's my story.", "source_group": "Minimally invasive bunion surgery"},
    {"body": "I had surgery on January 9th. MIS and hammertoe correction. My outside ankle really is swollen and hurting a lot. Has anyone else noticed this at all?", "source_group": "Minimally invasive bunion surgery"},
    {"body": "Thanks for the add! Here are pics of my progress so far. Pictures of hardware before and after and 2 week and 4 week progress. How long do you feel the stiffness inside your foot? My dr said to expect swelling for up to 6 months.", "source_group": "Minimally invasive bunion surgery"},
    {"body": "So good and bad. I went to the Dr today cause my left toe next to my pinky feels like someone is squeezing it. Sometimes real painful, sometimes not. I got an ingrown toenail! And of course that toe has fungus on it. Referral to podiatrist, just have to wait a couple weeks. My PCP gave me antibiotics and told me to soak it too.", "source_group": "Toenail Fungus Support & Management"},
    {"body": "I had a partial ingrown toenail removed earlier today. I did not know it could possibly involve chemicals. I'm breastfeeding and am worried they used Phenol. Is there any way to tell?", "source_group": "Toenail Fungus Support & Management"},
    {"body": "It gives me a giggle to know I have fungus at 25. I've had it for 2 years now with nothing helping or curing it. I just recently used some kerasal to make my nail mushy to get rid of the icky under the nail plate. I have tried multiple different things including medication from doctors, nail polish type things, oils, creams. I think I might schedule an appointment with the podiatrist to get my toenail removed.", "source_group": "Toenail Fungus Support & Management"},
    {"body": "Has anyone had all their toe nails removed with the nail bed before? I would like some photos once all healed. I am looking to get this done as I have tried everything including the tablets 3 times and they come back worse each time.", "source_group": "Toenail Fungus Support & Management"},
    {"body": "I come from a long line of people with big bunions. Both my mother and grandmother had much worse bunions than I do. Mine were exacerbated by surgery to remove tophi from many gout episodes 2.5 years ago. I've lost weight and taken meds to further shrink remaining tophi. I have a hard time with most shoes but have learned to manage by wearing zero drop shoes with a wide toe box.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Hi everyone! Will be having surgery on Thursday for bunion and hammertoe. Also they will be taking a bit of bone from my heel to fill a negative space where gout has eroded the bone. I wasn't worried until I began researching. Now I'm a bit terrified.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "Hi! I am six weeks post op and I have been walking in recovery shoe. I have been given the go ahead to walk without it. Please give me your advice about footwear, techniques, physiotherapy, anything.", "source_group": "Bunion Support Group"},
    {"body": "I'm just feeling really defeated with my recovery at the moment. My physio even said to me in our session yesterday, what happened to me was not normal and shouldn't have happened, that my case is complex and very unfortunate. It's really frustrating that I had to suffer so much more because of a negligent doctor.", "source_group": "Bunion Support Group"},
    {"body": "Update - I sent the picture to my foot doctor today and received a phone call back. He says it looks fine. I appreciate everyone's input. And I wish all of us a speedy full recovery! I had bunion surgery 18 days ago. I was told to take a shower today. I still can't put weight on that foot.", "source_group": "Bunion Support Group"},
    {"body": "Good afternoon all. I'm just wondering who in their 70s has had the big toe broken and plated bunion operation and hammer toe fixed. My bunions are severe but don't hurt anymore but the hammer toe now crossing over the big toe is painful. I also have osteoarthritis. Was wanting feedback on those older who've had the operation and recovery.", "source_group": "Bunion Support Group"},
    {"body": "How's your back, neck and mind after surgery and during recovery? I'm scared of the whole process. Been to my first consultation today. Was diagnosed with a mild bunion but looks like its getting worse daily. Scared of surgery as I also have no job at the moment and need to save up for recovery. I'm only 36 but also have no support group.", "source_group": "Bunion Support Group"},
    {"body": "For my friends in UK. My bunions are pretty bad and operating is for medical reasons. Has anyone had minimal invasive surgery and were you happy with it? Looking for UK experiences.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "5 weeks post OP. Minimal invasive surgery. Bunionectomy, silver bunionectomy, McBride soft tissue procedures as well as Akin osteotomy. 5th metatarsal Weil osteotomy and claw toe correction splinted with K wire. First picture in the morning after elevating. Second picture swollen foot after walking less than 20 metres.", "source_group": "Minimally invasive bunion surgery"},
    {"body": "5 years post surgery. Does anyone have insight for surgery several years out? I've been relatively pain free after all the recovery. However recently, almost 5 years post surgery, I'm having significant pain and discomfort. Also having a hard time finding comfortable shoes for not just the bunion area, but my entire footbed and arch.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "6 weeks post op. I was wondering if others experience more swelling when they first get up in the morning rather than after being up and walking around? Maybe its the blood moving that helps? My first few steps in the morning always make me feel like I've taken a step back in my recovery.", "source_group": "bunion surgery / foot surgery support group"},
    {"body": "How do you keep your toenails healthy while treating fungus? I've been trying various products and want to make sure I'm not damaging the nail further in the process.", "source_group": "Toenail Fungus Support & Management"},
]

added = 0
for post in new_posts_raw:
    key = post['body'][:80].lower().strip()
    if key in existing_keys:
        continue
    new_post = {
        "id": next_id,
        "body": post['body'],
        "author": None,
        "url": None,
        "source_group": post['source_group'],
        "date_captured": today,
        "conditions_mentioned": detect_conditions(post['body']),
        "surgery_types_mentioned": detect_surgery(post['body']),
        "treatments_mentioned": detect_treatments(post['body']),
        "products_mentioned": detect_products(post['body']),
        "comments": [],
        "images": []
    }
    existing_posts.append(new_post)
    existing_keys.add(key)
    next_id += 1
    added += 1

with open('posts.json', 'w') as f:
    json.dump(existing_posts, f, indent=2)

print(f"Added {added} new posts. Total: {len(existing_posts)}")

from collections import Counter
conditions = Counter()
for p in existing_posts:
    for c in [x.strip() for x in p.get('conditions_mentioned', '').split(',') if x.strip()]:
        conditions[c] += 1
print("\nCondition breakdown:")
for k, v in conditions.most_common():
    print(f"  {k}: {v}")
