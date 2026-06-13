# -*- coding: utf-8 -*-
"""Dados completos das 78 figurinhas — Heróis da Fé: Álbum de Seleções."""

STYLE=("Pixar / Disney / DreamWorks animated-movie style: clearly cartoon and stylized, smooth stylized skin, "
   "big friendly expressive eyes, soft rounded features, warm friendly expression. Upper-body bust, centered, facing camera. "
   "Soft cinematic lighting, rich vivid colors, wholesome. NOT photorealistic, not a real person, not a photograph. "
   "Vertical portrait. No text, no letters, no words, no numbers, no watermark, no frame, no border. High quality, crisp.")

def player_prompt(detail,jersey,emblem,bg):
    return (f"A stylized 3D animated cartoon character portrait of {detail}. "
            f"Wearing a plain {jersey} sports team jersey with a small {emblem} emblem on the chest. {STYLE} "
            f"Plain solid deep {bg} gradient background with a soft radial glow behind the character.")

def crest_prompt(theme,colors,symbols):
    return (f"A clean modern sports team crest emblem for a kids Bible collection, themed '{theme}'. "
            f"Shield-shaped badge, bold and simple, vivid saturated {colors} colors, with iconic symbols: {symbols}. "
            f"Friendly, wholesome, child-friendly, flat vector logo style with subtle 3D depth, thick clean outlines, glossy finish. "
            f"Centered emblem only, no mascot character. Plain solid white background. Square 1:1. "
            f"No text, no letters, no words, no watermark.")

