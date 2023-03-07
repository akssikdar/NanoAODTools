import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.UserCode.ObjectsDef import *


## -- Jets
def NanoJetToCIEMAT(NanoJetCollection, JESNames, btagNames):

    JetColl = []

    for NanoJet in NanoJetCollection:

        ijet = SkimJets()

        # Keep jets with syst. variation pT>18 GeV 
        if not (NanoJet.pt_jesTotalUp or NanoJet.pt_jesTotalDown or NanoJet.pt_jerUp or NanoJet.pt_jerDown) > 18:
            continue

        # Jet ID flags bit1 is loose (always false in 2017 since it does not exist), 
        # bit2 is tight, bit3 is tightLepVeto
        ijet.IDTight   = CheckFlag(NanoJet.jetId,1)
        ijet.IDLepVeto = CheckFlag(NanoJet.jetId,2)

        # Following the 2017/2018 recommendations: No looseID anymore.
        if not ijet.IDTight:
            continue
        
        ijet.raw_pt  = NanoJet.pt  # UNCORRECTED pt with JER [GeV]

        ijet.pt  = NanoJet.pt_nom  # CORRECTED pt with JER [GeV]
        ijet.eta = NanoJet.eta     # eta
        ijet.phi = NanoJet.phi     # phi

        # Not needed anymore, Nano already applies the JER
        # jet.ptGen       = NanoJet.pt[ (NanoJet.genJetIdx[ij]) ]; # pt [GeV]
        ijet.partonFlavour = NanoJet.partonFlavour
        ijet.hadronFlavour = NanoJet.hadronFlavour
        
        ijet.emEnergy            = NanoJet.chEmEF # electromagnetic energy [GeV]
        ijet.muonEnergy          = NanoJet.muEF   # muonic energy [GeV]
        
        ijet.btagCSV      = NanoJet.btagCSVV2     # CSV discriminant
        ijet.btagMVA      = NanoJet.btagCMVA      # MVA discriminant
        ijet.btagDeepCSV  = NanoJet.btagDeepB     # Deep CSV discriminant b jets
        ijet.ctagDeepCSV  = NanoJet.btagDeepC     # Deep CSV discriminant c jets
        ijet.btagDeepFJet = NanoJet.btagDeepFlavB # Deep Flavour Jet discriminant b jets
        ijet.ctagDeepFJet = NanoJet.btagDeepFlavC # Deep Flavour Jet discriminant c jets

        ijet.QGL = NanoJet.qgl # Quark-Gluon Likelihood for BKG estimation  
        
        # Max JES Uncertainty
        ijet.Unc = NanoJet.pt_jesTotalUp if NanoJet.pt_jesTotalUp > NanoJet.pt_jesTotalDown else NanoJet.pt_jesTotalDown 
	
        # JER
        # Other variables: pt_raw, corr_JER
        ijet.JERUp   = NanoJet.pt_jerUp
        ijet.JERDown = NanoJet.pt_jerDown

        # JES
        for JESName in range(len(JESNames)):
            ijet.systJESUp.  append(NanoJet.__getitem__("pt_jes"+JESNames[JESName]+"Up"))
            ijet.systJESDown.append(NanoJet.__getitem__("pt_jes"+JESNames[JESName]+"Down"))
        
        # b-tagging SF
        ijet.btagSF = NanoJet.deepcsv_shape
	
        for btagName in range(len(btagNames)):
            ijet.systbtagUp.  append(NanoJet.__getitem__("deepcsvSF_shape_up_"  +btagNames[btagName]))
            ijet.systbtagDown.append(NanoJet.__getitem__("deepcsvSF_shape_down_"+btagNames[btagName]))

        # Jet ID flags bit1 is loose (always false in 2017 since it does not exist), 
        # bit2 is tight, bit3 is tightLepVeto
        ijet.IDTight   = CheckFlag(NanoJet.jetId,1)
        ijet.IDLepVeto = CheckFlag(NanoJet.jetId,2)
        
        vjet = ROOT.TLorentzVector()
        vjet.SetPtEtaPhiM(ijet.pt,ijet.eta,ijet.phi,NanoJet.mass)
        ijet.Et = vjet.Et()  # E_T [GeV]
        ijet.E  = vjet.E()   # E   [GeV]
    
        JetColl.append(ijet)

    return JetColl

