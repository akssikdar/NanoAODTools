import ROOT
import os

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import InputTree


from PhysicsTools.NanoAODTools.postprocessing.UserCode.FillNanoAODCIEMAT import *
from PhysicsTools.NanoAODTools.postprocessing.UserCode.ObjectsDef import *

class NanoAODSkim(Module): 
    def __init__(self,InpSample,InpYear,InpOutName,InpCRAB):

	self.DirName = InpOutName[0]
	self.RefName = InpOutName[1]
	self.Year    = InpYear
	self.IsCRAB  = InpCRAB
	self.DS_MC   = False
	self.DS_TOP  = False
	self.DS_MuJ  = False
	self.DS_ElJ  = False
	self.DS_MuMu = False
	self.DS_ElEl = False
	self.DS_MuEl = False
	
	# - MC Sample
	if InpSample == "mc":
	    self.DS_MC = True
	# - TOP (ttbar,t,tbar)
	elif InpSample == "top":
	    self.DS_MC  = True
	    self.DS_TOP = True
	# - DATA	
	elif InpSample == "mujets":
	    self.DS_MuJ    = True
	elif InpSample == "ejets":
	    self.DS_ElJ    = True
	elif InpSample == "mumu":
	    self.DS_MuMu   = True
	elif InpSample == "ee":
	    self.DS_ElEl   = True
	elif InpSample == "mue":
	    self.DS_MuEl   = True
        
        self.JESNames = ["AbsoluteStat","AbsoluteScale","AbsoluteMPFBias",
                         "Fragmentation",
                         "SinglePionECAL","SinglePionHCAL",
                         "FlavorQCD",
                         "TimePtEta",
                         "RelativeJEREC1","RelativeJEREC2","RelativeJERHF",
                         "RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF",
                         "RelativeBal",
                         "RelativeFSR",
                         "RelativeStatFSR","RelativeStatEC","RelativeStatHF",
                         "PileUpDataMC",
                         "PileUpPtRef","PileUpPtBB","PileUpPtEC1","PileUpPtHF"]
        
        #self.JESNames = ["AbsoluteStat","AbsoluteScale"]
        #self.btagNames = ["jes"]
        
        self.btagNames = ["lf", "lfstats1", "lfstats2",
                          "hf", "hfstats1", "hfstats2",
                          "cferr1","cferr2",
                          "jes"]
        
        self.MET_FilterNames = ["METFilters" ,
                                "HBHENoiseFilter",
                                "HBHENoiseIsoFilter"  ,
                                "EcalDeadCellTriggerPrimitiveFilter" ,
                                "goodVertices" ,
                                "eeBadScFilter" ,
                                "globalSuperTightHalo2016Filter",
                                "BadPFMuonFilter"]
        
        pass

    def beginJob(self):
        print("Begin Job................")
	
        if (self.DS_MuJ or self.DS_ElJ or
	    self.DS_MuMu or self.DS_ElEl or self.DS_MuEl):
	    self.DS_TOP = False
	    self.DS_MC  = False
	    print ("[INFO] Configuration to run over DATA...")
            self.JESNames = []
            self.btagNames = []
	else:
	    self.DS_MC = True
	    print ("[INFO] Configuration to run over MC...")
	    if self.DS_TOP:
		print ("[INFO] TOP GEN Particle information will be included...")

        # -- Output name configuration
        # File name
	if self.IsCRAB:
	    TreeFileName = "tree.root.hist"
	else:
	    TreeFileName = self.DirName + "/" + self.RefName + ".hist"
        print "Output file: " + TreeFileName
        
        # Create output root file
        self.f = ROOT.TFile( TreeFileName, 'recreate' )        

        NormHistoNames = ["N Evt","W Evt","Skim Evt",
                          "Scale[0]: muRDown MuFDown","Scale[1]: muRDown MuFNom","Scale[2]: muRDown MuFUp",
                          "Scale[3]: muRNom  MuFDown","Scale[4]: muRNom  MuFNom","Scale[5]: muRNom  MuFUp",
                          "Scale[6]: muRUp   MuFDown","Scale[7]: muRUp   MuFNom","Scale[8]: muRUp   MuFUp"
                          "PS[0]: ISRDown FSRNom","PS[1]: ISRNom  FSRDown","PS[2]: ISRUp   FSRNom","PS[3]: ISRNom  FSRUp"]

        self.h_Evt   = ROOT.TH1D("LHEweights","LHEweights", len(NormHistoNames), 0, len(NormHistoNames) )

        for ihn in range(len(NormHistoNames)):
            self.h_Evt.GetXaxis().SetBinLabel(ihn+1,NormHistoNames[ihn]);

	print ("[FILE] File with HISTOGRAMS created...")
        pass
        
    def endJob(self):
        print("End Job.................")
        self.f.Write()
        self.f.Close()
	pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print("Begin File................")
        self.initReaders(inputTree) # initReaders must be called in beginFile

        self.out = wrappedOutputTree
        
        # -------------------  All new branches  ------------------- #
        # Event Variables
        self.out.branch("event",     "L");
        self.out.branch("run",       "L");
        self.out.branch("lumiBlock", "I");

        self.out.branch("rho",     "F");
        self.out.branch("nVertex", "I");
        self.out.branch("pvX",     "F");
        self.out.branch("pvY",     "F");
        self.out.branch("pvZ",     "F");

        self.out.branch("puWeight",    "F");
        self.out.branch("puWeightUp",  "F");
        self.out.branch("puWeightDown","F");

        self.out.branch("passHLT","I");

	self.out.branch("WL1PreFiring",    "F");
	self.out.branch("WL1PreFiringUp",  "F");
	self.out.branch("WL1PreFiringDown","F");

        # JETS
        for ijb in SkimJets().__dict__.keys():
            if "JESUp" in ijb:
                for ijesb in self.JESNames:
                    self.out.branch("jet_JES%sUp"%ijesb,  "F",lenVar="nJet");
                    self.out.branch("jet_JES%sDown"%ijesb,"F",lenVar="nJet");
            elif "btagUp" in ijb:
                for ibtagb in self.btagNames:
                    self.out.branch("jet_btag%sUp"%ibtagb,  "F",lenVar="nJet");
                    self.out.branch("jet_btag%sDown"%ibtagb,"F",lenVar="nJet");
            elif "JESDown" in ijb or "btagDown" in ijb:
                continue
            else:
                if isinstance( getattr(SkimJets(),ijb), int ): typeVar = "I"
                else: typeVar = "F"
                self.out.branch("jet_%s"%ijb,typeVar,lenVar="nJet");

        # Taus
        for itb in SkimTaus().__dict__.keys():
            if isinstance( getattr(SkimTaus(),itb), int ): typeVar = "I"
            else: typeVar = "F"
            self.out.branch("tau_%s"%itb,typeVar,lenVar="nTau");

        # Gen Taus
        for igtb in SkimGenVisTau().__dict__.keys():
            if isinstance( getattr(SkimGenVisTau(),igtb), int ): typeVar = "I"
            else: typeVar = "F"
            #print("Gen tau variables: ", igtb)
            self.out.branch("tau_%s"%igtb,typeVar,lenVar="nGenVisTau");

        # Muons
        for imb in SkimMuons().__dict__.keys():
            if isinstance( getattr(SkimMuons(),imb), int ): typeVar = "I"
            else: typeVar = "F"
            self.out.branch("muon_%s"%imb,typeVar,lenVar="nMuon");

        # Electrons
        for ieb in SkimElectrons().__dict__.keys():
            if isinstance( getattr(SkimElectrons(),ieb), int ): typeVar = "I"
            else: typeVar = "F"
            self.out.branch("electron_%s"%ieb,typeVar,lenVar="nElectron");

        # MET
        for imetb in SkimMET().__dict__.keys():
            self.out.branch("met_%s"%imetb,"F");
                        
        # MET Filters
        for imetfb in self.MET_FilterNames:
            self.out.branch("metFilter_%s"%imetfb,"F");

        # MC Generetor Information
        if self.DS_MC:
            for igib in SkimGenInfo().__dict__.keys():
                if  not("Weights" in igib):
                    self.out.branch("genInfo_%s"%igib,"F");
            self.out.branch("genInfo_ScaleWeights","F",lenVar="nLHEScaleWeight");
            self.out.branch("genInfo_PSWeights","F",lenVar="nPSWeight");
            self.out.branch("genInfo_PDFWeights","F",lenVar="nLHEPdfWeight");
                                    
        if self.DS_TOP:
            # GenParticles
            for igpb in SkimGenParticles().__dict__.keys():
                if isinstance( getattr(SkimGenParticles(),igpb), int ): typeVar = "I"
                else: typeVar = "F"
                self.out.branch("genParticles_%s"%igpb,typeVar,lenVar="nGenPart");

            # Top system particles
            for igpb in SkimGenParticles().__dict__.keys():
                if isinstance( getattr(SkimGenParticles(),igpb), int ): typeVar = "I"
                else: typeVar = "F"
                self.out.branch("topGenParticles_%s"%igpb,typeVar,5);
            # Topbar system particles
            for igpb in SkimGenParticles().__dict__.keys():
                if isinstance( getattr(SkimGenParticles(),igpb), int ): typeVar = "I"
                else: typeVar = "F"
                self.out.branch("topbarGenParticles_%s"%igpb,typeVar,5);

            # Top
            self.out.branch("top_cosThKF",  "F");
            self.out.branch("top_cosThMlb", "F");
            self.out.branch("top_LepHad",   "F");
            self.out.branch("top_rwF0Mlb",  "F");
            self.out.branch("top_rwFLMlb",  "F");
            self.out.branch("top_rwFRMlb",  "F");
            self.out.branch("top_rwF0KF",   "F");
            self.out.branch("top_rwFLKF",   "F");
            self.out.branch("top_rwFRKF",   "F");
            # Topbar
            self.out.branch("topbar_cosThKF",  "F");
            self.out.branch("topbar_cosThMlb", "F");
            self.out.branch("topbar_LepHad",   "F");
            self.out.branch("topbar_rwF0Mlb",  "F");
            self.out.branch("topbar_rwFLMlb",  "F");
            self.out.branch("topbar_rwFRMlb",  "F");
            self.out.branch("topbar_rwF0KF",   "F");
            self.out.branch("topbar_rwFLKF",   "F");
            self.out.branch("topbar_rwFRKF",   "F");

        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print("End File................")
        pass


    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        # Event Info
        print("Init Reader................")

	# Trigger Definitions (Name without 'HLT_')
	self.HLTData = {}
	self.HLTData["2016_mujets"] = ["IsoMu24","IsoTkMu24"] # 2016 Muon
        self.HLTData["2016_ejets" ] = [#"Ele32_WPTight_Gsf",   # This trigger is ONLY available in Run H
				       "Ele32_eta2p1_WPTight_Gsf","Ele27_eta2p1_WPTight_Gsf"] # 2016 Electron
	self.HLTData["2017_mujets"] = ["IsoMu27"]             # 2017 Muon
	self.HLTData["2017_ejets" ] = ["Ele32_WPTight_Gsf_L1DoubleEG"]   # 2017 Electron
	self.HLTData["2018_mujets"] = ["IsoMu24"]             # 2018 Muon
	self.HLTData["2018_ejets" ] = ["Ele32_WPTight_Gsf"]   # 2018 Electron
	
        self.HLTList = []

	if self.DS_MuJ:
	    self.HLTList = self.HLTData[self.Year+"_mujets"]
	elif self.DS_ElJ:
	    self.HLTList = self.HLTData[self.Year+"_ejets"]
	elif self.DS_MC:
	    self.HLTList = self.HLTData[self.Year+"_mujets"] + self.HLTData[self.Year+"_ejets"]
	
	# Triggers to be use
	print("HLT trigger names: " + str(self.HLTList))
        
    # Adding branches to the NanoAOD
    def analyze(self, event): 
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # -- Histogram
        self.h_Evt.Fill(0.) # N Evt
        EvtWeight = 1.
	if self.DS_MC and hasattr(event, 'LHEWeight_originalXWGTUP'):
            EvtWeight = event.LHEWeight_originalXWGTUP/abs(event.LHEWeight_originalXWGTUP) # W Evt
	    
        self.h_Evt.Fill(1.,EvtWeight) # W Evt



	# -- Object Collections
        CIEMATColl_Taus      = NanoTauToCIEMAT    ( Collection(event, "Tau") )
        CIEMATColl_Muons     = NanoMuonToCIEMAT    ( Collection(event, "Muon") )
        CIEMATColl_Electrons = NanoElectronToCIEMAT( Collection(event, "Electron") )
	CIEMATColl_METFilters= NanoMETFiltersToCIEMAT ( Object (event, "Flag"), self.MET_FilterNames )

	# -- TOP gen information: Keep all events
        KeepEvt = True

	if self.DS_TOP:
	    CIEMATColl_GenPart   = NanoGenPartToCIEMAT ( Collection(event, "GenPart") )
	    CIEMATnTuple_Top     =  GetGENTopInfo ( CIEMATColl_GenPart,  1 )
	    CIEMATnTuple_TopBar  =  GetGENTopInfo ( CIEMATColl_GenPart, -1 )

	else:
	    CIEMATColl_GenPart   = SkimGenParticles()
	    CIEMATnTuple_Top     = SkimTop ()
	    CIEMATnTuple_TopBar  = SkimTop ()

        # -- Skim cuts if is NOT TOP
        # - Trigger
        PassTrigger = True
        if not NanoHLTToCIEMAT(Object(event, "HLT"), self.HLTList):
            # print("Rejected by Trigger")
            PassTrigger = False

        # - Number of leptons skim (at least 1 muon)
        if (len(CIEMATColl_Muons) == 0 and len(CIEMATColl_Electrons) == 0 and len(CIEMATColl_Taus) == 0 ):
            # print ("Rejected by number of leptons")
            KeepEvt = False

	# -- Weights
	vLHEScaleWeight = []
	vLHEPdfWeight   = []
	vPSWeight       = []	
	# - MC Collections (not set for real data)
        CIEMAT_GenInfo   = None

	# - ONLY MC
	if self.DS_MC:
            # - Gen tau from MC
            CIEMATColl_GenVisTau     = NanoGenTauToCIEMAT    ( Collection(event, "GenVisTau") )	
	    # - Jet objects from MC
	    #CIEMATColl_Jets      = NanoJetToCIEMAT      ( Collection(event, "Jet"), self.JESNames, self.btagNames )
            CIEMATColl_Jets      = NanoJetNoSYSTToCIEMAT ( Collection(event, "Jet"))
	    #CIEMATColl_MET       = NanoMETToCIEMAT      ( Object    (event, "MET") )
            CIEMATColl_MET       = NanoMETNoSYSTToCIEMAT ( Object    (event, "MET") )

	    CIEMAT_GenInfo = SkimGenInfo ()
	    IsMCInfo =  hasattr(event, 'LHEScaleWeight') and hasattr(event, 'LHEPdfWeight') and hasattr(event, 'PSWeight')

	    # In the case that MC samples contain Theory variations 
	    # - Scale (muR and muF at ME)
	    if  IsMCInfo:
	    	for isw in range(len(event.LHEScaleWeight)):
	    	    vLHEScaleWeight.append(event.LHEScaleWeight[isw])
                    self.h_Evt.Fill(3.+isw,event.LHEScaleWeight[isw]) # Scale Evt
		# - PDF (100 weights)
		for ipdfw in range(len(event.LHEPdfWeight)):
	    	    vLHEPdfWeight.append(event.LHEPdfWeight[ipdfw])
		# PS: ISR and FSR
		for ipsw in range(len(event.PSWeight)):
	    	    vPSWeight.append(event.PSWeight[ipsw])
                    self.h_Evt.Fill(12.+ipsw,event.PSWeight[ipsw]) # PS Evt
	    	# -- Collections from NanoAOD
	    	CIEMAT_GenInfo   = NanoGenInfoToCIEMAT ( Object(event, "Generator"), 
	    						     Object(event, "Pileup"),
	    						     event.LHEWeight_originalXWGTUP,
	    						     #event.nLHEPart,
	    						     vLHEScaleWeight,
	    						     vPSWeight,
	    						     vLHEPdfWeight)
	    else:
	    	CIEMAT_GenInfo = SkimGenInfo ()


	# - DATA w/o MC collections/information
	else:
	    # Collections for DATA w/o uncertainties 
	    CIEMATColl_Jets      = NanoJetNoSYSTToCIEMAT ( Collection(event, "Jet"))
	    CIEMATColl_MET       = NanoMETNoSYSTToCIEMAT ( Object    (event, "MET") )
	    # PU
	    event.puWeight     = 0.
	    event.puWeightUp   = 0.
	    event.puWeightDown = 0.
	    # GenInfo
	    CIEMAT_GenInfo = SkimGenInfo ()


        if not KeepEvt:
            # - Keep only GEN info for TOP
            if self.DS_TOP:
                CIEMATColl_Jets = [] # remove jets (reduce size in full hadronic)
            else:                
                return False



	# -- Fill CIEMAT tree
        self.h_Evt.Fill(2.,EvtWeight) # PS Evt
        # Fill branches
        # -------------------  Fill branches  ------------------- #
        # Event Variables
        self.out.fillBranch("event",     event.event);
        self.out.fillBranch("run",       event.run);
        self.out.fillBranch("lumiBlock", event.luminosityBlock);

        self.out.fillBranch("rho",     event.fixedGridRhoFastjetCentralNeutral);
        self.out.fillBranch("nVertex", event.PV_npvsGood);
        self.out.fillBranch("pvX",     event.PV_x);
        self.out.fillBranch("pvY",     event.PV_y);
        self.out.fillBranch("pvZ",     event.PV_z);

        #self.out.fillBranch("puWeight",    event.puWeight);
        #self.out.fillBranch("puWeightUp",  event.puWeightUp);
        #self.out.fillBranch("puWeightDown",event.puWeightDown);
        
	# 2017 L1PreFiring weight
	if self.Year == 2017:
	    self.out.fillBranch("WL1PreFiring",     event.L1PreFiringWeight_Nom);
	    self.out.fillBranch("WL1PreFiringUp",   event.L1PreFiringWeight_Up);
	    self.out.fillBranch("WL1PreFiringDown", event.L1PreFiringWeight_Dn);
	    
        # Trigger
        self.out.fillBranch("passHLT",PassTrigger);

        # JETS
        #for ijb in SkimJets().__dict__.keys():
        '''
            if "JESUp" in ijb:
                for ijesb in range(len(self.JESNames)):
                    aJetJESUp   = []
                    aJetJESDown = []
                    for fj in CIEMATColl_Jets:
                        aJetJESUp.append  (fj.systJESUp  [ijesb])
                        aJetJESDown.append(fj.systJESDown[ijesb])
                    self.out.fillBranch("jet_JES%sUp"%self.JESNames[ijesb],  aJetJESUp );
                    self.out.fillBranch("jet_JES%sDown"%self.JESNames[ijesb],aJetJESDown );
            elif "btagUp" in ijb:
                for ibtagb in range(len(self.btagNames)):
                    aJetbtagUp   = []
                    aJetbtagDown = []
                    for fj in CIEMATColl_Jets:
                        aJetbtagUp.append  (fj.systbtagUp  [ibtagb])
                        aJetbtagDown.append(fj.systbtagDown[ibtagb])
                    self.out.fillBranch("jet_btag%sUp"%self.btagNames[ibtagb],  aJetbtagUp);
                    self.out.fillBranch("jet_btag%sDown"%self.btagNames[ibtagb],aJetbtagDown);
            elif "JESDown" in ijb or "btagDown" in ijb:
                continue
            else:
        '''
        for ijb in SkimJets().__dict__.keys():
            aJet = []
            for fj in CIEMATColl_Jets:
                aJet.append( getattr(fj,ijb) )
            self.out.fillBranch("jet_%s"%ijb, aJet);

        # Taus
        for itb in SkimTaus().__dict__.keys():
            aTau = []
            for ft in CIEMATColl_Taus:       
                aTau.append( getattr(ft,itb) )
            self.out.fillBranch("tau_%s"%itb, aTau);
        
        # GenTaus
        if self.DS_MC: #==False and self.DS_TOP==False:
            for igtb in SkimGenVisTau().__dict__.keys():
                agenTau = []
                #print("filling gen tau: ", igtb)
                for ft in CIEMATColl_GenVisTau:
                    agenTau.append( getattr(ft,igtb) )
                self.out.fillBranch("tau_%s"%igtb, agenTau);
 
        # Muons
        for imb in SkimMuons().__dict__.keys():
            aMuon = []
            for fm in CIEMATColl_Muons:       
                aMuon.append( getattr(fm,imb) )
            self.out.fillBranch("muon_%s"%imb, aMuon);

        # Electrons
        for ieb in SkimElectrons().__dict__.keys():
            aElectron = []
            for fe in CIEMATColl_Electrons:
                aElectron.append( getattr(fe,ieb) )
            self.out.fillBranch("electron_%s"%ieb,aElectron);

        # MET
        for imetb in SkimMET().__dict__.keys():
            self.out.fillBranch("met_%s"%imetb, getattr(CIEMATColl_MET,imetb) );

        # MET Filters
        for imetfb in range(len(self.MET_FilterNames)):
            self.out.fillBranch("metFilter_%s"%self.MET_FilterNames[imetfb],CIEMATColl_METFilters[imetfb] );

        # MC Generetor Information
        if self.DS_MC and IsMCInfo:
            for igib in SkimGenInfo().__dict__.keys():
                    self.out.fillBranch("genInfo_%s"%igib, getattr(CIEMAT_GenInfo,igib) );

        if self.DS_TOP:
            # GenParticles
            for igpb in SkimGenParticles().__dict__.keys():
                aGenParticles = []
                for fp in CIEMATColl_GenPart:
                    aGenParticles.append( getattr(fp,igpb) )
                self.out.fillBranch("genParticles_%s"%igpb,aGenParticles);

            # Top system particles
            self.out.fillBranch("top_cosThKF", CIEMATnTuple_Top.cosThKF);
            self.out.fillBranch("top_cosThMlb",CIEMATnTuple_Top.cosThMlb);
            self.out.fillBranch("top_LepHad",  CIEMATnTuple_Top.LepHad);
            self.out.fillBranch("top_rwF0Mlb", CIEMATnTuple_Top.rwF0Mlb);
            self.out.fillBranch("top_rwFLMlb", CIEMATnTuple_Top.rwFLMlb);
            self.out.fillBranch("top_rwFRMlb", CIEMATnTuple_Top.rwFRMlb);
            self.out.fillBranch("top_rwF0KF",  CIEMATnTuple_Top.rwF0KF);
            self.out.fillBranch("top_rwFLKF",  CIEMATnTuple_Top.rwFLKF);
            self.out.fillBranch("top_rwFRKF",  CIEMATnTuple_Top.rwFRKF);

            for igpb in SkimGenParticles().__dict__.keys():
                aGenParticles = []
                # [0]=Top [1]=b [2]=W [3]=Up [4]=Down
                aGenParticles.append( getattr(CIEMATnTuple_Top.Top,igpb)  )
                aGenParticles.append( getattr(CIEMATnTuple_Top.b,igpb)    )
                aGenParticles.append( getattr(CIEMATnTuple_Top.W,igpb)    )
                aGenParticles.append( getattr(CIEMATnTuple_Top.Up,igpb)   )
                aGenParticles.append( getattr(CIEMATnTuple_Top.Down,igpb) )
                
                self.out.fillBranch("topGenParticles_%s"%igpb,aGenParticles);
            
            # Topbar system particles
            self.out.fillBranch("topbar_cosThKF", CIEMATnTuple_TopBar.cosThKF);
            self.out.fillBranch("topbar_cosThMlb",CIEMATnTuple_TopBar.cosThMlb);
            self.out.fillBranch("topbar_LepHad",  CIEMATnTuple_TopBar.LepHad);
            self.out.fillBranch("topbar_rwF0Mlb", CIEMATnTuple_TopBar.rwF0Mlb);
            self.out.fillBranch("topbar_rwFLMlb", CIEMATnTuple_TopBar.rwFLMlb);
            self.out.fillBranch("topbar_rwFRMlb", CIEMATnTuple_TopBar.rwFRMlb);
            self.out.fillBranch("topbar_rwF0KF",  CIEMATnTuple_TopBar.rwF0KF);
            self.out.fillBranch("topbar_rwFLKF",  CIEMATnTuple_TopBar.rwFLKF);
            self.out.fillBranch("topbar_rwFRKF",  CIEMATnTuple_TopBar.rwFRKF);

            for igpb in SkimGenParticles().__dict__.keys():
                aGenParticles = []
                # [0]=Top [1]=b [2]=W [3]=Up [4]=Down
                aGenParticles.append( getattr(CIEMATnTuple_TopBar.Top,igpb)  )
                aGenParticles.append( getattr(CIEMATnTuple_TopBar.b,igpb)    )
                aGenParticles.append( getattr(CIEMATnTuple_TopBar.W,igpb)    )
                aGenParticles.append( getattr(CIEMATnTuple_TopBar.Up,igpb)   )
                aGenParticles.append( getattr(CIEMATnTuple_TopBar.Down,igpb) )
                
                self.out.fillBranch("topbarGenParticles_%s"%igpb,aGenParticles);
            
        return True # It wont fill the NanoOutput

# Still missing how to transfer information to the initial configuration    
createNanoAODSkim = lambda InpSample, InpYear, InpOutName, InpCRAB : NanoAODSkim(InpSample,InpYear,InpOutName,InpCRAB)
