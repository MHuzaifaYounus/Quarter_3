from fastapi import FastAPI  # type: ignore
import random
app = FastAPI()

quranic_ayats = {
    "happy": [
        "So remember Me; I will remember you. And be grateful to Me and do not deny Me. (2:152)",
        "If you are grateful, I will certainly give you more. (14:7)",
        "And We have certainly created man in the best of stature. (95:4)",
        "Indeed, with hardship comes ease. (94:6)",
        "Say, ‘In the bounty of Allah and in His mercy – in that let them rejoice; it is better than what they accumulate.’ (10:58)",
        "Whoever does righteousness, whether male or female, while being a believer – We will surely cause him to live a good life. (16:97)",
        "Allah does not intend to make difficulty for you, but He intends to purify you and complete His favor upon you that you may be grateful. (5:6)",
        "And they will say, ‘Praise be to Allah, who has removed from us [all] sorrow. Indeed, our Lord is Forgiving and Appreciative.’ (35:34)",
        "And We will have removed whatever is within their breasts of resentment, [while] flowing beneath them are rivers. And they will say, ‘Praise be to Allah, who has guided us to this.’ (7:43)",
        "They will have whatever they wish therein, and with Us is more. (50:35)",
        "For them are good tidings in the worldly life and in the Hereafter. (10:64)",
        "And your Lord is the Forgiving, Full of Mercy. If He were to impose blame upon them for what they earned, He would have hastened for them the punishment. (18:58)",
        "Indeed, those who have said, ‘Our Lord is Allah’ and then remained steadfast – the angels will descend upon them [saying], ‘Do not fear and do not grieve but receive good tidings of Paradise, which you were promised.’ (41:30)",
        "For them are the gardens of perpetual residence beneath which rivers flow, wherein they will abide eternally. (9:72)",
        "And they will be given to drink a cup [of wine] whose mixture is of ginger. (76:17)"
    ],
    "sad": [
        "Do not grieve; indeed, Allah is with us. (9:40)",
        "Verily, with every difficulty, there is relief. (94:6)",
        "And when My servants ask you concerning Me, indeed I am near. (2:186)",
        "And We will surely test you with something of fear and hunger and a loss of wealth, lives, and fruits, but give good tidings to the patient. (2:155)",
        "And despair not of relief from Allah. Indeed, no one despairs of relief from Allah except the disbelieving people. (12:87)",
        "Perhaps Allah will put, between you and those to whom you have been enemies, affection. And Allah is competent, and Allah is Forgiving and Merciful. (60:7)",
        "And We have not sent you, [O Muhammad], except as a mercy to the worlds. (21:107)",
        "And be patient, for indeed, Allah does not allow to be lost the reward of those who do good. (11:115)",
        "No disaster strikes except by permission of Allah. And whoever believes in Allah – He will guide his heart. (64:11)",
        "And whoever fears Allah – He will make for him a way out. (65:2)",
        "They said, ‘Upon Allah do we rely. Our Lord, make us not [objects of] trial for the wrongdoing people.’ (10:85)",
        "Say, ‘Never will we be struck except by what Allah has decreed for us; He is our protector.’ (9:51)",
        "And they will say, ‘Praise be to Allah, who has removed from us [all] sorrow. Indeed, our Lord is Forgiving and Appreciative.’ (35:34)",
        "Indeed, the patient will be given their reward without account. (39:10)",
        "And never think of those who have been killed in the cause of Allah as dead. Rather, they are alive with their Lord, receiving provision. (3:169)"
    ],
    "anxiety": [
        "And whoever fears Allah – He will make for him a way out. (65:2)",
        "Allah does not burden a soul beyond that it can bear. (2:286)",
        "Indeed, it is in the remembrance of Allah that hearts find peace. (13:28)",
        "But they plan, and Allah plans. And Allah is the best of planners. (8:30)",
        "So do not weaken and do not grieve, and you will be superior if you are [true] believers. (3:139)",
        "Unquestionably, by the remembrance of Allah hearts are assured. (13:28)",
        "And rely upon Allah; and sufficient is Allah as Disposer of affairs. (33:3)",
        "Do not grieve. Indeed, Allah is with us. (9:40)",
        "And be patient, for indeed, Allah does not allow to be lost the reward of those who do good. (11:115)",
        "Indeed, the patient will be given their reward without account. (39:10)",
        "And never say of anything, ‘Indeed, I will do that tomorrow,’ except [when adding], ‘If Allah wills.’ (18:23-24)",
        "And We will surely test you until We make evident those who strive among you and the patient. (47:31)",
        "And put your trust in Allah. And sufficient is Allah as Disposer of affairs. (33:3)",
        "And whoever relies upon Allah – then He is sufficient for him. (65:3)",
        "And your Lord has not forsaken you, nor has He become displeased. (93:3)"
    ],
    "hope": [
        "And whoever puts his trust in Allah, then He will suffice him. (65:3)",
        "Do not lose hope, nor be sad. (3:139)",
        "For indeed, with hardship [will be] ease. (94:5)",
        "Your Lord has not forsaken you, nor has He become displeased. (93:3)",
        "Say, ‘O My servants who have transgressed against themselves [by sinning], do not despair of the mercy of Allah. Indeed, Allah forgives all sins.’ (39:53)",
        "And We will surely give those who were patient their reward according to the best of what they used to do. (16:96)",
        "Indeed, those who have said, ‘Our Lord is Allah’ and then remained steadfast – the angels will descend upon them [saying], ‘Do not fear and do not grieve but receive good tidings of Paradise, which you were promised.’ (41:30)",
        "For them are the gardens of perpetual residence beneath which rivers flow, wherein they will abide eternally. (9:72)",
        "And they will be given to drink a cup [of wine] whose mixture is of ginger. (76:17)",
        "And never say of anything, ‘Indeed, I will do that tomorrow,’ except [when adding], ‘If Allah wills.’ (18:23-24)",
        "And whoever fears Allah – He will make for him a way out. (65:2)",
        "And be patient, for indeed, Allah does not allow to be lost the reward of those who do good. (11:115)",
        "Indeed, the patient will be given their reward without account. (39:10)",
        "And your Lord is the Forgiving, Full of Mercy. If He were to impose blame upon them for what they earned, He would have hastened for them the punishment. (18:58)",
        "And We have certainly created man in the best of stature. (95:4)"
    ],
    "patience" :[
    "And seek help through patience and prayer, and indeed, it is difficult except for the humbly submissive [to Allah]. (2:45)",
    "O you who have believed, seek help through patience and prayer. Indeed, Allah is with the patient. (2:153)",
    "And We will surely test you with something of fear and hunger and a loss of wealth, lives, and fruits, but give good tidings to the patient. (2:155)",
    "Indeed, the patient will be given their reward without account. (39:10)",
    "And be patient, for indeed, Allah does not allow to be lost the reward of those who do good. (11:115)",
    "And be patient, for the promise of Allah is truth, and ask forgiveness for your sin and exalt [Allah] with praise of your Lord in the evening and the morning. (40:55)",
    "And We made from among them leaders guiding by Our command when they were patient and [when] they were certain of Our signs. (32:24)",
    "So be patient with gracious patience. (70:5)",
    "And obey Allah and His Messenger and do not dispute and [thus] lose courage and [then] your strength would depart, and be patient. Indeed, Allah is with the patient. (8:46)",
    "And endure patiently, for your endurance is only through Allah. And do not grieve over them and do not be in distress over what they conspire. (16:127)",
    "And those who are patient, seeking the countenance of their Lord, and establish prayer and spend from what We have provided for them secretly and publicly and prevent evil with good – those will have the good consequence of [this] home. (13:22)",
    "And be patient, [O Muhammad], and your patience is not but through Allah. And do not grieve over them and do not be in distress over what they conspire. (16:127)",
    "But if you endure patiently, it is better for those who are patient. (16:126)",
    "And We made them leaders guiding by Our command when they were patient and [when] they were certain of Our signs. (32:24)",
    "So be patient. Indeed, the promise of Allah is truth. And do not let those who have no certainty make you impatient. (30:60)"
],
    "forgiveness_ayats" :[
    "And let them pardon and overlook. Would you not like that Allah should forgive you? And Allah is Forgiving and Merciful. (24:22)",
    "But if you pardon and overlook and forgive – then indeed, Allah is Forgiving and Merciful. (64:14)",
    "And He it is who accepts repentance from His servants and pardons misdeeds, and He knows what you do. (42:25)",
    "And who forgive people; and Allah loves the doers of good. (3:134)",
    "Indeed, Allah loves those who constantly repent and loves those who purify themselves. (2:222)",
    "And whoever forgives and makes reconciliation, his reward is [due] from Allah. Indeed, He does not like the wrongdoers. (42:40)",
    "The good deed and the bad deed are not equal. Repel [evil] by that [deed] which is better; and thereupon the one whom between you and him is enmity will become as though he was a devoted friend. (41:34)",
    "Indeed, the mercy of Allah is near to the doers of good. (7:56)",
    "And My Mercy encompasses all things. (7:156)",
    "Say, 'O My servants who have transgressed against themselves [by sinning], do not despair of the mercy of Allah. Indeed, Allah forgives all sins. Indeed, it is He who is the Forgiving, the Merciful.' (39:53)",
    "And turn to Allah in repentance, all of you, O believers, that you might succeed. (24:31)",
    "Except those who repent and believe and do righteous work; for them Allah will replace their evil deeds with good. And ever is Allah Forgiving and Merciful. (25:70)",
    "Indeed, Allah is Pardoning and Forgiving. (4:99)",
    "And if you punish [an enemy], punish with an equivalent of that with which you were harmed. But if you are patient – it is better for those who are patient. (16:126)",
    "Indeed, Allah is with those who fear Him and those who are doers of good. (16:128)"
],

"love" :[
    "And He is the Forgiving, the Loving. (85:14)",
    "Indeed, those who have believed and done righteous deeds – the Most Merciful will appoint for them affection. (19:96)",
    "Indeed, Allah loves those who rely upon Him. (3:159)",
    "Indeed, Allah loves the righteous [who fear Him]. (9:4)",
    "And do good; indeed, Allah loves the doers of good. (2:195)",
    "Indeed, Allah loves those who act justly. (5:42)",
    "Indeed, Allah loves those who purify themselves. (2:222)",
    "And those who believe are stronger in love for Allah. (2:165)",
    "Indeed, Allah loves the steadfast. (3:146)",
    "And lower to them the wing of humility out of mercy and say, 'My Lord, have mercy upon them as they brought me up [when I was] small.' (17:24)",
    "Indeed, Allah loves those who fight in His cause in a row as though they are a [single] structure joined firmly. (61:4)",
    "Indeed, Allah does not love the wrongdoers. (3:140)",
    "Indeed, Allah does not love those who are arrogant and boastful. (4:36)",
    "Indeed, Allah does not like corruption. (2:205)",
    "Indeed, Allah is full of kindness to the people. (2:143)"
],

"strength" :[
    "And rely upon Allah; and sufficient is Allah as Disposer of affairs. (33:3)",
    "And seek help through patience and prayer. (2:153)",
    "So be patient. Indeed, the promise of Allah is truth. (30:60)",
    "And do not weaken and do not grieve, and you will be superior if you are [true] believers. (3:139)",
    "Indeed, Allah does not burden a soul beyond that it can bear. (2:286)",
    "And whoever fears Allah – He will make for him a way out. (65:2)",
    "And whoever relies upon Allah – then He is sufficient for him. (65:3)",
    "Indeed, with hardship comes ease. (94:6)",
    "And remember Allah often that you may succeed. (62:10)",
    "So be patient over what they say and exalt [Allah] with praise of your Lord before the rising of the sun and before its setting. (50:39)",
    "And those who strive for Us – We will surely guide them to Our ways. (29:69)",
    "Indeed, Allah is with the patient. (2:153)",
    "And whoever puts his trust in Allah, He will suffice him. (65:3)",
    "Say, 'Nothing will ever befall us except what Allah has decreed for us; He is our protector.' (9:51)",
    "And establish prayer and give zakah and bow with those who bow [in worship and obedience]. (2:43)"
],
"justice" :[
    "Indeed, Allah commands you to render trusts to whom they are due and when you judge between people to judge with justice. (4:58)",
    "And establish weight in justice and do not make deficient the balance. (55:9)",
    "O you who have believed, be persistently standing firm for Allah, witnesses in justice. (5:8)",
    "And do not let the hatred of a people prevent you from being just. Be just; that is nearer to righteousness. (5:8)",
    "Indeed, Allah loves those who act justly. (5:42)",
    "And establish the testimony for the sake of Allah. (65:2)",
    "And if you judge, judge between them with justice. Indeed, Allah loves those who act justly. (5:42)",
    "And do not deprive people of their due and do not commit abuse on the earth, spreading corruption. (26:183)",
    "Indeed, Allah commands justice, good conduct, and giving to relatives and forbids immorality, bad conduct, and oppression. (16:90)",
    "And let not hatred of a people prevent you from being just. (5:8)",
    "And whoever does a wrong or wrongs himself but then seeks forgiveness of Allah will find Allah Forgiving and Merciful. (4:110)",
    "And establish justice even if it be against yourselves or parents and relatives. (4:135)",
    "And give full measure and weight in justice. (6:152)",
    "And if you give your word, be just, even if it concerns a near relative. (6:152)",
    "Indeed, Allah does not wrong the people at all, but it is the people who are wronging themselves. (10:44)"
],

"gratitude" :[
    "And [remember] when your Lord proclaimed, 'If you are grateful, I will surely increase you [in favor]; but if you deny, indeed, My punishment is severe.' (14:7)",
    "So remember Me; I will remember you. And be grateful to Me and do not deny Me. (2:152)",
    "And be grateful for the favor of Allah, if it is [indeed] Him that you worship. (16:114)",
    "And whoever is grateful, he is only grateful for [the benefit of] himself. And whoever denies [His favor] – then indeed, Allah is Free of need and Praiseworthy. (31:12)",
    "Indeed, We guided him to the way, be he grateful or be he ungrateful. (76:3)",
    "And few of My servants are grateful. (34:13)",
    "And whatever you have of favor – it is from Allah. (16:53)",
    "Why should Allah punish you if you are grateful and believe? And ever is Allah Appreciative and Knowing. (4:147)",
    "Indeed, Allah is full of bounty to the people, but most of the people do not show gratitude. (2:243)",
    "Then eat of what Allah has provided for you [which is] lawful and good. And be grateful for the favor of Allah, if it is [indeed] Him that you worship. (16:114)",
    "Indeed, your efforts are appreciated. (76:22)",
    "And whoever desires the reward of this world – We will give him thereof; and whoever desires the reward of the Hereafter – We will give him thereof. And We will reward the grateful. (3:145)",
    "And those who believe and do righteous deeds – We will surely remove from them their misdeeds and will surely reward them according to the best of what they used to do. (29:7)",
    "Then remember Me; I will remember you. Be grateful to Me and do not reject Me. (2:152)",
    "Indeed, the patient and the grateful will have a great reward. (42:23)"
],

"guidance" :[
    "This is the Book about which there is no doubt, a guidance for those conscious of Allah. (2:2)",
    "Indeed, this Qur'an guides to that which is most upright. (17:9)",
    "And Allah increases those who were guided, in guidance. (19:76)",
    "And whoever holds firmly to Allah has certainly been guided to a straight path. (3:101)",
    "And whoever is guided is only guided for [the benefit of] himself. (27:92)",
    "And whoever Allah guides – he is the [rightly] guided; and whoever He sends astray – it is those who will be the losers. (7:178)",
    "And We have certainly made the Qur'an easy for remembrance, so is there any who will remember? (54:17)",
    "Say, 'Indeed, the [true] guidance is the guidance of Allah.' (3:73)",
    "And whoever Allah guides – there is no one to misguide him. (39:37)",
    "And whoever follows My guidance will neither go astray [in the world] nor suffer [in the Hereafter]. (20:123)",
    "And We have certainly sent down to you distinct verses and examples from those who passed away before you and an admonition for the righteous. (24:34)",
    "Indeed, We sent it down as an Arabic Qur'an that you might understand. (12:2)",
    "And those who strive for Us – We will surely guide them to Our ways. (29:69)",
    "And We guided them to the straight path. (37:118)",
    "And indeed, you guide to a straight path. (42:52)"
]


}

@app.get("/")
def get_ayats(mood:str):
    """Return a random ayat"""
    if mood not in list(quranic_ayats.keys()):
        return {"Error":f"Select a mood from this list {list(quranic_ayats.keys())}"}
        
    return {"ayat":random.choice(quranic_ayats[mood])}

    