## -- Jets
def NanoJetNoSYSTToCIEMAT( NanoJetCollection ):
    
    JetColl = []

    for NanoJet in NanoJetCollection:

        ijet = SkimJets()

        # Keep jets with syst. variation pT>20 GeV 
        if not (NanoJet.pt > 20):
            continue

        ijet.raw_pt = 0.

        ijet.pt  = NanoJet.pt  # pt [GeV]
        ijet.eta = NanoJet.eta # eta
        ijet.phi = NanoJet.phi # phi

        ijet.btagCSV      = NanoJet.btagCSVV2     # CSV discriminant
        #ijet.btagMVA      = NanoJet.btagCMVA      # MVA discriminant
        ijet.btagDeepCSV  = NanoJet.btagDeepB     # Deep CSV discriminant b jets
        #ijet.ctagDeepCSV  = NanoJet.btagDeepC     # Deep CSV discriminant c jets
        ijet.btagDeepFJet = NanoJet.btagDeepFlavB # Deep Flavour Jet discriminant b jets
        #ijet.ctagDeepFJet = NanoJet.btagDeepFlavC # Deep Flavour Jet discriminant c jets
        
        ijet.QGL = NanoJet.qgl # Quark-Gluon Likelihood for BKG estimation  

	# b-tagging SF
	ijet.btagSF = 1.
	
        # Jet ID flags bit1 is loose (always false in 2017 since it does not exist), 
        # bit2 is tight, bit3 is tightLepVeto
        ijet.IDTight   = CheckFlag(NanoJet.jetId,1)
        ijet.IDLepVeto = CheckFlag(NanoJet.jetId,2)
        
        vjet = ROOT.TLorentzVector()
        vjet.SetPtEtaPhiM(ijet.pt,ijet.eta,ijet.phi,NanoJet.mass)
        ijet.Et = vjet.Et()  # E_T [GeV]
        ijet.E  = vjet.E()   # E   [GeV]
    
        JetColl.append(ijet)

    return JetColl
 

## -- MET 
def NanoMETToCIEMAT( NanoMETCollection ):
    
    iMET = SkimMET()

    MET = ROOT.TLorentzVector() 
    # Before JER
    # MET.SetPtEtaPhiM(NanoMETCollection.pt,0.,NanoMETCollection.phi,0.)
    iMET.metNoCorrFromJets = NanoMETCollection.pt
    # After JER nominal
    MET.SetPtEtaPhiM(NanoMETCollection.pt_nom,0.,NanoMETCollection.phi_nom,0.)
    iMET.met = MET.Pt()
    iMET.px  = MET.Px()
    iMET.py  = MET.Py()
    iMET.phi = MET.Phi()

    iMET.sumEt = NanoMETCollection.sumEt 
    iMET.significance = NanoMETCollection.significance 
    
    iMET.unclup   = NanoMETCollection.pt_unclustEnUp
    iMET.uncldown = NanoMETCollection.pt_unclustEnDown 

    # Systematic Uncertainties from Jet variations 
    iMET.systJERUp   = NanoMETCollection.pt_jerUp
    iMET.systJERDown = NanoMETCollection.pt_jerDown
    iMET.systJESUp   = NanoMETCollection.pt_jesTotalUp
    iMET.systJESDown = NanoMETCollection.pt_jesTotalDown

    return iMET

## -- MET 
def NanoMETNoSYSTToCIEMAT( NanoMETCollection ):
    
    iMET = SkimMET()

    MET = ROOT.TLorentzVector() 
    MET.SetPtEtaPhiM(NanoMETCollection.pt,0.,NanoMETCollection.phi,0.)
    iMET.met = MET.Pt()
    iMET.px  = MET.Px()
    iMET.py  = MET.Py()
    iMET.phi = MET.Phi()

    iMET.metNoCorrFromJets = 0.
    
    iMET.sumEt = NanoMETCollection.sumEt 
    iMET.significance = NanoMETCollection.significance 
    
    iMET.unclup   = 0.
    iMET.uncldown = 0.

    iMET.systJERUp   = 0.
    iMET.systJERDown = 0.
    iMET.systJESUp   = 0.
    iMET.systJESDown = 0.

    return iMET

# -- MET Filters
def NanoMETFiltersToCIEMAT( NanoMETFiltersCollection, MET_FilterNames ):

    iMET_Filters = []
    for iFilter in range(len(MET_FilterNames)):
        iMET_Filters.append(NanoMETFiltersCollection.__getitem__(MET_FilterNames[iFilter]))

    return iMET_Filters


