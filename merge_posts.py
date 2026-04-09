import json
from datetime import datetime

# Load existing posts
with open('/tmp/fixfeetfast/posts.json', 'r') as f:
    existing_posts = json.load(f)

max_id = max(p['id'] for p in existing_posts)
existing_fingerprints = set()
for p in existing_posts:
    fp = p['body'][:80].lower().strip()
    existing_fingerprints.add(fp)

print(f"Existing posts: {len(existing_posts)}, Max ID: {max_id}")
print(f"Existing fingerprints: {len(existing_fingerprints)}")

today = datetime.now().strftime('%Y-%m-%d')

# All captured posts from today's scrape
new_raw_posts = [
    # === FROM MAIN FEED - bunion surgery group ===
    {
        "body": "Hi everyone, I hope you are all doing well. I wanted to give an update after my 2 weeks post op appointment. I had hardware removal, triplane osteotomy of the hindfoot, 1st metatarsal wedge osteotomy, heel slide osteotomy, and a bone marrow aspiration from the proximal tibia. They used a dynanail mini and a compression screw to give the best chance of healing at the hindfoot with constant compression. My surgeon and surgeon's fellow feel that everything is looking good so far.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": ["Good to hear from you so glad you are doing well, let's hope this is it xxx sending love and wishing speedy recovery"],
    },
    # === LAPIPLASTY SEARCH - bunion surgery group ===
    {
        "body": "Positive story so far. Had lapiplasty in January of this year on the right foot. Not gonna lie it was living hell the first few days. But my bones fused in record time (surgeon's words) and its been pretty seamless since. Still some swelling and tenderness but every day is a little better. Had MIS surgery today on my left foot. So far its been painless! He numbed the foot but no nerve block. He doesn't like doing them. Thinks it causes nerve damage. About yeeted myself out of the surgery center before surgery. The nurse informed me that it was going to be an hour and 45 minutes and I was getting a general anesthesia. Surgeon initially told me 30 minutes and under twilight. Will be partial weight bearing tomorrow as tolerated. So far I'm glad I did both feet and hope to be walking without bunion pain soon! It's to see what does better...just screws or a plate and screws.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Hey yall! I am having the lapiplasty operation on my left foot this June! I had the Austin procedure done to my right foot in 2022. It was a long hard recovery. But the pain was manageable. Just took a long time for my foot to look normal nevertheless, it changed my life for the better! And it's time to do the left! I am in pain all day everyday! I am wondering if anyone has had the two separate procedures on their feet?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "I had surgery (lapiplasty n hammer toe) on March 28, 2026. I am still in a lot of pain n some days are worse then others. I use a knee scooter to be able to get to the bathroom. Told not to put any weight on my foot for the next 4 weeks. So I am trying to walk on my heel to transfer from bed to scooter. Is it normal for me to have so much pain on some days and not on others?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Recovery update after my June 11, 2025 bunion repair (Lapiplasty with correction of the bunion with Calcaneal Bone Graft and lesser toe corrections): Non-weight bearing for 4 weeks to walking in boot for 4 weeks. Then transitioned to a tennis shoe for 12 weeks of physical therapy and returned to work in October on modified duty. After returning, I started having pain under the outside of my ankle toward pinkie toe. I saw my surgeon again.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Good Morning! I will be having Lapiplasty procedure done on April 8th. I know how some feel about this procedure, but my DR and I have agreed this is best for me. My question, what is something that you wish you did before your surgery or bought to help with recovery?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    # === TOE SPACER SEARCH - bunion surgery group ===
    {
        "body": "I think I made a mistake. I have been using a toe spacer between my big toe and second toe and have just left it there for months - I guess now that I think about it pretty gross. Now my second toe is all inflamed and swollen and the skin is peeling off. Feels like it's broken. I finally took the toe spacer out and slathered neosporin on it. Has anyone else had this happen?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "5 days post op. Foot was rewrapped and can be removed Friday. Then toe spacer between first and second toe. Next follow up in two weeks stitches will be removed and fresh x-rays taken.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Looking for recommendations for a toe spacer? Specially for my large toe and the one next to it. I don't want to waste money trying different ones so hoping you can help me!",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "1st photo is pre surgery Nov 2023. Had surgery 10/2024. Middle photo is Jan 2025 - foot looking good but I wasn't faithful wearing toe spacer. Right photo last week Jan 2026. Toe has definitely wandered back. Could go back in for bunion bone shaved and big toe fusion but I'm still trying to get flexibility in all my toes (3 were shortened and why I have pins). Anyone have similar issue and did you go back for a fusion and shave?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Uh did anyone else wear a toe spacer for a while and as a result get a pain in the middle top of the foot? I feel like I'm trading one issue for another.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    # === SWELLING SEARCH - bunion surgery group ===
    {
        "body": "First pic is from last September and the second is from today. I had bunion surgery and hammertoe fusion back last June 2025. It's almost a year but this toe is still big and swollen looking. Will it stay like this? It's currently pretty sore at the moment but it's usually sore on and off like that. The swelling and size stays constant.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "When did your swelling completely go away?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "7 weeks post op right bunion surgery and still swelling with mild pain. Also noticed a space between great toe and 2nd toe. How long did it take you for swelling to go away and did 2nd toe go back to normal?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Something interesting I learned while recovering from foot surgery. Pain and swelling aren't only controlled by medication. Several body systems can reduce pain chemistry naturally. Strong non-drug tools include various approaches.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    # === HEEL SPUR SEARCH - PF group ===
    {
        "body": "Plantar fasciitis with multiple treatments for 15 years. Just got steroid injections. It cleared the pain up all except for where my heel spur is in my left foot. The insoles make me feel the best, but depending on what shoe I'm wearing, my feet either slide to the outside where I start getting pains and other places on my foot or hip. So I tried Kuru shoes.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Not PF specific but PF adjacent - I have a sharp pain in this area. It's kind of extra bony right there. Anyone know what this is? I googled and it doesn't seem to be in the right place for a bunion or bone spur, right?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Help please I had a steroid injection in my heel yesterday done under ultrasound having plantar fasciitis since last April. I was told it would be painful, yes it was, very. I never want another one. I was told to take paracetamol as it would hurt when the anesthesia wore off. Nothing has prepared me for the pain I'm feeling from 2am this morning, I can't even put my foot to the floor. Can't walk, the pain is unbearable. Has anyone experienced this?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I do feel a bit uneasy. Had TenJet surgery in December after injections and boot and all that jazz to try to heal my PF. Still had more pain weeks after procedure. Doctor ordered another MRI and PF got worse, is now tearing off the heel bone on the inside and lateral side plus tendinitis of the tibia tendon and heel spurs. Podiatrist recommended releasing the fascia as we have been at this for 2 years now with no progress.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I just went to a podiatrist and he said I have calcification around the heel spur. I'm in so much pain. I am doing the frozen water bottle rolling, tennis ball rolling, the stretches in the AM and throughout the day and nothing seems to be easing it. The doctor wants me to have physical therapy for 3 months and if that doesn't work, he would give me a shot of Cortisone.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === NIGHT SPLINT SEARCH - PF group ===
    {
        "body": "I have had heel spurs with plantar fasciitis under both feet for 20 months now. I have tried a night splint, 8 shockwave treatments, 5 osteopath visits, orthopedic insoles, stretching and strengthening exercises including with a ball, cooling, and massage devices. Nothing helps; I am at my wit's end. Do you have any tips? Or good stories, because I am afraid this will never go away. I am a young woman of 29.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Night splints... please share pros and cons and if I should be wearing them. Thanks so much.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Almost fully recovered thanks to my night splint. Next up: 10 day trip to Paris this summer. I have very flat feet, so a little lift in my shoes works wonders. Experienced flat footers weigh in! What sandal would you recommend for flat feet and somewhat stylish?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "My Doctor didn't give me a shot for my tendon. He gave me a boot to wear for 6 weeks. He does not give shots to a tendon. Secondly he gave me a night splint.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Is night splint a big help for you guys? Planning to buy those.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === TERBINAFINE SEARCH - Toenail Fungus group ===
    {
        "body": "Hey! Ive been on Terbinafine for 2 months and the situation looks the same. No change. My case is mild, the root is clear. Its the tip and sides thats yellow. Has anyone experienced this and knows how long it takes to kick in?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Just saw a sponsored ad that looks very interesting. It's a topical of itraconazole and terbinafine with DMSO to aid in absorption. I took terbinafine in the past and I had issues with it, so this is very interesting. I have not checked it out yet.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Hi all. I was prescribed Terbinafine after other home treatments were unsuccessful. After a few days of treatment my throat became sore, not realising it could possibly be the Terbinafine I took some antihistamines thinking it may have been after cutting my grass for the first time this year. During the 3rd week on Terbinafine I developed ulcers on my tongue, throat and what felt in my upper lungs felt inflamed, like a burning sensation.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Has anyone ever used the tanning bed at least twice per week while taking Terbinafine/Lamisil? I was prescribed this medication. I've taken it before but can't remember if I was tanning at the time or not. I want to keep tanning. I'm getting my graduation pictures done in a few weeks and want to be tan.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Dermatologist diagnosed a fungal nail infection. I used LOCETAR nail lacquer for treatment but also looking at other options.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    # === HOKA SEARCH - bunion surgery group ===
    {
        "body": "I transitioned into shoes last Thursday and I went and bought 8.5 mens wide Hoka Bondi 9. The women's Hoka shoe at the store don't have a wide. I feel so good in the men's wide. This week marks 10 weeks post op. I'm now walking around 8-10k steps most days. I continue to elevate my foot and ice it anytime I'm sitting down during the days or evening before bed time.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Any ladies out there looking for sandals should check these two out, one high end price and one is low end. 1. Hoka Infini Hike TC and 2. Whitin Hiking Sandal. Both have been very comfortable since transitioning from having to wear a carbon fiber insole. They also are fully adjustable and allow for my swelling that I am still experiencing.",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "Shoes or slippers? I was fitted for Hoka Clifton at running shop. I wore these on Sunday, but shoes seems pretty snug on surgical foot. Foot was too swollen for any shoes by mid-morning on Monday so I bought extra large mens slippers. Should I buy a size up for my surgical foot in the Bondi's and wear two different sizes?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "7 days post washing my foot. I can see it healing. Thank you bunion family for encouraging to wash. Someone said washing will help with healing, I been using antibacterial soap. Currently 8 weeks post op. Hopefully I can drive soon. What sneakers are better Hoka or Brooks?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    {
        "body": "I bought Hoka x-wide Clifton from running store after surgery. Are these wide toe box enough?",
        "source_group": "bunion surgery / foot surgery support group",
        "comments": [],
    },
    # === NEUROMA SEARCH - Forefoot Forum ===
    {
        "body": "Hi has anyone tried softwave for Morton's neuroma?",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
    {
        "body": "Hello! I'm trying to decide between surgical options or no surgery. I'm 57 years old and have lots of travel and other plans for being active. Problem: painful toes for 15+ years and metatarsal ball of foot since last fall. Cause of pain: 1) toes stepping on the bottoms of their neighboring toes causing painful sores and 2) prominent metatarsals taking too much impact, leading to stress fractures.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
    {
        "body": "Hi, I'm hoping for some advice. I live in the UK and I hurt my foot at the beginning of June. The pain is around the ball of my foot, it feels like there is a lump there and it's painful to walk on. I have been to my GP, who thinks it may be a Morton's neuroma and has referred me to hand and foot surgery. I'm not convinced as it is now making my second toe stick up and there is generalised swelling in the area.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
    {
        "body": "Hi, had a little bump on left foot for a while and the right one popped a year ago. I didn't know anything about bunions before that. But now its extreme, no shoes fit. Pain is horrible. Got some hoka wide shoes but even they hurt after a while. Any info on shoes I can try would be appreciated. Also it seems like there is a lot of inflammation going on inside, has anyone tried cortisone injections? I'm so limited by this condition.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
    {
        "body": "My pinky folds down and I got a bump below my pinky. All the podiatrists say it is not a tailor's bunion. I don't know what to do. 4th toe also curls bad and hurts.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
    # === ARCH SUPPORT SEARCH - PF group ===
    {
        "body": "I have always liked Teva sandals, I messaged them and got this prompt reply. This is for UK customers. Although we are unable to provide any medical advice, it sounds like you may benefit from a Teva with a contoured footbed and a specialized heel to absorb shock. For this reason, we suggest you check out our Tirra styles. It features great arch support and a Shoc Pad in the heel that specifically cushions the area where plantar fasciitis pain occurs.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I tried on some Oofos flip flops today, but the arch support was more towards the front of my foot. I need an arch support that goes a little more towards the heel. Anyone have any other recommendations?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Low profile sneakers with arch support? I hate the look of big bulky sneakers. Are there any sneakers out there with good arch support that are lower profile style?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Has anyone tried the Vionic shoes? Supposed to be comparable to expensive arch support.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I've had PF for 4+ months. I've recently started running again just 3-4 miles at a time and seem to be tolerating it okay. I mostly run in Altra FWD Vias. The last two times, I ran without the inserts my podiatrist recommended. I just used the insoles that came with the shoes. It actually felt a lot better as I ran. I still got the same level of flare up post run. Does anybody know why removing the inserts feels better? Is it okay to run without them?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === WEIGHT BEARING SEARCH - MIS bunion group ===
    {
        "body": "My before and after. Surgery on 12/18. Just had my 6 weeks. Doc told me everything looks great and I'm healing well.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    {
        "body": "Does anyone have any guidelines on the weight-bearing timelines post op? I believe I've seen a lot of 0% weight bearing the first 2 weeks post op, but then what? I'm at 6-weeks post op and the surgical site and even my hammertoe correction seems to be recovering well, but every few days I get the most wicked sprained ankle pain to the point my ankles are purple. And I know it's because I'm compensating. I feel if I can start putting 50% weight on my entire foot it would help out my ankle a lot. When does bone fully heal anyway?",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    {
        "body": "I need to hear some MIS SUCCESS stories! Let me hear from the people who have had no issues, who have healed and recovered as they were told they would. I feel like the horror stories take center stage. I am 10 days PO, 50% weight-bearing, and see my surgeon tomorrow for my 1st PO visit/suture removal. Thus far, I have had no pain and have only needed ibuprofen with the exception of day 5 after a minor stumble I took an actual pain pill.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    {
        "body": "I had a bunion operation on my right foot a number of years ago. I now need to do my left foot but cannot remember how long I was non weight bearing. For minimally invasive surgery is the period of non weight bearing very long?",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    {
        "body": "I had my Arthrex MIS bunion surgery on Feb 14th. I was instructed to be non weight bearing until my 2 week post op follow up on the 27th. I am told I'd be able to bear weight only on heel for short distance after that. Anyone else have the same experience? I've been in boot 24/7 per instruction. I'm so nervous about putting weight on it. How is the pain 2 weeks post op? Also has anyone else experienced a very tender to press on heel? It's numb to the touch but when I press on it.",
        "source_group": "Minimally invasive bunion surgery",
        "comments": [],
    },
    # === FUNGAL NAIL SEARCH - Toenail Fungus group ===
    {
        "body": "What has truly worked for successfully recovering from toenail fungus?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Has anyone tried a product called Bare Feet? It's a capsule and advertised and talked about by a Pharmacist named Lisa. Claims it cures the Fungus, not just camouflages the ugly nail. It is between 40 and 60 dollars a bottle. They claim success in weeks but then offers a years supply which sounds contradictory to me. We'd like to hear of your experience.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Hi I have OCD contamination and toenail fungus. It's so hard to have the conditions together. I tried to console my mind and looked online and found out about dermatophytes. The fungi that can cause toenail fungus. It has made me maybe even feel worse. These dermatophytes if you have toenail fungus can be in your home maybe in dust too. I'm a senior and I isolate myself. Any thoughts?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Anyone ever say forget it, it's not going anywhere anyway and just put polish on or a fake nail just so you can wear flip flops or sandals? I know they say it makes it worse, but this feels like a life sentence. I need my toes out, and that's not cute.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "I have fought and learned to live with toenail fungus for 15 years. If it's easy enough to contract it at the gym or the pool, why haven't my husband or kids caught it? Is this the case with any of you?",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    # === CORRECT TOES SEARCH - Bunion Support Group ===
    {
        "body": "What are your thoughts? Haven't had surgery just yet as it's my last option. Went to physical therapy and therapist recommended the HOKA shoes and Bunion Relief and Toe Corrector. What are your thoughts? I really don't want to have to get surgery.",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
    {
        "body": "Dear lovely friends, please can I ask your advice? I am scheduled to have a meeting with a new surgeon who is an expert in the field. He wants to do revision surgery. The first surgery I had on the NHS went wrong because the surgeon did not correct the hammer toes and also left a big toe floating in the air and pressing pretty hard against the second toe. I am therefore now in more pain than I was before the first surgery.",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
    {
        "body": "Does anyone have a good website to buy the Correct Toes Stable Toes? The official website is charging crazy postage and Yoga Matters is out of stock! I'm desperate to get something else as my silicone ones have started to hurt my poor second toe. Yes, I'm already wearing Altra and Topo, sized up in mens and looking like a hobbit.",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
    {
        "body": "Hi all, can anyone recommend a corrector or toe separator that can help? Can now feel my big toe pushing the other toes. I've been referred for surgery but in meantime wondering if there's a reputable product to help?",
        "source_group": "Bunion Support Group",
        "comments": [],
    },
    # === SHOCKWAVE SEARCH - PF group ===
    {
        "body": "Dr. Staschiak explains Regular Shockwave Therapy vs High Intensity SWT. Very informative comparison of the two different approaches to shockwave treatment for plantar fasciitis.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Hi I've been told by hospital doctor I need shock wave therapy on my feet and has referred me to Physio for shockwave therapy, but Physio from my local hospital don't do it, no machine. Does anybody know if any Hospital in Scotland does it? Doctor says they're not doing steroid injections anymore as it destroys the fat in the foot.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "Shockwave differences: Choose RSWT for acute or general plantar fasciitis cases. Choose FSWT for long-term chronic, recalcitrant, or calcific plantar fasciitis that requires deeper, targeted treatment.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "I had my first shockwave treatment on my left heel but it didn't hurt at all. I was under the impression that shockwave hurts. Has anyone else had it not hurt? Even my podiatrist was surprised. Has shockwave helped cure your PF?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    {
        "body": "When cortisone finally stopped working I went with the next best thing. Had my first shockwave treatment today. He said I will probably need 4-5 treatments. Obviously we hope this works. If it doesn't I can opt for plasma injections or surgery. I can use my own plasma but he has much better success with immature plasma extracted from umbilical cords. One day at a time.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "comments": [],
    },
    # === TEA TREE OIL SEARCH - Toenail Fungus group ===
    {
        "body": "I'm on oral medicine terbinafine and decided to get myself some things on Amazon. Foot soak epsom salts, Listerine, Anti fungal wash, Tea tree oil for my toenail fungus treatment routine.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "After trying iodine, tea tree oil, niacinamide, Vicks vapor rub, cloves, peroxide, vinegar, OTC creams and nail repair, emuaidMax with metallic silver, Listerine... I found a cure on accident.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "I give up. I'm just going to use nail polish with tea tree oil in it. I've been using prescription and also over the counter treatments for over a year. No help. I can't afford to go have all my nails lasered.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "I've battled with my toenail fungus for 20 years, trying various topical over the counter medications, curanail, scholl. They did not work. I tried soaking them in epsom salts, applying tea tree oil, which did improve them but not destroy the fungus permanently. I tried imperial feet as it was highlighted rated on amazon, that just made the nails soft to cut it back, again not killing the fungus. I then tried laser treatment, which was expensive, but came highly rated to cure toenail fungus. I had high hopes but it did not work. I finally had success in February 2025. I went to my doctors and got prescribed antifungal terbinafine tablets, 1 a day for 3 months, it's taken a few more months for the nails to fully regrow but I'm now toenail fungus free.",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    {
        "body": "Has anyone ever used tea tree oil and oregano oil for toenail fungus? And did it work? I'm desperate for a solution that works!",
        "source_group": "Toenail Fungus Support & Management",
        "comments": [],
    },
    # === HALLUX RIGIDUS SEARCH - Forefoot Forum ===
    {
        "body": "Hi everyone. Former athlete here. At the age of 20, I started experiencing pain in my right big toe, and around the same time I developed chronic muscle tightness in my calves. Over the years, this tightness gradually spread to my thighs, glutes, and lower back. After an MRI evaluation, it was found that I have very advanced cartilage degeneration (hallux rigidus) in my right big toe joint, while my left foot shows no structural issues at all. After many years of conservative treatments, I'm now considering first MTP joint fusion surgery, together with proper gait rehabilitation.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
    {
        "body": "I have bunions and hallux rigidus on both feet. That makes me need a very large toebox for a wide and sensitive forefoot but the rest of my foot is just a medium. I'm a hiker and it's very hard for me to find a comfortable hiking boot. I've tried Keens, Merrells, Altra, I even tried Hanwag, which advertises itself as the bunion shoe. Does anyone have any recommendations? Oh, I also tried Orthofeet and that one wasn't comfortable either.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
    {
        "body": "Hello people, I think I'm in the early stages of hallux valgus. Runs in family. I walk/jog everyday which is triggering or speeding it. Anything I can do to move my toe back naturally?",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
    {
        "body": "Hi all. I have had Hallux limitus for about a year now. I dropped something on my toe, the pain never left, and I got my diagnosis. As I'm sure most of you are, I'm super frustrated. I asked my orthopedic doctor if I could get a cheilectomy, but he says I'm in a gray area. I really don't see the point in letting this get worse. I have lots of mobility in my toe. Has anyone had a cheilectomy while in a gray area? Did it help?",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "comments": [],
    },
]

# Auto-detection lists
conditions_list = {
    'bunion': ['bunion', 'bunions'],
    'hammer toe': ['hammer toe', 'hammertoe', 'hammer toes'],
    'hallux valgus': ['hallux valgus'],
    'hallux limitus': ['hallux limitus'],
    'hallux rigidus': ['hallux rigidus'],
    "tailor's bunion": ["tailor's bunion", 'tailors bunion', "tailor bunion"],
    'bunionette': ['bunionette'],
    'plantar fasciitis': ['plantar fasciitis', 'plantar fascilitis', 'pf'],
    'heel spur': ['heel spur', 'heel spurs'],
    'flat feet': ['flat feet', 'flat foot', 'fallen arch'],
    'toenail fungus': ['toenail fungus', 'fungal nail', 'nail fungus', 'fungus'],
    'ingrown toenail': ['ingrown toenail'],
    'metatarsalgia': ['metatarsalgia', 'metatarsal'],
    'neuroma': ['neuroma', "morton's neuroma", 'mortons neuroma'],
    'sesamoiditis': ['sesamoiditis'],
    'gout': ['gout'],
    'arthritis': ['arthritis'],
    'bone spur': ['bone spur'],
    'callus': ['callus'],
    'corn': ['corn'],
    'blister': ['blister'],
    'neuropathy': ['neuropathy'],
    'edema': ['edema'],
    'tendonitis': ['tendonitis', 'tendinitis'],
    'plantar plate tear': ['plantar plate'],
}

surgery_types_list = {
    'MIS': ['mis ', 'minimally invasive'],
    'Lapiplasty': ['lapiplasty'],
    'scarf akin': ['scarf akin'],
    'osteotomy': ['osteotomy'],
    'chevron': ['chevron'],
    'Austin': ['austin procedure'],
    'arthroplasty': ['arthroplasty'],
    'arthrodesis': ['arthrodesis'],
    'bunionectomy': ['bunionectomy'],
    'toe fusion': ['toe fusion', 'fusion surgery', 'joint fusion', 'big toe fusion', 'hammertoe fusion'],
    'MICA': ['mica'],
    'percutaneous': ['percutaneous'],
    'cheilectomy': ['cheilectomy', 'chielectomy'],
}

products_list = {
    'Hoka': ['hoka'],
    'Orthofeet': ['orthofeet', 'ortho feet'],
    'New Balance': ['new balance'],
    'Skechers': ['skechers'],
    'Brooks': ['brooks'],
    'Nike': ['nike'],
    'Asics': ['asics'],
    'Birkenstock': ['birkenstock'],
    'Vionic': ['vionic'],
    'Oofos': ['oofos', 'oofoo'],
    'Crocs': ['crocs'],
    'Correct Toes': ['correct toes'],
    'Yoga Toes': ['yoga toes'],
    "Dr. Scholl's": ["dr. scholl", "dr scholl"],
    'Superfeet': ['superfeet'],
    'Powerstep': ['powerstep'],
    'KT Tape': ['kt tape'],
    'Voltaren': ['voltaren'],
    'Biofreeze': ['biofreeze'],
    'Vicks': ['vicks'],
    'Lamisil': ['lamisil'],
    'Jublia': ['jublia'],
    'Kerasal': ['kerasal'],
    'Altra': ['altra'],
    'Teva': ['teva'],
    'Kuru': ['kuru'],
    'Topo': ['topo'],
}

treatments_list = {
    'surgery': ['surgery', 'surgical'],
    'physical therapy': ['physical therapy', 'pt '],
    'cortisone': ['cortisone', 'cortison'],
    'steroid injection': ['steroid injection', 'steroid shot'],
    'orthotics': ['orthotic', 'insole', 'inserts'],
    'taping': ['taping'],
    'icing': ['icing', 'ice it', 'ice pack', 'frozen water bottle'],
    'elevation': ['elevat'],
    'stretching': ['stretch'],
    'massage': ['massage'],
    'shockwave therapy': ['shockwave', 'shock wave'],
    'laser therapy': ['laser treatment', 'laser therapy'],
    'anti-inflammatory': ['anti-inflammatory', 'anti inflammatory'],
    'ibuprofen': ['ibuprofen'],
    'gabapentin': ['gabapentin'],
    'custom orthotics': ['custom orthotic'],
    'terbinafine': ['terbinafine'],
    'tea tree oil': ['tea tree oil'],
    'night splint': ['night splint'],
    'arch support': ['arch support'],
    'rolling': ['rolling'],
}

def detect(body_lower, detection_dict):
    found = []
    for key, keywords in detection_dict.items():
        for kw in keywords:
            if kw in body_lower:
                found.append(key)
                break
    return found

new_count = 0
for post in new_raw_posts:
    fp = post['body'][:80].lower().strip()
    if fp in existing_fingerprints:
        continue
    
    max_id += 1
    body_lower = post['body'].lower()
    
    new_post = {
        "id": max_id,
        "body": post['body'],
        "author": None,
        "url": None,
        "source_group": post['source_group'],
        "date_captured": today,
        "conditions_mentioned": detect(body_lower, conditions_list),
        "surgery_types_mentioned": detect(body_lower, surgery_types_list),
        "treatments_mentioned": detect(body_lower, treatments_list),
        "products_mentioned": detect(body_lower, products_list),
        "comments": post.get('comments', []),
        "images": []
    }
    
    existing_posts.append(new_post)
    existing_fingerprints.add(fp)
    new_count += 1
    print(f"  Added post {max_id}: {post['body'][:60]}...")

print(f"\nNew posts added: {new_count}")
print(f"Total posts now: {len(existing_posts)}")

# Save
with open('/tmp/fixfeetfast/posts.json', 'w') as f:
    json.dump(existing_posts, f, indent=2)

print("posts.json saved successfully")
