#include <stdio.h>
#include <iostream>
#include "Riostream.h"
#include "TBranch.h"
#include "TFile.h"
#include "TChain.h"
#include "TH2F.h"
#include "TProfile.h"
#include <fstream>
#include <string>
#include <map>
#include <set>
#include <fstream>
#include <stdexcept>
#include <cstdlib>
#include <TROOT.h>
#include <TMath.h>

// Macro to make a BH flat ntuple. John Hakala 12/1/2015

void BHflatTuplizer(std::string inFilename, std::string outFilename, std::string metListFilename);
float dR(float eta1, float phi1, float eta2, float phi2);
float invMass(float vector4[4]);
std::map<unsigned, std::set<unsigned> > readEventList(char const* _fileName);

// inFilename    = NTuple input
// outFilename   = output root
//  metListFilename = txt of un-filtered MET events
//  PtCut        = Lower PtCut for Jet/Electron/Photon/MET
//  is2016H      = Switch to recover 2016H trigger inefficiency
void BHflatTuplizer(std::string inFilename, std::string outFilename, std::string metListFilename, bool is2016H, double PtCut) {
  std::map<unsigned, std::set<unsigned> > list = readEventList(metListFilename.c_str());
  bool isData        = true;
  bool debugFlag     = false ;
  int  eventsToDump  = 25    ;  // if debugFlag is true, then stop once the number of dumped events reaches eventsToDump
  bool dumpBigEvents = false ;
  bool dumpIsoInfo   = false ;
  int  nDumpedEvents = 0     ;
  bool useMETcut     = false ;
  int  nBin      = 130   ; // 100 for 100 GeV bin, 1000 for 10 GeV bin in ST histograms 
  int  STlow         = 0     ; // Lower bound of ST histogram: 500 GeV or 0 GeV
  int  STup          = 13000 ; // Upper bound of ST histogram


  // define output textfile
  ofstream outTextFile;
  std::string outTextFilename  = outFilename+"_log.tx";
  outTextFile.open(outTextFilename.c_str());

  // define output histograms
  // Basic quantities
  TH1F Ngen     = TH1F("Ngen" ,"Ngen" ,1,0,1);
  TH1F NJets    = TH1F("NJets","NJets",20,0,20);
  TH1F h_NPV    = TH1F("NPV","NPV",100,0,100);
  TH1F NJetPhElMu   = TH1F("NJetPhElMu","NJetPhElMu",20,0,20);
  TH1F h_mBH    = TH1F("mBH"  ,"mBH"  ,130,0,13000);
  TH1F MET      = TH1F("MET"  ,"MET"  ,130,0,13000);
  TH1F OurMET   = TH1F("OurMET"  ,"OurMET"  ,130,0,13000);
  TH1F JetNHF   = TH1F("JetNHF","JetNHF",1000,0,1);
  TH1F JetCHF   = TH1F("JetCHF","JetCHF",1000,0,1);
  TH1F JetNHF_pt1  = TH1F("JetNHF_pt1" ,"JetNHF_pt1",160,0,8000);
  TH1F JetNHF_eta1 = TH1F("JetNHF_eta1","JetNHF_eta1",50,-5,5);
  TH1F JetNHF_pt2 = TH1F("JetNHF_pt2","JetNHF_pt2",160,0,8000);
  TH1F JetNHF_eta2 = TH1F("JetNHF_eta2","JetNHF_eta2",50,-5,5);
  TH1F JetCHF_pt1  = TH1F("JetCHF_pt1" ,"JetCHF_pt1",160,0,8000);
  TH1F JetCHF_eta1 = TH1F("JetCHF_eta1","JetCHF_eta1",50,-5,5);
  TH1F JetCHF_pt2 = TH1F("JetCHF_pt2","JetCHF_pt2",160,0,8000);
  TH1F JetCHF_eta2 = TH1F("JetCHF_eta2","JetCHF_eta2",50,-5,5);


  TProfile NPV_multi = TProfile("NPV_multi","NPV_multi",10,2,12,"s"); 
  TH2F  multi_NPV    = TH2F("multi_NPV","multi_NPV",50,0,50,10,2,12); 

  TH2F METvsMHT                            = TH2F("METvsMHT"                            ,  "METvsMHT"                        ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2                        = TH2F("METvsMHTinc2"                        ,  "METvsMHTinc2"                    ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2hasMuon                 = TH2F("METvsMHTinc2hasMuon"                 ,  "METvsMHTinc2hasMuon"             ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2hasPhoton               = TH2F("METvsMHTinc2hasPhoton"               ,  "METvsMHTinc2hasPhoton"           ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2hasElectron             = TH2F("METvsMHTinc2hasElectron"             ,  "METvsMHTinc2hasElectron"         ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2onlyJets                = TH2F("METvsMHTinc2onlyJets"                ,  "METvsMHTinc2onlyJets"            ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHT_tight                      = TH2F("METvsMHT_tight"                      ,  "METvsMHT_tight"                  ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2_tight                  = TH2F("METvsMHTinc2_tight"                  ,  "METvsMHTinc2_tight"              ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2hasMuon_tight           = TH2F("METvsMHTinc2hasMuon_tight"           ,  "METvsMHTinc2hasMuon_tight"       ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2hasPhoton_tight         = TH2F("METvsMHTinc2hasPhoton_tight"         ,  "METvsMHTinc2hasPhoton_tight"     ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2hasElectron_tight       = TH2F("METvsMHTinc2hasElectron_tight"       ,  "METvsMHTinc2hasElectron_tight"   ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH2F METvsMHTinc2onlyJets_tight          = TH2F("METvsMHTinc2onlyJets_tight"          ,  "METvsMHTinc2onlyJets_tight"      ,  1000,  0.,  20000.,  1000,  0.,  20000.);
  TH1F METoverSumET                      = TH1F("METoverSumET"                      ,  "METoverSumET"                      ,  300,  0.,  3.);
  TH1F METoverSumETinc2                  = TH1F("METoverSumETinc2"                  ,  "METoverSumETinc2"                  ,  300,  0.,  3.);
  TH1F METoverSumETinc2hasMuon           = TH1F("METoverSumETinc2hasMuon"           ,  "METoverSumETinc2hasMuon"           ,  300,  0.,  3.);
  TH1F METoverSumETinc2hasPhoton         = TH1F("METoverSumETinc2hasPhoton"         ,  "METoverSumETinc2hasPhoton"         ,  300,  0.,  3.);
  TH1F METoverSumETinc2hasElectron       = TH1F("METoverSumETinc2hasElectron"       ,  "METoverSumETinc2hasElectron"       ,  300,  0.,  3.);
  TH1F METoverSumETinc2onlyJets          = TH1F("METoverSumETinc2onlyJets"          ,  "METoverSumETinc2onlyJets"          ,  300,  0.,  3.);
  TH1F METoverSumET_tight                = TH1F("METoverSumET_tight"                ,  "METoverSumET_tight"                ,  300,  0.,  3.);
  TH1F METoverSumETinc2_tight            = TH1F("METoverSumETinc2_tight"            ,  "METoverSumETinc2_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc3_tight            = TH1F("METoverSumETinc3_tight"            ,  "METoverSumETinc3_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc4_tight            = TH1F("METoverSumETinc4_tight"            ,  "METoverSumETinc4_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc5_tight            = TH1F("METoverSumETinc5_tight"            ,  "METoverSumETinc5_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc6_tight            = TH1F("METoverSumETinc6_tight"            ,  "METoverSumETinc6_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc7_tight            = TH1F("METoverSumETinc7_tight"            ,  "METoverSumETinc7_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc8_tight            = TH1F("METoverSumETinc8_tight"            ,  "METoverSumETinc8_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc9_tight            = TH1F("METoverSumETinc9_tight"            ,  "METoverSumETinc9_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc10_tight            = TH1F("METoverSumETinc10_tight"            ,  "METoverSumETinc10_tight"            ,  300,  0.,  3.);
  TH1F METoverSumETinc2hasMuon_tight     = TH1F("METoverSumETinc2hasMuon_tight"     ,  "METoverSumETinc2hasMuon_tight"     ,  300,  0.,  3.);
  TH1F METoverSumETinc2hasPhoton_tight   = TH1F("METoverSumETinc2hasPhoton_tight"   ,  "METoverSumETinc2hasPhoton_tight"   ,  300,  0.,  3.);
  TH1F METoverSumETinc2hasElectron_tight = TH1F("METoverSumETinc2hasElectron_tight" ,  "METoverSumETinc2hasElectron_tight" ,  300,  0.,  3.);
  TH1F METoverSumETinc2onlyJets_tight    = TH1F("METoverSumETinc2onlyJets_tight"    ,  "METoverSumETinc2onlyJets_tight"    ,  300,  0.,  3.);

  TH1F MuonJetIso1             = TH1F("MuonJetIso1"             ,  "MuonJetIso1"             ,  300,   0.,  3);
  TH1F MuonJetIso2             = TH1F("MuonJetIso2"             ,  "MuonJetIso2"             ,  300,   0.,  3);
  TH1F MuonJetIso3             = TH1F("MuonJetIso3"             ,  "MuonJetIso3"             ,  300,   0.,  3);
  TH1F MuonJetIso4             = TH1F("MuonJetIso4"             ,  "MuonJetIso4"             ,  300,   0.,  3);
  TH1F MuonJetoverlapdR1       = TH1F("MuonJetIso4overlapdR1"   ,  "MuonJetIso4overlapdR1"   ,  300,   0., .3);
  TH1F MuonJetoverlapdR2       = TH1F("MuonJetIso4overlapdR2"   ,  "MuonJetIso4overlapdR2"   ,  300,   0., .3);
  TH1F MuonJetoverlapdR3       = TH1F("MuonJetIso4overlapdR3"   ,  "MuonJetIso4overlapdR3"   ,  300,   0., .3);
  TH1F MuonJetoverlapdR4       = TH1F("MuonJetIso4overlapdR4"   ,  "MuonJetIso4overlapdR4"   ,  300,   0., .3);
  TH1F ElectronJetIso1         = TH1F("ElectronJetIso1"         ,  "ElectronJetIso1"         ,  300,   0.,  3);
  TH1F ElectronJetIso2         = TH1F("ElectronJetIso2"         ,  "ElectronJetIso2"         ,  300,   0.,  3);
  TH1F ElectronJetIso3         = TH1F("ElectronJetIso3"         ,  "ElectronJetIso3"         ,  300,   0.,  3);
  TH1F ElectronJetIso4         = TH1F("ElectronJetIso4"         ,  "ElectronJetIso4"         ,  300,   0.,  3);
  TH1F ElectronJetoverlapdR1   = TH1F("ElectronJetoverlapdR1"   ,  "ElectronJetoverlapdR1"   ,  300,   0., .3);
  TH1F ElectronJetoverlapdR2   = TH1F("ElectronJetoverlapdR2"   ,  "ElectronJetoverlapdR2"   ,  300,   0., .3);
  TH1F ElectronJetoverlapdR3   = TH1F("ElectronJetoverlapdR3"   ,  "ElectronJetoverlapdR3"   ,  300,   0., .3);
  TH1F ElectronJetoverlapdR4   = TH1F("ElectronJetoverlapdR4"   ,  "ElectronJetoverlapdR4"   ,  300,   0., .3);
  TH1F PhotonJetIso1           = TH1F("PhotonJetIso1"           ,  "PhotonJetIso1"           ,  300,   0.,  3);
  TH1F PhotonJetIso2           = TH1F("PhotonJetIso2"           ,  "PhotonJetIso2"           ,  300,   0.,  3);
  TH1F PhotonJetIso3           = TH1F("PhotonJetIso3"           ,  "PhotonJetIso3"           ,  300,   0.,  3);
  TH1F PhotonJetIso4           = TH1F("PhotonJetIso4"           ,  "PhotonJetIso4"           ,  300,   0.,  3);
  TH1F PhotonJetoverlapdR1     = TH1F("PhotonJetoverlapdR1"     ,  "PhotonJetoverlapdR1"     ,  300,   0., .3);
  TH1F PhotonJetoverlapdR2     = TH1F("PhotonJetoverlapdR2"     ,  "PhotonJetoverlapdR2"     ,  300,   0., .3);
  TH1F PhotonJetoverlapdR3     = TH1F("PhotonJetoverlapdR3"     ,  "PhotonJetoverlapdR3"     ,  300,   0., .3);
  TH1F PhotonJetoverlapdR4     = TH1F("PhotonJetoverlapdR4"     ,  "PhotonJetoverlapdR4"     ,  300,   0., .3);

  // loop to create ST histograms for inclusive and exclusive multiplicities from 2 up to multMax
  TH1F stHist = TH1F("stHist", "ST", nBin, STlow, STup);
  TH1F stHist_tight = TH1F("stHist_tight", "ST_tight", nBin, STlow, STup);
  int mult=2;
  int multMax = 12;
  TH1F *mBH_IncHist[multMax-2];
  TH1F *mBH_ExcHist[multMax-2];
  TH1F *mBH_jet_ExcHist[multMax-2];
  // signal histograms
  TH1F *mBHsig_nJet[multMax-2];
  TH1F *mBHsig_nEle[multMax-2];
  TH1F *mBHsig_nMuon[multMax-2];
  TH1F *mBHsig_nPhoton[multMax-2];
  TH1F *mBHsig_MET[multMax-2];
  TH1F *mBHsig_JetEta[multMax-2];
  TH1F *mBHsig_JetpT[multMax-2];
  TH1F *mBHsig_JetEt[multMax-2];
  TH1F *mBHsig_ST[multMax-2];
  TH1F *mBHsig_STmet50[multMax-2];
  TH1F *mBHsig_STmet100[multMax-2];
  TH1F *mBHsig_STmet200[multMax-2];
  // background histograms
  TH1F *mBHbkg_nJet[multMax-2];
  TH1F *mBHbkg_nEle[multMax-2];
  TH1F *mBHbkg_nMuon[multMax-2];
  TH1F *mBHbkg_nPhoton[multMax-2];
  TH1F *mBHbkg_MET[multMax-2];
  TH1F *mBHbkg_JetEta[multMax-2];
  TH1F *mBHbkg_JetpT[multMax-2];
  TH1F *mBHbkg_JetEt[multMax-2];
  TH1F *mBHbkg_ST[multMax-2];
  TH1F *mBHbkg_STmet50[multMax-2];
  TH1F *mBHbkg_STmet100[multMax-2];
  TH1F *mBHbkg_STmet200[multMax-2];
  // ISR/FSR histograms
  TH1F *Jet_Eta[multMax-2];
  TH1F *Jet_dR[multMax-2];
  TH1F *Jet_dRmax[multMax-2];
  TH1F *Jet_dRmin[multMax-2];
  TH1F *Jet_dRratio[multMax-2];
  TH1F *nPV[multMax-2];

  // ST histograms
  TH1F *stIncHist[multMax-2];
  TH1F *stExcHist[multMax-2];
  TH1F *stIncHist_tight[multMax-2];
  TH1F *stExcHist_tight[multMax-2];
  TH1F stHistMHT = TH1F("stHistMHT", "ST using MHT", nBin, STlow, STup);
  TH1F stHistMHT_tight = TH1F("stHistMHT_tight", "ST_tight using MHT_tight", nBin, STlow, STup);
  TH1F *stIncHistMHT[multMax-2];
  TH1F *stExcHistMHT[multMax-2];
  TH1F *stIncHistMHT_tight[multMax-2];
  TH1F *stExcHistMHT_tight[multMax-2];
  char *histTitle = new char[20];
  // These use pat::slimmedMETs
  for (int iHist = 0; iHist<multMax-2; ++iHist) {
    sprintf(histTitle, "mBH_Inc%02dHist", mult);
    mBH_IncHist[iHist] = new TH1F(histTitle, "Inclusive mBH", nBin*2, STlow, STup);
    sprintf(histTitle, "mBH_Exc%02dHist", mult);
    mBH_ExcHist[iHist] = new TH1F(histTitle, "Exclusive mBH", nBin*2, STlow, STup);
    sprintf(histTitle, "mBH_jet_Exc%02dHist", mult);
    mBH_jet_ExcHist[iHist] = new TH1F(histTitle, "Exclusive mBH", nBin*2, STlow, STup);

    //Signal histograms
    sprintf(histTitle, "mBHsig_nJet_Exc%02d", mult);
    mBHsig_nJet[iHist]    = new TH1F(histTitle, "nJet in signal", 10, 0, 10);
    sprintf(histTitle, "mBHsig_nEle_Exc%02d", mult);
    mBHsig_nEle[iHist]    = new TH1F(histTitle, "nEle in signal", 10, 0, 10);
    sprintf(histTitle, "mBHsig_nMuon_Exc%02d", mult);
    mBHsig_nMuon[iHist]   = new TH1F(histTitle, "nMuon in signal", 10, 0, 10);
    sprintf(histTitle, "mBHsig_nPhoton_Exc%02d", mult);
    mBHsig_nPhoton[iHist] = new TH1F(histTitle, "nPhoton in signal", 10, 0, 10);
    sprintf(histTitle, "mBHsig_MET_Exc%02d", mult);
    mBHsig_MET[iHist]     = new TH1F(histTitle, "MET in signal", 120, 0, 6000);
    sprintf(histTitle, "mBHsig_JetEta_Exc%02d", mult);
    mBHsig_JetEta[iHist]  = new TH1F(histTitle, "JetEta in signal", 50, -5, 5);
    sprintf(histTitle, "mBHsig_JetpT_Exc%02d", mult);
    mBHsig_JetpT[iHist]   = new TH1F(histTitle, "JetpT in signal", 120, 0,6000 );
    sprintf(histTitle, "mBHsig_JetEt_Exc%02d", mult);
    mBHsig_JetEt[iHist]   = new TH1F(histTitle, "JetEt in signal", 120, 0,6000 );
    sprintf(histTitle, "mBHsig_ST_Exc%02d", mult);
    mBHsig_ST[iHist]      = new TH1F(histTitle, "ST in signal", 130, 0,13000 );
    sprintf(histTitle, "mBHsig_STmet50_Exc%02d", mult);
    mBHsig_STmet50[iHist]      = new TH1F(histTitle, "ST in signal,met>50", 130, 0,13000 );
    sprintf(histTitle, "mBHsig_STmet100_Exc%02d", mult);
    mBHsig_STmet100[iHist]      = new TH1F(histTitle, "ST in signal,met>100", 130, 0,13000 );
    sprintf(histTitle, "mBHsig_STmet200_Exc%02d", mult);
    mBHsig_STmet200[iHist]      = new TH1F(histTitle, "ST in signal,met>200", 130, 0,13000 );

    //ISR/FSR study
    sprintf(histTitle, "Jet_Eta_Exc%02d", mult);
    Jet_Eta[iHist]      = new TH1F(histTitle, "IsoJet Eta,ST>2TeV", 50, -5,5 );
    sprintf(histTitle, "Jet_dR_Exc%02d", mult);
    Jet_dR[iHist]      = new TH1F(histTitle, "IsoJet dR,ST>2TeV", 100, 0, 10 );
    sprintf(histTitle, "Jet_dRmax_Exc%02d", mult);
    Jet_dRmax[iHist]      = new TH1F(histTitle, "IsoJet dRmax,ST>2TeV", 100, 0, 10 );
    sprintf(histTitle, "Jet_dRmin_Exc%02d", mult);
    Jet_dRmin[iHist]      = new TH1F(histTitle, "IsoJet dRmin,ST>2TeV", 100, 0, 10 );
    sprintf(histTitle, "Jet_dRratio_Exc%02d", mult);
    Jet_dRratio[iHist]      = new TH1F(histTitle, "IsoJet dRmax/dRmin,ST>2TeV", 200, 0, 40 );
    sprintf(histTitle, "nPV_Exc%02d", mult);
    nPV[iHist]             = new TH1F(histTitle, "nPV", 100, 0, 100 );

    //Bkg histograms
    sprintf(histTitle, "mBHbkg_nJet_Exc%02d", mult);
    mBHbkg_nJet[iHist]    = new TH1F(histTitle, "nJet in bkg", 10, 0, 10);
    sprintf(histTitle, "mBHbkg_nEle_Exc%02d", mult);
    mBHbkg_nEle[iHist]    = new TH1F(histTitle, "nEle in bkg", 10, 0, 10);
    sprintf(histTitle, "mBHbkg_nMuon_Exc%02d", mult);
    mBHbkg_nMuon[iHist]   = new TH1F(histTitle, "nMuon in bkg", 10, 0, 10);
    sprintf(histTitle, "mBHbkg_nPhoton_Exc%02d", mult);
    mBHbkg_nPhoton[iHist] = new TH1F(histTitle, "nPhoton in bkg", 10, 0, 10);
    sprintf(histTitle, "mBHbkg_MET_Exc%02d", mult);
    mBHbkg_MET[iHist]     = new TH1F(histTitle, "MET in bkg", 120, 0, 6000);
    sprintf(histTitle, "mBHbkg_JetEta_Exc%02d", mult);
    mBHbkg_JetEta[iHist]  = new TH1F(histTitle, "JetEta in bkg", 50, -5, 5);
    sprintf(histTitle, "mBHbkg_JetpT_Exc%02d", mult);
    mBHbkg_JetpT[iHist]   = new TH1F(histTitle, "JetpT in bkg", 120, 0,6000 );
    sprintf(histTitle, "mBHbkg_JetEt_Exc%02d", mult);
    mBHbkg_JetEt[iHist]   = new TH1F(histTitle, "JetEt in bkg", 120, 0,6000 );
    sprintf(histTitle, "mBHbkg_ST_Exc%02d", mult);
    mBHbkg_ST[iHist]      = new TH1F(histTitle, "ST in bkg", 130, 0,13000 );
    sprintf(histTitle, "mBHbkg_STmet50_Exc%02d", mult);
    mBHbkg_STmet50[iHist]      = new TH1F(histTitle, "ST in bkg,met>50", 130, 0,13000 );
    sprintf(histTitle, "mBHbkg_STmet100_Exc%02d", mult);
    mBHbkg_STmet100[iHist]      = new TH1F(histTitle, "ST in bkg,met>100", 130, 0,13000 );
    sprintf(histTitle, "mBHbkg_STmet200_Exc%02d", mult);
    mBHbkg_STmet200[iHist]      = new TH1F(histTitle, "ST in bkg,met>200", 130, 0,13000 );



    sprintf(histTitle, "stInc%02dHist", mult);
    stIncHist[iHist] = new TH1F(histTitle, "Inclusive ST", nBin, STlow, STup);
    sprintf(histTitle, "stExc%02dHist", mult);
    stExcHist[iHist] = new TH1F(histTitle, "Exclusive ST", nBin, STlow, STup);
    sprintf(histTitle, "stInc%02dHist_tight", mult);
    stIncHist_tight[iHist] = new TH1F(histTitle, "Inclusive ST_tight", nBin, STlow, STup);
    sprintf(histTitle, "stExc%02dHist_tight", mult);
    stExcHist_tight[iHist] = new TH1F(histTitle, "Exclusive ST_tight", nBin, STlow, STup);
    sprintf(histTitle, "stInc%02dHistMHT", mult);
    stIncHistMHT[iHist] = new TH1F(histTitle, "Inclusive ST using MHT", nBin, STlow, STup);
    sprintf(histTitle, "stExc%02dHistMHT", mult);
    stExcHistMHT[iHist] = new TH1F(histTitle, "Exclusive ST using MHT", nBin, STlow, STup);
    sprintf(histTitle, "stInc%02dHistMHT_tight", mult);
    stIncHistMHT_tight[iHist] = new TH1F(histTitle, "Inclusive ST_tight using MHT_tight", nBin, STlow, STup);
    sprintf(histTitle, "stExc%02dHistMHT_tight", mult);
    stExcHistMHT_tight[iHist] = new TH1F(histTitle, "Exclusive ST_tight using MHT_tight", nBin, STlow, STup);
    ++mult;
  }

  // variables calculated in the loop
  float OurMet           = 0.            ;
  float Px               = 0.            ;
  float Py               = 0.            ;
  float ST               = 0.            ;
  float STMHTnoMET       = 0.            ;
  int multiplicity       = 0             ;
  int nIsoJet            = 0             ;
  int nIsoEle            = 0             ;
  int nIsoMuon           = 0             ;
  int nIsoPhoton         = 0             ;
  bool passIso           = true          ;
  float OurMet_tight     = 0.            ;
  float Px_tight         = 0.            ;
  float Py_tight         = 0.            ;
  float ST_tight         = 0.            ;
  float STMHTnoMET_tight = 0.            ;
  int multiplicity_tight = 0             ;
  bool isLeadingJetTight = false          ;
  bool passIso_tight     = true          ;
  bool passMetCut        = true          ;
  bool passMetCut_tight  = true          ;
  char *messageBuffer    = new char[400] ;
  bool eventHasMuon      = false         ;
  bool eventHasPhoton    = false         ;
  bool eventHasElectron  = false         ;
  bool  TightJets[25]                    ;
  bool  JetIso[25]                       ;
  bool  EleIso[25]                       ;
  bool  MuonIso[25]                       ;
  bool  PhotonIso[25]                       ;
  bool  isTightJet       = false         ;
  float JetMuonEt        = 0.            ;
  float JetElectronEt    = 0.            ;
  float JetPhotonEt      = 0.            ;
  float      vecSum[4]                   ;
  float      mBH_cut     = 0.             ;
  float      mBH_jet     = 0.             ;

  // variables accessed from the tree
  //TODO
  Bool_t     firedHLT_PFHT800            ;
  Bool_t     firedHLT_PFHT900            ;
  Bool_t     firedHLT_PFHT475            ;
  Bool_t     firedHLT_PFJet450            ;
  Bool_t     firedHLT_AK8PFJet450            ;
  Bool_t     firedHLT_CaloJet500_NoJetID            ;
  Bool_t     passed_globalTightHalo2016Filter ;
  Bool_t     passed_goodVertices       ;
  Bool_t     passed_eeBadScFilter      ;
  Bool_t     passed_EcalDeadCellTriggerPrimitiveFilter;
  Bool_t     passed_filterbadChCandidate;
  Bool_t     passed_filterbadPFMuon;
  //Bool_t     passed_GiovanniFilter;
  Bool_t     passed_Dimafilter;
  Bool_t     passed_HBHENoiseFilter;
  Bool_t     passed_HBHENoiseIsoFilter;
  int        runno                     ;
  long long  evtno                     ;
  int        lumiblock                 ;
  float      JetE [25]                ;
  float      JetEt [25]                ;
  float      JetPt [25]                ;
  float      JetPx [25]                ;
  float      JetPy [25]                ;
  float      JetPz [25]                ;
  float      JetEta[25]                ;
  float      JetPhi[25]                ;
  float      JetNeutHadFrac[25]        ;
  float      JetNeutEMFrac[25]         ;
  float      JetChgHadFrac[25]         ;
  float      JetMuFrac[25]             ;
  float      JetChgEMFrac[25]          ;
  int        JetNConstituents[25]      ;
  int        JetNNeutConstituents[25]  ;
  int        JetNChgConstituents[25]   ;
  float      EleE[25]                 ;
  float      EleEt[25]                 ;
  float      ElePt[25]                 ;
  float      ElePx[25]                 ;
  float      ElePy[25]                 ;
  float      ElePz[25]                 ;
  float      EleEta[25]                ;
  float      ElePhi[25]                ;
  float      PhE[25]                  ;
  float      PhEt[25]                  ;
  float      PhPt[25]                  ;
  float      PhPx[25]                  ;
  float      PhPy[25]                  ;
  float      PhPz[25]                  ;
  float      PhEta[25]                 ;
  float      PhPhi[25]                 ;
  float      MuE[25]                  ;
  float      MuEt[25]                  ;
  float      MuPt[25]                  ;
  float      MuPx[25]                  ;
  float      MuPy[25]                  ;
  float      MuPz[25]                  ;
  float      MuEta[25]                 ;
  float      MuPhi[25]                 ;
  float      MuPFdBiso[25]             ;
  float      Met                       ;
  float      MetPx                     ;
  float      MetPy                     ;
  float      mBH                       ;
  int        NPV               ;

  // tree branches
  //TODO
  TBranch  *b_firedHLT_PFHT800          ;
  TBranch  *b_firedHLT_PFHT900          ;
  TBranch  *b_firedHLT_PFHT475          ;
  TBranch  *b_firedHLT_PFJet450         ;
  TBranch  *b_firedHLT_CaloJet500_NoJetID         ;
  TBranch  *b_firedHLT_AK8PFJet450         ;
  TBranch  *b_passed_globalTightHalo2016Filter ;
  TBranch  *b_passed_goodVertices       ;
  TBranch  *b_passed_eeBadScFilter      ;
  TBranch  *b_passed_EcalDeadCellTriggerPrimitiveFilter;   
  TBranch  *b_passed_filterbadChCandidate;   
  TBranch  *b_passed_filterbadPFMuon;   
  TBranch  *b_passed_GiovanniFilter;   
  TBranch  *b_passed_Dimafilter;   
  TBranch  *b_passed_HBHENoiseFilter;   
  TBranch  *b_passed_HBHENoiseIsoFilter;   
  TBranch  *b_JetE                     ;
  TBranch  *b_JetEt                     ;
  TBranch  *b_JetPt                     ;
  TBranch  *b_JetPx                     ;
  TBranch  *b_JetPy                     ;
  TBranch  *b_JetPz                     ;
  TBranch  *b_JetEta                    ;
  TBranch  *b_JetPhi                    ;
  TBranch  *b_JetNeutHadFrac            ;
  TBranch  *b_JetNeutEMFrac             ;
  TBranch  *b_JetChgHadFrac             ;
  TBranch  *b_JetMuFrac                 ;
  TBranch  *b_JetChgEMFrac              ;
  TBranch  *b_JetNConstituents          ;
  TBranch  *b_JetNNeutConstituents      ;
  TBranch  *b_JetNChgConstituents       ;
  TBranch  *b_EleE                     ;
  TBranch  *b_EleEt                     ;
  TBranch  *b_ElePt                     ;
  TBranch  *b_ElePx                     ;
  TBranch  *b_ElePy                     ;
  TBranch  *b_ElePz                     ;
  TBranch  *b_EleEta                    ;
  TBranch  *b_ElePhi                    ;
  TBranch  *b_PhE                      ;
  TBranch  *b_PhEt                      ;
  TBranch  *b_PhPt                      ;
  TBranch  *b_PhPx                      ;
  TBranch  *b_PhPy                      ;
  TBranch  *b_PhPz                      ;
  TBranch  *b_PhEta                     ;
  TBranch  *b_PhPhi                     ;
  TBranch  *b_MuE                      ;
  TBranch  *b_MuEt                      ;
  TBranch  *b_MuPt                      ;
  TBranch  *b_MuPx                      ;
  TBranch  *b_MuPy                      ;
  TBranch  *b_MuPz                      ;
  TBranch  *b_MuEta                     ;
  TBranch  *b_MuPhi                     ;
  TBranch  *b_MuPFdBiso                 ;
  TBranch  *b_Met                       ;
  TBranch  *b_MetPx                       ;
  TBranch  *b_MetPy                       ;
  TBranch  *b_runno                     ;
  TBranch  *b_evtno                     ;
  TBranch  *b_lumiblock                 ;
  TBranch  *b_mBH                   ;
  TBranch  *b_NPV                   ;

  //create a chain by looping over the input filename
  TChain chain("bhana/t");
  //ifstream infile;
  //infile.open(inFilename.c_str());
  //std::string buffer;
  //const char *eosURL = "root://eoscms.cern.ch/";
  //chain.SetMakeClass(1);
  //while (std::getline(infile, buffer)) {
  //  std::string ntupleURL = eosURL + buffer;
  chain.Add(inFilename.c_str());
  //}

  cout << "Opened chain: " << chain.GetName() << endl;

  // set all branch addresses
  // TODO
  chain.SetBranchAddress( "firedHLT_PFHT800"          ,  &firedHLT_PFHT800          ,  &b_firedHLT_PFHT800       );
  chain.SetBranchAddress( "firedHLT_PFHT900"          ,  &firedHLT_PFHT900          ,  &b_firedHLT_PFHT900       );
  chain.SetBranchAddress( "firedHLT_PFHT475"          ,  &firedHLT_PFHT475          ,  &b_firedHLT_PFHT475       );
  chain.SetBranchAddress( "firedHLT_PFJet450"         ,  &firedHLT_PFJet450         ,  &b_firedHLT_PFJet450      );
  chain.SetBranchAddress( "firedHLT_CaloJet500_NoJetID"  ,  &firedHLT_CaloJet500_NoJetID  ,  &b_firedHLT_CaloJet500_NoJetID      );
  chain.SetBranchAddress( "firedHLT_AK8PFJet450"         ,  &firedHLT_AK8PFJet450         ,  &b_firedHLT_AK8PFJet450      );
  chain.SetBranchAddress( "passed_globalTightHalo2016Filter" ,  &passed_globalTightHalo2016Filter ,  &b_passed_globalTightHalo2016Filter );
  chain.SetBranchAddress( "passed_goodVertices"       ,  &passed_goodVertices       ,  &b_passed_goodVertices       );
  chain.SetBranchAddress( "passed_eeBadScFilter"      ,  &passed_eeBadScFilter      ,  &b_passed_eeBadScFilter      );
  chain.SetBranchAddress( "passed_EcalDeadCellTriggerPrimitiveFilter"      ,  &passed_EcalDeadCellTriggerPrimitiveFilter      ,  &b_passed_EcalDeadCellTriggerPrimitiveFilter      );
  chain.SetBranchAddress( "passed_filterbadChCandidate"      ,  &passed_filterbadChCandidate      ,  &b_passed_filterbadChCandidate      );
  chain.SetBranchAddress( "passed_filterbadPFMuon"      ,  &passed_filterbadPFMuon      ,  &b_passed_filterbadPFMuon      );
//  chain.SetBranchAddress( "passed_GiovanniFilter"      ,  &passed_GiovanniFilter      ,  &b_passed_GiovanniFilter      );
  chain.SetBranchAddress( "passed_Dimafilter"         ,  &passed_Dimafilter         ,  &b_passed_Dimafilter      );
  chain.SetBranchAddress( "passed_HBHENoiseFilter"         ,  &passed_HBHENoiseFilter         ,  &b_passed_HBHENoiseFilter      );
  chain.SetBranchAddress( "passed_HBHENoiseIsoFilter"         ,  &passed_HBHENoiseIsoFilter         ,  &b_passed_HBHENoiseIsoFilter      );
  chain.SetBranchAddress( "runno"                     ,  &runno                     ,  &b_runno                     );
  chain.SetBranchAddress( "lumiblock"                 ,  &lumiblock                 ,  &b_lumiblock                 );
  chain.SetBranchAddress( "evtno"                     ,  &evtno                     ,  &b_evtno                     );
  chain.SetBranchAddress( "JetE"                      ,  JetE                       ,  &b_JetE                     );
  chain.SetBranchAddress( "JetEt"                     ,  JetEt                      ,  &b_JetEt                     );
  chain.SetBranchAddress( "JetPt"                     ,  JetPt                      ,  &b_JetPt                     );
  chain.SetBranchAddress( "JetPx"                     ,  JetPx                      ,  &b_JetPx                     );
  chain.SetBranchAddress( "JetPy"                     ,  JetPy                      ,  &b_JetPy                     );
  chain.SetBranchAddress( "JetPz"                     ,  JetPz                      ,  &b_JetPz                     );
  chain.SetBranchAddress( "JetEta"                    ,  JetEta                     ,  &b_JetEta                    );
  chain.SetBranchAddress( "JetPhi"                    ,  JetPhi                     ,  &b_JetPhi                    );
  chain.SetBranchAddress( "JetNeutHadFrac"            ,  JetNeutHadFrac             ,  &b_JetNeutHadFrac            );
  chain.SetBranchAddress( "JetNeutEMFrac"             ,  JetNeutEMFrac              ,  &b_JetNeutEMFrac             );
  chain.SetBranchAddress( "JetChgHadFrac"             ,  JetChgHadFrac              ,  &b_JetChgHadFrac             );
  chain.SetBranchAddress( "JetMuFrac"                 ,  JetMuFrac                  ,  &b_JetMuFrac                 );
  chain.SetBranchAddress( "JetChgEMFrac"              ,  JetChgEMFrac               ,  &b_JetChgEMFrac              );
  chain.SetBranchAddress( "JetNConstituents"          ,  JetNConstituents           ,  &b_JetNConstituents          );
  chain.SetBranchAddress( "JetNNeutConstituents"      ,  JetNNeutConstituents       ,  &b_JetNNeutConstituents      );
  chain.SetBranchAddress( "JetNChgConstituents"       ,  JetNChgConstituents        ,  &b_JetNChgConstituents       );
  chain.SetBranchAddress( "EleE"                      ,  EleE                       ,  &b_EleE                     );
  chain.SetBranchAddress( "EleEt"                     ,  EleEt                      ,  &b_EleEt                     );
  chain.SetBranchAddress( "ElePt"                     ,  ElePt                      ,  &b_ElePt                     );
  chain.SetBranchAddress( "ElePx"                     ,  ElePx                      ,  &b_ElePx                     );
  chain.SetBranchAddress( "ElePy"                     ,  ElePy                      ,  &b_ElePy                     );
  chain.SetBranchAddress( "ElePz"                     ,  ElePz                      ,  &b_ElePz                     );
  chain.SetBranchAddress( "EleEta"                    ,  EleEta                     ,  &b_EleEta                    );
  chain.SetBranchAddress( "ElePhi"                    ,  ElePhi                     ,  &b_ElePhi                    );
  chain.SetBranchAddress( "PhE"                      ,  PhE                       ,  &b_PhE                      );
  chain.SetBranchAddress( "PhEt"                      ,  PhEt                       ,  &b_PhEt                      );
  chain.SetBranchAddress( "PhPt"                      ,  PhPt                       ,  &b_PhPt                      );
  chain.SetBranchAddress( "PhPx"                      ,  PhPx                       ,  &b_PhPx                      );
  chain.SetBranchAddress( "PhPy"                      ,  PhPy                       ,  &b_PhPy                      );
  chain.SetBranchAddress( "PhPz"                      ,  PhPz                       ,  &b_PhPz                      );
  chain.SetBranchAddress( "PhEta"                     ,  PhEta                      ,  &b_PhEta                     );
  chain.SetBranchAddress( "PhPhi"                     ,  PhPhi                      ,  &b_PhPhi                     );
  chain.SetBranchAddress( "MuE"                      ,  MuE                       ,  &b_MuE                      );
  chain.SetBranchAddress( "MuEt"                      ,  MuEt                       ,  &b_MuEt                      );
  chain.SetBranchAddress( "MuPt"                      ,  MuPt                       ,  &b_MuPt                      );
  chain.SetBranchAddress( "MuPx"                      ,  MuPx                       ,  &b_MuPx                      );
  chain.SetBranchAddress( "MuPy"                      ,  MuPy                       ,  &b_MuPy                      );
  chain.SetBranchAddress( "MuPz"                      ,  MuPz                       ,  &b_MuPz                      );
  chain.SetBranchAddress( "MuEta"                     ,  MuEta                      ,  &b_MuEta                     );
  chain.SetBranchAddress( "MuPhi"                     ,  MuPhi                      ,  &b_MuPhi                     );
  chain.SetBranchAddress( "MuPFdBiso"                 , MuPFdBiso                   ,  &b_MuPFdBiso                 );
  chain.SetBranchAddress( "Met"                       ,  &Met                       ,  &b_Met                       );
  chain.SetBranchAddress( "MetPx"                     ,  &MetPx                       ,  &b_MetPx                       );
  chain.SetBranchAddress( "MetPy"                     ,  &MetPy                       ,  &b_MetPy                       );
  chain.SetBranchAddress( "mBH"                       ,  &mBH                       ,  &b_mBH                       );
  chain.SetBranchAddress( "NPV"                       ,  &NPV                       ,  &b_NPV                       );

  const int nEvents = chain.GetEntries();
  cout << "Number of events in chain is: " << nEvents << endl;
  Ngen.Fill(0.5,nEvents);
  bool passMETfilterList = true;
  // loop over all events
  for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
    if (iEvent%100000==0) {
      cout << std::fixed << std::setw(3) << std::setprecision(1) << (float(iEvent)/float(nEvents))*100 << "% done: Scanned " << iEvent << " events." << endl;
    }

    // reset variables
    isTightJet          = false ;
    OurMet              = 0.    ;
    Px                  = 0.    ;
    Py                  = 0.    ;
    ST                  = 0.    ;
    multiplicity        = 0     ;
    nIsoJet            = 0      ;
    nIsoEle            = 0      ;
    nIsoMuon           = 0      ;
    nIsoPhoton         = 0      ;
    OurMet_tight        = 0.    ;
    Px_tight            = 0.    ;
    Py_tight            = 0.    ;
    ST_tight            = 0.    ;
    multiplicity_tight  = 0     ;
    eventHasMuon        = false ;
    eventHasPhoton      = false ;
    eventHasElectron    = false ;
    mBH_cut             = 0.    ;
    mBH_jet             = 0.    ;
    std::fill(std::begin( TightJets    ), std::end( TightJets ), false );
    std::fill(std::begin( JetIso       ), std::end( JetIso    ), true );
    std::fill(std::begin( EleIso       ), std::end( EleIso    ), true );
    std::fill(std::begin( MuonIso      ), std::end( MuonIso   ), true );
    std::fill(std::begin( PhotonIso    ), std::end( PhotonIso ), true );
    std::fill(std::begin( vecSum       ), std::end( vecSum    ), 0. );

    chain.GetEntry(iEvent);
    // apply trigger and filter requirements
    //TODO
    if ( is2016H ){
      if ( isData &&  
       ( !(firedHLT_PFHT900||firedHLT_PFHT800  || firedHLT_PFJet450 || firedHLT_CaloJet500_NoJetID||firedHLT_AK8PFJet450)  
             || !passed_globalTightHalo2016Filter 
             || !passed_goodVertices 
             || !passed_eeBadScFilter  
             || !passed_filterbadChCandidate  
             || !passed_EcalDeadCellTriggerPrimitiveFilter  
             || !passed_filterbadPFMuon  
    //         || !passed_GiovanniFilter  
             || !passed_Dimafilter
             || !passed_HBHENoiseFilter
             || !passed_HBHENoiseIsoFilter
        ) ) continue;
    }
    else{
      if ( isData &&  
      ( !firedHLT_PFHT800    
        || !passed_globalTightHalo2016Filter 
        || !passed_goodVertices 
        || !passed_eeBadScFilter  
        || !passed_filterbadChCandidate  
        || !passed_EcalDeadCellTriggerPrimitiveFilter  
        || !passed_filterbadPFMuon  
    //  || !passed_GiovanniFilter  
                || !passed_Dimafilter
                || !passed_HBHENoiseFilter
            || !passed_HBHENoiseIsoFilter
       ) ) continue;
     }

    h_mBH.Fill(mBH);
        // use Yutaro's method for applying the event filter
        passMETfilterList=true;
        auto rItr(list.find(runno));
        if (rItr != list.end()) {
          if (rItr->second.find(evtno) != rItr->second.end()){
            if (dumpBigEvents && debugFlag) {
              sprintf(messageBuffer, "Event in MET list skipped: run number %d lumi section %d event number %lld\n", runno, lumiblock, evtno);
              outTextFile << messageBuffer;
            }
            passMETfilterList = false;
            continue;
          }
        }
        if (!passMETfilterList) cout << "ERROR! This event should be filtered!" << endl;
        if ( runno == 254790 && (lumiblock==211 || lumiblock==395) ) {
          sprintf(messageBuffer, "Event in lumiblock that could not be filtered skipped: run number %d lumi section %d event number %%lld\n", runno, lumiblock, evtno);
          outTextFile << messageBuffer;
          continue;
        }

        // apply isolation requirement and calculate ST and MHT.
        //Jets
        for (int iJet = 0; iJet < 25; ++iJet) {
          passIso=true;
          passIso_tight=true;
          isTightJet=false;
          JetMuonEt     =0;
          JetElectronEt =0;
          JetPhotonEt   =0;
          //if (fabs(JetEta[iJet])<=3 && JetNeutHadFrac[iJet]<0.9 && JetNeutEMFrac[iJet]<0.9 && JetNConstituents[iJet]>1 && JetMuFrac[iJet]<0.8) 
          //if (fabs(JetEta[iJet])<=2.7 && JetNeutHadFrac[iJet]<0.9 && JetNeutHadFrac[iJet]>0.001 && JetNeutEMFrac[iJet]<0.9 && JetNConstituents[iJet]>1 && JetMuFrac[iJet]<0.8) 
          if (fabs(JetEta[iJet])<=2.7 && JetNeutHadFrac[iJet]<0.9  && JetNeutEMFrac[iJet]<0.9 && JetNConstituents[iJet]>1 && JetMuFrac[iJet]<0.8) {
            isTightJet=true;
            if (fabs(JetEta[iJet])<=2.4) {
              if ( JetNChgConstituents[iJet] > 0 && JetChgHadFrac[iJet] > 0 && JetChgHadFrac[iJet]<0.99 && JetChgEMFrac[iJet]<0.9) isTightJet=true;
              else isTightJet=false;
            }
          }
          if (fabs(JetEta[iJet])>2.7 && fabs(JetEta[iJet])<=3.0){
              if ( JetNNeutConstituents[iJet] > 2 && JetNeutHadFrac[iJet] < 0.98 && JetNeutEMFrac[iJet]>0.01) isTightJet=true;
          }
          if (fabs(JetEta[iJet])>3 && JetNeutEMFrac[iJet] < 0.9 && JetNNeutConstituents[iJet] > 10) isTightJet=true;
          TightJets[iJet]=isTightJet;
          if (JetEt[iJet]>PtCut) {
            for (int iMuon = 0; iMuon < 25; ++iMuon ) {
              if (MuEt[iMuon]>PtCut && MuPFdBiso[iMuon]<0.15) {
                eventHasMuon = true;
                if (JetEt[iJet] && dR(JetEta[iJet],JetPhi[iJet], MuEta[iMuon], MuPhi[iMuon]) < 0.3) {
                  JetMuonEt+=MuEt[iMuon];
                  if (MuEt[iMuon]<150) {
                    MuonJetIso1.Fill(MuEt[iMuon]/JetEt[iJet]);
                    MuonJetoverlapdR1.Fill(dR(JetEta[iJet],JetPhi[iJet],MuEta[iMuon],MuPhi[iMuon]));
                  }
                  if (150<=MuEt[iMuon] && MuEt[iMuon]<250) {
                    MuonJetIso2.Fill(MuEt[iMuon]/JetEt[iJet]);
                    MuonJetoverlapdR2.Fill(dR(JetEta[iJet],JetPhi[iJet],MuEta[iMuon],MuPhi[iMuon]));
                  }
                  if (250<=MuEt[iMuon] && MuEt[iMuon]<400) {
                    MuonJetIso3.Fill(MuEt[iMuon]/JetEt[iJet]);
                    MuonJetoverlapdR3.Fill(dR(JetEta[iJet],JetPhi[iJet],MuEta[iMuon],MuPhi[iMuon]));
                  }
                  if (400<=MuEt[iMuon]) {
                    MuonJetIso4.Fill(MuEt[iMuon]/JetEt[iJet]);
                    MuonJetoverlapdR4.Fill(dR(JetEta[iJet],JetPhi[iJet],MuEta[iMuon],MuPhi[iMuon]));
                  }
                  if (JetMuonEt>0.8*JetEt[iJet]) {
                    passIso = false;
                    JetIso[iJet] = false;
                    if (isTightJet) {
                      passIso_tight=false;
                      if (dumpIsoInfo) {
                        sprintf(messageBuffer, "Jet number %d failed isolation with Muon number %d  in run number %d lumi section %d event number %lld\n", iJet, iMuon, runno, lumiblock, evtno);
                        outTextFile << messageBuffer;
                      }
                    }
                    break;
                  }
                }
              }
            }
            for (int iElectron = 0; iElectron < 25; ++iElectron ) {
              if (EleEt[iElectron]>PtCut) {
                eventHasElectron = true;
                if (dR(JetEta[iJet],JetPhi[iJet], EleEta[iElectron], ElePhi[iElectron]) < 0.3) {
                  JetElectronEt+=EleEt[iElectron];
                  if (EleEt[iElectron]<150) {
                    ElectronJetIso1.Fill(EleEt[iElectron]/JetEt[iJet]);
                    ElectronJetoverlapdR1.Fill(dR(JetEta[iJet],JetPhi[iJet],EleEta[iElectron],ElePhi[iElectron]));
                  }
                  if (150<=EleEt[iElectron] && EleEt[iElectron]<250) {
                    ElectronJetIso2.Fill(EleEt[iElectron]/JetEt[iJet]);
                    ElectronJetoverlapdR2.Fill(dR(JetEta[iJet],JetPhi[iJet],EleEta[iElectron],ElePhi[iElectron]));
                  }
                  if (250<=EleEt[iElectron] && EleEt[iElectron]<400) {
                    ElectronJetIso3.Fill(EleEt[iElectron]/JetEt[iJet]);
                    ElectronJetoverlapdR3.Fill(dR(JetEta[iJet],JetPhi[iJet],EleEta[iElectron],ElePhi[iElectron]));
                  }
                  if (400<=EleEt[iElectron]) {
                    ElectronJetIso4.Fill(EleEt[iElectron]/JetEt[iJet]);
                    ElectronJetoverlapdR4.Fill(dR(JetEta[iJet],JetPhi[iJet],EleEta[iElectron],ElePhi[iElectron]));
                  }
                  if (JetElectronEt > 0.7*JetEt[iJet] ) {
                    passIso = false;
            JetIso[iJet] = false;
                    if (isTightJet) {
                      passIso_tight=false;
                      if (dumpIsoInfo) {
                        sprintf(messageBuffer, "Jet number %d failed isolation with Electron number %d  in run number %d lumi section %d event number %lld\n", iJet, iElectron, runno, lumiblock, evtno);
                        outTextFile << messageBuffer;
                      }
                    }
                    break;
                  }
                }
              }
            }
            for (int iPhoton = 0; iPhoton < 25; ++iPhoton ) {
              if (PhEt[iPhoton]>PtCut) {
                eventHasPhoton = true;
                if (dR(JetEta[iJet],JetPhi[iJet], PhEta[iPhoton], PhPhi[iPhoton]) < 0.3) {
                  JetPhotonEt+=PhEt[iPhoton];
                  if (PhEt[iPhoton]<150) {
                    PhotonJetIso1.Fill(PhEt[iPhoton]/JetEt[iJet]);
                    PhotonJetoverlapdR1.Fill(dR(JetEta[iJet],JetPhi[iJet],PhEta[iPhoton],PhPhi[iPhoton]));
                  }
                  if (150<=PhEt[iPhoton] && PhEt[iPhoton]<250) {
                    PhotonJetIso2.Fill(PhEt[iPhoton]/JetEt[iJet]);
                    PhotonJetoverlapdR2.Fill(dR(JetEta[iJet],JetPhi[iJet],PhEta[iPhoton],PhPhi[iPhoton]));
                  }
                  if (250<=PhEt[iPhoton] && PhEt[iPhoton]<400) {
                    PhotonJetIso3.Fill(PhEt[iPhoton]/JetEt[iJet]);
                    PhotonJetoverlapdR3.Fill(dR(JetEta[iJet],JetPhi[iJet],PhEta[iPhoton],PhPhi[iPhoton]));
                  }
                  if (400<=PhEt[iPhoton]) {
                    PhotonJetIso4.Fill(PhEt[iPhoton]/JetEt[iJet]);
                    PhotonJetoverlapdR4.Fill(dR(JetEta[iJet],JetPhi[iJet],PhEta[iPhoton],PhPhi[iPhoton]));
                  }
                  if (JetPhotonEt>0.5*JetEt[iJet] ) {
                    passIso = false;
                    JetIso[iJet] = false;
                    if (isTightJet) {
                      passIso_tight=false;
                      if (dumpIsoInfo) {
                        sprintf(messageBuffer, "Jet number %d failed isolation with Photon number %d  in run number %d lumi section %d event number %lld\n", iJet, iPhoton, runno, lumiblock, evtno);
                        outTextFile << messageBuffer;
                      }
                    }
                    break;
                  }
                }
              }
            }
            if (!passIso) continue;

            if (debugFlag) outTextFile << "    JetEt for jet number " << iJet << " is: " << JetEt[iJet] << endl;
            ST += JetEt[iJet];
            multiplicity+=1;
            nIsoJet+=1;
            Px += JetPx[iJet];
            Py += JetPy[iJet];

            if(isTightJet) {
              ST_tight += JetEt[iJet];
              multiplicity_tight+=1;
              Px_tight += JetPx[iJet];
              Py_tight += JetPy[iJet];
            }
            if (debugFlag && dumpIsoInfo) {
              sprintf(messageBuffer, "Jet number %d passed isolation in run number %d lumi section %d event number %lld.\n       It had Px=%f and Py=%f\n", iJet, runno, lumiblock, evtno, JetPx[iJet], JetPy[iJet]);
              outTextFile << messageBuffer;
              sprintf(messageBuffer, "   Cumulative: Px=%f and Py=%f\n", Px, Py);
              outTextFile << messageBuffer;
            }
          }
          else break;
        }
    int iLeadingIsoJet = -1;
    //Exclude Leading jet that is not isolated. 
        for (int iJet = 0; iJet < 25; ++iJet) {
        if(JetIso[iJet]){
            if(iLeadingIsoJet==-1){
                iLeadingIsoJet = iJet;
                JetNHF.Fill(JetNeutHadFrac[iJet]);
                JetCHF.Fill(JetChgHadFrac[iJet]);
                if(JetNeutHadFrac[iJet]<=0.001){
                    JetNHF_pt1.Fill(JetPt[iJet]);
                    JetNHF_eta1.Fill(JetEta[iJet]);
                }else{
                    JetNHF_pt2.Fill(JetPt[iJet]);
                    JetNHF_eta2.Fill(JetEta[iJet]);
                }
                if(JetChgHadFrac[iJet]<0.99){
                    JetCHF_pt1.Fill(JetPt[iJet]);
                    JetCHF_eta1.Fill(JetEta[iJet]);
                }else{
                    JetCHF_pt2.Fill(JetPt[iJet]);
                    JetCHF_eta2.Fill(JetEta[iJet]);
                }

            }
        }
    }

    isLeadingJetTight = TightJets[iLeadingIsoJet];
    if (!isLeadingJetTight) continue;
    NJets.Fill(multiplicity);
        //Electrons
        if (eventHasElectron) {
          for (int iElectron = 0; iElectron < 25; ++iElectron) {
            passIso=true;
            passIso_tight=true;
            if (EleEt[iElectron]>PtCut) {
              for (int iJet = 0; iJet < 25; ++iJet ) {
                if (JetEt[iJet]>PtCut && dR(EleEta[iElectron],ElePhi[iElectron], JetEta[iJet], JetPhi[iJet]) < 0.3) {
                  if (EleEt[iElectron]<0.7*JetEt[iJet]) {
                    passIso = false;
                    EleIso[iElectron]=false;
                    if(TightJets[iJet]) {
                      passIso_tight=false;
                      if (dumpIsoInfo) {
                        sprintf(messageBuffer, "Electron number %d failed isolation with Jet number %d  in run number %d lumi section %d event number %lld\n", iElectron, iJet, runno, lumiblock, evtno);
                        outTextFile << messageBuffer;
                      }
                      break;
                    }
                  }
                }
              }
              if (!passIso_tight) continue;

              // Throw away electron if there's an electron/muon overlap.
              for (int iMuon = 0; iMuon < 25; ++iMuon ) {
                if (MuEt[iMuon]>PtCut && MuPFdBiso[iMuon]<0.15 && dR(EleEta[iElectron],ElePhi[iElectron], MuEta[iMuon], MuPhi[iMuon]) < 0.3) {
                  passIso = false;
                  EleIso[iElectron]=false;
                  passIso_tight = false;
                  if (dumpIsoInfo) {
                    sprintf(messageBuffer, "Electron number %d failed isolation with Muon number %d  in run number %d lumi section %d event number %lld\n", iElectron, iMuon, runno, lumiblock, evtno);
                    outTextFile << messageBuffer;
                  }
                  break;
                }
              }
              if (!passIso_tight) continue;

              if (debugFlag) cout << "    EleEt for electron number " << iElectron << " is: " << EleEt[iElectron] << endl;
              ST_tight += EleEt[iElectron];
              multiplicity_tight+=1;
              Px_tight += ElePx[iElectron];
              Py_tight += ElePy[iElectron];
              if (passIso) {
                ST += EleEt[iElectron];
                multiplicity+=1;
                nIsoEle+=1;
                Px += ElePx[iElectron];
                Py += ElePy[iElectron];
              }
              if (debugFlag && dumpIsoInfo) {
                sprintf(messageBuffer, "Ele number %d passed isolation in run number %d lumi section %d event number %lld.      \n It had Px=%f and Py=%f\n", iElectron, runno, lumiblock, evtno, ElePx[iElectron], ElePy[iElectron]);
                outTextFile << messageBuffer;
                sprintf(messageBuffer, "   Cumulative: Px=%f and Py=%f\n", Px, Py);
                outTextFile << messageBuffer;
              }
            }
            else break;
          }
        }

        //Photons
        if (eventHasPhoton) {
          for (int iPhoton = 0; iPhoton < 25; ++iPhoton) {
            passIso=true;
            if (PhEt[iPhoton]>PtCut) {
              for (int iJet = 0; iJet < 25; ++iJet ) {
                if (JetEt[iJet]>PtCut && dR(PhEta[iPhoton],PhPhi[iPhoton], JetEta[iJet], JetPhi[iJet]) < 0.3) {
                  if (PhEt[iPhoton]<0.5*JetEt[iJet]) {
                    passIso = false;
                    PhotonIso[iPhoton]=false;
                    if (TightJets[iJet]) {
                      passIso_tight=false;
                      if (dumpIsoInfo) {
                        sprintf(messageBuffer, "Photon number %d failed isolation with Jet number %d  in run number %d lumi section %d event number %lld\n", iPhoton, iJet, runno, lumiblock, evtno);
                        outTextFile << messageBuffer;
                      }
                      break;
                    }
                  }
                }
              }
              if (!passIso_tight) continue;

              // Throw out photon if there's a photon/muon overlap
              for (int iMuon = 0; iMuon < 25; ++iMuon ) {
                if (MuEt[iMuon]>PtCut && MuPFdBiso[iMuon]<0.15 && dR(PhEta[iPhoton], PhPhi[iPhoton], MuEta[iMuon], MuPhi[iMuon]) < 0.3) {
                  if (dumpIsoInfo) {
                    sprintf(messageBuffer, "Photon number %d failed isolation with Muon number %d  in run number %d lumi section %d event number %lld\n", iPhoton, iMuon, runno, lumiblock, evtno);
                    outTextFile << messageBuffer;
                  }
                  passIso = false;
                  passIso_tight = false;
                  PhotonIso[iPhoton]=false;
                  break;
                }
              }
              if (!passIso_tight) continue;

              // Throw out photon if there's a photon/electron overlap
              for (int iElectron = 0; iElectron < 25; ++iElectron ) {
                if (EleEt[iElectron]>PtCut && dR(PhEta[iPhoton], PhPhi[iPhoton], EleEta[iElectron], ElePhi[iElectron]) < 0.3) {
                  if (dumpIsoInfo) {
                    sprintf(messageBuffer, "Photon number %d failed isolation with Electron number %d  in run number %d lumi section %d event number %lld\n", iPhoton, iElectron, runno, lumiblock, evtno);
                    outTextFile << messageBuffer;
                  }
                  passIso = false;
                  PhotonIso[iPhoton]=false;
                  passIso_tight = false;
                  break;
                }
              }
              if (!passIso_tight) continue;

              if (debugFlag) cout << "    PhEt for photon number " << iPhoton << " is: " << PhEt[iPhoton] << endl;

              ST_tight += PhEt[iPhoton];
              multiplicity_tight+=1;
              Px_tight += PhPx[iPhoton];
              Py_tight += PhPy[iPhoton];
              if (passIso) {
                ST += PhEt[iPhoton];
                multiplicity+=1;
                nIsoPhoton+=1;
                Px += PhPx[iPhoton];
                Py += PhPy[iPhoton];
              }
              if (debugFlag && dumpIsoInfo) {
                sprintf(messageBuffer, "Photon number %d passed isolation in run number %d lumi section %d event number %lld.\n      It had Px=%f and Py=%f\n", iPhoton, runno, lumiblock, evtno, PhPx[iPhoton], PhPy[iPhoton]);
                outTextFile << messageBuffer;
                sprintf(messageBuffer, "   Cumulative: Px=%f and Py=%f\n", Px, Py);
                outTextFile << messageBuffer;
              }
            }
            else break;
          }
        }

        //Muons
        if (eventHasMuon) {
          for (int iMuon = 0; iMuon < 25; ++iMuon) {
            passIso=true;
            passIso_tight=true;
            if (MuEt[iMuon]>PtCut && MuPFdBiso[iMuon]<0.15) {
              if (debugFlag) cout << "    MuEt for muon number " << iMuon << " is: " << MuEt[iMuon] << endl;
              ST += MuEt[iMuon];
              multiplicity+=1;
              nIsoMuon+=1;
              Px += MuPx[iMuon];
              Py += MuPy[iMuon];
              ST_tight += MuEt[iMuon];
              multiplicity_tight+=1;
              Px_tight += MuPx[iMuon];
              Py_tight += MuPy[iMuon];
              if (debugFlag && dumpIsoInfo) {
                sprintf(messageBuffer, "Muon number %d passed isolation in run number %d lumi section %d event number %lld.\n       It had Px=%f and Py=%f\n", iMuon, runno, lumiblock, evtno, MuPx[iMuon], MuPy[iMuon]);
                outTextFile << messageBuffer;
                sprintf(messageBuffer, "   Cumulative: Px=%f and Py=%f\n", Px, Py);
                outTextFile << messageBuffer;
              }
            }
            else break;
          }
        }
    h_NPV.Fill(NPV);
    NJetPhElMu.Fill(multiplicity);
    NPV_multi.Fill(multiplicity,NPV);
    multi_NPV.Fill(NPV,multiplicity);
    nPV[multiplicity-2]->Fill(NPV);


        //debug info and big ST printing
        if (debugFlag) cout << "    Met from PAT collection is: " << Met << endl;
        OurMet = std::sqrt(Px*Px + Py*Py);
        OurMet_tight = std::sqrt(Px_tight*Px_tight + Py_tight*Py_tight);
        if (debugFlag) cout << "    Met calculated according to my recipe is: " << OurMet << endl;
        if (0.5*ST>Met || !useMETcut) passMetCut=true;
        else passMetCut=false;
        if (0.5*ST_tight>Met || !useMETcut) {
          passMetCut_tight=true;
        }
        else {
          sprintf(messageBuffer, "Event number %lld failed the MET cut in run number %d lumi section %d.\n       It had MET/HT=%f \n", evtno, runno, lumiblock, (Met/ST_tight));
          outTextFile << messageBuffer;
          passMetCut_tight=false;
        }
        if (ST>1500) {
          if (ST<3000) METoverSumET.Fill(Met/ST);
          if (ST_tight>1500 && ST_tight<3000) METoverSumET_tight.Fill(Met/ST_tight);
          if (multiplicity>=2){
            METoverSumETinc2.Fill(Met/ST);
            if (multiplicity_tight >=2 && ST_tight>1500 && ST_tight<3000)METoverSumETinc2_tight.Fill(Met/ST_tight);
            if (multiplicity_tight >=3 && ST_tight>1500 && ST_tight<3000)METoverSumETinc3_tight.Fill(Met/ST_tight);
            if (multiplicity_tight >=4 && ST_tight>1500 && ST_tight<3000)METoverSumETinc4_tight.Fill(Met/ST_tight);
            if (multiplicity_tight >=5 && ST_tight>1500 && ST_tight<3000)METoverSumETinc5_tight.Fill(Met/ST_tight);
            if (multiplicity_tight >=6 && ST_tight>1500 && ST_tight<3000)METoverSumETinc6_tight.Fill(Met/ST_tight);
            if (multiplicity_tight >=7 && ST_tight>1500 && ST_tight<3000)METoverSumETinc7_tight.Fill(Met/ST_tight);
            if (multiplicity_tight >=8 && ST_tight>1500 && ST_tight<3000)METoverSumETinc8_tight.Fill(Met/ST_tight);
            if (multiplicity_tight >=9 && ST_tight>1500 && ST_tight<3000)METoverSumETinc9_tight.Fill(Met/ST_tight);
            if (multiplicity_tight >=10 && ST_tight>1500 && ST_tight<3000)METoverSumETinc10_tight.Fill(Met/ST_tight);
            if (eventHasMuon)                                           METoverSumETinc2hasMuon.Fill(Met/ST);
            if (eventHasPhoton)                                         METoverSumETinc2hasPhoton.Fill(Met/ST);
            if (eventHasElectron)                                       METoverSumETinc2hasElectron.Fill(Met/ST);
            if (!eventHasMuon && !eventHasPhoton && !eventHasElectron)  METoverSumETinc2onlyJets.Fill(Met/ST);
            if (multiplicity_tight>=2 && ST_tight>1500 && ST_tight<3000) {
              if (eventHasMuon)                                           METoverSumETinc2hasMuon_tight.Fill(Met/ST_tight);
              if (eventHasPhoton)                                         METoverSumETinc2hasPhoton_tight.Fill(Met/ST_tight);
              if (eventHasElectron)                                       METoverSumETinc2hasElectron_tight.Fill(Met/ST_tight);
              if (!eventHasMuon && !eventHasPhoton && !eventHasElectron)  METoverSumETinc2onlyJets_tight.Fill(Met/ST_tight);
            }
          }
        }
        STMHTnoMET = ST + OurMet;
        STMHTnoMET_tight = ST_tight + OurMet_tight;
        ST += Met;
        ST_tight += Met;
        if (passMetCut){
          stHist.Fill(ST);
          stHistMHT.Fill(STMHTnoMET);
        }
        if (passMetCut_tight){
          stHist_tight.Fill(ST_tight);
          stHistMHT_tight.Fill(STMHTnoMET_tight);
        }

        // Calculate mBH from iso objects
        int nBH_jet = 0;
        int nBH_photon = 0;
        int nBH_electron = 0;
        int nBH_muon = 0;
        for (int iJet = 0; iJet < 25; ++iJet) {
            if(JetIso[iJet] && JetEt[iJet]>20.0){
                vecSum[0] += JetE[iJet];
                vecSum[1] += JetPx[iJet];
                vecSum[2] += JetPy[iJet];
                vecSum[3] += JetPz[iJet];
                nBH_jet +=1;
            }
        }
        mBH_jet   = invMass(vecSum);
        for (int iPhoton = 0; iPhoton < 25; ++iPhoton) {
            if(PhotonIso[iPhoton] && PhEt[iPhoton]>20.0){
                vecSum[0] += PhE[iPhoton];
                vecSum[1] += PhPx[iPhoton];
                vecSum[2] += PhPy[iPhoton];
                vecSum[3] += PhPz[iPhoton];
                nBH_photon +=1;
            }
        }
        for (int iMuon = 0; iMuon < 25; ++iMuon) {
            if(MuonIso[iMuon] && MuEt[iMuon]>20.0){
                vecSum[0] += MuE[iMuon];
                vecSum[1] += MuPx[iMuon];
                vecSum[2] += MuPy[iMuon];
                vecSum[3] += MuPz[iMuon];
                nBH_muon+=1;
            }
        }
        for (int iEle = 0; iEle < 25; ++iEle) {
            if(EleIso[iEle] && EleEt[iEle]>20.0){
                vecSum[0] += EleE[iEle];
                vecSum[1] += ElePx[iEle];
                vecSum[2] += ElePy[iEle];
                vecSum[3] += ElePz[iEle];
                nBH_electron +=1;
            }
        }
        vecSum[1] += MetPx;
        vecSum[2] += MetPy;
        mBH_cut   = invMass(vecSum);
        //int nBH_total = nBH_jet+nBH_electron+nBH_photon+nBH_muon;
        //cout << "mBH_cut="<<mBH_cut<<" mBH="<<mBH<<"   multiplicity = "<<multiplicity<<"    MET="<<Met<<"   nBH_total="<<nBH_total<<"   nBH_jet="<<nBH_jet<<"    nBH_electron="<<nBH_electron<<"   nBH_photon="<<nBH_photon<<"   nBH_muon="<<nBH_muon<<endl;
        
        // Fill Jet ISR/FSR plots
        for (int iHist = 0; iHist<multMax-2; ++iHist) {
            if(multiplicity == iHist+2 && ST>2000.0 ){
                // Just look at Jet pairs and make sure we have enough iso jets
                if(nBH_jet>=multiplicity){
                    double dRmax = 0;
                    double dRmin = 999;

                    for (int iJet = 0; iJet < 25; ++iJet) {
                        for (int jJet = 0; jJet < 25; ++jJet) {
                           //Look only at isolated jets entering ST calculation
                           if(JetIso[iJet] && JetIso[jJet] && JetEt[iJet]>PtCut && JetEt[jJet]>PtCut && iJet != jJet){
                                double dR_ij =  dR(JetEta[iJet],JetPhi[iJet],JetEta[jJet],JetPhi[jJet]);
                                Jet_dR[iHist]->Fill( dR_ij );
                                if(dR_ij > dRmax) dRmax = dR_ij;
                                if(dR_ij < dRmin) dRmin = dR_ij;
                           }
                        }
                        if(JetIso[iJet] && JetEt[iJet]>PtCut) Jet_Eta[iHist]->Fill(JetEta[iJet]);
                    }
                    Jet_dRratio[iHist]->Fill( dRmax/dRmin);
                    Jet_dRmax[iHist]->Fill( dRmax);
                    Jet_dRmin[iHist]->Fill( dRmin);
                }
            }
        }

        // Fill mBHsig/mBHbkg
        for (int iHist = 0; iHist<multMax-2; ++iHist) {
            if(multiplicity == iHist+2 && passMetCut){
                //if((mBH_cut>=2800 && mBH_cut<3300 )|| (mBH_cut>4700 && mBH_cut<=5500)){
                if((mBH_cut>=2500 && mBH_cut<2700 )|| (mBH_cut>3900 && mBH_cut<=5000)){
                    mBHbkg_nJet[iHist]->Fill(nIsoJet);
                    mBHbkg_nEle[iHist]->Fill(nIsoEle);
                    mBHbkg_nMuon[iHist]->Fill(nIsoMuon);
                    mBHbkg_nPhoton[iHist]->Fill(nIsoPhoton);
                    mBHbkg_MET[iHist]->Fill(Met);
                    for (int iJet = 0; iJet < 25; ++iJet) {
                        if(JetIso[iJet] && JetPt[iJet]>PtCut){
                            mBHbkg_JetpT[iHist]->Fill(JetPt[iJet]);
                            mBHbkg_JetEta[iHist]->Fill(JetEta[iJet]);
                            mBHbkg_JetEt[iHist]->Fill(JetEt[iJet]);
                        }
                    }
                    mBHbkg_ST[iHist]->Fill(ST);
                    if(Met>=50.0)  mBHbkg_STmet50[iHist]->Fill(ST);
                    if(Met>=100.0) mBHbkg_STmet100[iHist]->Fill(ST);
                    if(Met>=200.0) mBHbkg_STmet200[iHist]->Fill(ST);
                }
                if(mBH_cut>=2700 && mBH_cut<=3900 ){
                    mBHsig_nJet[iHist]->Fill(nIsoJet);
                    mBHsig_nEle[iHist]->Fill(nIsoEle);
                    mBHsig_nMuon[iHist]->Fill(nIsoMuon);
                    mBHsig_nPhoton[iHist]->Fill(nIsoPhoton);
                    mBHsig_MET[iHist]->Fill(Met);
                    for (int iJet = 0; iJet < 25; ++iJet) {
                        if(JetIso[iJet] && JetPt[iJet]>PtCut){
                            mBHsig_JetpT[iHist]->Fill(JetPt[iJet]);
                            mBHsig_JetEta[iHist]->Fill(JetEta[iJet]);
                            mBHsig_JetEt[iHist]->Fill(JetEt[iJet]);
                        }
                    }
                    mBHsig_ST[iHist]->Fill(ST);
                    if(Met>=50.0)  mBHsig_STmet50[iHist]->Fill(ST);
                    if(Met>=100.0) mBHsig_STmet100[iHist]->Fill(ST);
                    if(Met>=200.0) mBHsig_STmet200[iHist]->Fill(ST);

                }
            }
        }
        for (int iHist = 0; iHist<multMax-2; ++iHist) {
          if (multiplicity == iHist+2 && passMetCut) {
                stExcHist[iHist]->Fill(ST);
                // 2.5*sqrt(ST) ~ <3 sigma of MET resolution
                if( Met < 2.5*std::sqrt(ST)){
                    mBH_ExcHist[iHist]->Fill(mBH_cut);
                    mBH_jet_ExcHist[iHist]->Fill(mBH_jet);
                }
          }
          if (multiplicity >= iHist+2 && passMetCut) {
                stIncHist[iHist]->Fill(ST);  
                if (Met<2.5*std::sqrt(ST)){
                    mBH_IncHist[iHist]->Fill(mBH_jet);
                }
          }
          if (multiplicity_tight == iHist+2 && passMetCut_tight) stExcHist_tight[iHist]->Fill(ST_tight);
          if (multiplicity_tight >= iHist+2 && passMetCut_tight) stIncHist_tight[iHist]->Fill(ST_tight);
        }
        for (int iHist = 0; iHist<multMax-2; ++iHist) {
          if (multiplicity == iHist+2 && passMetCut) stExcHistMHT[iHist]->Fill(STMHTnoMET);
          if (multiplicity >= iHist+2 && passMetCut) stIncHistMHT[iHist]->Fill(STMHTnoMET);
          if (multiplicity_tight == iHist+2 && passMetCut_tight) stExcHistMHT_tight[iHist]->Fill(STMHTnoMET_tight);
          if (multiplicity_tight >= iHist+2 && passMetCut_tight) stIncHistMHT_tight[iHist]->Fill(STMHTnoMET_tight);
        }
    MET.Fill(Met);
    OurMET.Fill(OurMet);
        METvsMHT.Fill(OurMet,Met);
        METvsMHT_tight.Fill(OurMet_tight,Met);
        if (multiplicity>=2){
          METvsMHTinc2.Fill(OurMet,Met);
          METvsMHTinc2_tight.Fill(OurMet_tight,Met);
          if (eventHasMuon)                                           METvsMHTinc2hasMuon.Fill(OurMet, Met);
          if (eventHasPhoton)                                         METvsMHTinc2hasPhoton.Fill(OurMet, Met);
          if (eventHasElectron)                                       METvsMHTinc2hasElectron.Fill(OurMet, Met);
          if (!eventHasMuon && !eventHasPhoton && !eventHasElectron)  METvsMHTinc2onlyJets.Fill(OurMet, Met);
          if (multiplicity_tight>=2) {
            if (eventHasMuon)                                           METvsMHTinc2hasMuon_tight.Fill(OurMet_tight, Met);
            if (eventHasPhoton)                                         METvsMHTinc2hasPhoton_tight.Fill(OurMet_tight, Met);
            if (eventHasElectron)                                       METvsMHTinc2hasElectron_tight.Fill(OurMet_tight, Met);
            if (!eventHasMuon && !eventHasPhoton && !eventHasElectron)  METvsMHTinc2onlyJets_tight.Fill(OurMet_tight, Met);
          }
        }
        if (dumpIsoInfo && fabs(OurMet-Met)>300) {
          sprintf(messageBuffer, "MET-MHT is %f in run number %d lumi section %d event number %lld. ST is %f and multiplicity is %d\n", Met-OurMet, runno, lumiblock, evtno, ST, multiplicity);
          outTextFile << messageBuffer;
          if (debugFlag) cout << messageBuffer;
        }


        // dump info on events with very big ST
        if (multiplicity>=2 && ST>5500 && dumpBigEvents) {
          //sprintf(messageBuffer, "In run number %d lumi section %d event number %lld: ST is %f, ST_tight is %f, and multiplicity is %d\n", runno, lumiblock, evtno, ST, ST_tight, multiplicity);
      sprintf(messageBuffer, "In run number %d lumi section %d event number %llu: ST is %f, ST_tight is %f, and multiplicity is %d\n", runno, lumiblock, evtno, ST, ST_tight, multiplicity);
          outTextFile << messageBuffer;
      sprintf(messageBuffer, "DimaFilter for this event is: %d\n", passed_Dimafilter);
          outTextFile << messageBuffer;
          for (int j=0; j<25; ++j) {
            if(JetEt[j]>0.000) {
              sprintf(messageBuffer, "    Jet %d has TightJet=%d Et=%f, Px=%f, Py=%f, Eta=%f, Phi=%f ", j, TightJets[j],  JetEt[j], JetPx[j], JetPy[j], JetEta[j], JetPhi[j]);
              outTextFile << messageBuffer;
              sprintf(messageBuffer, "  NHF=%f, NEMF=%f, CHF=%f,  CEMF=%f  MuF=%f\n", JetNeutHadFrac[j], JetNeutEMFrac[j],JetChgHadFrac[j],JetChgEMFrac[j],JetMuFrac[j]);
              outTextFile << messageBuffer;
            }
            if (debugFlag) cout  << messageBuffer;
          }
          for (int j=0; j<25; ++j) {
            if(EleEt[j]>0.000) {
              sprintf(messageBuffer, "    Ele %d has Et=%f, Px=%f, Py=%f, Eta=%f, Phi=%f\n", j, EleEt[j], ElePx[j], ElePy[j], EleEta[j], ElePhi[j]);
              outTextFile << messageBuffer;
            }
            if (debugFlag) cout  << messageBuffer;
          }
          for (int j=0; j<25; ++j) {
            if(PhEt[j]>0.000) {
              sprintf(messageBuffer, "    Ph %d has Et=%f, Px=%f, Py=%f, Eta=%f, Phi=%f\n", j, PhEt[j], PhPx[j], PhPy[j], PhEta[j], PhPhi[j]);
              outTextFile << messageBuffer;
            }
            if (debugFlag) cout  << messageBuffer;
          }
          for (int j=0; j<25; ++j) {
            if(MuEt[j]>0.000) {
              sprintf(messageBuffer, "    Mu %d has Et=%f, Px=%f, Py=%f, Eta=%f, Phi=%f\n", j, MuEt[j], MuPx[j], MuPy[j], MuEta[j], MuPhi[j]);
              outTextFile << messageBuffer;
            }
            if (debugFlag) cout  << messageBuffer;
          }
          sprintf(messageBuffer, "    our Px is=%f\n", Px);
          outTextFile << messageBuffer;
          sprintf(messageBuffer, "    our Py is=%f\n", Py);
          outTextFile << messageBuffer;
          sprintf(messageBuffer, "    our MHT is=%f\n", OurMet);
          outTextFile << messageBuffer;
          sprintf(messageBuffer, "    our Px_tight is=%f\n", Px_tight);
          outTextFile << messageBuffer;
          sprintf(messageBuffer, "    our Py_tight is=%f\n", Py_tight);
          outTextFile << messageBuffer;
          sprintf(messageBuffer, "    our MHT_tight is=%f\n", OurMet_tight);
          outTextFile << messageBuffer;
          sprintf(messageBuffer, "    MET is=%f\n", Met);
          outTextFile << messageBuffer;
          if (debugFlag) cout  << messageBuffer;
          sprintf(messageBuffer, "\n\n\n\n");
          outTextFile << messageBuffer;
        }
        if (debugFlag && ( STMHTnoMET>4000 || Met > 2000 || OurMet > 2000 || fabs(OurMet-Met)>100) && multiplicity>=2) {
          if (debugFlag) cout << "In run number " << runno << " lumi section " << lumiblock << " event number " << evtno << " sT is:" << ST << endl;
          if (dumpIsoInfo) {
            sprintf(messageBuffer, "In run number %d lumi section %d event number %lld ST is %f and multiplicity is %d\n", runno, lumiblock, evtno, ST, multiplicity);
            outTextFile << messageBuffer;
          }
          if (debugFlag) cout << messageBuffer;

          // dump all object info
          for (int j=0; j<25; ++j) {
            if(debugFlag && dumpIsoInfo && JetEt[j]>0.000) {
              sprintf(messageBuffer, "    Jet %d has TightJet=%d Et=%f, Px=%f, Py=%f, Eta=%f, Phi=%f\n", j, TightJets[j],  JetEt[j], JetPx[j], JetPy[j], JetEta[j], JetPhi[j]);
              outTextFile << messageBuffer;
            }
            if (debugFlag) cout  << messageBuffer;
          }
          for (int j=0; j<25; ++j) {
            if(debugFlag && dumpIsoInfo && EleEt[j]>0.000) {
              sprintf(messageBuffer, "    Ele %d has Et=%f, Px=%f, Py=%f, Eta=%f, Phi=%f\n", j, EleEt[j], ElePx[j], ElePy[j], EleEta[j], ElePhi[j]);
              outTextFile << messageBuffer;
            }
            if (debugFlag) cout  << messageBuffer;
          }
          for (int j=0; j<25; ++j) {
            if(debugFlag && dumpIsoInfo && PhEt[j]>0.000) {
              sprintf(messageBuffer, "    Ph %d has Et=%f, Px=%f, Py=%f, Eta=%f, Phi=%f\n", j, PhEt[j], PhPx[j], PhPy[j], PhEta[j], PhPhi[j]);
              outTextFile << messageBuffer;
            }
            if (debugFlag) cout  << messageBuffer;
          }
          for (int j=0; j<25; ++j) {
            if(debugFlag && dumpIsoInfo && MuEt[j]>0.000) {
              sprintf(messageBuffer, "    Mu %d has Et=%f, Px=%f, Py=%f, Eta=%f, Phi=%f\n", j, MuEt[j], MuPx[j], MuPy[j], MuEta[j], MuPhi[j]);
              outTextFile << messageBuffer;
            }
            if (debugFlag) cout  << messageBuffer;
          }
          if (debugFlag && dumpIsoInfo) {
            sprintf(messageBuffer, "    our Px is=%f\n", Px);
            outTextFile << messageBuffer;
            sprintf(messageBuffer, "    our Py is=%f\n", Py);
            outTextFile << messageBuffer;
            sprintf(messageBuffer, "    our MHT is=%f\n", OurMet);
            outTextFile << messageBuffer;
            sprintf(messageBuffer, "    MET is=%f\n", Met);
            outTextFile << messageBuffer;
            if (debugFlag) cout  << messageBuffer;
            sprintf(messageBuffer, "\n\n\n\n");
            outTextFile << messageBuffer;
          }
        }
        nDumpedEvents+=1;
        if (debugFlag && nDumpedEvents==eventsToDump) break;
  }
  // write output textfile
  outTextFile.close();
  // write output root file
  TFile* outRootFile = new TFile(outFilename.c_str(), "RECREATE");
  Ngen.Write();
  NJets.Write();
  NJetPhElMu.Write();
  h_NPV.Write();
  h_mBH.Write();
  MET.Write();
  OurMET.Write();
  NPV_multi.Write();
  multi_NPV.Write();
  JetNHF.Write();
  JetNHF_pt1.Write();
  JetNHF_pt2.Write();
  JetNHF_eta1.Write();
  JetNHF_eta2.Write();
  JetCHF.Write();
  JetCHF_pt1.Write();
  JetCHF_pt2.Write();
  JetCHF_eta1.Write();
  JetCHF_eta2.Write();

  outRootFile->cd();
  outRootFile->mkdir("ST");
  outRootFile->mkdir("m_BH");
  outRootFile->mkdir("Jets");
  outRootFile->mkdir("ST_tight");
  outRootFile->mkdir("MET-MHT");
  outRootFile->mkdir("Isolation");

  outRootFile->cd("ST");
  stHist.Write();
  for (int iHist = 0; iHist<multMax-2; ++iHist) {
    stExcHist[iHist]->Write();
    stIncHist[iHist]->Write();
  }
  stHistMHT.Write();
  for (int iHist = 0; iHist<multMax-2; ++iHist) {
    stExcHistMHT[iHist]->Write();
    stIncHistMHT[iHist]->Write();
  }
  outRootFile->cd("m_BH");
  for (int iHist = 0; iHist<multMax-2; ++iHist) {
    mBH_ExcHist[iHist]->Write();
    mBH_jet_ExcHist[iHist]->Write();
    mBH_IncHist[iHist]->Write();
    mBHsig_nJet[iHist]->Write();
    mBHsig_nEle[iHist]->Write();
    mBHsig_nMuon[iHist]->Write();
    mBHsig_nPhoton[iHist]->Write();
    mBHsig_MET[iHist]->Write();
    mBHsig_JetEta[iHist]->Write();
    mBHsig_JetpT[iHist]->Write();
    mBHsig_JetEt[iHist]->Write();
    mBHsig_ST[iHist]->Write();
    mBHsig_STmet50[iHist]->Write();
    mBHsig_STmet100[iHist]->Write();
    mBHsig_STmet200[iHist]->Write();

    mBHbkg_nJet[iHist]->Write();
    mBHbkg_nEle[iHist]->Write();
    mBHbkg_nMuon[iHist]->Write();
    mBHbkg_nPhoton[iHist]->Write();
    mBHbkg_MET[iHist]->Write();
    mBHbkg_JetEta[iHist]->Write();
    mBHbkg_JetpT[iHist]->Write();
    mBHbkg_JetEt[iHist]->Write();
    mBHbkg_ST[iHist]->Write();
    mBHbkg_STmet50[iHist]->Write();
    mBHbkg_STmet100[iHist]->Write();
    mBHbkg_STmet200[iHist]->Write();


  }

  outRootFile->cd("Jets");
  for (int iHist = 0; iHist<multMax-2; ++iHist) {
    Jet_Eta[iHist]->Write();
    Jet_dR[iHist]->Write();
    Jet_dRmax[iHist]->Write();
    Jet_dRmin[iHist]->Write();
    Jet_dRratio[iHist]->Write();
    nPV[iHist]->Write();
  }


  outRootFile->cd("ST_tight");
  stHist_tight.Write();
  for (int iHist = 0; iHist<multMax-2; ++iHist) {
    stExcHist_tight[iHist]->Write();
    stIncHist_tight[iHist]->Write();
  }
  stHistMHT_tight.Write();
  for (int iHist = 0; iHist<multMax-2; ++iHist) {
    stExcHistMHT_tight[iHist]->Write();
    stIncHistMHT_tight[iHist]->Write();
  }

  outRootFile->cd("MET-MHT");
  METvsMHT.Write();
  METvsMHTinc2.Write();
  METvsMHTinc2hasMuon.Write();
  METvsMHTinc2hasPhoton.Write();
  METvsMHTinc2hasElectron.Write();
  METvsMHTinc2onlyJets.Write();
  METvsMHT_tight.Write();
  METvsMHTinc2_tight.Write();
  METvsMHTinc2hasMuon_tight.Write();
  METvsMHTinc2hasPhoton_tight.Write();
  METvsMHTinc2hasElectron_tight.Write();
  METvsMHTinc2onlyJets_tight.Write();
  METoverSumET.Write();
  METoverSumETinc2.Write();
  METoverSumETinc2hasMuon.Write();
  METoverSumETinc2hasPhoton.Write();
  METoverSumETinc2hasElectron.Write();
  METoverSumETinc2onlyJets.Write();
  METoverSumET_tight.Write();
  METoverSumETinc2_tight.Write();
  METoverSumETinc3_tight.Write();
  METoverSumETinc4_tight.Write();
  METoverSumETinc5_tight.Write();
  METoverSumETinc6_tight.Write();
  METoverSumETinc7_tight.Write();
  METoverSumETinc8_tight.Write();
  METoverSumETinc9_tight.Write();
  METoverSumETinc10_tight.Write();
  METoverSumETinc2hasMuon_tight.Write();
  METoverSumETinc2hasPhoton_tight.Write();
  METoverSumETinc2hasElectron_tight.Write();
  METoverSumETinc2onlyJets_tight.Write();

  outRootFile->cd("Isolation");
  MuonJetIso1.Write();
  MuonJetIso2.Write();
  MuonJetIso3.Write();
  MuonJetIso4.Write();
  MuonJetoverlapdR1.Write();
  MuonJetoverlapdR2.Write();
  MuonJetoverlapdR3.Write();
  MuonJetoverlapdR4.Write();
  ElectronJetIso1.Write();
  ElectronJetIso2.Write();
  ElectronJetIso3.Write();
  ElectronJetIso4.Write();
  ElectronJetoverlapdR1.Write();
  ElectronJetoverlapdR2.Write();
  ElectronJetoverlapdR3.Write();
  ElectronJetoverlapdR4.Write();
  PhotonJetIso1.Write();
  PhotonJetIso2.Write();
  PhotonJetIso3.Write();
  PhotonJetIso4.Write();
  PhotonJetoverlapdR1.Write();
  PhotonJetoverlapdR2.Write();
  PhotonJetoverlapdR3.Write();
  PhotonJetoverlapdR4.Write();

  outRootFile->Close();
}



// function to calculate dR between two objects
float dR(float eta1, float phi1, float eta2, float phi2) {
  return std::sqrt( ( eta1 - eta2 )*( eta1 - eta2 ) + std::pow(TMath::ATan2(TMath::Sin( phi1 - phi2), TMath::Cos(phi1-phi2)),2) );
}
float invMass(float vector4[4]){
    //E^2 - p^2
    return std::sqrt(vector4[0]*vector4[0] - vector4[1]*vector4[1] - vector4[2]*vector4[2]- vector4[3]*vector4[3]);
}

// function to make an event list object for MET filtering
std::map<unsigned, std::set<unsigned> > readEventList(char const* _fileName) {
  std::map<unsigned, std::set<unsigned> > list;
  ifstream listFile(_fileName);
  if (!listFile.is_open())
    throw std::runtime_error(_fileName);

  unsigned iL(0);
  std::string line;
  while (true) {
    std::getline(listFile, line);
    if (!listFile.good())
      break;

    if (line.find(":") == std::string::npos || line.find(":") == line.rfind(":"))
      continue;

    unsigned run(std::atoi(line.substr(0, line.find(":")).c_str()));
    unsigned event(std::atoi(line.substr(line.rfind(":") + 1).c_str()));

    list[run].insert(event);

    ++iL;
  }

  std::cout << "Loaded " << iL << " events" << std::endl;

  return list;
}