## -- Muons
def NanoMuonToCIEMAT( NanoMuonCollection ):

    MuonColl = []

    for NanoMuon in NanoMuonCollection:

	if not (NanoMuon.pt) > 8:
            continue
	if not abs(NanoMuon.eta) < 2.4:
            continue

        imuon = SkimMuons()

        imuon.isGlobal = NanoMuon.isGlobal
        imuon.isLoose  = 1 if (NanoMuon.isPFcand and (NanoMuon.isGlobal or NanoMuon.isTracker)) else 0
        imuon.isMedium = NanoMuon.mediumId
        imuon.isMediumPrompt = NanoMuon.mediumPromptId
        imuon.isTight  = NanoMuon.tightId
        
        # Keep only Loose Muons
        if not imuon.isLoose:
            continue
        
        imuon.pt     = NanoMuon.pt  # pt [GeV]
        imuon.eta    = NanoMuon.eta # eta
        imuon.phi    = NanoMuon.phi # phi
        imuon.charge = NanoMuon.charge    # charge
        
        imuon.dxy   = NanoMuon.dxy  # signed transverse distance to primary vertex [cm]
        imuon.dz    = NanoMuon.dz   # signed longitudinal distance to primary vertex at min. transv. distance [cm]
        imuon.ip3D  = NanoMuon.ip3d # 3D impact parameter wrt first PV, in cm

        #imuon.genPartFlav  = NanoMuon.genPartFlav
        #imuon.genPartIdx   = NanoMuon.genPartIdx
        
        imuon.chargedHadronIso = NanoMuon.pfRelIso03_chg
        imuon.iso03_pflow      = NanoMuon.pfRelIso03_all
        imuon.iso_pflow        = NanoMuon.pfRelIso04_all
            
        vmuon = ROOT.TLorentzVector()
        vmuon.SetPtEtaPhiM(imuon.pt,imuon.eta,imuon.phi,NanoMuon.mass)
        imuon.E = vmuon.E()
        
        MuonColl.append(imuon)

    return MuonColl

## -- Electrons 
def NanoElectronToCIEMAT( NanoElectronCollection ):

    ElectronColl = []

    for NanoElectron in NanoElectronCollection:

	if not (NanoElectron.pt) > 12:
            continue
	if not abs(NanoElectron.eta) < 2.4:
            continue

        ielectron = SkimElectrons()

	# Note: Electron CutBased ID is not implemented as bits. Each cut contains the previous one as is show in:
	# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
        # cut-based ID (0:fail, 1:veto, 2:loose, 3:medium, 4:tight)
        ielectron.isVetoCBID   = 1 if NanoElectron.cutBased > 0 else 0
        ielectron.isLooseCBID  = 1 if NanoElectron.cutBased > 1 else 0
        ielectron.isMediumCBID = 1 if NanoElectron.cutBased > 2 else 0
        ielectron.isTightCBID  = 1 if NanoElectron.cutBased > 3 else 0

	# --------------------------------------------
	# Debugging to extract antiIso electrons
	# Full info in NanoReader
	# --------------------------------------------
	# if(NanoElectron.cutBased is not 0):
	#     print "CutBased = " + str(NanoElectron.cutBased)
	#     print str(NanoElectron.vidNestedWPBitmap) + " = " + str(bin(NanoElectron.vidNestedWPBitmap))
	#     # VID compressed bitmap (MinPtCut,GsfEleSCEtaMultiRangeCut,GsfEleDEtaInSeedCut,GsfEleDPhiInCut,GsfEleFull5x5SigmaIEtaIEtaCut,GsfEleHadronicOverEMEnergyScaledCut,GsfEleEInverseMinusPInverseCut,GsfEleRelPFIsoScaledCut,GsfEleConversionVetoCut,GsfEleMissingHitsCut), 3 bits per cut
	#     print "Flag 0 (MinPtCut) = "                            + str(NanoElectron.pt)
	#     print "Flag 1 (GsfEleSCEtaMultiRangeCut) = "            + str("???")
	#     print "Flag 2 (GsfEleDEtaInSeedCut) = "                 + str(NanoElectron.deltaEtaSC)
	#     print "Flag 3 (GsfEleDPhiInCut) = "                     + "???"
	#     print "Flag 4 (GsfEleFull5x5SigmaIEtaIEtaCut) = "       + str(NanoElectron.sieie)
	#     print "Flag 5 (GsfEleHadronicOverEMEnergyScaledCut) = " + str(NanoElectron.hoe)
	#     print "Flag 6 (GsfEleEInverseMinusPInverseCut) = "      + str(NanoElectron.eInvMinusPInv)
	#     print "Flag 7 (GsfEleRelPFIsoScaledCut) = "             + str(NanoElectron.pfRelIso03_all)
	#     print "Flag 8 (GsfEleConversionVetoCut) = "             + str(NanoElectron.convVeto)
	#     print "Flag 9 (GsfEleMissingHitsCut) = "                + str(NanoElectron.lostHits)
	# --------------------------------------------	
	# --------------------------------------------
	
	# Keep only Veto electrons
	if not ielectron.isVetoCBID:
            continue

        # MVA    
        ielectron.MVAValue      = NanoElectron.mvaFall17V2Iso
        ielectron.MVANoIsoValue = NanoElectron.mvaFall17V2noIso

        ielectron.isLooseMVAID       = NanoElectron.mvaFall17V2Iso_WPL
        ielectron.isMediumMVAID      = NanoElectron.mvaFall17V2Iso_WP90
        ielectron.isTightMVAID       = NanoElectron.mvaFall17V2Iso_WP80
        ielectron.isLooseMVANoIsoID  = NanoElectron.mvaFall17V2noIso_WPL
        ielectron.isMediumMVANoIsoID = NanoElectron.mvaFall17V2noIso_WP90
        ielectron.isTightMVANoIsoID  = NanoElectron.mvaFall17V2noIso_WP80

        ielectron.pt     = NanoElectron.pt     # pt [GeV]
        ielectron.eta    = NanoElectron.eta    # eta
        ielectron.phi    = NanoElectron.phi    # phi
        ielectron.charge = NanoElectron.charge # charge
        ielectron.etaSC  = (NanoElectron.eta + NanoElectron.deltaEtaSC)
        
        ielectron.dxy   = NanoElectron.dxy    # signed transverse distance to primary vertex [cm]
        ielectron.dz    = NanoElectron.dz     # signed longitudinal distance to primary vertex at min.transv.distance [cm]
        ielectron.edxy  = NanoElectron.dxyErr # uncertainty on dxy [cm]
        ielectron.edz   = NanoElectron.dzErr  # uncertainty on dz [cm]
        ielectron.ip3D  = NanoElectron.ip3d

        #ielectron.genPartFlav  = NanoElectron.genPartFlav
        #ielectron.genPartIdx   = NanoElectron.genPartIdx
        
        ielectron.chargedHadronIso = NanoElectron.pfRelIso03_chg
        ielectron.iso_pflow        = NanoElectron.pfRelIso03_all # PF isolation in dR<0.3 cone, EA-subtracted

	ielectron.VID              = NanoElectron.vidNestedWPBitmap
        
        ielectron.convVeto         = NanoElectron.convVeto
                
        velectron = ROOT.TLorentzVector()
        velectron.SetPtEtaPhiM(ielectron.pt,ielectron.eta,ielectron.phi,NanoElectron.mass)
        
        ielectron.E = velectron.E()    

        ElectronColl.append(ielectron)
	
    return ElectronColl

