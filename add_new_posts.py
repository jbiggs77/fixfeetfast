import json

# Load existing posts
with open('posts.json', 'r') as f:
    existing = json.load(f)

print(f"Existing posts: {len(existing)}")
max_id = max(p['id'] for p in existing)

# Build dedup set from first 80 chars lowercased stripped
existing_keys = set()
for p in existing:
    key = p['body'][:80].lower().strip()
    existing_keys.add(key)

# All conditions to detect
CONDITIONS = {
    'bunion': ['bunion'],
    'hammer toe': ['hammer toe', 'hammertoe'],
    'hallux valgus': ['hallux valgus'],
    'hallux limitus': ['hallux limitus'],
    'hallux rigidus': ['hallux rigidus'],
    "tailor's bunion": ["tailor's bunion", 'bunionette', 'tailors bunion'],
    'plantar fasciitis': ['plantar fasciitis', 'plantar fascitis', 'pf pain'],
    'heel spur': ['heel spur', 'heal spur'],
    'flat feet': ['flat feet', 'fallen arch'],
    'toenail fungus': ['toenail fungus', 'fungal nail', 'nail fungus'],
    'ingrown toenail': ['ingrown toenail', 'ingrown nail'],
    'metatarsalgia': ['metatarsalgia', 'metatarsal pain'],
    'neuroma': ['neuroma', "morton's neuroma"],
    'sesamoiditis': ['sesamoiditis', 'sesamoid'],
    'gout': ['gout'],
    'arthritis': ['arthritis'],
    'bone spur': ['bone spur'],
    'neuropathy': ['neuropathy', 'nerve pain'],
    'tendonitis': ['tendonitis', 'tendinitis'],
}

SURGERY_TYPES = {
    'MIS': ['mis ', 'minimally invasive'],
    'Lapiplasty': ['lapiplasty', 'lapidus'],
    'scarf akin': ['scarf', 'akin osteotomy'],
    'osteotomy': ['osteotomy'],
    'bunionectomy': ['bunionectomy'],
    'toe fusion': ['toe fusion', 'mtp fusion', 'joint fusion'],
    'arthroplasty': ['arthroplasty'],
    'arthrodesis': ['arthrodesis'],
    'cheilectomy': ['cheilectomy'],
    'MICA': ['mica'],
}

PRODUCTS = {
    'Hoka': ['hoka'],
    'Brooks': ['brooks'],
    'Oofos': ['oofos'],
    'Crocs': ['crocs'],
    'Birkenstock': ['birkenstock'],
    'New Balance': ['new balance'],
    'Skechers': ['skechers'],
    'Nike': ['nike'],
    'Orthofeet': ['orthofeet'],
    'Vicks': ['vicks'],
    'Lamisil': ['lamisil'],
    'Jublia': ['jublia'],
    'Correct Toes': ['correct toes'],
    "Dr. Scholl's": ["dr. scholl"],
    'Superfeet': ['superfeet'],
    'Powerstep': ['powerstep'],
    'Voltaren': ['voltaren'],
    'Biofreeze': ['biofreeze'],
    'Theragun': ['theragun'],
    'Betadine': ['betadine'],
    'Kerasal': ['kerasal'],
    'KT Tape': ['kt tape'],
}

TREATMENTS = {
    'surgery': ['surgery', 'operation', 'procedure'],
    'physical therapy': ['physical therapy', ' pt '],
    'cortisone': ['cortisone', 'steroid injection', 'cortizone'],
    'orthotics': ['orthotic', 'insole', 'arch support'],
    'taping': ['taping'],
    'icing': ['icing', 'ice pack', 'icepack'],
    'elevation': ['elevat'],
    'stretching': ['stretch'],
    'massage': ['massage'],
    'shockwave therapy': ['shockwave', 'softwave'],
    'laser therapy': ['laser'],
    'anti-inflammatory': ['anti-inflammatory', 'ibuprofen', 'advil'],
    'terbinafine': ['terbinafine'],
    'tea tree oil': ['tea tree'],
    'night splint': ['night splint'],
    'custom orthotics': ['custom orthotic'],
    'acupuncture': ['acupuncture'],
}

def detect(text, mapping):
    text_lower = text.lower()
    found = []
    for name, keywords in mapping.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(name)
                break
    return found

