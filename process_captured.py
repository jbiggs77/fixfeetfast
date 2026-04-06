import json
import re
from datetime import date

# Load existing posts
with open('posts.json') as f:
    existing_posts = json.load(f)

existing_prefixes = set()
for p in existing_posts:
    prefix = p['body'][:80].lower().strip()
    existing_prefixes.add(prefix)

max_id = max(p['id'] for p in existing_posts)
today = date.today().isoformat()

# All captured posts from Facebook scraping
new_raw_posts = [
    # === FEED POST from bunion surgery group ===
    {
        "body": "Hello. I am almost three months post op, left foot bunionectomy with a plate and six screws. The incision was very slow to heal compared with my right foot done 11 years ago. My post is regarding the spot on the top of my foot. I saw my dermatologist four weeks ago when there was still a scab there and she wanted to biopsy it. It was just too sore so she agreed to recheck it in four weeks, which was today. She really believes it is a type of trauma induced skin cancer and took a biopsy today. If it matters, I have two autoimmune disorders that I believe added to me being slow to heal. Wondering if anyone here has any experience or knowledge to share?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [{"text": "I would agree your autoimmune disorders would delay your healing. I had delayed healing and the same surgery as you. At 9 weeks I discovered I wasn't healing on the inside or the outside. Which led me to finding a wound specialist."}]
    },
    # === SWELLING SEARCH - bunion surgery group ===
    {
        "body": "16 weeks post op Austin, still have swelling and dealing with sesamoiditis. Anyone else experience this? Any tips on ways to alleviate the pain?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Is this swelling normal? 8 weeks post op (MIS akin bunionectomy). I have nothing to compare it with.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Still a lot of swelling at 5 weeks post op hammer toe and bunion surgery.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "had bunion surgery in March 5. my swelling is still up and down. I have lots of pain still and am worried about my recovery.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "For a bunion surgery - MIS BOAT (similar to Chevron), how long did it really take for most swelling to subside? I know you can have swelling up to a year and that is really scaring me at this point. I am VERY active - I workout 6 days a week doing classes (HIIT, kickboxing, step), weightlifting and cycling (in summer about 70 miles per week). I'm only 3 weeks post-op right now, but I'm worried that by 12 weeks I will get super swollen.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    # === HOKA SEARCH - bunion surgery group ===
    {
        "body": "Any ladies out there looking for sandals should check these two out, one high end price and one is low end. 1. Hoka Infini Hike TC and 2. Whitin Hiking Sandal. Both have been very comfortable since transitioning from having to wear a carbon fiber insole. They also are fully adjustable and allow for my swelling that I am still experiencing. I will try and post links in the comments.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Shoes or slippers?! I was fitted for Hoka Clifton at running shop. I wore these on Sunday, but shoes seems pretty snug on surgical foot. Foot was too swollen for any shoes my mid-morning on Monday so I bought extra large mens slippers. Should I buy a size up for my surgical foot in the Bondi's and wear two different sizes?!",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "I bought Hoka x-wide Clifton from running store after surgery. Are these wide toe box enough?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Hi all I'm 15 months post op where I had my toe fused. I have been wearing Hoka Bondi shoes since I started walking. I have recently started wearing thongs again. I'm wearing Archies thongs and not finding them good. Any recommendations on comfortable thongs would be appreciated. Or even a slide on shoe that you've found to be comfy to walk in after toe fusion.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "I think I may need to order 100 pairs of these Hoka sneakers! I feel like I'm walking on cloud without inserts and I also am able to walk without a limp like I was able to before my surgery!",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    # === HEEL SPUR SEARCH - PF Talk group ===
    {
        "body": "I've had plantar fasciitis and a heel spur for 10 months despite steroid injections, B12 injections, and shockwave therapy. I still can't go back to the gym or Zumba and it's very frustrating. Has anyone tried plantar fascia embolization or PFE?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "My PF caused a heel bone spur, any suggestions for home remedies or anything else that helps with the bone spur?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I used to have intense pain in my heels, I have very large heel spurs, I had massive amounts of tearing to my PF muscle and I had a trapped Baxtor nerve. I had surgery for a Tarsal tunnel release and partial plantar fascia release- I had both done at the same time in Nov. Ive had a major set back as my foot got infected, however day by day, its getting better, still extremely tender and only put pressure on my foot for a certain amount of time, but its so much better than before the surgery. Its a long process, but so far, its been worth it.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "So after battling with PF for the last 15 months, I finally did it! Plantar fasciotomy, heel spur removal and scar tissue removal. New foot is the best Christmas gift ever. I've tried everything from cortisone shots, dry needling, shock wave therapy, barefoot shoes, 4 months of PT, compression socks, night splints, icing, heating, massaging, orthotics, etc. Had the same surgery on my left foot 5 years ago and it was the best decision ever, no pain since.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Looking for alternatives to surgery for heel spur, if any. I've had severe pain for 5+ months. Was originally thinking it was PF, but went in for x-ray recently.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    # === CORTISONE SEARCH - PF Talk group ===
    {
        "body": "I have done 3 cortisone injections in each heel. We are now talking surgery vs shockwave therapy. The shockwave therapy they offer is $750 upfront to go once a week for 5 weeks for one foot, and they claim the treatments only take 5-10 minutes. Has anyone done the once a week for 5 weeks for the shockwave therapy? Any relief?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "When cortisone finally stopped working I went with the next best thing. Had my first shockwave treatment today. He said I will prob need 4-5 treatments. Obviously we hope this works. If it doesn't I can opt for plasma in sections or surgery. I can use my own plasma but he has much better success with immature plasma extracted from umbilical cords. One day at a time.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I received a cortisone shot this past Thursday and not seeing any results! My foot hurts so bad to walk and even burns on the back of my upper heel. Any thoughts to my next step? I've even been doing my stretches.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I got Cortisone shot on both feet and the steroid pills what supplements should I seek? And be asking for to strengthen and supplement the Fascia?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Ok, well, so much for the cortisone treatment. It worked amazingly well until it didn't and now I'm in more pain. My only relief from the pain was walking in my floopi thongs as they are super cushioned. That's no longer a relief and I'm even limping in those. Back to square one. I have an appt with podiatrist next week. Let's see what he has up his sleeve next.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    # === TERBINAFINE SEARCH - Toenail Fungus group ===
    {
        "body": "Hi all. I was prescribed Terbinafine after other home treatments were unsuccessful. After a few days of treatment My throat became sore, not realising it could possibly be the Terbinafine I took some antihistamines thinking it may have been after cutting my grass for the first time this year. During the 3rd week on Terbinafine I developed ulcers on my tongue, throat and what felt in my upper lungs felt inflamed, like a burning sensation.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Does this look like new, clean growth? I've been on ciclopirox lacquer for almost 4 months. I was also on terbinafine but had to stop that a month in due to an allergic reaction. I THINK this is clean outgrowth but I don't want to get my hopes up. Out of the 4 that are infected, this is the only one showing improvement.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Would applying Terbinafine cream be any good, as well as taking the oral medication?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "So I've been on oral terbinafine for a bit over a month (no side effects, I was nervous). My big toenails are just slightly yellow at the tips in the corners but I've had the infection for a long time, I just use lots of topicals to keep it at bay. So they aren't a very extreme case. I want to try for a last baby once I'm done with the three month course of medicine, which means I really need to make sure the medicine works.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "After dealing with fungus for nearly two decades and trying almost every remedy, I had a podiatrist finally talk me into taking oral medication - Terbinafine. The left is from April 8th and the right is from today! I didn't have any side effects but I also don't drink coffee or alcohol. We checked my liver in the beginning, then halfway which showed elevated numbers. She had me stop for a month, then retest my liver, which was normal again, and I finished the course.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    # === TEA TREE OIL SEARCH - Toenail Fungus group ===
    {
        "body": "I'm on oral medicine terbinafine and decided to get myself some things on Amazon. Foot soak epsom salts, Listerine, Anti fungal wash, Tea tree oil.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "After trying iodine, tea tree oil, niacinamide, Vicks vapor rub, cloves, peroxide, vinegar, OTC creams and nail repair, emuaidMax metallic silver, Listerine... I found a cure on accident.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "I give up. I'm just going to use nail polish with tea tree oil in it. I've been using prescription and also over the counter treatments for over a year. No help. I can't afford to go have all my nails lasered.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "I've battled with my toenail fungus for 20 years, trying various topical over the counter medications, curanail, scholl... they did not work. I tried soaking them in epsom salts, applying tea tree oil, which did improve them but not destroy the fungus permanently. I tried imperial feet as it was highlighted rated on amazon, that just made the nails soft to cut it back, again not killing the fungus. I then tried laser treatment, which was expensive, but came highly rated to cure toenail fungus. I had high hopes but it did not work. I finally had success in February 2025. I went to my doctors and got prescribed antifungal terbinafine tablets, 1 a day for 3 months, it's taken a few more months for the nails to fully regrow but I'm now toenail fungus free.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    # === NIGHT SPLINT SEARCH - PF Talk group ===
    {
        "body": "I have had heel spurs with plantar fasciitis under both feet for 20 months now. I have tried a night splint, 8 shockwave treatments, 5 osteopath visits, orthopedic insoles, stretching and strengthening exercises (including with a ball), cooling, and massage devices. Nothing helps; I am at my wit's end. Do you have any tips? Or good stories, because I am afraid this will never go away. I am a young woman of 29.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "is night splint a big help for you guys? planning to buy those",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "While a night splint does seem to help, it's bulky and uncomfortable. My sheets are loose, but my feet are pointed down while I sleep and that seems to aggravate BOTH calves. Are y'all using anything while you sleep that keeps your feet more towards 90 degrees?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "My PT recommended a night splint sock but I couldn't find one that would fit me.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I've already try this Night Splint Foot but nothing is happen. My Plantar Fasciitis is still more pain. What can I do?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    # === TOE SPACER SEARCH - Bunion Support Group ===
    {
        "body": "Recently I noticed big toes were leading to second toes, it was more obvious for left toe. Sometimes I feel needles on the big toes. So I went to see a GP. He said he wouldn't refer me to specialist unless I have eg hammer toes or deformed bones, and also my needle sensation is not happening all the time. He only asked me to continue wearing toe spacers and do a blood test. Now I feel helpless coz it seems he can't refer me to a foot doctor yet. Was this also how your GP advise you?",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    {
        "body": "With the discomfort of toes touching one another, anyone is able to wear toe spacer the whole day when moving about?",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    {
        "body": "I got wide toe box sneakers. Does anyone have suggestions for comfortable toe separators or toe socks I can wear with them? I wear the pictured separator socks to bed. I know I can't correct my bunions these ways, but I'm hoping to stop the progression.",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    {
        "body": "Has anyone in the U.K. found toe spacers that can be used all the time comfortably? I splashed out on correct toes and they have damaged the skin and were very painful to walk in. (Rubbing the skin). I'm athletic and want to run in spacers.",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    {
        "body": "My foot is still slightly swollen but I'm noticing my second toe slightly shifts left touching my big toe. My doctor said the big toe is straight but I'm annoyed how close together my toes still are. What do y'all think? Am I overreacting? I'm happy I'm not in pain as I was in so much pain prior to surgery but I think now I'm obsessed with how it looks. I have been wearing a spacer and still do 24/7.",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    # === ARCH SUPPORT SEARCH - PF Talk group ===
    {
        "body": "I tried on some oofoo flip flops today, but the arch support was more towards the front of my foot. I need an arch support that goes a little more towards the heel. Anyone have any other recommendations?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Low profile sneakers with arch support? I hate the look of big bulky sneakers. Are there any sneakers out there with good arch support that are lower profile style?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Has any tried the vionic shoes? Supposed to be comparable to expensive arch support.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "If you don't want to buy different insoles for the shoes you already have, I've used these arch support pads and they are not expense so you're not spending a lot of money. You can find them almost anywhere - Walgreens, Walmart.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Where I bought my shoes - Archies Footwear - Arch Support Flip Flops and Footwear.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    # === FOREFOOT FORUM - plantar plate / toe exercises ===
    {
        "body": "Has anyone ever been advised to use a Pointer Plus acu-point to manage symptoms? I have a rigid big toe, which is likely the cause of my symptoms (metatarsalgia and sesamoiditis...still trying to diagnose). My osteopath suggested this device so I could try to manage on my own rather than paying $190 to see him every couple of weeks. He also showed me how to manipulate my big toe to keep it from getting locked up.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": []
    },
    {
        "body": "My 2nd toe is starting to push against my big toe. It's becoming a problem, and I'm looking for a way to stop it before it gets worse. My mom's eventually crossed over. I'm trying the velcro straps that tie it to the 3rd toe. And the soft bumper between it and the big toe. That works pretty well, and is more comfortable, but is bulky in shoes. Is there a fix?",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": []
    },
    {
        "body": "Hi everyone. Former athlete here. At the age of 20, I started experiencing pain in my right big toe, and around the same time I developed chronic muscle tightness in my calves. Over the years, this tightness gradually spread to my thighs, glutes, and lower back. The pain in my big toe and the muscle symptoms occur only during walking or running, not at rest. After an MRI evaluation, it was found that I have very advanced cartilage degeneration (hallux rigidus) in my right big toe joint, while my left foot shows no structural issues at all. After many years of conservative treatments, I'm now considering first MTP joint fusion surgery, together with proper gait rehabilitation.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": []
    },
    {
        "body": "Hey everyone, need some advice, I suffer from gout and plantar fasciitis, but recently I've suffered a kind of injury on the side of my foot on the pinky toe joint. I initially thought it might be gout, but it doesn't throb at night or anything, so now I think it might be a bunionette aka Tailor's bunion. Does anyone have any experience with this? I've had it near constantly for months, and seems to swell up once a week or so.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": []
    },
    # === MIS RECOVERY SEARCH - MIS bunion group ===
    {
        "body": "Surgery day! Amazing experience with HSSH today In London. Sedation and nerve block for bilateral bunionectomy.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    {
        "body": "Op booked for May 18th, feeling worried. The surgeon has a good name for competence and great results, but he made it all sound so simple, including the recovery. Scheduled for two osteotomies, bunion and second metatarsal with pins and loosening tendon on second toe. Will I have a floppy toe?! He said procedure with nerve block, immediate weight bearing, minimally invasive, three small incisions, I will walk out.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    {
        "body": "I am 6 weeks post op from MIS on left foot. No pins or screws. Cleared to get into regular shoes and cleared for most types of exercise. First 4 weeks I was in a boot, then went to oversized shoes wearing a brace on the toe to keep it in line for 2 weeks. Very little swelling, minimal pain. All recoveries are different but that's my story.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    {
        "body": "Just thought I'd post these. I'm 8 weeks post and the post surgery X-ray is at 4 weeks PO. The recovery was long but omg the difference is incredible.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    {
        "body": "Had my double bunion surgery yesterday (NYC), so glad I finally got it done and now the healing can begin. The nerve block is slowly going away and I try to ice and elevate as much as possible. They put me in surgical shoes and I can walk short distances, but should stay off my feet as much as possible for the first 2 weeks. But great experience all around with the surgeon and his team.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    # === HAMMER TOE SEARCH - bunion surgery group ===
    {
        "body": "Can anyone tell me if my hammer toe will be floppy after the tendon is released?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "15 days Post op with bunion and hammer toe surgery, these stitches were removed.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Hello I had a surgery for bunion, bunionette, and hammertoe almost 16 months ago; yet my 2nd and 3rd toe are still swollen (especially my 2nd toe). I'm sure swelling should've been gone now. Is this extra scar tissue? How can I treat this?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "I had the lapiplasty surgery, and hammer toe repair too.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "I had bunion and hammertoe surgery 3 years ago. Had issues with recovery due to having a reaction to hardware so it was all taken out. Now I'm having an issue with the toe that had the hammer toe surgery. Where the joint is fused, the toe shoots off to the right and on the left-hand side there's a bone sticking out. Does this mean that this is a failed fusion? It's progressively gotten worse over the last several months.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
]

# Detection lists
CONDITIONS = ['bunion', 'hammer toe', 'hammertoe', 'hallux valgus', 'hallux limitus', 'hallux rigidus', "tailor's bunion", 'bunionette', 'plantar fasciitis', 'heel spur', 'flat feet', 'toenail fungus', 'ingrown toenail', 'metatarsalgia', 'neuroma', 'sesamoiditis', 'gout', 'arthritis', 'bone spur', 'callus', 'corn', 'blister', 'neuropathy', 'edema', 'tendonitis', 'plantar plate tear']
SURGERY_TYPES = ['MIS', 'minimally invasive', 'Lapiplasty', 'scarf akin', 'osteotomy', 'chevron', 'Austin', 'arthroplasty', 'arthrodesis', 'bunionectomy', 'toe fusion', 'MICA', 'percutaneous', 'cheilectomy']
PRODUCTS = ['Hoka', 'Orthofeet', 'New Balance', 'Skechers', 'Brooks', 'Nike', 'Asics', 'Birkenstock', 'Vionic', 'Oofos', 'Crocs', 'Correct Toes', 'Yoga Toes', 'Mind Bodhi', "Dr. Scholl's", 'Superfeet', 'Powerstep', 'KT Tape', 'Voltaren', 'Biofreeze', 'Theragun', 'ERGOfoot', 'Betadine', 'Vicks', 'Lamisil', 'Jublia', 'Kerasal', 'FungiNail']
TREATMENTS = ['surgery', 'physical therapy', 'cortisone', 'steroid injection', 'orthotics', 'taping', 'icing', 'elevation', 'stretching', 'massage', 'acupuncture', 'shockwave therapy', 'laser therapy', 'MLS laser', 'anti-inflammatory', 'ibuprofen', 'gabapentin', 'custom orthotics', 'terbinafine', 'tea tree oil', 'night splint', 'rolling', 'arch support']

def detect(text, items):
    found = []
    text_lower = text.lower()
    for item in items:
        if item.lower() in text_lower:
            found.append(item)
    return ', '.join(found) if found else ''

# Deduplicate and add new posts
new_count = 0
for raw in new_raw_posts:
    prefix = raw['body'][:80].lower().strip()
    if prefix in existing_prefixes:
        continue

    existing_prefixes.add(prefix)
    max_id += 1
    new_count += 1

    post = {
        "id": max_id,
        "body": raw['body'],
        "author": None,
        "url": None,
        "source_group": raw['source_group'],
        "date_captured": today,
        "conditions_mentioned": detect(raw['body'], CONDITIONS),
        "surgery_types_mentioned": detect(raw['body'], SURGERY_TYPES),
        "treatments_mentioned": detect(raw['body'], TREATMENTS),
        "products_mentioned": detect(raw['body'], PRODUCTS),
        "comments": raw.get('comments', []),
        "images": []
    }
    existing_posts.append(post)

# Save
with open('posts.json', 'w') as f:
    json.dump(existing_posts, f, indent=2)

print(f"New posts added: {new_count}")
print(f"Total posts now: {len(existing_posts)}")
print(f"Duplicates skipped: {len(new_raw_posts) - new_count}")