## -- Trigger 
def NanoHLTToCIEMAT( NanoHLTCollection , HLTNames):

    for HLTName in HLTNames:	    
	# print(str(HLTName) +" = "+str(NanoHLTCollection.__getitem__(HLTName)))
	if NanoHLTCollection.__getitem__(HLTName):
	    return True
	    
    return False
        

## -- GenInfo
#def NanoGenInfoToCIEMAT( NanoGenInfoCollection, NanoPUCollection, LHEWOrgXWGTUP, nLHEPart, LHEScaleWeight, NanoPSWeight, LHEPdfWeight ):
def NanoGenInfoToCIEMAT( NanoGenInfoCollection, NanoPUCollection, LHEWOrgXWGTUP, LHEScaleWeight, NanoPSWeight, LHEPdfWeight ):

    igenInfo = SkimGenInfo ()
    
    # - PileUp 
    igenInfo.trueNumberOfInteractions = int (NanoPUCollection.nTrueInt)

    # - GenLevel
    igenInfo.id1 = NanoGenInfoCollection.id1
    igenInfo.id2 = NanoGenInfoCollection.id2
    igenInfo.x1  = NanoGenInfoCollection.x1
    igenInfo.x2  = NanoGenInfoCollection.x2

    igenInfo.scalePDF      = NanoGenInfoCollection.scalePDF
    igenInfo.MCWeight      = NanoGenInfoCollection.weight
    igenInfo.LHEWOrgXWGTUP = LHEWOrgXWGTUP
    
    # LHE Weights
    #igenInfo.nLHEPart = nLHEPart

    # Scale Weights
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # WARNING: Different order than the one at MiniAOD
    # 2 and 6 are unphysical anti-correlated variations
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #LHE scale variation weights (w_var / w_nominal) 
    # [0] is renscfact=0.5d0 facscfact=0.5d0  
    # [1] is renscfact=0.5d0 facscfact=1d0  
    # [2] is renscfact=0.5d0 facscfact=2d0  
    # [3] is renscfact=1d0 facscfact=0.5d0  
    # [4] is renscfact=1d0 facscfact=1d0  
    # [5] is renscfact=1d0 facscfact=2d0  
    # [6] is renscfact=2d0 facscfact=0.5d0  
    # [7] is renscfact=2d0 facscfact=1d0  
    # [8] is renscfact=2d0 facscfact=2d0

    for isw in LHEScaleWeight:
        igenInfo.ScaleWeights.append(isw)

    # PS variations: ISR and FSR
    # PS weights (w_var / w_nominal); 
    # [0] is ISR=0.5 FSR=1; [1] is ISR=1 FSR=0.5; [2] is ISR=2 FSR=1; [3] is ISR=1 FSR=2
    for ipsw in NanoPSWeight:
        igenInfo.PSWeights.append(ipsw)

    # PDF Weights 
    # LHE pdf variation weights (w_var / w_nominal) for LHA IDs 91400 - 91432
    for ipdfw in LHEPdfWeight:
        igenInfo.PDFWeights.append(ipdfw)
    
    return igenInfo


