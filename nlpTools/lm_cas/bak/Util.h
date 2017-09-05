#pragma once
#include <vector>
#include <string>
#include <sstream>
#include <iostream>
#include <limits>
#include <cmath>
#include "StaticData.h"


using namespace std;

typedef std::pair<int,int> Span;
typedef std::vector<Span> VecSpan;
typedef std::vector<std::string> VecStr;
typedef std::vector<int> VecInt;

//some default value
const std::string X1 = "$X_1";
const std::string X2 = "$X_2";
const std::string DELIM = " ||| "; 

const float LOG_E_10 = 2.30258509299405f;
const float NATURAL_LOG = (float)2.718;

const float MAX_FLOAT = std::numeric_limits<float>::max();
const float MIN_FLOAT = -std::numeric_limits<float>::max();
const int MAX_INT = std::numeric_limits<int>::max();
const int MIN_INT = std::numeric_limits<int>::min();

/** 
*	@brief: verbose macros
*/
#define TRACE_ERR(str) std::cerr << str
#define VERBOSE(level,str) { if (StaticData::Instance().s_verboseLevel >= level) { TRACE_ERR(str); } }
#define IFVERBOSE(level) if (StaticData::Instance().s_verboseLevel >= level)

//#define TRACE_ERR(str) std::cerr << str
//#define VERBOSE(level,str) { if (1 >= level) { TRACE_ERR(str); } }
//#define IFVERBOSE(level) if (1 >= level)

/** 
*	@brief:	Token a string, 
*
*	@param[in] str:	The string to be token
*	@param[in] delimiters:	The delimiters for split str, default is table character(ASCII 0x9)
*	@return:	The token result, as a vector
*/
inline std::vector<std::string> Tokenize(const std::string& str,
										 const std::string& delimiters = " ||| ")
{
	std::vector<std::string> tokens;
	// Skip delimiters at beginning.
	std::string::size_type lastPos = str.find_first_not_of(delimiters, 0);
	// Find first "non-delimiter".
	std::string::size_type pos     = str.find_first_of(delimiters, lastPos);

	while (std::string::npos != pos || std::string::npos != lastPos)
	{
		// Found a token, add it to the vector.
		tokens.push_back(str.substr(lastPos, pos - lastPos));
		// Skip delimiters.  Note the "not_of"
		lastPos = str.find_first_not_of(delimiters, pos);
		// Find next "non-delimiter"
		pos = str.find_first_of(delimiters, lastPos);
	}

	return tokens;
}

/** 
*	@brief:	Token a string, 
*
*	@param[in] str:	The string to be token
*	@param[in] separator:	The delimiters for split str
*	@return:	The token result, as a vector
*/
inline std::vector<std::string> TokenizeMultiCharSeparator(const std::string& str,
														   const std::string& separator)
{
	std::vector<std::string> tokens;

	size_t pos = 0;
	// Find first "non-delimiter".
	std::string::size_type nextPos     = str.find(separator, pos);

	while (nextPos != std::string::npos)
	{
		// Found a token, add it to the vector.
		tokens.push_back(str.substr(pos, nextPos - pos));
		// Skip delimiters.  Note the "not_of"
		pos = nextPos + separator.size();
		// Find next "non-delimiter"
		nextPos	= str.find(separator, pos);
	}
	tokens.push_back(str.substr(pos, nextPos - pos));

	return tokens;
}

/** 
*	@brief:	Delete dropChars from  then end of str
*	@param[in] str:	string for trim
*	@param[in] dropChars:	Characters to be trim
*	@return:	The trim result
*/
inline std::string Trim(const std::string& str, const std::string dropChars)
{
	std::string res = str;
	res.erase(str.find_last_not_of(dropChars)+1);
	return res.erase(0, res.find_first_not_of(dropChars));
}

/** 
*	@brief:	Read an object of T from string input
*
*	@param[in] input:	The string to be read, it will be considered as a string then read
*	@return:	An object of T from string input
*/
template <typename T>
inline T Scan(const std::string input)
{
	std::stringstream stream(input);
	T ret;	
	stream >> ret;	
	return ret;
}

/** 
*	@brief:	Conver string input to a bool result, and return the bool result
*/
inline bool ScanBool(const std::string &input)
{
	std::string lc = input;
	if (lc == "yes" || lc == "y" || lc == "true" || lc == "1")
		return true;
	if (lc == "no" || lc == "n" || lc =="false" || lc == "0")
		return false;

	return false;
	//TRACE_ERR( "Scan<bool>: didn't understand '" << lc << "', returning false" << std::endl);
	//return false;
}

