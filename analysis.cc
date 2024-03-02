//No polarization
#include "TH1.h"
#include "TH2.h"
#include "TFile.h"

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC2.h"

#include "Tauola/Tauola.h"
#include "Tauola/TauolaHepMCEvent.h"
#include "Tauola/Log.h"

#include "Pythia8/HepMCInterface.h"
#include "HepMC/GenEvent.h"
#include "HepMC/IO_GenEvent.h"
#include "HepMC/Units.h"

#include "Pythia8/ParticleData.h"


#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"

#include "LHAPDF/LHAPDF.h"

#include <fstream>
#include <string>
#define MIN -1;

using namespace Pythia8;
using namespace LHAPDF;
using namespace Tauolapp;

double deltaR(double eta1, double eta2, double phi1, double phi2) 
{
  double dphi = fabs(phi1-phi2);
  if(dphi > M_PI) 
    {
      dphi = (2*M_PI - dphi);
    }
  double deta = fabs(eta1-eta2);
  return sqrt(dphi*dphi + deta*deta);
}
double deltaphi(double phi1, double phi2) 
{
  double dphi = fabs(phi1-phi2);
  if(dphi > M_PI) 
    {
      dphi = (2*M_PI - dphi);
    }
  return dphi;
}
double CorrectPhi(double phi, double x, double y)
{
  if(y<0)phi-=(2*M_PI);//without this you have 0<phi<2pi, but with this
  return phi;//you get -pi<phi<pi
}

struct bjet{
  double px,py,pz,e,eta,phi;
};


