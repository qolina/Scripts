
#include <ctime>

#include "LanguageModel.h"
//#include "Util.h"
#include <vector>
#include <iostream>
#include "lmsri.h"
#include <stdlib.h>


// added by qin
#include <fstream>
#include <algorithm>

using namespace std;

LanguageModel::LanguageModel(size_t order,
							 const std::string lmFile)
{
	m_active = false;
	m_order = order;
	m_lmFile = lmFile;
}

LanguageModel::~LanguageModel(void)
{

	if(m_active)
	{
        cerr<<"directly used exit()"<<endl;
        exit(0);
		sriUnloadLM(this->m_lmPtr);
	}

}

bool LanguageModel::Load()
{
	clock_t start = clock();
	this->m_lmPtr = sriLoadLM(m_lmFile.c_str(),1,m_order,1,0);
	clock_t finish = clock();

	if(m_lmPtr)
	{
		m_active = true;
		return true;
	}else{
		return false;
	}
}

float LanguageModel::GetFullScore(const std::string &str)const
{
	float prob = 0;
	int pos = 1;
	size_t order = this->m_order;

	vector<int> wordPosVec;
	int spp1 = 0,
		spp2 = (int)str.find(' ', spp1);
	wordPosVec.push_back(spp1);

	while (spp2 != string::npos)
	{
		spp1 = spp2 + 1;
		wordPosVec.push_back(spp1);
		spp2 = (int)str.find(' ', spp1);
	}

	for (int i = pos; i <= (int)wordPosVec.size(); i++)
	{
		string word = i < (int)wordPosVec.size() ? 
			          str.substr(wordPosVec[i - 1], wordPosVec[i] - 1 - wordPosVec[i - 1]) :
		              str.substr(wordPosVec[i - 1], str.size() - wordPosVec[i - 1]),
			   context = "";

		if (i > 1)
		{
			int start = (i < order) ? 0 : wordPosVec[i - order];
			context = str.substr(start, wordPosVec[i - 1] - 1 - start);
		}

		float p = GetProb(word, context);

		prob += p;

	}

	return prob;
}

float LanguageModel::GetProb(const std::string &word, const std::string &context)const
{
	float ret = sriWordProb(this->m_lmPtr,word.c_str(),context.c_str())*LOG_E_10 ;
    //return ret;
	return ret>-100? ret:-100;
}

//TODO
/*
float LanguageModel::GetProb(const std::string &str, size_t order, size_t position){
	
}*/


// added main function
int main()
{

    string lmFilename = "../lm_models/US_english_lm/en-70k-0.1.lm";
    LanguageModel lm_instance = LanguageModel(3, lmFilename);
//    cout << "LM instance created." << endl;
    lm_instance.Load();
//    cout << "LM instance loaded." << endl;

//    string sentence = "I want to eat an apple";
//    cout << sentence << endl;


    string tweetsFilename = "/home/yxqin/corpus/data_twitter201301/201301_clean/tweetText";
    string dayArr[] = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"};
    for (string dayStr: dayArr)
    {
//        cout << tweetsFilename + dayStr << endl;
        string sentence;
        ifstream tweetsFile (tweetsFilename+dayStr);
        if (tweetsFile.is_open())
        {
            while (getline (tweetsFile, sentence))
            {
                std::transform(sentence.begin(), sentence.end(), sentence.begin(), ::tolower);
                float sen_prob = lm_instance.GetFullScore(sentence);
                cout << sen_prob << "\t";
                cout << sentence << endl;
            }
            tweetsFile.close();
        }
        else cout << "Open file failed." << endl;
        cout << "*****" << endl;
    }

    return 1;

}


