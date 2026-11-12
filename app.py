import streamlit as st
import math

def verduennung(c1, c2, v2):
  if c1 <= 0 or c2 <= 0 or v2 <= 0:
    return "FEHLER: Alle Werte müssen größer als 0 sein."
  v1 = (c2 * v2) / c1
  if v1 > v2:
    return "ACHTUNG: v1 größer als v2, prüfe die Eingaben!"
  return v1

def einwaage(konzentration, volumen_l, molmasse):
  if konzentration <= 0 or volumen_l <= 0 or molmasse <= 0:
    return "FEHLER: Alle Werte müssen größer als 0 sein."
  masse = konzentration * volumen_l * molmasse
  return masse

def puffer_ph(pks, konz_base, konz_saeure):
  if konz_base <= 0 or konz_saeure <= 0:
    return "FEHLER: Konzentrationen müssen größer als 0 sein."
  ph = pks + math.log10(konz_base / konz_saeure)
  return ph

def mastermix(komponenten, anzahl_proben, extra=1):
  if anzahl_proben <= 0:
    return "FEHLER: Anzahl Proben muss größer als 0 sein."
  gesamt = anzahl_proben + extra
  ergebnis = {}
  for name, menge in komponenten.items():
    ergebnis[name] = menge * gesamt
  return ergebnis

def verduennungsreihe(start_konz, faktor, zielvolumen, anzahl_stufen):
  if start_konz <= 0 or faktor <= 1 or zielvolumen <= 0 or anzahl_stufen <= 0:
    return "FEHLER: Prüfe die Eingaben (Faktor muss größer als 1 sein)."
  probe = zielvolumen / faktor
  loesungsmittel = zielvolumen - probe
  stufen = []
  konz = start_konz
  for i in range(1, anzahl_stufen + 1):
    konz = konz / faktor
    stufen.append({
      "Stufe": i,
      "Konzentration": konz,
      "Probe (µl)": probe,
      "Lösungsmittel (µl)": loesungsmittel
    })
  return stufen

def od_zu_zellzahl(od, faktor):
  if od < 0 or faktor <= 0:
    return "FEHLER: OD darf nicht negativ und Faktor muss größer als 0 sein."
  zellzahl = od * faktor
  return zellzahl

def masse_mol_molmasse(masse, mol, molmasse):
  if masse == 0 and mol > 0 and molmasse > 0:
    return "Masse (g)", mol * molmasse
  elif mol == 0 and masse > 0 and molmasse > 0:
    return "Stoffmenge (mol)", masse / molmasse
  elif molmasse == 0 and masse > 0 and mol > 0:
    return "Molmasse (g/mol)", masse / mol
  else:
    return "FEHLER", "Genau ein Feld auf 0 lassen (das gesuchte), die anderen zwei ausfüllen."


st.title("Labor-Rechner")

auswahl = st.selectbox(
  "Was willst du berechnen?",
  ["Verdünnung", "Einwaage", "Puffer-pH", "PCR-Mastermix", "Verdünnungsreihe", "OD → Zellzahl", "g ↔ mol"]
)

if auswahl == "Verdünnung":
  st.header("Verdünnung (C1*V1 = C2*V2)")
  c1 = st.number_input("Stammkonzentration c1", value=1.0)
  c2 = st.number_input("Zielkonzentration c2", value=0.1)
  v2 = st.number_input("Zielvolumen v2", value=100.0)
  if st.button("Berechnen"):
    st.write("Ergebnis:", verduennung(c1, c2, v2))

elif auswahl == "Einwaage":
  st.header("Einwaage (Masse in Gramm)")
  konz = st.number_input("Konzentration (mol/l)", value=0.1)
  vol = st.number_input("Volumen (Liter)", value=0.5)
  mm = st.number_input("Molmasse (g/mol)", value=58.44)
  if st.button("Berechnen"):
    st.write("Ergebnis (g):", einwaage(konz, vol, mm))

elif auswahl == "Puffer-pH":
  st.header("Puffer-pH (Henderson-Hasselbalch)")
  pks = st.number_input("pKs-Wert", value=4.76)
  base = st.number_input("Konzentration Base", value=0.1)
  saeure = st.number_input("Konzentration Säure", value=0.1)
  if st.button("Berechnen"):
    ph_wert = puffer_ph(pks, base, saeure)
    st.write("pH:", round(ph_wert, 2))

elif auswahl == "PCR-Mastermix":
  st.header("PCR-Mastermix")
  proben = st.number_input("Anzahl Proben", value=8, step=1)
  extra = st.number_input("Extra-Proben (Sicherheit)", value=1, step=1)
  komponenten = {
    "Puffer": 2.0,
    "dNTPs": 0.5,
    "Primer vorwärts": 1.0,
    "Primer rückwärts": 1.0,
    "Polymerase": 0.25,
    "Wasser": 15.25
  }
  if st.button("Berechnen"):
    ergebnis = mastermix(komponenten, int(proben), int(extra))
    if isinstance(ergebnis, dict):
      st.subheader("Mastermix-Mengen (µl):")
      for name, menge in ergebnis.items():
        st.write(name, ":", round(menge, 2), "µl")
    else:
      st.write(ergebnis)

elif auswahl == "Verdünnungsreihe":
  st.header("Serielle Verdünnungsreihe")
  start = st.number_input("Startkonzentration", value=1.0)
  faktor = st.number_input("Verdünnungsfaktor (z.B. 10 für 1:10)", value=10.0)
  zielvol = st.number_input("Zielvolumen pro Röhrchen (µl)", value=1000.0)
  stufen_zahl = st.number_input("Anzahl Stufen", value=3, step=1)
  if st.button("Berechnen"):
    ergebnis = verduennungsreihe(start, faktor, zielvol, int(stufen_zahl))
    if isinstance(ergebnis, list):
      for stufe in ergebnis:
        st.write(
          "Stufe", stufe["Stufe"],
          "→ Konz.", round(stufe["Konzentration"], 5),
          "| Probe:", round(stufe["Probe (µl)"], 1), "µl",
          "| Lösungsmittel:", round(stufe["Lösungsmittel (µl)"], 1), "µl"
        )
    else:
      st.write(ergebnis)
elif auswahl == "OD → Zellzahl":
  st.header("OD₆₀₀ → Zellzahl")
  faktoren = {
    "E. coli": 800000000.0,
    "Hefe (S. cerevisiae)": 30000000.0,
    "Eigener Wert": 1.0
  }
  organismus = st.selectbox("Organismus", list(faktoren.keys()))
  start_faktor = faktoren[organismus]
  od = st.number_input("OD₆₀₀", value=1.0)
  faktor = st.number_input("Umrechnungsfaktor (Zellen/ml pro OD)", value=start_faktor)
  if st.button("Berechnen"):
    ergebnis = od_zu_zellzahl(od, faktor)
    if isinstance(ergebnis, str):
      st.write(ergebnis)
    else:
      st.write("Zellzahl:", ergebnis, "Zellen/ml")

elif auswahl == "g ↔ mol":
  st.header("g ↔ mol Umrechner")
  st.write("Fülle zwei Felder aus, lass das gesuchte auf 0.")
  masse = st.number_input("Masse (g)", value=0.0)
  mol = st.number_input("Stoffmenge (mol)", value=0.0)
  molmasse = st.number_input("Molmasse (g/mol)", value=0.0)
  if st.button("Berechnen"):
    name, wert = masse_mol_molmasse(masse, mol, molmasse)
    if name == "FEHLER":
      st.write(wert)
    else:
      st.write(name, ":", round(wert, 4))
