# -*- coding: utf-8 -*-
"""Super Trunfo "Heróis da Fé" — dados das 33 cartas (32 + Super Trunfo Jesus).

Reaproveita as artes do álbum (assets/cards/*.png, assets/legends/* p/ Paulo) e
as cores das seleções de reinokids_data.TEAMS. Cada carta tem 5 atributos (0-99):
FÉ · CORAGEM · SABEDORIA · LIDERANÇA · FORÇA — cada herói com 1 destaque, ninguém
batendo o Jesus (Super Trunfo = 99 em tudo)."""
import os
from reinokids_data import TEAMS

ATTRS = ["FÉ", "CORAGEM", "SABEDORIA", "LIDERANÇA", "FORÇA"]

# group -> (índice da seleção em TEAMS, nome da seleção)
GROUPS = {
    "A": (0, "Patriarcas"),
    "B": (1, "Família da Promessa"),
    "C": (2, "Libertadores"),
    "D": (3, "Juízes"),
    "E": (4, "Reis"),
    "F": (5, "Profetas"),
    "G": (6, "Nascimento"),
    "H": (7, "Apóstolos"),
}

# code, grupo, nome, id_arte, ref, (FÉ, CORAGEM, SABEDORIA, LIDERANÇA, FORÇA)
_TABLE = [
    ("A1", "A", "Adão",            "03_adao",            "Gênesis 1:27",  (60, 55, 65, 70, 75)),
    ("A2", "A", "Eva",             "04_eva",             "Gênesis 3:20",  (58, 60, 68, 55, 50)),
    ("A3", "A", "Noé",             "05_noe",             "Gênesis 6:9",   (92, 70, 75, 80, 65)),
    ("A4", "A", "Abraão",          "06_abraao",          "Gênesis 15:6",  (99, 75, 80, 88, 60)),
    ("B1", "B", "Jacó",            "11_jaco",            "Gênesis 28:15", (78, 70, 82, 75, 72)),
    ("B2", "B", "José",            "14_jose",            "Gênesis 37:3",  (88, 75, 90, 92, 60)),
    ("B3", "B", "Judá",            "15_judá",            "Gênesis 49:9",  (70, 85, 72, 80, 85)),
    ("B4", "B", "Raquel",          "13_raquel",          "Gênesis 29:18", (72, 65, 70, 60, 45)),
    ("C1", "C", "Moisés",          "19_moises",          "Êxodo 14:21",   (95, 88, 85, 99, 70)),
    ("C2", "C", "Arão",            "20_arao",            "Êxodo 4:14",    (80, 65, 75, 82, 60)),
    ("C3", "C", "Josué",           "22_josue",           "Josué 1:9",     (90, 95, 78, 92, 88)),
    ("C4", "C", "Calebe",          "23_calebe",          "Números 13:30", (88, 92, 75, 80, 82)),
    ("D1", "D", "Gideão",          "27_gideao",          "Juízes 6:12",   (82, 90, 76, 85, 80)),
    ("D2", "D", "Sansão",          "28_sansao",          "Juízes 16:28",  (70, 88, 50, 65, 99)),
    ("D3", "D", "Débora",          "29_debora",          "Juízes 4:4",    (85, 88, 92, 90, 55)),
    ("D4", "D", "Boaz",            "32_boaz",            "Rute 2:1",      (78, 70, 80, 78, 75)),
    ("E1", "E", "Samuel",          "35_samuel",          "1 Samuel 3:10", (95, 75, 88, 85, 50)),
    ("E2", "E", "Saul",            "36_saul",            "1 Samuel 10:1", (60, 80, 65, 82, 85)),
    ("E3", "E", "Davi",            "38_davi",            "1 Samuel 16:7", (95, 99, 80, 92, 82)),
    ("E4", "E", "Salomão",         "39_salomao",         "1 Reis 3:9",    (85, 65, 99, 95, 55)),
    ("F1", "F", "Elias",           "43_elias",           "1 Reis 18:36",  (96, 90, 85, 88, 70)),
    ("F2", "F", "Eliseu",          "44_eliseu",          "2 Reis 2:9",    (90, 80, 86, 80, 65)),
    ("F3", "F", "Daniel",          "47_daniel",          "Daniel 6:22",   (99, 95, 92, 82, 50)),
    ("F4", "F", "Jonas",           "48_jonas",           "Jonas 2:1",     (70, 60, 72, 68, 55)),
    ("G1", "G", "Maria",           "51_maria",           "Lucas 1:38",    (99, 85, 88, 80, 50)),
    ("G2", "G", "José de Nazaré",  "52_jose_de_nazare",  "Mateus 1:20",   (90, 78, 82, 85, 70)),
    ("G3", "G", "João Batista",    "53_joao_batista",    "João 1:23",     (95, 92, 80, 88, 68)),
    ("G4", "G", "Gabriel",         "56_gabriel",         "Lucas 1:19",    (95, 85, 90, 85, 80)),
    ("H1", "H", "Jesus",           "59_jesus",           "João 3:16",     (99, 99, 99, 99, 99)),  # ★ SUPER TRUNFO
    ("H2", "H", "Pedro",           "60_pedro",           "Mateus 16:18",  (88, 90, 75, 92, 78)),
    ("H3", "H", "João",            "62_joao",            "João 13:23",    (92, 80, 88, 82, 60)),
    ("H4", "H", "Paulo",           "L73_paulo",          "Atos 9:15",     (96, 92, 95, 95, 60)),
]  # 32 cartas (A1–H4) — Jesus (H1) = carta SUPER TRUNFO marcada dentro do grupo H

# Jesus / Super Trunfo usa o dourado da seleção dos Apóstolos
GOLD_TC, GOLD_TCD = (214, 176, 92), (120, 88, 30)

_BASE = os.path.dirname(os.path.abspath(__file__))
_CARDS = os.path.join(_BASE, "assets", "cards")
_LEGENDS = os.path.join(_BASE, "assets", "legends")


def art_path(art_id):
    """Resolve o caminho da arte: lendas (L*) em assets/legends, resto em assets/cards."""
    folder = _LEGENDS if art_id.startswith("L") else _CARDS
    return os.path.join(folder, art_id + ".png")


def cards():
    """Lista de dicts prontos p/ o build: code, name, art, ref, attrs, cores, crest, super_trunfo."""
    out = []
    for code, grp, name, art_id, ref, attrs in _TABLE:
        is_super = name == "Jesus"  # Jesus (H1) é a carta Super Trunfo, mas pertence ao grupo H
        idx, sel = GROUPS[grp]
        tc, tcd = TEAMS[idx]["tc"], TEAMS[idx]["tcd"]
        crest = os.path.join(_BASE, "assets", "crests", f"team{idx + 1}.png")
        out.append({
            "code": code, "name": name, "selecao": sel, "art": art_path(art_id),
            "ref": ref, "attrs": dict(zip(ATTRS, attrs)), "attr_list": list(attrs),
            "tc": tc, "tcd": tcd, "crest": crest, "super_trunfo": is_super,
        })
    return out


if __name__ == "__main__":
    cs = cards()
    missing = [c["name"] for c in cs if not os.path.exists(c["art"])]
    print(f"{len(cs)} cartas. Artes faltando: {missing or 'nenhuma'}")
    for c in cs:
        print(f"  {c['code']:>3} {c['name']:<16} {c['attr_list']} {'★SUPER' if c['super_trunfo'] else ''}")