# tc = cor da moldura/vidro ; tcd = cor escura da placa
TEAMS=[
 {"name":"Patriarcas FC","theme":"The Patriarchs","tc":(150,110,70),"tcd":(74,52,30),
  "jersey":"earthy brown and gold","bg":"warm brown","emblem":"a small golden star",
  "colors":"brown and gold","symbols":"stars and a tent",
  "players":[
   ("Adão","Adam, the first man","Gênesis","Gênesis 1:27","O Primeiro Homem"),
   ("Eva","Eve, the first woman","Gênesis","Gênesis 3:20","A Primeira Mãe"),
   ("Noé","Noah holding a small wooden ark","Gênesis","Gênesis 6:9","O Construtor"),
   ("Abraão","Abraham, an old man with a long white beard","Gênesis","Gênesis 15:6","O Pai da Fé"),
   ("Sara","Sarah, a kind elderly woman","Gênesis","Gênesis 18:14","A Mãe das Nações"),
   ("Isaque","Isaac, a gentle young man","Gênesis","Gênesis 26:24","O Filho da Promessa")]},
 {"name":"Família da Promessa","theme":"Family of Promise","tc":(80,150,90),"tcd":(28,72,40),
  "jersey":"green","bg":"green","emblem":"a small ladder","colors":"green","symbols":"a ladder and twelve stars",
  "players":[
   ("Jacó","Jacob, a young shepherd","Gênesis","Gênesis 28:15","O Lutador"),
   ("Rebeca","Rebecca, a kind young woman with a water jar","Gênesis","Gênesis 24:67","A Decidida"),
   ("Raquel","Rachel, a gentle young shepherdess","Gênesis","Gênesis 29:18","A Amada"),
   ("José","Joseph wearing a colorful coat of many colors","Gênesis","Gênesis 37:3","O Sonhador"),
   ("Judá","Judah, a strong brave young man","Gênesis","Gênesis 49:9","O Leão"),
   ("Benjamim","Benjamin, a cheerful young boy","Gênesis","Gênesis 35:24","O Caçula")]},
 {"name":"Libertadores do Egito","theme":"Out of Egypt","tc":(66,110,184),"tcd":(26,50,100),
  "jersey":"royal blue","bg":"royal blue","emblem":"a small wooden staff","colors":"royal blue","symbols":"a wooden staff and stone tablets",
  "players":[
   ("Moisés","Moses holding a wooden staff","Êxodo","Êxodo 14:21","O Libertador"),
   ("Arão","Aaron the priest holding a budding rod","Êxodo","Êxodo 4:14","A Voz"),
   ("Miriam","Miriam holding a tambourine","Êxodo","Êxodo 15:20","A Cantora"),
   ("Josué","Joshua, a brave young soldier holding up a golden trumpet, no horns on his head","Josué","Josué 1:9","O General"),
   ("Calebe","Caleb, a brave explorer holding grapes","Números","Números 13:30","O Explorador"),
   ("Raabe","Rahab, a kind young woman holding a red cord","Josué","Josué 2:21","A Corajosa")]},
 {"name":"Juízes & Guerreiros","theme":"Judges and Warriors","tc":(192,72,60),"tcd":(96,28,24),
  "jersey":"red","bg":"red","emblem":"a small shield","colors":"red","symbols":"a shield and a torch",
  "players":[
   ("Gideão","Gideon, a young soldier holding a torch","Juízes","Juízes 6:12","O Valente"),
   ("Sansão","Samson, a strong young man with long hair","Juízes","Juízes 16:28","O Forte"),
   ("Débora","Deborah, a wise woman judge","Juízes","Juízes 4:4","A Juíza Sábia"),
   ("Baraque","Barak, a brave commander","Juízes","Juízes 4:14","O Comandante"),
   ("Rute","Ruth, a kind young woman holding wheat","Rute","Rute 1:16","A Fiel"),
   ("Boaz","Boaz, a kind strong farmer","Rute","Rute 2:1","O Protetor")]},
 {"name":"Reis de Israel","theme":"Kings of Israel","tc":(120,78,168),"tcd":(58,32,92),
  "jersey":"royal purple","bg":"royal purple","emblem":"a golden crown","colors":"royal purple and gold","symbols":"a golden crown, a harp and a shining star",
  "players":[
   ("Samuel","young prophet Samuel holding an oil lamp","1 Samuel","1 Samuel 3:10","O Profeta-Menino"),
   ("Saul","King Saul, a tall king with a simple golden crown","1 Samuel","1 Samuel 10:1","O Primeiro Rei"),
   ("Jônatas","Jonathan, a brave young prince with a bow","1 Samuel","1 Samuel 18:3","O Amigo Leal"),
   ("Davi","young King David holding a sling and a small harp","1 Samuel","1 Samuel 16:7","O Rei Corajoso"),
   ("Salomão","King Solomon, a wise young king with a crown and scroll","1 Reis","1 Reis 3:9","O Rei Sábio"),
   ("Ester","Queen Esther, a kind young queen with a crown","Ester","Ester 4:14","A Rainha Corajosa")]},
 {"name":"Os Profetas","theme":"The Prophets","tc":(222,132,52),"tcd":(120,64,20),
  "jersey":"orange","bg":"orange","emblem":"a small flame","colors":"orange and red","symbols":"a flame and a scroll",
  "players":[
   ("Elias","Elijah, a prophet with a small flame and a raven","1 Reis","1 Reis 18:36","O Profeta de Fogo"),
   ("Eliseu","Elisha, a kind prophet holding a cloak","2 Reis","2 Reis 2:9","O Sucessor"),
   ("Isaías","Isaiah, a wise prophet holding a scroll","Isaías","Isaías 6:8","O Anunciador"),
   ("Jeremias","Jeremiah, a young prophet","Jeremias","Jeremias 1:5","O Corajoso"),
   ("Daniel","Daniel praying calmly with a friendly lion","Daniel","Daniel 6:22","O Sem Medo"),
   ("Jonas","Jonah beside a friendly big whale","Jonas","Jonas 2:1","O Recomeço")]},
 {"name":"O Nascimento","theme":"The Nativity","tc":(90,150,200),"tcd":(40,80,130),
  "jersey":"light blue and white","bg":"light blue","emblem":"a small star","colors":"light blue and white","symbols":"the star of Bethlehem and a manger",
  "players":[
   ("Maria","Mary, a gentle young woman in a soft blue veil","Lucas","Lucas 1:38","A Mãe"),
   ("José de Nazaré","Joseph of Nazareth, a gentle young carpenter","Mateus","Mateus 1:20","O Carpinteiro"),
   ("João Batista","John the Baptist by a river in a simple robe","João","João 1:23","O Mensageiro"),
   ("Isabel","Elizabeth, a kind older woman","Lucas","Lucas 1:42","A Bendita"),
   ("Zacarias","Zechariah, an old kind priest","Lucas","Lucas 1:13","O Sacerdote"),
   ("Gabriel","the angel Gabriel with gentle wings and a soft glow","Lucas","Lucas 1:19","O Anjo Mensageiro")]},
 {"name":"Jesus & os Apóstolos","theme":"Jesus and the Apostles","tc":(214,176,92),"tcd":(120,88,30),
  "jersey":"gold and white","bg":"gold","emblem":"a white lamb","colors":"gold and white","symbols":"a lamb and a crown of light",
  "players":[
   ("Jesus","Jesus, kind with a warm gentle smile","João","João 3:16","O Salvador"),
   ("Pedro","the apostle Peter, a fisherman with a short beard holding a net","Mateus","Mateus 16:18","A Pedra"),
   ("André","the apostle Andrew, a friendly fisherman","João","João 1:40","O Primeiro Chamado"),
   ("João","the apostle John, a kind young man","João","João 13:23","O Amado"),
   ("Tiago","the apostle James, a friendly bearded man","Marcos","Marcos 1:19","Filho do Trovão"),
   ("Mateus","the apostle Matthew holding a scroll","Mateus","Mateus 9:9","O Escritor"),
   ("Filipe","the apostle Philip, a friendly young man","João","João 1:43","O Apóstolo"),
   ("Bartolomeu","the apostle Bartholomew, a kind honest man","João","João 1:49","O Sincero"),
   ("Tomé","the apostle Thomas, a thoughtful young man","João","João 20:28","O Que Creu"),
   ("Tiago Menor","the apostle James son of Alphaeus, a gentle young man","Marcos","Marcos 3:18","O Apóstolo"),
   ("Tadeu","the apostle Thaddaeus, a friendly man","Lucas","Lucas 6:16","O Apóstolo"),
   ("Simão","the apostle Simon the Zealot, a passionate young man","Lucas","Lucas 6:15","O Zeloso"),
   ("Matias","the apostle Matthias, a faithful young man","Atos","Atos 1:26","O Escolhido"),
   ("Judas Iscariotes","the apostle Judas Iscariot, a sorrowful regretful man","Mateus","Mateus 26:15","O Traidor")]},
]

