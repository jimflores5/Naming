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

BimolecularCpds = [('Diboron hexachloride','B2Cl6',0), ('Dibromine monoxide','Br2O','Dibromine monooxide'), ('Bromine trifluoride','BrF3',0), ('Dicarbon dihydride','C2H2','Ethyne'), ('Dicarbon tetrahydride','C2H4','Ethene'), ('Dicarbon hexahydride','C2H6','Ethane'), ('Tricarbon tetrahydride','C3H4','Propyne'), ('Tricarbon hexahydride','C3H6','Propene'), ('Tricarbon octahydride','C3H8','Propane'), ('Tetracarbon decahydride','C4H10','Butane'), ('Tetracarbon hexahydride','C4H6','Butyne'), ('Tetracarbon octahydride','C4H8','Butene'), ('Pentacarbon decahydride','C5H10','Pentene'), ('Pentacarbon octahydride','C5H8','Pentyne'), ('Carbon tetrachloride','CCl4',0), ('Carbon tetrahydride','CH4','Methane'), ('Dichlorine monoxide','Cl2O','Dichlorine monooxide'), ('Carbon monoxide','CO','Carbon monooxide'), ('Carbon dioxide','CO2',0), ('Dihydrogen monoxide','H2O','Water'), ('Diiodine tetroxide','I2O4','Diiodine tetraoxide'), ('Diiodine pentoxide','I2O5','Diiodine pentaoxide'), ('Iodine monobromide','IBr',0), ('Dinitrogen monoxide','N2O','Dinitrogen monooxide'), ('Dinitrogen tetroxide','N2O4','Dinitrogen tetraoxide'), ('Nitrogen trihydride','NH3','Ammonia'), ('Nitrogen tribromide','NBr3',0), ('Nitrogen monoxide','NO','Nitrogen monooxide'), ('Nitrogen dioxide','NO2',0), ('Diphosphorous tetrabromide','P2Br4',0), ('Tetraphosphorous decoxide','P4O10','Tetraphosphorous decaoxide'), ('Phosphorous pentachloride','PCl5',0), ('Phosphorous trifluoride','PF3',0), ('Phosphouous trihydride','PH3',0), ('Sulfur difluoride','SF2',0), ('Sulfur hexafluoride','SF6',0), ('Sulfur dioxide','SO2',0), ('Sulfur trioxide','SO3',0)]
# Molecular tuple order = (Name, forumla, alternate name (0 if none))

cations = PosOneCations+PosTwoCations+PosThreeCations+PosFourCations+MiscCations
anions = MonatomicAnions+PolyatomicAnions
digits = ['0','1','2','3','4','5','6','7','8','9']

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'yrtsimehc'

def chooseCompound(type='all'):
    if type == 'molecular':
        choice = random.choice(BimolecularCpds)
        compound = (choice[0],choice[1])
    elif type == 'ionic':
        cation = random.choice(cations)
        anion = random.choice(anions)
        name = cation[0] + ' ' + anion[0]
        formula = findSubscripts(cation,anion)
        compound = (name, formula)
    else:
        if random.randint(0,5) == 0:
            choice = random.choice(BimolecularCpds)
            compound = (choice[0],choice[1])
        else:
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
    if any(name in code for code in BimolecularCpds):
        index = [x for x, y in enumerate(BimolecularCpds) if y[0] == name]
        choice = BimolecularCpds[index[0]]
        name = name.replace(' ','')
        answer = answer.replace(' ','')
        if choice[2] != 0:
            altname = choice[2].replace(' ','')
            if answer.lower() == name.lower() or answer.lower() == altname.lower():
                result = True
            else:
                result = False
        else:
            if answer.lower() == name.lower():
                result = True
            else:
                result = False
    else:
        answer = answer.replace(' ','')
        name = name.replace(' ','')
        if answer.lower() == name.lower():
            result = True
        else:
            result = False
    return result

@app.route('/')
def index():
    session.clear()
    return render_template('index.html',title="Naming Practice")

@app.route('/namesfromformulas/<type>',methods=['POST', 'GET'])
def namesfromformulas(type):
    if request.method == 'POST':
        answer = request.form['answer']
        name = request.form['name']
        formula = request.form['formula']
        if checkName(answer,name):
            flash('Correct!  :-)', 'correct')
        else:
            flash('Try again, or click here to reveal the answer.', 'error')
    
        return render_template('namesfromformulas.html', title="Names fron Formulas", name = name, formula = formula, answer = answer, digits = digits, type = type)

    Compound = chooseCompound(type)
    return render_template('namesfromformulas.html',title="Names fron Formulas", name = Compound[0], formula = Compound[1], digits = digits, type = type)

@app.route('/formulasfromnames/<type>',methods=['POST', 'GET'])
def formulasfromnames(type):
    if request.method == 'POST':
        answer = request.form['answer']
        name = request.form['name']
        formula = request.form['formula']
        if answer == formula:
            flash('Correct!  :-)', 'correct')
        else:
            flash('Try again, or click here to reveal the answer.', 'error')
    
        return render_template('formulasfromnames.html', title="Formulas from Names", name = name, formula = formula, answer = answer, digits = digits, type = type)

    Compound = chooseCompound(type)
    return render_template('formulasfromnames.html',title="Formulas from Names", name = Compound[0], formula = Compound[1], digits = digits, type = type)

@app.route('/allnaming',methods=['POST', 'GET'])
def allnaming():
    if request.method == 'POST':
        answer = request.form['answer']
        name = request.form['name']
        formula = request.form['formula']
        question = request.form['question']
        if question == '0' and checkName(answer,name):
            flash('Correct!  :-)', 'correct')
        elif question == '1' and answer == formula:
            flash('Correct!  :-)', 'correct')
        else:
            flash('Try again, or click here to reveal the answer.', 'error')
    
        return render_template('allnaming.html', title="Practice All Naming", name = name, formula = formula, answer = answer, digits = digits, question = question)

    Compound = chooseCompound()
    question = str(random.randint(0,1))
    return render_template('allnaming.html',title="Practice All Naming", name = Compound[0], formula = Compound[1], digits = digits, question = question)

if __name__ == '__main__':
    app.run()