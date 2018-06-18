import random
from flask import Flask, request, redirect, render_template, session, flash
import cgi

PosOneCations = [('Hydrogen','H',1,0), ('Lithium','Li',1,0), ('Sodium','Na',1,0), ('Potassium','K',1,0), ('Rubidium','Rb',1,0), ('Cesium','Cs',1,0), ('Silver','Ag',1,0), ('Copper (I)','Cu',1,0), ('Gold (I)','Au',1,0), ('Gallium (I)','Ga',1,0), ('Indium (I)','In',1,0), ('Ammonium','NH4',1,1)]
PosTwoCations = [('Beryllium','Be',2,0), ('Magnesium','Mg',2,0), ('Calcium','Ca',2,0), ('Strontium','Sr',2,0), ('Barium','Ba',2,0), ('Chromium (II)','Cr',2,0), ('Manganese (II)','Mn',2,0), ('Iron (II)','Fe',2,0), ('Cobalt (II)','Co',2,0), ('Nickel','Ni',2,0), ('Copper (II)','Cu',2,0), ('Zinc','Zn',2,0), ('Cadmium','Cd',2,0), ('Mercury (II)','Hg',2,0), ('Tin (II)','Sn',2,0), ('Lead (II)','Pb',2,0)]
PosThreeCations = [('Scandium','Sc',3,0), ('Titanium (III)','Ti',3,0), ('Vanadium (III)','V',3,0), ('Chromium (III)','Cr',3,0), ('Iron (III)','Fe',3,0), ('Cobalt (III)','Co',3,0), ('Galium (III)','Ga',3,0), ('Indium (III)','In',3,0), ('Yttrium','Y',3,0), ('Rhodium (III)','Rh',3,0), ('Gold (III)','Au',3,0), ('Aluminum','Al',3,0)]
PosFourCations = [('Tin (IV)','Sn',4,0), ('Lead (IV)','Pb',4,0), ('Titanium (IV)','Ti',4,0), ('Vanadium (IV)','V',4,0), ('Manganese (IV)','Mn',4,0), ('Rhodium (IV)','Rh',4,0), ('Tungsten (IV)','W',4,0), ('Osmium (IV)','Os',4,0)]
MiscCations = [('Vanadium (V)','V',5,0), ('Tungsten (V)','W',5,0), ('Chromium (VI)','Cr',6,0), ('Tungsten (VI)','W',6,0)]
MonatomicAnions = [('fluoride','F',-1,0), ('chloride','Cl',-1,0), ('bromide','Br',-1,0), ('iodide','I',-1,0), ('oxide','O',-2,0), ('sulfide','S',-2,0), ('selenide','Se',-2,0), ('nitride','N',-3,0), ('phosphide','P',-3,0)]
PolyatomicAnions = [('nitrate','NO3',-1,1), ('nitrite','NO2',-1,1), ('hydroxide','OH',-1,1), ('hypochlorite','ClO',-1,1), ('chlorite','ClO2',-1,1), ('chlorate','ClO3',-1,1), ('perchlorate','ClO4',-1,1), ('permanganate','MnO4',-1,1), ('acetate','C2H3O2',-1,1), ('cyanide','CN',-1,1), ('hydrogen carbonate','HCO3',-1,1), ('hydrogen sulfate','HSO4',-1,1), ('dihydrogen phosphate','H2PO4',-1,1), ('sulfate','SO4',-2,1), ('sulfite','SO3',-2,1), ('carbonate','CO3',-2,1), ('chromate','CrO4',-2,1), ('dichromate','Cr2O7',-2,1), ('hydrogen phospate','HPO4',-2,1), ('oxalate','C2O4',-2,1), ('phosphate','PO4',-3,1), ('phosphite','PO3',-3,1)]
# Ion tuple order = (Ion name, forumla, charge, monatomic/polyatomic ID 0/1 = No/Yes)

cations = PosOneCations+PosTwoCations+PosThreeCations+PosFourCations+MiscCations
anions = MonatomicAnions+PolyatomicAnions

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'yrtsimehc'

def chooseCompound():
    cation = random.choice(cations)
    anion = random.choice(anions)
    name = cation[0] + ' ' + anion[0]
    formula = findSubscripts(cation,anion)
    compound = (name, formula)
    return compound

def findSubscripts(cation, anion):
    if cation[2] == -anion[2]:
        formula = cation[1]+anion[1]
    elif cation[2] < -anion[2] and -anion[2]%cation[2]==0:
        if cation[3]:
            formula = "({0}){1}{2}".format(cation[1],str(int(-anion[2]/cation[2])),anion[1]) 
        else:
            formula = cation[1]+str(int(-anion[2]/cation[2]))+anion[1]
    elif cation[2] > -anion[2] and -cation[2]%anion[2]==0:
        if anion[3]:
            formula = "{0}({1}){2}".format(cation[1],anion[1],str(int(-cation[2]/anion[2]))) 
        else:
            formula = cation[1]+anion[1]+str(int(-cation[2]/anion[2]))
    else:
        if cation[3]:
            formula = "({0}){1}".format(cation[1],str(-anion[2]))
        else:
            formula = cation[1]+str(-anion[2])
        if anion[3]:
            formula += "({0}){1}".format(anion[1],str(cation[2]))
        else:
            formula += anion[1]+str(cation[2])
    return formula

def checkName(answer,name):
    #remove spaces from answer and expected name, then compare.
    #Return boolen as 'result'
    return result

@app.route('/')
def index():
    session.clear()
    return render_template('index.html',title="Naming Practice")

@app.route('/namesfromformulas',methods=['POST', 'GET'])
def namesfromformulas():
    if request.method == 'POST':
        answer = request.form['answer']
        name = request.form['name']
        formula = request.form['formula']
        if answer.lower() == name.lower():
            flash('Correct!  :-)', 'correct')
        else:
            flash('Try again, or click here to reveal the answer.', 'error')
    
        return render_template('namesfromformulas.html', name = name, formula = formula, answer = answer)

    Compound = chooseCompound()
    return render_template('namesfromformulas.html',title="Names fron Formulas", name = Compound[0], formula = Compound[1])

if __name__ == '__main__':
    app.run()