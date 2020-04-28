from crhelper import CfnResource
import logging
import string
import random

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL')

string_length = 6


######## ######## ######## ######## ######## ######## ######
######## BELOW CODE HANDLES CLOUDFORMATION REQUESTS ########
######## ######## ######## ######## ######## ######## ######


@helper.create
def build_and_return_bucket_name(event, context):
    try:
        logger.info('Received request to build a random bucket name.')
        properties = event.get('ResourceProperties', {})
        bucket_prefix= properties.get('bucket_prefix')
        if not bucket_prefix or len(bucket_prefix) == 0:
            raise Exception('Must provide a bucket_prefix value in properties')

        random_bucket_name = bucket_prefix+"-"+generate_random_guid()
        helper.Data.update({"bucket_name": random_bucket_name.lower()})

    except Exception as e:
        logger.error(e)
        raise e

def generate_random_guid():
    try:
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=string_length))
        return str(res)
    except Exception as e:
        raise e

@helper.update
def no_op(_, __):
    pass


@helper.delete
def no_op(_, __):
    pass


def handler(event, context):
    helper(event, context)