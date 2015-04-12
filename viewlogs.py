from boto import logs
import os, sys, getopt
l_group_name = ''
log_streams = []
events = []
l_stream_name_like = ''
l_stream_name_prefix = None
s_time = None
e_time = None

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"ha:s:r",["access_key=","secret_key=", "region="])
    except getopt.GetoptError:
        print 'viewlogs.py'
    sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'viewlogs.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-a", "--access_key"):
            a_key = arg
        elif opt in ("-s", "--secret_key"):
            s_key = arg
        elif opt in ("-r", "--region"):
            s_key = arg

    if not a_key:
        a_key = os.environ.get('AWS_ACCESS_KEY_ID') if os.environ.has_key('AWS_ACCESS_KEY_ID') else None
    if not s_key:
        s_key = os.environ.get('AWS_SECRET_ACCESS_KEY_ID') if os.environ.has_key('AWS_SECRET_ACCESS_KEY_ID') else None
    if not region:
        region = os.environ.get('REGION') if os.environ.has_key('REGION') else 'us-east-1'

if __name__ == "__main__":
    main(sys.argv[1:])

print 'getting log_streams by log_group'

def connect(region_name=region, aws_access_key_id=a_key, aws_secret_access_key=s_key):
    conn = logs.connect_to_region(region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

print 'connecting'
connect()

def filter_stream_name(l_s_name, l_s):
    return filter(lambda x: x[u'logStreamName'].__contains__(l_s_name), l_s)

def concat_log_streams(l_streams, _next_token=None):
    l_stream = conn.describe_log_streams(log_group_name=l_group_name, log_stream_name_prefix=l_stream_name_prefix, limit=50)
    l_streams += filter_stream_name(l_stream_name_like, l_stream['logStreams'])
    if l_stream.has_key('nextToken') and l_stream['nextToken'] and l_stream['logStreams']:
        concat_log_streams(l_streams, l_stream['nextToken'])

concat_log_streams(log_streams)
print 'filtering log_streams'
if l_stream_name_like:
    log_streams = filter(lambda x: x[u'logStreamName'].__contains__(l_stream_name_like), log_streams)

def concat_event(_log_group_name, _log_stream_name, _next_token, evs):
    event = conn.get_log_events(log_group_name=_log_group_name, log_stream_name=_log_stream_name, start_from_head=False, next_token=_next_token, start_time=s_time, end_time=e_time)
    evs += event['events']
    if event.has_key('nextBackwardToken') and event['nextBackwardToken'] and event.has_key('events') and event['events']:
        concat_event(_log_group_name, _log_stream_name, event['nextBackwardToken'], evs)

print 'getting log_events'
for ls in log_streams:
    concat_event(l_group_name, ls[u'logStreamName'], None, events)

events = sorted(events, key=lambda k: k['timestamp'], reverse=True)
with open('le%s' % (datetime.now().strftime("%Y%m%d-%H%M%S%f")), 'w') as f:
    f.write('\n'.join(l['message'] for l in events))