# -- GenParticles
def NanoGenPartToCIEMAT( GenParticles ):

    agenPartSel    = []
    agenPartSelMom = []
    
    # gen status flags stored bitwise, bits are: 
    # 0 : isPrompt, 
    # 1 : isDecayedLeptonHadron, 
    # 2 : isTauDecayProduct, 
    # 3 : isPromptTauDecayProduct, 
    # 4 : isDirectTauDecayProduct, 
    # 5 : isDirectPromptTauDecayProduct, 
    # 6 : isDirectHadronDecayProduct, 
    # 7 : isHardProcess, 
    # 8 : fromHardProcess, 
    # 9 : isHardProcessTauDecayProduct, 
    # 10 : isDirectHardProcessTauDecayProduct, 
    # 11 : fromHardProcessBeforeFSR, 
    # 12 : isFirstCopy, 
    # 13 : isLastCopy, 
    # 14 : isLastCopyBeforeFSR,

    for gp in GenParticles: 
	
	ParID = abs( gp.pdgId )
	MomID = abs( GenParticles[gp.genPartIdxMother].pdgId ) if gp.genPartIdxMother > 0 else 0

    	# b or t, W Mother a W
    	if ( ParID == 6  or ParID == 5 or ParID == 24 or MomID == 24 ): 
	    # print str(GenParticles[gp.genPartIdxMother].pdgId) + " -> " + str( gp.pdgId) 
	    # # --------------------------------------
	    # # Flag validation
	    # # --------------------------------------
	    # print "Flag = " + str(gp.statusFlags) + " = " + bin(gp.statusFlags)
	    # print "pdgid = " + str(ParID)
	    # print "isPrompt statusFlags[0] = " +  str(CheckFlag(gp.statusFlags,0))
	    # print "isDecayedLeptonHadron statusFlags[1] = " +  str(CheckFlag(gp.statusFlags,1))
	    # print "isTauDecayProduct statusFlags[2] = " +  str(CheckFlag(gp.statusFlags,2))
	    # print "isPromptTauDecayProduct statusFlags[3] = " +  str(CheckFlag(gp.statusFlags,3))
	    # print "isDirectTauDecayProduct statusFlags[4] = " +  str(CheckFlag(gp.statusFlags,4))
	    # print "isDirectPromptTauDecayProduct statusFlags[5] = " +  str(CheckFlag(gp.statusFlags,5))
	    # print "isDirectHadronDecayProduct statusFlags[6] = " +  str(CheckFlag(gp.statusFlags,6))
	    # print "isHardProcess statusFlags[7] = " +  str(CheckFlag(gp.statusFlags,7))
	    # print "fromHardProcess statusFlags[8] = " +  str(CheckFlag(gp.statusFlags,8))
	    # print "isHardProcessTauDecayProduct statusFlags[9] = " +  str(CheckFlag(gp.statusFlags,9))
	    # print "isDirectHardProcessTauDecayProduct statusFlags[10] = " +  str(CheckFlag(gp.statusFlags,10))
	    # print "fromHardProcessBeforeFSR statusFlags[11] = " +  str(CheckFlag(gp.statusFlags,11))
	    # print "isFirstCopy statusFlags[12] = " +  str(CheckFlag(gp.statusFlags,12))
	    # print "isLastCopy statusFlags[13] = " +  str(CheckFlag(gp.statusFlags,13))
	    # print "isLastCopyBeforeFSR statusFlags[14] = " +  str(CheckFlag(gp.statusFlags,14))

    	    # statusFlags[11]: fromHardProcessBeforeFSR 
    	    if ( not CheckFlag(gp.statusFlags,11) and (ParID == 6 or ParID == 24) ):
    		continue

    	    # If is a b not comming from top or W
    	    if ( ParID == 5 and (MomID != 6 and MomID !=24) ):
    		continue;

	    # --------------------------------------
    	    # statusFlags[7]:  isHardProcess	    
    	    # statusFlags[8]:  fromHardProcess() was originally fromHardProcessFinalState()
            # statusFlags[11]: fromHardProcessBeforeFSR
    	    if( not CheckFlag(gp.statusFlags,7)  and 
    		not CheckFlag(gp.statusFlags,8)  and 
    		not CheckFlag(gp.statusFlags,11) ):
    		continue

    	    # Not coming from proton
    	    if( MomID == 2212 ):
    		continue

	    # t, b, W, light quarks and leptons from W 	    
	    if( ParID == 5 or ParID == 6 or ParID == 24 or 
		ParID < 5  or (ParID > 10 and ParID < 17) ):
		agenPartSel.append(gp)    	
                agenPartSelMom.append(MomID)

    genPartColl = []
    for igps in range(len(agenPartSel)):
	genPartColl.append(fillGenPart(agenPartSel[igps],agenPartSelMom[igps]) ) 

    return genPartColl


