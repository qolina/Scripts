
# phrase:(new_id, phrase_type, phrase_span, phrase_text, event_types)
# event :[(role_name, phrase_span, phrase_id_num)]

import sys
import os

EVENT_types = ["Transaction", "PersonEvent", "Quantity", "Policy", "Project", "Lawsuit", "Investigation", "General"]

def obtainAnn(ann_dir_path):
	debug = False

	file_list = os.listdir(ann_dir_path)
	events_in_docs = []
	phrases_in_docs = []
	for ann_file in sorted(file_list):
		if not ann_file.endswith(".ann"): continue
		#if ann_file[:5] in ["DP001", "GS004"]: continue
		#if ann_file[:5] not in ["DP005"]: continue
		#if ann_file[:5] not in ["GS005"]: continue
		content = open(ann_dir_path + ann_file, "r").readlines()
		events_in_doc = []
		phrases_in_doc = []
		phrase_id_remap = {} # old_id:new_id

		if len(content) == 0: 
			events_in_docs.append(events_in_doc)
			phrases_in_docs.append(phrases_in_doc)
			continue

# phrase
# in: (T1, event_type|phrase st ed, text)
# out:(new_id, phrase_type, phrase_span, phrase_text, event_type)
		phrases_raw = [line.strip().split("\t") for line in content if line.startswith("T")]
		st_phrases = [(int(phrase[1].split()[1]), phrase) for phrase in phrases_raw]
		sorted_phrases_by_st = sorted(st_phrases, key = lambda a:a[0])

		for st, phrase in sorted_phrases_by_st:
			old_phrase_id, type_span, text = phrase

			new_phrase_id = old_phrase_id[0] + str(len(phrases_in_doc)+1)
			phrase_type = type_span.split()[0]
			phrase_span = type_span.split()[1:3]
			phrase_span = (int(phrase_span[0]), int(phrase_span[1]))
			phrase_text = text

			phrase_id_remap[old_phrase_id] = int(new_phrase_id[1:]) - 1
			new_phrase = (new_phrase_id, phrase_type, phrase_span, phrase_text, [])
			phrases_in_doc.append(new_phrase)

		#if debug:
		#	for phrase in phrases_in_doc:
		#		outputPhrase(phrase)

# event
# in: (E1, trigger:T1 role:T2 role:T3)
# out:(role_name, phrase_span, phrase_id_num)
		events_raw = [line.strip().split("\t") for line in content if line.startswith("E")]
		for event in events_raw:
			roles_in_event = []
			_, role_all = event
			roles = role_all.split()
			event_type = roles[0].split(":")[0]
			for role in roles:
				role_name, old_phrase_id = role.split(":")
				new_phrase_id_num = phrase_id_remap[old_phrase_id]
				phrases_in_doc[new_phrase_id_num][-1].append(event_type)
				if debug:
					phrase = phrases_in_doc[new_phrase_id_num]
					outputPhrase(phrase)
				
				new_role = (role_name, phrase[2], new_phrase_id_num)
				roles_in_event.append(new_role)

			events_in_doc.append(roles_in_event)
		#if debug:
			#for event in events_in_doc:
			#	outputEvent(event)
		if 0:
			for phrase in phrases_in_doc:
				outputPhrase(phrase)

		events_in_docs.append(events_in_doc)
		phrases_in_docs.append(phrases_in_doc)

	return events_in_docs, phrases_in_docs

def spanComp(span1, span2, strictFlag):
	if strictFlag:
		if span1 == span2: return True
		else: return False
	else:
		common = set(range(span1[0], span1[1])).intersection(set(range(span2[0], span2[1])))
		len1 = span1[1]-span1[0]
		len2 = span2[1]-span2[0]
		min_len = min(len1, len2)
		if len(list(common)) >= min(min_len*0.5, 1): return True
		else: return False
	
def triggerSame(phrase1, phrase2, span_strict_flag):
	debug = False
	id1, type1, span1, text1, event_types1 = phrase1
	id2, type2, span2, text2, event_types2 = phrase2
	iden_flag = True if spanComp(span1, span2, span_strict_flag) else False
	class_flag = True if iden_flag and (type1 == type2) else False
	if debug:
		if iden_flag != class_flag:
			print "-- iden , class, ", iden_flag, class_flag
			outputPhrase(phrase1)
			outputPhrase(phrase2)
	return iden_flag, class_flag

def phraseSame(phrase1, phrase2, span_strict_flag):
	id1, type1, span1, text1, event_types1 = phrase1
	id2, type2, span2, text2, event_types2 = phrase2
	event_type_flag = True if len(list(set(event_types1)&set(event_types2))) > 0 else False
	iden_flag = True if event_type_flag and spanComp(span1, span2, span_strict_flag) else False
	class_flag = True if iden_flag and (type1 == type2) else False
	return iden_flag, class_flag


def roleSame(role1, role2, span_strict_flag):
	role_name1, role_span1, _ = role1
	role_name2, role_span2, _ = role1
	iden_flag = True if spanComp(role_span1, role_span2, span_strict_flag) else False
	class_flag = True if iden_flag and (role_name1 == role_name2) else False
	return iden_flag, class_flag
	
