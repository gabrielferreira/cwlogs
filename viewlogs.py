from boto import logs
import os
s_key = os.environ.get('AWS_SECRET_ACCESS_KEY_ID')
a_key = os.environ.get('AWS_ACCESS_KEY_ID')
region = os.environ.get('REGION')
print 'conectando'
conn = logs.connect_to_region(region_name=region, aws_access_key_id=a_key, aws_secret_access_key=s_key)
l_group_name = 'Osklen-Webstore-PROD'
log_streams = []
events = []
l_stream_name_like = ''
l_stream_name_prefix = None

print 'pegando log_streams pelo log_group'

def filter_stream_name(l_s_name, l_s):
    return filter(lambda x: x[u'logStreamName'].__contains__(l_s_name), l_s)

def concat_log_streams(l_streams, _next_token=None):
    l_stream = conn.describe_log_streams(log_group_name=l_group_name, log_stream_name_prefix=l_stream_name_prefix, limit=50)
    l_streams += filter_stream_name(l_stream_name_like, l_stream['logStreams'])
    if l_stream.has_key('nextToken') and l_stream['nextToken'] and l_stream['logStreams']:
        concat_log_streams(l_streams, l_stream['nextToken'])

concat_log_streams(log_streams)
import ipdb; ipdb.set_trace()
print 'filtrando log_streams'
# log_streams = filter(lambda x: x[u'logStreamName'].__contains__(l_stream_name_like), log_streams)

def concat_event(_log_group_name, _log_stream_name, _next_token, evs):
    event = conn.get_log_events(log_group_name=_log_group_name, log_stream_name=_log_stream_name, start_from_head=False, next_token=_next_token)
    evs += event['events']
    if event.has_key('nextBackwardToken') and event['nextBackwardToken'] and event.has_key('events') and event['events']:
        concat_event(_log_group_name, _log_stream_name, event['nextBackwardToken'], evs)

print 'pegando log_events'
for ls in log_streams:
    concat_event(l_group_name, ls[u'logStreamName'], None, events)

events = sorted(events, key=lambda k: k['timestamp'], reverse=True)
import ipdb; ipdb.set_trace()
with open('result', 'w') as f:
    f.write('\n'.join(l['message'] for l in events))
