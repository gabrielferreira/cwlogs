from boto import logs
import os
s_key = os.environ.get('AWS_SECRET_ACCESS_KEY_ID')
a_key = os.environ.get('AWS_ACCESS_KEY_ID')
region = os.environ.get('REGION')
conn = logs.connect_to_region(region_name=region, aws_access_key_id=a_key, aws_secret_access_key=s_key)

events = []
for ls in conn.describe_log_streams(log_group_name='access_log')['logStreams']:
    event = conn.get_log_events(log_group_name='access_log', log_stream_name=ls[u'logStreamName'])
    events += event['events']

import ipdb; ipdb.set_trace()
