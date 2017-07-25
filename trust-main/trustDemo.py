from __future__ import print_function
from datetime import datetime, timedelta, time
import logging
import urllib2
import json



logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)
apikey = 'tiNFg9zDKRWXaIpI8pPyWbXd4ACa9ZDt'


def getAPIdata(_url):
    """
    request json from url.
    :param _url: string - endpoint to hit.
    :return: json - response from url.
    """
    req = urllib2.Request(_url)
    req.add_header('ApiKey', apikey)
    resp = urllib2.urlopen(req).read()
    return json.loads(resp)


def whatAgeisReview(_reviewdate, _rate):
    newreviewdate = datetime.strptime(_reviewdate.split('T')[0], "%Y-%m-%d")
    now = datetime.now().date()

    if _rate != 5:
        if newreviewdate.date() > (now - timedelta(days=100)):
            return 1
        elif newreviewdate.date() < (now - timedelta(days=100)) and newreviewdate.date() > (now - timedelta(days=400)):
            return 1.05
        else:
            return 1.10
    else:
        return 1


def lambda_handler(event, context):
    """
    Event handler used for AWS Lambda service.
    :return: json
    """
    try:
        domain = event['Domain']
        logger.debug('Domain=' + domain)

        sfindurl = r"https://api.trustpilot.com/v1/business-units/find?name={0}"
        sreviewurl = r"https://api.trustpilot.com/v1/business-units/{0}/reviews?page={1}"

        response = getAPIdata(sfindurl.format(domain))

        buisnessUId = response['id']
        logger.debug(buisnessUId)

        persons = 0
        ratingsum = 0.0
        # Each request returns 20 reviews per. page. We need at the most 300.
        for x in range(1, 16):
            reviews = getAPIdata(sreviewurl.format(buisnessUId, x))
            if not reviews['reviews']:
                break
            logger.debug(reviews)
            logger.debug(reviews['reviews'])

            for review in reviews['reviews']:
                persons += 1
                logger.debug(review['createdAt'])
                ageingfacter = whatAgeisReview(review['createdAt'], int(review['stars']))
                logging.debug(str(float(review['stars']) * float(ageingfacter)) + '  !!  ' + str(ageingfacter))
                ratingsum += (float(review['stars']) * float(ageingfacter))
            rating = (float(ratingsum/float(persons)))
        return {"Result": "Successfully", "Domain": domain, "RatingResult": {"Ratings": persons, "Average": rating}}
    except Exception as e:
        logger.error("!!!! -- CRITICAL ERROR -- !!!! := " + str(e.message))
        return {"Result": "Error", "Domain": "unknown", "RatingResult": 0.0}


if __name__ == '__main__':
    _event = {"Domain": "www.endomondo.com"}
    test = lambda_handler(_event, None)
    print (test)
