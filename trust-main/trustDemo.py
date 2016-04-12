from __future__ import print_function
import logging
import urllib2
import json


logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)
apikey = 'tiNFg9zDKRWXaIpI8pPyWbXd4ACa9ZDt'


def lambda_handler(event, context):
    """
    Event handler used for AWS Lambda service.
    :return: json
    """
    try:
        logger.info("Test: " + str(event))
        company = event['Domain']
        logger.info('Company=' + company)

        sfindurl = r"https://api.trustpilot.com/v1/business-units/find?name={0}"
        req = urllib2.Request(sfindurl.format(company))
        req.add_header('ApiKey', apikey)
        resp = urllib2.urlopen(req).read()
        response = json.loads(resp)
        buisnessUId = response['id']
        logger.debug(buisnessUId)
        sreviewurl = r"https://api.trustpilot.com/v1/business-units/{0}/reviews?apikey={1}"
        reviewurl = sreviewurl.format(buisnessUId, apikey)
        reviewstr = urllib2.urlopen(reviewurl).read()
        d = json.loads(reviewstr)
        logger.debug(d['reviews'])
        persons = 0
        ratingsum = 0
        for n in d['reviews']:
            persons += 1
            ratingsum += int((n['stars']))
        rating = (float(ratingsum/float(persons)))

        return {"Result": "Successfully", "Domain": company, "RatingReslut": rating}
    except Exception as e:
        logger.error("!!!! -- CRITICAL ERROR -- !!!! := " + str(e.message))
        return {"Result": "Error", "Domain": "unknown", "RatingReslut": 0.0}


if __name__ == '__main__':
    _event = {"Domain": "www.dan-ejendomme.dk"}
    test = lambda_handler(_event, None)

    print (test)
