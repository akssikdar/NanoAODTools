class SkimGenInfo:
    def __init__(self):
        self.trueNumberOfInteractions = -999.

        self.id1  = -999.
        self.id2  = -999.
        self.x1   = -999.
        self.x2   = -999.

        self.scalePDF      = -999.
        self.MCWeight      = -999.
        #self.LHEWOrgXWGTUP = -999.
        #self.nLHEPart      = -999.
        
        # Scale Weights
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # WARNING: Different order than the one at MiniAOD
        # 2 and 6 are unphysical anti-correlated variations
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # LHE scale variation weights (w_var / w_nominal)
        # [0] is renscfact=0.5d0 facscfact=0.5d0
        # [1] is renscfact=0.5d0 facscfact=1d0
        # [2] is renscfact=0.5d0 facscfact=2d0
        # [3] is renscfact=1d0 facscfact=0.5d0
        # [4] is renscfact=1d0 facscfact=1d0
        # [5] is renscfact=1d0 facscfact=2d0
        # [6] is renscfact=2d0 facscfact=0.5d0
        # [7] is renscfact=2d0 facscfact=1d0
        # [8] is renscfact=2d0 facscfact=2d0
        self.ScaleWeights = []

        # PS variations: ISR and FSR
        # PS weights (w_var / w_nominal);
        # [0] is ISR=0.5 FSR=1; [1] is ISR=1 FSR=0.5; [2] is ISR=2 FSR=1; [3] is ISR=1 FSR=2
        self.PSWeights = []

        # PDF Weights
        # LHE pdf variation weights (w_var / w_nominal) for LHA IDs 91400 - 91432 
        self.PDFWeights = []

class SkimJets:
    def __init__(self):        

        self.pt  = -999.
        self.eta = -999. 
        self.phi = -999.
        self.E   = -999.
        self.Et  = -999.

        self.IDTight   = int(-999)
        self.IDLepVeto = int(-999)

        self.partonFlavour = int(-999)
        self.hadronFlavour = int(-999)

        self.btagCSV      = -999.
        self.btagMVA      = -999.
        self.btagDeepCSV  = -999.
        self.ctagDeepCSV  = -999.
        self.btagDeepFJet = -999.
        self.ctagDeepFJet = -999.
        self.QGL          = -999.

        self.Unc          = -999.
        self.JERUp        = -999.
        self.JERDown      = -999.
        
        #self.systJESUp    = []
        #self.systJESDown  = []
        #self.systbtagUp   = []
        #self.systbtagDown = []

        self.btagSF       = 1.0 

        self.raw_pt  = -999.
            
    pass


class SkimMuons:
    def __init__(self):
        self.pt     = -999.
        self.eta    = -999. 
        self.phi    = -999.
        self.E      = -999.
        self.charge = int(-999)
 
        self.chargedHadronIso = -999.
        self.iso_pflow        = -999.
        self.iso03_pflow      = -999.

        self.genPartFlav = -999.
        self.genPartIdx  = -999.
        
        self.dxy   = -999.
        self.dz    = -999.
        self.ip3D  = -999.

        self.isGlobal       = int(-999)
        self.isLoose        = int(-999)
        self.isMedium       = int(-999)
        self.isMediumPrompt = int(-999)
        self.isTight        = int(-999)

    pass

class SkimElectrons:
    def __init__(self):
        self.pt     = -999.
        self.eta    = -999. 
        self.phi    = -999.
        self.E      = -999.
        self.charge = int(-999)
        self.etaSC  = -999.

        self.chargedHadronIso = -999.
        self.iso_pflow        = -999.

        self.dxy   = -999.
        self.dz    = -999.
        self.edxy  = -999.
        self.edz   = -999.
        self.ip3D  = -999.

        self.genPartFlav = -999.
        self.genPartIdx  = -999.

        self.isVetoCBID   = int(-999)
        self.isLooseCBID  = int(-999)
        self.isMediumCBID = int(-999)
        self.isTightCBID  = int(-999)
        
        self.MVAValue      = -999.
        self.MVANoIsoValue = -999.

        self.isLooseMVAID       = int(-999)
        self.isMediumMVAID      = int(-999)
        self.isTightMVAID       = int(-999)
        self.isLooseMVANoIsoID  = int(-999)
        self.isMediumMVANoIsoID = int(-999)
        self.isTightMVANoIsoID  = int(-999)

	self.VID = int(-999)

    pass

class SkimMET:
    def __init__(self):

        self.met          = -999.
        self.px           = -999.
        self.py           = -999.
        self.phi          = -999.
        self.sumEt        = -999.
        self.significance = -999.

        self.metNoCorrFromJets = -999.

        self.unclup      = -999.
        self.uncldown    = -999.
        self.systJESUp   = -999.
        self.systJESDown = -999.
        self.systJERUp   = -999.
        self.systJERDown = -999.

    pass

class SkimGenParticles:
    def __init__(self):

        self.status   = int(-999)
        self.pdgId    = int(-999)
        self.motherId = int(-999)
        
        self.pt   = -999.
        self.eta  = -999.
        self.phi  = -999.
        self.E    = -999.

    pass


class SkimTop:
    def __init__(self):

        self.Top  = SkimGenParticles() 
        self.W    = SkimGenParticles() 
        self.b    = SkimGenParticles() 
        self.Up   = SkimGenParticles() 
        self.Down = SkimGenParticles() 

        self.cosThKF  = -999.
        self.cosThMlb = -999.
        self.LepHad   = -999.
        self.rwF0Mlb  = -999.
        self.rwFLMlb  = -999.
        self.rwFRMlb  = -999.

        self.rwF0KF  = -999.
        self.rwFLKF  = -999.
        self.rwFRKF  = -999.


class SkimTaus:
    def __init__(self):
        self.pt     = -999.
        self.eta    = -999. 
        self.phi    = -999.
        self.E      = -999.
        self.mass   = -999.
        self.charge = int(-999)
 
        self.dxy   = -999.
        self.dz    = -999.
        self.chargedIso = -999.

        self.decayMode = int(-999)
        self.idDecayModeNewDMs   = int(-999)

        self.idDeepTau2017v2p1VSe   = -999.
        self.idDeepTau2017v2p1VSmu  = -999.
        self.idDeepTau2017v2p1VSjet = -999.

        self.genPartIdx   = -999. # MC matching to status ==2 for taus
        self.genPartFlav  = -999.
        self.jetIdx       = int(-999)
        self.puCorr       = -999.

    pass

class SkimGenVisTau:
    def __init__(self):
        self.pt     = -999.
        self.eta    = -999.
        self.phi    = -999.
        self.status = int(-999)
        self.mass   = -999.
        self.charge = int(-999)
        self.genPartIdxMother = int(-999) #index of the mother particle

    pass