/** 
*	@brief:	Read a serial of object of Type T from string input and return it as an vector
*	@param[in] input:	a vector of objects in the form of string for convert
*	@return:	a vector of objects converted
*/
template<typename T>
inline std::vector<T> Scan(const std::vector< std::string > &input)
{
	std::vector<T> output(input.size());
	for (size_t i = 0 ; i < input.size() ; i++)
	{
		output[i] = Scan<T>( input[i] );
	}
	return output;
}

/** 
*	@brief:	Connect a vector of string to one big string
*	@param[in] vec:	a vector of string to be connected as a big string
*	@return:	The connected big string
*/
inline string Vec2Str(const vector<string> vec)
{
	string ret = "";
	for(size_t i=0; i<vec.size(); i++)
	{
		ret += vec[i];
		if(vec.size()-1 != i)
		{
			ret += " ";
		}
	}
	return ret;
}


/** 
*	@brief:	Return how many words exist in one string
*	@param[in] str:	string for count words
*	@return:	The number of words exist in str
*/
inline int CountWords(const std::string& str)
{
	int count = 0;

	std::istringstream iss(str.c_str());
	std::string w;

	while (iss >> w)
	{
		count++;
	}

	return count;
}

inline std::vector<std::string> Split(const std::string& str) 
{
	string delims = " \t";
	vector<string> tokens;
	string::size_type last_pos = str.find_first_not_of(delims, 0);
	string::size_type pos = str.find_first_of(delims, last_pos);

	while (string::npos != pos || string::npos != last_pos) {
		tokens.push_back(str.substr(last_pos, pos - last_pos)); //found a token
		last_pos = str.find_first_not_of(delims, pos); //skip delimiters
		pos = str.find_first_of(delims, last_pos); // find next non-delimiters
	}
	return tokens;
}

//split by the delimiter
inline vector<string> Split(const string& str, const string& delim)
{
	vector<string> tokens;
	size_t pos = 0;
	string::size_type next_pos = str.find(delim, pos);

	while (string::npos != next_pos) {
		tokens.push_back(str.substr(pos, next_pos - pos));
		pos = next_pos + delim.size();
		next_pos = str.find(delim, pos);
	}
	tokens.push_back(str.substr(pos));
	return tokens;
}

template <typename T>
inline std::string Join(const vector<T>& vec, const std::string& seperator)
{
	stringstream ss;
	for (size_t i = 0; i < vec.size(); i++) {
		ss << vec[i];
		if (vec.size() - 1 != i) 
			ss << seperator;
	}
	return ss.str();
}

inline bool ReadFile(const std::string &file, ifstream &fstream)
{
	fstream.open(file.c_str());
	if (!fstream.good()) {
		cerr << "Error: fail to read file: " << file.c_str() << "." << endl;
		return false;
	}
	return true;
}

inline bool WriteFile(const std::string &file, ofstream &fstream)
{
	fstream.open(file.c_str());
	if (!fstream.good()) {
		cerr << "Error: fail to open file: " << file.c_str() << "." << endl;
		return false;
	}
	return true;
}

template <typename T>
inline T Min(const vector<T>& vec) 
{
	T ret = (T)std::numeric_limits<int>::max();
	for (size_t i = 0; i < vec.size(); i++)
		if (vec[i] < ret)
			ret = vec[i];
	return ret;
}

template <typename T>
inline void Norm(vector<T>& vec) 
{
	double total = 0.0;
	for (size_t i = 0; i < vec.size(); i++) 
		total += vec[i];
	if (total == 0) return;
	for (size_t i = 0; i < vec.size(); i++)
		vec[i] = (T)(vec[i]/total);
}

template <typename T>
inline void NormLogProb(vector<T>& vec) 
{
	double max_score =  std::numeric_limits<int>::min();
	for (size_t i = 0; i < vec.size(); i++) 
		if (max_score < vec[i])
			max_score = vec[i];
	double total = 0.0;
	for (size_t i = 0; i < vec.size(); i++) 
		total += exp(vec[i] - max_score);
	for (size_t i = 0; i < vec.size(); i++)
		vec[i] = (T)(exp(vec[i] - max_score)/total);
}

template <typename T>
inline double LogPerplexity(const vector<T>& vec)
{
	//if (need_norm) Norm<T>(vec);
	double ret = 0.0;
	for (size_t i = 0; i < vec.size(); ++i)
		if (vec[i] > 0)
			ret += vec[i] * log(vec[i]);
		else if (vec[i] < 0) 
			cerr << "@negative " << vec[i] << endl;
	ret = - (ret/log(2.0));
	ret *= 0.1;
	return ret;
}