def CheckFlag(statusFlags,flag):
    return (statusFlags & (1 << flag) != 0)



def fillGenPart(nanoGenPart, nanoGenPartMom):

    genpart = SkimGenParticles ()

    genpart.pdgId    = nanoGenPart.pdgId
    genpart.status   = nanoGenPart.status
    genpart.motherId = nanoGenPartMom

    genpart.pt     = nanoGenPart.pt
    genpart.eta    = nanoGenPart.eta
    genpart.phi    = nanoGenPart.phi
    
    vgp = ROOT.TLorentzVector()    
    vgp.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,nanoGenPart.mass)

    genpart.E = vgp.E();

    return genpart


# -- GenTop (from NtupleProducer)
def GetGENTopInfo(GenParCollection, TopOrAntiTop):
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # WARNING: Reference of helicity fractions in the SM
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    F0_KF = 0.6952 # old choice was 0.6671
    FL_KF = 0.3030 # old choice was 0.3325
    FR_KF = 1. - F0_KF - FL_KF
    # Reference helicity fractions in the SM
    F0_Mlb = 0.7010
    FL_Mlb = 0.2984
    FR_Mlb = 1. - F0_Mlb - FL_Mlb

    TopLeg = SkimTop ()
    
    # Top and decay products
    genTop = ROOT.Math.PtEtaPhiEVector ()
    genW   = ROOT.Math.PtEtaPhiEVector ()
    genb   = ROOT.Math.PtEtaPhiEVector ()
    genUp  = ROOT.Math.PtEtaPhiEVector ()
    genDown= ROOT.Math.PtEtaPhiEVector ()
    
    thereisTop = False
    thereisb   = False
    
    for genPart in GenParCollection: 
    	genPartChargeID    = TopOrAntiTop*genPart.pdgId
    	genMomPartChargeID = TopOrAntiTop*genPart.motherId

    	# Top Products	
    	if ( genPartChargeID == 6):
    	    TopLeg.Top.status = genPart.status # fill the rest below with top = W+b
    	    thereisTop = True

        elif (  genPartChargeID == 5 and genMomPartChargeID != 24 ):
    	    genb.SetCoordinates( genPart.pt, genPart.eta, genPart.phi, genPart.E)
    	    TopLeg.b.mass   = genb.mass()
    	    TopLeg.b.status = genPart.status
    	    TopLeg.b.pt     = genPart.pt
    	    TopLeg.b.eta    = genPart.eta
    	    TopLeg.b.phi    = genPart.phi
    	    TopLeg.b.E      = genPart.E
    	    thereisb = True # included to avoid a crash when Top->qW

    	elif ( genPartChargeID == 24 ):
    	    genW.SetCoordinates( genPart.pt, genPart.eta, genPart.phi, genPart.E)
    	    TopLeg.W.mass   = genW.mass()
    	    TopLeg.W.status = genPart.status
    	    TopLeg.W.pt     = genPart.pt
    	    TopLeg.W.eta    = genPart.eta
    	    TopLeg.W.phi    = genPart.phi
    	    TopLeg.W.E      = genPart.E

    	elif ( genPartChargeID == -11 or genPartChargeID == -13 or genPartChargeID == -15 or
    	       genPartChargeID == -1  or genPartChargeID == -3  or genPartChargeID == -5 ):
    	    genDown.SetCoordinates( genPart.pt, genPart.eta, genPart.phi, genPart.E )
    	    TopLeg.Down.mass   = genDown.mass() if genDown.mass() > 0. else 0.0 
    	    TopLeg.Down.status = genPart.status
    	    TopLeg.Down.pt     = genPart.pt
    	    TopLeg.Down.eta    = genPart.eta 
    	    TopLeg.Down.phi    = genPart.phi 
    	    TopLeg.Down.E      = genPart.E
    	    TopLeg.LepHad      = genPart.pdgId

    	elif ( genPartChargeID == 12 or genPartChargeID == 14 or genPartChargeID == 16 or
    	       genPartChargeID == 2  or genPartChargeID == 4 ):
    	    genUp.SetCoordinates( genPart.pt, genPart.eta, genPart.phi, genPart.E) 
    	    TopLeg.Up.mass   =  genUp.mass() if genUp.mass() > 0. else 0.0 
    	    TopLeg.Up.status = genPart.status
    	    TopLeg.Up.pt     = genPart.pt
    	    TopLeg.Up.eta    = genPart.eta 
    	    TopLeg.Up.phi    = genPart.phi 
    	    TopLeg.Up.E      = genPart.E

    if ( not (thereisTop and thereisb)):
    	return TopLeg
     
    WFromDecays   = ROOT.Math.PtEtaPhiEVector ()
    TopFromDecays = ROOT.Math.PtEtaPhiEVector ()
    Top           = ROOT.Math.PtEtaPhiEVector ()

    WFromDecays   = genUp + genDown;
    TopFromDecays = WFromDecays + genb;
    Top           = genW  + genb;
    
    TopLeg.Top.mass = Top.mass() 
    TopLeg.Top.pt   = Top.pt()
    TopLeg.Top.eta  = Top.eta() 
    TopLeg.Top.phi  = Top.phi() 
    TopLeg.Top.E    = Top.energy()

    genCosth           = computeThetaStar( genDown, Top,           genW,        genb, True)
    genCosthFromDecays = computeThetaStar( genDown, TopFromDecays, WFromDecays, genb, True)

    Mlb = ROOT.Math.PtEtaPhiEVector ()
    Mlb = genDown + genb;
    
    genCosthMlb = ( 2. * Mlb.mass() * Mlb.mass()/(Top.mass()*Top.mass() - genW.mass()*genW.mass()) ) - 1.
    
    distMl = ( F0_Mlb*(1.-genCosthMlb*genCosthMlb)*0.75 + 
    	       FL_Mlb*(1.-genCosthMlb)*(1.-genCosthMlb)*0.375 +
    	       FR_Mlb*(1.+genCosthMlb)*(1.+genCosthMlb)*0.375 )
    
    distKF = ( F0_KF*(1.-ROOT.TMath.Cos(genCosth)*ROOT.TMath.Cos(genCosth))*0.75 + 
    	       FL_KF*(1.-ROOT.TMath.Cos(genCosth))*(1.-ROOT.TMath.Cos(genCosth))*0.375 +
    	       FR_KF*(1.+ROOT.TMath.Cos(genCosth))*(1.+ROOT.TMath.Cos(genCosth))*0.375 )

    # F0 = 1
    rhoF0_Ml = (1.-genCosthMlb*genCosthMlb)*0.75
    # FL = 1
    rhoFL_Ml = (1.-genCosthMlb)*(1.-genCosthMlb)*0.375
    # FR = 1
    rhoFR_Ml = (1.+genCosthMlb)*(1.+genCosthMlb)*0.375
    # F0 = 1
    rhoF0_KF = (1.-ROOT.TMath.Cos(genCosth)*ROOT.TMath.Cos(genCosth))*0.75
    # FL = 1
    rhoFL_KF = (1.-ROOT.TMath.Cos(genCosth))*(1.-ROOT.TMath.Cos(genCosth))*0.375
    # FR = 1
    rhoFR_KF = (1.+ROOT.TMath.Cos(genCosth))*(1.+ROOT.TMath.Cos(genCosth))*0.375
    
    TopLeg.cosThKF  = ROOT.TMath.Cos(genCosth)
    TopLeg.cosThMlb = genCosthMlb
    TopLeg.rwF0Mlb  = rhoF0_Ml/distMl
    TopLeg.rwFRMlb  = rhoFR_Ml/distMl
    TopLeg.rwFLMlb  = rhoFL_Ml/distMl
    TopLeg.rwF0KF   = rhoF0_KF/distKF 
    TopLeg.rwFRKF   = rhoFR_KF/distKF 
    TopLeg.rwFLKF   = rhoFL_KF/distKF 

    return TopLeg