def legend_prompt(detail):
    return (f"A premium legendary GOLD portrait of {detail}, as a stylized 3D animated cartoon character. "
            f"Close-up upper-body bust, the character is LARGE and FILLS the entire frame, full-bleed, centered. "
            f"Pixar / Disney animated-movie style: clearly cartoon and stylized, smooth stylized skin, big friendly expressive eyes. "
            f"NOT photorealistic, not a real person, not a photograph. "
            f"Dramatic golden rim lighting, radiant glowing gold and amber background filling the whole image edge to edge, soft light rays and sparkles, "
            f"holographic premium foil feel, inspiring and reverent, wholesome. Vertical portrait. "
            f"No card, no card frame, no white border, no margins, no text, no letters, no words, no numbers, no watermark, no frame, no border. High quality, crisp.")

# num, nome, detalhe(en), livro/ref, papel
LEGENDS=[
 (65,"Abraão","Abraham, an old man with a long white beard, holding a staff and looking at the stars","Gênesis 22:18","Lenda da Fé",False),
 (66,"José","Joseph wearing a colorful coat of many colors","Gênesis 50:20","Lenda do Perdão",False),
 (67,"Moisés","Moses holding a wooden staff and stone tablets","Êxodo 14:21","Lenda da Liberdade",False),
 (68,"Davi","young King David holding a sling, brave","1 Samuel 17:50","Lenda da Coragem",False),
 (69,"Sansão","Samson, a strong young man with long hair","Juízes 16:30","Lenda da Força",False),
 (70,"Ester","Queen Esther, a kind young queen with a crown","Ester 4:14","Lenda da Coragem",False),
 (71,"Daniel","Daniel praying calmly with a friendly lion","Daniel 6:22","Lenda da Fé",False),
 (72,"Elias","Elijah, a prophet with a small flame","1 Reis 18:38","Lenda do Fogo",False),
 (73,"Paulo","Paul the apostle, a kind man with a short beard holding a scroll letter","Atos 9:15","O Missionário",False),
 (74,"Jesus","Jesus, kind and majestic with a warm gentle smile, the Savior","João 3:16","O Salvador",True),
]
def legend_items():
    out=[]
    for num,name,detail,ref,role,ultra in LEGENDS:
        out.append({"num":num,"name":name,
            "id":f"L{num}_"+name.lower().replace(' ','_').replace('ã','a').replace('é','e').replace('í','i').replace('ô','o').replace('â','a').replace('ó','o').replace('ê','e'),
            "ref":ref,"book":ref.rsplit(' ',1)[0],"role":role,"ultra":ultra,"prompt":legend_prompt(detail)})
    return out

def team_items(t):
    """retorna lista de jogadores do time t (0-indexed) com num, id, prompt e metadados do card."""
    tm=TEAMS[t]; base=t*8+2; out=[]
    for i,(name,detail,book,ref,role) in enumerate(tm["players"]):
        num=base+i+1
        out.append({"num":num,"name":name,
            "id":f"{num:02d}_"+name.lower().replace(' ','_').replace('ã','a').replace('é','e').replace('í','i').replace('ô','o').replace('â','a').replace('ó','o').replace('ê','e'),
            "book":book,"ref":ref,"role":role,"tc":tm["tc"],"tcd":tm["tcd"],
            "prompt":player_prompt(detail,tm["jersey"],tm["emblem"],tm["bg"])})
    return out
