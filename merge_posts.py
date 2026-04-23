import json
import re

# Load existing posts
with open('/tmp/fixfeetfast2/posts.json', 'r') as f:
    existing_posts = json.load(f)

print(f"Existing posts: {len(existing_posts)}")

# Build lookup by first 80 chars
existing_keys = {}
for post in existing_posts:
    key = post.get('body', '')[:80].lower().strip()
    existing_keys[key] = post

next_id = max(p.get('id', 0) for p in existing_posts) + 1

# Auto-detect lists
CONDITIONS = ['bunion', 'hammer toe', 'hallux valgus', 'hallux limitus', 'hallux rigidus', 
    "tailor's bunion", 'bunionette', 'plantar fasciitis', 'heel spur', 'flat feet', 
    'toenail fungus', 'ingrown toenail', 'metatarsalgia', 'neuroma', 'sesamoiditis', 
    'gout', 'arthritis', 'bone spur', 'callus', 'corn', 'blister', 'neuropathy', 
    'edema', 'tendonitis', 'plantar plate tear', 'bursitis', 'athletes foot']

SURGERY_TYPES = ['MIS', 'minimally invasive', 'Lapiplasty', 'scarf akin', 'osteotomy', 
    'chevron', 'Austin', 'arthroplasty', 'arthrodesis', 'bunionectomy', 'toe fusion', 
    'MICA', 'percutaneous', 'cheilectomy', '360 bunionplasty', 'bursectomy']

PRODUCTS = ['Hoka', 'Orthofeet', 'New Balance', 'Skechers', 'Brooks', 'Nike', 'Asics',
    'Birkenstock', 'Vionic', 'Oofos', 'Crocs', 'Correct Toes', 'Yoga Toes', 
    'Mind Bodhi', "Dr. Scholl's", 'Superfeet', 'Powerstep', 'KT Tape', 'Voltaren',
    'Biofreeze', 'Theragun', 'ERGOfoot', 'Betadine', 'Vicks', 'Lamisil', 'Jublia',
    'Kerasal', 'FungiNail', 'Hobibear', 'Altra', 'Dansko', 'Xero Shoes', 'Vivobarefoot',
    'Lems', 'Topo Athletic']

TREATMENTS = ['surgery', 'physical therapy', 'cortisone', 'steroid injection', 'orthotics',
    'taping', 'icing', 'elevation', 'stretching', 'massage', 'acupuncture', 
    'shockwave therapy', 'laser therapy', 'MLS laser', 'anti-inflammatory', 'ibuprofen',
    'gabapentin', 'custom orthotics', 'terbinafine', 'tea tree oil', 'night splint',
    'rolling', 'arch support', 'PRP', 'epsom salt', 'apple cider vinegar', 'castor oil',
    'Listerine', 'graston', 'zinc oxide tape', 'lidocaine']

def detect_items(text, items):
    found = []
    text_lower = text.lower()
    for item in items:
        if item.lower() in text_lower:
            found.append(item.lower())
    return ', '.join(sorted(set(found))) if found else ''

def make_post(body, comments, source_group):
    global next_id
    all_text = body + ' ' + ' '.join(comments)
    post = {
        'id': next_id,
        'body': body,
        'comments': comments,
        'author': None,
        'url': None,
        'source_group': source_group,
        'images': [],
        'conditions_mentioned': detect_items(all_text, CONDITIONS),
        'surgery_types_mentioned': detect_items(all_text, SURGERY_TYPES),
        'products_mentioned': detect_items(all_text, PRODUCTS),
        'treatments_mentioned': detect_items(all_text, TREATMENTS)
    }
    next_id += 1
    return post