# event1 -> event_gold
#def eventSame(event1, event2):
#	trigger_in_event1, roles_in_event1 = event1[0], event1[1:]
#	trigger_in_event2, roles_in_event2 = event2[0], event2[1:]
#
#	trigger_iden_flag, trigger_class_flag = roleSame(trigger_in_event1, trigger_in_event2)
	#roles_same = [(role1[0], role2[0]) for role1 in roles_in_event1 for role2 in roles_in_event2 if roleSame(role1, role2)]
	#roles_same_flag = True if len(roles_same) >= len(roles_in_event1)*0.5: else False


# item_flag: trigger or phrase 
# eval_flag: iden or class
def agreement(items_in_docs_gold, items_in_docs, item_flag, eval_flag, span_strict_flag):
	debug = False

	common_in_docs = []
	num_in_docs_gold = []
	num_in_docs = []
	for items_in_doc, items_in_doc_gold in zip(items_in_docs_gold, items_in_docs):
		common_in_doc = []
		for item in items_in_doc:

			if item_flag == "trigger":
				if eval_flag == "iden":
					item_matched = [item_id_gold for item_id_gold, item_gold in enumerate(items_in_doc_gold) if triggerSame(item_gold, item, span_strict_flag)[0]]
				elif eval_flag == "class":
					item_matched = [item_id_gold for item_id_gold, item_gold in enumerate(items_in_doc_gold) if triggerSame(item_gold, item, span_strict_flag)[1]]

			if item_flag == "phrase":
				if eval_flag == "iden":
					item_matched = [item_id_gold for item_id_gold, item_gold in enumerate(items_in_doc_gold) if phraseSame(item_gold, item, span_strict_flag)[0]]
				elif eval_flag == "class":
					item_matched = [item_id_gold for item_id_gold, item_gold in enumerate(items_in_doc_gold) if phraseSame(item_gold, item, span_strict_flag)[1]]

			if len(item_matched) > 0:
				common_in_doc.append(len(item_matched))
				if debug:
					outputPhrase(item)
					for item_id_gold in item_matched:
						item_gold = items_in_doc_gold[item_id_gold]
						outputPhrase(item_gold)
						iden_flag, class_flag = triggerSame(item_gold, item, span_strict_flag)
						print "-- trigger iden , class, ", iden_flag, class_flag
						iden_flag, class_flag = phraseSame(item_gold, item, span_strict_flag)
						print "-- phrase iden , class, ", iden_flag, class_flag
			else:
				if 1:
					print "-- missed gold: ",
					outputPhrase(item)

		common_in_docs.append(len(common_in_doc))
		num_in_docs_gold.append(len(items_in_doc_gold))
		num_in_docs.append(len(items_in_doc))

	common = sum(common_in_docs)
	num_gold = sum(num_in_docs_gold)
	num = sum(num_in_docs)

	if debug:
		print "-- common, num_gold, num:", common, num_gold, num
		print "-- common_in_docs", common_in_docs
		print "-- num_in_docs_gold", num_in_docs_gold
		print "-- num_in_docs", num_in_docs

	if common == 0: return 0.0, 0.0, 0.0

	pre = common*100.0/num
	rec = common*100.0/num_gold
	f1 = 2*pre*rec/(pre+rec)

	return pre, rec, f1

def outputEvent(event):
	print "############## Event:"
	for role_in_event in event:
		outputRole(role_in_event)

def outputRole(role):
	print role
	#print role[:2],
	#outputPhrase(role[2])

def outputPhrase(phrase):
	print phrase[:3], phrase[3], phrase[4]

def outputPRF(arr):
	Tab = "\t"
	arr = ["%.2f"%i for i in arr]
	print "-- Pre, Rec, F1:", Tab, arr[0], Tab, arr[1], Tab, arr[2]

def obtainTrigger(phrases_in_docs):
	triggers_in_docs = []
	args_in_docs = []

	for phrases_in_doc in phrases_in_docs:
		triggers_in_doc = []
		args_in_doc = []
		for phrase in phrases_in_doc:
			phrase_id, phrase_type, phrase_span, phrase_text, event_types = phrase
			if phrase_type in EVENT_types:
				triggers_in_doc.append(phrase)
			else:
				args_in_doc.append(phrase)
		triggers_in_docs.append(triggers_in_doc)
		args_in_docs.append(args_in_doc)

	return triggers_in_docs, args_in_docs

if __name__ == "__main__":
	print "Usage: python .py annDirPath1 annDirPath2"
	print sys.argv

	ann_dir_path_1 = sys.argv[1]
	ann_dir_path_2 = sys.argv[2]
	
	events_in_docs1, phrases_in_docs1 = obtainAnn(ann_dir_path_1)
	events_in_docs2, phrases_in_docs2 = obtainAnn(ann_dir_path_2)

	triggers_in_docs1, args_in_docs1 = obtainTrigger(phrases_in_docs1)
	triggers_in_docs2, args_in_docs2 = obtainTrigger(phrases_in_docs2)

	#prf_trigger = agreement(triggers_in_docs1, triggers_in_docs2, "trigger", "iden")
	#outputPRF(prf_trigger)
	prf_trigger = agreement(triggers_in_docs1, triggers_in_docs2, "trigger", "class", False)
	outputPRF(prf_trigger)

	#prf_phrase = agreement(args_in_docs1, args_in_docs2, "phrase", "iden")
	#outputPRF(prf_phrase)
	prf_phrase = agreement(args_in_docs1, args_in_docs2, "phrase", "class", False)
	outputPRF(prf_phrase)