int main(int argc, char *argv[]) {

//  int HowManyEvents=10000;
//  string CmndFile;
//  string output;
 
 if(argc!=6){//for signal
//  if(argc!=5){ //for background
    cout<<"./Analysis.exe CmndFile OutputRootFile EventsToSkip NumberOfEvents"<<endl;
    cout<<"Error ......"<<endl;
    cout<<"Please run as the following :"<<endl;
//    cout<<"./Analysis.exe CmndFile InputLHEFile OutputRootFile EventsToSkip NumberOfEvents"<<endl;
    exit(1);
  }
  HepMC::I_Pythia8 ToHepMC;
  Pythia pythia;
  Event& event = pythia.event;
  Info& info = pythia.info;
 
   pythia.readFile(argv[1]);
   pythia.init(argv[2]);

   TFile f(argv[3],"recreate");
// TFile f(argv[3],"recreate");
   pythia.LHAeventSkip(atoi(argv[4]));
   int HowManyEvents=atoi(argv[5]);
//   pythia.init( 2212, 2212, 14000.);//LHC
   
   ParticleData& pdt=pythia.particleData;
  //These are to switch on or off some of decays which are already set by slha file
 
  pdt.readString("6:onMode   = off");//top
  pdt.readString("6:onIfAny  = 24 -5");//W
  pdt.readString("24:onMode   = off");
  pdt.readString("24:onIfAny  = 1 2 3 4 5");//jets
//for QCD multijet production
//  pythia.readString("HardQCD:all = on");    
//  pythia.readString("PhaseSpace:pTHatMin = 200.");

  pdt.listChanged();
//  TFile f(output.c_str(),"recreate");

  TH1F *hjetmul=new TH1F("JetMul","Jet Mul.",10,0.,10.);
  TH1F *hbjetmul=new TH1F("BJetMul.","B Jet Mul.",10,0.,10.);

  TH1F *hjetet=new TH1F("JetEt","Jet Et",200,0.,500.);
  TH1F *hjeteta=new TH1F("JetEta","Jet Eta",100,-5.,5.);
  TH1F *hjetphi=new TH1F("JetPhi","Jet Phi",100,-7.,7.);

  TH1F *hbjetet=new TH1F("bJetEt","bJet Et",200,0.,500.);
  TH1F *hbjeteta=new TH1F("bJetEta","bJet Eta",100,-5.,5.);
  TH1F *hbjetphi=new TH1F("bJetPhi","bJet Phi",100,-7.,7.);

  TH1F *hWmasshad=new TH1F("Wmasshad","W jj mass",100,0.,200.);
  TH1F *hWhadpt=new TH1F("Whadpt","W Pt",100,0.,300.);
    
  TH1F *htopmass=new TH1F("topmass","top mass",200,0.,300.);
  TH1F *htoppt=new TH1F("toppt","top pt",100,0.,300.);
  TH1F *hdeltaphitb=new TH1F("deltaphitb","#delta phi(t,b)",100,0.,4.);

  TH1F *hchmass=new TH1F("CHmass","CH mass",300,0.,600.);
  TH1F *hchpt=new TH1F("CHpt","CH pt",100,0.,300.);
  
//  ParticleData& pdt=pythia.particleData;

  bool FirstEvent = true;

  // ================= Fastjet analysis - select algorithm and parameters

  double Rparam = 0.4;
  fastjet::Strategy               strategy = fastjet::Best;
  fastjet::RecombinationScheme    recombScheme = fastjet::Et_scheme;
  fastjet::JetDefinition         *jetDef = NULL;
  jetDef = new fastjet::JetDefinition(fastjet::antikt_algorithm, Rparam,
                                      recombScheme, strategy);
  // Fastjet input
  std::vector <fastjet::PseudoJet> fjInputs;


  //================== event selection efficiency variables ==========
  
  int nev=0;

  int passedJetCut=0;
  int passedWmassCut=0;
  int passedBJetCut=0;
  int passedphiCut=0;
//  int passedBJetPtCut=0;
  int passedTopCut=0;
 
  ifstream inp("NumberOfEvents.txt");
  inp>>nev>>passedJetCut>>passedWmassCut>>passedBJetCut>>passedTopCut;
  cout<<"==========="<<endl;
  cout<<"Initial number of events after each cut :"<<endl;
  cout<<"Number of events analyzed :"<<nev<<endl;
  cout<<"passedJetCut :"<<passedJetCut<<endl;
  cout<<"passedWmassCut :"<<passedWmassCut<<endl;
  cout<<"passedBJetCut :"<<passedBJetCut<<endl;
  //cout<<"passedBJetPtCut :"<<passedBJetPtCut<<endl;
  cout<<"passedTopCut :"<<passedTopCut<<endl;
  cout<<"==========="<<endl;
  inp.close();
  
   int iseed=0;
  // Begin event loop. Generate event. Skip if error. List first one.
  for (int iEvent = 0; iEvent < HowManyEvents; ++iEvent) {

    if(iEvent%1000==0){
      fprintf(stdout,"Event number is :  %d \r",iEvent);
      fflush(stdout);
    }
    
    //==================== PYTHIA Event Loop ==================
    if(!pythia.next())break;
//    if (iEvent==0)pythia.event.list(); 
    if (iEvent<2)pythia.process.list(); 
    //=========>>>>> pythia.event.list() prints full event
    //========>>>>> pythia.process.list() prints a summary of event

    nev++;
    // Convert event record to HepMC
    HepMC::GenEvent * HepMCEvt = new HepMC::GenEvent();

    //Conversion needed if HepMC uses different momentum units
    //than Pythia. However, requires HepMC 2.04 or higher.
    HepMCEvt->use_units(HepMC::Units::GEV,HepMC::Units::MM);

    ToHepMC.fill_next_event(pythia, HepMCEvt);


    // Reset Fastjet input for each event
    fjInputs.resize(0);

    // Keep track of missing ET
    double mex=0.;
    double mey=0.;
    double mez=0.;
    double met=0.;
    double me=0.;
    double etanu=0;
    double mee=0;

    double pxlepton=0.;
    double pylepton=0.;
    double pzlepton=0.;
    double elepton=0.;
    double max=MIN;
    double second_max=MIN;
    double pxw=0.;
    double pyw=0.;
    double pzw=0.;
    double ew=0.;
    const int ns=20;

    double Wx[ns]={0},Wy[ns]={0},Wz[ns]={0},We[ns]={0},Wpt[ns];
    int njets=0;
    int nbjets=0;
    int nleptons=0;
    
    vector<bjet> bjets;
    bjets.clear();
    bool W2Tau;
    
    for(HepMC::GenEvent::particle_const_iterator p = HepMCEvt->particles_begin(); 
        p!= HepMCEvt->particles_end(); ++p ){
      
      int pid=(*p)->pdg_id();
      double pt=(*p)->momentum().perp();
      double px=(*p)->momentum().px();
      double py=(*p)->momentum().py();
      double pz=(*p)->momentum().pz();
      double e=(*p)->momentum().e();
      double eta=(*p)->momentum().eta();
      double phi=(*p)->momentum().phi();
      double pxlep=0;double pylep=0; double elep=0;
      double pxnu=0;double pynu=0; double enu=0; 
      
      if(abs(pid)==15){
        if ( (*p)->production_vertex() ) {
          for ( HepMC::GenVertex::particle_iterator mother = 
                  (*p)->production_vertex()->particles_begin(HepMC::parents);
                mother!=(*p)->production_vertex()->particles_end(HepMC::parents); 
                ++mother ) 
            {
              if(abs((*mother)->pdg_id())==24){
                W2Tau=true;
              }
            }
        }
      }

              
      // Final state only
      if ((*p)->status()!=1)continue;
      
      // neutrinos     
         if (abs(pid)==12 || abs(pid)==14 || abs(pid)==16) {
            if(fabs(eta) < 3.6) {
            // Missing ET
              mex += px;
              mey += py;
              mee += e;
              etanu=eta;
                }
        }                       
      // Store as input to Fastjhttps://mail.google.com/mail/u/0/?shva=1#inboxet
       fjInputs.push_back(fastjet::PseudoJet (px,py,pz,e));
            
    }//loop over particles in the event
    
    if(W2Tau){nev--;continue;}//to the next event

    //==============================================
   
    if (fjInputs.size() == 0) {
      cout << "Error: event with no final state particles" << endl;
      delete HepMCEvt;
      continue;
    }
    // Run Fastjet algorithm
    vector <fastjet::PseudoJet> inclusiveJets, sortedJets;
    fastjet::ClusterSequence clustSeq(fjInputs, *jetDef);

    // For the first event, print the FastJet details
    if (FirstEvent) {
      cout << "Ran " << jetDef->description() << endl;
      cout << "Strategy adopted by FastJet was "
           << clustSeq.strategy_string() << endl << endl;
      FirstEvent = false;
    }

    // Extract inclusive jets sorted by pT
    inclusiveJets = clustSeq.inclusive_jets();
    sortedJets    = sorted_by_pt(inclusiveJets);  

    //==================== Analysis ==================
    bool high1=false;
    bool high2=false; 
    for (unsigned int i = 0; i < sortedJets.size(); i++) {

      //Beware that fastjet produces 0<phi<2pi while HepMC event map is -pi<phi<pi      
      double jet_et=sortedJets[i].perp();
      double jet_eta=sortedJets[i].eta();
      double jet_phi=sortedJets[i].phi();
      double jet_px=sortedJets[i].px();
      double jet_py=sortedJets[i].py();
      double jet_pz=sortedJets[i].pz();
      double jet_e=sortedJets[i].e();

      jet_phi=CorrectPhi(jet_phi,jet_px,jet_py);
      hjetet->Fill(jet_et);
      hjeteta->Fill(jet_eta);
      hjetphi->Fill(jet_phi);  
      //From here the jet phi map is -pi<phi<pi      
      if (jet_et < 20.0) break;
      if (abs(jet_eta) > 4.0)  continue;
        njets++;
//******************W->qq*****************************************  

      for(HepMC::GenEvent::particle_const_iterator p = HepMCEvt->particles_begin();
        p!= HepMCEvt->particles_end(); ++p ){
        int pid=(*p)->pdg_id();        
//        if ((*p)->status()!=1)continue;
      
      if (abs(pid) ==1 || abs(pid) ==2 || abs(pid) ==3 || abs(pid) ==4){
      double lqpt =(*p)->momentum().perp();
      double lqphi=(*p)->momentum().phi();
      double lqeta=(*p)->momentum().eta();
//      if(lqpt < 20 || fabs(lqeta) > 2.5)continue;
	if ( (*p)->production_vertex() ) {
	  for ( HepMC::GenVertex::particle_iterator mother = 
		  (*p)->production_vertex()->particles_begin(HepMC::parents);
		mother!=(*p)->production_vertex()->particles_end(HepMC::parents); 
		++mother )  {
	   if(abs((*mother)->pdg_id())!=24) continue;//W
    	   double DRJetB = deltaR(jet_eta,lqeta,jet_phi,lqphi);
           if(DRJetB > 0.2) continue; 	
	      i] = jet_px;
           Wy[i] = jet_py;
           Wz[i] = jet_pz;
           We[i] = jet_e;
           Wpt[i]= jet_et;
        
	if (Wpt[i] > max){
        second_max=max;
        max=Wpt[i];
        high1=true;}
        else if (Wpt[i] > second_max){
        second_max =Wpt[i];
        high2=true;}
	  }      	                                            
      }
     }
    }
      
         
//      if(jet_et<20. || fabs(jet_eta)>3.0)continue;

      //////////////////// BJETS ///////////////////////////
      for(HepMC::GenEvent::particle_const_iterator p = HepMCEvt->particles_begin(); 
	  p!= HepMCEvt->particles_end(); ++p ){
	int pid=(*p)->pdg_id();
	// 	if((*p)->status()<21 || (*p)->status()>29)continue;
	if(abs(pid)!=5 && abs(pid)!=4)continue;
	double b_pt=(*p)->momentum().perp();
	double b_eta=(*p)->momentum().eta();
	double b_phi=(*p)->momentum().phi();
	if(b_pt<20 || fabs(b_eta)>3.0)continue;
	double DRJetB=deltaR(jet_eta,b_eta,jet_phi,b_phi);
	if(DRJetB<0.4){
	  if((abs(pid)==5 && rand()%100<60) || (abs(pid)==4 && rand()%100<10)){
//	    nbjets++;
	    hbjetet->Fill(jet_et);
	    hbjeteta->Fill(jet_eta);
	    hbjetphi->Fill(jet_phi);
	    bjet bj;
	    bj.px=jet_px;
	    bj.py=jet_py;
	    bj.pz=jet_pz;
	    bj.e=jet_e;
	    bj.eta=jet_eta;
	    bj.phi=jet_phi;
	    bjets.push_back(bj);
	    if (jet_et < 50) nbjets++;
	    break;
	  }
	}	
      }
      
    }//loop over jets     

   
     hjetmul->Fill(njets);
     hbjetmul->Fill(nbjets);
     
//    if(njets!=2)continue;//2 jets with pt>20 and eta>3.0
    if  ((high1*high2)!=1) continue;
      passedJetCut++;
    
    if(nbjets != 2)continue; //2 bjets with 
    passedBJetCut++;
    
     double Wjet_e1,Wjet_px1,Wjet_py1,Wjet_pz1,Wjet_e2,Wjet_px2,Wjet_py2,Wjet_pz2;
      for (int j=0; j<= ns;j++){
          if (Wpt[j] == max){           
           Wjet_px1= Wx[j];
	   Wjet_py1= Wy[j];
	   Wjet_pz1= Wz[j];
	   Wjet_e1= We[j];
	   }
	   
      else if (Wpt[j] == second_max){
           Wjet_px2= Wx[j];
	   Wjet_py2= Wy[j];
	   Wjet_pz2= Wz[j];
	   Wjet_e2= We[j];
	   }	   
	}
    double Whade  = Wjet_e1+Wjet_e2;
    double Whadpx = Wjet_px1+Wjet_px2;
    double Whadpy = Wjet_py1+Wjet_py2;
    double Whadpz = Wjet_pz1+Wjet_pz2;
    double Whadpt = sqrt(pow(Whadpx,2)+pow(Whadpy,2));
    double Wmasshad=sqrt(pow(Whade,2)-pow(Whadpx,2)-pow(Whadpy,2)-pow(Whadpz,2));  
    hWmasshad->Fill(Wmasshad);
    hWhadpt->Fill(Whadpt);
//    cout<<"Wmass had == "<<Wmasshad<<endl;

    if (Wmasshad < 60 || Wmasshad > 100) continue;
    passedWmassCut++;

    
   
    double b1pt=sqrt(pow(bjets[0].px,2)+pow(bjets[0].py,2));
    double b2pt=sqrt(pow(bjets[1].px,2)+pow(bjets[1].py,2));
//    if(b1pt<50. && b2pt<50.)continue;
//    passedBJetPtCut++;

 
   
    
//    double DRb1b2=deltaR(bjets[0].eta,bjets[1].eta,bjets[0].phi,bjets[1].phi);
//    cout<<"DR(b1,b2)  ===  "<<DRb1b2<<endl;
    double toppt = sqrt(pow(Whadpx+bjets[0].px,2)+ pow(Whadpy+bjets[0].py,2));
    htoppt->Fill(toppt);
    double topmass1=sqrt(pow(Whade+bjets[0].e,2)-
			 pow(Whadpx+bjets[0].px,2)-
			 pow(Whadpy+bjets[0].py,2)-
			 pow(Whadpz+bjets[0].pz,2));    
    
    double topmass2=sqrt(pow(Whade+bjets[1].e,2)-
			 pow(Whadpx+bjets[1].px,2)-
			 pow(Whadpy+bjets[1].py,2)-
			 pow(Whadpz+bjets[1].pz,2));    
    
    double diff1=fabs(topmass1-173.);
    double diff2=fabs(topmass2-173.);
    
    double topmass=0;

    if(diff1<diff2)topmass=topmass1;
    else
      topmass=topmass2;
//   cout<<"topmass== "<<topmass<<endl;
    htopmass->Fill(topmass);
    double topphi=atan2(Whadpx+bjets[1].px,Whadpy+bjets[1].py);
    double bphi = atan2(bjets[0].px,bjets[0].py);
    double deltaphitb = deltaphi(topphi,bphi);

    hdeltaphitb->Fill(deltaphitb);   
    
    if(topmass<150 || topmass>190)continue;
    passedTopCut++;

    double chmass=sqrt(pow(Whade+bjets[0].e+bjets[1].e,2)-
		       pow(Whadpx+bjets[0].px+bjets[1].px,2)-
		       pow(Whadpy+bjets[0].py+bjets[1].py,2)-
		       pow(Whadpz+bjets[0].pz+bjets[1].pz,2));
		       
    if (deltaphitb < 3.0) continue;
    passedphiCut++;
    double chpt=sqrt(pow(Whadpx+bjets[0].px+bjets[1].px,2)+pow(Whadpy+bjets[0].py+bjets[1].py,2));	       
    hchpt->Fill(chpt);
    hchmass->Fill(chmass);

    delete HepMCEvt;
    if(iEvent%100000==0){
      cout<<"================================="<<endl;
      cout<<"passedJetCut :"<<passedJetCut<<endl;
      cout<<"passedWmassCut :"<<passedWmassCut<<endl;
      cout<<"passedBJetCut :"<<passedBJetCut<<endl;
      cout<<"passedTopCut :"<<passedTopCut<<endl;
      cout<<"passedphiCut :"<<passedphiCut<<endl;

    }
    // End of event loop. Done.
  }//
  pythia.stat();
  double sigmafb = pythia.info.sigmaGen() * 1.0E12;
  
  cout<<"++++++++++++++++++"<<endl;
  cout<<"cross section is : "<<sigmafb<<" fb."<<endl;
  cout<<"++++++++++++++++++"<<endl;

  cout<<"============================"<<endl;
  cout<<" number of events analyzed  : "<<nev<<endl;
  cout<<" passing 2 Jets eff %      : "<<100*double(passedJetCut)/nev<<endl;
  cout<<" passing 2 bJets eff %   : "<<100*double(passedBJetCut)/passedJetCut<<endl;
  cout<<" passing W mass cut eff %   : "<<100*double(passedWmassCut)/passedBJetCut<<endl;
  cout<<" passing Top mass cut eff % : "<<100*double(passedTopCut)/passedWmassCut<<endl;
  cout<<" passing Dphi(t,b) eff %   : "<<100*double(passedphiCut)/passedTopCut<<endl;
  cout<<" total eff %                : "<<100*double(passedphiCut)/nev<<endl;
  cout<<"============================"<<endl;
  cout<<" Expected number of events at 1 fb-1 :"<<sigmafb*double(passedphiCut)/nev<<endl;
  cout<<"==========================="<<endl;
  f.cd();
  f.Write();
  f.Close();
  
     
  ofstream outp("NumberOfEvents.txt");
  outp<<nev<<endl;
  outp<<passedJetCut<<endl;
  outp<<passedWmassCut<<endl;
  outp<<passedBJetCut<<endl;
  outp<<passedTopCut<<endl;
  outp<<passedphiCut<<endl;
  outp.close();
  return 0;
}