def computeThetaStar( lepP4, topP4, wP4, bP4, ThetaLepb ):

  topRF = ROOT.Math.XYZVector ()
  topRF = topP4.BoostToCM();
  
  wTopRF = ROOT.Math.PxPyPzEVector () 
  wTopRF = ROOT.Math.VectorUtil.boost( wP4, topRF )

  wRF = ROOT.Math.XYZVector ()
  wRF = wTopRF.BoostToCM()
  
  lepTopRF = ROOT.Math.PxPyPzEVector () 
  lepTopRF = ROOT.Math.VectorUtil.boost( lepP4, topRF )
 
  lepWRF   = ROOT.Math.PxPyPzEVector () 
  lepWRF   = ROOT.Math.VectorUtil.boost( lepTopRF, wRF )
  
  bTopRF = ROOT.Math.PxPyPzEVector () 
  bTopRF = ROOT.Math.VectorUtil.boost( bP4, topRF )
  
  bWRF   = ROOT.Math.PxPyPzEVector ()
  bWRF   = ROOT.Math.VectorUtil.boost( -bTopRF, wRF )
  
  thetaStar_Lepb   = ROOT.Math.VectorUtil.Angle( lepWRF, bWRF ) 
  thetaStar_LepTop = ROOT.Math.VectorUtil.Angle( lepWRF, wTopRF ) 
  phiStar = lepWRF.theta()
  
  if (ThetaLepb):
      return thetaStar_Lepb 
  else:
      return thetaStar_LepTop 