# New posts captured from Facebook
new_raw_posts = [
    # === BUNION SURGERY GROUP - Feed ===
    {
        "body": "Having this surgery is 100% an exhausting recovering and then all of the sudden one day it gets better. I'm 6 months out and zero pain, totally happy with the results and I could care less that I have a scar. It's way better than having my bunion. Also, I deliver mail - im on my feet for long hours every day and I still have zero pain. BUT one thing I do want to mention to this group is I have Federal Blue Cross Blue Shield. I usually have $300-500 copays for surgeries (like when I had my hysterectomy). For this surgery I have a $5000 copay!!!! Why? Because for implants I have a 30% deductible. I never knew, never had an implant before - my point is, some hospitals will let u know your costs up front. Mine did not. I just assumed it would be my typical copay. I definitely was not expecting a titanium bolt to cost my insurance $40,000 and my copay to be $5,000. It would have been more but I met my out of pocket max for the year. So, I healed great from my foot surgery and extremely happy with everything except for my huge bill.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": ["How long till you were pain free I am 12 weeks and walking in shoe shoes my foot hurts on the inside and arch I have supports the doc gave me but the more I walk the worse it gets. I keep seeing that one day I will turn a corner but hopping it is soon.", "Wow that's crazy. Insurance is ridiculous sometimes. Mine has a clause that out patient surgery regardless of implants is covered 100% I just had to pay the Dr copay of 20% billed charges. Max out of pocket is $1000."]
    },
    # === LAPIPLASTY RECOVERY SEARCH ===
    {
        "body": "Had my one week follow up today! The left is the x-ray of my foot before the surgery and the right is the x-ray of it after! My surgery was on 2/23/26. I had lapiplasty, with a donor bone graft. So far recovery is going better than I anticipated. The nerve block wore off the day after surgery and the pain was horrible. Before it wore off, I felt no pain at all. I am taking journavx, hydrocodone/acetaminophen for pain. I started the journavx the day of my surgery, but held off on the hydrocodone/acetaminophen until the pain started. Once the pain started, the hydrocodone was able to significantly reduce it. My doctor gave me the go ahead to take two of the hydrocodone at first, since the one I took wasn't helping. He also said I could take it every 4 hours, instead of 6. This was absolutely needed for the first few days, as the pain would start coming back badly after 4 hours. I have began weaning off of the hydrocodone, while continuing the journavx and acetaminophen. I am getting to where the pain isn't returning as quickly/badly. It has been 9 hours since I last took hydrocodone, and it still isn't hurting me! I had the splint removed today, and was given a boot to wear! So now I'm able to wear my foot icepack, which feels soooo good! I'm also working on moving my ankle and toes up and down. I'm continuing to elevate my foot as much as possible, and using a knee scooter to get around. I also have knee pads that I wear that help when I have to get down on the ground with my son. Hoping for fast healing and progress!",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Has anyone had Lapiplasty without fusion? My doctor offered this option because I'm worried about toe mobility after surgery and the long recovery time. He said it's possible, but it would require a larger incision and more stitches since he needs better visibility of the area during the procedure.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Hi, my daughter (almost 15) had lapiplasty on Friday. One of the best and most experienced podiatrists in New England. He said everything went well, no issues. But When Block wore off on Saturday the pain got worse and worse until it was Unbearable. Pain meds were completely ineffective. We went to ER and were admitted to pediatrics. Morphine drip, loosening of bandaging and she's now back to Tylenol, advil & oxy rotation and her pain is down from 10 to 2. We were under the impression that this was the least invasive & painful, and most effective long term solution but now I'm having regrets and worried about all of the horror stories I'm reading about. Seems like 90% of the people who have reported their experiences have regrets, long and painful recovery full of setbacks. She's supposed to go back to school in a boot on Dec 2 but from what I've read, that seems far fetched. Did we make a mistake? I feel like we should have left well enough alone. UPDATE: Monday 11/24 She's feeling much better after 24 hours in the hospital which included a morphine drip and cuts in the bandage to loosen certain areas that were too tight. That got pain under control. We met with the surgeon this morning and he did a bandage re-wrap with light pressure and said everything looked as it should. Her pain now is minimal, she hasn't even mentioned it all day & she took her first shower since Thursday. We're much more hopeful and optimistic than we were when I posted this.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Had my lapiplasty at 1:30 today. Any recovery tips?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    # === HALLUX RIGIDUS SEARCH ===
    {
        "body": "Has Anyone had a hemi implant? The doctor wants to put one in my big toe. I'm scared. The big toe hurts and I guess because of the pain I'm transferring my weight to the metatarsal area which is actually where most of my pain is. The 2nd metatarsal. I want to be able to bend my toe, but I have a lot of arthritis in the toe. Will they clean it out?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Hi everyone. I joined this group a couple of weeks ago because I was convinced I had a bunion. I saw the podiatrist today and it turns out I have bad arthritis in my big toe - hallux rigidus. She said I could be conservative and wear a certain kind of shoe or she could shave the bone down. I was told I would be able to drive in 2 weeks. I'm pretty sick of the big bump on the top of my foot and my foot swelling everytime I wear an enclosed shoe.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "I had a first MTP (metatarsophalangeal) joint fusion to permanently join the bones of the big toe, typically for severe arthritis (hallux rigidus) or sometimes severe bunions on Dec 19 still on scooter and boot no weight. This recovery is far worse than rotator cuff surgery i had 10 years ago. Is it because i'm older (70).",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "I've been diagnosed with Hallux Rigidus in my right big toe, and while I'm no foot doctor, it sure seems like minimally invasive surgery would be the better route, but I can't seem to find anyone in the Southeast who actually does these regularly. Any ideas would be greatly appreciated!",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Apparently, I have a few things going on here: 1. Bunion - had it for years but became more pronounced this year where you can see it poking out a little in my Hoka's. 2. Hallux Limitus- stiff big toe & starting to lean inward. 3. Lateral deviation of the sesamoid bone positioning. X-ray showed the one was on the right of my big toe metatarsal instead of underneath it where it should be. I believe this is what's causing me the most pain walking. I've been having trouble walking correctly where I can't push off the ball of my foot and put pressure on my toes and noticing my walking stance is now leaning towards the outside of my right foot. Noticing pain in my hips and lower back too, so I think this could be a domino effect. I've been limited to only wearing my Hoka's even to work bc other shoes just hurt. Upon the doctor telling me I could get a Cortizone shot there's really nothing else I can do because I have orthotics already, I brought up surgery (she did not) & she said she can fix this with surgery. My gut is telling me to go for it now that my deductible has been met and get it over with, but not sure if I need to research this doctor more and even how to do that. I like her but she's no frills, gets you in & out, and her last Google reviews are from 2017 and prior. Any advice is welcome. Should I bother getting a second opinion?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    # === PF GROUP - Recovery Stretching ===
    {
        "body": "I'd like to share a couple things I do that have helped my pain go from a 4 to a 1, on a scale of 1-5. I'm sure they're unconventional, but they've worked for me. I was dx'd with PF on 1/27 by a podiatrist. She gave me some stretches to do and sent me on my way with an appointment in 4 weeks if the pain hadn't been reduced by 50%. I canceled my appointment. I started with the daily stretching, then added a balance board after doing research online.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I AM BEYOND GRATEFUL!!! MY GOAL FOR THE PAST 3 YEARS WAS TO WAKE UP AND FORGET I HAD FEET AND THEY WOULD DO THEIR JOB WITHOUT PAIN...THIS IS WHAT WORKED FOR ME. I started this journey (from HELL) almost 3 years ago-I am 56 years old and was very active when I got PF.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    # === TOENAIL FUNGUS - Terbinafine ===
    {
        "body": "Hi all. I was prescribed Terbinafine after other home treatments were unsuccessful. After a few days of treatment My throat became sore, not realising it could possibly be the Terbinafine I took some antihistamines thinking it may have been after cutting my grass for the first time this year.. during the 3rd week on Terbinafine I developed ulcers on my tongue, throat and what felt in my upper lungs felt inflamed, like a burning sensation.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "So I've been on oral terbinafine for a bit over a month (no side effects, I was nervous). My big toenails are just slightly yellow at the tips in the corners but I've had the infection for a long time, I just use lots of topicals to keep it at bay. So they aren't a very extreme case. I want to try for a last baby once I'm done with the three month course of medicine, which means I really need to make sure the medicine works.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Would applying Terbinafine cream be any good, as well as taking the oral medication?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Fellow sufferers! I have a plan. The problem is getting the medication to the fungus. So - I've bought an inexpensive nail drill and filed my nails down as much as I dare (although I might get braver). I crushed up 2 terbinafine tablets & put them into an old over-the-counter nail treatment bottle that I had in the house, with water. My nails look better already. Wish me luck!",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Has anyone had a severe reaction to terbinafine?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "I was on Terbinafine for 7 months last year and my toenails cleared up beautifully. After stopping meds it rapidly came back. Now back on around 2 of Terbinafine since 3 months: no difference or improvement at all.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    # === FOREFOOT FORUM - Hammer Toe ===
    {
        "body": "Surgery on rt foot for Tailor's bunion and hammer toe (4th) on Tuesday. Nervous but excited to FINALLY deal with this after a lifetime of pain that has gotten worse in recent years.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": []
    },
    {
        "body": "I'm 14 weeks post op bunionectomy, hammer toe. I'm still having difficulty walking without a walker or cane, but yesterday I walked much more than usual and today my foot is painful and swollen more than usual. I also put a very uncomfortable ice pack on my foot yesterday and feel I applied it too tight so maybe it's that causing pain. Anyone have these issues.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": []
    },
    {
        "body": "Has anyone heard of a dr fixing a hammer toe in the office?",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": []
    },
    {
        "body": "Hello! I'm trying to decide between surgical options or no surgery. I'm 57 years old and have lots of travel and other plans for being active. Problem: painful toes (15+ years) and metatarsal ball of foot (since last fall). Cause of pain: 1) toes stepping on the bottoms of their neighboring toes causing painful sores and 2) prominent metatarsals taking too much impact, leading to stress fractures.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": []
    },
    # === PF GROUP - Night Splint ===
    {
        "body": "I've already try this Night Splint Foot but nothing is happen. My Plantar Fasciitis is still more pain. What can I do?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Tonight will be the 3rd night using this splint. So far it's been a game changer for relieving those excruciating first morning steps. Still have a bit of pain but I was pleasantly surprised when I didn't have to hold on to the wall or furniture to get to the bathroom. Wasn't even limping.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I was very bad for 2 years, using the night splint I immediately recovered! I'm doing now this exercises daily.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Plantar Fasciitis sufferer here! It was recommended I get a night splint. I ordered one but it doesn't work as intended. Can anyone recommend a night brace that worked for them?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Has anyone tried acupuncture or night splints for pf pain. I've just bought some arch support shoes from amazon so hope they also help.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    # === TOENAIL FUNGUS - Tea Tree / Vicks ===
    {
        "body": "I'm not sure what's more annoying......when someone says Try Vicks or when someone says I bathe my feet 3 times a day and use an electric nail file each week I also buy anti fungal washing powder and wash all my socks and towels separately, and change the bed sheets every night. Every morning and night I put tea tree oil on my toes mixed with antifungal cream, then apply vicks on top and hold it down with a plaster and wear cotton socks.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "My nail finally fell (almost completely) off. What should I use on the nail bed so the fungus wont come back? I have some Ciclopirox solution but should I try Vicks or tea tree oil instead? Or just leave it?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "After trying iodine, tea tree oil, niacinamide, Vicks vapor rub, cloves, peroxide, vinegar, OTC creams/nail repair, emuaidMax (metallic silver), Listerine... I found a cure on accident.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Has Vicks worked for anyone?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "I've read that Teatree oil and Vicks is good for toenail fungus. How about if I open a capsule of liposomal vitamin C and add a drop of Teatree oil?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    # === CORTISONE INJECTION SEARCH ===
    {
        "body": "I had MIS surgery 2 years ago and I still have nerve pain. My doctor suggested a cortisone injection but I'm reluctant to do that. I've had them in my knees and ankle with little to no improvement. The slightest pressure is painful. Thoughts? Thanks.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Update from X-ray: Severe pain and swelling bunion 2nd, 3rd, 4th hammertoe deformities. Off for a cortisone injection tomorrow, and then the waiting game on when I'll get an appointment at the hospital for surgery.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Ok, I'm new here in SC. I've been living off of cortisone shots in my feet every 4 yrs. I have had 2 foot surgeries in the past for heal spurs, and a damaged nerve back when I was 30. I'm 53 now and bunions are my problem. I also have a fracture on the knuckle under my big toenail on my left foot. The left foot bunion with that fracture hurts beyond explaining. The tailor bunion on my right foot hurts beyond explaining. I am a waitress. The shots usually last 4 years and I do not want another surgery.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "I've had multiple surgeries on my left foot, a bunionectomy, 1st MTP fusion and sesamoid removal. I don't have much fat padding on the bottom of my foot. I saw a podiatrist who wants to give me a cortisone injection since I'm still having pain on the ball of my foot. I'm leery to get a cortisone shot since I don't have much padding now, does anyone have any recommendations?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Hi I'm having a steroid cortisone injection tomorrow on my 2nd TMTJ due to pain caused by arthritis. Surgeon not interested in touching the bunion yet. He said if the injection doesn't work he would consider a two procedures in one operation - fusion of TMTJ and bunion removal at same time. Has anyone else been treated like this - I'm NHS UK patient? Seems to me like they're addressing the symptom and not the cause.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    # === HOKA SHOES - Bunion Support Group ===
    {
        "body": "What are your thoughts? Haven't had surgery just yet as it's my last option. Went to physical therapy and therapist recommended the HOKA shoes and Bunion Relief & Toe Corrector. What are your thoughts? I really don't want to have to get surgery.",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    {
        "body": "Hi there, which of the following trainer brands are recommended for good support for arches, bunions, and various tendinitis of the foot? Birkenstocks, On, Hoka, Alta?",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    {
        "body": "Hi Guys, which HOKA trainers do you recommend? I havent had surgery yet but have been refered. I need some trainers for the coming cold season.",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    {
        "body": "New journey for me. This group has been so helpful with finding new shoes. Brooks Ghost 16 wide and Oofos slides are working out great. I am still trying to decide if I like the Hoka Bondi variety. The orthotic insole project has been interesting too. I am now on a quest for dressy sandals and low heels for work meetings and upcoming holiday gatherings. I have a high arch, so good support is much needed. Any suggestions would be appreciated. Thank you!",
        "source_group": "Bunion Support Group",
        "comments": []
    },
    # === SHOCKWAVE THERAPY - PF Group ===
    {
        "body": "For people who have tried softwave/shockwave therapy for plantar fasciitis how many treatments did you do?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Advice needed. I had shockwave treatment last week and everything was fine. I was actually starting to feel better! I had my second treatment this Thursday and it hurt more during treatment and now my calf muscle is so tight I can barely walk. Is this the norm? I've tried the massage gun to make it less tight but so far it's not worked. Now dreading next week's treatment!",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Question for the group: I've been wanting to try shockwave therapy and understand it gets expensive. I am therefore considering buying my own machine. Has anyone made the switch from clinic treatments to a home device? I'm curious if the home version is powerful enough to actually work. Any brand recommendations?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Has anyone used Shockwave therapy?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I am undergoing shockwave therapy, and it has been painful for me. After the third session, I had to go out for three consecutive days, and I experienced pain in my leg. One of those days, I wore a compression sock that I had just bought, but it turned out to be tighter than needed, which caused congestion and increased pain. My doctor prescribed anti-inflammatory medications. Is what happened concerning? And should I stop the shockwave therapy sessions?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    # === MIS BUNION - Swelling Recovery ===
    {
        "body": "I'm 4 and a half months into my surgery, and my foot is still super sensitive even when I take a shower and the water hits my foot. Is this normal? I have my husband run my foot to try and stop it from freaking out but I haven't been able to take my ace bandage off when it's in a shoe.. swelling still comes and goes especially with the heat I try icing behind the knee I try keeping myself cool, but it swells to an uncomfortable level.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    {
        "body": "I had surgery on January 9th. MIS and hammertoe correction. My outside ankle really is swollen and hurting a lot. Has anyone else noticed this at all?",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    {
        "body": "UK here. 3rd week post double foot op. You all seem to know what was done to your feet. I am waiting until 6 week check to hear what actually happened in the surgery. Have to say as a person who has had many operations this operation has thrown me. Patience is needed. Question. My big toe sticks up like a thumb, still very swollen and it feels like I can feel the screws. I was told to wait for the swelling to go down. Struggle to sleep as it's very uncomfortable and annoying. Maybe it's just the swelling. It's on the ball of the foot under the big toe. Anyone else feel this sensation?",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    {
        "body": "Thanks for the add! Here are pics of my progress so far. Pics of hardware before and after and 2 week and 4 week progress. How long do you feel the stiffness inside your foot? My dr said to expect swelling for up to 6 months.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    {
        "body": "Okay I'm on here a lot but I've never had this type of surgery I am having issues with the swelling. It has gone down because I can tell you exactly where my screws are because it hurts a bit when something touches it and it's still swollen there. Should I be worried? It isn't horrid pain feels like a pinch then after awhile it goes away. Its a little shiny but it's like I am starting to get feeling back in my foot and it freaks me out.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": []
    },
    # === SCARF AKIN SEARCH ===
    {
        "body": "Finally scheduled surgery for my r-foot at my appt this morning. It's scheduled for June 3rd! It'll be with the same podiatrist from last year! Procedure will be Scarf Bunionectomy w/Reese OR Akin Osteotomy, nerve block injection and w/MAC anesthesia. Looking forward to a successful procedure, zero complications, an uneventful yet positive recovery journey, pt and no longer suffering from bunion pain.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Hi all, I hope you are doing well. 8 months PO. My issues were: hallux valgus deformity, Hammering of the lesser toes, bunionette deformities and gastroc-soleus equinus. No TMJ joint hypermobility.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "My surgery is 12/26, and I am terrified. I am having nightmares and waking up way too early with anxiety over it. My procedures are: Right foot: 1. Lapidus bunionectomy. 2. Akin osteotomy. 3. Tailor's bunionectomy. This is what my foot currently looks like. The surgeon said he will take a wedge out of my big toe to align it. Will this make my second toe in next to my big toe significantly longer than my big toe with a wedge missing? I was excited for it to be straighter.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "For those who had right foot lapidus akin bunionectomy, when did you start driving again?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    {
        "body": "Has this happened to anyone...I had SCARF and Akin osteotomy end of July and I still have been having pain and swelling of that foot. 6-weeks post x-ray showed non-union of the Akin osteotomy and seem like it's still non-union to this day. Found out I'm 7 weeks pregnant and during my last appointment, my surgeon does not want to do anything for now and maybe wait next year after I have given birth for the hardware removal.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": []
    },
    # === TOENAIL FUNGUS - Laser ===
    {
        "body": "I'm seeing a podiatrist in a few weeks who has a foot aesthetics practice. From what I can tell from reviews, her patients have had success with laser. All of my online research looks like lasers for fungus are 50/50. Anyone here had any luck with lasers? Two rounds of terbinafine did nothing for me.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Has anyone tried laser treatment? If so, what was your outcome?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "How much does laser treatment cost and how many times do you need for moderate to severe infection basically on all toes?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Has anyone had success with professional Lazer treatment and ointment?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    {
        "body": "Has anyone had success with lasers? If so what type of laser, how often did you have to do it, and how long did it take to see results?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": []
    },
    # === PF GROUP - Hoka/Shoes ===
    {
        "body": "Which shoe works best for you? I've tried Hoka & Brooks and both sent me into a flair up. My crocs are literally the only thing I can tolerate right now.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Which Hoka shoe is best?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I need suggestions on winter boots! I currently wear my hoka recovery slides indoors and my brooks glycerin shoes outdoors but I live in Canada and my feet are cold and wet. I am looking for suggestions on SHORT winter boots that will provide the same amount of support as my current shoes. I will add here that orthotics didn't work for me so if that's your suggestion, please keep scrolling.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "Brooks Ariel or Hoka Bondi? My doc said Ariel but I don't like available color options so wondering if Hoka Bondi is good motion control too?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
    {
        "body": "I've tried Hoka Bondi 9, Brooks Adrenaline GTS and Hoka Arahi 9. No good. Foot still hurting. Any recommendations for a shoe or inserts.. etc? TIA",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": []
    },
]

# Deduplicate and add new posts
new_count = 0
for raw in new_raw_posts:
    key = raw['body'][:80].lower().strip()
    if key in existing_keys:
        continue
    existing_keys.add(key)
    max_id += 1
    new_count += 1
    
    body = raw['body']
    full_text = body + ' ' + ' '.join(raw.get('comments', []))
    
    post = {
        "id": max_id,
        "body": body,
        "author": None,
        "url": None,
        "source_group": raw['source_group'],
        "conditions": detect(full_text, CONDITIONS),
        "surgery_types": detect(full_text, SURGERY_TYPES),
        "products": detect(full_text, PRODUCTS),
        "treatments": detect(full_text, TREATMENTS),
        "images": [],
        "comments": raw.get('comments', [])
    }
    existing.append(post)

print(f"New posts added: {new_count}")
print(f"Total posts now: {len(existing)}")

# Save
with open('posts.json', 'w') as f:
    json.dump(existing, f, indent=2)

print("posts.json updated successfully")

# Print topic breakdown
from collections import Counter
conds = Counter()
for p in existing:
    for c in p.get('conditions', []):
        conds[c] += 1
print("\nTopic breakdown:")
for c, n in conds.most_common():
    print(f"  {c}: {n}")

# Print surgery types
surgs = Counter()
for p in existing:
    for s in p.get('surgery_types', []):
        surgs[s] += 1
print("\nSurgery types:")
for s, n in surgs.most_common():
    print(f"  {s}: {n}")

# Print products
prods = Counter()
for p in existing:
    for pr in p.get('products', []):
        prods[pr] += 1
print("\nProducts mentioned:")
for pr, n in prods.most_common():
    print(f"  {pr}: {n}")