def merge_post(new_body, new_comments, source_group):
    """Try to merge with existing, or add as new. Returns 'new', 'enriched', or 'duplicate'."""
    global next_id
    key = new_body[:80].lower().strip()
    
    if key in existing_keys:
        existing = existing_keys[key]
        status = 'duplicate'
        
        # Merge comments
        existing_comment_keys = set(c[:50].lower().strip() for c in existing.get('comments', []))
        new_added = 0
        for comment in new_comments:
            if comment[:50].lower().strip() not in existing_comment_keys:
                existing.setdefault('comments', []).append(comment)
                existing_comment_keys.add(comment[:50].lower().strip())
                new_added += 1
        
        # Merge longer body
        if len(new_body) > len(existing.get('body', '')):
            existing['body'] = new_body
        
        # Re-detect metadata with all text
        all_text = existing['body'] + ' ' + ' '.join(existing.get('comments', []))
        for field, items in [('conditions_mentioned', CONDITIONS), ('surgery_types_mentioned', SURGERY_TYPES),
                            ('products_mentioned', PRODUCTS), ('treatments_mentioned', TREATMENTS)]:
            existing_vals = set(v.strip().lower() for v in existing.get(field, '').split(',') if v.strip())
            new_vals = set(v.strip().lower() for v in detect_items(all_text, items).split(',') if v.strip())
            combined = existing_vals | new_vals
            if combined:
                existing[field] = ', '.join(sorted(combined))
        
        if new_added > 0:
            status = 'enriched'
        return status, new_added
    else:
        post = make_post(new_body, new_comments, source_group)
        existing_posts.append(post)
        existing_keys[key] = post
        return 'new', len(new_comments)

# ============================================
# ALL SCRAPED POSTS FROM THIS RUN
# ============================================

new_count = 0
enriched_count = 0
total_new_comments = 0