## -- Taus
def NanoTauToCIEMAT( NanoTauCollection ):

  TauColl = []

  for NanoTau in NanoTauCollection:

     if not (NanoTau.pt) > 20:  continue
     if not abs(NanoTau.eta) < 2.4:  continue
     if abs(NanoTau.dz)>0.2: continue
     if NanoTau.decayMode not in [0,1,2,10,11]: continue
     if abs(NanoTau.charge)!=1: continue
     if not (NanoTau.idDeepTau2017v2p1VSjet) >= 4: continue #VLoose
     if not (NanoTau.idDeepTau2017v2p1VSe)   >= 4: continue #VLoose
     if not (NanoTau.idDeepTau2017v2p1VSmu)  >= 1: continue #VLoose

     itau = SkimTaus()
        
     itau.pt     = NanoTau.pt  
     itau.eta    = NanoTau.eta 
     itau.phi    = NanoTau.phi 
     itau.charge = NanoTau.charge
     itau.mass   = NanoTau.mass   
        
     itau.dxy   = NanoTau.dxy  # signed transverse distance to primary vertex [cm]
     itau.dz    = NanoTau.dz   # signed longitudinal distance to primary vertex at min. transv. distance [cm]

     itau.decayMode   = NanoTau.decayMode
     #itau.idDecayModeNewDMs = NanoTau.idDecayModeNewDMs
     #itau.genPartFlav = NanoTau.genPartFlav
     #itau.genPartIdx  = NanoTau.genPartIdx

     itau.idDeepTau2017v2p1VSe   = NanoTau.idDeepTau2017v2p1VSe
     itau.idDeepTau2017v2p1VSmu  = NanoTau.idDeepTau2017v2p1VSmu
     itau.idDeepTau2017v2p1VSjet = NanoTau.idDeepTau2017v2p1VSjet

     itau.jetIdx  = NanoTau.jetIdx
     itau.puCorr  = NanoTau.puCorr

     vtau = ROOT.TLorentzVector()
     vtau.SetPtEtaPhiM(itau.pt,itau.eta,itau.phi,itau.mass)
     itau.E = vtau.E()
        
     TauColl.append(itau)

  return TauColl

def NanoGenTauToCIEMAT( NanoGenTauCollection ):

  GenTauColl = []

  for NanoGenTau in NanoGenTauCollection:

     igentau = SkimGenVisTau()

     igentau.pt     = NanoGenTau.pt
     igentau.eta    = NanoGenTau.eta
     igentau.phi    = NanoGenTau.phi
     igentau.charge = NanoGenTau.charge
     igentau.mass   = NanoGenTau.mass

     igentau.status            = NanoGenTau.status
     igentau.genPartIdxMother  = NanoGenTau.genPartIdxMother

     vgentau = ROOT.TLorentzVector()
     vgentau.SetPtEtaPhiM(igentau.pt,igentau.eta,igentau.phi,igentau.mass)
     igentau.E = vgentau.E()

     GenTauColl.append(igentau)

  return GenTauColl




