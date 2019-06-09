import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "gitbot-uqjriq"

from firebase import firebase

firebase = firebase.FirebaseApplication('https://gitbot-uqjriq.firebaseio.com/', None)

import github3

github = github3.login(token=token)


def get_repos(parameters):
	global firebase
	l=['List of Respositories: ' ]
	for short_repository in github.repositories_by(parameters.get('username')):
		l.append(str(short_repository))
	str2= "\n".join(l)
	firebase.post("/post",str2)
	return str2[:1000]

def get_issues(parameters):
	global firebase
	l=[]
	print('p', parameters)
	for issue in github3.issues_on(parameters.get('username'),parameters.get('repo')):
		print('p', issue.number)
		l.append(str('#{}: "{}"\n\t{}'.format(issue.title, issue.number, issue.html_url)))

	str2= "\n".join(l)
	
	firebase.post("/issues",str2)
	if len(str2) is not 0:
		return "Issues are \n" + str2
	else:
		return "No issues found"

'''
def firebase(parameters):
	firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
	result1[] = firebase.get(parameters.get('username'), None)
	return result1

'''


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def fetch_reply(query, session_id):
	response = detect_intent_from_text(query,session_id)
	print("............")
	print(response.parameters)
	if response.intent.display_name =='get_repo':
		return get_repos(dict(response.parameters))
	elif response.intent.display_name=='get_issues':
		return get_issues(dict(response.parameters))
		
	else:
		return response.fulfillment_text




'''
for short_repository in github.repositories_by('harshgarg27'):
	print(short_repository)
	'''