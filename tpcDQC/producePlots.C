producePlots(int run=5213, string in_dir="/home/reinhold/data/CAPTAIN/", string out_dir="html/figures/"){
  using namespace std;
  //these are input parameters supposed to be passed to this script
  //string in_dir="/home/reinhold/data/CAPTAIN/";
  //int run=5213;
  //string out_dir=in_dir + "html/figures/";
  out_dir = in_dir+out_dir;

  vector<string> vVars;
  vVars.push_back("baseline");
  vVars.push_back("pedestalRMS");
  vVars.push_back("shutoff");
  vVars.push_back("pulseCheckPositive");
  vVars.push_back("pulseCheckNegative");
  vVars.push_back("eventTiming");
  
  vector<string> vCh;
  vCh.push_back("wire");
  vCh.push_back("ch");
  vCh.push_back("conn_ch");
  vCh.push_back("disc_ch");

  TFile *f=new TFile(Form("%s/tpcDQC_%d.root", in_dir.c_str(), run));

  vector<string>::iterator itVars = vVars.begin();
  vector<string>::iterator itCh = vCh.begin();

  //loop through all histograms and plot them
  for(itVars = vVars.begin();itVars!=vVars.end();itVars++){
    //cout << itVars).c_str() << endl;;
    if (!itVars->compare("eventTiming")){
      cout << Form("*** %s", itVars->c_str()) << endl;;
      TH1F *h1 = (TH1F *)f->Get(Form("%s", itVars->c_str()));
      h1->Draw();
      c1->SaveAs(Form("%s/%s_run%d.png", out_dir.c_str(), itVars->c_str(), run));
      continue;
    }
    
    for(itCh = vCh.begin();itCh!=vCh.end();itCh++){
      cout << Form("%s_%s", itVars->c_str(), itCh->c_str()) << endl;;
      //cout << itVars) << ", " << itCh) << endl;
      TH1F *h1 = (TH1F *)f->Get(Form("%s_%s", itVars->c_str(), itCh->c_str()));
      h1->Draw();
      c1->SaveAs(Form("%s/%s_%s_run%d.png", out_dir.c_str(), itVars->c_str(), itCh->c_str(), run));
    } 
  }

  //outdir
}

//from visualisation.py
//array_variables = [('baseline',1), ('pedestalRMS',1), ('shutoff',2), ('pulseCheckPositive',2), ('pulseCheckNegative',2), ('eventTiming',2)] #list the variables with the second argument being the importance of the variable: 1 is most important, 2nd is less, 0 is disabled
//array_ch = [('wire',1), ('ch',2), ('conn_ch',2), ('disc_ch',2)]
