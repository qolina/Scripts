#pragma once

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

#include "Parameter.h"
#include "LanguageModel.h"
#include "RuleTable.h"
class TopicModel;
class CohesionModel;
/** 
*	@brief: This class is responsible for analyzing command line and configuration file to get the necessary parameters.
*/
class StaticData
{
public:	
	~StaticData();

public:
	/**
	 * @brief: Get instance of StaticData, as Single Patton
	 * @return: A const reference to StaticData object
	 */	
	static const StaticData& Instance() { return s_instance; }
	/**
	 * @brief: Load static data 
	 * @param[in] param: Parameter which tells how and where to load the static data
	 * @return: true for success and false if fail
	 */	
	static bool LoadDataStatic(Parameter * param)
	{ 
		return s_instance.LoadData(param);
	}

	/**	
	*	@brief: Initialize each variable by param( in fact by m_setting of param), for future use. This method is responsible for initializing data based on a Parameter instance. The data includes translation table, language table and some parameters used in the search process
	*
	*	@param[in] param:		configuration file for decoder
	*	@return: 	true for success, false for fail
	*/	
	bool LoadData(Parameter * param);	

private:
	/**
	 * @brief: constructor of StaticData
	 */	
	StaticData();
	static StaticData	s_instance;
	
	Parameter	*m_parameter;
	string m_ruleFile;
	string m_lmFile;

	float m_weightRuleCount;
	float m_weightGlueCount;
	float m_weightLM;
	float m_weightWordPenalty;

	float m_weightSynCount;
	float m_weightHyperCount;
	float m_weightHyponCount;

public:

	RuleTable	*s_ruleTable; 
	size_t	s_ruleTableLimit;
	float	s_ruleTableThres; 
	size_t s_ruleFeatCount;


	LanguageModel	*s_languageModel; 
	size_t s_nGramOrder; 


	bool s_isUseRuleCount;
	bool s_isUseGlueCount;
	bool s_isUseWP;
	bool s_isUseLM;	
	

	bool s_isUseSynCount;
	bool s_isUseHyperCount;
	bool s_isUseHyponCount;

	vector<float> s_weightRule;
	vector<float> s_allWeight;

	
	size_t s_ruleLenLimit; //rule source side length
	size_t s_ruleSpanLimit; //cover lenght of source side
	//size_t s_varSpanLimit; 
	size_t s_nBestSize;
	size_t s_candLimit;
	size_t s_transLimit;

	std::string s_inputFile;
	std::string s_outputFile;
	int s_refCount;
	string s_nBestFile;


	size_t s_verboseLevel;

	string doc_id_file_;
	TopicModel * topic_model_;
	CohesionModel * cohesion_model_;

	bool is_use_cohesion_;

	int use_topic_rule_type_;

	bool is_use_doc_topic_;
	bool is_use_trg_doc_topic_;
	bool is_use_doc_topic_theta_;
	bool is_use_sent_topic_;
	bool is_use_local_topic_;
	bool is_use_var_topic_;
	bool is_use_cover_topic_;
	bool is_use_adapt_lex_; 

	float weight_doc_topic_;
	float weight_trg_doc_topic_;
	float weight_doc_topic_theta_;
	float weight_sent_topic_;	
	float weight_local_topic_;
	float weight_var_topic_;
	float weight_cover_topic_;
	float weight_adpat_lex_;
	
	bool is_use_per_dt_;
	bool is_use_per_tdt_;
	float weight_per_dt_;
	float weight_per_tdt_;
};