# --- PF GROUP: Feed browsing ---
# Post 1: PRP post
status, nc = merge_post(
    "Just talk to doc, I've decided to do PRP. Anyone done this I'm a chicken",
    [
        "Don't waste your money.",
        "I have and it's not effective at all!!",
        "Tape your feet with zinc oxide tape",
        "My son is college pitcher and had it done in his shoulder without success, but I think it just depends. He's had teammates have success. Give it a try!",
        "Following.. in the same boat!",
        "I've had this done on my left foot for Plantar Fasciitis and it was fantastic! Had it done in 2019 and to this day no issue with PF in that foot.",
        "I done this for my elbow helped for a year or so. I have PF have for years have tried everything except that or surgery nothing works",
        "The tendons and ligaments around my wife's hip was causing her very bad pain. She did everything the doctor recommended and nothing helped. He told her that a PRP injection has helped some but not everyone. She decided to try it. 3 weeks later the pain began to subside and now she's pain free.",
        "A friend did it for an elbow thing. Said he's pain free and very happy with PRP.",
        "Evidence shows that progressive strengthening of the foot and other relevant muscles is the most effective way to treat PF, and prevent it from ever returning."
    ],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- PF GROUP: "anyone else" search ---
# Post 2: Foot cramps
status, nc = merge_post(
    "Does anyone else get frequent foot cramps? I get them pretty often and in all areas of my feet. I just wonder if it's related to PF or something different.",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 3: Thyroid connection
status, nc = merge_post(
    "Has anyone else in the group had their thyroid removed? I'm just wondering if there could be a connection.",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 4: Treadmill flare-up
status, nc = merge_post(
    "Does the treadmill make anyone else's pf flare up and burn? I want to exercise but I suffer for days if I push myself. What other exercises is good that won't make pf flare up?",
    [
        "Yes. My doctor said no treadmill. I do the exercise bike and yoga",
        "The treadmill is one of the worst things that you can be on because every single solitary step is exactly the same one right after the other. The alternative would be either a really good exercise bike or what I think is the best of the best which is an elliptical.",
        "At physical therapy I would start on a bike for 5 minutes to get the blood moving. I usually stayed on it longer",
        "Elliptical, NuStep, Bike, Swimming, weights, Rower.",
        "Yep, switched to the bike for a year. Hated it. But necessary. I bought my own seat to bring to the gym",
        "I had to switch to swimming",
        "Treadmill use was one of the reasons I have pf. It's very bad for pf. Elliptical trainer has been my go to",
        "An incline over 3 will do it.",
        "Unfortunately treadmills don't have the same force absorption as the ground does. I would avoid the treadmill until your PF subsides.",
        "I was thinking of trying a rowing machine. I heard it is great exercise! Anyone tried rowing with pf?"
    ],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 5: Epsom salts soak
status, nc = merge_post(
    "I don't know if this may help anyone else but recently I have been soaking my feet in very hot water, with Epsom salts, apple cider vinegar and tea tree oil. My pain is receding and I am managing to run 12 miles a week slowly.",
    [
        "What is the proportion for apple cider, epsom and tea tree oil? thanks",
        "U had only inflammation?",
        "How much time soaking",
        "How much of the Epsom salts, apple cider vinegar, and tee tree oils do you use? How long do you soak them?",
        "Yes! I did this as well and it helped a Lot! After being in pain n barely walking for 6 months or so, my feet have been great for past 3 months!",
        "Hot Epson water is the only thing that relieved my pain.",
        "Everybody talks about their heel hurting, but mine is sore right in the middle of my foot so do you all think that is PF?",
        "I'm gonna try this.",
        "I do the graston technique on my feet and calves after soaking mine in a very hot Epsom salt bath. TenJet got me to the 90% mark and this got me to the 100% mark.",
        "Epsom salt works for mine"
    ],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 6: Heel pain
status, nc = merge_post(
    "Does anyone else get sharp, horrible pain in the heel as circled in the photo? It's driving me bonkers. I only get pain in the arch of my foot when I've been on my feet too long, but my heel is another level",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- BUNION SURGERY GROUP: "is this normal" search ---
# Post 7: 6.5 weeks post op weight bearing
status, nc = merge_post(
    "I'm 6.5 weeks post op and allowed to bear weight. My foot hurts so much when I walk- top and bottom. Is this \"normal\"??",
    [
        "3 months and I still have constant burning pain",
        "All normal.",
        "Shouldn't hurt. Uncomfortable yes, but hurt not really. Please get in to physical therapy",
        "Absolutely. Things will feel weird for awhile.",
        "I'm the same as you. 6 weeks post op. Hurts top and bottom",
        "What kind surgery you had?"
    ],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 8: Stitches not removed
status, nc = merge_post(
    "I'm trying not to get upset but I'm a bit concerned. My stitches were not removed at my 2 week check up as the incision area was not healed. I was wrapped back up and am due back tomorrow for 4 week check up. I've just exposed my toes as the were feeling quite hot. I was shocked to see that I have severe athletes foot between my smaller toes. They were bound so tight the small one was tucked behind the other. I also have no feeling in my second toe! Is this normal after bunion surgery",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 9: Pin removal pain
status, nc = merge_post(
    "I had the pin removed from my second toe yesterday at 5 weeks post op. My toe hurt allllll night! Is this normal? No swelling or bleeding or anything, just pain deep down, like in the bone.",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 10: Can't bend big toe 3 months
status, nc = merge_post(
    "3 months post op and I still can't bend my big toe. I can wiggle it but it will not bend downwards Is this normal?",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 11: Walking boot pain
status, nc = merge_post(
    "Walking Boot Question. 3ish weeks post op. Yesterday I got my cast / splint off and moved to a walking boot. It's miserable! It's actually more painful than the cast was. Is this normal? I ended up taking it off because the pain was really bad and I couldn't sleep. Thanks!!",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- TOENAIL FUNGUS GROUP: "home remedy" search ---
# Post 12: Desperate for help
status, nc = merge_post(
    "Most people that post here are clearly in desperate need for help and have severe toenail fungus. They have clearly tried everything and are looking for a miracle cure, the truth is there isn't one otherwise we would all be using the same product.",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 13: 17 years fungus terbinafine
status, nc = merge_post(
    "Hi everyone, Had foot nail fungus for 17 years now. I'm pretty positive I caught it with my mom's contaminated nail polish and clippers. I wasn't aware. It started on my left big toe and then it spread like wildfire to the other. I also had AF and my feet were itchy. So never took medical care because I was ashamed. I went years without exposing my feet. I was afraid of vacations and yoga classes. Anything that involves exposing my feet. I'm 33 and I said no more to this embarrassment. I have insurance and I decided to see a good Foot and ankle doctor. She took clipping sent it to a lab and then said Terbinafine is the answer for 12 weeks.",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 14: Oral meds no side effects
status, nc = merge_post(
    "Just a note for those considering oral meds, I didn't have a single side effect taking it for 3 months and my liver wasn't affected at all, it stayed normal. My nail fungus was mild but had lasted over 7 years.",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 15: What treatment worked
status, nc = merge_post(
    "Has anyone here ever dealt with toenail nail fungus? What treatment actually worked for you?",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 16: Which home remedies worked
status, nc = merge_post(
    "Which home remedies have you tried, and did they actually work for you?",
    [
        "Vicks worked for me and many others",
        "Nonyx nail gel, dettol in your washing. Regularly filing and cleaning out nail. Epsom salts and apple cider vinegar foot soaks.",
        "I've had this going on for 5 years plus, I've tried everything and nothing worked so I hear every one talking about Vicks vapor rub and gave it a shot. U have to get rid of the nail by grinding it down or clipping it off and I use peroxide in warm water, put my feet in and soak about 10 min then put on Vicks and socks and go to bed, I can tell it's working!",
        "I was on Reddit awhile back trying to look at new ways and someone posted Betadine/iodine 10% solution. You have to cut the nails back really short and then file them until they are a bit porous and then apply twice a day for a few months maybe longer depending on level of infection.",
        "None",
        "Vinegar. 5 toes had it. It's taken Almost 2 years. 4 toes clear... big toe close. But better than anything else I've tried in 15 years including meds.. prescriptions.. Vicks... nothing else worked.",
        "I've tried so many, some worked a little, but nothing cured it until I finally just took terbinafine. I partially procrastinate because the topical version did nothing, but the oral medication worked.",
        "Vicks works if you apply a nice amount and cover it with a band-Aid."
    ],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- FOREFOOT FORUM: "podiatrist" search ---
# Post 17: When to remove tailor's bunion
status, nc = merge_post(
    "When did y'all decide it was time to remove a tailors bunion surgically? I just recently got one maybe 4 months ago, and it's progressively gotten worse. I went to a podiatrist where they did x rays and they recommended I get a sole pad, some of this arthritic cream that takes months to work, and a little toe splint thing but I can only wear it when I also have a lidocaine patch on it because it still hurts. Is it worth going through all these steps to help relieve pain or should I just go ahead and consider surgery?",
    [],
    "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 18: Wide feet pregnancy tailor's bunion
status, nc = merge_post(
    "I've always had wide feet. I could manage to squeeze into fashionable trainers etc but would rub. Anyway, I was pregnant last year and my left foot mainly just went whomp and the tailors bunion appeared! It doesn't give me pain really unless it was in a shoe. I'm basically only really able to wear crocs at this point. I'm pregnant again and worried it will get worse. I'm 31 and I feel so sad about how I can't wear all of the nice trainers and footwear others get to wear.",
    [],
    "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 19: Child with lump - tailor's bunion
status, nc = merge_post(
    "Hi members. This lump appeared on my daughter's foot (aged 11) 3 weeks ago, it's hard and very sore in shoes, could it be a Tailors Bunion?",
    [],
    "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 20: Podiatrist vs orthopedic
status, nc = merge_post(
    "Those who have had tailor's bunion surgery who did it a podiatrist do it or a foot and ankle orthopedic surgeon do it?",
    [],
    "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 21: Tailor's bunion removed yesterday
status, nc = merge_post(
    "I just had a Tailors bunion removed from my right foot yesterday. So far it's doing well. I'll let you know more after the bandages come off.",
    [],
    "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- BUNION SURGERY GROUP: "back to work" search ---
# Post 22: Nurses return to work
status, nc = merge_post(
    "Nurses: What week did you return to work?",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 23: Scheduled surgery back to work
status, nc = merge_post(
    "I'm scheduled for surgery this Saturday. I've been reading through posts to get an idea of how I'm going to feel/manage. I like to think I push pain to one side and just get on with things however I know that I'll definitely need rest and elevation. I've given myself a 2 week schedule to switch off. I'm office based and plan to go back to work, sedentary after 2 weeks. Am I being unrealistic? How was your pain in the first few days? How long until weight bearing? Did it drive you crazy doing nothing?",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 24: MIS surgery return to work
status, nc = merge_post(
    "I'm having my MIS surgery on this Friday. I'm just curious how long did you take to be able to go back to work. I'm in property management, so I can sit down as needed and, my foot is my driving foot. I'm just estimating like 3 weeks but wanted to see how it worked out for people who have already been through it.",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 25: First day back WFH
status, nc = merge_post(
    "6 weeks and 4 days PO. Just finished my first day back at work. So glad I work from home! I'm sore and it's a desk job! While I couldn't elevate toes above nose, I was able to get it up a little, and ice my foot. It's still swollen and dark almost purple. Doesn't hurt though so I'm all good.",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 26: Before and after scarf akin positive
status, nc = merge_post(
    "Before and after scarf akin in the uk. Now 5 weeks post surgery. Walking approx 6000 steps a day. Back swimming and driving and back to work in a week. I had a fantastic surgeon. Just wanted to post a little positive update to anyone in early stages as I read many negative stories before",
    [],
    "bunion surgery / foot surgery support group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- MIS BUNION GROUP: "second opinion" search ---
# Post 27: Beginning search for doctor
status, nc = merge_post(
    "Hello, I'm only beginning this search. Y'all are scaring me with all the posts of pain. Which type of doctor should I be looking for?",
    [],
    "Minimally invasive bunion surgery"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 28: Double 360 bunionplasty pain
status, nc = merge_post(
    "Well I've got my double 360 bunionplasty. First two days didn't feel a thing because of the exparel shots aka lidocaine. But now that that has worn off I'm in excruciating pain and the medicine isn't working at all. I'm afraid I may have messed something up when I was numb! Is this pain normal? Follow up on Monday. Two long days away...",
    [],
    "Minimally invasive bunion surgery"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 29: Revision surgery needed
status, nc = merge_post(
    "Hi! Had bunion surgery February 17, doctor said my big toe is tilted and wants to do surgery again next week to correct it. I don't think I want to do surgery again, can't really bend big toe and have pain on the bottom of my foot.",
    [],
    "Minimally invasive bunion surgery"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 30: Can't bend toe after MIS with pins
status, nc = merge_post(
    "So I got surgery on my right foot back in Dec 2025, I got the one where they work right on the part of the bunion with pins only no plates and I still cannot bend my big toe like with pressure or just naturally curling my toe. Is this normal will it eventually let me bend it?",
    [],
    "Minimally invasive bunion surgery"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- PF GROUP: "wide toe box" search ---
# Post 31: Narrow slipper
status, nc = merge_post(
    "Any recommendations for a narrow slipper or slide to wear in the house? I wear a sz 10.5 narrow. While I know a wider toe box is best, many slides are too wide for me in my sz- they literally fly off my feet when trying to walk. I prefer not to wear shoes or sneakers inside as it's too hot.",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 32: Which Brooks wide toe box
status, nc = merge_post(
    "Which Brooks (specifically) makes a wide toe box, without the thick cushion?",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 33: Altra Flow 2 review
status, nc = merge_post(
    "I just brought the Altra flow 2. They are very light and wide toe box. Really good in the heel. This is my first pair of this brand. Have pf for months and for the first time seeing an improvement even after first day. The only thing that was sore were my legs but it was my first day using them.",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 34: Hobibear barefoot shoes
status, nc = merge_post(
    "I just wanted to say that I completely understand that everybody's feet are different.... not everything works for everybody. But I think I have found what works for me. $39 Hobibear barefoot shoes on Amazon. Zero heel drop. Wide toe box. I'm walking without intense pain or limping. Am I healed completely? No, not yet. But this is a wonderful start.",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 35: Hike or Peak footwear
status, nc = merge_post(
    "Does anyone recommend Hike or Peak foot wear? Im looking for wide toe box, zero lift. I tried Hobibear, but not sure if I like them.",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- PF GROUP: "barefoot shoes" search ---
# Post 36: Flat feet + zero drop
status, nc = merge_post(
    "Anyone with flat feet able to wear zero drop shoes and walk barefoot? If so, any advice? Thank you",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 37: Walking barefoot on sand or grass
status, nc = merge_post(
    "Walking barefoot on sand or grass - yes or no and why? Thanks!",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 38: What to wear around the house
status, nc = merge_post(
    "Finally saw a podiatrist today and confirmed I have PF. Any suggestions on what to buy and wear around the house? She said to try and avoid walking barefoot or just in socks or flat slippers. I'm usually in socks or flat slippers but not looking to spend $160 on just shoes for the house.",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 39: Supportive vs barefoot shoes conundrum
status, nc = merge_post(
    "The supportive shoe vs barefoot shoes conundrum... I have and use both kinds, but I feel better using support because the floors I walk on all day are super hard. I have wood and slate tile floors that I'm in constant contact with, therefore I need a more supportive shoe such as an Oofos or Crocs.",
    [],
    "Plantar Fasciitis Talk and Tips Support Group"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- TOENAIL FUNGUS GROUP: "essential oil" search ---
# Post 40: 18 years fungus multiple remedies
status, nc = merge_post(
    "I've had severe toenail fungus for 18 years! I've tried everything. Finally this year, I feel like I'm seeing huge improvement. Castor oil, tea tree, tinactin cream and Jublia. Wow. Two weeks ago, rashes popped up on my groin, armpits and on my head. Great, athletes foot has spread I assume.",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 41: Oral terbinafine + Amazon products
status, nc = merge_post(
    "I'm on oral medicine terbinafine and decided to get myself some things on Amazon. Foot soak epsom salts, Listerine, Anti fungal wash, Tea tree oil",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 42: Tea tree oil experience desperate
status, nc = merge_post(
    "Looking for anyone's experience with this product or with tea tree oil for getting rid of toenail fungus. Has either product worked for you? Im desperate",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 43: Castor oil worth trying
status, nc = merge_post(
    "Castor oil, is it worth trying? If you use this, how are you applying it, and does it have to be the organic one?",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Post 44: 20 years fungus finally terbinafine
status, nc = merge_post(
    "I've battled with my toenail fungus for 20 years, trying various topical over the counter medications, curanail, scholl... they did not work. I tried soaking them in epsom salts, applying tea tree oil, which did improve them but not destroy the fungus permanently. I tried imperial feet as it was highlighted rated on amazon, that just made the nails soft to cut it back, again not killing the fungus. I then tried laser treatment, which was expensive, but came highly rated to cure toenail fungus. I had high hopes but it did not work. I finally had success in February 2025. I went to my doctors and got prescribed antifungal terbinafine tablets, 1 a day for 3 months, it's taken a few more months for the nails to fully regrow but I'm now toenail fungus free.",
    [],
    "Toenail Fungus Support & Management"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# --- FOOT PAIN COMMUNITY: Feed browsing ---
# Post 45: Bursectomy ball of foot
status, nc = merge_post(
    "Anyone had bursectomy done on ball of foot? It's been 6 months since surgery and I still cannot walk properly because of the pain. My foot seems to not tolerate load. I now got custom insoles but it's still painful when I walk a few metres at one go. Anyone gone through this?",
    [
        "Ask your pedorthist about an offload for that area.",
        "did you not get a surgery boot for after surgery?"
    ],
    "Foot Pain Community"
)
if status == 'new': new_count += 1
elif status == 'enriched': enriched_count += 1
total_new_comments += nc

# Save
with open('/tmp/fixfeetfast2/posts.json', 'w') as f:
    json.dump(existing_posts, f, indent=2)

print(f"\nResults:")
print(f"  New posts added: {new_count}")
print(f"  Existing posts enriched: {enriched_count}")
print(f"  Total new comments added: {total_new_comments}")
print(f"  Total posts now: {len(existing_posts)}")

# Topic breakdown
groups = {}
for p in existing_posts:
    g = p.get('source_group', 'unknown')
    groups[g] = groups.get(g, 0) + 1
print(f"\nBy group:")
for g, c in sorted(groups.items(), key=lambda x: -x[1]):
    print(f"  {c:4d} | {g}")

total_comments = sum(len(p.get('comments', [])) for p in existing_posts)
print(f"\nTotal comments across all posts: {total_comments}")

