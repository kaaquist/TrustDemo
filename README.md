# TrustDemo

This is a code challenge from Trustpilot.


API developer challenge
========================================

The challenge is to make a trustscore calculator based on reviews retrieved from our APIs.
Also, implement aging into the algorithm. So, the older the review, the less it counts towards the final score.

Prerequisites:
 - You should have an API key to complete this challenge.

Set up an API in Amazon AWS using Api Gateway and AWS Lambda to do the following:

1. Make an API endpoint that takes an argument "domain"
2. This endpoint should call a Lambda function
3. The Lambda function should retrieve data from our APIs
  It should search for the domain using this endpoint:
	https://developers.trustpilot.com/business-unit-api#Find a business unit

  And when you have the ID (called businessUnitId), you should call this endpoint to get the reviews:
	https://developers.trustpilot.com/business-unit-api#Get a business unit's reviews

Use this data to do the calculator. The calculator should return an appropriate API response object.

Hints:
- You should not base the trustscore on all reviews. Only use the 300 first ratings.
- Here is the developer documentation: https://developers.trustpilot.com/
- Be RESTful.

Please send us a working endpoint URL and a copy of the Lambda code you used, along
with any other information you'd like to share about your approach.