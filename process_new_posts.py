import json
import re
from datetime import datetime

# Load existing posts
with open('/tmp/fixfeetfast/posts.json', 'r') as f:
    existing_posts = json.load(f)

print(f"Existing posts: {len(existing_posts)}")

# Get existing post fingerprints for dedup
existing_fingerprints = set()
for p in existing_posts:
    body = p.get('body', '')
    fp = body[:80].lower().strip()
    fp = re.sub(r'\s+', ' ', fp)
    existing_fingerprints.add(fp)

# All new captured posts
new_raw_posts = [
    # === BUNION SURGERY GROUP - Lapiplasty search ===
    {
        "body": "I had surgery (lapiplasty n hammer toe) on March 28, 2026. I am still in a lot of pain n some days are worse then others. I us a knee scooter to b able to get to the bathroom. Told not to put any weight on my foot for d next 4 weeks. So I am trying to walk on my heal To transfer from bed to scooter. Is it norms for me to have so much pain in some days n not in others? Thx",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": ["I learned the hard way, 9 days was not fun.", "I learned the hard way. This problem as well as not being prepared for nausea were the worst part of the first week."],
    },
    {
        "body": "I had lapiplasty and akin osteotomy on 1/15 of this year. These were taken at my 6 week appointment. My great toe looks raised and almost rotated towards my pinky. Anybody else's X-rays look similar? Maybe it improved over time and didn't impact you in the long run?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Had my one week follow up today! The left is the x-ray of my foot before the surgery and the right is the x-ray of it after! My surgery was on 2/23/26. I had lapiplasty, with a donor bone graft. So far recovery is going better than I anticipated. The nerve block wore off the day after surgery and the pain was horrible. Before it wore off, I felt no pain at all. I am taking journavx, hydrocodone/acetaminophen for pain. I started the journavx the day of my surgery, but held off on the hydrocodone/acetaminophen until the pain started. Once the pain started, the hydrocodone was able to significantly reduce it. My doctor gave me the go ahead to take two of the hydrocodone at first, since the one I took wasn't helping. He also said I could take it every 4 hours, instead of 6. This was absolutely needed for the first few days, as the pain would start coming back badly after 4 hours. I have began weaning off of the hydrocodone, while continuing the journavx and acetaminophen. I am getting to where the pain isn't returning as quickly/badly. It has been 9 hours since I last took hydrocodone, and it still isn't hurting me! I had the splint removed today, and was given a boot to wear! So now I'm able to wear my foot icepack, which feels soooo good! I'm also working on moving my ankle and toes up and down. I'm continuing to elevate my foot as much as possible, and using a knee scooter to get around. I also have knee pads that I wear that help when I have to get down on the ground with my son. Hoping for fast healing and progress!",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "I am 4 weeks + 1 day PO. I had lapiplasty on NYE. Today i graduated to a boot. I feel great so far. And am excited to get moving again. The hardest part of all this for me has been being entirely dependent. My husband has been AMAZING. I am hoping to get in a tennis shoe in two weeks. I have included pics for you. I followed my docs instructions and took the pain meds. I am in MO, USA.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Hi! I recently joined this group to receive advice on a lapiplasty performed on my left foot where it appears I have a non-union and an abscess (sinus tunnel) that has formed over the Treace hardware that was used. Quick background. I am physically fit and mid-50s in age. I am not a smoker. I do cardio sports to stay in shape - primarily Cycling and Running. I believe I have good circulation in my feet. I had an issue with a Morton's neuroma where my toes would go numb.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    # === BUNION SURGERY GROUP - swelling recovery search ===
    {
        "body": "Had bunion surgery July 25, 2025. Had major swelling and dr said 'are you sure you aren't allergic to absorbable surtures?' But did nothing. At all check ups, doctor said everything was 'normal', the pain, the swelling, the funny feeling. Walking is still painful (7 out of 10) Foot is still slightly swollen and feels like there is a very tight band around my foot. Edit - when my foot has no pressure, my big toe touches my second toe.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "4 weeks post op right foot - lapidus procedure. Before and now photo - recovery going well - no weight bearing yet but pleased with how it looks and hardly any swelling and no pain. That will probably come when I start to weight bear.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "ETA: Finally home from the hospital. I am allergic to anti-inflammatory drugs so my surgeon wrapped it loose to allow for swelling and I was given an extra nerve block that will hopefully last for 48 hours. Happy healing everyone! About a year ago I had lapidus and a tendon release for hammertoe on my second toe. Recovery was long and frustrating, but smooth, and I am back to normal. Tomorrow I will say good-bye to my little friend on my right foot. I am definitely not excited about going through recovery again.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    # === BUNION SURGERY GROUP - feed post ===
    {
        "body": "If I can offer one crucial bit of advice for surgery recovery after anesthesia: Fibre. Water. Laxatives. If you know, you know.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": ["I learned the hard way, 9 days was not fun.", "I learned the hard way. This problem as well as not being prepared for nausea were the worst part of the first week."],
    },
    # === FOREFOOT FORUM - hammer toe search ===
    {
        "body": "Surgery on rt foot for Tailor's bunion and hammer toe (4th) on Tuesday. Nervous but excited to FINALLY deal with this after a lifetime of pain that has gotten worse in recent years.",
        "source_group": "Forefoot Forum",
        "comments": [],
    },
    {
        "body": "I'm 14 weeks post op bunionectomy, hammer toe. I'm still having difficulty walking without a walker or cane, but yesterday I walked much more than usual and today my foot is painful and swollen more than usual. I also put a very uncomfortable ice pack on my foot yesterday and feel I applied it too tight so maybe it's that causing pain. Anyone have these issues?",
        "source_group": "Forefoot Forum",
        "comments": [],
    },
    {
        "body": "Does anyone have recommendations for a slipper or recovery slide that has worked well with having a tailor's bunion? A thong type flip flop won't work for me due to a hammer toe I developed on the 2nd toe.",
        "source_group": "Forefoot Forum",
        "comments": [],
    },
    {
        "body": "Hello! I'm trying to decide between surgical options or no surgery. I'm 57 years old and have lots of travel and other plans for being active. Problem: painful toes (15+ years) and metatarsal ball of foot (since last fall). Cause of pain: 1) toes stepping on the bottoms of their neighboring toes causing painful sores and 2) prominent metatarsals taking too much impact, leading to stress fractures.",
        "source_group": "Forefoot Forum",
        "comments": [],
    },
    {
        "body": "New to post. Need help for ugly hammer toe!!!!",
        "source_group": "Forefoot Forum",
        "comments": [],
    },
    # === PF GROUP - heel spur search ===
    {
        "body": "I just went to a podiatrist and he said I have calcification around the heel spur. I'm in so much pain. I am doing the frozen water bottle rolling, tennis ball rolling, the stretches in the AM & throughout the day and nothing seems to be easing it. The doctor wants me to have physical therapy for 3 months and if that doesn't work, he would give me a shot of Cortisone. I may be able to get a shot through a different doctor. Has that helped anyone?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Heel Spurs. They are not the cause of your pain when it comes to PF. Over 15% of the world's population have a heel spur. Most of these people don't even realise they have one. And only discover it when they have a X-Ray for PF.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I've had plantar fasciitis and a heel spur for 10 months despite steroid injections, B12 injections, and shockwave therapy. I still can't go back to the gym or Zumba and it's very frustrating. Has anyone tried plantar fascia embolization or PFE?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "My PF caused a heel bone spur, any suggestions for home remedies or anything else that helps with the bone spur? Thanks",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I used to have intense pain in my heels, I have very large heel spurs, I had massive amounts of tearing to my PF muscle and I had a trapped Baxtor nerve. I had surgery for a Tarsal tunnel release and partial plantar fascia release- I had both done at the same time in Nov. Ive had a major set back as my foot got infected, however day by day, its getting better, still extremely tender and only put pressure on my foot for a certain amount of time, but its so much better than before the surgery. Its a long process, but so far, its been worth it. Pic of incision is in the comments. Feel free to ask any questions.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === TOENAIL FUNGUS GROUP - terbinafine search ===
    {
        "body": "Hi all. I was prescribed Terbinafine after other home treatments were unsuccessful. After a few days of treatment My throat became sore, not realising it could possibly be the Terbinafine I took some antihistamines thinking it may have been after cutting my grass for the first time this year. During the 3rd week on Terbinafine I developed ulcers on my tongue, throat and what felt in my upper lungs felt inflamed, like a burning sensation.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Has anyone ever used the tanning bed at least twice/week while taking Terbinafine/Lamisil? I was prescribed this medication (I've taken it before but can't remember if I was tanning at the time or not) and I want to keep tanning. I'm getting my graduation pictures (for my doctorate) done in a few weeks and want to be tan, then I graduate May 9th. I want to continue tanning at least until then, so I was wondering if I should take it and keep tanning.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Does this look like new, clean growth? I've been on ciclopirox lacquer for almost 4 months. I was also on terbinafine but had to stop that a month in due to an allergic reaction. I THINK this is clean outgrowth but I don't want to get my hopes up. Out of the 4 that are infected, this is the only one showing improvement.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "So this is pretty representative of how my toenail fungus stays with over the counter stuff. I did two months of terbinafine a month ago then stopped because life stuff and now I have to do my final month. I really hope the yellow corners go away. Should I cut them off even though I'd have to cut my nail deep in the corners instead of straight across? Ignore the white in the crease of the left pic, I just buffed them to keep them extra thin since I do topical stuff too.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Would applying Terbinafine cream be any good, as well as taking the oral medication?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    # === PF GROUP - night splint search ===
    {
        "body": "Almost fully recovered thanks to my night splint. Next up: 10 day trip to Paris this summer. I have very flat feet, so a little lift in my shoes works wonders. Experienced flat footers weigh in!!!! What sandal would you recommend for flat feet and somewhat stylish.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Is night splint a big help for you guys? Planning to buy those.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "While a night splint does seem to help, it's bulky and uncomfortable. My sheets are loose, but my feet are pointed down while I sleep and that seems to aggravate BOTH calves. Are y'all using anything while you sleep that keeps your feet more towards 90 degrees?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I've been using a night splint, just wondering if anyone else has used one and do they help.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "My PT recommended a night splint sock but I couldn't find one that would fit me.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === BUNION SURGERY GROUP - Hoka search ===
    {
        "body": "Shoes or slippers?! I was fitted for Hoka Clifton at running shop. I wore these on Sunday, but shoes seems pretty snug on surgical foot. Foot was too swollen for any shoes my mid-morning on Monday so I bought extra large mens slippers. Should I buy a size up for my surgical foot in the Bondi's and wear two different sizes?!",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "I bought Hoka x-wide Clifton from running store after surgery. Are these wide toe box enough?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Hi all I'm 15 months post op where I had my toe fused. I have been wearing Hoka Bondi shoes since I started walking. I have recently started wearing thongs again. I'm wearing Archies thongs and not finding them good. Any recommendations on comfortable thongs would be appreciated. Or even a slide on shoe that you've found to be comfy to walk in after toe fusion. Thanks in advance.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "I think I may need to order 100 pairs of these Hoka sneakers! I feel like I'm walking on cloud without inserts and I also am able to walk without a limp like I was able to before my surgery! Thanks mom!",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Apparently, I have a few things going on here: 1. Bunion - had it for years but became more pronounced this year where you can see it poking out a little in my Hoka's. 2. Hallux Limitus- stiff big toe & starting to lean inward. 3. Lateral deviation of the sesamoid bone positioning. X-ray showed the one was on the right of my big toe metatarsal instead of underneath it where it should be. I believe this is what's causing me the most pain walking. I've been having trouble walking correctly where I can't push off the ball of my foot and put pressure on my toes and noticing my walking stance is now leaning towards the outside of my right foot. Noticing pain in my hips and lower back too, so I think this could be a domino effect. I've been limited to only wearing my Hoka's even to work bc other shoes just hurt. Upon the doctor telling me I could get a Cortizone shot there's really nothing else I can do because I have orthotics already, I brought up surgery (she did not) & she said she can fix this with surgery. My gut is telling me to go for it now that my deductible has been met and get it over with, but not sure if I need to research this doctor more and even how to do that. I like her but she's no frills, gets you in & out, and her last Google reviews are from 2017 and prior. Any advice is welcome. Should I bother getting a second opinion?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    # === PF GROUP - cortisone injection search ===
    {
        "body": "I had a cortisone injection in my right foot 2 wks ago. I had 1 week of some relief. I will have 2 more injections done tomorrow in the top of my foot by an xray machine. Has anyone had injections like this before?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "What are people's experience with cortisone injections for PF?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Has anyone had success with a cortisone injection for a torn plantar fascia? I'd love to hear about your experience. Thank you.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Wondering if anyone has experienced this and whether or not to go to urgent care. So I had plantar fascitis for months got a cortisone injection and it seemed to settle. Well yesterday I went down steps and felt a pop to the back of the heel and now it really hurts more then before with the plantar fascitis. Even in my toes it is tingling.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I read different posts about people experiences with PRP. It seems doctors follow different ways of doing it. Mine said it will be similar to the cortisone injection. He does the first shot of Lidocaine and then cortisone shot. I can tolerate those shots. Mine are injected in the side of my foot. Not the heal. I see it mentioned about a nerve blocker on this site. Not sure what that is. Has anyone had this done in a similar way?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === PF GROUP - custom orthotics search ===
    {
        "body": "Custom or ready made Amazon Orthotics? Which is better? Share your experiences. For me it's a transitioning issue.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "PF diagnosed in 2015. Custom orthotics + PT off/on for a year. 2016 PF partial rupture in right foot. Boot for 3 months. 2017 - 8k spent in PT, shockwave, acupuncture. No improvements. 2018 PF partial tare in the left foot. Boot for 2 months until I could tolerate the pain without. Half a dozen orthotics over the years. Various trials and doses of cortisone injections every 3 months from 2019-2024.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Does anyone have pain that moves around? Every time I wear a different shoe even if it's with my same custom orthotics the pain moves to different areas. Also, has anyone had custom orthotics that made their feet worse? I am wondering if I should try again with my custom orthotics.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Has anyone had luck with custom orthotics such as StrideSoles or Upstep? They're so expensive, I don't want to spend the money unless they actually work.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "When you buy new shoes to help with PF, do you still use inserts or custom orthotics in the new shoes?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === TOENAIL FUNGUS GROUP - laser treatment search ===
    {
        "body": "Hi. I had fungal nails for years then laser therapy cleared it up over 2yrs ago. They recovered well. But I'm now experiencing chronic oncholysis resulting in toenails being really damaged. I don't have any debris etc to indicate fungus has returned & I treated for a while but stopped as I felt it wasn't helping. I think my toes got worse after a 3 week period of nail polish 4 months ago but now they just seem to have deteriorated. Any ideas what other conditions would more likely cause this?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "I'm seeing a podiatrist in a few weeks who has a foot aesthetics practice. From what I can tell from reviews, her patients have had success with laser. All of my online research looks like lasers for fungus are 50/50. Anyone here had any luck with lasers? Two rounds of terbinafine did nothing for me.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "I've battled with my toenail fungus for 20 years, trying various topical over the counter medications, curanail, scholl....they did not work. I tried soaking them in epsom salts, applying tea tree oil, which did improve them but not destroy the fungus permanently. I tried imperial feet as it was highlighted rated on amazon, that just made the nails soft to cut it back, again not killing the fungus. I then tried laser treatment, which was expensive, but came highly rated to cure toenail fungus. I had high hopes but it did not work. I finally had success in February 2025. I went to my doctors and got prescribed antifungal terbinafine tablets, 1 a day for 3 months, it's taken a few more months for the nails to fully regrow but I'm now toenail fungus free.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Has any one tried laser treatment? If so, what was your outcome?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "How much cost is laser treatment and how many times do u need for moderate to severe infection basically on all toes?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    # === MIS BUNION GROUP - minimally invasive search ===
    {
        "body": "This whole time I misunderstood and thought I was getting lapiplasty till I spoke with the doctors office and they told me the name of my procedure is Right minimally invasive hallux Valgus Correction.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    {
        "body": "Has anyone had the bunionplasty 360? It's a relatively new procedure, but from the pictures I've seen, it doesn't look as minimally invasive as doctor claims. Surgery in 3 weeks for both feet!",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    {
        "body": "I have a surgeon who recommends, and does herself, minimally invasive bunion surgery, and tells me I have about a decade before it is too late. These have come on in the last year and it is genetic in my family, just late and fast for me (I'm 64). How many opinions should I get and how on earth do I choose?",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    {
        "body": "I'm a healthy 70 yr. old facing Arthrex minimally invasive surgery. I live alone. Will I be able to manage on my own? How soon before I can walk my dog?",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    {
        "body": "Friendly reminder from someone who learned the hard way. If you're scheduled for (or recovering from) minimally invasive bunion surgery, please don't rush the walking - even if you feel like you can. I truly thought I was being careful, but starting to walk too soon caused my toe to shift and the screws in my foot to move. Now there's a possibility my doctor may have to go back in and remove them, which was never my intention. I'm sharing this as a gentle warning, not to scare anyone - just to encourage rest, patience, and following post-op instructions closely. Healing takes time, even when the surgery is minimally invasive. Learn from my experience: rest really means rest. Your future self (and your foot!) will thank you. Sending healing vibes to everyone in recovery. Side note: I have to wear my surgical shoe for another month and watch the swelling and possible pain. This is not fun but could've been prevented.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    # === PF GROUP - shockwave therapy search ===
    {
        "body": "For people who have tried softwave/shockwave therapy for plantar fasciitis how many treatments did you do?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Question for the group: I've been wanting to try shockwave therapy and understand it gets expensive. I am therefore considering buying my own machine. Has anyone made the switch from clinic treatments to a home device? I'm curious if the 'home version' is powerful enough to actually work. Any brand recommendations?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Has anyone used Shockwave therapy?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I am undergoing shockwave therapy, and it has been painful for me. After the third session, I had to go out for three consecutive days, and I experienced pain in my leg. One of those days, I wore a compression sock that I had just bought, but it turned out to be tighter than needed, which caused congestion and increased pain. My doctor prescribed anti-inflammatory medications. Is what happened concerning? And should I stop the shockwave therapy sessions?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Talk to me about Shockwave therapy. Does it actually work? What is the success rate? Has anyone had any success getting it covered by insurance? EDIT: Has anyone done it with success after having PF for several years and being post OP about 7 month of the plantar fasciotomy with extreme swelling and scar tissue accompanied with pain from the surgery and had positive results?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === BUNION SUPPORT GROUP - toe spacer search ===
    {
        "body": "Recently I noticed big toes were leading to second toes, it was more obvious for left toe. Sometimes I feel needles on the big toes. So I went to see a GP. He said he wouldn't refer me to specialist unless I have eg hammer toes or deformed bones, and also my needle sensation is not happening all the time. He only asked me to continue wearing toe spacers and do a blood test. Now I feel helpless coz it seems he can't refer me to a foot doctor yet. Was this also how your GP advise you?",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
    {
        "body": "I got wide toe box sneakers. Does anyone have suggestions for comfortable toe separators or toe socks I can wear with them? I wear the pictured separator socks to bed. I know I can't correct my bunions these ways, but I'm hoping to stop the progression. Of course our cat got in the way of my picture, but I figured I won't redo it. I know many people like cat and dog pictures (like me).",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
    {
        "body": "With the discomfort of toes touching one another, anyone is able to wear toe spacer the whole day when moving about?",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
    {
        "body": "Has anyone in the U.K. found toe spacers that can be used all the time comfortably? I splashed out on correct toes and they have damaged the skin and were very painful to walk in. (Rubbing the skin). I'm athletic and want to run in spacers.",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
    {
        "body": "My foot is still slightly swollen but I'm noticing my second toe slightly shifts left touching my big toe. My doctor said the big toe is straight but I'm annoyed how close together my toes still are. What do y'all think? Am I overreacting? I'm happy I'm not in pain as I was in so much pain prior to surgery but I think now I'm obsessed with how it looks. I have been wearing a spacer and still do 24/7. I added my before photo at the end.",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
]

# Auto-detect functions
CONDITIONS = {
    'bunion': r'\bbunion\b',
    'hammer toe': r'\bhammer\s*toe\b',
    'hallux valgus': r'\bhallux\s*v[ao]lgus\b',
    'hallux limitus': r'\bhallux\s*limitus\b',
    'hallux rigidus': r'\bhallux\s*rigidus\b',
    "tailor's bunion": r"\btailor'?s?\s*bunion\b",
    'bunionette': r'\bbunionette\b',
    'plantar fasciitis': r'\bplantar\s*fasc[ii]tis\b',
    'heel spur': r'\bheel\s*spur\b',
    'flat feet': r'\bflat\s*feet\b',
    'toenail fungus': r'\b(toenail|toe\s*nail)\s*fungus\b|fungal\s*nail',
    'ingrown toenail': r'\bingrown\s*toenail\b',
    'metatarsalgia': r'\bmetatarsalgia\b',
    'neuroma': r'\bneuroma\b',
    'sesamoiditis': r'\bsesamoid\b',
    'gout': r'\bgout\b',
    'arthritis': r'\barthritis\b',
    'bone spur': r'\bbone\s*spur\b',
    'neuropathy': r'\bneuropathy\b',
    'tendonitis': r'\btendonitis\b',
    'plantar plate tear': r'\bplantar\s*plate\b',
    'oncholysis': r'\boncholysis\b',
}

SURGERY_TYPES = {
    'MIS': r'\b(MIS|minimally\s*invasive)\b',
    'Lapiplasty': r'\blapiplasty\b',
    'scarf akin': r'\bscarf\s*akin\b',
    'osteotomy': r'\bosteotomy\b',
    'chevron': r'\bchevron\b',
    'Austin': r'\baustin\b',
    'arthroplasty': r'\barthroplasty\b',
    'arthrodesis': r'\barthrodesis\b',
    'bunionectomy': r'\bbunionectomy\b',
    'toe fusion': r'\btoe\s*fus(ion|ed)\b',
    'MICA': r'\bMICA\b',
    'percutaneous': r'\bpercutaneous\b',
    'cheilectomy': r'\bcheilectomy\b',
    'lapidus': r'\blapidus\b',
    'akin': r'\bakin\b',
    'tarsal tunnel release': r'\btarsal\s*tunnel\b',
    'plantar fascia release': r'\bplantar\s*fasc(ia|iotomy)\s*release\b',
}

PRODUCTS = {
    'Hoka': r'\bhoka\b',
    'Orthofeet': r'\borthofeet\b',
    'New Balance': r'\bnew\s*balance\b',
    'Skechers': r'\bskechers\b',
    'Brooks': r'\bbrooks\b',
    'Nike': r'\bnike\b',
    'Birkenstock': r'\bbirkenstock\b',
    'Correct Toes': r'\bcorrect\s*toes\b',
    'Archies': r'\barchies\b',
    'Arthrex': r'\barthrex\b',
    'Lamisil': r'\blamisil\b',
    'Vicks': r'\bvicks\b',
    'Dr. Scholl\'s': r'\bdr\.?\s*scholl\b',
    'Superfeet': r'\bsuperfeet\b',
    'StrideSoles': r'\bstridesoles\b',
    'Upstep': r'\bupstep\b',
}

TREATMENTS = {
    'surgery': r'\bsurg(ery|ical)\b',
    'physical therapy': r'\b(physical\s*therapy|PT)\b',
    'cortisone': r'\bcortizone?\b|cortisone',
    'steroid injection': r'\bsteroid\s*inject\b',
    'orthotics': r'\borthotic\b',
    'icing': r'\bice\s*pack\b|\bicing\b',
    'elevation': r'\belevat\b',
    'stretching': r'\bstretch\b',
    'shockwave therapy': r'\bshockwave\b|softwave',
    'laser therapy': r'\blaser\b',
    'anti-inflammatory': r'\banti.?inflammat\b|ibuprofen',
    'terbinafine': r'\bterbinafine\b',
    'tea tree oil': r'\btea\s*tree\b',
    'night splint': r'\bnight\s*splint\b',
    'rolling': r'\brolling\b',
    'custom orthotics': r'\bcustom\s*orthotic\b',
    'nerve block': r'\bnerve\s*block\b',
    'PRP': r'\bPRP\b',
    'acupuncture': r'\bacupuncture\b',
    'ciclopirox': r'\bciclopirox\b',
    'bone graft': r'\bbone\s*graft\b',
    'compression': r'\bcompression\b',
    'toe spacers': r'\btoe\s*spacer\b|toe\s*separator\b',
}

def detect(text, mapping):
    found = []
    for name, pattern in mapping.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found

# Process and deduplicate
next_id = max(p['id'] for p in existing_posts) + 1
new_posts = []
skipped = 0
today = datetime.now().strftime('%Y-%m-%d')

for raw in new_raw_posts:
    body = raw['body']
    fp = body[:80].lower().strip()
    fp = re.sub(r'\s+', ' ', fp)
    
    if fp in existing_fingerprints:
        skipped += 1
        continue
    
    existing_fingerprints.add(fp)
    
    post = {
        "id": next_id,
        "body": body,
        "author": None,
        "url": None,
        "source_group": raw['source_group'],
        "date_captured": today,
        "conditions_mentioned": detect(body, CONDITIONS),
        "surgery_types_mentioned": detect(body, SURGERY_TYPES),
        "treatments_mentioned": detect(body, TREATMENTS),
        "products_mentioned": detect(body, PRODUCTS),
        "comments": raw.get('comments', []),
        "images": []
    }
    
    new_posts.append(post)
    next_id += 1

print(f"New posts to add: {len(new_posts)}")
print(f"Skipped (duplicates): {skipped}")

# Merge
all_posts = existing_posts + new_posts

# Save
with open('/tmp/fixfeetfast/posts.json', 'w') as f:
    json.dump(all_posts, f, indent=2)

print(f"Total posts now: {len(all_posts)}")

# Print summary
conditions_count = {}
for p in new_posts:
    for c in p['conditions_mentioned']:
        conditions_count[c] = conditions_count.get(c, 0) + 1

products_count = {}
for p in new_posts:
    for pr in p['products_mentioned']:
        products_count[pr] = products_count.get(pr, 0) + 1

treatments_count = {}
for p in new_posts:
    for t in p['treatments_mentioned']:
        treatments_count[t] = treatments_count.get(t, 0) + 1

print("\nConditions in new posts:")
for k, v in sorted(conditions_count.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("\nProducts mentioned:")
for k, v in sorted(products_count.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("\nTreatments mentioned:")
for k, v in sorted(treatments_count.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

# Groups breakdown
groups = {}
for p in new_posts:
    g = p['source_group']
    groups[g] = groups.get(g, 0) + 1
print("\nNew posts by group:")
for k, v in sorted(groups.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
